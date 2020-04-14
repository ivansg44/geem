#!/usr/bin/env python3

"""TODO: document script"""

import argparse
import re

parsing_exps = {
    'day - integer': {
        'exp': r'^(?P<day_int>[1-9]|[12][0-9]|30|31)$',
        'unit': 'day',
        'unit_uri': 'UO_0000033'
    },
    'day - 2 digit': {
        'exp': r'^(?P<day_dd>0[1-9]|[12][0-9]|30|31)$',
        'unit': 'day',
        'unit_uri': 'UO_0000033'
    },
    'weekday - integer': {
        'exp': r'^(?P<weekday_int>[1-7])$',
        'unit': 'day',
        'unit_uri': 'UO_0000033'
    },
    'weekday - 3 char': {
        'exp': r'^(?P<weekday_abbr>(mon|tue|wed|thu|fri|sat|sun))$',
        'unit': 'day',
        'unit_uri': 'UO_0000033'
    },
    'weekday - word': {
        'exp': r'^(?P<weekday_word>'
               r'(monday|tuesday|wednesday|thursday|friday|saturday|sunday))$',
        'unit': 'day',
        'unit_uri': 'UO_0000033'
    },
    'month - integer': {
        'exp': r'^(?P<month_int>[1-9]|10|11|12)$',
        'unit': 'month',
        'unit_uri': 'UO_0000035'
    },
    'month - 2 digit': {
        'exp': r'^(?P<month_mm>0[1-9]|10|11|12)$',
        'unit': 'month',
        'unit_uri': 'UO_0000035'
    },
    'month - 3 char': {
        'exp': r'^(?P<month_abbr>'
               r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))$',
        'unit': 'month',
        'unit_uri': 'UO_0000035'
    },
    'month - word': {
        'exp': r'^(?P<month_word>'
               r'(january|february|march|april|may|june|july'
               r'|august|september|october|november|december))$',
        'unit': 'month',
        'unit_uri': 'UO_0000035'
    },
    'year - 4 digit': {
        'exp': r'^(?P<year_yyyy>\d{4})$',
        'unit': 'year',
        'unit_uri': 'UO_0000036'
    },
    'year - 2 digit': {
        'exp': r'^(?P<year_yy>\d\d)$',
        'unit': 'year',
        'unit_uri': 'UO_0000036'
    },
    'date - iso 8601': {
        'exp': r'^(?P<year_yyyy>\d{4})'
               r'-(?P<month_mm>0[1-9]|10|11|12)'
               r'-(?P<day_dd>0[1-9]|[12][0-9]|30|31)$',
    },
    'date - mm/dd/yy': {
        'exp': r'^(?P<month_mm>0[1-9]|10|11|12)'
               r'/(?P<day_dd>0[1-9]|[12][0-9]|30|31)'
               r'/(?P<year_yy>\d\d)$',
    },
    'integer': {
        'exp': r'^(?P<integer>\d+)$',
    },
    'decimal': {
        'exp': r'^(?P<integer>\d+)(?P<fractional>\.\d+)$',
    },
    'boolean 1/0': {
        'exp': r'^(?P<boolean_10>[01])$',
    },
    'boolean y/n': {
        'exp': r'^(?P<boolean_yn>[yn])$',
    },
    'boolean yes/no': {
        'exp': r'^(?P<boolean_yes_no>yes|no)$'
    }
}


def get_col_components(col, exp):
    """TODO: document function"""
    compiled_exp = re.compile(parsing_exps[exp]['exp'], re.IGNORECASE)

    # e.g. ``{'month_mm': [], 'day_dd': [], 'year_yy': []}``
    col_components = {x: [] for x in compiled_exp.groupindex}

    for val in col:
        match = compiled_exp.match(val)
        for component in col_components:
            if match:
                col_components[component] += [match.group(component)]
            else:
                col_components[component] += [None]

    return col_components


def map_col(col_components, exp):
    """TODO: document function"""
    compiled_exp = re.compile(parsing_exps[exp]['exp'], re.IGNORECASE)

    # Iterate over parameters in ``exp``.
    # e.g., ``month_mm``, ``day_dd``, ``year_yy``
    for expected_component in compiled_exp.groupindex.keys():
        # Raise an error if a parameter is missing from
        # ``col_components``.
        if expected_component not in col_components:
            msg = 'This column type cannot be converted into ' + exp
            raise argparse.ArgumentTypeError(msg)

    return []


def main(args_):
    col_components = get_col_components(args_.column, args_.parsing_expression)
    if args_.mapping_expression:
        return map_col(col_components, args_.mapping_expression)
    return col_components


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('parsing_expression', choices=parsing_exps.keys())
    parser.add_argument('column', nargs='*')
    parser.add_argument('--mapping_expression', choices=parsing_exps.keys())
    args = parser.parse_args()
    main(args)
