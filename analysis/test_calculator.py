#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# test if tie and faction calculator works properly
import unittest
from calculateTies import *
from calculateFactions import *


def verify_pattern(pattern):
    if pattern not in \
        ['politicianCentrality_politicallNetwork', 'politicianManagerNeighbors',
            'managerCentrality_politicianNetwork']:
        raise ValueError('Check the filenames you specified...')
    return pattern


class TestVerifyPattern(unittest.TestCase):
    def test_verify_pattern_success(self):
        actual = verify_pattern('politicianCentrality_politicallNetwork')
        expected = 'politicianCentrality_politicallNetwork'
        self.assertEqual(actual, expected)

    def test_verify_pattern_exception(self):
        wrong_pattern = 'politicianCentrality_politicalNetwork'
        with self.assertRaises(ValueError) as e:
            verify_pattern(pattern=wrong_pattern)
        self.assertEqual(
            str(e.exception),
            "Check the filenames you specified..."
        )
