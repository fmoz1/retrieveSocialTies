# #!/usr/local/bin/python
# -*- coding: utf-8 -*-
# basic imports
import pandas as pd
import numpy as np

# custom functions
from calculateTies import find_data, match_csvs, add_timestamp_and_concat
from calculateFactions import *
# plot
import matplotlib.pyplot as plt

# iterator
from itertools import product

RELATION_TYPES_ = (
    'eitherRelations',  # default
    'eitherRelations_withPartySchool',
    'alumni',
    'colleague',
    'alumni_withPartySchool',
)

# export manager centrality
# TO DO: SPECIFY RELATION TYPE
# relation_type: TIES BETWEEN MANAGERS AND POLITICIANS (BASED ON WHICH CENTRALITY IS CALCULATED)
data = add_timestamp_and_concat(
    find_data(relation_type='eitherRelations'))
print('Shape of manager centrality among politicians data: ', data.shape)

# export manager faction centrality
# TO DO: SPECIFY RELATION TYPE
# inner_pol: TIES BETWEEN POLITICIANS AND POLITICIANS
# relation_near: DIRECT TIES BETWEEN MANGERS AND POLITICIANS
iv_data = construct_iv(relation_inner_pol='eitherRelations',
                       relation_near='alumni')
print('Shape of manager calculated faction centrality instrument: ', iv_data.shape)
