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


def get_synthesis_exps():
    """TODO: document function"""
    synthesis_exps_json_path = \
        os.path.join(BASE_DIR, 'scripts', 'data', 'synthesis_exps.json')
    with open(synthesis_exps_json_path) as fp:
        return json.load(fp)


def parse_args(parsing_exps, synthesis_exps):
    """TODO: document function"""
    parser = argparse.ArgumentParser()
    parser.add_argument('parsing_expression', choices=parsing_exps.keys())
    parser.add_argument('column', nargs='*')
    parser.add_argument('--mapping_expression', choices=synthesis_exps.keys())
    return parser.parse_args()


def get_col_components(col, parsing_exp_dict):
    """TODO: document function"""
    compiled_exp = re.compile(parsing_exp_dict['exp'], re.IGNORECASE)
    col_matches = [compiled_exp.match(val) for val in col]

    # e.g. ``{'month_mm': [], 'day_dd': [], 'year_yy': []}``
    col_components = {x: [] for x in compiled_exp.groupindex}

    def helper(k):
        return [match.group(k) if match else None for match in col_matches]

    return {k: helper(k) for k, v in col_components.items()}


def create_col(col_components, synthesis_exp, col_len):
    """TODO: document function"""
    col_components_items = col_components.items()

    def helper(i):
        mapping = {k: v[i] for k, v in col_components_items}
        if None in mapping.values():
            return None
        return synthesis_exp.format_map(mapping)

    ret = [helper(i) for i in range(col_len)]
    return ret


def main():
    parsing_exps = get_parsing_exps()
    synthesis_exps = get_synthesis_exps()
    args = parse_args(parsing_exps, synthesis_exps)
    parsing_exp = args.parsing_expression
    mapping_exp = args.mapping_expression

    col_components = \
        get_col_components(args.column, parsing_exps[parsing_exp])
    if mapping_exp:
        # TODO: map col components
        # if parsing_exp == mapping_exp:
        #     return args.column
        col_len = len(args.column)
        return create_col(col_components, synthesis_exps[mapping_exp], col_len)
    return col_components


if __name__ == '__main__':
    main()
