# #!/usr/local/bin/python
# -*- coding: utf-8 -*-
# TO DO: CUSTOMIZE THE PARAMATERS IN THIS FILE
# traverse the main directory
# define the relations of interest, default is eitherRelations ('colleagues' OR 'alumni')
# locate the csv files
import os
import re


def match_regex(relation_type='eitherRelations'):
    """
    Specify the type of relations of interest between politicians and managers,
    politician and politicians.

    Args:
        relation_type (str, optional): type of relation based on which centrality
        is calculated. Defaults to 'eitherRelations'.

    Returns:
        tuple: regular expression pattern.
    """
    manager_pol_centrality_regex = re.compile(
        rf'managerCentrality_politicianNetwork_\d\d\d\d_*_{relation_type}.csv')

    # politician's political centrality
    # note the double l
    politician_pol_centrality_regex = re.compile(
        rf'politicianCentrality_politicallNetwork_\d\d\d\d_*_{relation_type}.csv')

    # politician-manager neighbors
    politician_manager_neighbors_regex = re.compile(
        rf'politicianManagerNeighbors_\d\d\d\d_{relation_type}.csv'
    )
    return manager_pol_centrality_regex, politician_pol_centrality_regex, politician_manager_neighbors_regex


def find_data(directory='../datafiles',
              relation_type='eitherRelations'):
    """
        Specify the directory to search for data.

        Args:
            directory (str, optional): Defaults to '../datafiles'.
            relation_type (str, optional): Defaults to 'eitherRelations'.
            Other options: ('alumni', 'colleague', 'alumni_withPartySchool', 'eitherRelations_withPartySchool')

        Returns:
            tuple: list of paths for files by types (e.g., managers' centrality,
            political-manger ties, politicians' centrality)
        """

    managerPolCentrality = []
    politicianManagerNeighbors = []
    politicianPolCentrality = []

    MANAGER_POL_CENTRALITY_REGEX, POLITICIAN_POL_CENTRALITY_REGEX, POLITICIAN_MANAGER_NEIGHBORS_REGEX = \
        match_regex(relation_type)

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if MANAGER_POL_CENTRALITY_REGEX.match(filename):
                managerPolCentrality.append(os.path.join(root, filename))
            elif POLITICIAN_MANAGER_NEIGHBORS_REGEX.match(filename):
                politicianManagerNeighbors.append(os.path.join(root, filename))
            elif POLITICIAN_POL_CENTRALITY_REGEX.match(filename):
                politicianPolCentrality.append(os.path.join(root, filename))
    return managerPolCentrality, politicianManagerNeighbors, politicianPolCentrality


# if __name__ == '__main__':
#    f0, f1, f2 = find_data()
