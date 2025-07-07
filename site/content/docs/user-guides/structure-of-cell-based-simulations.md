---
title: "Structure of Cell-based Simulations in Chaste"
description: "Structure of Cell-based Simulations in Chaste"
draft: false
images: []
toc: true
layout: "single"
---

This page is intended for new cell-based Chaste users/developers and was written as part of the 2012 Chaste cell-based modelling workshop to summarize the structure of cell-based simulations in Chaste.
For information, see the technical [Chaste papers](/publications).

## Initialization

In order to set up a simulation object, we first need to do the following:

- Set up a vector of `Cell`s (for example, by using a helper class such as
  `CellsGenerator`) and an associated mesh (for example, by using a helper class
  such as `HoneycombMeshGenerator`). Note that in the case of node-based
  simulations, we still supply a mesh, albeit a special type called
  `NodesOnlyMesh`.
- Using these, we may then create a suitable subclass of
  `AbstractCellPopulation`.
- Using this, we may then create a suitable subclass of
  `AbstractCellBasedSimulation`.
- Further objects, such as `Force`s or `CellKiller`s, may also be passed to the
  simulation object in order to fully specify a model.
- Prior to calling `Solve()`, we must first call the methods
  `SetOutputDirectory()` and `SetEndTime()` on the simulation object, in order
  to specify where results are written to file and for how long we wish the
  simulation to proceed. We may also call `SetSamplingTimestepMultiple()` on the
  simulation object, which specifies how often results are written to file.

## The Solve() method

The actual simulation of a cell-based model is implemented by calling the method
`Solve()` on a subclass of `AbstractCellBasedSimulation`. This method comprises
a number of steps, which we summarize below:

**Initialization**: begin by setting up the simulation via the following steps:

- Set up the `SimulationTime` singleton class: given the specified end time and
  size of time step, compute the number of time steps.
- Set up the simulation output directory using the specified directory name and
  create output files.
- Call the method `SetupSolve()` on the simulation object. This method can be
  overridden by child classes (e.g. to set up a PDE solver).
- Age the cells to the correct time. Note that cells are created with negative
  birth times so that some are initially almost ready to divide.
- Output initial conditions to file.

**Main time loop**: while not yet at the end time, and as long as no stopping
event has occurred, simulate the cell population via the following steps.

- Call the method `UpdateCellPopulation()` on the simulation object, which in
  turn calls `DoCellRemoval()`, `DoCellBirth()` and `CellPopulation::Update()`.
  - **TODO**: talk a bit more about `DoCellRemoval()`, `DoCellBirth()` and `CellPopulation::Update()`.
- Call the method `UpdateCellLocationsAndTopology()` on the simulation object,
  which synchronously updates the location of each cell as well as the cell
  topology (which cells are neighbours of each other).
  - **TODO**: talk a bit more about `UpdateCellLocationsAndTopology()`.
- Call the method `PostSolve()` on the simulation object, which may be
  overridden by child classes (e.g. to solve a PDE).
- Increment the simulation time by one time step and output the results to file.
- Note that we proceed through the main time loop as long as the simulation
  method `StoppingEventHasOccurred()` returns `false`. This method is evaluated
  at the start of each time step, and can be used to specify conditions under
  which we require the simulation to stop prematurely. For example, we might
  wish to simulate a crypt until it becomes monoclonal, if this event occurs.

**Post-processing**: after leaving the main time loop, tidy up via the following
steps.

- Carry out a final call to the `UpdateCellPopulation()` method so that the cell
  population is coherent with new cell positions. Note that cell birth and death
  still need to be checked because they may be spatially dependent.
- Call the method `AfterSolve()` on the simulation object, which may be
  overridden by child classes (e.g. to solve a PDE).
- Close output files.
- Note that a helper class, `CellBasedEventHandler`, can be used to evaluate the
  time spent in each part of the cell-based code.

File format information is given in the file `docs/FileFormats.html`, supplied
with the release. (The latest version of this file may also be viewed
[here](https://raw.githubusercontent.com/Chaste/Chaste/develop/docs/FileFormats.html)).

{{< callout context="tip" title="See Also" icon="outline/rocket" >}}

- [Cell-based Chaste Code Structure](../cell-based-chaste-code-structure)
- [User Tutorials](../../user-tutorials/)
- [Chaste Papers](/publications)

{{< /callout >}}
