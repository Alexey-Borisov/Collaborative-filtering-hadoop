#!/usr/bin/python3


import os
import sys
from math import sqrt


precision = int(os.environ["float_precision"])

ij_prod_sum = 0.0
i_squares_sum = 0.0
j_squares_sum = 0.0
eps = 1e-9
for i, line in enumerate(sys.stdin):
    # Input format: (item_i, item_j) -> (rating_i, rating_j)
    key_part, value_part = line.rstrip().split('\t')
    if i != 0 and key_part != old_key_part:
        sim_ij = ij_prod_sum /  (sqrt(i_squares_sum) * sqrt(j_squares_sum) + eps)
        # save only positive similarities
        if sim_ij > 0:
            # Output format: (item_i, item_j) -> sim(i, j)
            print(f"{old_key_part}\t{sim_ij:.{precision}f}")
        ij_prod_sum = 0.0
        i_squares_sum = 0.0
        j_squares_sum = 0.0

    rating_i, rating_j = value_part.split(",")
    rating_i, rating_j = float(rating_i), float(rating_j)
    ij_prod_sum += rating_i * rating_j
    i_squares_sum += rating_i**2
    j_squares_sum += rating_j**2
    old_key_part = key_part

# last key
sim_ij = ij_prod_sum / (sqrt(i_squares_sum) * sqrt(j_squares_sum) + eps)
# save only positive similarities
if sim_ij > 0:
    # Output format: (item_i, item_j) -> sim(i, j)
    print(f"{old_key_part}\t{sim_ij:.{precision}f}")
