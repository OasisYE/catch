"""Dataset with 'Mumps rubulavirus' sequences.

A dataset with 296 'Mumps rubulavirus' genomes.

THIS PYTHON FILE WAS GENERATED BY A COMPUTER PROGRAM! DO NOT EDIT!
"""

import sys

from catch.datasets import GenomesDatasetSingleChrom


ds = GenomesDatasetSingleChrom(__name__, __file__, __spec__)
ds.add_fasta_path("data/mumps_rubulavirus.fasta.gz", relative=True)
sys.modules[__name__] = ds
