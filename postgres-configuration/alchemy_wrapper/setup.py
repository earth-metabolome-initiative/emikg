"""Module installing the alchemy wrapper package."""
from setuptools import find_packages, setup

setup(
    name='alchemy_wrapper',
    version="0.0.1",
    description='Module providing interfaces for the SQLAlchemy db.',
    author="Luca Cappelletti", # Other authors can be added here
    license='MIT',
    python_requires='>=3.8.0',
    packages=find_packages(
        exclude=['contrib', 'docs', 'tests*', 'notebooks*']),
    install_requires=["sqlalchemy", "psycopg2"],
    include_package_data=True,
)
