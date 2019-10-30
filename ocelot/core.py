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

from abc import ABCMeta, abstractmethod
from collections import Counter
from copy import deepcopy
from pickle import dump, load
from sys import argv
from scipy.spatial.transform import Rotation
import numpy as np
import pandas as pd
from .constants import element_list, atomic_number, covalent_radius  # comment this line to test


class Atom(object):
    '''
    Atom class, defined by chemical element (atomic number), charge, spin,
    and coordinates (numpy array).

    Example 1:
        To initialize a carbon atom (atomic number = 6) at coordinates = (1.0, 3.0, 5.0), use:
        carbon1 = Atom(element = 6, coordinates = [1.0, 3.0, 5.0])

        Aditional attributes of atom objects are charge (by default = 0), and spin (by default = 0).

    Example 2:
        To initialize a chloride anion (charge = -1.0), at coordinates = (0.0, 0.0, 3.14), use:
        chloride1 = Atom(element = 17, charge = -1.0, spin = 0.0, coordinates = [0.0, 0.0, 3.14])
    '''
    def __init__(self, element=0, charge=0.0, spin=0.0, coordinates=np.array([0.0, 0.0, 0.0])):
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
        if not isinstance(value, int):
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
        if not (isinstance(values, list) or isinstance(values, np.ndarray)):
            raise TypeError("Coordinates should by type list or numpy array (np.ndarray).")
        elif len(values) != 3:
            raise Exception("Coordinates must be 3 values in a list or numpy array.")
        self.__coordinates = np.array(values)


class Chemical(Atom):
    '''
        Abstract class to build both Molecule and Material classes.
    '''

    __metaclass__ = ABCMeta

    def to_dataframe(self):
        '''
            Convert a list of atoms in a pandas dataframe.
        '''
        elements = [int(atom.element) for atom in self.atoms]
        coordinates = [atom.coordinates for atom in self.atoms]

        coordinate_x = np.array(coordinates)[:, 0]
        coordinate_y = np.array(coordinates)[:, 1]
        coordinate_z = np.array(coordinates)[:, 2]

        df = pd.DataFrame()
        df['element'] = elements
        df['label'] = [element_list[atom] for atom in elements]
        df['x'] = coordinate_x
        df['y'] = coordinate_y
        df['z'] = coordinate_z
        df.sort_values('element', inplace=True)
        df = df.reset_index().drop(['index'], axis=1)
        return df

    def min_coordinates(self):
        df = self.to_dataframe()
        return [df['x'].min(), df['y'].min(), df['z'].min()]

    def max_coordinates(self):
        df = self.to_dataframe()
        return [df['x'].max(), df['y'].max(), df['z'].max()]

    def move(self, vector=np.array([0.0, 0.0, 0.0])):
        '''
            Return a new object shifted by a constant vector.
        '''
        new_obj = deepcopy(self)
        for atom in new_obj.atoms:
            atom.coordinates += vector
        return new_obj

    def rotate(self, seq='z', angles=0.0, degrees=True):
        '''
            Return a new object rotated by Euler matrices with sequence "seq", and angles "angles".
        '''
        new_obj = deepcopy(self)
        R = Rotation.from_euler(seq, angles, degrees)
        for atom in new_obj.atoms:
            atom.coordinates = R.apply(atom.coordinates)
        return new_obj

    def save(self, filename):
        '''
            Save object with pickle.
        '''
        with open(filename, "wb") as handle:
            dump(self, handle)

    def load(self, filename):
        '''
            Load object with pickle.
        '''
        with open(filename, "rb") as handle:
            obj = load(handle)

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
    def __init__(self, atoms=[Atom()], charge=None, spin=None, vacuum=15.0, fixed=False):
        '''
            Molecule object constructor.
        '''
        self.__atoms = atoms
        self.__vacuum = vacuum
        self.__fixed = fixed
        if charge is None:
            self.__charge = sum([atom.charge for atom in self.__atoms])
        else:
            self.__charge = charge
        if spin is None:
            self.__spin = sum([atom.spin for atom in self.__atoms])
        else:
            self.__spin = spin

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

    def bonds(self, tolerance=0.2):
        '''
            Return a dataframe with bonds among atoms of a molecule object.
            Use distances up to (1+tolerance)*(R_i + R_j), with R_i the covalent radius of atom i.
        '''
        bonds_topology = []
        directions = []
        df = self.to_dataframe()

        for index1, atom1 in df.iterrows():
            for index2, atom2 in df.iterrows():
                d = np.linalg.norm(atom1[['x', 'y', 'z']] - atom2[['x', 'y', 'z']])
                covalent_sum = covalent_radius[int(atom1['element'])] + covalent_radius[int(atom2['element'])]
                if (d < covalent_sum*(1+tolerance)) and (d > 0.0) and (index2 > index1):
                    bonds_topology.append([
                        index1,
                        index2,
                        df['label'].iloc[index1],
                        df['label'].iloc[index2],
                        d])
                    directions.append(
                        (np.array(atom1[['x', 'y', 'z']], dtype=np.float32)
                        - np.array(atom2[['x', 'y', 'z']], dtype=np.float32))/d)

        bonds_df = pd.DataFrame(bonds_topology, columns=[
            'index 1',
            'index 2',
            'label 1',
            'label 2',
            'distance'])
        bonds_df['direction'] = directions
        bonds_df.sort_values('distance', inplace=True)
        bonds_df = bonds_df.reset_index().drop(['index'], axis=1)
        return bonds_df
        # end of bonds() method

    def nearest_neighbors_list(self, bonds=None):
        '''
            From each atom in the molecule object, return a list with nearest neighbors (atom) indeces.
        '''
        if bonds:
            bonds_df = bonds
        else:
            bonds_df = self.bonds()

        number_of_atoms = self.to_dataframe().shape[0]
        nn_list = []
        for atom_index in range(number_of_atoms):
            nn_atom = []
            for index, bond in bonds_df.iterrows():
                if atom_index == bond['index 1']:
                    nn_atom.append(bond['index 2'])
                elif atom_index == bond['index 2']:
                    nn_atom.append(bond['index 1'])

            nn_list.append(nn_atom)
        return nn_list
        # end of nearest_neighbors_list() method

    def nearest_neighbors_matrix(self, bonds=None):
        '''
            Return a N*N matrix (dataframe) with N = number of atoms.
            The matrix element [i][j] is the bond distance if i and j are nearest neighbors,
            and 0 otherwise.
        '''
        if bonds:
            bonds_df = bonds
        else:
            bonds_df = self.bonds()

        number_of_atoms = self.to_dataframe().shape[0]
        nn_matrix = np.zeros([number_of_atoms, number_of_atoms])
        for index, bond in bonds_df.iterrows():
            nn_matrix[bond['index 1']][bond['index 2']] = bond['distance']

        return pd.DataFrame(nn_matrix)
        # end of nearest_neighbors_matrix() method

    def angles(self, tolerance=0.2):
        '''
            Return a dataframe of angles of a molecule object.
        '''
        bonds_df = self.bonds(tolerance=tolerance)
        df = self.to_dataframe()

        number_of_atoms = df.shape[0]
        nn_list = []

        for atom_index in range(number_of_atoms):
            nn_atom = []
            for index, bond in bonds_df.iterrows():
                if atom_index == bond['index 1']:
                    nn_atom.append([bond['index 2'], np.array(bond['direction'])])
                elif atom_index == bond['index 2']:
                    nn_atom.append([bond['index 1'], -1*np.array(bond['direction'])])
            nn_list.append(nn_atom)

        nn_df = pd.DataFrame(nn_list)

        angles = []
        for ref_atom, bonds in nn_df.iterrows():
            new_bonds = bonds[bonds.notnull()]
            if len(new_bonds) > 2:
                for neighbor1 in new_bonds:
                    for neighbor2 in new_bonds:
                        if (neighbor1[0] > neighbor2[0]):
                            dot = np.dot(neighbor1[1], neighbor2[1])
                            cross = np.cross(neighbor1[1], neighbor2[1])
                            angle = np.arccos(np.clip(-1, 1, dot))
                            angles.append([
                                ref_atom,
                                neighbor1[0],
                                neighbor2[0],
                                df['label'].iloc[ref_atom],
                                df['label'].iloc[neighbor1[0]],
                                df['label'].iloc[neighbor2[0]],
                                angle*180/np.pi,
                                cross/np.linalg.norm(cross)])

        angles_df = pd.DataFrame(angles, columns=[
            'index 1',
            'index 2',
            'index 3',
            'label 1',
            'label 2',
            'label 3',
            'angle',
            'normal'])
        return angles_df
        # end of angles() method

    def dihedral_angles(self, tolerance=0.2):
        '''
            Return a dataframe of dihedral (proper) angles of a molecule object.
        '''
        angles_df = self.angles(tolerance)
        df = self.to_dataframe()
        # for index1, angle1 in angles_df.iterrows():
        #     for index2, angle2 in angles_df.iterrows():
        # angle1['normal'] * angle2['normal']

        # TODO

    def improper_angles(self, tolerance=0.2):
        '''
            Return a data frame of improper torsion angles for a molecule object.
        '''
        pass  # TODO

    def sizes(self):
        '''
            Return a array with molecule dimensions.
        '''
        df = self.to_dataframe()
        delta_x = df['x'].max() - df['x'].min()
        delta_y = df['y'].max() - df['y'].min()
        delta_z = df['z'].max() - df['z'].min()
        return [delta_x, delta_y, delta_z]

    def molecule_box(self):
        '''
            Return a matrix with molecule dimensions plus vacuum spacing.
        '''
        return np.diag(self.sizes()) + self.vacuum*np.eye(3)

    def get_center(self):
        '''
            Return a vector with the center of the molecule coordinates.
        '''
        signs = self.min_coordinates()/(np.abs(self.min_coordinates()))
        half_size = np.array(self.sizes())/2
        return [half_size[x] - signs[x]*self.min_coordinates()[x] for x in range(3)]

    def join(self, molecule):
        for atom in molecule.atoms:
            self.atoms.append(atom)

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
            atom = Atom(
                element=row['element'],
                coordinates=np.array(row[['x', 'y', 'z']]))
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
        label = [element_list[int(atom)] for atom in list(df['element'])]

        df['label'] = label
        df = df[['label', 'x', 'y', 'z']]
        for index, row in df.iterrows():
            print("{}  {:.8f}  {:.8f}  {:.8f}".format(row[0], row[1], row[2], row[3]))     
        # end of write_xyz() method


class Material(Chemical):
    '''
        Materials are defined by a list of atoms (object) and Bravais lattice vectors. 
    '''
    def __init__(self, atoms, lattice_constant=1.0, bravais_vector=np.eye(3), crystallographic=True):
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

    def from_molecule(self, molecule):
        pass  # TODO

    def from_xyz(self, filename):
        pass  # TODO

    def from_poscar(self, filename):
        pass  # TODO

    def write_xyz(self):
        '''
            Write xyz file of a Material object.
        '''
        df = self.to_dataframe()
        print(df.shape[0])
        print("  ")   
        label = [element_list[atom] for atom in list(df['element'])]

        df['label'] = label
        if self.crystallographic:
            atoms_xyz = np.matmul(np.array(df[['x', 'y', 'z']]), self.bravais_lattice.transpose())
            df['x_cart'] = atoms_xyz[:, 0]
            df['y_cart'] = atoms_xyz[:, 1]
            df['z_cart'] = atoms_xyz[:, 2]
            df = df[['label', 'x_cart', 'y_cart', 'z_cart']]
            for index, row in df.iterrows():
                print("{}  {:.8f}  {:.8f}  {:.8f}".format(row[0], row[1], row[2], row[3]))
        else:
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
        print("   ", end=" ")
        for unique_atom in unique_atoms:
            print(element_list[unique_atom], end=" ")

        print("\n   ", end=" ")
        for unique_atom in unique_atoms:
            print(unique_atoms[unique_atom], end="  ")

        print("\nDirect")
        if self.crystallographic:
            coordinates_block = self.to_dataframe()[['x', 'y', 'z']]
            print(coordinates_block.to_string(index=False, header=False))
        else:
            coordinates_xyz = np.array(self.to_dataframe()[['x', 'y', 'z']])
            # REFACTORING
            coordinates_crystal = np.matmul(coordinates_xyz, np.linalg.inv(self.bravais_lattice))
            coordinates_df = pd.DataFrame(coordinates_crystal)
            print(coordinates_df.to_string(index=False, header=False))

    def reciprocal_lattice(self):
        return 2 * np.pi * np.linalg.inv(self.bravais_lattice).transpose()

    def supercell_lattice(self, matrix=np.eye(3)):
        self.__matrix = np.array(matrix)
        return self.bravais_lattice * self.__matrix


# testing module core
if __name__ == '__main__':
    from constants import element_list, atomic_number, covalent_radius
    # atom1 = Atom(element = 6, charge =  1.00, coordinates = [0.86380, 1.07246, 1.16831])
    # atom2 = Atom(element = 1, charge = -0.25, coordinates = [0.76957, 0.07016, 1.64057])
    # atom3 = Atom(element = 1, charge = -0.25, coordinates = [1.93983, 1.32622, 1.04881])
    # atom4 = Atom(element = 1, charge = -0.25, coordinates = [0.37285, 1.83372, 1.81325])
    # atom5 = Atom(element = 1, charge = -0.25, coordinates = [0.37294, 1.05973, 0.17061])
    # methane = Molecule(atoms = [atom1, atom2, atom3, atom4, atom5])
    # print(methane.charge)
    # methane.write_xyz()

    # carbon1 = Atom(element = 6, charge = 0, spin = 0, coordinates = [0.0, 0.00000, 10.0])
    # carbon2 = Atom(element = 6, charge = 0, spin = 0, coordinates = [1.42028, 0.0000, 10.0])
    # graphene = Material(atoms = [carbon1, carbon2],
    #                     lattice_constant = 2.46,
    #                     bravais_vector = [[np.sqrt(3)/2, -1/2, 0.0],
    #                                       [np.sqrt(3)/2,  1/2, 0.0],
    #                                       [0.0, 0.0, 20.0/2.46]],
    #                     crystallographic = False)
    # graphene.write_poscar()
    # print(graphene.to_dataframe())

    filename = argv[1]
    molecule = Molecule()
    molecule.from_xyz(filename)
    # print(molecule.min_coordinates())
    # molecule2= molecule.move([6.19524, -0.5353, 1.68151])
    # molecule2.write_xyz()
    # print("Molecule center:")
    # print(molecule.get_center())
    print("Molecule dataframe:")
    print(molecule.to_dataframe())
    # molecule.write_xyz()

    # print("Molecule bonds:")
    # print(molecule.bonds())

    # print("Molecule angles:")
    # print(molecule.angles())

    # mol2 = molecule.rotate('z', angles = 90).move([0.0, 0.0, 5.0])
    # mol2.write_xyz()
    # molecule.join(mol2)

    # molecule.write_xyz()

    # print('\nBonds dataframe:')
    # print(molecule.bonds(tolerance = 0.1))

    # print("\nNearest neighbors list:")
    # print(molecule.nearest_neighbors_list())

    # print('\nAngles dataframe:')
    # print(methane.angles(tolerance = 0.1))

    # methane.angles().to_csv('angles.csv', encoding='utf-8', index=False)
    # print('\nMolecule box:')
    # print(methane.molecule_box())

    # molecule = Molecule()
    # molecule.from_xyz("./C150H30.xyz")
    # print("Molecule dataframe")
    # molecule = molecule.load("test.obj")
    # print(molecule.to_dataframe())

    # print('\nBonds dataframe:')
    # print(molecule.bonds(tolerance = 0.1))

    # print('\nAngles dataframe:')
    # print(molecule.angles(tolerance = 0.1))
