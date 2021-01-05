"""
Simulation functions for osira.

Written by Ed Oughton

January 2021

"""
import random
from collections import Counter


def simulation(data, num_substations, probabilities, iterations):
    """
    This function runs the infrastructure simulation.

    For a given number of nodes we wish to knock-out, quantify the potential
    population disruption.

    Parameters
    ----------
    data : list of dicts
        Contains all electricity substation information.
    num_substations : list
        The number of electricity substation nodes we wish to select for each scenario.
    probabilities : list
        Contains the cumulative probabilities we wish to use.
    iterations : int
        The number of Monte Carlo draws we wish to undertake.

    Returns
    -------
    output : list of dicts
        Contains all generated results.

    """
    random.seed(42)

    output = []

    for nodes in num_substations:

        for i in range(0, iterations):

            substation_ids = []

            while len(substation_ids) < nodes:

                n = random.randint(0, len(data))

                if not n in substation_ids:
                    substation_ids.append(n)

            substation_asset_ids = []

            population = 0

            for key, value in data.items():

                if key in substation_ids:
                    substation_asset_ids.append(value['id'])
                    population += value['population']

            output.append({
                'nodes': nodes,
                'iteration': i,
                'population': population,
                'substation_ids': substation_ids,
                'substation_asset_ids': substation_asset_ids,
            })

    return output


def cascading_failures(results, data_indirect):
    """
    Quantify indirect cascading failures.

    Parameters
    ----------
    results : list of dicts
        All iterations generated in the simulation function.
    data_indirect : dict
        Lookup table for indirect network connections.

    Returns
    -------
    output : list of dicts
        Results containing indirect impacts.

    """
    output = []

    for item in results:

        substation_asset_ids = item['substation_asset_ids']

        indirect_assets_affected = []

        for asset_id in substation_asset_ids:

            for key, value in data_indirect.items():

                if asset_id == key:

                    indirect_assets_affected.append(value['dest_func'])

        count = Counter(indirect_assets_affected)

        result = {}

        for key, value in item.items():
            result[key] = value
        for key, value in count.items():
            result[key] = value

        output.append(result)

    return output


def allocate_probabilities(results, num_substations, probabilities):
    """
    Allocate cumulative probabilities.

    Parameters
    ----------
    results : list of dicts
        All iterations generated in the simulation function.
    num_substations : list
        The number of electricity substation nodes we wish to select for each scenario.
    probabilities : list
        Contains the cumulative probabilities we wish to use.

    Returns
    -------
    output : list of dicts
        Contains all generated results with probabilities.

    """
    output = []

    for nodes in num_substations:

        ranked_data = add_cp(results, nodes, probabilities)

        for probability in probabilities:

            scenario = min(
                ranked_data,
                key=lambda x: abs(float(x["cum_probability"]) - probability)
            )

            output.append(scenario)

    return output


def add_cp(results, nodes, probabilities):
    """
    Add the F-N cumulative frequency.

    See equation (1) from Oughton et al. 2019.

    Parameters
    ----------
    results : list of dicts
        All iterations generated in the simulation function.
    nodes : int
        Number of substations for the scenario.
    probabilities : list
        Contains the cumulative probabilities we wish to use.

    Returns
    -------
    output : list of dicts
        Results containing cumulative probability.

    """
    output = []

    results = sorted(
        results,
        reverse=True,
        key=lambda k: k['population']
    )

    rank = 1

    for item in results:

        if not item['nodes'] == nodes:
            continue

        item['rank'] = rank
        item['cum_probability'] = round(rank / (len(results) / len(probabilities) + 1), 3)

        output.append(item)

        rank += 1

    return output
