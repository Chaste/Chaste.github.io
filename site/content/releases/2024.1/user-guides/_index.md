---
title: "User Guides"
description: "User Guides"
draft: false
images: []
toc: true
layout: "single"
version: "2024.1"
version: "2024.1"
---

{{< callout context="note" title="Note" icon="info-circle" >}}

Before reading this have a look at [Getting Started](../) to decide whether you
are a _user_ of releases or a _developer_ contributing back to Chaste core code.

{{< /callout >}}

_Users_ can download the latest stable release of the source code from our
[GitHub releases page](https://github.com/Chaste/Chaste/releases), or checkout
the `develop` branch to get the latest features.

## Installation

- [Install Guides](../installguides): How to install Chaste and its
  dependencies.
- [CMake First Run Guide](cmake-first-run): How to configure, build, and run tests to
  check the installation.

## Running Chaste Simulations

- [Tutorials](../user-tutorials): Detailed lessons on using Chaste's capabilities.
- [Visualisation Guides](visualisation-guides): Information on how to visualise
  simulation results.
- [How-to Index](../how-tos): Links to code snippets illustrating how various
  things can be done in Chaste.
- [User Projects](user-projects): Creating/using a project which can utilize the
  core Chaste code and build/testing framework.

## Code Documentation
- [Changes Since Last Release](../release-notes/changes-since-last-release)
- [Release Notes](../release-notes/release-notes)
- [API Documentation](../doxygen)

## Miscellaneous Information
- [Chaste Units](chaste-units): Units of parameters used in Chaste.
- Default Cardiac parameter values: These are read off from
  [`heart/src/problem/HeartConfigDefaults.hpp`](https://github.com/Chaste/Chaste/blob/develop/heart/src/problem/HeartConfigDefaults.hpp)
  (ignore the `Simulation` block, which only applies to the old cardiac
  executable).
- File Formats: This information is given in the version of
  [`docs/FileFormats.html`](https://raw.githubusercontent.com/Chaste/Chaste/develop/docs/FileFormats.html)
  supplied with the release.

## Advanced

- [Boost Serialization](boost-serialization): Notes on using the the
  Serialization library from Boost to checkpoint and save/resume simulations.
- [Cardiac Mechanics Solvers](cardiac-mechanics-solvers): A bit of information
  on how the cardiac mechanics solvers are connected to the main mechanics
  solvers.
- [Cell-based Chaste Code Structure](cell-based-chaste-code-structure): An
  overview of the structure of the cell-based Chaste codebase.
- [Code Generation from CellML](code-generation-from-cellml): Notes on
  generating Chaste code for cardiac cell models from CellML files, using
  chaste_codegen.
- [Finding Chaste Dependencies](finding-chaste-dependencies): Notes on manually
  setting hints for Chaste dependency locations if they are not found
  automatically.
-
  [Finite Element Assemblers and Solvers](finite-element-assemblers-and-solvers):
  Notes on how PDE assemblers and solvers work internally.
- [Finite Element Implementations](finite-element-implementations): A lists of
  the equations and finite element implementations used in various solvers in
  the Chaste codebase.
- [Installing chaste_codegen](install-codegen): Guidance on manually installing
  chaste_codegen.
- [Running Binaries From Command Line](running-binaries-from-command-line): How
  to run binaries directly rather than via `ctest`.
- [Solving Cardiac Problems](solving-cardiac-problems): A high-level overview of
  the code execution flow when solving a cardiac problem.
- [State Variable Interpolation](state-variable-interpolation): How and when to
  use state-variable interpolation to compute the ionic current in tissue
  simulations.
- [Structure of Cell-based Simulations](structure-of-cell-based-simulations): An
  overview of the steps involved in setting up and running a cell-based
  simulation.
