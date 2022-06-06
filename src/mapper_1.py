#!/usr/bin/python3


import os
import sys


precision = int(os.environ["float_precision"])

for line in sys.stdin:
    # Input format: user_id, item_id, rating, timestamp
    user_id, item_id, rating, timestamp = line.split(',')
    # skip header
    if user_id == "userId":
        continue
    normalized_rating = (float(rating) - 1.0) / 4.0 # normalize rating to [0, 1] interval
    # Output format: user_id -> (item_id, norm_rating)
    print(f"{user_id}\t{item_id},{normalized_rating:.{precision}f}")


