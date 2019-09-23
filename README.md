![Image](https://github.com/ocelot-quantum/ocelot/blob/master/logo.png)

Ocelot is an open-source framework for quantum simulation of materials in quantum computers.

## Installation

```bash
pip install --user ocelot-quantum
``` 

## Getting started

```python
import numpy as np
import ocelot as oct

carbon1 = oct.Atom(6, [0.0, 0.0, 0.0])
carbon2 = oct.Atom(6, [1/3, 1/3, 0.0])

graphene = oct.Material([carbon1, carbon2],
                        lattice_constant = 2.46,
                        bravais_vector = [[np.sqrt(3)/2, -1/2, 0.0],
                                          [np.sqrt(3)/2,  1/2, 0.0],
                                          [0.0, 0.0, 20.0/2.46]])
```

## License

[Apache License 2.0](LICENSE.txt)
