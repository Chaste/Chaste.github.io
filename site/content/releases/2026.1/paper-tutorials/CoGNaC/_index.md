---
title: "CoGNaC: a Chaste plugin for the multiscale simulation of Gene regulatory Networks driving the spatial dynamics of tissues and Cancer"
draft: false
layout: "single"
showPageLinks: true
paperTutorialProject: "https://github.com/Chaste/project_CoGNaC"
version: "2026.1"
---


Welcome to the Chaste wiki.

Designed only to work as bolt-on project for Chaste v3.2 or v3.3.

This section contains pages generated automatically from the source code accompanying Rubinacci et al. "[CoGNaC: A Chaste Plugin for the Multiscale Simulation of Gene Regulatory Networks Driving the Spatial Dynamics of Tissues and Cancer](http://dx.doi.org/10.4137/CIN.S19965)", our paper in [Cancer informatics](http://www.la-press.com/journal-cancer-informatics-j10), 2015.


## User manual

A detailed user guide of CoGNaC can be found as an attachment at the bottom of this page.


## Getting the code and installing dependencies

Before running these examples you will need to [install Chaste's dependencies](/old_releases/release_3.4/InstallGuides/InstallGuide.html) and the [source code for version 3.3](https://github.com/Chaste/Chaste/releases/tag/release_3.3).
The easiest way to do this is using an Ubuntu machine (or an Ubuntu virtual machine) as discussed on [InstallGuides/UbuntuPackage](/old_releases/release_3.3/InstallGuides/UbuntuPackage.html).
Note that Chaste is only fully supported on Linux/Unix systems, so users of Windows or Mac OS X may need to follow the virtual machine route.
For manual installation of each dependency, on any version of Linux, see DeveloperInstallGuide.

You will also need the source for the CoGNaC project.
From the Chaste `projects` directory:

```bash
git clone https://github.com/Chaste/project_CoGNaC CoGNaC
```

**Update 2018:**  This code has been tested with Chaste versions 3.3 and 3.4.


Once you have checked out the project you need to install [BuDDy](http://buddy.sourceforge.net/manual/main.html) tool, you may do so from the command line as follows:

```bash
sudo apt-get install libbdd-dev
```


This will install BuDDy using the standard folders but you also need to inform Chaste to add BuDDy as library dependency,
adding this information to the hostconfing file.
Scons will tell you which machine file it's using in the first few lines, e.g:

```bash
cd <Chaste3.3 path>
scons
 scons: Reading SConscript files ...
 Using hostconfig settings from python/hostconfig/ubuntu.py
 Running infrastructure tests...
```


So, in the file you are using (e.g. `python/hostconfig/ubuntu.py`), just add 'bdd' similar to:

```python
other_libraries = boost_libs + ['xerces-c',
                                'hdf5', 'z',
                                'parmetis', 'metis', 'bdd']
```


Now the project should be installed, and everything should compile and run correctly. In order to
test if everything is installed correctly, you can run some tests. So from a command line do:

```bash
cd <Chaste3.3 path>
scons test_suite=projects/CoGNaC/test/TestGraphNode.hpp
scons test_suite=projects/CoGNaC/test/TestArrayDirectedGraph.hpp
scons test_suite=projects/CoGNaC/test/TestDifferentiationTree.hpp
scons test_suite=projects/CoGNaC/test/TestRandomBooleanNetwork.hpp
```


If each test run is passed, you can run some tests or simulations, or create your own test suites.


## Documentation

There are three folders - `networks_samples`, `src` and `test`.

 1. The `networks_samples` folder contains networks and matrices used for tests and simulations.
 1. The `src` folder contains the following classes:

* `ArrayDirectedGraph.hpp`, `GraphNode.hpp` - modelling a directed graph.
* `RandomBooleanNetwork.hpp` - used for the generation of a random Boolean network (RBN) and the attractor search.
* `ThresholdErgodicSetDifferentiationTree.hpp` - generating an ATN and a `DifferentiationTree` object from a RBN.
* `DifferentiationTree.hpp`, `DifferentiationTreeNode.hpp` - used to represent a cellular differentiation tree.
* `DifferentiationTreeBasedCellCycleModel.hpp`, `DifferentiationTreeBasedWithAsymmetricDivisionCellCycleModel.hpp` - used for the representation of a cell cycle model, using the information contained in a `DifferentiationTree` object and performing stochastic differentiation. In addition `DifferentiationTreeBasedWithAsymmetricDivisionCellCycleModel.hpp` implements stem cells asymmetric division.

 1. The `test` folder contains:

* `TestArryDirectedGraph.hpp` - testing `ArrayDirectedGraph.hpp` class.
* `TestDifferentiationTree.hpp` - testing `DifferentiationTree.hpp` class.
* `TestGraphNode.hpp` - testing `GraphNode.hpp` class.
* `TestRandomBooleanNetwork.hpp` - testing `RandomBooleanNetwork.hpp` class and the Buddy dependency.
* [TestSearchingGeneActivationPatternsInThelperNetworkLiteratePaper.hpp](https://github.com/Chaste/project_CoGNaC/blob/402efb914aecc0ae0f504bfaeba61f70e56b655c/test/TestSearchingGeneActivationPatternsInThelperNetworkLiteratePaper.hpp) - this file can be run to generate the results in Figure 3 showing the attractors of the Thelper newtork and the generated ATN.
* [TestCancerCellColonizationOfaColonCryptLiteratePaper.hpp](https://github.com/Chaste/project_CoGNaC/blob/402efb914aecc0ae0f504bfaeba61f70e56b655c/test/TestCancerCellColonizationOfaColonCryptLiteratePaper.hpp) - this file can be run to generate the results in Figure 4 showing the ATN and the differentiation tree and to generate the crypt simulations shown in Figure 5.


## Running tests

You can then run tests and simulations with, for example,

```bash
cd <Chaste3.3 path>
scons test_suite=projects/CoGNaC/test/TestSearchingGeneActivationPatternsInThelperNetwork.hpp
```

or

```bash
scons test_suite=projects/CoGNaC/test/TestCancerCellColonizationOfaColonCryptLiteratePaper.hpp
```


**NB**: the paper was developed with release version 3.2 and 3.3. We have not tested the compatibility with release version 3.1 or under.

For further information on using Chaste, see the [extensive guide material](/old_releases/release_3.3/ChasteGuides.html).
You may also wish to look at some of the [basic user tutorials](/old_releases/release_3.3/UserTutorials.html).


## Section contents
