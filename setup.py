# -*- coding: utf-8 -*-

# ocelot

import inspect
import sys
import os

from setuptools import setup, find_packages

setup(
    name = "ocelot",
    version = "0.0.1",
    packages = find_packages(),
    author = "Leandro Seixas",
    author_email = "leandro.seixas@mackenzie.br", 
    description = """
    ocelot is an open-source library for quantum simulation
    of solids with periodic boundary conditions.
    """,

    install_requires = ['numpy >= 1.16.4',
                        'pandas >= 0.24.2',
                        'matplotlib >= 2.2.4',
                        'seaborn >= 0.9.0', 
                        'behave >= 1.2.6',
                        'qiskit >= 0.11.0',
                        'cirq >= 0.6.0'],
    license = 'Apache 2',
    python_requires = '>= 3.7.0'
)
