# #!/usr/local/bin/python
# -*- coding: utf-8 -*-
# basic imports
import pandas as pd
import numpy as np

# custom functions
# 1. step 1: locate data
from findRelations import *
# step 2: modify and concat data
from concatData import add_timestamp_and_concat

# plot
import matplotlib.pyplot as plt

# IMPORTANT:
# TO DO: CHECK ASSUMPTION BEFORE RECONSTRUCT FACTION-BASED IV
# regarding the community detection algorithm
# the unsupervised method implies no ground truth
# it categorizes politicians into clusters *EVERY YEAR*, and
# so faction id is
# 1. categorical
# 2. needs to transformed into new categorical variable by year
# faction id also has no meaning itself, so it makes sense if
# politicians in faction 1-2000 and politicians in faction 1-2001 have no overlap.


def transform_factions_id(df):
    df['id'] = None
    new_df = pd.DataFrame()
    for i, (n, g) in enumerate(df.groupby(['faction_id', 'year'])):
        g['id'] = i
        new_df = new_df.append(g)

    new_df.set_index('id', inplace=True)
    return new_df


def load_politicians():

    # to modify the relations type you need, go to findRelations.py
    _, _, politicianPolCentrality = find_data()

    # call modify and concat data
    polFactions_df = add_timestamp_and_concat(politicianPolCentrality)
    print("Shape of politicians data:", polFactions_df.shape)

    # examine the variables
    polFactions_df = polFactions_df.rename(
        columns={'commuinity_id': 'faction_id'})

    polFactions_df = transform_factions_id(polFactions_df)
    print(f'Transformed politicians data: {polFactions_df.shape}')
    print(f'Number of year-varying factions: {polFactions_df.index.nunique()}')

    # check id for same year same faction_id
    test = polFactions_df[(polFactions_df.year == 2000) &
                          (polFactions_df.faction_id == 3)]
    result = all(element == test.index[0] for element in test.index)
    print("Passed check of transformed faction id's: ", result)
    return polFactions_df


def calculate_factions(polFactions_df):

    factions_df = polFactions_df.reset_index()

    centrality_columns = [
        x for x in factions_df.columns if x.endswith('Centrality')]

    factions_df = factions_df.groupby(['faction_id', 'year'])[centrality_columns].aggregate(
        ['sum', 'max', 'mean', 'count']
    )

    factions_df.columns = [''.join(col).strip()
                           for col in factions_df.columns.values]
    # check how many politicians belong to a faction defined based on *YEAR*
    factions_df.degreeCentralitycount.describe()
    # max: 468, min: 1, median: 69, mean: 74

    # how many factions (based on *YEAR*) only have one politician?
    print("What percentage of factions only have one politician?",
          round(
              len(factions_df[factions_df.degreeCentralitycount == 1])/len(factions_df)*100, 2)
          )
    return factions_df


def merge_factions(factions_df, polFactions_df):
    # ready to merge factions collective centrality with politician individuals
    factions_df = transform_factions_id(factions_df)
    df = pd.concat([factions_df, polFactions_df], axis=1)

    print('Shape of merged politicians with factions info data: ', df.shape)
    print('Number of faction variables: ', len(factions_df.columns))
    print('Number of Politician standalone variables: ',
          len(polFactions_df.columns))
    return df


if __name__ == '__main__':
    politicians = load_politicians()
    factions = calculate_factions(politicians)
    politiciansFactions = merge_factions(factions, politicians)
