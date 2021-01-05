===============
Getting Started
===============

This tutorial provides explanation for the use of the ``osira`` codebase.

Firstly, a summary of the main primary parameters and outputs is given.

Primary input parameters
------------------------

====================== ===============================================
Parameters             Description
====================== ===============================================
data                   Electricity substation information
num_substations        Number of electricity substation nodes
probabilities          Cumulative probabilities we wish to use
iterations             Number of Monte Carlo draws
results                All iterations generated
data_indirect          Lookup table for indirect network connections
====================== ===============================================

Secondary parameters
--------------------

============================ ==============================================
Secondary Parameters         Description
============================ ==============================================
population                   Direct population disruption
substation_ids               Node ids based on the runner index
substation_asset_ids         Secondary node ids based on the runner index
rank                         The iteration rank
cum_probability              Cumulative probability
Railway Station
Gas Distribution or Storage
============================ ==============================================

Outputs
-------

====================== ===============================================
Outputs                Description
====================== ===============================================
output                 Contains all generated results
====================== ===============================================


The model can be run using either the demo data provided via `demo.py` or by generating
real data via `preprocessing.py` and using `run.py`. Each will be discussed in turn.


Demo Mode (`demo.py`)
---------------------

Synthetic data is generated via the `demo.py` script and utilizes the given functions within
the `osira` source code.

Once you execute the code below...

.. code-block:: python

    python scripts/demo.py

The direct and indirect effects of each event are written to `all_results.csv` within the
`results` directory.

Additionally, the cumulative probabilities for the specific scenarios
are estimated and exported within `cp_scenarios.csv`.

The results produced are visualized using `vis.py` in order to plot all event combinations,
given their cumulative probability and level of societal disruption.


Run Mode (`run.py`)
-------------------

In contrast to the demo, actual empirical data can be obtained and used to run `osira`.

However, the data are not released with `osira` as you probably will require a licence.

For example, the repository has been developed using Ordanance Survey MasterMap data. Should
you have access to this data, you can then run the preprocessing script, as follows:

.. code-block:: python

    python scripts/preprocessing.py

As each function is run, there will be a message printed to the console explaining the
preprocessing steps being undertaken. This involves processing the different types of assets,
connecting each asset to an electricity substation and finally exporting the data.

Additionally, local statistical area boundaries are obtained and merged with population
estimates. The datasets required are:

- Local area boundaries via the [ONS geoportal](https://geoportal.statistics.gov.uk/)
- Population estimates via [NOMIS](https://www.nomisweb.co.uk/)

After merging the data, it is then possible to use the centroid of each polygon to estimate
the proportion of the population served by each electricity substation.
