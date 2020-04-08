#!/usr/bin/env python3

import argparse
import re

parsing_exps = {
    'day - integer':
        '(?P<day_int>[123]?\\d)',
    'day - 2 digit':
        '(?P<day_dd>[0123]\\d)',
    'weekday - integer':
        '(?P<weekday_int>[1-7])',
    'weekday - 3 char':
        '(?P<weekday_abbr>(mon|tue|wed|thu|fri|sat|sun))',
    'weekday - word':
        '(?P<weekday_word>'
        '(monday|tuesday|wednesday|thursday|friday|saturday|sunday))',
    'month - integer':
        '(?P<month_int>\\d?\\d)',
    'month - 2 digit':
        '(?P<month_mm>\\d\\d)',
    'month - 3 char':
        '(?P<month_abbr>(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))',
    'month - word':
        '(?P<month_word>'
        '(january|february|march|april|may|june|july'
        '|august|september|october|november|december))',
    'year - 4 digit':
        '(?P<year_yyyy>\\d{4})',
    'year - 2 digit':
        '(?P<year_yy>\\d\\d)',
    'year - 19yy':
        '(?P<year_yy>\\d\\d)',
    'date - iso 8601':
        '(?P<year_yyyy>\\d{4})-(?P<month_mm>\\d\\d)-(?P<day_dd>\\d?\\d)',
    'Date - mm/dd/yy':
        '(?P<month_mm>\\d{4})/(?P<day_dd>\\d\\d)/(?P<year_yy>\\d?\\d)',
    'integer':
        '(?P<integer>\\d+)',
    'decimal':
        '(?P<integer>\\d+)(?P<fractional>\\.\\d+)'
}


def main(exp, col):
    compiled_exp = re.compile(parsing_exps[exp])

    # e.g. ``{'month_mm': [], 'day_dd': [], 'year_yy': []}``
    col_components = {x: [] for x in compiled_exp.groupindex}

    for val in col:
        match = compiled_exp.match(val)
        for component in col_components:
            if match:
                col_components[component] += [match.group(component)]
            else:
                col_components[component] += [None]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('expression', choices=parsing_exps.keys())
    parser.add_argument('column', nargs='*')
    args = parser.parse_args()
    main(args.expression, args.column)
