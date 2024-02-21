---
title: "Using the cardiac executable"
draft: false
layout: "single"
images: []
---

This page provides examples of how to use the Chaste cardiac executable.

## Building the cardiac executable

Please see [Building Executable Apps](../../dev-guides/building-executable-apps/) for instructions on how to compile the cardiac executable, called simply `Chaste`.

## Running the executable

If you have built the executable yourself from source on the same machine, then your paths will (probably) be set up already, and you can simply run

```bash
./apps/src/Chaste <PATH TO CONFIG FILE>/ChasteParameters.xml
```

Then to run this in parallel you should use mpirun (or perhaps mpiexec) associated with the mpi/PETSc you used to compile Chaste:

```bash
mpirun -np N ./apps/src/Chaste <PATH TO CONFIG FILE>/ChasteParameters.xml
```

where N is the number of processes to run with.

## Visualization

In all of these examples, you can change to use the visualizer that you want by setting one of these options ([meshalyzer](https://opencarp.org/documentation/examples/visualization/meshalyzer), [vtk](https://vtk.org/) or [cmgui](https://www.cmiss.org/cmgui)) in the `<Simulation>` block:

```xml
<OutputVisualizer meshalyzer="yes" vtk="yes" cmgui="yes" precision="8"/>
```

vtk (visualized using [`paraview`](https://www.paraview.org/)) seems to be the most well supported and likely to still work if you are reading this in a few years, if not the simplest to use!

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

See [CodeGenerationFromCellML](/docs/user-guides/code-generation-from-cellml) for more details and options for annotations within CellML files.

* [UserTutorials/CardiacExecutable/UsingCellmlFiles](usingcellmlfiles) -- this shows how to use cell models defined directly from a cellml file (not one of the hardcoded options), and how to output cell model variables
* [UserTutorials/CardiacExecutable/DrugAction](drugaction) Running a simulation with multiple-channel drug action


## Utilities

* [UserTutorials/CardiacExecutable/MeshConvert](meshconvert) -- making the `MeshConvert` utility and using it to help produce scalable mesh loading
