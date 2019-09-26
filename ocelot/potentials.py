# -*- coding: utf-8 -*-
# file: potentials.py

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

'''
  Module for bonded and nonbonded potential energies for interactions between atoms.
'''

class Potential(object):
  '''
  Potencial define a potential energy among atoms.
  '''

  def __init__(self, mesh):
    pass

  def lennard_jones(self):
    pass

  def stillinger_weber(self):
    pass

  def coulomb(self):
    pass

  def harmonic_bonds(self):
    pass

  def harmonic_angles(self):
    pass

  def harmonic_dihedral(self):
    pass

  def harmonic_improper(self):
    pass