# -*- coding: utf-8 -*-
# filename: heart.py

'''
  Module heart 
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
        if ((value < 1) or (value > 118)):
            raise Exception("Atomic number must be a integer number between 1 and 118.")
        self.__species = value

    @property
    def coordinates(self):
        return self.__coordinates

    @coordinates.setter
    def coordinates(self, values):
        if not (isinstance(values,list) or isinstance(values,np.ndarray)):
            raise TypeError("Coordinates should by type list or numpy array (np.ndarray).")
        if len(values) != 3:
            raise Exception("Coordinates must be 3 values in a list or numpy array.")
        self.__coordinates = np.array(values)



class Material(Atom):
    def __init__(self, atoms, lattice_constant = 1.0, bravais_lattice = np.eye(3)):
        self.__atoms = atoms
        self.__lattice_constant = lattice_constant
        self.__bravais_lattice = bravais_lattice

# TODO @property for atoms and bravais_lattice

# testing loading
print("Module heart loaded successfully") 
