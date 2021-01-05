"""
Demo simulation script for osira using synthetic data.

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

RESULTS = os.path.join(BASE_PATH, '..', 'results')


def load_data():
    """
    Produce demo data.

    """
    random.seed(42)

    data = {}

    for i in range(0, total_substation):
        data[i] = {
            'id': i,
            'population': random.randint(1e4, 1e5)
            }

    return data


def load_indirect_data():
    """
    Produce indirect demo lookup table data.

    """
    random.seed(42)

    data_indirect = {}

    for i in range(0, 100):

        rand = random.randint(1, 2)

        if rand == 1:
            function = 'Railway Station'
        elif rand == 2:
            function = 'Gas Distribution or Storage'
        else:
            print('Did not recognize selected int')

        data_indirect[i] = {
            'dest_func': function,
            }

    return data_indirect


if __name__ == '__main__':

    if not os.path.exists(RESULTS):
        os.makedirs(RESULTS)

    total_substation = 100
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
