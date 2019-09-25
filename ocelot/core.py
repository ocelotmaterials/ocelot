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
from abc import ABCMeta, abstractmethod
from collections import Counter
from scipy.spatial.distance import euclidean
import yaml
import sys
from .constants import element, atomic_number, covalent_radius # comment this line to test

class Atom(object):
    '''
        Atom class, defined by chemical species (atomic number), and coordinates (numpy array).
    '''
    def __init__(self, species = 0, coordinates = np.array([0.0, 0.0, 0.0])):
        '''
        Atom object constructor.
        '''
        if ((species < 0) or (species > 118)): 
            raise Exception("Species should be defined by atomic number between 0 and 118.")
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


class Chemical(Atom):
    '''
    Abstract class to build Molecule and Material classes.
    '''

    __metaclass__ = ABCMeta

    def to_dataframe(self):
        '''
        Convert a list of atoms in a pandas data frame.
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
        df.sort_values('Species', inplace = True)
        df = df.reset_index().drop(['index'], axis = 1)
        return df

    @abstractmethod
    def from_xyz(self, filename):
        pass

    @abstractmethod
    def write_xyz(self):
        pass


class Molecule(Chemical):
    '''
    Molecule is defined by a list of atoms, charge and spin. 
    '''
    def __init__(self, atoms = [Atom()], charge = 0.0, spin = 0.0, vacuum = 15.0):
        '''
        Molecule object constructor.
        '''
        self.__atoms = atoms
        self.__charge = charge
        self.__spin = spin
        self.__vacuum = vacuum

    @property
    def atoms(self):
        return self.__atoms

    @property
    def charge(self):
        return self.__charge
    
    @charge.setter
    def charge(self, value):
        self.__charge = value

    @property
    def spin(self):
        return self.__spin

    @spin.setter
    def spin(self, value):
        self.__spin = value

    def bonds(self, tolerance = 0.3):
        topo_bonds = []
        df = self.to_dataframe()
        for atom1 in self.atoms:
            for atom2 in self.atoms:
                d = euclidean(atom1.coordinates, atom2.coordinates)
                if (d < (covalent_radius[atom1.species]+covalent_radius[atom2.species])*(1+tolerance)) and d > 0.0:
                    topo_bonds.append([atom1.species, atom2.species, d])
        return topo_bonds

    def angles(self, tolerance = 0.3):
        bonds = self.bonds(tolerance)
        pass # TODO

    def dihedral(self):
        pass # TODO

    def improper(self):
        pass # TODO

    def from_xyz(self, filename):
        # filename = sys.argv[1]
        with open(filename, 'r', encoding="utf-8") as stream:
            number_of_atoms = int(stream.readline())
            comment = stream.readline()
            species = []
            coordinate_x = []
            coordinate_y = []
            coordinate_z = []
            for index in range(number_of_atoms):
                line = stream.readline()
                str_species, str_x, str_y, str_z = line.split()
                species.append(atomic_number[str_species.strip()])
                coordinate_x.append(float(str_x))
                coordinate_y.append(float(str_y))
                coordinate_z.append(float(str_z))

        df = pd.DataFrame()
        df['Species'] = species
        df['x'] = coordinate_x
        df['y'] = coordinate_y
        df['z'] = coordinate_z

        atoms_list = []
        for index, row in df.iterrows():
            atom = Atom(species = row['Species'], coordinates = np.array(row[['x', 'y', 'z']]))
            atoms_list.append(atom)

        self.__atoms = atoms_list
        # self.__vacuum = ... # resize vaccum with molecule size + 15.0

    def write_xyz(self):
        '''
        Write xyz file of a Molecule object.
        '''
        
        df = self.to_dataframe()
        print(df.shape[0])
        print("  ")   
        label = []
        for atom in list(df['Species']):
            label.append(element[int(atom)])
        
        df['label'] = label
        df = df[['label', 'x', 'y', 'z']]
        for index, row in df.iterrows():
            print("{}  {:.8f}  {:.8f}  {:.8f}".format(row[0], row[1], row[2], row[3]))     


class Material(Chemical):
    '''
        Materials are defined by a list of atoms (object) and Bravais lattice vectors. 
    '''
    def __init__(self, atoms, lattice_constant = 1.0, bravais_vector = np.eye(3), crystallographic = True):
        '''
        Material object constructor.
        '''
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

    def write_yaml(self):
        '''
        Write an ocelot Materials object as a YAML file.
        '''
        cell = self.bravais_lattice
        df = self.to_dataframe()
        
        print("cell:")
        print("-  [{:.8f},  {:.8f},  {:.8f}]".format(cell[0][0], cell[0][1], cell[0][2]))
        print("-  [{:.8f},  {:.8f},  {:.8f}]".format(cell[1][0], cell[1][1], cell[1][2]))
        print("-  [{:.8f},  {:.8f},  {:.8f}]".format(cell[2][0], cell[2][1], cell[2][2]))
        print("atoms:")
        print(df.to_string(index = True, header = False))        

    #def read_yaml(self,filename):
    #    df = pd.read_yaml(sys.argv[1])
    # TODO

    def write_xyz(self):
        '''
        Write xyz file of a Material object.
        '''
        
        df = self.to_dataframe()
        print(df.shape[0])
        print("  ")   
        label = []
        for atom in list(df['Species']):
            label.append(element[atom])
        
        df['label'] = label
        if self.crystallographic:
            atoms_xyz = np.dot(np.array(df[['x', 'y', 'z']]), self.bravais_lattice)
            df['x_cart'] = atoms_xyz[:,0]
            df['y_cart'] = atoms_xyz[:,1]
            df['z_cart'] = atoms_xyz[:,2]
            df = df[['label', 'x_cart', 'y_cart', 'z_cart']]
            for index, row in df.iterrows():
                print("{}  {:.8f}  {:.8f}  {:.8f}".format(row[0], row[1], row[2], row[3]))
        else:
            atoms_xyz = np.array(df[['x', 'y', 'z']])
            df = df[['label', 'x', 'y', 'z']]
            for index, row in df.iterrows():
                print("{}  {:.8f}  {:.8f}  {:.8f}".format(row[0], row[1], row[2], row[3]))

    def write_poscar(self):
        '''
        Write an ocelot Material object as a POSCAR file.
        '''
        bravais = self.bravais_vector
        print("POSCAR file generated by ocelot")
        print("  {:.8f}".format(self.lattice_constant))
        print("    {:.8f}  {:.8f}  {:.8f}".format(bravais[0][0], bravais[0][1], bravais[0][2]))
        print("    {:.8f}  {:.8f}  {:.8f}".format(bravais[1][0], bravais[1][1], bravais[1][2]))
        print("    {:.8f}  {:.8f}  {:.8f}".format(bravais[2][0], bravais[2][1], bravais[2][2]))
        
        species = self.to_dataframe()['Species']
        unique_atoms = Counter(species)
        print("   ", end = " ")
        for unique_atom in unique_atoms:
            print(element[unique_atom], end = " ")

        print("\n   ", end = " ")
        for unique_atom in unique_atoms:
            print(unique_atoms[unique_atom], end = "  ")

        print("\nDirect")
        if self.crystallographic:
            coordinates_block = self.to_dataframe()[['x', 'y', 'z']]
            print(coordinates_block.to_string(index = False, header = False))
        #elif:
            # TODO

    def reciprocal_lattice(self):
        return 2 * np.pi * np.linalg.inv(self.bravais_lattice).transpose()
    
    def supercell_lattice(self,matrix = np.eye(3)):
        self.__matrix = np.array(matrix)
        return self.bravais_lattice * self.__matrix


# class ReciprocalLattice(object):
# class Supercell(object):

class KGrid(Material):
    '''
    k points sample in Brillouin Zone for a Material object.
    By default, using Monkhorst-Pack algorithm [Phys. Rev. B 13, 5188 (1976)].
    '''
    def __init__(self, matrix=np.eye(3), shift=np.array([0,0,0])):
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


# testing module core
if __name__ == '__main__':
    from constants import element, atomic_number, covalent_radius
    atom1 = Atom(6, [0.86380, 1.07246, 1.16831])
    atom2 = Atom(1, [0.76957, 0.07016, 1.64057])
    atom3 = Atom(1, [1.93983, 1.32622, 1.04881])
    atom4 = Atom(1, [0.37285, 1.83372, 1.81325])
    atom5 = Atom(1, [0.37294, 1.05973, 0.17061])

    #methane = Molecule([atom1, atom2, atom3, atom4, atom5])

    #print(methane.to_dataframe())
    #methane.write_xyz()

    # test from_xyz() method
    methane = Molecule()
    methane.from_xyz("./methane.xyz")
    #methane.write_xyz()
    #print(methane.to_dataframe())
