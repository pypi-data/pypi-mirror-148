import os
import subprocess
import shutil
import sys

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext
from setuptools.command.install import install



## Hardcode project names here
# Make sure they match the names in the pkg/module/.env file
# We can't load these names from the .env file, - `Build` installs the modules in
# setup_requires only after parsing this setup.py file.
PKG_NAME = 'cuneb-chenn'
MOD_NAME = 'cuneb'
MOD_PATH = 'src/cuneb/'



def check_for_cmake():

    CMAKE_EXE = os.environ.get('CMAKE_EXE', shutil.which('cmake'))
    if not CMAKE_EXE:
        print('cmake executable not found. '
              'Set CMAKE_EXE environment or update your path')
        sys.exit(1)

    return CMAKE_EXE

def register_env_names():

    from dotenv import load_dotenv
    load_dotenv(dotenv_path=MOD_PATH + '/.env', override=True)


class CMakeExtension(Extension):
    """
    setuptools.Extension for cmake
    """

    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

class CMakeBuildExt(build_ext):
    """
    setuptools build_ext which builds using cmake & make
    You can add cmake args with the CMAKE_COMMON_VARIABLES environment variable
    """

    def build_extension(self, ext):

        if isinstance(ext, CMakeExtension):
            CMAKE_EXE = check_for_cmake()
            register_env_names()

            output_dir = os.path.join( os.path.abspath( os.path.dirname(self.get_ext_fullpath(ext.name)) ), ext.name)

            build_type = 'Debug' if self.debug else 'Release'
            cmake_args = [CMAKE_EXE,
                          ext.sourcedir,
                          '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + output_dir,
                          '-DCMAKE_BUILD_TYPE=' + build_type]
            cmake_args.extend(
                [x for x in
                 os.environ.get('CMAKE_COMMON_VARIABLES', '').split(' ')
                 if x])

            env = os.environ.copy()
            if not os.path.exists(self.build_temp):
                os.makedirs(self.build_temp)

            subprocess.check_call(cmake_args,
                                  cwd=self.build_temp,
                                  env=env)
            subprocess.check_call(['make', '-j'+str(os.cpu_count() // 2), ext.name],
                                  cwd=self.build_temp,
                                  env=env)
            print()
        else:
            super().build_extension(ext)

class CustomInstall(install):

    def run(self):
        install.run(self)


def get_readme():
    with open('README.md') as f:
        return f.read()

setup(
    name=PKG_NAME,
    version='0.0.3',
    description='A simple package to wrap a pytorch CUDA/C++ extension',
    url='https://github.com/chrishenn/cuneb-chenn',
    author='Chris Henn',
    author_email='chenn@alum.mit.edu',
    license='MIT',
    long_description=get_readme(),
    long_description_content_type="text/markdown",

    packages=[MOD_NAME],
    package_dir = {MOD_NAME: MOD_PATH},

    ext_modules=[CMakeExtension(MOD_NAME, sourcedir=MOD_PATH)],
    cmdclass={
        'install': CustomInstall,
        'build_ext': CMakeBuildExt,
    },
    package_data={MOD_NAME : [".env", "CMakeLists.txt", "*.cpp", "*.cu", "*.cuh", "*.h", "*.so"]},

    setup_requires = [
        "setuptools>=42",
        "wheel",
        "torch>=1.8.2",
        "python-dotenv",
        'importlib-metadata; python_version >= "3.6"'
    ],
    install_requires = [
        "torch>=1.8.2",
        "python-dotenv",
        'importlib-metadata; python_version >= "3.6"'
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: GPU :: NVIDIA CUDA',
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)




