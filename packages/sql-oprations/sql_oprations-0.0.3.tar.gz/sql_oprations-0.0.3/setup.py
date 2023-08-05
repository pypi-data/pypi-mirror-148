from setuptools import setup, find_packages
import codecs
import os

readme = open('README.md').read()

VERSION = '0.0.3'
DESCRIPTION = 'this package is use for sql CRUD operations on sql database.'
LONG_DESCRIPTION = 'A package that allows to create table, insert row into table,update rows, delete row,drop table.'

# Setting up
setup(
    name="sql_oprations",
    version=VERSION,
    author="Sachin Indoriya",
    author_email="sachinindoriya63@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=readme,
    packages=find_packages(),
    install_requires=['mysql-connector-python'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
