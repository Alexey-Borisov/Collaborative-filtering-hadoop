#!/usr/bin/python3


import os
import sys


precision = int(os.environ["float_precision"])

sim_sum = 0.0
sim_r_sum = 0.0
skip_flag = False
eps = 1e-9
for i, line in enumerate(sys.stdin):
    # Two input formats:
    #   1) (item_id, user_id) -> 'r'
    #   2) (user_id, item_j) -> (item_i, rating_ui, sim(i, j)) # НЕ НУЖЕН ITEM
    key_part, value_part = line.rstrip().split('\t')
    if skip_flag is True and key_part == old_key_part:
        continue
    elif i != 0 and key_part != old_key_part:
        predicted_rating = sim_r_sum / (sim_sum + eps)
        # Output format: (user_id, item_id) -> predicted_rating
        print(f"{old_key_part}\t{predicted_rating:.{precision}f}")
        sim_sum = 0.0
        sim_r_sum = 0.0

    skip_flag = False
    if value_part == "r":
        skip_flag = True
        old_key_part = key_part
        sim_sum = 0.0
        sim_r_sum = 0.0
    else:
        item_id, rating, sim = value_part.split(',')
        rating, sim = float(rating), float(sim)
        sim_sum += sim
        sim_r_sum += sim * rating
        old_key_part = key_part

# last key if not skipped
if skip_flag is False:
    predicted_rating = sim_r_sum / (sim_sum + eps)
    # Output format: (user_id, item_id) -> predicted_rating
    print(f"{old_key_part}\t{predicted_rating:.{precision}f}")
