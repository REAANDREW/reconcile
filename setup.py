# -*- coding: utf-8 -*-

from setuptools import setup
from pip.req import parse_requirements
install_reqs = parse_requirements('./requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]


with open('README.md') as f:
  readme = f.read()

with open('LICENSE') as f:
  license = f.read()

setup(
    name='skeleton_python_system',
    version='0.1.0',
    description='Skeleton Python System',
    long_description=readme,
    author='Andrew Rea',
    author_email='code@andrewrea.co.uk',
    url='https://github.com/reaandrew/skeleton_python_system',
    license=license,
    packages=[],
    install_requires=reqs,
    include_package_data=True
)
