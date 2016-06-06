# -*- coding: utf-8 -*-

from setuptools import setup, Extension

clattices_loop = Extension("clattices_loop", 
							sources = ["clattices_loop.c", "loop.c"],
							depends = ["loop.h"],
							)

setup (
	name='clattices_loop',
	ext_modules=[clattices_loop],
	version='1.0',
	description='Loop module for finding coincidence lattices of 2D Crystals',
	author='Daniel S. Koda, Friedhelm Bechstedt, Marcelo Marques, Lara K. Teles',
	author_email='danielskoda@gmail.com, friedhelm.bechstedt@uni-jena.de, mmarques@ita.br, lkteles@ita.br',
	url='http://www.gmsn.ita.br/?q=en',
)
