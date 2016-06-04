# CoincidenceLattices

`clattices` is a Python module for calculating coincidence lattices for pairs of 2D crystals. Its methodology is described in [1] and is distributed as a complement to the article. The `clattices` command line interface requires a set of 2D crystals as input and returns a table with favorable coincidences.

Important parameters should also be supplied to the `clattices` module in order to calculate coincidence lattices of interest, such as:

1. Range of angles to investigate;
2. Maximum strains necessary to make the system commensurate;
3. Maximum supercell length;
4. Number of atoms inside the supercell.

If you find this software useful for your research, please cite [1].

[1] - Daniel S. Koda, Friedhelm Bechstedt, Marcelo Marques, and Lara K. Teles. Coincidence Lattices of 2D Crystals: Heterostructure Predictions and Applications. *The Journal of Physical Chemistry C* **2016** *120* (20), 10895-10908. DOI: 10.1021/acs.jpcc.6b01496

Installation
--------------

Installing `clattices` is pretty straightforward. Make sure you have the `numpy`, `argparse` and `re` packages installed
and run as superuser:

	`python setup.py install`

Usage
--------
To use `clattices`, follow the steps:

1. Define the set of crystals of interest. The standard for each crystal file is the following:

```
	Label
	Number of atoms inside the unit cell
	Bravais lattice name (square, rectangular, hexagonal or oblique)
	Necessary parameters to describe the unit cell (one/two lattice parameters and zero/one angle)
```

Each crystal must be contain the information described above in a plain text file. No extensions are necessary.

2. Define all parameters to investigate, such as strain, range of angles to be investigated, sampling of angles,
stopping criterion etc. All of these parameters are summarized when `clattices -h` or `clattices --help` is executed.

3. Execute `clattices` with the parameters. Please note that the software returns mathematical solutions and a physical
rationale must be employed to interpret whether it corresponds or not to a plausible supercell. Different results can be
obtained specially by tuning `tolerance` and `angle_tolerance`.

A step-by-step tutorial can be found in the `docs/` directory as a PDF file.

Compatibility
--------------
`clattices` works properly on Python 3.5.1.

Contribution
-------------
`clattices` is [available on GitHub](https://github.com/gmsn-ita/CoincidenceLattices). Suggestions and bug reports are welcome.
