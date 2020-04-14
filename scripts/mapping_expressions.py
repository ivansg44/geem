#!/usr/bin/env python3

"""TODO: document script"""

import argparse
import json
import re
import os

from definitions import BASE_DIR


def get_parsing_exps():
    """TODO: document function"""
    parsing_exps_json_path = \
        os.path.join(BASE_DIR, 'scripts', 'data', 'parsing_exps.json')
    with open(parsing_exps_json_path) as fp:
        return json.load(fp)


def parse_args(parsing_exps):
    """TODO: document function"""
    parser = argparse.ArgumentParser()
    parser.add_argument('parsing_expression', choices=parsing_exps.keys())
    parser.add_argument('column', nargs='*')
    parser.add_argument('--mapping_expression', choices=parsing_exps.keys())
    return parser.parse_args()


def get_col_components(col, parsing_exp):
    """TODO: document function"""
    compiled_exp = re.compile(parsing_exp['exp'], re.IGNORECASE)

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
    # compiled_exp = re.compile(parsing_exps[exp]['exp'], re.IGNORECASE)
    #
    # # Iterate over parameters in ``exp``.
    # # e.g., ``month_mm``, ``day_dd``, ``year_yy``
    # for expected_component in compiled_exp.groupindex.keys():
    #     # Raise an error if a parameter is missing from
    #     # ``col_components``.
    #     if expected_component not in col_components:
    #         msg = 'This column type cannot be converted into ' + exp
    #         raise argparse.ArgumentTypeError(msg)

    return []


def main():
    parsing_exps = get_parsing_exps()
    args = parse_args(parsing_exps)

    col_components = \
        get_col_components(args.column, parsing_exps[args.parsing_expression])
    if args.mapping_expression:
        return map_col(col_components, args.mapping_expression)
    return col_components


if __name__ == '__main__':
    main()
