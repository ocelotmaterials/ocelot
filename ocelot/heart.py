'''
  Module heart 
'''

class Atom:
    def __init__(self, species=0, coordinates=[0.0, 0.0, 0.0]):
        self._species = species
        self._coordinates = coordinates

    @property
    def species(self):
        return self._species

    @species.setter
    def species(self, value):
        if not isinstance(value,Number):
            raise TypeError("Atomic species should be defined by their atomic number.")
        self._species = value


# testing loading
print("Module heart loaded successfully") 
