import numpy as np
from collections import namedtuple

# ---------------------------------------------------------------------------- #

def try_loadtxt(path_to_file: str) -> np.ndarray:
	"""
	Returns <numpy.ndarray> saved in `path`.
	If `path` cannot be found, NaN is returned.
	For consistency, the NaN is returned as <numpy.ndarray>.

	Input
	-----
	path_to_file: <str> file that you would like to (try to) load
	"""
	val = np.asarray(np.nan)
	try:
		val = np.loadtxt(path_to_file)
	except OSError: # file not found
		pass
	return val

# ---------------------------------------------------------------------------- #

record = namedtuple("record", "potential_energy force_max")

def path_to_record(path_to_dir: str) -> namedtuple:
	"""
	Returns <namedtuple> of data from a directory.
	Intended to be used in conjunction with the AWK scripts corresponding
	to the various simulation packages.

	Input
	-----
	path_to_dir: <str> directory that contains data (as .txt files)
	"""
	path = path.rstrip('/')
	data = {key: None for key in record._fields}

	# potential energy
	data["potential_energy"] = try_loadtxt(path + "/potential_energy.txt")

	# maximum force
	data["force_max"] = np.nanmax(try_loadtxt(path + "/force.txt"))

	# ...add more here...

	# Make record out of data and return.
	rec = record(**data)
	return rec
