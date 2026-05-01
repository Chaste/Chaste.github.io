---
title: "Model of Crypt Fission"
draft: false
layout: "single"
showPageLinks: true
paperTutorialProject: "https://github.com/Chaste/project_CryptFissionPlos2016"
version: "2026.1"
---

This section contains pages generated automatically from the source code accompanying Langlands et al. (2016)
"Paneth cell-rich regions separated by a cluster of Lgr5+ cells initiate fission in the intestinal stem cell niche" <http://dx.doi.org/10.1371/journal.pbio.1002491>

The code to run single simulations, which was used to produce Figure 9, can be found here [TestCryptFissionLiteratePaper.hpp](https://github.com/Chaste/project_CryptFissionPlos2016/blob/04483b5e62bff1094bb320564c0fbaa2698563b0/test/TestCryptFissionLiteratePaper.hpp).

Before looking at this, you may wish to look at some of the [basic user tutorials](/old_releases/release_3.4/UserTutorials.html) for Chaste.


## Getting the code and installing dependencies

Before running these examples you will need to [install Chaste's dependencies](/old_releases/release_3.4/InstallGuides/InstallGuide.html) and the [source code for version 3.4](https://github.com/Chaste/Chaste/releases/tag/release_3.4).
The easiest way to do this is using an Ubuntu machine (or an Ubuntu virtual machine) as discussed on [InstallGuides/UbuntuPackage](/old_releases/release_3.4/InstallGuides/UbuntuPackage.html).
Note that Chaste is only fully supported on Linux/Unix systems, so users of Windows or Mac OS X may need to follow the virtual machine route.
For manual installation of each dependency, on any version of Linux, see DeveloperInstallGuide.

You will also need the source for the CryptFissionPlos2016 project.  This can be done by checking out the version from the repository by using the command

```bash
git clone https://github.com/Chaste/project_CryptFissionPlos2016.git CryptFissionPlos2016
```

in the projects folder of the Chaste directory.

Now the project should be installed, and everything should compile and run correctly.
You can now run the tests or simulations, or create your own test suites.


## Documentation

There are two folders - `src` and `test`.

 1. The `src` folder contains the classes necesary to run the simulation. These define the aditional forces and boundary conditions not in the core chaste code.
 1. The `test` folder contains:

* [TestCryptFissionLiteratePaper.hpp](https://github.com/Chaste/project_CryptFissionPlos2016/blob/04483b5e62bff1094bb320564c0fbaa2698563b0/test/TestCryptFissionLiteratePaper.hpp) - this file can be run to generate the results in Figure 9


### Running tests

You can then run tests and simulations with,

```bash
cd <Chaste3.4 path>
scons b=GccOpt ts=projects/CryptFissionPlos2016/test/TestCryptFissionLiteratePaper.hpp
```

**NB**: the paper was developed with release version 3.3, but will work on release version 3.4. It will not work with with release version 3.2 or under.

For further information on using Chaste, see the [extensive guide material](/old_releases/release_3.4/ChasteGuides.html).
You may also wish to look at some of the [basic user tutorials](/old_releases/release_3.4/UserTutorials.html).


## Section contents
