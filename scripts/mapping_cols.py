#!/usr/bin/env python3

"""TODO: document script"""

import argparse
import json
import re
import os

from definitions import BASE_DIR
from scripts import synthesis_exps


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


def get_col_components(col, parsing_exp_dict):
    """TODO: document function"""
    compiled_exp = re.compile(parsing_exp_dict['exp'], re.IGNORECASE)

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


def map_col(col_components, mapping_exp, parsing_exp):
    """TODO: document function"""
    try:
        mapping_fn = synthesis_exps.dispatcher[mapping_exp][parsing_exp]
    except KeyError:
        msg = parsing_exp + ' cannot be converted into ' + mapping_exp
        raise argparse.ArgumentTypeError(msg)

    return mapping_fn(col_components)


def main():
    parsing_exps = get_parsing_exps()
    args = parse_args(parsing_exps)
    parsing_exp = args.parsing_expression
    mapping_exp = args.mapping_expression

    col_components = \
        get_col_components(args.column, parsing_exps[parsing_exp])
    if mapping_exp:
        if parsing_exp == mapping_exp:
            return args.column
        return map_col(col_components, mapping_exp, parsing_exp)
    return col_components


if __name__ == '__main__':
    main()
