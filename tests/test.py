import numpy as np
import ocelot.core as ocl


# atom1 = ocl.Atom(6, [0.0,0.0,0.5])
# atom2 = ocl.Atom(6, [1/3, 1/3, 0.5])
# atom3 = ocl.Atom(1, [0, 0, 0.55])
# atom4 = ocl.Atom(1, [1/3, 1/3, 0.45])
# atom_x1 = ocl.Atom(6, [0.0, 0.0, 0.0])
# atom_x2 = ocl.Atom(6, [0.0, 1.47, 0.0])
# atom5 = Atom(79, [2/3, 2/3, 0.7])
# print(atom.species)
# print(atom.coordinates)
# material = ocl.Material([atom1, atom3, atom2, atom4],
#                         lattice_constant = 2.467,
#                         bravais_vector = [[np.sqrt(3)/2, -1/2, 0.0],
#                                           [np.sqrt(3)/2, 1/2, 0.0],
#                                           [0.0, 0.0, 20.0/2.467]])

# graphene = ocl.Material([atom_x1, atom_x2],
#                         lattice_constant = 2.47,
#                         bravais_vector = [[np.sqrt(3)/2, -1/2, 0.0],
#                                           [np.sqrt(3)/2, 1/2, 0.0],
#                                           [0.0, 0.0, 20.0/2.467]],
#                         crystallographic=False)

atom1 = ocl.Atom(6, [0.86380, 1.07246, 1.16831])
atom2 = ocl.Atom(1, [0.76957, 0.07016, 1.64057])
atom3 = ocl.Atom(1, [1.93983, 1.32622, 1.04881])
atom4 = ocl.Atom(1, [0.37285, 1.83372, 1.81325])
atom5 = ocl.Atom(1, [0.37294, 1.05973, 0.17061])

methane = ocl.Molecule([atom1, atom2, atom3, atom4, atom5])

#print(material.bravais_lattice)
print(methane.to_dataframe())
print(methane.bonds())
#graphene.write_xyz()
#graphene.write_yaml()
#print(material.supercell_lattice(2*np.eye(3)))
#material.to_dataframe().to_csv("out.csv", index=False, encoding='utf-8')
#print(material.reciprocal_lattice())
