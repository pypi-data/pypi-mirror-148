#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/5/1 16:15
# @Author : lixinpan
# @Site : 
# @File : set_up.py
# @function:

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ghost_pkg_io",
    version="0.0.2",
    author="ghost",
    author_email="xinpan_li@163.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ghostMozi/ghost_pypi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)