#!/usr/bin/env python
# coding:utf-8

from setuptools import find_packages, setup

setup(
name='efsm',
version='0.2.4.2',
description='> Easy and micro fsm could used in python3.x and micropython.',
long_description=open('readme.md', 'r', encoding='UTF-8').read(),
long_description_content_type = 'text/markdown',
author="Eagle'sBaby",
author_email='2229066748@qq.com',
maintainer="Eagle'sBaby",
maintainer_email='2229066748@qq.com',
packages=find_packages(),
url="https://github.com/EagleBaby/python_module-efsm",
platforms=["all"],
license='Apache Licence 2.0',
classifiers=[
'Programming Language :: Python',
'Programming Language :: Python :: 3',
],
#install_requires = ["mkr>=0.1.0", 'efr>=0.1.9'],
keywords = ["fsm", "micropython"],
python_requires='>=3', 
)