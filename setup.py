# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='reconcile',
    version='0.1.0',
    description='Distributed Systems Simulator',
    long_description=readme,
    author='Andrew Rea',
    author_email='code@andrewrea.co.uk',
    url='https://github.com/reaandrew/reconcile',
    license=license,
    packages=find_packages(exclude=('tests'))
)

