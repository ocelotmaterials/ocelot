import numpy as np
import ocelot as oct


atom1 = oct.Atom(6, [0.0,0.0,0.5])
atom2 = oct.Atom(6, [1/3, 1/3, 0.5])
atom3 = oct.Atom(1, [0, 0, 0.55])
atom4 = oct.Atom(1, [1/3, 1/3, 0.45])
atom_x1 = oct.Atom(6, [0.0, 0.0, 0.0])
atom_x2 = oct.Atom(6, [0.0, 1.47, 0.0])
#atom5 = Atom(79, [2/3, 2/3, 0.7])
# print(atom.species)
# print(atom.coordinates)
material = oct.Material([atom1, atom3, atom2, atom4],
                        lattice_constant = 2.467,
                        bravais_vector = [[np.sqrt(3)/2, -1/2, 0.0],
                                          [np.sqrt(3)/2, 1/2, 0.0],
                                          [0.0, 0.0, 20.0/2.467]])

graphene = oct.Material([atom_x1, atom_x2],
                        lattice_constant = 2.47,
                        bravais_vector = [[np.sqrt(3)/2, -1/2, 0.0],
                                          [np.sqrt(3)/2, 1/2, 0.0],
                                          [0.0, 0.0, 20.0/2.467]],
                        crystallographic=False)

#print(material.bravais_lattice)
material.write_xyz()
#graphene.write_xyz()
#graphene.write_yaml()
#print(material.supercell_lattice(2*np.eye(3)))
#material.to_dataframe().to_csv("out.csv", index=False, encoding='utf-8')
#print(material.reciprocal_lattice())
