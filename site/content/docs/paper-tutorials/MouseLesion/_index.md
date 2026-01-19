---
title: "Connexin 43 contributes to electrotonic conduction across scar tissue in the intact heart"
draft: false
layout: "single"
showPageLinks: true
paperTutorialProject: "https://github.com/Chaste/project_MouseLesion"
---


This section contains pages generated automatically from the source code accompanying
Mahoney et al. "Connexin 43 contributes to electrotonic conduction across scar tissue in the intact heart",
[Scientific Reports 6:26744 (2016)](http://www.nature.com/articles/srep26744).

Before running these examples you will need to [install Chaste's dependencies](https://chaste.github.io/old_releases/release_3.3/InstallGuides/InstallGuide.html) and the [source code for version 3.3](https://github.com/Chaste/Chaste/releases/tag/release_3.3).
The easiest way to do this is using an Ubuntu machine (or an Ubuntu virtual machine) as discussed on [InstallGuides/UbuntuPackage](https://chaste.github.io/old_releases/release_3.3/InstallGuides/UbuntuPackage.html).
Note that cardiac Chaste is not supported on Windows, so users of Windows will need to follow the virtual machine route.
For manual installation of each dependency, on any version of Linux, see DeveloperInstallGuide.

The simulations featured in the paper supplement are explained and annotated below.
For further information on using Chaste to solve these and related problems, see our [extensive guide material](https://chaste.github.io/old_releases/release_3.3/ChasteGuides.html).


## Sample commands to install Chaste

If you wish to install Chaste direct from our repository, you may do so from the command line as follows:

```bash
#!sh
git clone -b release_3.3 https://chaste.cs.ox.ac.uk/git/chaste.git Chaste
cd Chaste/projects
git clone https://github.com/Chaste/project_MouseLesion
```


## Code compilation

To compile the simulators, use:

```bash
#!sh
cd <path to Chaste source>
scons chaste_libs=1 brief=1 build=GccOptNative projects/MouseLesion
```


## Mouse Lesion study

The steps required to reproduce the study are:

 1. Run a simulation of a 2D lesion, with varying command line parameters ([C++ file for performing simulation](https://github.com/Chaste/project_MouseLesion/blob/e3ec7ce88b6cfb18e58369923d8afaee558f7bd0/test/TestFibroblastsLiteratePaper.hpp))
 1. Run a simulation of a 3D lesion, with varying command line parameters ([C++ file for performing simulation](https://github.com/Chaste/project_MouseLesion/blob/e3ec7ce88b6cfb18e58369923d8afaee558f7bd0/test/TestFibroblasts3dLiteratePaper.hpp))

To vary parameters and run simulations for the results shown in the paper, use the script `run_lesion_simulations.sh` and then (when they have finished) `collate_lesion_results.sh`,
followed by the matlab script `test/data/processing_scripts/process_APs_capacitance.m` to do the post-processing.


## Section contents
