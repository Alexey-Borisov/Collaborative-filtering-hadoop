#!/usr/bin/python3


import os
import sys
from itertools import product


users_list = []
sim_list = []
for i, line in enumerate(sys.stdin):
    # Two input formats:
    #   1) item_id -> u(user_id, rating)
    #   2) item_i -> (item_j, sim(i, j))
    key_part, value_part = line.rstrip().split('\t')
    if i != 0 and key_part != old_key_part:
        gen = product(users_list, sim_list)
        for elem in gen:
            # Output format: (user_id, item_j) -> (item_i, rating_ui, sim(i, j))
            print(f"{elem[0][0]},{elem[1][0]}\t{old_key_part},{elem[0][1]},{elem[1][1]}")
        users_list = []
        sim_list = []

    if value_part[0] == 'u':
        # collect users and ratings
        user_id, rating = value_part[1:].split(',')
        users_list.append((user_id, rating))
    else:
        # collect items and similarities
        other_item, sim = value_part.split(',')
        sim_list.append((other_item, sim))
    old_key_part = key_part

# last key
gen = product(users_list, sim_list)
for elem in gen:
    # Output format: (user_id, item_j) -> (item_i, rating_ui, sim(i, j))
    print(f"{elem[0][0]},{elem[1][0]}\t{old_key_part},{elem[0][1]},{elem[1][1]}")
