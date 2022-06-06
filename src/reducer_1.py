#!/usr/bin/python3


import os
import sys


precision = int(os.environ["float_precision"])

items_list = []
ratings_list = []
for i, line in enumerate(sys.stdin):
    # Input format: user_id -> (item_id, norm_rating)
    key_part, value_part = line.rstrip().split('\t')
    if i != 0 and key_part != old_key_part:
        mean_rating = sum(ratings_list) / len(ratings_list)
        items_ratings_string = ""
        for i in range(len(items_list)):
            items_ratings_string += items_list[i] + f",{ratings_list[i]:.{precision}f},"
        # Output format: user_id -> mean_user_rating, (item_1, rating_1), ... , (item_n, rating_n)
        print(f"{old_key_part}\t{mean_rating:.{precision}f},{items_ratings_string[:-1]}")
        items_list = []
        ratings_list = []

    item_id, rating = value_part.split(",")
    items_list.append(item_id)
    ratings_list.append(float(rating))
    old_key_part = key_part

# last key
mean_rating = sum(ratings_list) / len(ratings_list)
items_ratings_string = ""
for i in range(len(items_list)):
    items_ratings_string += items_list[i] + f",{ratings_list[i]:.{precision}f},"
# Output format: user_id -> mean_user_rating, (item_1, rating_1), ... , (item_n, rating_n)
print(f"{old_key_part}\t{mean_rating:.{precision}f},{items_ratings_string[:-1]}")
