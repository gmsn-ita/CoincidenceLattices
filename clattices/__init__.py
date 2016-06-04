"""
`clattices` is a Python module for calculating coincidence lattices for pairs of 2D crystals.
Its methodology is described in [1] and is distributed as a complement to the article.

The `clattices` command line interface requires a set of 2D crystals as input and returns a table with
favorable coincidences. Each crystal is described using discrete files with a standard and is loaded 
within the class `Crystal`. Then, classes `Coincidences` are created for each pair of crystals and coincidence
lattices are investigated. Finally, all results are printed with the `Printer` class.

Important parameters should also be supplied to the `clattices` module in order to calculate
coincidence lattices of interest, such as:

1. Range of angles to investigate;

2. Maximum strains necessary to make the system commensurate;

3. Maximum supercell length;

4. Number of atoms inside the supercell.

To calculate the coincidence lattices, `clattices` solves the system of diophantine described in eq. 11 of [1]
by brute force. This requires a C module to speeds the process, which is called `clattices_loop`. The installation
of the `clattices` module itself requires the installation of the `clattices_loop` module.

[1] - Daniel S. Koda, Friedhelm Bechstedt, Marcelo Marques, and Lara K. Teles. Coincidence Lattices of 2D Crystals: Heterostructure Predictions and Applications. *The Journal of Physical Chemistry C* **2016** *120* (20), 10895-10908. DOI: 10.1021/acs.jpcc.6b01496

Installation
-------------------------------------------------------------------------

Installing `clattices` is pretty straightforward. Make sure you have the `numpy`, `argparse` and `re` packages installed
and run as superuser:

	python setup.py install

Usage
-------------------------------------------------------------------------
To use `clattices`, follow the steps:

1. Define the set of crystals of interest. The standard for each crystal file is the following:

	Label
	Number of atoms inside the unit cell
	Bravais lattice name (square, rectangular, hexagonal or oblique)
	Necessary parameters to describe the unit cell (one/two lattice parameters and zero/one angle)

Each crystal must be contain the information described above in a plain text file. No extensions are necessary.

2. Define all parameters to investigate, such as strain, range of angles to be investigated, sampling of angles,
stopping criterion etc. All of these parameters are summarized when `clattices -h` or `clattices --help` is executed.

3. Execute `clattices` with the parameters. Please note that the software returns mathematical solutions and a physical
rationale must be employed to interpret whether it corresponds or not to a plausible supercell. Different results can be
obtained specially by tuning `tolerance` and `angle_tolerance`.

Compatibility
-------------------------------------------------------------------------
`clattices` works properly on Python 3.5.1.

Contribution
-------------------------------------------------------------------------
`clattices` is available on GitHub (https://github.com/gmsn-ita/CoincidenceLattices). Suggestions and bug reports are welcome.
"""

__version__ = '1.0'
__all__ = ["Crystal", "Combination", "Printer"]

