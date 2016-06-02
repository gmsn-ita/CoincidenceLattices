class Printer (object):
	"""
	Base class to print all information from the investigation to the output.
	
	All information is written to the default output file passed as parameter.
	"""
	
	def __init__ (self, outputFile, labelSpacing=20, columnTitle="bilayer"):
		"""
		Initializes the printer with useful information, such as the output file and the size of the labels.
		"""
		
		self.outputFile = outputFile
		"""
		Output file to be written.
		"""
		
		self.labelSpacing = labelSpacing
		"""
		Number of spaces for the first column.
		"""
		
		self.columnTitle = columnTitle
		"""
		Title for the first column
		"""
		
	def printMatrixNotation (self, supercellList, maxAtoms):
		"""
		Prints the list of supercells given to the output file using a matrix notation
		for the solutions (m1, m2, n1, n2) and (m1', m2', n1', n2')
		"""
		
		spaceCol_1 = self.labelSpacing
		spaceCol_2 = 15
		spaceCol_3 = 15
		spaceCol_4 = 15
		spaceCol_5 = 6
		spaceCol_6 = 10
		
		with open (self.outputFile, 'w') as f:
			f.write ("%s%s" % (self.columnTitle, (spaceCol_1 - len(self.columnTitle))*' '))
			f.write ("[  m1   m1']%s" % ((spaceCol_2 - len("[  m1   m1']"))*' '))
			f.write ("[  n1   n1']%s" % ((spaceCol_3 - len("[  n1   n1']"))*' '))
			f.write ("angle (deg)%s" % ((spaceCol_4 - len("angle (deg)"))*' '))
			f.write ("N%s" % ((spaceCol_5 - len("N"))*' '))
			f.write ("e (%%)%s" % ((spaceCol_6 - len("e (%%)"))*' '))
			f.write ("\n")
			f.write ("%s" % ((spaceCol_1)*' '))
			f.write ("[  m2   m2']%s" % ((spaceCol_2 - len("[  m2   m2']"))*' '))
			f.write ("[  n2   n2']%s" % ((spaceCol_3 - len("[  n2   n2']"))*' '))
			f.write ("%s" % ((spaceCol_4 + spaceCol_5 + spaceCol_6)*' '))
			f.write ("\n")
		
			for s in supercellList:
				if s.nAtoms <= maxAtoms:
					f.write ("%s/%s%s" % (s.label_1, s.label_2, (spaceCol_1 - 1 - len(s.label_1) - len(s.label_2))*' '))
					f.write ("[% 4d  % 4d]%s" % (s.solutions[0][0], s.solutions[1][0], (spaceCol_2 - len("[  m1  m1' ]"))*' '))
					f.write ("[% 4d  % 4d]%s" % (s.solutions[0][2], s.solutions[1][2], (spaceCol_3 - len("[  n1  n1' ]"))*' '))
					f.write ("%2.1f%s" % (s.angle, (spaceCol_4-3)*' '))
					f.write ("%d%s" % (s.nAtoms, (spaceCol_5 - len(str(s.nAtoms)))*' '))
					f.write ("% 1.2f%s" % (100*s.strain[0], (spaceCol_6 - 5)*' '))
					f.write ("\n")
					f.write ("%s" % ((spaceCol_1)*' '))
					f.write ("[% 4d  % 4d]%s" % (s.solutions[0][1], s.solutions[1][1], (spaceCol_2 - len("[  m2  m2' ]"))*' '))
					f.write ("[% 4d  % 4d]%s" % (s.solutions[0][3], s.solutions[1][3], (spaceCol_3 - len("[  n2  n2' ]"))*' '))
					f.write ("%s" % (spaceCol_4*' '))
					f.write ("%s" % ((spaceCol_5)*' '))
					f.write ("% 1.2f%s" % (100*s.strain[1], (spaceCol_6 - 5)*' '))
					f.write ("\n\n")
			
