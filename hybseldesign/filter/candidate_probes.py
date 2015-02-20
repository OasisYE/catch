"""Functions for generating lists of many (likely redundant) probes,
termed candidate probes, from a sequence or list of sequences.
"""

# Author: Hayden Metsky <hayden@mit.edu>

import sys
import re
import numpy as np

from hybseldesign.utils import seq_io
from hybseldesign import probe
from hybseldesign.datasets import ebola2014


"""Generates and returns a list of candidate probes from the sequence
seq.

The probes are probe_length bp long and separated by probe_stride bp.
Possible probes that would contains strings of min_n_string_length or
more N's are discarded and, instead, new probes flanking the string
are added.

When the sequence length is not divisible by probe_stride there are
remaining bases at the end not covered. An extra probe is added for
these iff add_probe_for_end_bases is True. (This argument was added
to replicate past software and results, in which its value would be
False.)

insert_bug adds a bug to the code in order to replicate past software
(the first version of probe design, as Matlab code) and its reuslts.

It is possible (especially when there are strings of N's) that
duplicate probes are returned.
"""
def make_candidate_probes_from_sequence(seq, probe_length=100,
    probe_stride=50, min_n_string_length=2,
    add_probe_for_end_bases=True, insert_bug=False):
  if probe_length > len(seq):
    raise ValueError("Invalid probe_length " + str(probe_length))

  if type(seq) is np.ndarray or type(seq) is np.array:
    seq = seq.tostring()
  n_string_query = re.compile('(N{'+str(min_n_string_length)+',})')

  # Make a probe based on the subsequence seq[start:end].
  # Namely, if that subsequence contains no string of N's, then it
  # is a probe to be added and the probe is returned in a single-
  # valued list. Otherwise, an empty list is returned.
  def add_probe_from_subsequence(start, end, is_bug_location=False):
    subseq = seq[start:end]
    probes = []

    if insert_bug and is_bug_location:
      if 'N' in subseq:
        # A bug in the original version of the probe design (Matlab code)
        # considered a probe with just a single 'N' (even if
        # min_n_string_length > 1) to be invalid and otherwise to be
        # valid
        pass
      else:
        probes += [subseq]
    else:
      # Search for strings of min_n_string_length or more N's in subseq
      # and only add a probe if there is not such a string
      if not n_string_query.search(subseq):
        # There's no string of N's, so this subsequence is a valid probe
        probes += [subseq]

    return probes

  # Populate a list of probes
  probes = []
  for start in np.arange(0, len(seq), probe_stride):
    if start + probe_length > len(seq):
      break
    # A bug in the original version of the probe design (Matlab code)
    # was present in designing a so-called 'B adapter'
    is_bug_location = start % probe_length == probe_stride
    probes += add_probe_from_subsequence(start, start+probe_length,
                is_bug_location=is_bug_location)
  if len(seq) % probe_stride != 0 and add_probe_for_end_bases:
    # There are bases on the right that were never covered, so add
    # another probe for this
    probes += add_probe_from_subsequence(len(seq)-probe_length, len(seq))

  # Add probes flanking each string of N's. Specifically, add a probe
  # to the left of a string and to the right. The called function
  # must check that the flanking probe does not contain a string of
  # N's before adding. (Don't recursively chase flanking probes.)
  for match in n_string_query.finditer(seq):
    if match.start() - probe_length >= 0:
      # Add the left flanking probe for match
      probes += add_probe_from_subsequence(match.start()-probe_length,
                  match.start())
    if match.end() + probe_length <= len(seq):
      # Add the right flanking probe for match
      probes += add_probe_from_subsequence(match.end(),
                  match.end()+probe_length)

  # Convert the probes from a Python list of Python strings to a
  # list of probe.Probe
  for i in xrange(len(probes)):
    probes[i] = probe.Probe.from_str(probes[i])

  return probes


"""Generates and returns a list of probes from a list of sequences
seqs.

It is possible (perhaps even likely depending on where
the sequences come from) that duplicate probes are returned.
"""
def make_candidate_probes_from_sequences(seqs, probe_length=100,        
    probe_stride=50, min_n_string_length=2,
    add_probe_for_end_bases=True, insert_bug=False):
  if type(seqs) != list:
    raise ValueError("seqs must be a list of sequences")
  if len(seqs) == 0:
    raise ValueError("seqs must have at least one sequence")
  for seq in seqs:
    if type(seq) != str:
      raise ValueError("seqs must be a list of Python strings")

  probes = []
  for seq in seqs:
    probes += make_candidate_probes_from_sequence(seq,
                probe_length=probe_length, probe_stride=probe_stride,
                min_n_string_length=min_n_string_length,
                add_probe_for_end_bases=add_probe_for_end_bases,
                insert_bug=insert_bug)
  return probes
