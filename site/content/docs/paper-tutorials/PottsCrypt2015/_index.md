---
title: "A Cellular Potts Model (CPM) of Colorectal Cancer"
draft: false
layout: "single"
showPageLinks: true
paperTutorialProject: "https://github.com/Chaste/project_PottsCrypt2015"
---

This section contains pages generated automatically from the source code accompanying "Multiscale Model of Colorectal Cancer Using the Cellular Potts Framework" <http://dx.doi.org/10.4137/CIN.S19332>.

The code to run single simulations and was used to produce Figures 2 and 3 can be found here [TestPottsCryptLiteratePaper.hpp](https://github.com/Chaste/project_PottsCrypt2015/blob/8bf784bde6cc2e8db10093789c3b89a95fb3cba6/test/TestPottsCryptLiteratePaper.hpp)

The code to run parameter sweeps and was used produce Figure 4 can be found here [TestPottsCryptSweepsLiteratePaper.hpp](https://github.com/Chaste/project_PottsCrypt2015/blob/8bf784bde6cc2e8db10093789c3b89a95fb3cba6/test/TestPottsCryptSweepsLiteratePaper.hpp)

The code to run include mutations and was used produce Figures 5, 7 and 8 can be found here [TestPottsCryptMutantLiteratePaper.hpp](https://github.com/Chaste/project_PottsCrypt2015/blob/8bf784bde6cc2e8db10093789c3b89a95fb3cba6/test/TestPottsCryptMutantLiteratePaper.hpp)

Before looking at these, you may wish to look at some of the [basic user tutorials](/old_releases/release_3.3/UserTutorials.html) for Chaste.


## Getting the code and installing dependencies

Before running these examples you will need to [install Chaste's dependencies](/old_releases/release_3.4/InstallGuides/InstallGuide.html) and the [source code for version 3.3](https://github.com/Chaste/Chaste/releases/tag/release_3.3).
The easiest way to do this is using an Ubuntu machine (or an Ubuntu virtual machine) as discussed on [InstallGuides/UbuntuPackage](/old_releases/release_3.3/InstallGuides/UbuntuPackage.html).
Note that Chaste is only fully supported on Linux/Unix systems, so users of Windows or Mac OS X may need to follow the virtual machine route.
For manual installation of each dependency, on any version of Linux, see DeveloperInstallGuide.

**NB**: the paper was developed with release version 3.3 of Chaste. It does not work with release version 3.2 or under. It may need updating to work on newer revisions of the trunk code.

You will also need the source for the PottsCrypt2015 project.  This can be done by checking out the version from the repository by using the command

```bash
git clone https://github.com/Chaste/project_PottsCrypt2015.git PottsCrypt2015
```

in the projects folder of the Chaste directory.

Now the project should be installed, and everything should compile and run correctly.
You can now run the tests or simulations, or create your own test suites.


## Documentation

There are two folders - `src` and `test`.

 1. The `src` folder contains the following classes:

* `CellShapeOutputModifier.xpp` - Modifier class to output the area, perimeter, and circularity of cells in a simulation.
* `FixedSimpleWntCellCycleModel.xpp` - A version of the [SimpleWntCellCycleModel](https://chaste.cs.ox.ac.uk/public-docs/classSimpleWntCellCycleModel.html) class to represent the cell cycle model as described in the paper.
* `MutantBaseTrackerModifier.xpp` - Modifier class which tracks the base (and top) of the mutant patch.
* `MutantCellPottsUpdateRule.xpp` - The component of the Hamiltonian (represented as a `PottsUpdateRule`) which models mutant cells as described in the paper.

 1. The `test` folder contains:

* [TestPottsCryptLiteratePaper.hpp](https://github.com/Chaste/project_PottsCrypt2015/blob/8bf784bde6cc2e8db10093789c3b89a95fb3cba6/test/TestPottsCryptLiteratePaper.hpp) - this file can be run to generate the results in Figures 2 and 3.
* [TestPottsCryptSweepsLiteratePaper.hpp](https://github.com/Chaste/project_PottsCrypt2015/blob/8bf784bde6cc2e8db10093789c3b89a95fb3cba6/test/TestPottsCryptSweepsLiteratePaper.hpp) - this file can be run to generate the results in Figure 4.
* [TestPottsCryptMutantLiteratePaper.hpp](https://github.com/Chaste/project_PottsCrypt2015/blob/8bf784bde6cc2e8db10093789c3b89a95fb3cba6/test/TestPottsCryptMutantLiteratePaper.hpp) - this file can be run to generate the results in Figures 5 7 and 8.


## Running tests

You can then run tests and simulations with,

```bash
cd <Chaste3.3 path>
scons b=GccOpt ts=projects/PottsCrypt2015/test/TestPottsCryptLiteratePaper.hpp
```

and

```bash
scons b=GccOpt ts=projects/PottsCrypt2015/test/TestPottsCryptSweepLiteratePaper.hpp
```

and

```bash
scons b=GccOpt ts=projects/PottsCrypt2015/test/TestPottsCryptMutantLiteratePaper.hpp
```

**NB**: the paper was developed with release version 3.3. It will not work with with release version 3.2 or under.

For further information on using Chaste, see the [extensive guide material](/old_releases/release_3.3/ChasteGuides.html).
You may also wish to look at some of the [basic user tutorials](/old_releases/release_3.3/UserTutorials.html).


## Section contents
