from setuptools import setup, find_packages

setup(
    name='pyboletox',
    version='0.1.1',
    packages=find_packages(),
    package_data={
        'pyboletox': ['logos/*.png']
    }
)
