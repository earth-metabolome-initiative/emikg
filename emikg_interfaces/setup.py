"""Module installing the emikg interfaces package."""
from setuptools import find_packages, setup

setup(
    name='emikg_interfaces',
    version="0.0.5",
    description='Module providing interfaces for the emikg project.',
    url='https://github.com/emikg/emikg',
    author="Luca Cappelletti", # Other authors can be added here
    license='MIT',
    python_requires='>=3.8.0',
    packages=find_packages(
        exclude=['contrib', 'docs', 'tests*', 'notebooks*']),
    install_requires=[],
    include_package_data=True,
)
