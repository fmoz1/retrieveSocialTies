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
# step 3: concat factions based on politicians' centrality irrespective of managers
from concatFaction import *

# plot
import matplotlib.pyplot as plt

# iterator
from itertools import product

# TO DO: SPECIFY THE AGGREGATION METHOD HERE
# statistics used to calculate aggregate faction centrality attributed to each manager
MANAGER_FACTION_ATTRIBUTION = ['sum', 'max', 'mean']
# centrality measures
FACTION_CENTRALITY = ['closenessCentrality',
                      'degreeCentrality', 'eigenCentrality', 'betweenessCentrality']


def load_factions():
    politicians = load_politicians()
    factions = calculate_factions(politicians)
    politiciansFactions = merge_factions(factions, politicians)
    return politiciansFactions


def load_neighbors():
    _, politicianManagerEdges, _ = find_data()
    politicianManagerEdges_df = add_timestamp_and_concat(
        politicianManagerEdges, names=['id1', 'id2'])
    print("Shape of politician-manager links data:",
          politicianManagerEdges_df.shape)
    return politicianManagerEdges_df


def check_ties(edges):
    # print('Missing values')
    # print(politician_manager_edges.isna().sum())
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


def construct_iv():
    # process edges files
    politician_manager_edges = load_neighbors()
    check_ties(politician_manager_edges)
    politician_politician_edges, politician_manager_edges = classify_ties(
        politician_manager_edges)

    # load factions
    factions = load_factions()

    # generate manager faction links (non-unique manager-year index)
    managerFactions = link_managers_to_factions(
        politician_manager_edges, factions)

    # calculate manager faction centrality in each year (unique manager-year index)
    managerFactionCentrality = sort_managers(managerFactions)
    print('Shape of manager faction centrality data: ',
          managerFactionCentrality.shape)
    return managerFactionCentrality
