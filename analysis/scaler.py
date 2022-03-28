#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# scale centrality measures (0,1)

from sklearn.preprocessing import MinMaxScaler, StandardScaler


def normalize(data, columns=['closenessCentrality'], scaler=MinMaxScaler):
    """
    Standardize centrality variables (to remove issues with centralities on different scales).

    Args:
        data (pd.dataFrame): original panel data with personal-level centralities. 
        columns (list, optional): list of columns to be transformed. Defaults to ['closenessCentrality'].
        scaler (object, optional): a method for scaling inherited from sklearn.preprocessing class. Defaults to MinMaxScaler.

    Returns:
        pd.DataFrame: data after feature standardization. 
    """
    scaler = scaler()
    data[columns] = scaler.fit_transform(data[columns])
    return data
