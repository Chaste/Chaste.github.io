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

## (changes since Release 2024.1)

### Headline features

- [#257](https://github.com/Chaste/Chaste/issues/257) Support Ubuntu 24.04 LTS. Due to issues surrounding libexpat and VTK ([see this issue](https://github.com/Chaste/Chaste/issues/249)) this required us to ship a patched version of VTK 9.3 (9.3.0+dfsg1-1build1) along with the `chaste-dependencies` Debian package.
- [#270](https://github.com/Chaste/Chaste/issues/270) The default location of test output is now the subdirectory `testoutput` of the build directory (the directory that `cmake` is run from). The old default behaviour was `tmp\${USER}\testoutput`. It is still recommended to set the environment variable `CHASTE_TEST_OUTPUT` to override this default behaviour.

### Dependency changes

- [#241](https://github.com/Chaste/Chaste/issues/241) and [#235](https://github.com/Chaste/Chaste/issues/235) Fix boost deprecation warning preventing Chaste using Boost versions 1.73 and 1.74.
- [#263](https://github.com/Chaste/Chaste/issues/263) Replace deprecated `PETSC_NULL` with `PETSC_NULLPTR` to support PETSc 3.19.
- [#293](https://github.com/Chaste/Chaste/issues/293) Selectively ignore internal boost ublas warnings to support boost 1.75-1.85 inclusive.

### Core

- [#322](https://github.com/Chaste/Chaste/issues/322) Support newer compilers: Clang up to 18 and GCC up to 14.

### Cell Based

- [#267](https://github.com/Chaste/Chaste/issues/267) Add tutorial for cell-based simulation command line arguments and parameter sweeping. See the tutorial at this link: https://chaste.github.io/docs/user-tutorials/commandlinearguments/
- [#300](https://github.com/Chaste/Chaste/issues/300) Fixed bug which prevented cell velocities being output on the last timestep of a simulation.
- [#305](https://github.com/Chaste/Chaste/issues/305) Extended functionality for generating bounded Voronoi tessellations.

### Future Plans

- The next release should merge PyChaste support into the main repository.
