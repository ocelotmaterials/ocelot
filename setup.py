# -*- coding: utf-8 -*-
# file: setup.py

# This code is part of Ocelot.
#
# Copyright (c) 2019 Leandro Seixas Rocha.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from setuptools import setup, find_packages

with open("README.md", "r") as handle:
    long_description = handle.read()

# Read in requirements.txt
requirements = open('requirements.txt').readlines()
requirements = [r.strip() for r in requirements]

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
    install_requires = requirements,
    license = 'Apache 2',
    classifiers = [
         "Development Status :: 1 - Planning",
         "Programming Language :: Python :: 3",
         "Topic :: Scientific/Engineering :: Chemistry",
         "Topic :: Scientific/Engineering :: Physics",
         "License :: OSI Approved :: Apache Software License",
         "Operating System :: OS Independent"
    ],
    python_requires = '>= 3.7.*'
)
