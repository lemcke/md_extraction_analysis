#!/usr/bin/awk -f

# ------------------------------------------------------------------------ #
# Reads VASP OUTCAR file and writes data to parameter-specific text files. |
# Currently supports:                                                      |
#  - cell dims   -> 3x3 array of cell vectors    ("cell.txt")              |
#  - positions   -> Nx3 array of ionic positions ("position.txt")          |
#  - forces      -> Nx3 array of ionic forces    ("force.txt")             |
#  - pot. energy -> last PE value                ("potential_energy.txt")  |
#  - convergence -> 1 (true) or 0 (false)        ("converge.txt")          |
# ------------------------------------------------------------------------ #

BEGIN {
	OFS = "\t"  # output field separator

	# Initialize variables.
	potential_energy = "nan"
	converge = 0

	for (i = 0; i < 3; i++)
		for (j = 0; j < 3; j++)
			cell[i,j] = "nan"
}

# Get cell dimensions.
# /^[[:space:]]+direct lattice vectors/ {
$1 == "direct" && $2 == "lattice" {
	for (i = 0; i < 3; i++) {
		getline
		cell[i,0] = $1
		cell[i,1] = $2
		cell[i,2] = $3
	}
	next
}

# Get potential energy.
# /^[[:space:]]+energy[[:space:]]+without/ {
$1 == "energy" && $2 == "without" {
	potential_energy = $NF
	next
}

# Get positions of and forces on atoms.
$1 == "POSITION" && $2 == "TOTAL-FORCE" {
	getline  # skip section header line
	getline  # skip dashed section line
	idx = 0
	# while (!/^[[:space:]]+--/) {
	while ($1 !~ /--/) {
		pos[idx,0] = $1
		pos[idx,1] = $2
		pos[idx,2] = $3
		frc[idx,0] = $4
		frc[idx,1] = $5
		frc[idx,2] = $6
		idx += 1  # `idx` also doubles as "number of atoms"
		getline
	}
	next
}

# Check for convergence.
# /^[[:space:]]+reached[[:space:]]+required[[:space:]]+accuracy/ {
$1 == "reached" && $2 == "required" {
	converge = 1
}

END {
	# ---- Write all output files. ---- #
	print potential_energy > "potential_energy.txt"
	print converge > "converge.txt"
	print_m3_array(cell, 3, "cell.txt")
	print_m3_array(frc, idx, "force.txt")
	print_m3_array(pos, idx, "position.txt")
}

function print_m3_array(arr, m, out) {
	# Print an Mx3 array to an output file.
	printf "% f%s% f%s% f\n", arr[0,0], OFS, arr[0,1], OFS, arr[0,2] > out
	for (i=1; i < m; i++) {
		printf "% f%s% f%s% f\n", arr[i,0], OFS, arr[i,1], OFS, arr[i,2] > out
	}
	return 0
}
