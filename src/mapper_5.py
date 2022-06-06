#!/usr/bin/python3


import os
import sys
import pandas as pd


movies_df = pd.read_csv("movies.csv", index_col="movieId")

for line in sys.stdin:
    # Input formats:  (user_id, item_id) -> predicted_rating

    key_part, value_part = line.rstrip().split('\t')
    user_id, item_id = key_part.split(',')
    # Output format: user_id -> (item_name, predicted_rating)
    print(f"{user_id}\t{movies_df.loc[int(item_id)].title},{value_part}")




