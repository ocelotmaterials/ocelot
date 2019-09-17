# -*- coding: utf-8 -*-

# ocelot

import inspect
import sys

from setuptools import setup, find_packages

with open("README.md", "r") as handle:
    long_description = handle.read()


setup(
    name = "ocelot-quantum",
    version = "0.0.1",
    packages = find_packages(),
    author = "Leandro Seixas",
    author_email = "leandro.seixas@mackenzie.br", 
    url="https://ocelot-quantum.org",
    description = "Ocelot is a framework for quantum simulation of materials in quantum computers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = ['numpy >= 1.16.4',
                        'pandas >= 0.24.2',
                        'matplotlib >= 2.2.4',
                        'seaborn >= 0.9.0', 
                        'behave >= 1.2.6',
                        'qiskit >= 0.11.0',
                        'cirq >= 0.6.0'],
    license = 'Apache 2',
    classifiers = [
         "Programming Language :: Python :: 3",
         "Topic :: Scientific/Engineering :: Chemistry",
         "Topic :: Scientific/Engineering :: Physics",
         "License :: OSI Approved :: Apache Software License",
         "Operating System :: OS Independent"
    ]
    python_requires = '>= 3.7.*'
)
