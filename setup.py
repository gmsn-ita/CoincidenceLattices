# -*- coding: utf-8 -*-

from setuptools import setup
    
setup (
	name='Coincidence Lattices for 2D Crystals',
	packages=['clattices'],
	
	requires = [
	'numpy',
	'argparse',
	],
	entry_points = {
        "console_scripts": ['clattices = clattices.clattices:main']
        },
	version='1.0',
	description='Coincidence Lattices for 2D Crystals',
	author='Daniel S. Koda, Friedhelm Bechstedt, Marcelo Marques, Lara K. Teles',
	author_email='danielskoda@gmail.com, friedhelm.bechstedt@uni-jena.de, mmarques@ita.br, lkteles@ita.br',
	url='http://www.gmsn.ita.br/',
	)
