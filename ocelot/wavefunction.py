# -*- coding: utf-8 -*-
# file: wavefunction.py

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
  Module wavefunction
'''

class KGrid(Material):
    '''
        k points sample in Brillouin Zone for a Material object.
        By default, using Monkhorst-Pack algorithm [Phys. Rev. B 13, 5188 (1976)].
    '''
    def __init__(self, matrix = np.eye(3), shift = np.array([0,0,0])):
        '''
            KGrid object constructor.
        '''
        self.__matrix = matrix
        self.__shift = shift
        self.__supercell = self.bravais_lattice*self.__matrix


class Planewave(KGrid):
    '''
        Planewave class to span pediodic wave functions.
        A planewave object is defined by a list of reciprocal lattice vectors [G_1, G_2, ...].

            \psi_{nk}(r) = \sum_{G}c_{n}(k+G)exp(i(k+G).r)

    '''
    def __init__(self, energy_cutoff = 20, energy_unit = "Ha"):
        '''
            Planewave object constructor.
        '''
        self.__energy_cutoff = energy_cutoff
        self.__energy_unit = energy_unit


class Operator(Planewave):
    '''
        Operator class in planewave basis
    '''
    def __init__(self):
        pass # TODO

    def kinetic_operator(self):
        pass # TODO

    def hartree_operator(self):
        pass # TODO

    def exchange_operator(self):
        pass # TODO
