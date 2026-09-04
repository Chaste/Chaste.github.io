---
title : "Changes since last release"
date: 2020-10-06T08:47:36+00:00
draft: false
images: []
toc: true
---



**Users:** If you are working with the develop branch and your local code or project has been broken
by a recent interface change then please see here for fix suggestions.

**Developers:** Please mention any changes to the code which will break users' code here - to be put in the release notes for the next release.  Also mention any significant improvements or new features.  The real definitive release notes will be written in [release notes](../release-notes)  at the time of release.  To make that process easier, please structure this page in the same manner.


## Changes since last release appear below

---


## (changes since Release 2026.1)


### Headline features

- [#513](https://github.com/Chaste/Chaste/pull/513) The cell-based force hierarchy has been refactored, replacing `GeneralisedLinearSpringForce` and related classes with dedicated force classes. This is a breaking API change; see Cell Based below for the replacements.
- [#557](https://github.com/Chaste/Chaste/pull/557) Chaste has adopted the [Contributor Covenant](https://www.contributor-covenant.org/) code of conduct.


### Dependency changes

This will be the last Chaste release to support Ubuntu 22.04 LTS (Jammy), and the following dependencies versions will no longer be supported in future releases.

- Boost < 1.83
- HDF5 < 1.10.10
- PETSc < 3.19
- SUNDIALS < 6.4
- VTK < 9.1
- GCC < 13
- Clang < 18
- CMake < 3.28

Newly supported dependency versions:

- [#522](https://github.com/Chaste/Chaste/issues/522) PETSc 3.25 is now supported.
- [#526](https://github.com/Chaste/Chaste/issues/526) XSD 4.2 is now supported.


### Core

- [#548](https://github.com/Chaste/Chaste/issues/548) Chaste now sets explicit permissions on the files and directories it creates rather than inheriting the platform default. This resolves some, but not all, of the sporadic permission-related test failures seen in the Docker container on macOS.
- [#562](https://github.com/Chaste/Chaste/pull/562) gperftools CPU profiling is supported again: the CMake machinery has been restored and runs in CI, and can also be run locally by following the [profiling guide](https://chaste.github.io/docs/dev-guides/profiling/).


### Heart


### Cell Based

- [#513](https://github.com/Chaste/Chaste/pull/513) The cell-based force hierarchy has been refactored. `GeneralisedLinearSpringForce`, `RepulsionForce` and `DifferentialAdhesionGeneralisedLinearSpringForce` are removed in favour of dedicated classes that work across both mesh-based and node-based populations:
  - `LinearSpringForce`: Meineke-style linear springs;
  - `PathmanathanInteractionForce`: logarithmic repulsion / exponential attraction;
  - `SimpleLogarithmicRepulsionForce`: repulsion only;
  - `DifferentialAdhesionLinearSpringForce` / `DifferentialAdhesionPathmanathanInteractionForce`: differential-adhesion variants.
- [#511](https://github.com/Chaste/Chaste/pull/511) Added `RK4NumericalMethod`, a 4th-order Runge-Kutta numerical method for off-lattice cell mechanics, as a drop-in alternative to `ForwardEulerNumericalMethod`. Also adds `NoNumericalMethod`, required for the cell populations that update node positions with their own machinery (`NodeBasedCellPopulationWithBuskeUpdate` and `ImmersedBoundaryCellPopulation`). Fixes a bug in the step-halving adaptive-timestep loop, which may change results for simulations using an adaptive timestep.


### Future Plans
