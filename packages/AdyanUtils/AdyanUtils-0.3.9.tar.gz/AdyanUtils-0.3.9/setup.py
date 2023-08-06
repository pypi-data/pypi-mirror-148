#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/26 11:42
# @Author  : Adyan
# @File    : setup.py


import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AdyanUtils",
    version="0.3.9",
    author="Adyan",
    author_email="228923910@qq.com",
    description="Special package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/liujiang99/AdyanUtils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests'],
    python_requires='>=3.7',
)
