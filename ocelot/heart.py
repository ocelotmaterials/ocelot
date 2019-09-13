# -*- coding: utf-8 -*-
# filename: heart.py

'''
  Module heart 
'''

class Atom(object):
    def __init__(self, species=0, coordinates=[0.0, 0.0, 0.0]):
        self.__species = species
        self.__coordinates = coordinates

    @property
    def species(self):
        return self.__species

    @species.setter
    def species(self, value):
        if not isinstance(value,Number):
            raise TypeError("Atomic species should be defined by their atomic number.")
        self.__species = value

# TODO @property for coordinates

class Material(Atom):
    def __init__(self, atoms, lattice_constant = 1.0, bravais_lattice):
        self.__atoms = atoms
        self.__lattice_constant = lattice_constant
        self.__bravais_lattice = bravais_lattice

# TODO @property for atoms and bravais_lattice

# testing loading
print("Module heart loaded successfully") 
