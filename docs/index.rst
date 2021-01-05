Open Source Infrastructure Risk Analytics (osira)
=================================================

.. image:: https://travis-ci.com/edwardoughton/osira.svg?branch=main
    :target: https://travis-ci.org/edwardoughton/osira
    :alt: Build Status

.. image:: https://readthedocs.org/projects/osira/badge/?version=latest
    :target: https://osira.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/edwardoughton/osira/badge.svg?branch=main
    :target: https://coveralls.io/github/edwardoughton/osira?branch=main
    :alt: Coverage Status

.. image:: https://img.shields.io/badge/github-osira-brightgreen
    :target: https://github.com/edwardoughton/osira
    :alt: Source Code


Welcome to the documentation for osira!


Description
-----------

These docs provide an overview of the Open Source Infrastructure Risk Analytics (osira)
codebase written in Python.

The aim is to be able to quantify the direct and indirect impacts of infrastructure cascading
failure, such as from cyber-attacks on electricity assets.


Citation
--------

- Oughton, E. J. et al. (2019) ‘Stochastic Counterfactual Risk Analysis for the Vulnerability
  Assessment of Cyber-Physical  Attacks on Electricity Distribution Infrastructure Networks’,
  Risk Analysis, 39(9), pp. 2012–2031. https://doi.org/10.1111/risa.13291.
- Cambridge Centre for Risk Studies (2016) Integrated infrastructure: Cyber resiliency in
  society, mapping the consequences of an interconnected digital economy. Cambridge: Cambridge
  Centre for Risk Studies.


Statement of Need
-----------------

Disruption in electricity supply has major ramifications for both society and the economy.
Risk analysts working in the insurance sector have a major interest in trying to understand
the potential business interuption impacts.

Indeed, catastrophic events such as cyber-attacks are both a major risk management issue and a
huge business opportunity for different types of insurers.

However, it is surprising that we lack open-source models to help quantify these risks,
providing strong motivation for the content of the `osira` repository.


Setup and Configuration
-----------------------

All code for itmlogic is written in Python (Python>=3.7).

See requirements.txt for a full list of dependencies.


Installing via conda
--------------------

The recommended installation method is to use conda to handle packages and virtual
environments. The conda-forge channel also has a host of pre-built libraries and
packages.

Create a conda environment called osira:

    conda create --name osira python=3.7 gdal

Activate it (run this each time you switch projects):

    conda activate osira

First, you need to install necessary packages, which at a minimum, is `geopandas`:

    conda install geopandas pytest matplotlib seaborn

Then clone this repository and run:

    python setup.py install

Or if you want to develop the package:

    python setup.py develop

And, also should you want to run the tests:

    python -m pytest


Quick Start
-----------

To quickly get started using synthetic data run this:

    python scripts/demo.py

Followed by using the `vis.py` script to visualize the results:

    python vis/vis.py


Background and funding
----------------------

The approach has been developed over many years at numerous institutions:

- 2015-2017: Cambridge Centre for Risk Studies, University of Cambridge
- 2017-2020: Environmental Change Institute, University of Oxford
- 2020-2021: Geography and Geoinformation Sciences, George Mason University

We would like to thank UKRI, specifically the Engineering and Physical Sciences Research
Council for support via grant EP/N017064/1.


Contents
--------

.. toctree::
   :maxdepth: 3

   Getting Started <getting-started>
   Reference <api/modules>

.. toctree::
   :maxdepth: 1

   License <license>
   Authors <authors>


Make Contact
------------

- Report bugs, suggest features or view the source code `on GitHub`_.
    .. _on GitHub: https://github.com/edwardoughton/osira
