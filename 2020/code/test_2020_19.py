import pytest

from day19 import parse_rule_dict

rule_dict_1 = {
    0: '4 1 5',
    1: '2 3 | 3 2',
    4: '"a"',
}

expected_rule_dict_parsed_1 = {
    0: ('sequence', [4, 1, 5]),
    1: ('two_sequences', [[2, 3], [3, 2]]),
    4: ('letter', "a"),
}

def test_parse_rule_dict_1():
    """Test transforming rule dict."""
    assert parse_rule_dict(rule_dict_1) == expected_rule_dict_parsed_1

rule_dict_2 = {
    0: '4 1 5 6',
    1: '42',
    2: '2 | 3 2 1'
}

expected_rule_dict_parsed_2 = {
    0: ('sequence', [4, 1, 5, 6]),
    1: ('sequence', [42]),
    2: ('two_sequences', [[2], [3, 2, 1]])
}

def test_parse_rule_dict_2():
    """Test transforming rule dict."""
    assert parse_rule_dict(rule_dict_2) == expected_rule_dict_parsed_2