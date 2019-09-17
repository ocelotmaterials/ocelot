# -*- coding: utf-8 -*-
# file: core.py

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
  Module core 
'''

import numpy as np
import pandas as pd
from collections import Counter    # importing Counter

class Atom(object):
    '''
        Atom class, defined by chemical species (atomic number), and coordinates (numpy array).
    '''
    def __init__(self, species=0, coordinates=np.array([0.0, 0.0, 0.0])):
        if ((species < 1) or (species > 118)):
            raise Exception("species should be defined by an atomic number between 1 and 118.")
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
        self.__crystallographic = crystallographic

    @property
    def atoms(self):
        return self.__atoms

    @property
    def lattice_constant(self):
        return self.__lattice_constant

    @lattice_constant.setter
    def lattice_constant(self, value):
        if not isinstance(self.__lattice_constant, float):
            raise TypeError("Lattice constant should be a float number.")
        self.__lattice_constant = value

    @property
    def bravais_vector(self):
        return self.__bravais_vector

    @bravais_vector.setter
    def bravais_vector(self, value):
        self.__bravais_vector = value

    @property
    def crystallographic(self):
        return self.__crystallographic

    @property
    def bravais_lattice(self):
        return np.array(self.__bravais_vector) * self.__lattice_constant

    def to_dataframe(self):
        '''
        Convert a list of atoms in a Material object to a pandas DataFrame.
        '''
        species = []
        for atom in self.atoms:
            species.append(atom.species)

        coordinates = []
        for atom in self.atoms:
            coordinates.append(atom.coordinates)

        coordinate_x = np.array(coordinates)[:,0]
        coordinate_y = np.array(coordinates)[:,1]
        coordinate_z = np.array(coordinates)[:,2]

        df = pd.DataFrame()
        df['Species'] = species
        df['x'] = coordinate_x
        df['y'] = coordinate_y
        df['z'] = coordinate_z
        df.sort_values('Species', inplace=True)
        df = df.reset_index().drop(['index'], axis = 1)
        return df

    #def read_yaml(self,filename):
    #    import sys
    #    df = pd.read_yaml(sys.argv[1])

    def write_simple_xyz(self): # deprecated method
        '''
        Convert an Material object to a xyz file.
        '''
        if self.crystallographic:
            print(len(self.atoms))
            print(" ")
            for atom in self.atoms:
                atom_xyz = np.dot(atom.coordinates,self.bravais_lattice)
                print("{}  {:.6f}  {:.6f}  {:.6f}".format(chem[atom.species], atom_xyz[0], atom_xyz[1], atom_xyz[2]))
        else:
            print(len(self.atoms))
            print(" ")
            for atom in self.atoms:
                print("{}  {:.6f}  {:.6f}  {:.6f}".format(chem[atom.species], atom.coordinates[0], atom.coordinates[1], atom.coordinates[2]))

    def write_xyz(self):
        
        df = self.to_dataframe()
        print(df.shape[0])
        print("  ")
            
        label = []
        for atom in list(df['Species']):
            label.append(chem[atom])
        
        df['label'] = label

        if self.crystallographic:
            atoms_xyz = np.dot(np.array(df[['x', 'y', 'z']]), self.bravais_lattice)
            
            df['x_cart'] = atoms_xyz[:,0]
            df['y_cart'] = atoms_xyz[:,1]
            df['z_cart'] = atoms_xyz[:,2]
            df = df[['label', 'x_cart', 'y_cart', 'z_cart']]
            for index, row in df.iterrows():
                print("{}  {:.8f}  {:.8f}  {:.8}".format(row[0], row[1], row[2], row[3]))
        else:
            atoms_xyz = np.array(df[['x', 'y', 'z']])
            df = df[['label', 'x', 'y', 'z']]
            for index, row in df.iterrows():
                print("{}  {:.8f}  {:.8f}  {:.8}".format(row[0], row[1], row[2], row[3]))


    def write_poscar(self):
        '''
        Convert an Material object to a POSCAR file.
        '''
        print("POSCAR file generated by ocelot")
        print("  {:.6f}".format(self.lattice_constant))
        print("    {:.12f}  {:.12f}  {:.12f}".format(self.bravais_vector[0][0], self.bravais_vector[0][1], self.bravais_vector[0][2]))
        print("    {:.12f}  {:.12f}  {:.12f}".format(self.bravais_vector[1][0], self.bravais_vector[1][1], self.bravais_vector[1][2]))
        print("    {:.12f}  {:.12f}  {:.12f}".format(self.bravais_vector[2][0], self.bravais_vector[2][1], self.bravais_vector[2][2]))
        
        species = self.to_dataframe()['Species']
        unique_atoms = Counter(species)
        print("   ", end=" ")
        for unique_atom in unique_atoms:
            print(chem[unique_atom], end=" ")

        print("\n   ", end=" ")
        for unique_atom in unique_atoms:
            print(unique_atoms[unique_atom], end="  ")

        print("\nDirect")
        if self.crystallographic:
            coordinates_block = self.to_dataframe()[['x', 'y', 'z']]
            print(coordinates_block.to_string(index=False, header=False))
        #elif:
            # to do

    def reciprocal_lattice(self):
        return 2 * np.pi * np.linalg.inv(self.bravais_lattice).transpose()
    
    def supercell_lattice(self,matrix=np.eye(3)):
        self.__matrix = np.array(matrix)
        return self.bravais_lattice * self.__matrix

class KGrid(Material):
    '''
    k points sample in Brillouin Zone for a Material object.
    By default, using Monkhorst-Pack algorithm [Phys. Rev. B 13, 5188 (1976)].
    '''
    def __init__(self, matrix=np.eye(3), shift=np.array([0,0,0])):
        self.__matrix = matrix
        self.__shift = shift


class Planewave(KGrid):
    def __init__(self, energy_cutoff = 20, energy_unit = "Ha"):
        self.__energy_cutoff = energy_cutoff
        self.__energy_unit = energy_unit


# Periodic table
chem = [' ', 'H ', 'He', 'Li', 'Be', 'B ', 'C ', 'N ', 'O ', 'F ', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P ', 'S ', 'Cl', 'Ar', 'K ', 'Ca',
             'Sc', 'Ti', 'V ', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y ', 'Zr',
             'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I ', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd',
             'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W ', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg',
             'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U ', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm',
             'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']


if __name__ == '__main__':
    atom1 = Atom(6, [0.0,0.0,0.5])
    atom2 = Atom(6, [1/3, 1/3, 0.5])
    atom3 = Atom(1, [0, 0, 0.55])
    atom4 = Atom(1, [1/3, 1/3, 0.45])
    atom_x1 = Atom(6, [0.0, 0.0, 0.0])
    atom_x2 = Atom(6, [0.0, 1.47, 0.0])
    #atom5 = Atom(79, [2/3, 2/3, 0.7])
    # print(atom.species)
    # print(atom.coordinates)
    material = Material([atom1, atom3, atom2, atom4],
                        lattice_constant = 2.467,
                        bravais_vector = [[np.sqrt(3)/2, -1/2, 0.0],
                                          [np.sqrt(3)/2, 1/2, 0.0],
                                          [0.0, 0.0, 20.0/2.467]])

    material2 = Material([atom_x1, atom_x2],
                        lattice_constant = 2.47,
                        bravais_vector = [[np.sqrt(3)/2, -1/2, 0.0],
                                          [np.sqrt(3)/2, 1/2, 0.0],
                                          [0.0, 0.0, 20.0/2.467]],
                        crystallographic=False)

    #print(material.bravais_lattice)
    #material.write_xyz()
    #material.write_xyz()
    material2.write_xyz()
    #print(material.supercell_lattice(2*np.eye(3)))
    #material.to_dataframe().to_csv("out.csv", index=False, encoding='utf-8')
    #print(material.reciprocal_lattice())
