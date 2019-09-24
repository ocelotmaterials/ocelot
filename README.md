<p align="center"> <a href="https://ocelot-quantum.org/">
<img src="https://raw.githubusercontent.com/ocelot-quantum/ocelot/master/logo.png" style="height: 100px">
</a></p>

[![PyPI - License](https://img.shields.io/pypi/l/ocelot-quantum?color=brightgreen&style=for-the-badge)](LICENSE.txt)    ![PyPI - Downloads](https://img.shields.io/pypi/dm/ocelot-quantum?style=for-the-badge)  [![PyPI](https://img.shields.io/pypi/v/ocelot-quantum?style=for-the-badge)](https://pypi.org/project/ocelot-quantum/)

(Under development). **Ocelot** is an open-source framework for quantum simulation of materials in quantum computers.

## Installation

The best way of installing ocelot is using pip:
```bash
$ pip install ocelot-quantum
```

For the latest cutting edge version, install with:
```bash
$ git clone https://github.com/ocelot-quantum/ocelot.git
$ cd ocelot
$ python setup.py install
```

## Getting started

```python
import numpy as np
import ocelot as ocl

carbon1 = ocl.Atom(6, [0.0, 0.0, 0.5])
carbon2 = ocl.Atom(6, [1/3, 1/3, 0.5])

graphene = ocl.Material([carbon1, carbon2],
                        lattice_constant = 2.46,
                        bravais_vector = [[np.sqrt(3)/2, -1/2, 0.0],
                                          [np.sqrt(3)/2,  1/2, 0.0],
                                          [0.0, 0.0, 20.0/2.46]])
```

## License
This is an open source code under Apache license 2.0

[Apache License 2.0](LICENSE.txt)
