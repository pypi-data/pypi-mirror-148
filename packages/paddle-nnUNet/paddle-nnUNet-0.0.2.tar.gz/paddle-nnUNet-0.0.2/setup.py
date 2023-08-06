# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import setuptools
from setuptools import setup

with open('requirements.txt', 'r') as fp:
    requirements = list(filter(bool, (line.strip() for line in fp)))

with open('README.md', mode='r', encoding='utf-8') as fp:
    long_description = fp.read()

package_data = []

setup(
    name='paddle-nnUNet',

    url='https://github.com/szuboy/paddle-nnUNet#readme',
    project_urls={
        'Documentation': 'https://paddle-nnunet.readthedocs.io/',
        'Github': 'https://github.com/szuboy/paddle-nnUNet'
    },

    author='szuboy',
    author_email='szujeremy@gmail.com',

    version='0.0.2',

    packages=setuptools.find_packages(),

    package_data={'paddlennunet': package_data},

    description='nnUNet paddlepaddle version',
    long_description=long_description,
    long_description_content_type="text/markdown",

    license='Apache License',

    keywords='nnUNet paddle paddlepaddle python medical image segmentation',

    install_requires=requirements,

    python_requires='>=3.0'
)