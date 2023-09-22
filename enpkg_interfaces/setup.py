"""Module installing the ENPKG interfaces package."""
from setuptools import find_packages, setup

setup(
    name='enpkg_interfaces',
    version="0.0.5",
    description='Module providing interfaces for the ENPKG project.',
    url='https://github.com/enpkg/enpkg',
    author="Luca Cappelletti", # Other authors can be added here
    license='MIT',
    python_requires='>=3.8.0',
    packages=find_packages(
        exclude=['contrib', 'docs', 'tests*', 'notebooks*']),
    install_requires=[],
    include_package_data=True,
)
