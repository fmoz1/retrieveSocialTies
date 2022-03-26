# #!/usr/local/bin/python
# -*- coding: utf-8 -*-
# basic imports
import pandas as pd
import numpy as np

# custom functions
from findRelations import *  # 1. step 1: locate data
from concatData import add_timestamp_and_concat  # step 2: modify and concat data
# step 3: concat factions based on politicians' centrality irrespective of managers
from concatFaction import *
# step 4: calculate manager faction centrality (unique manager-year index)
from constructIV import *

# plot
import matplotlib.pyplot as plt

# iterator
from itertools import product

# CONFIG OPTIONS
RELATIONS_TYPES_ = ('eitherRelations', 'colleagues', 'alumni',
                    'alumni_withPartySchool', 'eitherRelations_withPartySchool')

relation_type = 'eitherRelations'
# export manager centrality in politician networks panel
manager_political_centrality, _, _ = find_data(relation_type=relation_type)
manager_political_centrality_panel = add_timestamp_and_concat(
    manager_political_centrality)


# export managers' faction centrality panel
manager_faction_centrality = construct_iv()
