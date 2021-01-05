import pytest
import random
from osira.sim import simulation, allocate_probabilities, cascading_failures


def test_simulation():
    """
    Integration test for the main simulation generation function.

    """
    random.seed(42)

    data = {}

    for i in range(0, 100):
        data[i] = {
            'id': i,
            'population': random.randint(100, 1000)
            }

    num_substations = [4]
    iterations = 100
    probabilities = [0.5, 0.1, 0.01]

    all_results = simulation(data, num_substations, probabilities, iterations)

    assert len(all_results) == 100

    max_iters = max([i['iteration'] for i in all_results])

    assert max_iters == (iterations - 1) #Remember: iterations run from 0 to 99.

    max_nodes = max([len(i['substation_ids']) for i in all_results])

    assert max_nodes == num_substations[0]

    unique_nodes = list(set([i['nodes'] for i in all_results]))

    assert unique_nodes == num_substations


def test_cascading_failures():
    """
    Unit test for quantifying cascading failures.

    """
    random.seed(42)

    data = {}

    for i in range(0, 100):
        data[i] = {
            'id': i,
            'population': random.randint(100, 1000)
            }

    data_indirect = {}

    for i in range(0, 100):

        rand = random.randint(0, 2)

        if rand == 1:
            function = 'Railway Station'
        elif rand == 2:
            function = 'Gas Distribution or Storage'
        else:
            print('Did not recognize selected int')

        data_indirect[i] = {
            'dest_func': function,
            }

    num_substations = [4]
    iterations = 1
    probabilities = [0.01]

    all_results = simulation(data, num_substations, probabilities, iterations)

    all_results = cascading_failures(all_results, data_indirect)

    assert  all_results[0]['Railway Station'] == 2
    assert  all_results[0]['Gas Distribution or Storage'] == 2


def test_allocate_probabilities():
    """
    Unit test for allocating cumulative probabilities.

    """
    random.seed(42)

    data = {}

    for i in range(0, 100):
        data[i] = {
            'id': i,
            'population': random.randint(100, 1000)
            }

    num_substations = [4]
    iterations = 100
    probabilities = [0.01]

    all_results = simulation(data, num_substations, probabilities, iterations)

    cp_scenarios = allocate_probabilities(all_results, num_substations, probabilities)

    assert len(cp_scenarios) == 1
    assert cp_scenarios[0]['nodes'] == 4
    assert cp_scenarios[0]['iteration'] == 96
    assert cp_scenarios[0]['population'] == 3477
    assert cp_scenarios[0]['substation_ids'] == [33, 26, 85, 91]
    assert cp_scenarios[0]['rank'] == 1
    assert cp_scenarios[0]['cum_probability'] == 0.01

    data = {}

    for i in range(0, 100):
        data[i] = {
            'id': i,
            'population': random.randint(100, 1000)
            }

    num_substations = [7]
    iterations = 100
    probabilities = [0.5]

    all_results = simulation(data, num_substations, probabilities, iterations)

    cp_scenarios = allocate_probabilities(all_results, num_substations, probabilities)

    assert len(cp_scenarios) == 1
    assert cp_scenarios[0]['nodes'] == 7
    assert cp_scenarios[0]['iteration'] == 92
    assert cp_scenarios[0]['population'] == 3551
    assert cp_scenarios[0]['substation_ids'] == [89, 49, 63, 51, 31, 18, 83]
    assert cp_scenarios[0]['rank'] == 50
    assert cp_scenarios[0]['cum_probability'] == 0.495

    num_substations = [4, 7, 14]

    all_results = simulation(data, num_substations, probabilities, iterations)

    cp_scenarios = allocate_probabilities(all_results, num_substations, probabilities)

    assert len(cp_scenarios) == 3
