"""Dataset with 'Bwamba orthobunyavirus' sequences.

A dataset with 2 'Bwamba orthobunyavirus' sequences. The virus is
segmented and has 1 segments. Based on their strain and/or isolate,
these sequences were able to be grouped into 2 genomes. Many genomes
may have fewer than 1 segments.

THIS PYTHON FILE WAS GENERATED BY A COMPUTER PROGRAM! DO NOT EDIT!
"""

from os.path import dirname
from os.path import join
from os import listdir
import sys

from hybseldesign.datasets import GenomesDatasetMultiChrom

__author__ = 'Hayden Metsky <hayden@mit.edu>'

chrs = ["segment_" + seg for seg in ['S']]

def seq_header_to_chr(header):
    import re
    c = re.compile(r'\[segment (S)\]')
    m = c.search(header)
    if not m:
        raise ValueError("Unknown segment in header %s" % header)
    seg = m.group(1)
    valid_segs = ['S']
    if seg not in valid_segs:
        raise ValueError("Unknown segment %s" % seg)
    return "segment_" + seg


ds = GenomesDatasetMultiChrom(__name__, __file__, __spec__,
                              chrs, seq_header_to_chr)

for f in listdir(join(dirname(__file__), "data/bwamba/")):
    ds.add_fasta_path("data/bwamba/" + f, relative=True)

sys.modules[__name__] = ds
