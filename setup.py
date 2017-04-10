# -*- coding: utf-8 -*-

from setuptools import setup
from pip.req import parse_requirements
install_reqs = parse_requirements('./requirements.txt')
reqs = [str(ir.req) for ir in install_reqs]


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
    packages=['reconcile'],
    install_requires=reqs,
    include_package_data=True
)
