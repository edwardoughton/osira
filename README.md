# Open Source Infrastructure Risk Analytics (osira)

[![Build Status](https://travis-ci.com/edwardoughton/osira.svg?branch=main)](https://travis-ci.com/edwardoughton/osira)
[![Documentation Status](https://readthedocs.org/projects/osira/badge/?version=latest)](https://osira.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/edwardoughton/osira/badge.svg?branch=main)](https://coveralls.io/github/edwardoughton/osira?branch=main)


This repository provides an open source codebase to quantify the direct and indirect impacts
of infrastructure cascading failure. For example, resulting from a cyber-attack.

The repository name is taken from Wonder Woman where Osira is a fictional Egyptian Goddess
respected for her advanced understanding of technology.

Advancing our understanding of the groups of technologies known as 'infrastructure systems'
can help us make better decisions, particularly in relation to risk management.

Despite infrastructure being of growing importance, there are surprisingly few open source,
fully-tested, fully-documented codebases available for risk analysts to use. The contribution
of this repository is to fill this gap.


Citations
---------

- Oughton, E. J. et al. (2019) ‘Stochastic Counterfactual Risk Analysis for the Vulnerability
  Assessment of Cyber-Physical  Attacks on Electricity Distribution Infrastructure Networks’,
  Risk Analysis, 39(9), pp. 2012–2031. https://doi.org/10.1111/risa.13291.
- Cambridge Centre for Risk Studies (2016) Integrated infrastructure: Cyber resiliency in
  society, mapping the consequences of an interconnected digital economy. Cambridge: Cambridge
  Centre for Risk Studies.


Example results
---------------
![Example](/fn_curve.png)


Using conda
-----------

The recommended installation method for `osira` is to use conda, which handles packages and
virtual environments, along with the conda-forge channel which has a host of pre-built
libraries and packages.

Create a conda environment called `osira`:

    conda create --name osira python=3.7 gdal

Activate it (run this each time you switch projects):

    conda activate osira

You need to install necessary packages:

    conda install geopandas pytest matplotlib seaborn

Then clone this repository and run:

    python setup.py install

Or if you want to develop the package:

    python setup.py develop

And if you want to check test coverage run `pytest`:

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


Contributors
------------
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
