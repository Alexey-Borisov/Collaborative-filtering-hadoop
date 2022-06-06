#!/usr/bin/python3


import os
import sys
import numpy as np


precision = int(os.environ["float_precision"])

pairs_list = []
for i, line in enumerate(sys.stdin):
    # Input format: user_id -> (item_name, predicted_rating)
    key_part, value_part = line.rstrip().split('\t')
    if i != 0 and key_part != old_key_part:
        pairs_list = sorted(pairs_list)
        result_string = f"{old_key_part}"
        for pair in pairs_list[:100]:
            result_string += f"@{(-pair[0]):.{precision}f}%{pair[1]}"
        # Output format:
        print(f"{result_string}")
        pairs_list = []

    # collect items and similarities
    comma = value_part.rfind(',')
    rating = -float(value_part[comma+1:])
    item_name = value_part[:comma]
    pairs_list.append((rating, item_name))
    old_key_part = key_part

# last key
pairs_list = sorted(pairs_list)
result_string = f"{old_key_part}"
for pair in pairs_list[:100]:
    result_string += f"@{-pair[0]:.{precision}f}%{pair[1]}"
# Output format:
print(f"{result_string}")
pairs_list = []
