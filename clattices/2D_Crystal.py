import sys

class 2D_Crystal (object):
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
		The Bravais lattice of the 2D crystal.
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
		a1 a2 angle,
		in which a1 and a2 are the length of the first and second vectors (respectively) and
		angle is the angle in degrees between the two vectors. It is not necessary to specify the angle for Rectangular,
		Hexagonal and Square lattices. Hexagonal and Square lattices also accept only one lattice parameter a1
		as input.
		"""
		
		BravaisLattices = {
			'oblique' : ,
			'rectangular' : ,
			'hexagonal' : ,
			'square' : ,
		}
		
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
			sys.exit(3)
			
		return nAtoms
		
	
	
