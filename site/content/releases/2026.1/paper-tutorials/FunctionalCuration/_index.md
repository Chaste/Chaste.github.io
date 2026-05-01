---
title: "Functional Curation"
draft: false
layout: "single"
showPageLinks: true
paperTutorialProject: "https://github.com/Chaste/project_FunctionalCuration"
version: "2026.1"
---


The [FunctionalCuration](https://github.com/Chaste/project_FunctionalCuration) project is an add-on to Chaste aiming to provide a framework for a coherent approach to model fitting, simulation, comparison and validation.
It does this by separate model structure (described in [CellML](http://www.cellml.org/)) from details of the experimental scenario to apply to a model.
Experiments are described in a protocol language extending [SED-ML](http://www.sed-ml.org/).
For more details see the [FunctionalCuration](https://github.com/Chaste/trac_archive/wiki/Functional-Curation) wiki pages.

The inaugural paper on Functional Curation is
"[High throughput functional curation of cellular electrophysiology models](./functionalcuration)",
published in *Prog Biophys Mol Biol* in 2011, and the linked wiki page gives details of how to
reproduce the results from that paper, having installed the necessary Chaste components and dependencies
as set out below.

For work on applying Functional Curation to the cell-based side of Chaste, see our
[paper in ICCS2013](../wisc2013).


## Installation

This project requires the Chaste source tree to be installed, and you to have write access to your local copy, in order to be usable.
You will thus need to [install Chaste's dependencies](/old_releases/release_3.2/InstallGuides/InstallGuide.html) and build the Chaste software yourself.
The easiest way to do this is using an Ubuntu machine (or an Ubuntu virtual machine) as discussed on InstallGuides/UbuntuPackage.
For manual installation of each dependency, on any version of Linux, see DeveloperInstallGuide.
Note that you will require those Chaste dependencies marked as 'cardiac only', and that this project requires at least
version 1.39 of the Boost libraries.  In order to generate result figures automatically, you will also need to install
[Gnuplot](http://www.gnuplot.info/).

Note that it is advisable to install the source tree on local disk, rather than an NFS mount: we have experienced occasional
problems in the latter case, depending on Linux distribution and version.  Compiling Chaste is also fairly disk intensive, so
benefits from local storage.

Having installed (and ideally tested!) the Chaste source tree, unpack this project
as `<Chaste>/projects/FunctionalCuration`.  It is crucial to match the folder name
and location, or the project will not work.

If you wish to work with the latest version of the Chaste and project code, you can obtain them
from the Chaste repository using the following commands:

```bash
git clone --branch "release_3.2" https://github.com/Chaste/Chaste.git Chaste
cd Chaste/projects
git clone --branch "FunctionalCuration_release_3.2" https://github.com/Chaste/project_FunctionalCuration.git FunctionalCuration
```


## Usage

Source code for the project is contained in the `src` folder, and tests of its
functionality in `tests`.  Annotated CellML files suitable for use with the framework
are in `cellml`.  Some additional interesting locations are:

* `tests/protocols`  contains example protocols
* `src/proto/library`  contains protocol libraries with functions available to all protocols
* `src/proto/parsing/protocol.rnc`  is a schema for the protocol XML language


See the [sub-page for our main paper](./functionalcuration) for details of how to reproduce
its results.  There are also many tests covering the lower-level functionality available for use by
protocols.  Run all the default tests with:

```bash
scons cl=1 b=GccOpt projects/FunctionalCuration
```

If you have multiple cores available, you can build in parallel with (using 4 cores for example):

```bash
scons -j4 cl=1 b=GccOpt projects/FunctionalCuration
```


To build an executable that can run a single protocol on a single model, do:

```bash
scons cl=1 exe=1 b=GccOpt projects/FunctionalCuration/apps
```

The executable will appear at `projects/FunctionalCuration/apps/src/FunctionalCuration`.
You'll need the environment variable `LD_LIBRARY_PATH` set up as described in the Chaste
documentation in order to run it, since it needs to find the Chaste libraries and their
dependencies.

For further information on using Chaste generally, see our [extensive guide material](/old_releases/release_3.2/ChasteGuides.html).
You may also wish to look at some of the [basic user tutorials](/old_releases/release_3.2/UserTutorials.html).


## Section contents
