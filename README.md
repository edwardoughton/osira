# Open Source Infrastructure Risk Analytics (osira)

[![Build Status](https://travis-ci.com/edwardoughton/osira.svg?branch=main)](https://travis-ci.com/edwardoughton/osira)
[![Documentation Status](https://readthedocs.org/projects/osira/badge/?version=latest)](https://osira.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/edwardoughton/osira/badge.svg?branch=main)](https://coveralls.io/github/edwardoughton/osira?branch=main)


This repository provides an open source codebase to quantify the direct and indirect impacts
of infrastructure cascading failure. For example, resulting from a cyber-attack.

The repository name is taken from Wonder Woman where Osira was a fictional Egyptian god
respected for her advanced understanding of technology, therefore providing inspiration for
this codebase.

Indeed, infrastructure systems are groups of technologies, thus advancing our understanding
can help us make better decisions, for example, in relation to risk management.

Despite infrastructure being of growing importance, there are surprisingly few open source,
fully-tested, fully-documented codebases available for risk analysts to use. This repository
therefore makes a strong contribution to the field of risk analytics.


Citation
========

- Oughton, E. J. et al. (2019) ‘Stochastic Counterfactual Risk Analysis for the Vulnerability
  Assessment of Cyber-Physical  Attacks on Electricity Distribution Infrastructure Networks’,
  Risk Analysis, 39(9), pp. 2012–2031. https://doi.org/10.1111/risa.13291.


Example results
===============
![Example](/fn_curve.png)


Using conda
===========

The recommended installation method is to use conda, which handles packages and virtual
environments, along with the conda-forge channel which has a host of pre-built libraries and
packages.

Create a conda environment called osira:

    conda create --name osira python=3.7 gdal

Activate it (run this each time you switch projects):

    conda activate osira

You need to install necessary packages:

    conda install geopandas pytest matplotlib seaborn

And if you want to check test coverage enter as follows:

    python -m pytest


Quick Start
===========

To quick start, install the `osira` package:

    python setup.py install

Or if you want to develop the package:

    python setup.py develop

Then run the simulation to generate results:

    python scripts/run.py

If you want to create the map try:

    python scripts/preprocess.py

Followed by:

    python scripts/results.py

And then:

    python vis/vis.py


Background and funding
======================

The approach has been developed over many years at numerous institutions.

- 2015-2017: Cambridge Centre for Risk Studies, University of Cambridge
- 2017-2020: Environmental Change Institute, University of Oxford
- 2020-2021: Geography and Geoinformation Sciences, George Mason University.

We would like to thank UKRI, specifically the Engineering and Physical Sciences Research
Council for support via grant EP/N017064/1.


Contributors
============
- Ed Oughton (GMU & Oxford)
- Daniel Ralph (Cambridge)
- Eireann Leverett (Cambridge & Airbus)
- Raghav Pant (Oxford)
- Jen Copic (Cambridge)
- Simon Ruffle (Cambridge)
- Andrew Coburn (Cambridge)
- Michele Tuveson (Cambridge)
- Scott Thacker (Oxford & UNOPS)
- Jim Hall (Oxford)
- Scott Kelly (Cambridge & UTS)
