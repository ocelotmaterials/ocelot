<p align="center"> <a href="https://ocelotquantum.com/">
<img src="https://raw.githubusercontent.com/ocelotquantum/ocelot/master/logo_ocelot.png" style="height: 90px">
</a></p>


[![PyPI - License](https://img.shields.io/pypi/l/ocelot-materials?color=green&style=for-the-badge)](LICENSE.txt)    [![PyPI](https://img.shields.io/pypi/v/ocelot-materials?color=red&label=version&style=for-the-badge)](https://pypi.org/project/ocelot-materials/)    [![PyPI - Downloads](https://img.shields.io/pypi/dm/ocelot-materials?style=for-the-badge)](https://pypistats.org/packages/ocelot-materials)

(Under development). **Ocelot** is an open-source framework for materials simulations.

## Installation

The best way of installing ocelot is using pip:
```bash
$ python -m pip install ocelot-quantum
```

For the latest cutting edge version, install with:
```bash
$ git clone https://github.com/ocelotquantum/ocelot.git
$ cd ocelot
$ python setup.py install
```

## Getting started

```python
import numpy as np
import ocelot as ocl

# to build a methane molecule
carbon1   = ocl.Atom(element = 6, charge = 0, spin = 0, coordinates = [0.86380, 1.07246, 1.16831])
hydrogen1 = ocl.Atom(element = 1, coordinates = [0.76957, 0.07016, 1.64057]) # default: charge = 0, spin =0
hydrogen2 = ocl.Atom(element = 1, coordinates = [1.93983, 1.32622, 1.04881])
hydrogen3 = ocl.Atom(element = 1, coordinates = [0.37285, 1.83372, 1.81325])
hydrogen4 = ocl.Atom(element = 1, coordinates = [0.37294, 1.05973, 0.17061])

methane = ocl.Molecule(atoms = [carbon1, hydrogen1, hydrogen2, hydrogen3, hydrogen4])

# to build a graphene sheet
carbon1 = ocl.Atom(element = 6, charge = 0, spin = 0, coordinates = [0.0, 0.0, 0.5])
carbon2 = ocl.Atom(element = 6, charge = 0, spin = 0, coordinates = [1/3, 1/3, 0.5])

graphene = ocl.Material(species = [carbon1, carbon2],
                        lattice_constant = 2.46,
                        bravais_vector = [[np.sqrt(3)/2, -1/2, 0.0],
                                          [np.sqrt(3)/2,  1/2, 0.0],
                                          [0.0, 0.0, 20.0/2.46]],
                        crystallographic = True)
```

A molecule object can also be created reading a *xyz* file with:
```python
molecule = ocl.Molecule()           # creating a empty Molecule object
molecule.from_xyz("./methane.xyz")  # reading xyz file
```


## How to cite

If you used ocelot quantum in your paper, please cite: (to be published)


## Contributing


## License

This is an open source code under [Apache License 2.0](LICENSE.txt).
