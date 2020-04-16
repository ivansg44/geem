#!/usr/bin/env python3

"""Tests ``mapping_cols.py``."""

import unittest

from scripts import mapping_cols


class TestGetColComponents(unittest.TestCase):
    parsing_exps = mapping_cols.get_parsing_exps()

    def test_empty_col(self):
        col = []
        parsing_exp = self.parsing_exps['day - integer']
        expected = {'day_int': []}
        actual = mapping_cols.get_col_components(col, parsing_exp)
        self.assertDictEqual(expected, actual)

    def test_case_insensitivity(self):
        col = [
            'mOn'
        ]
        parsing_exp = self.parsing_exps['weekday - 3 char']
        expected = {
            'weekday_abbr': [
                'mOn'
            ]
        }
        actual = mapping_cols.get_col_components(col, parsing_exp)
        self.assertDictEqual(expected, actual)

    def test_day_integer(self):
        col = [
            '', 'ham', '0', '1', '2', '9', '99', '10', '11', '19', '20',
            '2020', '30', '3030', '31', '3131'
        ]
        parsing_exp = self.parsing_exps['day - integer']
        expected = {
            'day_int': [
                None, None, None, '1', '2', '9', None, '10', '11', '19', '20',
                None, '30', None, '31', None
            ]
        }
        actual = mapping_cols.get_col_components(col, parsing_exp)
        self.assertDictEqual(expected, actual)

    def test_day_2_digit(self):
        col = [
            '', 'ham', '1', '0', '01', '02', '09', '0909', '10', '11',
            '19', '20', '2020', '30', '3030', '31', '3131'
        ]
        parsing_exp = self.parsing_exps['day - 2 digit']
        expected = {
            'day_dd': [
                None, None, None, None, '01', '02', '09', None, '10', '11',
                '19', '20', None, '30', None, '31', None
            ]
        }
        actual = mapping_cols.get_col_components(col, parsing_exp)
        self.assertDictEqual(expected, actual)
        self.assertDictEqual(expected, actual)

    def test_weekday_integer(self):
        col = [
            '', 'ham', '0', '1', '2', '7', '8', '77'
        ]
        parsing_exp = self.parsing_exps['weekday - integer']
        expected = {
            'weekday_int': [
                None, None, None, '1', '2', '7', None, None
            ]
        }
        actual = mapping_cols.get_col_components(col, parsing_exp)
        self.assertDictEqual(expected, actual)

    def test_weekday_3_char(self):
        col = [
            '', 'ham', 'mon', 'wed', 'wedwed'
        ]
        parsing_exp = self.parsing_exps['weekday - 3 char']
        expected = {
            'weekday_abbr': [
                None, None, 'mon', 'wed', None
            ]
        }
        actual = mapping_cols.get_col_components(col, parsing_exp)
        self.assertDictEqual(expected, actual)

    def test_weekday_word(self):
        col = [
            '', 'ham', 'monday', 'wednesday', 'wednesdaywednesday'
        ]
        parsing_exp = self.parsing_exps['weekday - word']
        expected = {
            'weekday_word': [
                None, None, 'monday', 'wednesday', None
            ]
        }
        actual = mapping_cols.get_col_components(col, parsing_exp)
        self.assertDictEqual(expected, actual)

    def test_month_integer(self):
        col = [
            '', 'ham', '0', '1', '2', '9', '99', '10', '1010', '11', '1111',
            '12', '1212'
        ]
        parsing_exp = self.parsing_exps['month - integer']
        expected = {
            'month_int': [
                None, None, None, '1', '2', '9', None, '10', None, '11', None,
                '12', None
            ]
        }
        actual = mapping_cols.get_col_components(col, parsing_exp)
        self.assertDictEqual(expected, actual)
        self.assertDictEqual(expected, actual)

    def test_month_2_digit(self):
        col = [
            '', 'ham', '0', '1', '00', '01', '02', '09', '0909', '10', '1010',
            '11', '1111', '12', '1212'
        ]
        parsing_exp = self.parsing_exps['month - 2 digit']
        expected = {
            'month_mm': [
                None, None, None, None, None, '01', '02', '09', None, '10',
                None, '11', None, '12', None
            ]
        }
        actual = mapping_cols.get_col_components(col, parsing_exp)
        self.assertDictEqual(expected, actual)

    def test_month_3_char(self):
        col = [
            '', 'ham', 'jan', 'may', 'maymay'
        ]
        parsing_exp = self.parsing_exps['month - 3 char']
        expected = {
            'month_abbr': [
                None, None, 'jan', 'may', None
            ]
        }
        actual = mapping_cols.get_col_components(col, parsing_exp)
        self.assertDictEqual(expected, actual)

    def test_month_word(self):
        col = [
            '', 'ham', 'january', 'may', 'maymay'
        ]
        parsing_exp = self.parsing_exps['month - word']
        expected = {
            'month_word': [
                None, None, 'january', 'may', None
            ]
        }
        actual = mapping_cols.get_col_components(col, parsing_exp)
        self.assertDictEqual(expected, actual)

    def test_year_4_digit(self):
        col = [
            '', 'ham', '1', '11', '111', '1111', '0000', '9999', '99999'
        ]
        parsing_exp = self.parsing_exps['year - 4 digit']
        expected = {
            'year_yyyy': [
                None, None, None, None, None, '1111', '0000', '9999', None
            ]
        }
        actual = mapping_cols.get_col_components(col, parsing_exp)
        self.assertDictEqual(expected, actual)

    def test_year_2_digit(self):
        col = [
            '', 'ham', '1', '11', '22', '00', '99', '999'
        ]
        parsing_exp = self.parsing_exps['year - 2 digit']
        expected = {
            'year_yy': [
                None, None, None, '11', '22', '00', '99', None
            ]
        }
        actual = mapping_cols.get_col_components(col, parsing_exp)
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
        parsing_exp = self.parsing_exps['date - iso 8601']
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
        actual = mapping_cols.get_col_components(col, parsing_exp)
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
        parsing_exp = self.parsing_exps['date - mm/dd/yy']
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
        actual = mapping_cols.get_col_components(col, parsing_exp)
        self.assertDictEqual(expected, actual)

    def test_integer(self):
        col = [
            '', 'ham', '1', '11', '0', '9', '090', '090 ham'
        ]
        parsing_exp = self.parsing_exps['integer']
        expected = {
            'integer': [
                None, None, '1', '11', '0', '9', '090', None
            ]
        }
        actual = mapping_cols.get_col_components(col, parsing_exp)
        self.assertDictEqual(expected, actual)

    def test_decimal(self):
        col = [
            '', 'ham', '1', '1.', '1.1', '11.1', '1.11', '0.0', '9.9',
            '9.9 ham'
        ]
        parsing_exp = self.parsing_exps['decimal']
        expected = {
            'integer': [
                None, None, None, None, '1', '11', '1', '0', '9', None
            ],
            'fractional': [
                None, None, None, None, '.1', '.1', '.11', '.0', '.9', None
            ]
        }
        actual = mapping_cols.get_col_components(col, parsing_exp)
        self.assertDictEqual(expected, actual)

    def test_boolean_1_0(self):
        col = [
            '', 'ham', '1', '0', '1 ham'
        ]
        parsing_exp = self.parsing_exps['boolean 1/0']
        expected = {
            'boolean_10': [
                None, None, '1', '0', None
            ]
        }
        actual = mapping_cols.get_col_components(col, parsing_exp)
        self.assertDictEqual(expected, actual)

    def test_boolean_y_n(self):
        col = [
            '', 'ham', 'y', 'n', 'yes'
        ]
        parsing_exp = self.parsing_exps['boolean y/n']
        expected = {
            'boolean_yn': [
                None, None, 'y', 'n', None
            ]
        }
        actual = mapping_cols.get_col_components(col, parsing_exp)
        self.assertDictEqual(expected, actual)

    def test_boolean_yes_no(self):
        col = [
            '', 'ham', 'yes', 'no', 'yes ham'
        ]
        parsing_exp = self.parsing_exps['boolean yes/no']
        expected = {
            'boolean_yes_no': [
                None, None, 'yes', 'no', None
            ]
        }
        actual = mapping_cols.get_col_components(col, parsing_exp)
        self.assertDictEqual(expected, actual)


class TestCreateCol(unittest.TestCase):
    def test_stub(self):
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
