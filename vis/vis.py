"""
Visualize results.

Written by Ed Oughton

January 2021.

"""
import os
import configparser
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
# import contextily as ctx

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_INTERMEDIATE = os.path.join(BASE_PATH, 'intermediate')
RESULTS = os.path.join(BASE_PATH, '..', 'results')
VIS = os.path.join(BASE_PATH, '..', 'vis', 'figures')


def load_results():
    """
    Load results.

    """
    path = os.path.join(RESULTS, 'all_results.csv')
    all_results = pd.read_csv(path)

    all_results['population_m'] = all_results['population'] / 1e6

    # all_results['cum_probability'] = np.log2(all_results['cum_probability'])

    all_results = all_results[['nodes', 'population_m', 'cum_probability']]

    all_results.columns = [
        'Substations Affected',
        'Population (Millions)',
        'Cumulative Frequency'
    ]

    return all_results


def generate_fn_curves(results):
    """
    Generate F-N cumulative frequency curve, as per Figure 4 in Oughton et al. (2019).

    Parameters
    ----------
    results : pandas dataframe
        Contains the simulation results ready for plotting.

    """
    fig, ax = plt.subplots()

    palette = sns.color_palette("rocket_r", 3)
    sns.set_context("paper", font_scale=0.9)

    plot = sns.lineplot(
        x='Population (Millions)', y='Cumulative Frequency',
        hue='Substations Affected', style='Substations Affected',
        palette=palette, dashes=[(2,3), (2,2), (2,1)],
        linewidth = .75,
        data=results, ax=ax,
    )

    plot.axhline(y=0.5, linewidth=0.2, color='black', linestyle='--')
    plot.axhline(y=0.1, linewidth=0.2, color='black')
    plot.axhline(y=0.01, linewidth=0.2, color='black')
    plot.set_title('Stochastic Infrastructure Cyber-Attack Events: Direct Population Disruption')

    plot.text(5e5, 0.51, '50% CP',rotation=0)
    plot.text(5e5, 0.11, '10% CP',rotation=0)
    plot.text(5e5, 0.02, '1% CP',rotation=0)

    fig = plot.get_figure()
    fig.savefig(os.path.join(VIS, 'fn_curve.png'), dpi=300)


if __name__ == '__main__':

    if not os.path.exists(VIS):
        os.makedirs(VIS)

    results = load_results()

    generate_fn_curves(results)

    # print(results)

    # path = os.path.join(RESULTS, 'cp_scenarios.csv')
    # cp_scenarios = pd.read_csv(path, index=False)
