# #!/usr/local/bin/python
# -*- coding: utf-8 -*-
# basic imports
import numpy as np
import pandas as pd

# custom functions
# 1. step 1: locate data
from findRelations import find_data, match_regex

# sanity checks of data
from scipy.stats import sem
import re

# calling find_data()
managerPolCentrality, _, _, = find_data()


def add_timestamp_and_concat(data_path, names=None):
    """
    Add year column to each csv file with 
    the year specified in the csv file,
    concat the csvs into an unbalanced panel. 
    Args:
        data_path (str): the path for all the csvs according to types
        (either managerPolCentrality, politicalMangerNeighbors, 
        politicalPolCentrality)
        names (list, optional): list of colnames for csv. Default is None. 
    Return:
        a panel pd dataframe.
    """
    concat_data = pd.concat([pd.read_csv(csv, names=names).assign(
        year=int(re.findall('_[0-9]{4}_', csv)[0].replace('_', '')))
        for csv in data_path]).sort_values(by='year')
    return concat_data


# test
managerPolCentrality_df = add_timestamp_and_concat(managerPolCentrality)

# TO DO: sanity check
# # annual statistics
# d = managerPolCentrality_df.sort_values(
#     by='year')[['degreeCentrality', 'year']].groupby('year')
# stderr_ = d.apply(
#     lambda x: x.std() / np.sqrt(x.count()))
