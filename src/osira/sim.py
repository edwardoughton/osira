"""
Simulation code for osira.

Written by Ed Oughton

January 2021

"""
import random


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

            population = 0

            for key, value in data.items():
                if key in substation_ids:
                    population += value['population']

            output.append({
                'nodes': nodes,
                'iteration': i,
                'population': population,
                'substation_ids': substation_ids,
            })

    return output


def allocate_probabilities(results, num_substations, probabilities):
    """
    Allocate cumulative probabilities.

    Parameters
    ----------
    results : list of dicts
        All iterations generated in the simulation function.
    probabilities : list
        Contains the cumulative probabilities we wish to use.

    """
    output = []

    for nodes in num_substations:

        ranked_data = add_cp(results, nodes)

        for probability in probabilities:

            scenario = min(
                ranked_data,
                key=lambda x: abs(float(x["cum_probability"]) - probability)
            )

            output.append(scenario)

    return output


def add_cp(results, nodes):
    """
    Add the F-N cumulative frequency.

    See equation (1) from Oughton et al. 2019.

    Parameters
    ----------
    results : list of dicts
        All iterations generated in the simulation function.
    nodes : int
        Number of substations for the scenario.

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
        item['cum_probability'] = round(rank / (len(results) + 1), 3)

        output.append(item)

        rank += 1

    return output
