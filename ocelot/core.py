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
import yaml
import sys
from .constants import element_tuple, atomic_number, covalent_radius # comment this line to test

class Atom(object):
    '''
        Atom class, defined by chemical element (atomic number), electric charge, spin, and coordinates (numpy array).
    '''
    def __init__(self, element = 0, charge = 0.0, spin = 0.0, coordinates = np.array([0.0, 0.0, 0.0])):
        '''
        Atom object constructor.
        '''
        if ((element < 0) or (element > 118)): 
            raise Exception("Element should be defined by atomic number between 0 and 118.")
        self.__element = element
        self.__charge = charge
        self.__spin = spin
        self.__coordinates = np.array(coordinates)

    @property
    def element(self):
        return self.__element

    @element.setter
    def element(self, value):
        if not isinstance(value,int):
            raise TypeError("Atomic element should be defined by their atomic number.")
        elif ((value < 0) or (value > 118)):
            raise Exception("Atomic number must be a integer number between 0 and 118.")
        self.__element = value

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
        element = [ int(atom.element) for atom in self.atoms ]
        coordinates = [ atom.coordinates for atom in self.atoms ]

        coordinate_x = np.array(coordinates)[:,0]
        coordinate_y = np.array(coordinates)[:,1]
        coordinate_z = np.array(coordinates)[:,2]

        df = pd.DataFrame()
        df['element'] = element
        df['label'] = [element_tuple[atom] for atom in element ]
        df['x'] = coordinate_x
        df['y'] = coordinate_y
        df['z'] = coordinate_z
        df.sort_values('element', inplace = True)
        df = df.reset_index().drop(['index'], axis = 1)
        return df

    def min_coordinates(self):
        df = self.to_dataframe()
        return [df['x'].min(), df['y'].min(), df['z'].min()]

    def max_coordinates(self):
        df = self.to_dataframe()
        return [df['x'].max(), df['y'].max(), df['z'].max()]

    def save(self, filename):
        '''
        Save object
        '''
        import pickle
        with open(filename, "wb") as handle:
           pickle.dump(self, handle)

    def load(self, filename):
        '''
        Load object
        '''
        import pickle
        with open(filename, "rb") as handle:
            obj = pickle.load(handle)
        
        return obj

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
    def __init__(self, atoms = [Atom()], charge = 0.0, spin = 0.0, vacuum = 15.0, fixed = False):
        '''
        Molecule object constructor.
        '''
        self.__atoms = atoms
        self.__charge = charge
        self.__spin = spin
        self.__vacuum = vacuum
        self.__fixed = fixed

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

    @property
    def vacuum(self):
        return self.__vacuum

    @vacuum.setter
    def vacuum(self, value):
        self.__vacuum = value

    @property
    def fixed(self):
        return self.__fixed

    @fixed.setter
    def fixed(self, value):
        self.__fixed = value

    def bonds(self, tolerance = 0.1):
        '''
        Return a data frame with bonds among atoms of a molecule object.
        Use distances up to (1+tolerance)*(R_i + R_j), with R_i the covalent radius of atom i.
        '''
        bonds_topology = []
        directions = []
        df = self.to_dataframe()
        for index1, atom1 in df.iterrows():
            for index2, atom2 in df.iterrows():
                d = np.linalg.norm(atom1[['x', 'y', 'z']] - atom2[['x', 'y', 'z']])
                covalent_sum = covalent_radius[int(atom1['element'])]+covalent_radius[int(atom2['element'])]
                if (d < covalent_sum*(1+tolerance)) and (d > 0.0) and (index2 > index1):
                    bonds_topology.append([index1, index2, df['label'].iloc[index1], df['label'].iloc[index2], d])
                    directions.append((np.array(atom1[['x', 'y', 'z']], dtype=np.float32)-np.array(atom2[['x', 'y', 'z']], dtype=np.float32))/d)
        
        bonds_df = pd.DataFrame(bonds_topology, columns = ['index 1', 'index 2', 'label 1', 'label 2', 'distance'])
        bonds_df['direction'] = directions
        bonds_df.sort_values('distance', inplace = True)
        bonds_df = bonds_df.reset_index().drop(['index'], axis = 1)
        return bonds_df

    def wrong_angles(self, tolerance = 0.1):
        '''
        Return a data frame of angles between bonds of a molecule object.
        Need corrections.
        '''
        bonds_df = self.bonds(tolerance)
        label_df = self.to_dataframe()['label']
        angles = []
        indeces = []
        labels = []
        for index1, bond1 in bonds_df.iterrows():
            for index2, bond2 in bonds_df.iterrows():
                union = set(bond1[['index 1', 'index 2']]).union(set(bond2[['index 1', 'index 2']]))
                if len(union) == 3 and (index2 > index1):
                    dotproduct = np.dot(bond1['direction'], bond2['direction'])
                    normalized_dotproduct = dotproduct/(np.linalg.norm(bond1['direction'])*np.linalg.norm(bond2['direction']))
                    angle = np.arccos(np.clip(normalized_dotproduct, -1, 1))*180/np.pi
                    angles.append(angle)
                    labels.append([label_df.iloc[i] for i in list(union)])
                    indeces.append(list(union))

        df1 = pd.DataFrame(indeces, columns = ['index 1', 'index 2', 'index 3'])
        df2 = pd.DataFrame(labels, columns = ['label 1', 'label 2', 'label 3'])
        angles_df = pd.concat([df1, df2], axis = 1)
        angles_df['angle'] = angles
        return angles_df

    def angles(self, tolerance = 0.1):
        '''
        Return a data frame of angles of a molecule object.
        '''
        pass # TODO

    def dihedral_angles(self, tolerance = 0.1):
        '''
        Return a data frame of dihedral (proper) angles of a molecule object.
        '''
        pass
        # angles_df = self.angles(tolerance)
        # TODO

    def improper_angles(self):
        '''
        Return a data frame of improper torsion angles for a molecule object.
        '''
        pass # TODO

    def molecule_box(self):
        '''
        Return a array with molecule dimensions plus vacuum spacing.
        '''
        df = self.to_dataframe()
        delta_x = df['x'].max() - df['x'].min()
        delta_y = df['y'].max() - df['y'].min()
        delta_z = df['z'].max() - df['z'].min()
        return np.diag([delta_x, delta_y, delta_z])+self.vacuum*np.eye(3)

    def move(self, vector = np.array([0.0, 0.0, 0.0])):
        import copy
        new_molecule = copy.deepcopy(self)
        for atom in new_molecule.atoms:
                atom.coordinates += vector
        return new_molecule

    def rotate(self, angle = 0.0, vector = np.array([0.0, 0.0, 1.0])):
        import copy
        from scipy.spatial.transform import Rotation
        new_molecule = copy.deepcopy(self)
        rot = Rotation.from_rotvec(angle*(np.pi/180)*np.array(vector))
        # use as: new_vector = rot.apply(vector)

        # df = self.to_dataframe()
        # matrix = np.array(df[['x', 'y', 'z']])
        # new_matrix = np.matmul(matrix, rot)
        #df[['x', 'y', 'z']] = new_matrix
        #for atom in new_molecule.atoms:
        #    atom.coordinates = new_matrix[,:]
        # pass # TODO

    def join(self, molecule):
        pass # TODO

    def from_xyz(self, filename):
        '''
        Set molecule object with data from xyz file.
        Usage:
            molecule = Molecule()
            molecule.from_xyz('./molecule.xyz')
        '''
        element = []
        coordinate_x = []
        coordinate_y = []
        coordinate_z = []
        with open(filename, 'r', encoding="utf-8") as stream:
            number_of_atoms = int(stream.readline())
            comment = stream.readline()
            for index in range(number_of_atoms):
                str_atom = stream.readline()
                str_element, str_x, str_y, str_z = str_atom.split()
                element.append(atomic_number[str_element.strip()])
                coordinate_x.append(float(str_x))
                coordinate_y.append(float(str_y))
                coordinate_z.append(float(str_z))

        df = pd.DataFrame()
        df['element'] = element
        df['x'] = coordinate_x
        df['y'] = coordinate_y
        df['z'] = coordinate_z

        atoms_list = []
        for index, row in df.iterrows():
            atom = Atom(element = row['element'], coordinates = np.array(row[['x', 'y', 'z']]))
            atoms_list.append(atom)

        self.__atoms = atoms_list
        # end of from_xyz() method

    def write_xyz(self):
        '''
        Write xyz file of a Molecule object.
        '''
        
        df = self.to_dataframe()
        print(df.shape[0])
        print("  ")   
        label = [element_tuple[int(atom)] for atom in list(df['element'])]
        
        df['label'] = label
        df = df[['label', 'x', 'y', 'z']]
        for index, row in df.iterrows():
            print("{}  {:.8f}  {:.8f}  {:.8f}".format(row[0], row[1], row[2], row[3]))     
        # end of write_xyz() method

class Material(Molecule):
    '''
        Materials are defined by a list of atoms (object) and Bravais lattice vectors. 
    '''
    def __init__(self, species, lattice_constant = 1.0, bravais_vector = np.eye(3), crystallographic = True):
        '''
        Material object constructor.
        '''
        self.__species = species
        self.__lattice_constant = lattice_constant
        self.__bravais_vector = bravais_vector
        self.__crystallographic = crystallographic

    @property
    def species(self):
        return self.__species

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
        label = [element_tuple[atom] for atom in list(df['element'])]
        
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
        
        element = self.to_dataframe()['element']
        unique_atoms = Counter(element)
        print("   ", end = " ")
        for unique_atom in unique_atoms:
            print(element_tuple[unique_atom], end = " ")

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


class Operator(Planewave):
    '''
    Operator class in planewave basis
    '''
    def __init__(self):
        pass


# testing module core
if __name__ == '__main__':
    from constants import element_tuple, atomic_number, covalent_radius
    # atom1 = Atom(6, [0.86380, 1.07246, 1.16831])
    # atom2 = Atom(1, [0.76957, 0.07016, 1.64057])
    # atom3 = Atom(1, [1.93983, 1.32622, 1.04881])
    # atom4 = Atom(1, [0.37285, 1.83372, 1.81325])
    # atom5 = Atom(1, [0.37294, 1.05973, 0.17061])
    #methane = Molecule([atom1, atom2, atom3, atom4, atom5])
    #methane.write_xyz()

    # methane = Molecule()
    # methane.from_xyz("./methane.xyz")
    # print("Molecule dataframe:")
    # print(methane.to_dataframe())

    # print('\nBonds dataframe:')
    # print(methane.bonds(tolerance = 0.1))

    # print('\nAngles dataframe:')
    # print(methane.angles(tolerance = 0.1))

    #methane.angles().to_csv('angles.csv', encoding='utf-8', index=False)
    # print('\nMolecule box:')
    # print(methane.molecule_box())

    molecule = Molecule()
    molecule.from_xyz("./C150H30.xyz")
    print("Molecule dataframe")
    #molecule = molecule.load("test.obj")
    print(molecule.to_dataframe())

    #print('\nBonds dataframe:')
    #print(molecule.bonds(tolerance = 0.1))

    # print('\nAngles dataframe:')
    # print(molecule.angles(tolerance = 0.1))

