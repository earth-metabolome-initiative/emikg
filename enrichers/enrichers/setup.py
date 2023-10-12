"""Module providing the enrichers interfaces."""
from setuptools import find_packages, setup

setup(
    name='enrichers',
    version="0.0.1",
    description='Module providing the enrichers interfaces.',
    author="Luca Cappelletti", # Other authors can be added here
    license='MIT',
    python_requires='>=3.8.0',
    packages=find_packages(
        exclude=['contrib', 'docs', 'tests*', 'notebooks*']),
    install_requires=["alchemy-wrapper"],
    include_package_data=True,
)
