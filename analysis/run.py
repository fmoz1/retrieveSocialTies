# #!/usr/local/bin/python
# -*- coding: utf-8 -*-

# TO EXPORT DATA FOR ANALYSIS,
# CHANGE PARAMETERS IN THIS SCRIPT
# AND IN TERMINAL
# python3 run.py

# basic imports
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# custom functions
from calculateTies import find_data, match_csvs, add_timestamp_and_concat
from calculateFactions import *
from scaler import normalize
# plot
import matplotlib.pyplot as plt

# iterator
from itertools import product

# for data version naming
from inspect import signature

# store data in new directory
OUT_DIRECTORY = '../output/'

# PARAMS OPTIONS
RELATION_TYPES_ = (
    'eitherRelations',  # default
    'eitherRelations_withPartySchool',
    'alumni',
    'colleague',
    'alumni_withPartySchool',
)

CENTRALITY = ('closenessCentrality',
              'degreeCentrality', 'eigenCentrality', 'betweenessCentrality')

WEIGHTING_OPTIONS_ = ('sum', 'max', 'mean')

# faction centrality has 4 * 3 * 3 = 36 options
# why? we have two step procedure:
# politicians' affiliated faction's power: max, mean, sum
# factions attributed to each manager through manager's connected politicians: max, mean, sum

FACTION_CENTRALITY_OPTIONS = [''.join(_) for _ in product(
    CENTRALITY, WEIGHTING_OPTIONS_, WEIGHTING_OPTIONS_)]

# TO DO:
# CHOOSE PARAMMS HER
PARAMS = {'politician_manager_relation_type': 'eitherRelations',
          'politician_politician_relation_type': 'eitherRelations',
          'centrality_to_normalize': ['closenessCentrality'],
          # note: list of centralities
          # 'centrality_to_normalize': ['degreeCentrality', 'closenessCentrality', 'eigenCentrality'],
          'scaler': MinMaxScaler,
          # or StandardScaler
          }


def get_data(**PARAMS):
    data = add_timestamp_and_concat(
        find_data(relation_type=PARAMS['politician_manager_relation_type']))

    print('Shape of manager centrality among politicians data: ', data.shape)

    data = normalize(data=data, columns=PARAMS['centrality_to_normalize'],
                     scaler=PARAMS['scaler'])

    output_name = "".join([i for i in
                           str(signature(find_data).parameters['pattern']).
                           split('=')[1]
                           if i.isalpha()])\
        + '_' \
        + str(PARAMS['politician_manager_relation_type'])

    # OPTIONAL: specify relation type between politicians and politicians
    # inner_pol: TIES BETWEEN POLITICIANS AND POLITICIANS
    # relation_near: DIRECT TIES BETWEEN MANGERS AND POLITICIANS
    iv_data = construct_iv(relation_inner_pol=PARAMS['politician_politician_relation_type'],
                           relation_near=PARAMS['politician_manager_relation_type'])

    # OPTIONAL: specify faction centrality measures to transform
    # suppose we just need closeness centralities, there are 3 x 3 combinations
    iv_centralities = [_ for _ in FACTION_CENTRALITY_OPTIONS
                       if _.startswith(tuple(PARAMS['centrality_to_normalize']))]
    iv_data = normalize(data=iv_data, columns=iv_centralities,
                        scaler=PARAMS['scaler'])

    # EXPORT DATA
    data.to_csv(OUT_DIRECTORY + f'{output_name}.csv')
    iv_data.to_csv(OUT_DIRECTORY +
                   f"factionIV_{PARAMS['politician_politician_relation_type']}.csv")


if __name__ == '__main__':
    get_data(**PARAMS)
