#!/usr/bin/env python
# coding:utf-8

from setuptools import find_packages, setup

setup(
name='efsm',
version='0.2.4.7',
description='> Easy and micro fsm could used in python3.x and micropython.',
packages=find_packages(),
platforms=["all"],
license='Apache Licence 2.0',
classifiers=[
'Programming Language :: Python',
'Programming Language :: Python :: 3',
],
# install_requires = ["numpy", "keras==2.3"],
keywords = ["AI", "micropython"],
python_requires='>=3', 
)