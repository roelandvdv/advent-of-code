# Started over in script, much from notebook

from pathlib import Path
import re

data_path = Path(__file__).parent.parent / "data/day19test.txt"

# Load data
with open(data_path, "r") as f:
    input = f.read()

parts = input.split("\n\n")
rules = parts[0]
msgs = parts[1].split("\n")

rule_dict = {int(rule.split(":")[0]):rule.split(":")[1][1:] for rule in rules.split("\n")}
print(rule_dict)

# Parse rules
def parse_rule_dict(rule_dict: dict):

    rule_dict_parsed = {}
    for n, rule_to_parse in rule_dict.items():
        if "|" in rule_to_parse:
            rule_type = "two_sequences"
            parts = rule_to_parse.split("|")
            value = [[int(value) for value in part.strip().split(" ")] for part in parts]

        elif "a" in rule_to_parse or "b" in rule_to_parse:
            rule_type = "letter"
            value = rule_to_parse.strip('"')

        else:
            rule_type = "sequence"
            value = [int(value) for value in rule_to_parse.strip().split(" ")]

        rule_dict_parsed[n] = (rule_type, value)

    return rule_dict_parsed

rule_dict_parsed = parse_rule_dict(rule_dict)
print(rule_dict_parsed)


