# #!/usr/local/bin/python
# -*- coding: utf-8 -*-
# TO DO: CUSTOMIZE THE PARAMATERS IN THIS FILE
# traverse the main directory
# define the relations of interest, default is eitherRelations ('colleagues' OR 'alumni')
# locate the csv files
import os
import re
import pandas as pd
import numpy as np


def match_csvs(filename_pattern, relation_type):
    return re.compile(rf'{filename_pattern}_\d\d\d\d_*_{relation_type}.csv')


def find_data(pattern='managerCentrality_politicianNetwork', relation_type='eitherRelations', directory='../datafiles'):
    """
    Retrieve all data for managers' centrality, politicians' centrality, and manager-politician ties. 

    Args:
        pattern (str, optional): identifier of the csv files. Defaults to 'managerCentrality_politicianNetwork'.
        Other options for pattern: ['politicianCentrality_politicallNetwork', 'politicianManagerNeighbors'] 
        relation_type (str, optional): particular relation types. Defaults to 'eitherRelations'.
        Other options for relation_type: ['alumni', 'colleague', 'eitherRelations_withPartySchool', 'alumni_withPartySchool']
        directory (str, optional): main directory where data is stored. Defaults to '../datafiles'.

    Returns:
        list: list of csv file names. 
    """
    matched_csvs = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if match_csvs(pattern, relation_type).match(filename):
                matched_csvs.append(os.path.join(root, filename))
    return matched_csvs


# test
# test_files = find_data(
#    pattern='politicianCentrality_politicallNetwork', relation_type='alumni')


def add_timestamp_and_concat(files, names=None):
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
        for csv in files]).sort_values(by='year')
    return concat_data


# export manager centrality data
data = add_timestamp_and_concat(find_data())  # all default
