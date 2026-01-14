---
title: "Model of Crypt Fission"
draft: false
layout: "single"
paperTutorialProject: "https://github.com/Chaste/project_CryptFissionPlos2016"
---

This section contains pages generated automatically from the source code accompanying Langlands et al. (2016)
"Paneth cell-rich regions separated by a cluster of Lgr5+ cells initiate fission in the intestinal stem cell niche" http://dx.doi.org/10.1371/journal.pbio.1002491

The code to run single simulations, which was used to produce Figure 9, can be found here [TestCryptFissionLiteratePaper.hpp](https://github.com/Chaste/trac_archive/wiki/Paper-Tutorials-_-Crypt-Fission-Plos2016-_-Crypt-Fission)

Before looking at this, you may wish to look at some of the [basic user tutorials](https://github.com/Chaste/trac_archive/wiki/User-Tutorials) for Chaste.


### Getting the code and installing dependencies

Before running these examples you will need to [install Chaste's dependencies](https://github.com/Chaste/trac_archive/wiki/Install-Guides-_-Install-Guide) and the [source code for version 3.4](http://www.cs.ox.ac.uk/chaste/download.html).
The easiest way to do this is using an Ubuntu machine (or an Ubuntu virtual machine) as discussed on [InstallGuides/UbuntuPackage](https://github.com/Chaste/trac_archive/wiki/Install-Guides-_-Ubuntu-Package).
Note that Chaste is only fully supported on Linux/Unix systems, so users of Windows or Mac OS X may need to follow the virtual machine route.
For manual installation of each dependency, on any version of Linux, see DeveloperInstallGuide.

You will also need the source for the CryptFissionPlos2016 project.  This can be done by checking out the version from the repository by using the command

```

svn checkout https://chaste.cs.ox.ac.uk/svn/chaste/projects/CryptFissionPlos2016
```

in the projects folder of the Chaste directory. You will need to use the supplied username and password.

Now the project should be installed, and everything should compile and run correctly.
You can now run the tests or simulations, or create your own test suites.

### Documentation
There are two folders - `src` and `test`.
 1. The `src` folder contains the classes necesary to run the simulation. These define the aditional forces and boundary conditions not in the core chaste code.
 1. The `test` folder contains:

* [TestCryptFissionLiteratePaper.hpp](https://github.com/Chaste/trac_archive/wiki/Paper-Tutorials-_-Crypt-Fission-Plos2016-_-Crypt-Fission) - this file can be run to generate the results in Figure 9

 == Running tests ==
You can then run tests and simulations with,

```

cd <Chaste3.4 path>
scons b=GccOpt ts=projects/CryptFissionPlos2016/test/TestCryptFissionLiteratePaper.hpp
```

----
**NB**: the paper was developed with release version 3.3, but will work on release version 3.4. It will not work with with release version 3.2 or under.

For further information on using Chaste, see the [extensive guide material](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides).
You may also wish to look at some of the [basic user tutorials](https://github.com/Chaste/trac_archive/wiki/User-Tutorials).


-----
### Section contents
[SubWiki()](SubWiki())

