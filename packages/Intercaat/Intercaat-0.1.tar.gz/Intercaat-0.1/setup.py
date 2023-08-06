from setuptools import setup

setup(name='Intercaat',
      version='0.1',
      description='This program uses a PDB file to identify the residues present in the interface between a query chain and an interacting chain(s)',
      url='https://github.com/eved1018/Intercaat',
      author='Steve Grudman',
      author_email='steven.grudman@einsteinmed.edu',
      license='MIT',
      packages=['Intercaat'],
      zip_safe=False, 
      install_requires=[         
        'scipy',         
        'numpy',
        'pyhull'],
      entry_points = {
        'console_scripts': ['intercaat=Intercaat.intercaat:main'],
    })


