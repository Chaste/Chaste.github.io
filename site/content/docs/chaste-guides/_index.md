---
title: "Chaste Guides"
description: "Guides for using chaste"
date: 2020-08-27T19:23:18+02:00
lastmod: 2020-08-27T19:23:18+02:00
draft: false
images: []
toc: true
layout: "single"
---

Before reading this have a look at [Getting Started](/docs) to decide whether you are a *user* of releases or a *developer* contributing back to Chaste core code.

*Users* can download the latest stable release of the source code from our [GitHub releases page](https://github.com/Chaste/Chaste/releases), or check out a [tested development branch](https://github.com/Chaste/Chaste/branches) to get the latest features.

New *developers* should, rather than downloading the release, follow the installation instructions below, including the part on checking-out the latest version of the code.

## 1. User Guides

### Installation

* [Install guides](/docs/installguides) -- How to install Chaste and its dependencies.
* [CMake first run](cmake-first-run) -- How to configure, build, and run tests to check the installation.


### Running Chaste Simulations

* [Release notes](/docs/release-notes/release-notes) and [latest news](/docs/release-notes/changes-since-last-release) on changes since the last release
* [Tutorials](/docs/user-tutorials)
* [Visualisation guides](visualisation-guides)
* [How-to index](/docs/how-tos) -- links to test code illustrating how various things can be done
* [CMake first run guide](cmake-first-run). For all available options, including compiling optimised code, see the full [Cmake build guide](cmake-build-guide).
* [Public API documentation for the latest revision](/docs/doxygen) and [API documentation for release versions](//chaste/tutorials/)


### Writing your own code that uses Chaste

* [User Projects](user-projects) -- for creating (or cloning an existing) personal user project which can use the core code and build/testing framework.


### Miscellaneous information

* File format information is given in the file `docs/FileFormats.html`, supplied with the release (the latest version of this file may also be viewed [here](https://raw.githubusercontent.com/Chaste/Chaste/develop/docs/FileFormats.html)).
* [Units of parameters used in Chaste](chaste-units)
* [Default parameter values](https://github.com/Chaste/Chaste/blob/develop/heart/src/problem/HeartConfigDefaults.hpp) -- read off from this file, ignore the `Simulation` block, which only applies to the old cardiac executable.


## 2. Further information for developers
New developers (including users based in Compbio/CMB) should read the 'users of the source code' section above, and also see

* [External developer guide](external-developer-guide) -- Helpful resources for external users of development versions of Chaste including how to use the git Chaste repository, in particular see [the issue workflow section](external-developer-guide#issue-workflow).
* [Cmake build guide](cmake-build-guide) -- for a detailed guide of all the cmake options.
* [Building executable apps](building-executable-apps) -- making standalone executables that don't use the CxxTest framework.
* [Chaste strategies](/docs/strategies) -- see in particular the coding standards guide


## 3. Advanced

* [Repository access](access-code-repository) for non-core developers (see also [external developer guide](external-developer-guide))
* [Cardiac mechanics solvers](cardiac-mechanics-solvers) -- a bit of information on how the cardiac mechanics solvers are connected to the main mechanics solvers.


-----

## Automatically generated alphabetical listing of guide pages

[SubWiki(ChasteGuides/)](SubWiki(ChasteGuides/))
