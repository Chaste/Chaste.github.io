---
title: "Two Sequential Monte Carlo Samplers for Exact and Approximate Bayesian Inference on Cardiac Models"
draft: false
layout: "single"
paperTutorialProject: "https://github.com/Chaste/project_DalySMC"
version: "2026.1"
---

This tutorial describes how to download and execute the Sequential Monte Carlo code
for inference on the linear, polynomial, and O'Hara-Rudy models as described in "Comparing two sequential Monte Carlo samplers for exact and approximate Bayesian inference on biological models", *J. R. Soc. Interface*, 2017, [doi: 10.1098/rsif.2017.0340](https://doi.org/10.1098/rsif.2017.0340).


## Installation

This project requires the Functional Curation add-on to Chaste in order to run, which in turn requires the Chaste source tree to be installed.
Instructions for this installation can be found for a variety of operating systems under InstallGuides/.

Extra install commands needed as well as the Ubuntu chaste-dependencies package are (on 14.04 at least):

```bash
#!sh
sudo apt-get install python-dev python-scipy python-numpy cython python-tables python-matplotlib python-numexpr python-pip
sudo apt-get install scons
sudo -H pip install dill pathos
```

This project works with Chaste version 3.4.
Obtain the relevant version of all the code from the Chaste repositories using:

```bash
#!sh
git clone -b release_3.4 https://chaste.cs.ox.ac.uk/git/chaste.git Chaste
cd Chaste/projects

git clone https://github.com/Chaste/project_FunctionalCuration.git
git clone https://github.com/Chaste/project_DalySMC
```


## Usage

Source code for the SMC parameter fitting algorithms is contained in the `src` folder.
Python scripts for performing inference on all model problems can be found in `tests`.

An annotated CellML file describing the O'Hara-Rudy model problem can be found in
the top-level project directory as `ohara_rudy_2011.cellml`, while functional curation
protocol files that describe the simulation and recording thereof are contained within
`tests/protocols`.

A description of important files and their contents follows below.

Files relevant for implementation of the samplers:

* `src/python/modeling/fitting/approximatebayes` contains the implementation of both Toni and Del Moral SMC algorithms.
* `src/python/modeling/fitting/objective/py` contains the implementation of the objective functions used for inference


Files relevant for inference on the linear model:

* `test/LinearFitting.py` defines the linear model and all fitting experiments associated with this model as described in the paper.


Files relevant for inference on the polynomial model:

* `test/PolynomialFitting.py` defines the polynomial model and all fitting experiments associated with this model as described in the paper.


Files relevant for inference on the O'Hara-Rudy model:

* `ohara_rudy_2011.cellml` in the top-level directory contains a CellML description of the equations governing the O'Hara-Rudy model.
* `test/protocols/oh_aptrace.txt` contains a functional curation protocol that describes the recording of a single action potential from said model.
* `test/protocols/oh_aptrace_sumstats.txt` contains a functional curation protocol that describes the recording of five summary statistics of a single action potential from said model.
* `test/data/OHrAPtrace-8-2.dat` contains simulated noisy action potential data that is used for exact inference in the study.
* `test/data/OHrSumStats-8-2.dat` contains sumulated noisy summary statistic data that is used for approximate inference in the study.
* `test/OHaraRudyFitting.py` defines all fitting experiments associated with this model as described in the paper.


To generate all described posterior estimates for the linear model
as described in the paper, go to the top-level Chaste directory and use:

```bash
scons projects/DalySMC/test/LinearFitting.py
```

To generate all described posterior estimates for the polynomial model
as described in the paper, use:

```bash
scons projects/DalySMC/test/PolynomialFitting.py
```

To generate all described posterior estimates for the O'Hara-Rudy model
as described in the paper, use:

```bash
scons projects/DalySMC/test/OHaraRudyFitting.py
```

To see verbose output on the progress of the ABC algorithm, add the flag `no_store_results=1` to the `scons` commands above.
Note however that this will prevent storing a copy of the output on disk.
