from distutils.core import setup
from distutils.command.install_data import install_data

try:
    from post_setup import main as post_install
except ImportError:
    post_install = lambda: None

class my_install(install_data):
    def run(self):
        install_data.run(self)
        post_install()

if __name__ == '__main__':
    with open("README.txt", "r", encoding="utf-8") as fh:
        long_description = fh.read()
    setup(name='Intercaat',
        version="1.7",
        description='This program uses a PDB file to identify the residues present in the interface between a query chain and an interacting chain(s)',
        url='https://gitlab.com/fiserlab.org/intercaat',
        author='Steve Grudman',
        author_email='steven.grudman@einsteinmed.edu',
        license='MIT',
        packages=['Intercaat'],
        zip_safe=False, 
        include_package_data=True,
        cmdclass={'install_data': my_install},
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