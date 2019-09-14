# -*- coding: utf-8 -*-

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
  Module heart 
    filename: heart.py
'''

import numpy as np

class Atom(object):
    '''
        Atom class, defined by chemical species (atomic number), and coordinates (numpy array).
    '''
    def __init__(self, species=0, coordinates=np.array([0.0, 0.0, 0.0])):
        self.__species = species
        self.__coordinates = np.array(coordinates)

    @property
    def species(self):
        return self.__species

    @species.setter
    def species(self, value):
        if not isinstance(value,int):
            raise TypeError("Atomic species should be defined by their atomic number.")
        elif ((value < 1) or (value > 118)):
            raise Exception("Atomic number must be a integer number between 1 and 118.")
        self.__species = value

    @property
    def coordinates(self):
        return self.__coordinates

    @coordinates.setter
    def coordinates(self, values):
        if not (isinstance(values,list) or isinstance(values,np.ndarray)):
            raise TypeError("Coordinates should by type list or numpy array (np.ndarray).")
        elif len(values) != 3:
            raise Exception("Coordinates must be 3 values in a list or numpy array.")
        self.__coordinates = np.array(values)


class Material(Atom):
    '''
        Materials are defined by a list of atoms (object) and a Bravais lattice vector. 
    '''
    def __init__(self, atoms, lattice_constant = 1.0, bravais_vector = np.eye(3), crystallographic=True):
        self.__atoms = atoms
        self.__lattice_constant = lattice_constant
        self.__bravais_vector = bravais_vector
        self.__bravais_lattice = np.array(self.__bravais_vector) * self.__lattice_constant
        self.__crystallographic = crystallographic

    @property
    def lattice_constant(self):
        return self.__lattice_constant

    @lattice_constant.setter
    def lattice_constant(self, value):
        if not isinstance(lattice_constant, float):
            raise TypeError("Lattice constant should be a float number.")
        self.__lattice_constant = value

    @property
    def bravais_vector(self):
        return self.__bravais_vector

    @bravais_vector.setter
    def bravais_vector(self, value):
        self.__bravais_vector = value

    @property
    def bravais_lattice(self):
        return self.__bravais_lattice


    def to_xyz(self):
        if self.__crystallographic:
            print(len(self.__atoms))
            print("  ")
            for atom in self.__atoms:
                atom_xyz = np.dot(atom.coordinates,self.__bravais_lattice)
                print("{}  {:.6f}  {:.6f}  {:.6f}".format(chem[atom.species-1], atom_xyz[0], atom_xyz[1], atom_xyz[2]))

        #else:
            # to do

    #def to_poscar(self, cartesian=False):
        # to do

class KGrid(Material):
    def __init__(self, value):
        self.__diagonal = value


# Periodic table
chem = ['H ', 'He', 'Li', 'Be', 'B ', 'C ', 'N ', 'O ', 'F ', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P ', 'S ', 'Cl', 'Ar', 'K', 'Ca',
        'Sc', 'Ti', 'V ', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y ', 'Zr',
        'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I ', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd',
        'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W ', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg',
        'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U ', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm',
        'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']


if __name__ == '__main__':
    atom1 = Atom(6, [0.0,0.0,0.0])
    atom2 = Atom(6, [1/3, 1/3, 0.0])
    # print(atom.species)
    # print(atom.coordinates)
    material = Material([atom1, atom2], lattice_constant = 2.47, bravais_vector=[[np.sqrt(3)/2, -1/2, 0.0], [np.sqrt(3)/2, 1/2, 0.0], [0.0, 0.0, 20.0/2.47]])
    #print(material.bravais_lattice)
    material.to_xyz()
