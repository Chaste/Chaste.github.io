---
title: "On-Lattice Agent-based Simulation of Populations of Cells within the Open-Source Chaste Framework"
draft: false
layout: "single"
showPageLinks: true
paperTutorialProject: "https://github.com/Chaste/project_InterfaceFocus2013"
version: "2024.2"
---


This section contains pages generated automatically from the source code accompanying
Figueredo et al (2013) "On-Lattice Agent-based Simulation of Populations of Cells within the Open-Source Chaste Framework", Royal Society Interface Focus.
[doi: 10.1098/rsfs.2012.0081](https://doi.org/10.1098/rsfs.2012.0081)

The code to run single simulations, which was used to produce the figures in the paper, can be found here
[TestCaWithMultipleMutationStatesLiteratePaper.hpp](https://github.com/Chaste/project_InterfaceFocus2013/blob/ad1b4be9d7cadeb23e931a8ab46e12022e5071e2/test/TestCaWithMultipleMutationStatesLiteratePaper.hpp)
and here [TestCaBasedCellPopulationUsingPdesLiteratePaper.hpp](https://github.com/Chaste/project_InterfaceFocus2013/blob/ad1b4be9d7cadeb23e931a8ab46e12022e5071e2/test/TestCaBasedCellPopulationUsingPdesLiteratePaper.hpp)

Before looking at this, you may wish to look at some of the [basic user tutorials](/old_releases/release_3.2/UserTutorials.html) for Chaste.


## Getting the code and installing dependencies

Before running these examples you will need to [install Chaste's dependencies](h/old_releases/release_3.2/InstallGuides/InstallGuide.html) and the [source code for version 3.2](https://github.com/Chaste/Chaste/releases/tag/release_3.2).
The easiest way to do this is using an Ubuntu machine (or an Ubuntu virtual machine) as discussed on [InstallGuides/UbuntuPackage](/old_releases/release_3.4/InstallGuides/UbuntuPackage.html).
Note that Chaste is only fully supported on Linux/Unix systems, so users of Windows or Mac OS X may need to follow the virtual machine route.
For manual installation of each dependency, on any version of Linux, see DeveloperInstallGuide.

*2026 note: you will need to find the corresponding Git commit, which is very close to [this commit](https://github.com/Chaste/Chaste/commit/5e5ed91bf8d07d718cd3632f27fac94da83d08bc).*

You will need to checkout revision 18673 of the Chaste source code.  This can be done by checking out the version from the repository by using the command

```bash
svn checkout https://chaste.cs.ox.ac.uk/svn/chaste/trunk -r 18673
```


You will also need the source for the InterfaceFocus2013 project.  This can be done by checking out the version from the repository by using the command

```bash
git clone https://github.com/Chaste/project_InterfaceFocus2013.git InterfaceFocus2013
```

in the projects folder of the Chaste directory. If you dont have a Chaste user account you can use the username "anonymous" and your email for the password.

Now the project should be installed, and everything should compile and run correctly.
You can now run the tests or simulations, or create your own test suites.


## Documentation

There are two folders - `src` and `test`.

 1. The `src` folder contains the classes necesary to run the simulation. These define the aditional ell cycle models etc. that  not in the core chaste code.
 1. The `test` folder contains:

* [TestCaWithMultipleMutationStatesLiteratePaper.hpp](https://github.com/Chaste/project_InterfaceFocus2013/blob/ad1b4be9d7cadeb23e931a8ab46e12022e5071e2/test/TestCaWithMultipleMutationStatesLiteratePaper.hpp) - this file can be run to generate the results in the paper.
* [TestCaBasedCellPopulationUsingPdesLiteratePaper.hpp](https://github.com/Chaste/project_InterfaceFocus2013/blob/ad1b4be9d7cadeb23e931a8ab46e12022e5071e2/test/TestCaBasedCellPopulationUsingPdesLiteratePaper.hpp) - this file can be run to generate the results in the paper.


## Running tests

You can then run tests and simulations with,

```bash
cd <Chaste path>
scons b=GccOpt ts=projects/InterfaceFocus2013/test/TestCaWithMultipleMutationStatesLiteratePaper.hpp
```

and

```bash
scons b=GccOpt ts=projects/InterfaceFocus2013/test/TestCaBasedCellPopulationUsingPdesLiteratePaper.hpp
```


**NB**: the paper was developed with r18673 version. It may not work with other revisions.

For further information on using Chaste, see the [extensive guide material](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides).
You may also wish to look at some of the [basic user tutorials](https://github.com/Chaste/trac_archive/wiki/User-Tutorials).


## Section contents
