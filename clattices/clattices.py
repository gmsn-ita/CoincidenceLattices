#!/usr/bin/env python

import argparse
import numpy as np
from . import *

def parseArgs():
	"""
	Parse arguments from the command line. Uses the `argparse` package to
	establish all positional and optional arguments.
	"""
	parser = argparse.ArgumentParser(description='Find coincidence lattices within combinations of 2D crystals.',
									epilog= "If you find this script useful, please cite J. Phys. Chem. C, 2016, 120 (20), pp 10895-10908.")

	parser.add_argument('input_files', nargs='+', help="2D crystals description files")

	parser.add_argument('-o', '--output_file', default='CoincidenceLattices.dat', help="output file for combinations table (default: CoincidenceLattices.dat file)")
	
	parser.add_argument('-a', '--angles', type=float, nargs=2, default=[0.0, 30.0], help="interval of angles (in degrees) to be investigated (default: 0 to 30 deg)", metavar=('ANGLE_MIN', 'ANGLE_MAX'))
	
	parser.add_argument('-s', '--angles_step', type=float, default=0.1, help="step for the investigation of angles (default: 0.1)")
	parser.add_argument('-f', '--self_combinations', action='store_true', help="display combinations of the 2D crystals with themselves (default: False)")
	
	parser.add_argument('-N', type=int, default=7,metavar="Nmax", help="integer cutoff for the stopping criterion (default: 7)")
	parser.add_argument('-t', '--tolerance', type=float, default=0.02, help="maximum strain to be applied to one crystal to make the system commensurate (default: 0.02)")
	
	parser.add_argument('--angle_tolerance', type=float, default=0.05, help="tolerance for approximating angles when finding coincidence lattices (default: 0.05)")
	
	parser.add_argument('-n', '--n_atoms', type=int, default=100, help="maximum number of atoms inside the supercell (default: 100 atoms)")
	
	parser.add_argument('-l', '--label_size', type=int, default=20, help="spacing of the label in the first column of the output file (default: 20 chars)")
	
	return parser.parse_args()
	
def main():
	args = parseArgs()
	
	# Creates a list with the 2D crystals
	crystals = []
	for crystalFile in args.input_files:
		crystals.append (Crystal.Crystal(crystalFile))
	
	# Arguments passed by the command line
	angles = [args.angles[0], args.angles[1], args.angles_step]
	
	# Creates a list of combinations for each pair of crystals
	combinations = []
	if args.self_combinations:
		for i in range (len(crystals)):
			for j in range (i, len(crystals)):
				combinations.append (Combination.Combination([crystals[i], crystals[j]], angles, [args.N, args.tolerance, args.angle_tolerance]))
	else:
		for i in range (len(crystals)):
			for j in range (i+1, len(crystals)):
				combinations.append (Combination.Combination([crystals[i], crystals[j]], angles, [args.N, args.tolerance, args.angle_tolerance]))

	supercellCombinationsList = []
	# Solve all combinations
	for c in combinations:
		print ("%s/%s" % (c.crystal_1.label, c.crystal_2.label))
		c.findSolutions()
		supercellCombinationsList.append (c.findMinimumArea())
	
	# Print everything
	p = Printer.Printer (args.output_file, labelSpacing=args.label_size)
	
	p.printMatrixNotationHeader()
	for s in supercellCombinationsList:
		p.printMatrixNotation(s, args.n_atoms)
