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

from .core import Atom, Chemical, Molecule, Material

class Potential(Molecule):
    '''
    Potencial define a potential energy among atoms.
    '''

    def __init__(self, mesh):
        pass

    def lennard_jones(self):
        '''
        Lennard-Jones potential for non-bonding interactions

        V(r; epsilon, sigma) = 4\epsilon ((\sigma/r)**12 - (\sigma/r)**6)
        '''
        pass

    def reduced_lennard_jones(self):
        '''
        Truncated and shifted form of Lennard-Jones potential for non-bonding interactions, with r_c = 2.5 * \sigma (default).
        for r > 2.5 * \sigma:
            V(r) = 0
        else:
            V(r; epsilon, sigma) = 4\epsilon ((\sigma/r)**12 - (\sigma/r)**6) + constant
        '''
        pass

    def buckingham(self):
        '''
        Buckingham potential
            V(r; A, B, C) = A*exp(-B*r) - C/r**6
        '''
        pass

    def stillinger_weber(self):
        pass

    def coulomb(self):
        '''
        Coulomb potential between charged particles
            V(r; q1, q2, epsilon) = 1/(4*pi*epsilon*\epsilon_0)*(q1*q2/r)
        '''
        pass

    def morse(self):
        '''
        Morse potential
            V(r; D_e, a; r_e) = D_e*(1-exp(-a(r-r_e)))**2
        '''
        pass

    def harmonic_bonds(self):
        if self.fixed:
            pass  # do nothing if molecule is fixed
        else:
            pass  # TODO

    def harmonic_angles(self):
        if self.fixed:
            pass  # do nothing if molecule is fixed
        else:
            pass  # TODO

    def harmonic_dihedral(self):
        if self.fixed:
            pass  # do nothing if molecule is fixed
        else:
            pass  # TODO

    def harmonic_improper(self):
        if self.fixed:
            pass  # do nothing if molecule if fixed
        else:
            pass  # TODO
