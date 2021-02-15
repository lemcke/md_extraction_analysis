import numpy as np
import warnings

def argstates(energies, sensitive=False) -> np.ndarray:
	"""
	Returns three indices indicating the left-hand energy minimum,
	barrier energy, and right-hand energy minimum of a chemical reaction.

	Input
	-----
	energies:  <array-like> of energy values
	sensitive: <bool>
	           If `True`, LHS is the last minimum before barrier
			   and RHS is the first minimum after the barrier.
			   If `False`, LHS and RHS are the absolute minima
			   on their respective sides of the barrier.
	"""
	e = np.asarray(energies)
	lhs, bar, rhs = None, None, None

	# First, warn the user if the energy array contains NaNs.
	if np.isnan(e).all():
		msg = "energy array contains only NaN, returning [None, None, None]"
		warnings.warn(msg)
		return np.asarray([lhs, bar, rhs])
	elif np.isnan(e).any():
		warnings.warn("energy array contains NaN")
	
	idx_relmax = arg_local_maxima(e)

	# If no relative maxima are found, assume global max is barrier.
	# Otherwise, assume barrier is the largest local maximum.
	if idx_relmax.size == 0:
		warnings.warn("no loc max found, assume barrier = highest energy")
		bar = np.nanargmax(e)
	else:
		e_relmax = e[idx_relmax]
		bar = idx_relmax[np.nanargmax(e_relmax)]
	
	# Now that we have the barrier, split the energy array at the barrier
	# into right-hand and left-hand sides.
	e_lhs = e[:bar + 1] # (should include barrier for finding local mins)
	e_rhs = e[bar:]

	idx_relmin_lhs = arg_local_minima(e_lhs)
	idx_relmin_rhs = arg_local_minima(e_rhs) + bar

	# For LHS and RHS, if only NaN are left, assume barrier index.
	# Otherwise, if sensitive=True, use local min/max if available.
	# Otherwise, use absolute min/max.
	# TODO: Make this more compact, DRY?
	if np.isnan(e_lhs).all():
		lhs = bar
	elif sensitive and idx_relmin_lhs.size > 0:
		lhs = idx_relmin_lhs[-1]
	else:
		lhs = np.nanargmin(e_lhs)
	
	if np.isnan(e_rhs).all():
		rhs = bar
	elif sensitive and idx_relmin_rhs.size > 0:
		rhs = idx_relmin_rhs[0]
	else:
		rhs = np.nanargmin(e_rhs) + bar
	
	return np.asarray([lhs, bar, rhs], dtype=np.uint)

# Auxiliary functions -------------------------------------------------------- #

def arg_local_minima(arr) -> np.ndarray:
	"""
	Returns array of indices of local minima in `arr`.
	Ignores NaN, only detecting local minima where the comparison
	between a value and its neighbours is unambiguous.

	Input
	-----
	arr: <array-like>
	"""
	arr = np.asarray(arr)
	return np.asarray([
		idx for idx in range(1, arr.size - 1)
		if arr[idx] < arr[idx-1] and arr[idx] < arr[idx+1]
		and not np.isnan([arr[idx-1], arr[idx], arr[idx+1]]).any()
	])

# ---------------------------------------------------------------------------- #

def arg_local_maxima(arr) -> np.ndarray:
	"""
	Returns array of indices of local maxima in `arr`.
	See `arg_local_minima`.
	"""
	arr = np.asarray(arr)
	return np.asarray([
		idx for idx in range(1, arr.size - 1)
		if arr[idx] > arr[idx-1] and arr[idx] > arr[idx+1]
		and not np.isnan([arr[idx-1], arr[idx], arr[idx+1]]).any()
	])
