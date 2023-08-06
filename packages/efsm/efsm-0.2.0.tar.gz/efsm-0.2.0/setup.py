#!/usr/bin/env python
# coding:utf-8

from setuptools import find_packages, setup

setup(
name='efsm',
version='0.2.0',
description='> Easy and micro fsm could used in python3.x and micropython.\n> Copy the efsm/core.py for your micropython mpu.\n > You could link many statemachine, make them form a net. Then when you could run one sm in the net, it would auto retarget.',
author="Eagle'sBaby",
author_email='2229066748@qq.com',
maintainer="Eagle'sBaby",
maintainer_email='2229066748@qq.com',
packages=find_packages(),
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