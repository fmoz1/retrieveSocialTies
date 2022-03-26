# #!/usr/local/bin/python
# -*- coding: utf-8 -*-
# TO DO: CUSTOMIZE THE PARAMATERS IN THIS FILE
# traverse the main directory
# define the relations of interest, default is eitherRelations ('colleagues' OR 'alumni')
# locate the csv files
# basic
import os
import re
import pandas as pd
import numpy as np

# iterator
from itertools import product

# custom functions
from calculateTies import *

# OPTIONAL: SPECIFY THE AGGREGATION METHOD HERE
# statistics used to calculate aggregate faction centrality attributed to each manager
MANAGER_FACTION_ATTRIBUTION = ['sum', 'max', 'mean']
# centrality measures
FACTION_CENTRALITY = ['closenessCentrality',
                      'degreeCentrality', 'eigenCentrality', 'betweenessCentrality']


def transform_factions_id(df):
    df['id'] = None
    new_df = pd.DataFrame()
    for i, (n, g) in enumerate(df.groupby(['faction_id', 'year'])):
        g['id'] = i
        new_df = new_df.append(g)

    new_df.set_index('id', inplace=True)
    return new_df


def load_politicians(relation_inner_pol='eitherRelations'):
    """
    Retrieve politicians centrality and their factions info.

    Args:
        relation (str, optional): particular relation types. Defaults to 'eitherRelations'.
        Other options for relation_type: ['alumni', 'colleague', 'eitherRelations_withPartySchool', 'alumni_withPartySchool']

    Returns:
        pd.DataFrame: transformed panda dataframe of politicians centrality panel. 
    """

    # modify and concat politicians csv's
    polFactions_df = add_timestamp_and_concat(find_data(relation_type=relation_inner_pol,
                                                        pattern='politicianCentrality_politicallNetwork'))

    # rename the variable
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

    # centrality measures of each politician in the political network
    centrality_columns = [
        x for x in factions_df.columns if x.endswith('Centrality')]

    # aggregate centrality measures by factions
    factions_df = factions_df.groupby(['faction_id', 'year'])[centrality_columns].aggregate(
        ['sum', 'max', 'mean', 'count']
    )

    # rename the faction variables
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

    factions_df = transform_factions_id(factions_df)
    return factions_df


def merge_factions(factions_df, polFactions_df):
    # a politician's centrality now represented by its associated faction's aggregate centrality
    df = pd.concat([factions_df, polFactions_df], axis=1)

    print('Shape of merged politicians with factions info data: ', df.shape)
    print('Number of faction variables: ', len(factions_df.columns))
    print('Number of Politician standalone variables: ',
          len(polFactions_df.columns))
    return df


def load_neighbors(relation_near='eitherRelations'):
    # modify and concat politicians csv's
    polManagerEdges_df = add_timestamp_and_concat(
        find_data(relation_type=relation_near,
                  pattern='politicianManagerNeighbors'),
        names=['id1', 'id2'])

    # check the shape of edges data
    print("Shape of politician-manager links data:",
          polManagerEdges_df.shape)
    return polManagerEdges_df


def check_ties(edges):
    print("LEFT nodes are all politicians: ",
          (edges['id1'] >= 10000).sum() == 0)
    # IMPORTANT:
    # politicalManagerNeighbors*.csv's
    # seem to include politician-politician tie
    # MANAGER ID BEGINS WITH 100001
    print("RIGHT nodes are all managers: ",
          (edges['id2'] < 10000).sum() == 0)


def classify_ties(edges):
    # politician-politician tie
    polPolTie = edges[
        (edges['id1'] < 10000)
        &
        (edges['id2'] < 10000)]

    # politician-manager tie
    polManagerTie = edges[
        (edges['id1'] < 10000)
        &
        (edges['id2'] >= 10000)]

    # check sum up to total ties
    print("Sum of tie passed test: ", len(polManagerTie) + len(polPolTie) ==
          len(edges))
    return polPolTie, polManagerTie


def link_managers_to_factions(manager_edges, faction):
    """
    Link managers to factions centrality by following procedure:
    1. Retrieve politicians and politicians' associated faction centrality in each year
    2. Retrieve all manager-politician links in each year
    3. Link manager to factions bridged by politician

    Caveat:
    1. A manager could have ties to multiple politicians and factions in the same year.
    \What faction's centrality should we attribute to the manager?
    2. Concat does not apply to non-unique indices.


    Args:
        manager_edges (pd.DataFrame): raw manager-politician edges in each year
        faction (pd.DataFrame): raw politician-faction centrality calculations in each year.
    Returns:
        pd.DataFrame: panel that contains managers and its (exogenously) linked faction's centrality
    """
    # rename columns
    manager_edges.columns = ['politician_id', 'manager_id', 'year']
    manager_edges = manager_edges[['manager_id', 'politician_id', 'year']]
    df = pd.merge(manager_edges, faction, how='outer')
    # sort by managerid year
    df = df.sort_values(by=['manager_id', 'year'])
    # remove null values
    # df = df.dropna()
    # note difference from just removing obs where
    # politicians are not linked to managers
    df = df[df.manager_id.notnull()]
    return df


def sort_managers(linked_df):
    # use dict to store every combination for faction centrality attributes to managers
    # e.g., 'closenesscentralitySum': ['sum', 'max', 'mean']
    # means the manager's of linked factions's centrality calculated using 3 statistics (i.e., sum, max, mean)
    # where faction's centrality is calculated based on sum of politicians' centrality (i.e., Sum)
    grouped_df = linked_df.groupby(['manager_id', 'year']).aggregate(
        {
            "".join(i): MANAGER_FACTION_ATTRIBUTION for i in list(
                product(FACTION_CENTRALITY, MANAGER_FACTION_ATTRIBUTION))
        }
    )
    return grouped_df


def construct_iv(relation_near='eitherRelations', relation_inner_pol='eitherRelations'):
    # process edges files
    politician_manager_edges = load_neighbors(relation_near)
    check_ties(politician_manager_edges)
    _, politician_manager_edges = classify_ties(
        politician_manager_edges)

    # retrieve factions
    politicians = load_politicians(relation_inner_pol)
    factions = calculate_factions(politicians)
    faction_politician_edges = merge_factions(factions, politicians)

    # generate manager faction links (non-unique manager-year index)
    managerFactions = link_managers_to_factions(
        politician_manager_edges, faction_politician_edges)

    # calculate manager faction centrality in each year (unique manager-year index)
    managerFactionCentrality = sort_managers(managerFactions)
    print('Shape of manager faction centrality data: ',
          managerFactionCentrality.shape)
    return managerFactionCentrality
