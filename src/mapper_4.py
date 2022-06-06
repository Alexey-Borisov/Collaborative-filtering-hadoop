#!/usr/bin/python3


import os
import sys


current_file = os.environ['mapreduce_map_input_file']

for line in sys.stdin:
    # Input formats:
    #   rating.csv: user_id, item_id, rating, timestamp
    #   stage_3: (user_id, item_j) -> (item_i, rating_ui, sim(i, j))
    if current_file[-3:] == "csv":
        user_id, item_id, rating, timestamp = line.rstrip().split(',')
        if user_id == "userId":
            continue
        # Output format: (item_id, user_id) -> 'r'
        # flag that this item has already been rated
        print(f"{user_id},{item_id}\tr")
    else:
        # emit without change
        print(line, end='')



