import ase.io
import numpy as np
from numpy.testing import assert_allclose
import unittest


# Tests assume that ASE correctly reads OUTCAR files.
# ASE data from <Atoms> object, read from OUTCAR@-1.
# Data written using `outcar_parse.awk` is read from text files.


class TestOutcarReporter(unittest.TestCase):

	# This method runs at the beginning of the `main` function.
	# See `unittest` documentation.
	@classmethod
	def setUpClass(cls):
		print('reading `OUTCAR@-1`...')
		atoms = ase.io.read('OUTCAR@-1')
		
		cls.cell_ase = atoms.get_cell()
		cls.energy_ase = atoms.get_potential_energy()
		cls.force_ase = atoms.get_forces()
		cls.position_ase = atoms.get_positions()
		
		print('reading extractor output files')
		cls.cell = np.loadtxt('cell.txt')
		cls.energy = np.loadtxt('potential_energy.txt')
		cls.force = np.loadtxt('force.txt')
		cls.position = np.loadtxt('position.txt')

		print('setup finished successfully')
	
	def test_potential_energy(self):
		self.assertIsNone(
			assert_allclose(self.energy_ase, self.energy, atol=1.0e-7)
		)
	
	def test_cell(self):
		self.assertIsNone(
			assert_allclose(self.cell_ase, self.cell, atol=1.0e-7)
		)
	
	def test_force(self):
		self.assertIsNone(
			assert_allclose(self.force_ase, self.force, atol=1.0e-7)
		)

	def test_position(self):
		self.assertIsNone(
			assert_allclose(self.position_ase, self.position, atol=1.0e-7)
		)

if __name__=='__main__':
	unittest.main()
