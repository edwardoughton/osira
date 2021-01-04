"""
Simulation run script for Globalsat.

Written by Bonface Osoro & Ed Oughton.

December 2020

"""
import configparser
import os
import random
import pandas as pd

from osira.sim import simulation, allocate_probabilities

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

RESULTS = os.path.join(BASE_PATH, '..', 'results')


if __name__ == '__main__':

    if not os.path.exists(RESULTS):
        os.makedirs(RESULTS)

    total_substation = 100
    num_substations = [4, 7, 14]
    iterations = 1000
    probabilities = [0.5, 0.1, 0.01]

    data = {}

    for i in range(0, total_substation):
        data[i] = {
            'id': i,
            'population': random.randint(1e4, 1e5)
            }

    all_results = simulation(data, num_substations, probabilities, iterations)

    cp_scenarios = allocate_probabilities(all_results, num_substations, probabilities)

    all_results = pd.DataFrame(all_results)
    path = os.path.join(RESULTS, 'all_results.csv')
    all_results.to_csv(path, index=False)

    cp_scenarios = pd.DataFrame(cp_scenarios)
    path = os.path.join(RESULTS, 'cp_scenarios.csv')
    cp_scenarios.to_csv(path, index=False)
