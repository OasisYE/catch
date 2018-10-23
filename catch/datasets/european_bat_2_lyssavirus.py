"""Dataset with 'European bat 2 lyssavirus' sequences.

A dataset with 29 'European bat 2 lyssavirus' genomes.

THIS PYTHON FILE WAS GENERATED BY A COMPUTER PROGRAM! DO NOT EDIT!
"""

import sys

from catch.datasets import GenomesDatasetSingleChrom


ds = GenomesDatasetSingleChrom(__name__, __file__, __spec__)
ds.add_fasta_path("data/european_bat_2_lyssavirus.fasta.gz", relative=True)
sys.modules[__name__] = ds