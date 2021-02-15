import numpy as np
from numpy.testing import assert_array_equal
from reaction_tools import argstates
from hypothesis import given, settings, assume
from hypothesis.strategies import lists, floats
import unittest

# Unit tests ----------------------------------------------------------------- #
class TestArgstates(unittest.TestCase):
	
	# Test cases for parameter `sensitive`
	def test_non_sensitive_ignores_local_minima_closer_to_barrier(self):
		e = np.array([1, 0, 2, 1, 3, 2, 1, 2, 0])
		expect = np.array([1, 4, 8])
		got = argstates(e)
		self.assertIsNone(assert_array_equal(expect, got))
	
	def test_sensitive_detects_local_minima_closer_to_barrier(self):
		e = np.array([1, 0, 2, 1, 3, 2, 1, 2, 0])
		expect = np.array([3, 4, 6])
		got = argstates(e, sensitive=True)
		self.assertIsNone(assert_array_equal(expect, got))

if __name__ == "__main__":
	unittest.main()


# Property-based tests ------------------------------------------------------- #

@settings(max_examples=500)
@given(
	lists(
		floats(
			allow_nan = True,
			allow_infinity = False
		),
		min_size = 3
	)
)
def test_argstates_order_is_lhs_barrier_rhs(energies):
	lhs, bar, rhs = argstates(energies)
	assume(all([idx is not None for idx in (lhs, bar, rhs)]))
	assert lhs <= bar <= rhs

@settings(max_examples=500)
@given(
	lists(
		floats(
			allow_nan = True,
			allow_infinity = False
		),
		min_size = 3
	)
)
def test_argstates_barrier_has_highest_energy(energies):
	lhs, bar, rhs = argstates(energies)
	assume(all([idx is not None for idx in (lhs, bar, rhs)]))
	e_lhs, e_bar, e_rhs = energies[lhs], energies[bar], energies[rhs]
	assert e_bar >= e_lhs and e_bar >= e_rhs
