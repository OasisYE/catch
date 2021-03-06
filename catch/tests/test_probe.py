"""Tests for probe module.
"""

from collections import defaultdict
import logging
import multiprocessing
import time
import unittest

import numpy as np

from catch import probe

__author__ = 'Hayden Metsky <hayden@mit.edu>'


class TestProbe(unittest.TestCase):
    """Tests methods in the Probe class.
    """

    def setUp(self):
        # Disable logging
        logging.disable(logging.WARNING)

        self.a = probe.Probe.from_str('ATCGTCGCGGATCG')
        self.b = probe.Probe.from_str('ATCCTCGCGTATNG')
        self.c = probe.Probe.from_str('ATCGTCGCGGATC')
        self.d = probe.Probe.from_str('GATCGTCGCGGATC')
        self.e = probe.Probe.from_str('GGATTGTCGGGGAT')
        self.f = probe.Probe.from_str('GTCGCGGAACGGGG')
        self.g = probe.Probe.from_str('GTCGCTGATCGATC')

    def make_random_probe(self, length):
        bases = ['A', 'T', 'C', 'G']
        s = "".join(np.random.choice(bases, size=length, replace=True))
        return probe.Probe.from_str(s)

    def test_parse_str(self):
        """Test that probe parses the string correctly.
        """
        np.testing.assert_array_equal(self.a.seq,
                                      np.array(['A', 'T', 'C', 'G', 'T', 'C',
                                                'G', 'C', 'G', 'G', 'A', 'T',
                                                'C', 'G']))

    def test_mismatches(self):
        """Test mismatches method.
        """
        self.assertEqual(self.a.mismatches(self.a), 0)
        self.assertEqual(self.a.mismatches(self.b), 3)
        self.assertEqual(self.b.mismatches(self.a), 3)

    def test_mismatches_at_offset(self):
        """Test mismatches_at_offset method.
        """
        self.assertEqual(self.a.mismatches_at_offset(self.d, -1), 0)
        self.assertEqual(self.a.mismatches_at_offset(self.e, -2), 2)
        self.assertEqual(self.a.mismatches_at_offset(self.f, 3), 1)
        self.assertRaises(ValueError, self.a.mismatches_at_offset, self.c, 1)
        self.assertRaises(ValueError, self.a.mismatches_at_offset, self.b, 15)

    def test_min_mismatches_within_shift(self):
        """Test min_mismatches_within_shift method.
        """
        self.assertEqual(self.a.min_mismatches_within_shift(self.g, 5), 1)
        self.assertEqual(self.g.min_mismatches_within_shift(self.a, 5), 1)
        self.assertEqual(self.a.min_mismatches_within_shift(self.g, 2), 8)
        self.assertEqual(self.g.min_mismatches_within_shift(self.a, 2), 8)
        self.assertEqual(self.a.min_mismatches_within_shift(self.b, 0), 3)
        self.assertEqual(self.b.min_mismatches_within_shift(self.a, 0), 3)
        self.assertEqual(self.a.min_mismatches_within_shift(self.b, 2), 3)
        self.assertEqual(self.b.min_mismatches_within_shift(self.a, 2), 3)

    def test_reverse_complement(self):
        """Test reverse_complement method.
        """
        a_rc = self.a.reverse_complement()
        a_rc_desired = probe.Probe.from_str('CGATCCGCGACGAT')
        self.assertEqual(a_rc, a_rc_desired)

    def test_with_prepended_str(self):
        """Test with_prepended_str method.
        """
        a_prepended = self.a.with_prepended_str('TATA')
        a_prepended_desired = probe.Probe.from_str('TATAATCGTCGCGGATCG')
        self.assertEqual(a_prepended, a_prepended_desired)

    def test_with_appended_str(self):
        """Test with_appended_str method.
        """
        a_appended = self.a.with_appended_str('TATA')
        a_appended_desired = probe.Probe.from_str('ATCGTCGCGGATCGTATA')
        self.assertEqual(a_appended, a_appended_desired)

    def test_identifier(self):
        """Test identifier method.

        This randomly produces 100 probes and checks that their identifiers
        are all unique. They are not guaranteed to be, but certainly
        should be.
        """
        np.random.seed(1)
        probes = [self.make_random_probe(100) for _ in range(100)]
        identifiers = {p.identifier() for p in probes}
        self.assertEqual(len(identifiers), 100)

    def test_share_some_kmers_nonmemoized(self):
        """Test share_some_kmers method.
        """
        np.random.seed(1)
        args = {'k': 5, 'num_kmers_to_test': 10, 'memoize_kmers': False}
        a = probe.Probe.from_str('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        b = probe.Probe.from_str('ZYXWVUTSRQPONMLKJIHGFEDCBA')
        c = probe.Probe.from_str('ABCXDEFGHIJKLMNOPQRATUVWYZ')
        ab, ba, ac, ca = 0, 0, 0, 0
        for i in range(100):
            if a.shares_some_kmers(b, **args):
                ab += 1
            if b.shares_some_kmers(a, **args):
                ba += 1
            if a.shares_some_kmers(c, **args):
                ac += 1
            if c.shares_some_kmers(a, **args):
                ca += 1
        self.assertLess(ab, 10)
        self.assertLess(ba, 10)
        self.assertGreater(ac, 90)
        self.assertGreater(ca, 90)

    def test_share_some_kmers_memoized(self):
        """Test share_some_kmers method.
        """
        np.random.seed(1)
        args = {'k': 5, 'num_kmers_to_test': 10, 'memoize_kmers': True}
        a = probe.Probe.from_str('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        b = probe.Probe.from_str('ZYXWVUTSRQPONMLKJIHGFEDCBA')
        c = probe.Probe.from_str('ABCXDEFGHIJKLMNOPQRATUVWYZ')
        ab, ba, ac, ca = 0, 0, 0, 0
        for i in range(100):
            if a.shares_some_kmers(b, **args):
                ab += 1
            if b.shares_some_kmers(a, **args):
                ba += 1
            if a.shares_some_kmers(c, **args):
                ac += 1
            if c.shares_some_kmers(a, **args):
                ca += 1
        self.assertLess(ab, 10)
        self.assertLess(ba, 10)
        self.assertGreater(ac, 90)
        self.assertGreater(ca, 90)

    def test_share_some_kmers_with_return_kmer(self):
        """Test share_some_kmers method.
        """
        np.random.seed(1)
        args = {'k': 5, 'num_kmers_to_test': 10, 'memoize_kmers': True,
                'return_kmer': True}
        a = probe.Probe.from_str('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        b = probe.Probe.from_str('ZYXWVUTSRQPONMLKJIHGFEDCBA')
        c = probe.Probe.from_str('ABCXDEFGHIJKLMNOPQRATUVWYZ')
        for i in range(100):
            ac = a.shares_some_kmers(c, **args)
            if ac:
                self.assertTrue(ac in a.seq_str)
                self.assertTrue(ac in c.seq_str)
            ca = c.shares_some_kmers(a, **args)
            if ca:
                self.assertTrue(ca in a.seq_str)
                self.assertTrue(ca in c.seq_str)

    def test_construct_kmers(self):
        """Test construct_kmers method.
        """
        a = probe.Probe.from_str('ABCDEFGHI')
        self.assertEqual(a.construct_kmers(4),
                         ['ABCD', 'BCDE', 'CDEF', 'DEFG', 'EFGH', 'FGHI'])

    def tearDown(self):
        # Re-enable logging
        logging.disable(logging.NOTSET)


class TestConstructRandKmerProbeMap(unittest.TestCase):
    """Tests _construct_rand_kmer_probe_map function.
    """

    def setUp(self):
        # Disable logging
        logging.disable(logging.WARNING)

    def make_random_probe(self, length):
        bases = ['A', 'T', 'C', 'G']
        s = "".join(np.random.choice(bases, size=length, replace=True))
        return probe.Probe.from_str(s)

    def test_random(self):
        """Make 50 random probes. From them, construct the kmer probe map
        with k=15 and with 10 kmers per probe. For each probe, check that
        at least 8 of its kmers can be found in this map (because kmers
        are selected from the probes with replacement, not all 10 may be
        present, and indeed not even 8 may be present).
        """
        np.random.seed(1)
        k = 15
        num_kmers_per_probe = 10
        probes = [self.make_random_probe(100) for _ in range(50)]
        kmer_map = probe._construct_rand_kmer_probe_map(
            probes,
            k=k,
            num_kmers_per_probe=num_kmers_per_probe)
        for p in probes:
            num_found = 0
            for kmer in p.construct_kmers(k):
                if kmer in kmer_map and p in kmer_map[kmer]:
                    num_found += 1
            self.assertGreaterEqual(num_found, 0.8 * num_kmers_per_probe)

    def test_shared_kmer(self):
        np.random.seed(1)
        a = probe.Probe.from_str('ABCDEFG')
        b = probe.Probe.from_str('XYZDEFH')
        probes = [a, b]
        # Use a high num_kmers_per_probe to ensure all possible
        # kmers are selected to be put into the map
        kmer_map = probe._construct_rand_kmer_probe_map(probes,
                                                        k=3,
                                                        num_kmers_per_probe=50)
        self.assertTrue(a in kmer_map['DEF'])
        self.assertTrue(b in kmer_map['DEF'])
        self.assertTrue(a in kmer_map['ABC'])
        self.assertFalse(b in kmer_map['ABC'])
        self.assertFalse(a in kmer_map['XYZ'])
        self.assertTrue(b in kmer_map['XYZ'])
        self.assertTrue(a in kmer_map['EFG'])
        self.assertFalse(b in kmer_map['EFG'])
        self.assertFalse(a in kmer_map['EFH'])
        self.assertTrue(b in kmer_map['EFH'])

    def test_positions(self):
        np.random.seed(1)
        a = probe.Probe.from_str('ABCDEFGABC')
        b = probe.Probe.from_str('XYZDEFHGHI')
        probes = [a, b]
        # Use a high num_kmers_per_probe to ensure all possible
        # kmers are selected to be put into the map
        kmer_map = probe._construct_rand_kmer_probe_map(probes,
                                                        k=3,
                                                        num_kmers_per_probe=50,
                                                        include_positions=True)
        self.assertCountEqual(kmer_map['DEF'], [(a, 3), (b, 3)])
        self.assertCountEqual(kmer_map['ABC'], [(a, 0), (a, 7)])
        self.assertCountEqual(kmer_map['XYZ'], [(b, 0)])
        self.assertCountEqual(kmer_map['EFG'], [(a, 4)])
        self.assertCountEqual(kmer_map['EFH'], [(b, 4)])

    def tearDown(self):
        # Re-enable logging
        logging.disable(logging.NOTSET)


class TestConstructPigeonholedKmerProbeMap(unittest.TestCase):
    """Tests _construct_pigeonholed_kmer_probe_map function.
    """

    def setUp(self):
        # Disable logging
        logging.disable(logging.WARNING)

    def test_no_mismatches(self):
        a = probe.Probe.from_str('ABCDEFGHIJ')
        b = probe.Probe.from_str('ZYXWVUTSRQ')
        probes = [a, b]
        kmer_map = probe._construct_pigeonholed_kmer_probe_map(
            probes, 0, min_k=5)
        # k-mers equal to the full length of the probe should be
        # chosen
        self.assertTrue(a in kmer_map[a.seq_str])
        self.assertTrue(b in kmer_map[b.seq_str])
        self.assertFalse(a in kmer_map[b.seq_str])
        self.assertFalse(b in kmer_map[a.seq_str])

    def test_too_small_k(self):
        a = probe.Probe.from_str('ABCDEFGHIJ')
        b = probe.Probe.from_str('ZYXWVUTSRQ')
        probes = [a, b]
        with self.assertRaises(probe.PigeonholeRequiresTooSmallKmerSizeError):
            # Should pick k=5, but requires k=6
            probe._construct_pigeonholed_kmer_probe_map(
                probes, 1, min_k=6)
        with self.assertRaises(probe.PigeonholeRequiresTooSmallKmerSizeError):
            # Should pick k=2, but requires k=3
            probe._construct_pigeonholed_kmer_probe_map(
                probes, 3, min_k=3)

    def test_one_mismatch(self):
        a = probe.Probe.from_str('ABCDEFGHIJ')
        b = probe.Probe.from_str('ZYXWVUTSRQ')
        probes = [a, b]
        kmer_map = probe._construct_pigeonholed_kmer_probe_map(
            probes, 1, min_k=2)
        # Should pick k=5
        self.assertEqual(len(kmer_map), 4)
        self.assertCountEqual(kmer_map['ABCDE'], [a])
        self.assertCountEqual(kmer_map['FGHIJ'], [a])
        self.assertCountEqual(kmer_map['ZYXWV'], [b])
        self.assertCountEqual(kmer_map['UTSRQ'], [b])

    def test_shared_kmer(self):
        a = probe.Probe.from_str('ABCDEFGHIJ')
        b = probe.Probe.from_str('ZYXWVABCDE')
        probes = [a, b]
        kmer_map = probe._construct_pigeonholed_kmer_probe_map(
            probes, 1, min_k=2)
        # Should pick k=5
        self.assertEqual(len(kmer_map), 3)
        self.assertCountEqual(kmer_map['ABCDE'], [a, b])
        self.assertCountEqual(kmer_map['FGHIJ'], [a])
        self.assertCountEqual(kmer_map['ZYXWV'], [b])

    def test_positions(self):
        a = probe.Probe.from_str('ABCDEFGH')
        b = probe.Probe.from_str('ZYXWVUAB')
        probes = [a, b]
        kmer_map = probe._construct_pigeonholed_kmer_probe_map(
            probes, 3, min_k=2, include_positions=True)
        # Should pick k=2
        self.assertEqual(len(kmer_map), 7)
        self.assertCountEqual(kmer_map['AB'], [(a, 0), (b, 6)])
        self.assertCountEqual(kmer_map['CD'], [(a, 2)])
        self.assertCountEqual(kmer_map['EF'], [(a, 4)])
        self.assertCountEqual(kmer_map['GH'], [(a, 6)])
        self.assertCountEqual(kmer_map['ZY'], [(b, 0)])
        self.assertCountEqual(kmer_map['XW'], [(b, 2)])
        self.assertCountEqual(kmer_map['VU'], [(b, 4)])

    def tearDown(self):
        # Re-enable logging
        logging.disable(logging.NOTSET)


class TestSharedKmerProbeMap(unittest.TestCase):
    """Tests SharedKmerProbeMap class.
    """

    def setUp(self):
        # Disable logging
        logging.disable(logging.WARNING)

    def test_rand_kmer_map(self):
        np.random.seed(1)
        a = probe.Probe.from_str('ABCDEFGABC')
        b = probe.Probe.from_str('XYZDEFHGHI')
        probes = [a, b]
        # Use a high num_kmers_per_probe to ensure all possible
        # kmers are selected to be put into the map
        kmer_map = probe._construct_rand_kmer_probe_map(probes,
                                                        k=3,
                                                        num_kmers_per_probe=50,
                                                        include_positions=True)
        shared_kmer_map = probe.SharedKmerProbeMap.construct(kmer_map)
        a_str = a.seq_str
        b_str = b.seq_str
        self.assertCountEqual(shared_kmer_map.get('DEF'),
                              [(a_str, 3), (b_str, 3)])
        self.assertCountEqual(shared_kmer_map.get('ABC'),
                              [(a_str, 0), (a_str, 7)])
        self.assertCountEqual(shared_kmer_map.get('XYZ'),
                              [(b_str, 0)])
        self.assertCountEqual(shared_kmer_map.get('EFG'),
                              [(a_str, 4)])
        self.assertCountEqual(shared_kmer_map.get('EFH'),
                              [(b_str, 4)])
        self.assertIsNone(shared_kmer_map.get('MNO'))
        self.assertEqual(shared_kmer_map.k, 3)

    def test_pigeonholed_kmer_map(self):
        a = probe.Probe.from_str('ABCDEFGH')
        b = probe.Probe.from_str('ZYXWVUAB')
        probes = [a, b]
        kmer_map = probe._construct_pigeonholed_kmer_probe_map(
            probes, 3, min_k=2, include_positions=True)
        shared_kmer_map = probe.SharedKmerProbeMap.construct(kmer_map)
        # Should pick k=2
        a_str = a.seq_str
        b_str = b.seq_str
        self.assertEqual(len(kmer_map), 7)
        self.assertCountEqual(shared_kmer_map.get('AB'),
                              [(a_str, 0), (b_str, 6)])
        self.assertCountEqual(shared_kmer_map.get('CD'),
                              [(a_str, 2)])
        self.assertCountEqual(shared_kmer_map.get('EF'),
                              [(a_str, 4)])
        self.assertCountEqual(shared_kmer_map.get('GH'),
                              [(a_str, 6)])
        self.assertCountEqual(shared_kmer_map.get('ZY'),
                              [(b_str, 0)])
        self.assertCountEqual(shared_kmer_map.get('XW'),
                              [(b_str, 2)])
        self.assertCountEqual(shared_kmer_map.get('VU'),
                              [(b_str, 4)])
        self.assertIsNone(shared_kmer_map.get('MN'))
        self.assertEqual(shared_kmer_map.k, 2)

    def tearDown(self):
        # Re-enable logging
        logging.disable(logging.NOTSET)


class TestProbeCoversSequenceByLongestCommonSubstring(unittest.TestCase):
    """Tests probe_covers_sequence_by_longest_common_substring function.
    """

    def setUp(self):
        # Disable logging
        logging.disable(logging.WARNING)

        self.seq = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def test_match_no_mismatches(self):
        f = probe.probe_covers_sequence_by_longest_common_substring(0, 6)
        match = f('ZZZABCGHIJKLXYZ', self.seq, 6, 9, 15, len(self.seq))
        self.assertTrue(match is not None)
        start, end = match
        self.assertEqual(start, 6)
        self.assertEqual(end, 12)
        match = f('ZZZZAFGHIJKLMDEF', self.seq, 6, 9, 15, len(self.seq))
        self.assertTrue(match is not None)
        start, end = match
        self.assertEqual(start, 5)
        self.assertEqual(end, 13)

    def test_match_with_mismatches(self):
        f = probe.probe_covers_sequence_by_longest_common_substring(1, 6)
        match = f('ZZZGHIGHIXKLDEF', self.seq, 6, 9, 15, len(self.seq))
        self.assertTrue(match is not None)
        start, end = match
        self.assertEqual(start, 6)
        self.assertEqual(end, 12)
        match = f('ZZZZZZGHIJKXSWZ', self.seq, 6, 9, 15, len(self.seq))
        self.assertTrue(match is not None)
        start, end = match
        self.assertEqual(start, 6)
        self.assertEqual(end, 12)
        match = f('ZZAGTFGHIJKXM', self.seq, 6, 9, 13, len(self.seq))
        self.assertTrue(match is not None)
        start, end = match
        self.assertEqual(start, 5)
        self.assertEqual(end, 13)

    def test_no_match_no_mismatches(self):
        f = probe.probe_covers_sequence_by_longest_common_substring(0, 6)
        match = f('ZZZABCGHIXKLXYZ', self.seq, 6, 9, 15, len(self.seq))
        self.assertTrue(match is None)
        match = f('ZZZZZAGHIJKBC', self.seq, 6, 9, 13, len(self.seq))
        self.assertTrue(match is None)

    def test_no_match_with_mismatches(self):
        f = probe.probe_covers_sequence_by_longest_common_substring(1, 6)
        match = f('ZZZABCGHIXKXXYZ', self.seq, 6, 9, 15, len(self.seq))
        self.assertTrue(match is None)
        f = probe.probe_covers_sequence_by_longest_common_substring(1, 6)
        match = f('ZZZZZAGHIJYZ', self.seq, 6, 9, 12, len(self.seq))
        self.assertTrue(match is None)

    def test_match_with_island_of_exact_match(self):
        f = probe.probe_covers_sequence_by_longest_common_substring(1, 6, 4)
        match = f('ZZZGHIGHIJXLDEF', self.seq, 6, 9, 15, len(self.seq))
        self.assertEqual(match, (6, 12))

    def test_no_match_with_island_of_exact_match(self):
        f = probe.probe_covers_sequence_by_longest_common_substring(1, 6, 4)
        match = f('ZZZGHIGHIXKLDEF', self.seq, 6, 9, 15, len(self.seq))
        self.assertTrue(match is None)

    def test_match_with_probe_smaller_than_lcf_thres(self):
        f = probe.probe_covers_sequence_by_longest_common_substring(1, 6)
        match = f('GHIX', self.seq[6:10], 1, 3, 4, len(self.seq[6:10]))
        self.assertEqual(match, (0, 4))

    def test_no_match_with_probe_smaller_than_lcf_thres(self):
        f = probe.probe_covers_sequence_by_longest_common_substring(0, 6)
        match = f('GHIX', self.seq[6:10], 1, 3, 4, len(self.seq[6:10]))
        self.assertTrue(match is None)

    def test_match_from_probe_on_end(self):
        f = probe.probe_covers_sequence_by_longest_common_substring(0, 10)
        match = f('ABCDEF', self.seq, 1, 3, 6, len(self.seq))
        self.assertEqual(match, (0, 6))

    def test_no_match_from_probe_on_end(self):
        f = probe.probe_covers_sequence_by_longest_common_substring(0, 10)
        match = f('ABCDEF', self.seq, 1, 3, 10, len(self.seq))
        self.assertTrue(match is None)

    def test_match_with_probe_longer_than_sequence(self):
        f = probe.probe_covers_sequence_by_longest_common_substring(0, 6)
        match = f('DEFG', 'DEFG', 1, 3, 7, 4)
        self.assertEqual(match, (0, 4))

    def test_no_match_with_probe_longer_than_sequence(self):
        f = probe.probe_covers_sequence_by_longest_common_substring(0, 6)
        match = f('DEFX', 'DEFG', 1, 3, 7, 4)
        self.assertTrue(match is None)

    def tearDown(self):
        # Re-enable logging
        logging.disable(logging.NOTSET)


class TestFindProbeCoversInSequence(unittest.TestCase):
    """Tests find_probe_covers_in_sequence function.
    """

    def setUp(self):
        # Disable logging
        logging.disable(logging.WARNING)

    def test_one_or_no_occurrence(self):
        """Tests with short sequence and short probes
        where each probe appears zero or one times.
        """
        np.random.seed(1)
        sequence = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        a = probe.Probe.from_str('GHIJKL')
        b = probe.Probe.from_str('STUVWX')
        c = probe.Probe.from_str('ACEFHJ')
        probes = [a, b, c]
        kmer_map = probe.construct_kmer_probe_map_to_find_probe_covers(
            probes, 0, 6, min_k=6)
        kmer_map = probe.SharedKmerProbeMap.construct(kmer_map)
        f = probe.probe_covers_sequence_by_longest_common_substring(0, 6)
        for n_workers in [1, 2, 4, 7, 8]:
            probe.open_probe_finding_pool(kmer_map, f, n_workers)
            found = probe.find_probe_covers_in_sequence(sequence)
            self.assertCountEqual(found[a], [(6, 12)])
            self.assertCountEqual(found[b], [(18, 24)])
            self.assertFalse(c in found)
            probe.close_probe_finding_pool()

    def test_two_occurrences(self):
        """Tests with short sequence and short probes
        where one probe appears twice.
        """
        np.random.seed(1)
        sequence = 'ABCDEFGHIJKLMNOPCDEFGHQRSTU'
        a = probe.Probe.from_str('CDEFGH')
        b = probe.Probe.from_str('GHIJKL')
        c = probe.Probe.from_str('STUVWX')
        probes = [a, b, c]
        kmer_map = probe.construct_kmer_probe_map_to_find_probe_covers(
            probes, 0, 6, min_k=6)
        kmer_map = probe.SharedKmerProbeMap.construct(kmer_map)
        f = probe.probe_covers_sequence_by_longest_common_substring(0, 6)
        for n_workers in [1, 2, 4, 7, 8]:
            probe.open_probe_finding_pool(kmer_map, f, n_workers)
            found = probe.find_probe_covers_in_sequence(sequence)
            self.assertCountEqual(found[a], [(2, 8), (16, 22)])
            self.assertCountEqual(found[b], [(6, 12)])
            self.assertFalse(c in found)
            probe.close_probe_finding_pool()

    def test_more_than_cover(self):
        """Tests with short sequence and short probes
        where probes contain more than what they cover.
        """
        np.random.seed(1)
        sequence = 'ABCDEFGHIJKLMNOPQR' + ('Z' * 100) + 'STUVWXYZ'
        a = probe.Probe.from_str('XYZCDEFGHIJKABCSTUVWXABC')
        b = probe.Probe.from_str('PQRSGHIJKLMNXYZ')
        c = probe.Probe.from_str('ABCFGHIJKLZAZAZAGHIJKL')
        probes = [a, b, c]
        # This should default to the random approach, so set k (rather than
        # min_k)
        kmer_map = probe.construct_kmer_probe_map_to_find_probe_covers(
            probes, 0, 6, k=6)
        kmer_map = probe.SharedKmerProbeMap.construct(kmer_map)
        f = probe.probe_covers_sequence_by_longest_common_substring(0, 6)
        for n_workers in [1, 2, 4, 7, 8]:
            probe.open_probe_finding_pool(kmer_map, f, n_workers)
            found = probe.find_probe_covers_in_sequence(sequence)
            self.assertCountEqual(found[a], [(2, 11), (118, 124)])
            self.assertCountEqual(found[b], [(6, 14)])
            self.assertCountEqual(found[c], [(5, 12)])
            probe.close_probe_finding_pool()

    def test_repetitive(self):
        """Tests with short sequence and short probes
        where the sequence and probes have repetitive sequences, so that
        one probe can cover a lot of the sequence.
        """
        np.random.seed(1)
        sequence = 'ABCAAAAAAAAAAXYZXYZXYZXYZAAAAAAAAAAAAAXYZ'
        a = probe.Probe.from_str('NAAAAAAN')
        probes = [a]
        # This should default to the random approach, so set k (rather than
        # min_k)
        kmer_map = probe.construct_kmer_probe_map_to_find_probe_covers(
            probes, 0, 6, k=6)
        kmer_map = probe.SharedKmerProbeMap.construct(kmer_map)
        f = probe.probe_covers_sequence_by_longest_common_substring(0, 6)
        for n_workers in [1, 2, 4, 7, 8]:
            probe.open_probe_finding_pool(kmer_map, f, n_workers)
            found = probe.find_probe_covers_in_sequence(sequence)
            self.assertCountEqual(found[a], [(3, 13), (25, 38)])
            probe.close_probe_finding_pool()

    def test_island_with_exact_match1(self):
        """Tests the 'island_with_exact_match' argument for
        probe.probe_covers_sequence_by_longest_common_substring(..).
        """
        np.random.seed(1)
        sequence = 'ABCDEFGHIJKLMNOPYDEFGHQRSTU'
        a = probe.Probe.from_str('XDEFGH')
        b = probe.Probe.from_str('CXEFGH')
        c = probe.Probe.from_str('CDXFGH')
        d = probe.Probe.from_str('CDEXGH')
        e = probe.Probe.from_str('CDEFXH')
        f = probe.Probe.from_str('CDEFGX')
        g = probe.Probe.from_str('CDEFGH')
        probes = [a, b, c, d, e, f, g]
        kmer_map = probe.construct_kmer_probe_map_to_find_probe_covers(
            probes, 1, 6, k=3)
        kmer_map = probe.SharedKmerProbeMap.construct(kmer_map)
        fn = probe.probe_covers_sequence_by_longest_common_substring(1, 6, 4)
        for n_workers in [1, 2, 4, 7, 8]:
            probe.open_probe_finding_pool(kmer_map, fn, n_workers)
            found = probe.find_probe_covers_in_sequence(sequence)
            self.assertCountEqual(found[a], [(2, 8), (16, 22)])
            self.assertCountEqual(found[b], [(2, 8)])
            self.assertFalse(c in found)
            self.assertFalse(d in found)
            self.assertCountEqual(found[e], [(2, 8)])
            self.assertCountEqual(found[f], [(2, 8)])
            self.assertCountEqual(found[g], [(2, 8), (16, 22)])
            probe.close_probe_finding_pool()

    def test_island_with_exact_match2(self):
        """Tests the 'island_with_exact_match' argument for
        probe.probe_covers_sequence_by_longest_common_substring(..).
        """
        np.random.seed(1)
        sequence = 'ABCDEFGHIJKLMNOPCDEFGHQRSTU'
        a = probe.Probe.from_str('HXJKLMNOPCDE')
        b = probe.Probe.from_str('XIJKXMNOXCDE')
        c = probe.Probe.from_str('XIJKXMNOPXDE')
        probes = [a, b, c]
        kmer_map = probe.construct_kmer_probe_map_to_find_probe_covers(
            probes, 3, 6, k=3)
        kmer_map = probe.SharedKmerProbeMap.construct(kmer_map)
        fn = probe.probe_covers_sequence_by_longest_common_substring(3, 6, 4)
        for n_workers in [1, 2, 4, 7, 8]:
            probe.open_probe_finding_pool(kmer_map, fn, n_workers)
            found = probe.find_probe_covers_in_sequence(sequence)
            self.assertCountEqual(found[a], [(7, 19)])
            self.assertFalse(b in found)
            self.assertCountEqual(found[c], [(7, 19)])
            probe.close_probe_finding_pool()

    def test_pigeonhole_with_mismatch(self):
        """Tests with short sequence and short probes
        where the call to construct_kmer_probe_map_to_find_probe_covers tries
        the pigeonhole approach.
        """
        np.random.seed(1)
        sequence = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        a = probe.Probe.from_str('GHIJXL')
        b = probe.Probe.from_str('BTUVWX')
        c = probe.Probe.from_str('ACEFHJ')
        probes = [a, b, c]

        kmer_map = probe.construct_kmer_probe_map_to_find_probe_covers(
            probes, 1, 6, min_k=3, k=4)
        kmer_map = probe.SharedKmerProbeMap.construct(kmer_map)
        # This should try the pigeonhole approach, which should choose k=3
        self.assertEqual(kmer_map.k, 3)
        f = probe.probe_covers_sequence_by_longest_common_substring(1, 6)
        for n_workers in [1, 2, 4, 7, 8]:
            probe.open_probe_finding_pool(kmer_map, f, n_workers)
            found = probe.find_probe_covers_in_sequence(sequence)
            self.assertCountEqual(found[a], [(6, 12)])
            self.assertCountEqual(found[b], [(18, 24)])
            self.assertFalse(c in found)
            probe.close_probe_finding_pool()

        kmer_map = probe.construct_kmer_probe_map_to_find_probe_covers(
            probes, 1, 6, min_k=4, k=4)
        kmer_map = probe.SharedKmerProbeMap.construct(kmer_map)
        # This should try the pigeonhole approach and fail because it
        # chooses k=3, but min_k=4. So it should then try the random
        # approach with k=4.
        self.assertEqual(kmer_map.k, 4)
        f = probe.probe_covers_sequence_by_longest_common_substring(1, 6)
        for n_workers in [1, 2, 4, 7, 8]:
            probe.open_probe_finding_pool(kmer_map, f, n_workers)
            found = probe.find_probe_covers_in_sequence(sequence)
            self.assertCountEqual(found[a], [(6, 12)])
            self.assertCountEqual(found[b], [(18, 24)])
            self.assertFalse(c in found)
            probe.close_probe_finding_pool()

    def test_multiple_searches_with_same_pool(self):
        """Tests more than one call to find_probe_covers_in_sequence()
        with the same pool.
        """
        np.random.seed(1)
        sequence_a = 'ABCAXYZXYZDEFXYZAAYZ'
        sequence_b = 'GHIDAXYZXYZAAABCABCD'
        a = probe.Probe.from_str('AXYZXYZ')
        b = probe.Probe.from_str('AABCABC')
        probes = [a, b]
        # This should default to the random approach, so set k (rather than
        # min_k)
        kmer_map = probe.construct_kmer_probe_map_to_find_probe_covers(
            probes, 0, 6, k=3)
        kmer_map = probe.SharedKmerProbeMap.construct(kmer_map)
        f = probe.probe_covers_sequence_by_longest_common_substring(0, 6)
        for n_workers in [1, 2, 4, 7, 8]:
            probe.open_probe_finding_pool(kmer_map, f, n_workers)
            found_a = probe.find_probe_covers_in_sequence(sequence_a)
            self.assertEqual(found_a, {a: [(3, 10)]})
            found_b = probe.find_probe_covers_in_sequence(sequence_b)
            self.assertEqual(found_b, {a: [(4, 11)], b: [(12, 19)]})
            probe.close_probe_finding_pool()

    def test_open_close_pool_without_work(self):
        """Tests opening a probe finding pool and closing it without doing
        any work in between.

        There was a bug, caused by a bug in early versions of Python, that
        could cause closing the pool to hang indefinitely when no work
        is submitted.
        """
        probes = [probe.Probe.from_str('ABCDEF')]
        kmer_map = probe.construct_kmer_probe_map_to_find_probe_covers(
            probes, 0, 6, k=3)
        kmer_map = probe.SharedKmerProbeMap.construct(kmer_map)
        f = probe.probe_covers_sequence_by_longest_common_substring(0, 6)
        for n_workers in [1, 2, 4, 7, 8, None]:
            probe.open_probe_finding_pool(kmer_map, f, n_workers)
            time.sleep(1)
            probe.close_probe_finding_pool()
            time.sleep(1)

    def test_random_small_genome1(self):
        self.run_random(100, 15000, 25000, 300, seed=1)

    def test_random_small_genome2(self):
        self.run_random(100, 15000, 25000, 300, probe_length=75,
                        lcf_thres=75, seed=2)

    def test_random_small_genome_varied_k(self):
        for k in [21, 15, 13, 10]:
            self.run_random(100, 15000, 25000, 300,
                kmer_probe_map_k=k, seed=1)

    def test_random_large_genome1(self):
        self.run_random(1, 1500000, 2500000, 30000,
                        lcf_thres=100, seed=1)

    def test_random_large_genome2(self):
        self.run_random(1, 500000, 1000000, 6000,
                        lcf_thres=80, seed=2)

    def test_random_large_genome3(self):
        self.run_random(1, 500000, 1000000, 6000, probe_length=75,
                        lcf_thres=75, seed=3)

    def test_random_large_genome_varied_k(self):
        for k in [21, 15, 13, 10]:
            self.run_random(1, 1500000, 2500000, 30000,
                            lcf_thres=100, kmer_probe_map_k=k, seed=1)

    def test_random_large_genome_native_dict(self):
        self.run_random(1, 1500000, 2500000, 30000,
                        lcf_thres=100, seed=4, use_native_dict=True)

    def run_random(self, n, genome_min, genome_max, num_probes,
                   probe_length=100, lcf_thres=None, kmer_probe_map_k=20,
                   seed=1, n_workers=2, use_native_dict=False):
        """Run tests with a randomly generated sequence.

        Repeatedly runs tests in which a sequence is randomly generated,
        probes are generated from that sequence, and then the probes are
        looked up in the sequence.

        Creates the probes with the intention of determining coverage with
        a longest common substring.

        Args:
            n: number of times to run the test
            genome_min/genome_max: the genome (sequence) size is
                randomly chosen between genome_min and genome_max
            num_probes: the number of probes generated from the random
                sequence
            probe_length: number of bp to make each probe
            lcf_thres: lcf threshold parameter; when None, it is
                randomly chosen among 80 and 100
            kmer_probe_map_k: k-mer length to use when constructing the
                map of k-mers to probes
            seed: random number generator seed
            n_workers: number of workers to have in a probe finding pool
            use_native_dict: have the probe finding pool use a native Python
                dict
        """
        np.random.seed(seed)
        fixed_lcf_thres = lcf_thres

        for n in range(n):
            if fixed_lcf_thres is not None:
                lcf_thres = fixed_lcf_thres
            else:
                # Choose either lcf_thres=80 or lcf_thres=100
                lcf_thres = np.random.choice([80, 100])
            # Make a random sequence
            seq_length = np.random.randint(genome_min, genome_max)
            sequence = "".join(np.random.choice(['A', 'T', 'C', 'G'],
                                                size=seq_length,
                                                replace=True))
            desired_probe_cover_ranges = defaultdict(list)
            # Make num_probes random probes
            probes = []
            for m in range(num_probes):
                subseq_start = np.random.randint(0, seq_length - probe_length)
                subseq_end = subseq_start + probe_length
                cover_length = np.random.randint(lcf_thres, probe_length + 1)
                cover_start = subseq_start + \
                    np.random.randint(0, probe_length - cover_length + 1)
                cover_end = min(seq_length, cover_start + cover_length)
                probe_str_cover = sequence[cover_start:cover_end]
                # Add random bases before and after what the probe should
                # cover
                probe_str_start = "".join(
                    np.random.choice(['A', 'T', 'C', 'G'],
                                     size=cover_start - subseq_start,
                                     replace=True))
                probe_str_end = "".join(
                    np.random.choice(['A', 'T', 'C', 'G'],
                                     size=subseq_end - cover_end,
                                     replace=True))
                probe_str = probe_str_start + probe_str_cover + probe_str_end
                # Add 0, 1, 2, or 3 random mismatches
                for k in range(np.random.randint(0, 4)):
                    pos = np.random.randint(0, probe_length)
                    base_choices = [b for b in ['A', 'T', 'C', 'G']
                                    if b != probe_str[pos]]
                    probe_str = probe_str[:pos] + \
                        "".join(np.random.choice(base_choices, size=1)) + \
                        probe_str[(pos + 1):]
                p = probe.Probe.from_str(probe_str)
                desired_probe_cover_ranges[p].append((cover_start, cover_end))
                probes += [p]
            kmer_map = probe.construct_kmer_probe_map_to_find_probe_covers(
                probes, 3, lcf_thres,
                min_k=kmer_probe_map_k, k=kmer_probe_map_k)
            kmer_map = probe.SharedKmerProbeMap.construct(kmer_map)
            f = probe.probe_covers_sequence_by_longest_common_substring(
                3, lcf_thres)
            probe.open_probe_finding_pool(kmer_map, f, n_workers,
                                          use_native_dict=use_native_dict)
            found = probe.find_probe_covers_in_sequence(sequence)
            probe.close_probe_finding_pool()
            # Check that this didn't find any extraneous probes and that
            # it found at least 95% of the original (it may miss some
            # due to false negatives in the approach)
            self.assertLessEqual(len(found), len(probes))
            self.assertGreaterEqual(len(found), 0.95 * len(probes))
            # Check that each desired probe was found correctly
            for p, cover_ranges in desired_probe_cover_ranges.items():
                if p not in found:
                    continue
                found_cover_ranges = found[p]
                # This probe most likely was found once, but could have
                # been missed (due to false negatives in the approach) and
                # may have been found more than once due to chance (but
                # probably not too much more!)
                self.assertTrue(len(found_cover_ranges) in [1, 2])
                # The cover ranges should have been captured, and the ones
                # found may extend past what was desired by a small amount due
                # to allowing mismatches and chance
                # Because of mismatches possibly added to the end of the
                # desired cover range, what was recaptured may not always
                # encompass the entire cover range, so allow some small
                # tolerance
                for desired_cv in cover_ranges:
                    found_desired_cv = False
                    for found_cv in found_cover_ranges:
                        left_diff = desired_cv[0] - found_cv[0]
                        right_diff = found_cv[1] - desired_cv[1]
                        if left_diff >= -7 and left_diff < 15:
                            if right_diff >= -7 and right_diff < 15:
                                found_desired_cv = True
                                break
                    self.assertTrue(found_desired_cv)

    def tearDown(self):
        # Re-enable logging
        logging.disable(logging.NOTSET)
