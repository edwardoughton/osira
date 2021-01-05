"""
Simulation run script for osira using real data.

Make sure you first obtain the necessary data and run scripts/preprocess.py.

Written by Ed Oughton.

December 2020

"""
import configparser
import os
import random
import pandas as pd

from osira.sim import simulation, allocate_probabilities, cascading_failures

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_INTERMEDIATE = os.path.join(BASE_PATH, 'intermediate')
RESULTS = os.path.join(BASE_PATH, '..', 'results')

def load_data():
    """
    Load the preprocessed data.

    """
    path = os.path.join(DATA_INTERMEDIATE, 'pop_by_elec_node.csv')

    if not os.path.exists(path):
        print('You must run the preprocessing script first')
        print('If you do not have actual data try running demo.py')
        return

    preprocessed_data = pd.read_csv(path)
    preprocessed_data = preprocessed_data.to_dict('records')

    data = {}

    for idx, item in enumerate(preprocessed_data):

        data[idx] = {
            'id': item['id'],
            'population': item['population']
            }

    return data


def load_indirect_data():
    """
    Load the preprocessed indirect data.

    """
    path = os.path.join(DATA_INTERMEDIATE, 'indirect_lut.csv')

    if not os.path.exists(path):
        print('You must run the preprocessing script first')
        print('If you do not have actual data try running demo.py')
        return

    indirect_lut = pd.read_csv(path)
    indirect_lut = indirect_lut.to_dict('records')

    data_indirect = {}

    for idx, item in enumerate(indirect_lut):

        data_indirect[item['origin_id']] = {
            'origin_id': item['origin_id'],
            'dest_funth': item['dest_funth'],
            'dest_func': item['dest_func'],
            'dest_dist': item['dest_dist'],
            }

    return data_indirect


if __name__ == '__main__':

    if not os.path.exists(RESULTS):
        os.makedirs(RESULTS)

    num_substations = [4, 7, 14]
    iterations = 1000
    probabilities = [0.5, 0.1, 0.01]

    data = load_data()

    all_results = simulation(data, num_substations, probabilities, iterations)

    data_indirect = load_indirect_data()

    all_results = cascading_failures(all_results, data_indirect)

    cp_scenarios = allocate_probabilities(all_results, num_substations, probabilities)

    all_results = pd.DataFrame(all_results)
    path = os.path.join(RESULTS, 'all_results.csv')
    all_results.to_csv(path, index=False)

    cp_scenarios = pd.DataFrame(cp_scenarios)
    path = os.path.join(RESULTS, 'cp_scenarios.csv')
    cp_scenarios.to_csv(path, index=False)
