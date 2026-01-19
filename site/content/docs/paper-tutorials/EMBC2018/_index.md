---
title: "Model of Vascular Remodelling"
draft: false
layout: "single"
showPageLinks: true
paperTutorialProject: "https://github.com/Chaste/project_EMBC2018"
---


This section contains pages generated automatically from the source code accompanying Osborne and Bernabeu (2018)
"A fully discrete open source framework for the simulation of vascular remodelling", [doi: 10.1109/EMBC.2018.8513223](https://doi.org/10.1109/EMBC.2018.8513223).

Email <jmosborne@unimelb.edu.au> or <miguel.bernabeu@ed.ac.uk> with any questions.

The code to run the multiple cylinder comparison simulations, which were used to produce Figure 2, can be found in the [Paper Tutorial](analyticcomparison) for that paper.

The code to run single coupled simulations, which was used to produce Figure 3, can be found in the `python` and `src` folders.

Before looking at this, you may wish to look at some of the [basic user tutorials](/old_releases/release_3.4/UserTutorials.html) for Chaste.


## Getting the code and installing dependencies

Before running these examples you will need to [install Chaste's dependencies](/old_releases/release_3.4/InstallGuides/InstallGuide.html) and the [source code for version 3.4](https://github.com/Chaste/Chaste/releases/tag/release_3.4).
The easiest way to do this is using an Ubuntu machine (or an Ubuntu virtual machine) as discussed on [InstallGuides/UbuntuPackage](/old_releases/release_3.4/InstallGuides/UbuntuPackage.html).
Note that Chaste is only fully supported on Linux/Unix systems, so users of Windows or Mac OS X may need to follow the virtual machine route.
For manual installation of each dependency, on any version of Linux, see DeveloperInstallGuide.

YOU WILL ALSO NEED TO INSTALL HEMELB. INSTRUCTIONS TO FOLLOW.


Finally you will need the source for the EMBC2018 project.  This can be done by checking out the version from the repository by using the command:

```bash
git clone https://github.com/Chaste/project_EMBC2018.git
```

Now the project should be installed, and everything should compile and run correctly.
You can now run the tests or simulations, or create your own test suites.


## Documentation

There are four folders - `matlab`,`python',`src` and `test`.

 1. The `matlab` folder contains scripts to plot Figure 2 from the paper.
 1. The `python` folder contains python scrips to couple our Chaste executables from `src` to HemeLB.
 1. The `src` folder contains the classes necesary to run the simulation. These define the aditional forces and boundary conditions not in the core Chaste code.
 1. The `test` folder contains:

    * [TestAnalyticComparisonLiteratePaper.hpp](https://github.com/Chaste/project_EMBC2018/blob/4cd02c1602cce9be482da39fb5ad61f661241067/test/TestAnalyticComparisonLiteratePaper.hpp) - this file can be run to generate the results presented in Figure 2.
    * [TestSetupFlowinPipe.hpp](https://github.com/Chaste/project_EMBC2018/blob/4cd02c1602cce9be482da39fb5ad61f661241067/test/TestSetupFlowInPipe.hpp) and [TestRunFlowInPipe.hpp](https://github.com/Chaste/project_EMBC2018/blob/4cd02c1602cce9be482da39fb5ad61f661241067/test/TestRunFlowInPipe.hpp) these files can be compiled and used with the code from `python` to generate the results in Figure 3.


### Running tests

You can then run tests and simulations with,

```bash
cd <Chaste path>
scons b=GccOpt ts=projects/EMBC2018/test/TestAnalyticComparisonLiteratePaper.hpp
```


----
**NB**: the paper was developed with release version 3.4. It will not work with with release version 3.3 or under.

For further information on using Chaste, see the [extensive guide material](/old_releases/release_3.4/ChasteGuides.html).
You may also wish to look at some of the [basic user tutorials](/old_releases/release_3.4/UserTutorials.html).


## Section contents
