import sys
import re
import numpy as np

class Crystal (object):
	"""
	Base class for all 2D crystals.
	
	Every 2D crystal must be described using a 2D Bravais lattice and an atomic basis.
	This class ignores the atomic basis and uses only the number of atoms inside the given unit cell.
	
	Each 2D crystal is described in this code as a plain text file. A simple standard file could be:
	
	Gr
	2
	Hexagonal
	2.467
	"""
	
	def __init__ (self, filename):
		"""
		Initializes the 2D crystal by associating it to the `filename` given as argument.
		Each `filename` must contain a label for the material, the number of atoms inside the unit cell,
		the Bravais lattice and the lattice parameter.
		"""
		
		self.filename = filename
		"""
		The input file which describes the 2D crystal.
		"""
		
		self.label = self.getLabel ()
		"""
		The label of the 2D crystal.
		"""
		
		self.nAtoms = self.getNatoms ()
		"""
		The number of atoms inside the 2D crystal unit cell.
		"""
		
		self.latticeVectors = self.getBravaisLattice ()
		"""
		The Bravais lattice of the 2D crystal denoted by the matrix A (or B) shown Eq. 11 of the paper.
		"""
		
	def getLabel (self):
		"""
		Reads the label of the 2D crystal given in `filename`. The label must
		be the first line in the file.
		"""
		try:
			with f as open (self.filename, 'r'):
				lines = f.readlines()
		except FileNotFoundError:
			print ("File " + self.filename + "not found! Please check the arguments!\n")
			sys.exit(1)
		
		return lines[0]
	
	def getNatoms (self):
		"""
		Reads the number of atoms inside the unit cell of the 2D crystal given in `filename`.
		This information must be the second line in the file.
		"""
		
		try:
			with f as open (self.filename, 'r'):
				lines = f.readlines()
		except FileNotFoundError:
			print ("File " + self.filename + "not found! Please check the arguments!\n")
			sys.exit(1)
		
		try:
			nAtoms = int(lines[1])
		except ValueError:
			print ("Invalid number of atoms for file " + self.filename)
			sys.exit(2)
			
		return nAtoms
	
	def getBravaisLattice (self):
		"""
		Reads the Bravais Lattice of the 2D crystal given in `filename`.
		This information must be the third and fourth line of the file.
		
		Accepted values are: Oblique, Rectangular, Hexagonal and Square (non-case sensitive).
		In each case, the fourth line must contain the following information:
		`a1 a2 angle`,
		in which `a1` and `a2` are the length of the first and second vectors (respectively) and
		`angle` is the angle in degrees between the two vectors. It is not necessary to specify the angle for Rectangular,
		Hexagonal and Square lattices. Hexagonal and Square lattices also accept only one lattice parameter `a1`
		as input.
		"""
		
		BravaisLattices = ['oblique', 'rectangular', 'hexagonal','square']
		
		try:
			with f as open (self.filename, 'r'):
				lines = f.readlines()
		except FileNotFoundError:
			print ("File " + self.filename + "not found! Please check the arguments!\n")
			sys.exit(1)
		
		latticeName = re.sub('[\n\s]', '', lines[2].lower())
		if latticeName not in BravaisLattices:
			print ("Invalid 2D Bravais lattice: " + lines[2].strip('\n') + " for file " + self.filename + "\n")
			sys.exit(4)
		else:
			try:
				# Removes whitespace when reading
				BravaisParameters = [x for x in lines[3].split().strip('\n') if x]
				# Convert the strings to float
				BravaisParameters = [float(x) for x in BravaisParameters]
			except ValueError:
				print ("Wrong entry for description of the Bravais lattice: " + lines[3].strip('\n') " for file" + self.filename + "\n")
				sys.exit(5)
			
			if not BravaisParameters:
				print ("Not enough parameters to describe the Bravais lattice for file" + self.filename + "\n")
				sys.exit(6)
				
			if latticeName == 'square':
				try:
					lattice = np.array	([[BravaisParameters[0], 0],
									 [0, BravaisParameters[0]])
				except IndexError:
					print ("Not enough parameters to describe the Bravais lattice for file" + self.filename + "\n")
					print ("Square lattices require one parameter (a) to be entirely described\n")
					sys.exit(7)
					
			else if latticeName == 'rectangular':
				try:
					lattice = np.array	([[BravaisParameters[0], 0],
										 [0, BravaisParameters[1]])
				except IndexError:
					print ("Not enough parameters to describe the Bravais lattice for file" + self.filename + "\n")
					print ("Rectangular lattices require two parameters (ax, ay) to be entirely described\n")
					sys.exit(8)
			
			else if latticeName == 'hexagonal':
				try:
					lattice = np.array	([[BravaisParameters[0], 0],
										 [BravaisParameters[0]*np.cos(np.pi/3), BravaisParameters[0]*np.sin(np.pi/3)]])
				except IndexError:
					print ("Not enough parameters to describe the Bravais lattice for file" + self.filename + "\n")
					print ("Hexagonal lattices require one parameters (a) to be entirely described\n")
					sys.exit(9)
					
			else if latticeName == 'oblique':
				try:
					lattice = np.array	([[BravaisParameters[0], 0],
										 [BravaisParameters[1]*np.cos(BravaisParameters[2]*np.pi/180), BravaisParameters[1]*np.sin(BravaisParameters[2]*np.pi/180)]])
				except IndexError:
					print ("Not enough parameters to describe the Bravais lattice for file" + self.filename + "\n")
					print ("Oblique lattices require three parameters (a1, a2, angle) to be entirely described\n")
					sys.exit(10)
		
		return lattice
		
	
	
