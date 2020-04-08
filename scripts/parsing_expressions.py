#!/usr/bin/env python3

import argparse
import re

parsing_exps = {
    'day - integer': '(?P<day_int>[123]?\\d)'
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
