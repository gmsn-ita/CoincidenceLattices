import numpy as np
import sys
import clattices_loop
import re
import os

class Solution (object):
	"""
	Auxiliary class to solve the equations involving combinations of crystals.
	A solution is related to an angle and has a list of vectors (m1, m2, n1, n2)
	which are possible solutions to the coincidence lattice.
	"""
	
	def __init__ (self, angle):
		"""
		Initializes the class Solution with the angle.
		"""
		self.angle = angle
		self.solutions = []
		
class Supercell (object):
	"""
	Auxiliary class which represents a coincidence lattice. It has all necessary 
	information to describe the coincidence, such as number of atoms inside the supercell,
	the solution, the area, the constituents etc.
	"""
	
	def __init__ (self, solutions, combination):
		"""
		Initializes the class Supercell with its relevant information.
		"""
		
		self.angle = solutions.angle
		"""
		The angle which leads to the supercell.
		"""
		
		self.label_1 = combination.crystal_1.label
		self.label_2 = combination.crystal_2.label
		"""
		Label of the systems creating the supercell.
		"""
		
		self.solutions = solutions.solutions
		"""
		The pair of vectors which lead to the supercell.
		"""
		
		self.vectorScaling = self.calculateVectorScaling (solutions, combination)
		"""
		Derives the scaling of the supercell vectors relative to the first and second crystals
		"""
		
		self.vectorNorm = self.calculateVectorNorm (solutions, combination)
		"""
		Derives the absolute norm of the supercell vectors of the first and second crystals
		"""
		
		self.vectorScalingSquared = [int(round(x**2)) for x in self.vectorScaling]
		"""
		Derives the square of the scaling of the supercell vectors relative to the first and second crystals.
		Useful for the Wood notation.
		"""
		
		self.areaScaling = self.calculateRelativeArea (solutions)
		"""
		Derives the area of the supercell relative to the first and second crystals
		"""
		
		self.nAtoms = self.calculateAtoms (combination)
		"""
		Calculates the number of atoms inside the supercell
		"""
		
		self.strain = self.calculateStrain ()
		"""
		Calculates the strain necessary to form the system, according to the eq. 12
		"""
		
	def calculateRelativeArea (self, solutions):
		"""
		Calculates the relative area between the unit cell and the supercell.
		This is done basically by calculating |m x m'|, as well as |n x n'|
		"""
		
		m1 = solutions.solutions[0][0]
		m2 = solutions.solutions[0][1]
		m1_prime = solutions.solutions[1][0]
		m2_prime = solutions.solutions[1][1]
		
		n1 = solutions.solutions[0][2]
		n2 = solutions.solutions[0][3]
		n1_prime = solutions.solutions[1][2]
		n2_prime = solutions.solutions[1][3]
		
		area1 = m1*m2_prime - m1_prime*m2
		area2 = n1*n2_prime - n1_prime*n2
			
		return [area1, area2]
	
	def calculateVectorScaling (self, solutions, combination):
		"""
		Calculates the relative scaling between the unit cell vectors and the supercell vectors.
		This is done basically by calculating |m1*a1 + m2*a2|, as well as |n1*b1 + n2*b2|
		"""
		
		A = combination.crystal_1.latticeVectors
		B = combination.crystal_2.latticeVectors
		
		# Recovering the lattice vectors
		a1 = A[:,0]
		a2 = A[:,1]
		b1 = B[:,0]
		b2 = B[:,1]
		
		# Calculating the strain given the solutions (m1, m2, n1, n2) (solutions[0]) and (m1', m2', n1', n2') (solutions[1]):
		normA_1 = np.linalg.norm(a1*solutions.solutions[0][0] + a2*solutions.solutions[0][1])/np.linalg.norm(a1)
		normA_2 = np.linalg.norm(a1*solutions.solutions[1][0] + a2*solutions.solutions[1][1])/np.linalg.norm(a2)
		normB_1 = np.linalg.norm(b1*solutions.solutions[0][2] + b2*solutions.solutions[0][3])/np.linalg.norm(b1)
		normB_2 = np.linalg.norm(b1*solutions.solutions[1][2] + b2*solutions.solutions[1][3])/np.linalg.norm(b2)
			
		return [normA_1, normA_2, normB_1, normB_2]
	
	def calculateVectorNorm (self, solutions, combination):
		"""
		Calculates the absolute scaling of the supercell vectors.
		This is done basically by calculating |m1*a1 + m2*a2|, as well as |n1*b1 + n2*b2|
		"""
		
		A = combination.crystal_1.latticeVectors
		B = combination.crystal_2.latticeVectors
		
		# Recovering the lattice vectors
		a1 = A[:,0]
		a2 = A[:,1]
		b1 = B[:,0]
		b2 = B[:,1]
		
		# Calculating the strain given the solutions (m1, m2, n1, n2) (solutions[0]) and (m1', m2', n1', n2') (solutions[1]):
		normA_1 = np.linalg.norm(a1*solutions.solutions[0][0] + a2*solutions.solutions[0][1])
		normA_2 = np.linalg.norm(a1*solutions.solutions[1][0] + a2*solutions.solutions[1][1])
		normB_1 = np.linalg.norm(b1*solutions.solutions[0][2] + b2*solutions.solutions[0][3])
		normB_2 = np.linalg.norm(b1*solutions.solutions[1][2] + b2*solutions.solutions[1][3])
			
		return [normA_1, normA_2, normB_1, normB_2]
		
	
	def calculateAtoms (self, combination):
		"""
		Calculates the number of atoms inside the supercell.
		Uses the `areaScaling` variable and the information of the crystals
		passed by the `Combination` class.
		"""
		
		nAtoms1 = self.areaScaling[0] * combination.crystal_1.nAtoms
		nAtoms2 = self.areaScaling[1] * combination.crystal_2.nAtoms
		
		return nAtoms1 + nAtoms2
	
	def calculateStrain (self):
		"""
		Calculates the strain necessary to form the system, according to the eq. 12
		Two strains are listed, one for each vector. In the case of hexagonal and square systems, these strains
		will probably be equal.
		"""
		
		normA_1, normA_2, normB_1, normB_2 = self.vectorNorm
		
		strain1 = (normB_1 - normA_1)/(normB_1 + normA_1)
		strain2 = (normB_2 - normA_2)/(normB_2 + normA_2)
		
		return [strain1, strain2]
		
		
class Combination (object):
	"""
	Base class for combinations of 2D crystals.
	
	By adding to this class two different crystals already described, it is possible to find 
	coincidence lattices within the limits imposed.
	"""
	
	def __init__ (self, crystals, angles, limits):
		"""
		Initializes the class with the crystals, angles and rules for limiting the size of the supercell
		"""
		
		try:
			self.crystal_1 = crystals[0]
			self.crystal_2 = crystals[1]
			"""
			The two crystals which may form a coincidence lattice
			"""
		except IndexError:
			print ("Not enough crystals to describe the combination: two are required\n")
			sys.exit(11)
		
		try:
			self.angles = angles
			"""
			The range of angles to be investigated
			"""
		except TypeError:
			print ("No angles provided for the combination: at least one is required\n")
			sys.exit(12)
			
		try:
			self.Nmax = limits[0]
			"""
			The stopping criteria for the calculation
			"""
			self.tolerance = limits[1]
			"""
			The maximum strain allowed for determining coincidences
			"""
			self.angle_tolerance = limits[2]
			"""
			Tolerance for approximating angles for the lattice vectors
			"""
		except IndexError:
			print ("Limits not enough to calculate the combination: a list [Nmax, tolerance] is required\n")
			sys.exit(13)
			
		
			
		self.allSolutions = []
		"""
		List of all Solutions (m1, m2, n1, n2) of coincidences for the given crystals.
		"""
			
		self.supercell = []
		"""
		List to find a pair of linearly independent solutions (m1, m2, n1, n2), (m1', m2', n1', n2')
		which has minimum area.
		"""
		
		self.areaUnitCell = min (abs(np.linalg.det(self.crystal_1.latticeVectors)), abs(np.linalg.det(self.crystal_2.latticeVectors)))
		"""
		Useful information for knowing which is the minimum area allowed for the supercell.
		"""		
	
	def rotationMatrix (self, angle):
		"""
		Returns a rotation matrix M (eq. 10) for the given angle in degrees
		"""
		M = np.matrix ([[np.cos (angle*np.pi/180), np.sin (angle*np.pi/180)],
					  [-np.sin (angle*np.pi/180), np.cos (angle*np.pi/180)]])
		
		return M
		
	def findSolutions (self):		
		"""
		Solves the eq. 11 to find solutions (m1, m2, n1, n2) of coincidences for the given crystals and all angles.
		All solutions are lists of the type `[[angle_1, solutions_list], [angle_2, solutions_list], ...]`
		This method calls an extension built in C to speed the calculations, namely `clattices_loop`
		"""
		
		self.allSolutions = []
		
		# Print the lattice into a temporary file for the extension
		with open ("lattices.tmp", "w") as f:
			A = self.crystal_1.latticeVectors
			B = self.crystal_2.latticeVectors
			f.write ("%lf %lf \n%lf %lf\n" % (A.item(0,0), A.item(0,1), A.item(1,0), A.item(1,1)))
			f.write ("%lf %lf \n%lf %lf\n" % (B.item(0,0), B.item(0,1), B.item(1,0), B.item(1,1)))
			
		# Call the extension
		clattices_loop.clattices_loop (self.angles[0], self.angles[1], self.angles[2], self.Nmax, self.tolerance, self.angle_tolerance)
		
		# Read the solutions
		with open ("coincidences.tmp", 'r') as f:
			anglesBlock = [x for x in f.read().split('\n\n') if x]
			
			for x in anglesBlock:
				lines = x.split('\n')
				
				s = Solution(float (lines.pop(0)))
				for eachLine in lines:
					if eachLine:
						s.solutions.append([int (y) for y in eachLine.strip('\n').split(' ') if y])
				
				self.allSolutions.append(s)
		
		os.remove("lattices.tmp")
		os.remove("coincidences.tmp")
		
		return self.allSolutions
	
	def findMinimumArea (self):
		"""
		Finds a pair of linearly independent solutions (m1, m2, n1, n2), (m1', m2', n1', n2')
		which has minimum area. For each angle, minimizes |m x m'|. 
		"""
		
		a1 = self.crystal_1.latticeVectors[:,0]
		a2 = self.crystal_1.latticeVectors[:,1]
		
		self.supercell = []
		for s in self.allSolutions:
			
			minArea = sys.maxsize
			minAreaPair = []
			
			for i in range (len (s.solutions)):
				for j in range (i+1, len (s.solutions)):
					m1 = s.solutions[i][0]
					m2 = s.solutions[i][1]
					
					m1_prime = s.solutions[j][0]
					m2_prime = s.solutions[j][1]
					
					Am = m1*a1 + m2*a2
					Am_prime = m1_prime*a1 + m2_prime*a2
					
					area = m1*m2_prime - m1_prime*m2
					
					normAm = np.linalg.norm(Am)
					normAm_prime = np.linalg.norm(Am_prime)
					
					# To prevent rounding errors when using arcsin
					cosAngleVectors = (np.transpose(Am)*Am_prime).item(0,0)/(normAm*normAm_prime)
					if cosAngleVectors > 1:
						cosAngleVectors = 1
					elif cosAngleVectors < -1:
						cosAngleVectors = -1
						
					angleVectors = np.arccos(cosAngleVectors)*180/np.pi
					
					if self.crystal_1.bravaisLattice == "hexagonal" and self.crystal_2.bravaisLattice == "hexagonal":
						if  area >= 1 and area < minArea and abs(angleVectors - 60) < self.tolerance:
							minArea = area
							minAreaPair = [s.solutions[i], s.solutions[j]]
					elif  area >= 1 and area < minArea:
						minArea = area
						minAreaPair = [s.solutions[i], s.solutions[j]]
			
			if minAreaPair:
				minAreaSolution = Solution (s.angle)
				minAreaSolution.solutions = minAreaPair
				
				cell = Supercell (minAreaSolution, self)
				self.supercell.append (cell)
		
		return self.supercell
		
