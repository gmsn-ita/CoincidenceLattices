#!/usr/bin/env python

import argparse
from . import *

def parseArgs():
	"""
	Parse arguments from the command line. Uses the `argparse` package to
	establish all positional and optional arguments.
	"""
	parser = argparse.ArgumentParser(description='Find coincidence lattices within combinations of 2D crystals.',
									epilog= "If you find this script useful, please cite J. Phys. Chem. C, 2016, 120 (20), pp 10895-10908.")

	parser.add_argument('input_files', type=argparse.FileType('r'), nargs='+', help="2D crystals description files")
	parser.add_argument('-o', '--output', type=argparse.FileType('w'), default='CoincidenceLattices.dat', nargs=1, help="output file for combinations table (default: CoincidenceLattices.dat file)")
	
	parser.add_argument('-a', '--angles', type=float, nargs=2, default=[0.0, 30.0], help="interval of angles (in degrees) to be investigated (default: 0 to 30 deg)", metavar=('ANGLE_MIN', 'ANGLE_MAX'))
	
	parser.add_argument('-s', '--angles-step', type=float, nargs=1, default=0.1, help="step for the investigation of angles (default: 0.1)")
	parser.add_argument('-f', '--self-combinations', action='store_false', help="display combinations of the 2D crystals with themselves (default: False)")
	
	parser.add_argument('-N', type=int, default=7,metavar="Nmax", help="integer cutoff for the stopping criterion (default: 7)")
	parser.add_argument('-t', '--tolerance', type=float, default=0.02, help="maximum strain to be applied to one crystal to make the system commensurate (default: 0.02)")
	parser.add_argument('-n', '--n-atoms', type=int, default=100, help="maximum number of atoms inside the supercell (default: 100 atoms)")
	
	return parser.parse_args()
	
def main():
	args = parseArgs()

