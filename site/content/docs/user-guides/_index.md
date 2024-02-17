---
title: "User Guides"
description: "User Guides"
draft: false
images: []
toc: true
layout: "single"
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
- [CMake First Run](cmake-first-run): How to configure, build, and run tests to
  check the installation. For all available options, including compiling
  optimised code, see the full
  [CMake Build Guide](../dev-guides/cmake-build-guide).

## Running Chaste simulations

- [Tutorials](../user-tutorials): Detailed lessons on using Chaste's capabilities.
- [How-to Index](../how-tos): Links to code snippets illustrating how various
  things can be done in Chaste.
- [Visualisation Guides](visualisation-guides): Information on how to visualise
  simulation results.
- [User Projects](user-projects): Creating/using a project which can utilize the
  core Chaste code and build/testing framework.
- [Boost Serialization](boost-serialization): Notes on using the the
  Serialization library from Boost to checkpoint and save/resume simulations.

### Code documentation
- [Changes since last release](../release-notes/changes-since-last-release)
- [Release notes](../release-notes/release-notes)
- [API Documentation](../doxygen)


## Advanced

### General
- [Running Binaries From Command Line](running-binaries-from-command-line)
- [Finding Chaste Dependencies](finding-chaste-dependencies): Notes on manually
  setting hints for Chaste dependency locations if they are not found
  automatically.
- [Finite Element Assemblers and Solvers](finite-element-assemblers-and-solvers)
- [Finite Element Implementations](finite-element-implementations)

### Cardiac
- [Cardiac Mechanics Solvers](cardiac-mechanics-solvers): A bit of information
  on how the cardiac mechanics solvers are connected to the main mechanics
  solvers.
- [Code Generation from CellML](code-generation-from-cellml): Notes on
  generating Chaste code for cardiac cell models from CellML files, using
  chaste_codegen.
- [Installing chaste_codegen](install-codegen): Guidance on manually installing chaste_codegen.
- [Solving Cardiac Problems](solving-cardiac-problems)
- [State Variable Interpolation](state-variable-interpolation)

### Cell-based
- [Cell-based Code Structure](cell-based-chaste-code-structure): An
  overview of cell-based Chaste.

## Miscellaneous information
- [Chaste Units](chaste-units): Units of parameters used in Chaste.
- Default Cardiac parameter values: These are read off from
  [`heart/src/problem/HeartConfigDefaults.hpp`](https://github.com/Chaste/Chaste/blob/develop/heart/src/problem/HeartConfigDefaults.hpp)
  (ignore the `Simulation` block, which only applies to the old cardiac
  executable).
- File Formats: This information is given in the version of
  [`docs/FileFormats.html`](https://raw.githubusercontent.com/Chaste/Chaste/develop/docs/FileFormats.html)
  supplied with the release.
