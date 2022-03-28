# retrieveSocialTies
This repository contains refactored code for retrieving and calculating person-level network measures.
## Getting started
1. Install dependencies

   `pip install -e`

2. Specify parameters in the `run.py` file 

To obtain centralities based on networks calculated from particular types of edges, e.g, colleague, alumni, modify the parameter dictionary in  `run.py`. 

        PARAMS = {'politician_manager_relation_type': 'eitherRelations',
                'politician_politician_relation_type': 'eitherRelations',
                'centrality_to_normalize': ['closenessCentrality'], # <- a list!
                'scaler': MinMaxScaler,
                # or StandardScaler
                }

3. Pull data 

   `python run.py`

   Returns two datafiles in the `./output/` folder:
  
  * `managerCentralitypoliticianNetwork_{politician_manager_relation_type}.csv`
  * `factionIV_{politician_politician_relation_type}.csv`