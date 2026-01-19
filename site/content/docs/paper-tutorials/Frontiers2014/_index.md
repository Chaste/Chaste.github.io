---
title: "Cellular cardiac electrophysiology modelling with Chaste and CellML"
draft: false
layout: "single"
showPageLinks: true
paperTutorialProject: "https://github.com/Chaste/project_Frontiers2014"
---

This section contains pages generated automatically from the source code accompanying "[Cellular cardiac electrophysiology modelling with Chaste and CellML](http://dx.doi.org/10.3389/fphys.2014.00511)", our paper in [Frontiers in Physiology](http://journal.frontiersin.org/ResearchTopic/2502).

Before running these examples you will need to [install Chaste's dependencies](/old_releases/release_3.3/InstallGuides/InstallGuide.html) and the [source code for version 3.3](https://github.com/Chaste/Chaste/releases/tag/release_3.3).
The easiest way to do this is using an Ubuntu machine (or an Ubuntu virtual machine) as discussed on [InstallGuides/UbuntuPackage](/old_releases/release_3.3/InstallGuides/UbuntuPackage.html).
Note that cardiac Chaste is not supported on Windows, so users of Windows will need to follow the virtual machine route.
For manual installation of each dependency, on any version of Linux, see DeveloperInstallGuide.

The benchmark simulations from the paper are explained and annotated below.
For further information on using Chaste to solve these and related problems, see our [extensive guide material](/old_releases/release_3.3/ChasteGuides.html).


## Cellular electrophysiology benchmarks

The steps required to reproduce the study are:

 1. Generate accurate reference traces and calculate an acceptable level of error for each model ([Generating Reference Data](https://github.com/Chaste/project_Frontiers2014/blob/e495d4d2f7ae14f988de496f659f5056470c0434/test/TestGeneratingReferenceDataLiteratePaper.hpp))
 1. Work out the timesteps for each numerical method that are required to meet this error tolerance ([Calculate Required Timesteps](https://github.com/Chaste/project_Frontiers2014/blob/e495d4d2f7ae14f988de496f659f5056470c0434/test/TestCalculateRequiredTimestepsLiteratePaper.hpp))
 1. Benchmark solvers with these timesteps ([Ode Solving Times](https://github.com/Chaste/project_Frontiers2014/blob/e495d4d2f7ae14f988de496f659f5056470c0434/test/TestOdeSolvingTimesLiteratePaper.hpp))

You may if you wish run just the final step to benchmark the solvers on your system against our reference data and suggested timesteps.


## Tissue electrophysiology benchmarks

The [preliminary study examining convergence properties in space and time for the different models](https://github.com/Chaste/project_Frontiers2014/blob/e495d4d2f7ae14f988de496f659f5056470c0434/test/TestMonodomainConvergenceLiteratePaper.hpp) was run separately.
We then hardcoded suitable space and time steps for the PDE in the following steps, which can be followed to reproduce the study:

 1. Calculate the required ODE solver timesteps to meet target PDE accuracy ([Monodomain Calculate Required Timesteps](https://github.com/Chaste/project_Frontiers2014/blob/e495d4d2f7ae14f988de496f659f5056470c0434/test/TestMonodomainCalculateRequiredTimestepsLiteratePaper.hpp))
 1. Benchmark monodomain tissue simulation solving times with different numerical methods ([Monodomain Solving Times](https://github.com/Chaste/project_Frontiers2014/blob/e495d4d2f7ae14f988de496f659f5056470c0434/test/TestMonodomainSolvingTimesLiteratePaper.hpp))

Again, you may if you wish run just the final step to benchmark the solvers on your system against our reference data and suggested timesteps.


## Sample commands to install and run everything

If you wish to install the latest versions Chaste and this project direct from our repository, you may do so from the command line as follows:

```bash
#!sh
git clone -b release_3.3 https://chaste.cs.ox.ac.uk/git/chaste.git Chaste
cd Chaste/projects
git clone https://github.com/Chaste/project_Frontiers2014.git Frontiers2014
```


To run all the steps listed above, exploiting multiple cores on your machine where appropriate, use:

```bash
#!sh
cd path/to/Chaste
## Change the occurrences of 8 below to match the number of cores available
scons chaste_libs=1 brief=1 build=GccOptNative_8 -j8 projects/Frontiers2014/test/TestGeneratingReferenceDataLiteratePaper.hpp
scons chaste_libs=1 brief=1 build=GccOptNative_8 -j8 projects/Frontiers2014/test/TestCalculateRequiredTimestepsLiteratePaper.hpp
scons chaste_libs=1 brief=1 build=GccOptNative_8 -j8 projects/Frontiers2014/test/TestOdeSolvingTimesLiteratePaper.hpp

## Note the change in build= option: these simulations cannot run in parallel
scons chaste_libs=1 brief=1 build=GccOptNative -j8 projects/Frontiers2014/test/TestMonodomainCalculateRequiredTimestepsLiteratePaper.hpp
scons chaste_libs=1 brief=1 build=GccOptNative -j8 projects/Frontiers2014/test/TestMonodomainSolvingTimesLiteratePaper.hpp

## To run the preliminary study on PDE convergence, use
scons chaste_libs=1 brief=1 build=GccOptNative -j8 projects/Frontiers2014/test/TestMonodomainConvergenceLiteratePaper.hpp run_time_flags="--timestep 0.001 --spacestep 0.001 --reset"
## Other values for timestep & spacestep can be given, as desired.
## The --reset flag says to reset CVODE fully at each PDE time step.
```


## Section contents
