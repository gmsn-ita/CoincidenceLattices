import numpy as np
import sys

class Solution (object):
	"""
	Helping class to solve the equations involving combinations of crystals.
	A solution is related to an angle and has a list of vectors (m1, m2, n1, n2)
	which are possible solutions to the coincidence lattice.
	"""
	
	def __init__ (self, angle):
		"""
		Initializes the class Solution with the angle.
		"""
		self.angle = angle
		self.solutions = []
		
	
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
			self.tolerance = limits[1]
			"""
			The stopping criteria for the calculation
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
		
		self.areaUnitCell = min (abs(np.linalg.det(crystal1.latticeVectors), abs(np.linalg.det(crystal2.latticeVectors))
		"""
		Only coincidence lattices with area equal or greater to the area of the unit cell are allowed.
		This is required to calculate the supercell which has minimum area.
		"""
	
	def rotationMatrix (self, angle):
		"""
		Returns a rotation matrix M (eq. 10) for the given angle in degrees
		"""
		M = np.array ([[np.cos (angle*np.pi/180), np.sin (angle*np.pi/180)],
					  [-np.sin (angle*np.pi/180), np.cos (angle*np.pi/180)]])
		
		return M
		
	def findSolutionsAngle (self, angle):
		"""
		Solves the eq. 11 to find all solutions (m1, m2, n1, n2) of coincidences for the given crystals and a specific angle.
		All solutions (vectors in Z^4) are appended to a list and are used later.
		A big loop is used to compute every possibility.
		"""
		
		s = Solution (angle)

		for m1 in range (-self.Nmax, self.Nmax):
			for m2 in range (-self.Nmax, self.Nmax):
				for n1 in range (-self.Nmax, self.Nmax):
					for n2 in range (-self.Nmax, self.Nmax):
						coincidence = crystal_1.latticeVectors*np.array([[m1],[m2]]) - rotationMatrix(angle)*crystal_2.latticeVectors*np.array([[n1],[n2]])
						
						# The condition is satisfied
						if np.linalg.norm (coincidence) <= self.tolerance:
							s.solutions.append ([m1,m2,n1,n2])
		
		return s
	
	def findSolutions (self):		
		"""
		Solves the eq. 11 to find solutions (m1, m2, n1, n2) of coincidences for the given crystals and all angles.
		All solutions are lists of the type `[[angle_1, solutions_list], [angle_2, solutions_list], ...]`
		"""
		
		self.allSolutions = []
		
		for angle in self.angles:
			self.allSolutions.append (self.findSolutionsAngle(angle))
		
		return self.allSolutions
	
	def findMinimumArea (self):
		"""
		Finds a pair of linearly independent solutions (m1, m2, n1, n2), (m1', m2', n1', n2')
		which has minimum area. For each angle, minimizes |m x m'|. 
		"""
		
		self.supercell = []
		for s in self.allSolutions:
			cell = Solution (s.angle)
			
			minArea = sys.maxsize
			minAreaPair = []
			
			for i in range (len (s.solution)):
				for j in range (i+1, len (s.solution)):
					m1 = s.solution[i][0]
					m2 = s.solution[i][1]
					m1_prime = s.solution[j][0]
					m2_prime = s.solution[j][1]
					
					area = m1*m2_prime - m1_prime*m2
					
					if  area >= self.areaUnitCell && area < minArea:
						minArea = area
						minAreaPair = [s.solution[i], s.solution[j]]
			
			cell.solution = minAreaPair
					
		
		
		
		
		
								
		
		
		
