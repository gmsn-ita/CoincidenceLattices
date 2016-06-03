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

		self.columnTitle = columnTitle
		"""
		Title for the first column
		"""
		
		self.spaceCol_1 = labelSpacing
		"""
		Spacing for the first column.
		If you feel like the standard spacing is not adequate, it suffices to
		change the `spaceCol` variables in the `Printer` class.
		"""
		
		self.spaceCol_2 = 15
		"""
		Spacing for the second column
		"""
		
		self.spaceCol_3 = 15
		"""
		Spacing for the third column
		"""
		
		self.spaceCol_4 = 15
		"""
		Spacing for the fourth column
		"""
		
		self.spaceCol_5 = 6
		"""
		Spacing for the fifth column
		"""
		
		self.spaceCol_6 = 10
		"""
		Spacing for the sixth column
		"""
	def printMatrixNotationHeader (self):
		"""
		Prints the header of the output table using a matrix notation.
		"""
		
		with open (self.outputFile, 'w') as f:
			f.write (self.columnTitle.ljust(self.spaceCol_1))
			f.write ("[  m1   m1']".rjust(self.spaceCol_2))
			f.write ("[  n1   n1']".rjust(self.spaceCol_3))
			f.write ("angle (deg)".rjust(self.spaceCol_4))
			f.write ("N".rjust(self.spaceCol_5))
			f.write ("e (%)".rjust(self.spaceCol_6))
			f.write ("\n")
			f.write ("".rjust(self.spaceCol_1))
			f.write ("[  m2   m2']".rjust(self.spaceCol_2))
			f.write ("[  n2   n2']".rjust(self.spaceCol_3))
			f.write ("".rjust(self.spaceCol_4 + self.spaceCol_5 + self.spaceCol_6))
			f.write ("\n\n")
		
	def printMatrixNotation (self, supercellList, maxAtoms):
		"""
		Prints the list of supercells given to the output file using a matrix notation
		for the solutions (m1, m2, n1, n2) and (m1', m2', n1', n2').
		"""
		
		with open (self.outputFile, 'a') as f:		
			for s in supercellList:
				if s.nAtoms <= maxAtoms:
					f.write (("%s/%s" % (s.label_1, s.label_2)).ljust(self.spaceCol_1) )
					f.write (("[% 4d  % 4d]" % (s.solutions[0][0], s.solutions[1][0])).rjust(self.spaceCol_2))
					f.write (("[% 4d  % 4d]" % (s.solutions[0][2], s.solutions[1][2])).rjust(self.spaceCol_3))
					f.write (("%2.1f" % s.angle).rjust(self.spaceCol_4))
					f.write (("%d" % s.nAtoms).rjust(self.spaceCol_5))
					f.write (("% 1.2f" % (100*s.strain[0])).rjust(self.spaceCol_6))
					f.write ("\n")
					f.write ("".rjust(self.spaceCol_1))
					f.write (("[% 4d  % 4d]" % (s.solutions[0][1], s.solutions[1][1])).rjust(self.spaceCol_2))
					f.write (("[% 4d  % 4d]" % (s.solutions[0][3], s.solutions[1][3])).rjust(self.spaceCol_3))
					f.write ("".rjust(self.spaceCol_4 + self.spaceCol_5))
					f.write (("% 1.2f" % (100*s.strain[1])).rjust(self.spaceCol_6))
					f.write ("\n\n")
			
