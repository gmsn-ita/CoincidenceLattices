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
	parser.add_argument('-q', '--quiet', action='store_true', help="do not display text on the output window (default: False)")
	
	parser.add_argument('-r', '--first', action='store_true', help="investigate only combinations with the first crystal (default: False)")
	
	return parser.parse_args()

def printRunDescription (args, crystals, combinations):
	'''
	Print description of the options chosen and the crystals input.
	'''
	
	leftJustSpace = 20
	print ("Number of crystals:".ljust(leftJustSpace) + "%d" % len(crystals))
	print ("Combinations:".ljust(leftJustSpace) +  "%d\n" % len(combinations))
	print ("N:".ljust(leftJustSpace) + "%d" % args.N)
	print ("angles:".ljust(leftJustSpace) + "from %.2f to %.2f deg" % (args.angles[0], args.angles[1]))
	print ("angles_step:".ljust(leftJustSpace) + "%.2f deg" % args.angles_step)
	print ("tolerance:".ljust(leftJustSpace) + "%2.2f" % args.tolerance)
	print ("angle_tolerance:".ljust(leftJustSpace) + "%.2f" % args.angle_tolerance)
	print ("n_atoms:".ljust(leftJustSpace) + "%d\n" % args.n_atoms)
	
	
def main():
	args = parseArgs()
	
	if not args.quiet:
		print ("***********************")
		print ("    clattices v1.0     ")
		print ("***********************")
	
	# Creates a list with the 2D crystals
	crystals = []
	for crystalFile in args.input_files:
		crystals.append (Crystal.Crystal(crystalFile))
	
	# Arguments passed by the command line
	angles = [args.angles[0], args.angles[1], args.angles_step]
	
	# Creates a list of combinations for each pair of crystals
	combinations = []
	if args.self_combinations:
		for i in range (len(crystals) if not args.first else 1):
			for j in range (i, len(crystals)):
				combinations.append (Combination.Combination([crystals[i], crystals[j]], angles, [args.N, args.tolerance, args.angle_tolerance]))
	else:
		for i in range (len(crystals) if not args.first else 1):
			for j in range (i+1, len(crystals)):
				combinations.append (Combination.Combination([crystals[i], crystals[j]], angles, [args.N, args.tolerance, args.angle_tolerance]))

	if not args.quiet:
		printRunDescription (args, crystals, combinations)
		print ("Finding coincidence lattices for the following bilayer system%s:" % ('' if len(combinations) == 1 else 's'))
	
	supercellCombinationsList = []
	# Solve all combinations
	for c in combinations:
		if not args.quiet:
			print ("%s/%s" % (c.crystal_1.label, c.crystal_2.label))
		c.findSolutions()
		supercellCombinationsList.append (c.findMinimumArea())
	
	# Print everything
	p = Printer.Printer (args.output_file, labelSpacing=args.label_size)
	nCoincidences = 0
	
	p.printMatrixNotationHeader()
	for s in supercellCombinationsList:
		nCoincidences += p.printMatrixNotation(s, args.n_atoms)
	
	if not args.quiet:
		print ("\n%d coincidence lattice%s found\n" % (nCoincidences, '' if nCoincidences == 1 else 's'))
