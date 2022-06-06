#!/usr/bin/python3


import os
import sys
from itertools import combinations



precision = int(os.environ["float_precision"])

for line in sys.stdin:
    # Input format: user_id -> mean_user_rating, (item_1, rating_1), ... , (item_n, rating_n)
    user_id, other = line.rstrip().split('\t')

    other = other.split(',')
    mean_user_rating = float(other[0])
    items = other[1::2]

    # calculate differences (rating_i - mean_user_rating) because these differences are used in sim(i,j) calculations
    ratings = list(map(lambda x: float(x) - mean_user_rating, other[2::2]))

    # get all combinations (item_i, item_j) and corresponding (rating_i, rating_j)
    items_combinations = combinations(items, 2)
    ratings_combinations = combinations(ratings, 2)

    # emit pairs (item_i, item_j) -> (rating_i, rating_j) and consider item_i <= item_j
    for items_comb, ratings_comb in zip(items_combinations, ratings_combinations):

        if items_comb[0] <= items_comb[1]:
            print(f"{items_comb[0]},{items_comb[1]}\t{ratings_comb[0]:.{precision}f},{ratings_comb[1]:.{precision}f}")
        else:
            print(f"{items_comb[1]},{items_comb[0]}\t{ratings_comb[1]:.{precision}f},{ratings_comb[0]:.{precision}f}")



