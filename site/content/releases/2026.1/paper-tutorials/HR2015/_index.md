---
title: "HCQ reduces heart rate by modulating the hyperpolarisation-activated current *If*: Novel electrophysiological insights and therapeutic potential"
draft: false
layout: "single"
showPageLinks: true
paperTutorialProject: "https://github.com/Chaste/project_HR2015"
version: "2026.1"
---


This section contains pages generated automatically from the source code accompanying Capel et al., [Hydroxychloroquine reduces heart rate by modulating the hyperpolarisation activated current ‘If’: Novel electrophysiological insights and therapeutic potential.](http://dx.doi.org/10.1016/j.hrthm.2015.05.027), Heart Rhythm, (2015).

Before running these examples you will need to [install Chaste's dependencies](/old_releases/release_3.3/InstallGuides/InstallGuide.html) and the [source code for version 3.3](https://github.com/Chaste/Chaste/releases/tag/release_3.3).
The easiest way to do this is using an Ubuntu machine (or an Ubuntu virtual machine) as discussed on [InstallGuides/UbuntuPackage](/old_releases/release_3.3/InstallGuides/UbuntuPackage.html).
Note that cardiac Chaste is not supported on Windows, so users of Windows will need to follow the virtual machine route.
For manual installation of each dependency, on any version of Linux, see DeveloperInstallGuide.

The simulations featured in the paper supplement are explained and annotated below.
For further information on using Chaste to solve these and related problems, see our [extensive guide material](/old_releases/release_3.3/ChasteGuides.html).


## Sino-atrial node study

The steps required to reproduce the study are:

 1. Run a single cell simulation of a sino-atrial node model, with varying degrees of funny current block ([C++ file for performing simulation](https://github.com/Chaste/project_HR2015/blob/1e6f5888078c4a20005ee259938ccce93e957f12/test/TestSanWithFunnyCurrentBlockLiteratePaper.hpp))
 1. Run the matlab script `whole_cell_apd_changes.m` (after updating a folder name at the top to match your `CHASTE_TEST_OUTPUT` environment variable).


## Sample commands to install and run everything

If you wish to install Chaste and this project direct from our repository, you may do so from the command line as follows:

```bash
#!sh
git clone -b release_3.3 https://chaste.cs.ox.ac.uk/git/chaste.git Chaste
cd Chaste/projects
git clone https://github.com/Chaste/project_HR2015.git HR2015
```

To run the simulations, use:

```bash
#!sh
cd path/to/Chaste
scons chaste_libs=1 brief=1 build=GccOptNative projects/HR2015
```


## Section contents
