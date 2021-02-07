import pandas as pd
pd.set_option('display.max_rows', None) # tabular formatting

from ase.io import read
from ase.atom import Atom
from ase.atoms import Atoms

from bond_tools import find_bonds
from cutoffs import cutoffs_dict
from collections import namedtuple
from numpy import nan


# Define data container.
parameters = (
	'image event atom1 atom2 sym1 sym2 '
	'sep_before sep_after energy_before energy_after'
)

record = namedtuple('record', parameters)



def main():
	images = []
	records = []
	
	# Process inputs from command line.
	filenames = sys.argv[1:]
	
	for filename in filenames:
		
		contents = read(filename)
		
		if type(contents[0]) == Atom:
			images.append(contents)
		elif type(contents[0]) == Atoms:
			for image in contents:
				images.append(image)
		else:
			raise ValueError('Unrecognized input type')
	
	# Loop through all images and
	# record any changes in bond structure.
	for idx, image in enumerate(images):
		
		if idx == 0:
			bonds_prev = find_bonds(image, cutoffs_dict)
			image_prev = image
			continue

		bonds = find_bonds(image, cutoffs_dict)

		formed_bonds = bonds - bonds_prev
		broken_bonds = bonds_prev - bonds

		# Assert that intersection of both sets is empty.
		assert len(formed_bonds & broken_bonds) == 0

		# Make record for each formed or broken bond.
		for bond in formed_bonds | broken_bonds:
			d = {}
			
			d['image'] = idx
			d['event'] = 'formed' if bond in formed_bonds else 'broken'

			d['atom1'], d['atom2'] = min(bond), max(bond)
			d['sym1'], d['sym2'] = image[atom1].symbol, image[atom2].symbol

			d['sep_before'] = image_prev.get_distance(atom1, atom2, mic=True)
			d['sep_after'] = image.get_distance(atom1, atom2, mic=True)

			d['energy_before'] = try_energy(image_prev)
			d['energy_after'] = try_energy(image)

			r = record(**d)
			records.append(r)

		bonds_prev = bonds
		image_prev = image

	
	df = pd.DataFrame.from_records(records, columns=record._fields)
	print(df)

	return 0

def try_energy(atoms):
	try:
		return atoms.get_potential_energy()
	except:
		return nan


if __name__=='__main__':
	main()
