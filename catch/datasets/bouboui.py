"""Dataset with 'Bouboui virus' sequences.

A dataset with 1 'Bouboui virus' genomes.

THIS PYTHON FILE WAS GENERATED BY A COMPUTER PROGRAM! DO NOT EDIT!
"""

import sys

from catch.datasets import GenomesDatasetSingleChrom


ds = GenomesDatasetSingleChrom(__name__, __file__, __spec__)
ds.add_fasta_path("data/bouboui.fasta.gz", relative=True)
sys.modules[__name__] = ds
