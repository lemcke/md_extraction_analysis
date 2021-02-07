# Overview
This package is a collection of scripts for extracting and analysing results
from molecular dynamics (MD) simulations.

## Extraction
Extraction scripts are written on a per-package basis; there is no
generalized method for recognising output-filenames and physical parameters in
various packages.
Furthermore, scripts may extract different data from different packages,
depending on what the package does (e.g. thermal data from an MD simulation,
but not from a DFT calculation).

A few guidelines:
- filenames of the form `<package_name>/<simulation_type>/extract_<filename>`
- singular form of parameter name is preferred for consistency
  - e.g. `force.txt`, even if the file contains a Nx3 array of forces
- data saved in tabular form as `.txt` files (readable by `numpy.loadtxt`)
- British spelling is used to make us look smarter

## Analysis
The analysis scripts more or less assume the usage of the extraction scripts,
in the sense that the extracted data is simply saved as `.txt` files that can
be read by Python packages such as _pandas_ and _Numpy_.
