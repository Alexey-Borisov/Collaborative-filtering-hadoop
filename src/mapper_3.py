#!/usr/bin/python3


import os
import sys


current_file = os.environ['mapreduce_map_input_file']

for line in sys.stdin:
    # Input formats:
    #   rating.csv: user_id, item_id, rating, timestamp
    #   stage_2: (item_i, item_j) -> sim(i, j)
    if current_file[-3:] == "csv":
        user_id, item_id, rating, timestamp = line.rstrip().split(',')
        if user_id == "userId":
            continue
        # Output format: item_id -> u(user_id, rating)
        # 'u' to know that this output is from ratings.csv
        print(f"{item_id}\tu{user_id},{rating}")
    else:
        items, similarity = line.rstrip().split('\t')
        item_1, item_2 = items.split(',')
        # Output format: item_i -> (item_j, sim(i, j))
        print(f"{item_1}\t{item_2},{similarity}")
        print(f"{item_2}\t{item_1},{similarity}")


