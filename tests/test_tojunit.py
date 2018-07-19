from __future__ import absolute_import

import unittest

import pkg_resources

from pylint2junit.parse import parse_input_lines
from pylint2junit.tojunit import pylint_to_junit


class TestToJunit(unittest.TestCase):
    def test_defaultPyLint_expected(self):
        sample_in = pkg_resources.resource_string(
            'tests.data',
            'default_sample.txt'
        ).decode("utf-8")
        sample_expected = pkg_resources.resource_string(
            'tests.data',
            'default_sample.xml'
        ).decode("utf-8")
        xml_str = pylint_to_junit(parse_input_lines(sample_in.split('\n')))
        self.assertEqual(sample_expected, xml_str)
