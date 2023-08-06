from setuptools import setup, Extension
from setuptools.command.install import install
import subprocess
import os


def compile_and_install_software():
    """Used the subprocess module to compile/install the C software."""
    command = "curl www.qhull.org/download/qhull-2020-src-8.0.2.tgz --output qhull-2020-src-8.0.2.tgz && tar -xvf qhull-2020-src-8.0.2.tgz && cd qhull-2020.2 &&  make &&  export LD_LIBRARY_PATH=$PWD/lib:$LD_LIBRARY_PATH &&  make install && cp bin/qvoronoi ../Intercaat/qhull/bin && cd .. && rm -r qhull-2020.2"
    process = subprocess.Popen(command, shell=True)

class CustomInstall(install):
    """Custom handler for the 'install' command."""
    def run(self):
        compile_and_install_software()
        super().run()

# class CustomInstall(install):
#     def run(self):
#         command = "curl www.qhull.org/download/qhull-2020-src-8.0.2.tgz --output qhull-2020-src-8.0.2.tgz && tar -xvf qhull-2020-src-8.0.2.tgz && cd qhull-2020.2 &&  make &&  export LD_LIBRARY_PATH=$PWD/lib:$LD_LIBRARY_PATH &&  make install && cp bin/qvoronoi ../Intercaat/qhull/bin && cd .. && rm -r qhull-2020.2"
#         process = subprocess.Popen(command, shell=True)
#         process.wait()
#         install.run(self)

# module = Extension('packageName.library',
#                    sources = ['packageName/library.c'],
#                    include_dirs = ['packageName/include'],
#                    extra_compile_args=['-fPIC'])


with open("README.txt", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='Intercaat',
      version="1.5",
      description='This program uses a PDB file to identify the residues present in the interface between a query chain and an interacting chain(s)',
      url='https://gitlab.com/fiserlab.org/intercaat',
      author='Steve Grudman',
      author_email='steven.grudman@einsteinmed.edu',
      license='MIT',
      packages=['Intercaat'],
      zip_safe=False, 
      include_package_data=True,
      cmdclass={'install': CustomInstall},
      install_requires=[         
        'scipy',         
        'numpy',
        'pyhull'],
    long_description=long_description,
    long_description_content_type='text/markdown',
      entry_points = {
        'console_scripts': ['intercaat=Intercaat.intercaat:main'],
    })

#python setup.py sdist
#python3 -m twine upload dist/*