<p align="center"> <a href="https://ocelotmaterials.com/">
<img src="https://raw.githubusercontent.com/ocelotmaterials/ocelot/master/logo_horizontal.png" style="height: 90px">
</a></p>

[![PyPI - License](https://img.shields.io/pypi/l/ocelot-quantum?color=green&style=for-the-badge)](LICENSE.txt)    [![PyPI - Downloads](https://img.shields.io/pypi/dm/ocelot-quantum?style=for-the-badge)](https://pypistats.org/packages/ocelot-quantum)  [![PyPI](https://img.shields.io/pypi/v/ocelot-quantum?color=red&label=version&style=for-the-badge)](https://pypi.org/project/ocelot-quantum/)

(Under development). **Ocelot** is an open-source framework for materials simulations.

## Installation

The best way of installing ocelot is using pip:
```bash
$ python -m pip install ocelot-materials
```

For the latest cutting edge version, install with:
```bash
$ git clone https://github.com/ocelotmaterials/ocelot.git
$ cd ocelot
$ python setup.py install
```

## Getting started

```python
import numpy as np
import ocelot as ocl

# to build a methane molecule
carbon1   = ocl.Atom(element = 6, charge = 0, spin = 0, coordinates = [0.86380, 1.07246, 1.16831])
hydrogen1 = ocl.Atom(element = 1, charge = 0, spin = 0, coordinates = [0.76957, 0.07016, 1.64057])
hydrogen2 = ocl.Atom(element = 1, charge = 0, spin = 0, coordinates = [1.93983, 1.32622, 1.04881])
hydrogen3 = ocl.Atom(element = 1, charge = 0, spin = 0, coordinates = [0.37285, 1.83372, 1.81325])
hydrogen4 = ocl.Atom(element = 1, charge = 0, spin = 0, coordinates = [0.37294, 1.05973, 0.17061])

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

## License

This is an open source code under [Apache License 2.0](LICENSE.txt).
