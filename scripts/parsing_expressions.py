#!/usr/bin/env python3

"""TODO: document script"""

import argparse
import re

parsing_exps = {
    'day - integer':
        r'^(?P<day_int>[1-9]|[12][0-9]|30|31)$',
    'day - 2 digit':
        r'^(?P<day_dd>0[1-9]|[12][0-9]|30|31)$',
    'weekday - integer':
        r'^(?P<weekday_int>[1-7])$',
    'weekday - 3 char':
        r'^(?P<weekday_abbr>(mon|tue|wed|thu|fri|sat|sun))$',
    'weekday - word':
        r'^(?P<weekday_word>'
        r'(monday|tuesday|wednesday|thursday|friday|saturday|sunday))$',
    'month - integer':
        r'^(?P<month_int>[1-9]|10|11|12)$',
    'month - 2 digit':
        r'^(?P<month_mm>0[1-9]|10|11|12)$',
    'month - 3 char':
        r'^(?P<month_abbr>'
        r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))$',
    'month - word':
        r'^(?P<month_word>'
        r'(january|february|march|april|may|june|july'
        r'|august|september|october|november|december))$',
    'year - 4 digit':
        r'^(?P<year_yyyy>\d{4})$',
    'year - 2 digit':
        r'^(?P<year_yy>\d\d)$',
    'date - iso 8601':
        r'^(?P<year_yyyy>\d{4})'
        r'-(?P<month_mm>0[1-9]|10|11|12)'
        r'-(?P<day_dd>0[1-9]|[12][0-9]|30|31)$',
    'date - mm/dd/yy':
        r'^(?P<month_mm>0[1-9]|10|11|12)'
        r'/(?P<day_dd>0[1-9]|[12][0-9]|30|31)'
        r'/(?P<year_yy>\d\d)$',
    'integer':
        r'^(?P<integer>\d+)$',
    'decimal':
        r'^(?P<integer>\d+)(?P<fractional>\.\d+)$',
    'boolean 1/0':
        r'^(?P<boolean_10>[01])$',
    'boolean y/n':
        r'^(?P<boolean_yn>[yn])$',
    'boolean yes/no':
        r'^(?P<boolean_yes_no>yes|no)$'
}


def main(exp, col):
    """TODO: document function"""
    compiled_exp = re.compile(parsing_exps[exp], re.IGNORECASE)

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('expression', choices=parsing_exps.keys())
    parser.add_argument('column', nargs='*')
    args = parser.parse_args()
    main(args.expression, args.column)
