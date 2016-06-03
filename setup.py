# -*- coding: utf-8 -*-

from setuptools import setup, Extension

clattices_loop = Extension("clattices.clattices_loop", sources = ["clattices_loop/clattices_loop.c", "clattices_loop/loop.c"])

setup (
	name='Coincidence Lattices for 2D Crystals',
	#~ packages=['clattices', 'clattices.clattices_loop'],
	packages=['clattices'],
	#~ ext_package='clattices',
	ext_modules=[clattices_loop],
	requires = [
	'numpy',
	'argparse',
	're',
	],
	entry_points = {
        "console_scripts": ['clattices = clattices.clattices:main']
        },
	version='1.0',
	description='Coincidence Lattices for 2D Crystals',
	author='Daniel S. Koda, Friedhelm Bechstedt, Marcelo Marques, Lara K. Teles',
	author_email='danielskoda@gmail.com, friedhelm.bechstedt@uni-jena.de, mmarques@ita.br, lkteles@ita.br',
	url='http://www.gmsn.ita.br/?q=en',
)
