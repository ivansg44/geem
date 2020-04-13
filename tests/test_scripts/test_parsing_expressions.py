#!/usr/bin/env python3

"""Tests ``parsing_expressions.py``."""

import unittest

from scripts import parsing_expressions


class TestParsingExpressions(unittest.TestCase):
    def test_empty_col(self):
        col = []
        expected = {'day_int': []}
        actual = parsing_expressions.main('day - integer', col)
        self.assertDictEqual(expected, actual)

    def test_case_insensitivity(self):
        col = [
            'mOn'
        ]
        expected = {
            'weekday_abbr': [
                'mOn'
            ]
        }
        actual = parsing_expressions.main('weekday - 3 char', col)
        self.assertDictEqual(expected, actual)

    def test_day_integer(self):
        col = [
            '', 'ham', '0', '1', '2', '9', '99', '10', '11', '19', '20',
            '2020', '30', '3030', '31', '3131'
        ]
        expected = {
            'day_int': [
                None, None, None, '1', '2', '9', None, '10', '11', '19', '20',
                None, '30', None, '31', None
            ]
        }
        actual = parsing_expressions.main('day - integer', col)
        self.assertDictEqual(expected, actual)

    def test_day_2_digit(self):
        col = [
            '', 'ham', '1', '0', '01', '02', '09', '0909', '10', '11',
            '19', '20', '2020', '30', '3030', '31', '3131'
        ]
        expected = {
            'day_dd': [
                None, None, None, None, '01', '02', '09', None, '10', '11',
                '19', '20', None, '30', None, '31', None
            ]
        }
        actual = parsing_expressions.main('day - 2 digit', col)
        self.assertDictEqual(expected, actual)
        self.assertDictEqual(expected, actual)

    def test_weekday_integer(self):
        col = [
            '', 'ham', '0', '1', '2', '7', '8', '77'
        ]
        expected = {
            'weekday_int': [
                None, None, None, '1', '2', '7', None, None
            ]
        }
        actual = parsing_expressions.main('weekday - integer', col)
        self.assertDictEqual(expected, actual)

    def test_weekday_3_char(self):
        col = [
            '', 'ham', 'mon', 'wed', 'wedwed'
        ]
        expected = {
            'weekday_abbr': [
                None, None, 'mon', 'wed', None
            ]
        }
        actual = parsing_expressions.main('weekday - 3 char', col)
        self.assertDictEqual(expected, actual)

    def test_weekday_word(self):
        col = [
            '', 'ham', 'monday', 'wednesday', 'wednesdaywednesday'
        ]
        expected = {
            'weekday_word': [
                None, None, 'monday', 'wednesday', None
            ]
        }
        actual = parsing_expressions.main('weekday - word', col)
        self.assertDictEqual(expected, actual)

    def test_month_integer(self):
        col = [
            '', 'ham', '0', '1', '2', '9', '99', '10', '1010', '11', '1111',
            '12', '1212'
        ]
        expected = {
            'month_int': [
                None, None, None, '1', '2', '9', None, '10', None, '11', None,
                '12', None
            ]
        }
        actual = parsing_expressions.main('month - integer', col)
        self.assertDictEqual(expected, actual)
        self.assertDictEqual(expected, actual)

    def test_month_2_digit(self):
        col = [
            '', 'ham', '0', '1', '00', '01', '02', '09', '0909', '10', '1010',
            '11', '1111', '12', '1212'
        ]
        expected = {
            'month_mm': [
                None, None, None, None, None, '01', '02', '09', None, '10',
                None, '11', None, '12', None
            ]
        }
        actual = parsing_expressions.main('month - 2 digit', col)
        self.assertDictEqual(expected, actual)

    def test_month_3_char(self):
        col = [
            '', 'ham', 'jan', 'may', 'maymay'
        ]
        expected = {
            'month_abbr': [
                None, None, 'jan', 'may', None
            ]
        }
        actual = parsing_expressions.main('month - 3 char', col)
        self.assertDictEqual(expected, actual)

    def test_month_word(self):
        col = [
            '', 'ham', 'january', 'may', 'maymay'
        ]
        expected = {
            'month_word': [
                None, None, 'january', 'may', None
            ]
        }
        actual = parsing_expressions.main('month - word', col)
        self.assertDictEqual(expected, actual)

    def test_year_4_digit(self):
        col = [
            '', 'ham', '1', '11', '111', '1111', '0000', '9999', '99999'
        ]
        expected = {
            'year_yyyy': [
                None, None, None, None, None, '1111', '0000', '9999', None
            ]
        }
        actual = parsing_expressions.main('year - 4 digit', col)
        self.assertDictEqual(expected, actual)

    def test_year_2_digit(self):
        col = [
            '', 'ham', '1', '11', '22', '00', '99', '999'
        ]
        expected = {
            'year_yy': [
                None, None, None, '11', '22', '00', '99', None
            ]
        }
        actual = parsing_expressions.main('year - 2 digit', col)
        self.assertDictEqual(expected, actual)

    def test_date_iso_8601(self):
        col = [
            '--', 'ham-ham-ham', '2222-11-22', '22221122', '2222-1122',
            '222211-22', '222-11-22', '22-11-22', '2-11-22', '-11-22',
            '22222-11-22', '0000-11-22', '9999-11-22', '2222-1-22',
            '2222--22', '2222-111-22', '2222-00-22', '2222-01-22',
            '2222-09-22', '2222-12-22', '2222-13-22', '2222-11-2', '2222-11-',
            '2222-11-222', '2222-11-00', '2222-11-01', '2222-11-09',
            '2222-11-10', '2222-11-19', '2222-11-20', '2222-11-29',
            '2222-11-30', '2222-11-31', '2222-11-32'
        ]
        expected = {
            'year_yyyy': [
                None, None, '2222', None, None, None, None, None, None, None,
                None, '0000', '9999', None, None, None, None, '2222', '2222',
                '2222', None, None, None, None, None, '2222', '2222', '2222',
                '2222', '2222', '2222', '2222', '2222', None
            ],
            'month_mm': [
                None, None, '11', None, None, None, None, None, None, None,
                None, '11', '11', None, None, None, None, '01', '09', '12',
                None, None, None, None, None, '11', '11', '11', '11', '11',
                '11', '11', '11', None
            ],
            'day_dd': [
                None, None, '22', None, None, None, None, None, None, None,
                None, '22', '22', None, None, None, None, '22', '22', '22',
                None, None, None, None, None, '01', '09', '10', '19', '20',
                '29', '30', '31', None
            ]
        }
        actual = parsing_expressions.main('date - iso 8601', col)
        self.assertDictEqual(expected, actual)

    def test_date_mm_dd_yy(self):
        col = [
            '//', 'ham/ham/ham', '11/22/22', '112222', '11/2222',
            '1122/22', '11/22/2', '11/22/', '11/22/222', '11/22/00', 
            '11/22/99', '1/22/2222', '/22/22', '111/22/22', '00/22/22',
            '01/22/22', '09/22/22', '12/22/22', '13/22/22', '11/2/22',
            '11//22', '11/222/22', '11/00/22', '11/01/22', '11/09/22',
            '11/10/22', '11/19/22', '11/20/22', '11/29/22', '11/30/22',
            '11/31/22', '11/32/22'
        ]
        expected = {
            'year_yy': [
                None, None, '22', None, None, None, None, None, None, '00',
                '99', None, None, None, None, '22', '22', '22', None, None,
                None, None, None, '22', '22', '22', '22', '22', '22', '22',
                '22', None
            ],
            'month_mm': [
                None, None, '11', None, None, None, None, None, None, '11',
                '11', None, None, None, None, '01', '09', '12', None, None,
                None, None, None, '11', '11', '11', '11', '11', '11', '11',
                '11', None
            ],
            'day_dd': [
                None, None, '22', None, None, None, None, None, None, '22',
                '22', None, None, None, None, '22', '22', '22', None, None,
                None, None, None, '01', '09', '10', '19', '20', '29', '30',
                '31', None
            ]
        }
        actual = parsing_expressions.main('date - mm/dd/yy', col)
        self.assertDictEqual(expected, actual)

    def test_integer(self):
        col = [
            '', 'ham', '1', '11', '0', '9', '090', '090 ham'
        ]
        expected = {
            'integer': [
                None, None, '1', '11', '0', '9', '090', None
            ]
        }
        actual = parsing_expressions.main('integer', col)
        self.assertDictEqual(expected, actual)

    def test_decimal(self):
        col = [
            '', 'ham', '1', '1.', '1.1', '11.1', '1.11', '0.0', '9.9',
            '9.9 ham'
        ]
        expected = {
            'integer': [
                None, None, None, None, '1', '11', '1', '0', '9', None
            ],
            'fractional': [
                None, None, None, None, '.1', '.1', '.11', '.0', '.9', None
            ]
        }
        actual = parsing_expressions.main('decimal', col)
        self.assertDictEqual(expected, actual)

    def test_boolean_1_0(self):
        col = [
            '', 'ham', '1', '0', '1 ham'
        ]
        expected = {
            'boolean_10': [
                None, None, '1', '0', None
            ]
        }
        actual = parsing_expressions.main('boolean 1/0', col)
        self.assertDictEqual(expected, actual)

    def test_boolean_y_n(self):
        col = [
            '', 'ham', 'y', 'n', 'yes'
        ]
        expected = {
            'boolean_yn': [
                None, None, 'y', 'n', None
            ]
        }
        actual = parsing_expressions.main('boolean y/n', col)
        self.assertDictEqual(expected, actual)

    def test_boolean_yes_no(self):
        col = [
            '', 'ham', 'yes', 'no', 'yes ham'
        ]
        expected = {
            'boolean_yes_no': [
                None, None, 'yes', 'no', None
            ]
        }
        actual = parsing_expressions.main('boolean yes/no', col)
        self.assertDictEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
