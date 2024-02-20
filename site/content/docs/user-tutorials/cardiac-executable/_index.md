---
title: "Using the cardiac executable"
draft: false
layout: "single"
images: []
---

This page provides examples of how to use the Chaste cardiac executable.

## Commands

### Downloaded executable

If you have downloaded the executable you can run it with

```bash
./Chaste.sh <PATH TO CONFIG FILE>/ChasteParameters.xml
```

(the script will set up the necessary library paths etc. and then call the Chaste executable).
The downloadable executable is specially built with an old mpi version to run in parallel on most machines, so you can do

```bash
./Chaste.sh -np N <PATH TO CONFIG FILE>/ChasteParameters.xml
```

where N is the number of processes to run with.

### Compiled executable

If you have built the executable yourself from source (this is required only for [dynamic loading of CellML files](#further-examples-using-dynamic-loading-of-cellml-files)), then your paths will (probably) be set up already, and you can simply run

```bash
./apps/src/Chaste <PATH TO CONFIG FILE>/ChasteParameters.xml
```


Then to run this in parallel you should use mpirun (or perhaps mpiexec) associated with the mpi you used to compile Chaste:

```bash
mpirun -np N ./apps/src/Chaste <PATH TO CONFIG FILE>/ChasteParameters.xml
```

where N is the number of processes to run with.

## Visualization

In all of these examples, you can change to use the visualizer that you want by setting one of these options (meshalyzer, vtk, cmgui) in the `<Simulation>` block:

```xml
<OutputVisualizer meshalyzer="yes" vtk="yes" cmgui="yes" precision="8"/>
```

[vtk](https://www.vtk.org/) (visualized using `paraview`) seems to be the most well supported and likely to still work if you are reading this in a few years, if not the simplest to use!

## Basic simulations

* [UserTutorials/CardiacExecutable/Propagation1d](propagation1d) -- simple simulation on a 1d fibre
* [UserTutorials/CardiacExecutable/S1S2Protocol](s1s2protocol) -- 2d spiral wave simulation produced by two stimuli
* [UserTutorials/CardiacExecutable/Propagation3d](propagation3d)-- propagation on a anatomically realistic down-sampled ventricular mesh using fibre directions.  This tutorial also discusses visualising the results in different tools.

## Examples of further functionality

* How to determine what the [hardcoded cell model](hardcodedcellmodels) options are
    * See [below](#further-examples-using-dynamic-loading-of-cellml-files) for dynamic loading of CellML files
* [UserTutorials/CardiacExecutable/HeterogeneousExample](heterogeneousexample)
* [UserTutorials/CardiacExecutable/UsingFibreDefinitions](usingfibredefinitions) -- also mentions postprocessing options
* [UserTutorials/CardiacExecutable/BidomainSimulationsWithPerfusingBath](bidomainsimulationswithperfusingbath)
* [UserTutorials/CardiacExecutable/CheckpointingAndRestarting](checkpointingandrestarting) -- how to do checkpoint and restart.


## Further examples using dynamic loading of CellML files

These require a full developer install and the executable to be built from the source, since the CellML files need to be converted into code and compiled, see [CodeGenerationFromCellML](/docs/user-guides/code-generation-from-cellml) for more details.


* [UserTutorials/CardiacExecutable/UsingCellmlFiles](usingcellmlfiles) -- this shows how to use cell models defined directly from a cellml file (not one of the hardcoded options), and how to output cell model variables
* [UserTutorials/CardiacExecutable/DrugAction](drugaction) Running a simulation with multiple-channel drug action


## Utilities

* [UserTutorials/CardiacExecutable/MeshConvert](meshconvert) -- making the `MeshConvert` utility and using it to help produce scalable mesh loading
