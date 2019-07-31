#!/usr/bin/env python3

from setuptools import setup, find_packages


with open('README.md', 'r') as file:
    long_description = file.read()

with open('requirements.txt') as file:
    requirements = file.read().splitlines()

version = '0.2.0'

setup(name='r2c-inputset-generator',
      version=version,
      description='Return2Corp input set generator.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://ret2.co/',
      author='Ben Fulton',
      author_email='fulton.benjamin@gmail.com',
      packages=find_packages(exclude=['tests*']),
      entry_points={
          'console_scripts': ['r2c-isg=r2c_isg.cli:cli'],
      },
      install_requires=requirements,
      python_requires='>=3.6',
      zip_safe=False)
