---
title: "Supported versions of our dependencies"
description:  "Supported versions of our dependencies"
draft: false
images: []
toc: true
layout: "single"
---

Chaste has a number of dependencies. If you are using the 
[Ubuntu package](../ubuntu-package) then the best versions are selected and 
installed automatically for you.

If you are doing a manual linux installation, then this page shows you the 
supported and preferred versions of each dependency. Note that it reflects the 
status of the current trunk code, rather than previous releases of Chaste; see 
instead the copy of this page associated with a release for that information.

The [main install guide](InstallGuides/InstallGuide) should generally be 
updated to reflect installation instructions for one of the preferred versions.

## Key to tables

|  Symbol | Label       | Description | 
| :------ | :---------- | :---------- | 
| 🟢      | Preferred   | These are preferred versions which we regularly test and have no known problems with. We intend to maintain Chaste compatibility for as long as practical (usually longer than the package developers). Our preferred versions are normally the defaults in an Ubuntu LTS. | 
| 🟩      | Supported   | These are versions that we test against regularly and so should pass all standard tests. They are not our preferred versions because they might have small bugs, or not have as many features, or won't be supported for as long (e.g. because they're not the default in an Ubuntu LTS). | 
| 🟨      | Should Work | These versions are expected to work. We've generally tested them at least once, but these versions are not regularly tested with the development code. | 
| 🟦      | Future      | We do not yet support these versions, but plan to add support for them in the future. This may just mean we have not yet had the chance to test them for compatibility and adapt the code for them if needed. | 
| 🟪      | Sunsetting  | These versions will not be supported in future releases. However, they may work with the current Chaste release, and perhaps/probably/parts-of the development version. | 
| 🟥      | Not Supported | These versions are not compatible/supported, either because they have bugs, or are deprecated because they don't do everything we need now, or are too old to continue tested support for. | 

## Build Systems

The supported build system is now CMake - preferred versions are those that are 
default on Ubuntu LTS releases, but we expect every version of CMake above the 
minimum required to work fine.

Scons was the legacy build system and is no longer supported.

| CMake |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
|🟥 <3.16.3|🟩 3.16.3+|🟨 3.17|🟨 3.18|🟨 3.19|🟨 3.20|🟨 3.21|🟢 3.22|🟨 3.23|🟨 3.24|🟨 3.25|🟨 3.26|🟨 3.27|🟨 3.28|

## Compilers

Preferred compiler versions are the default versions of GCC and Clang on 
Ubuntu LTS releases, and specific versions of the Intel compiler that we 
regularly test Chaste with. We expect all other C++17-capable versions of GCC, 
Clang and Intel to compile Chaste with no problems.

| GCC |
|----|----|----|----|----|----|----|----|----|
|🟥 <5.x|🟪 6.x|🟨 7.x|🟨 8.x|🟩 9.x|🟢 10.x|🟨 11.x|🟢 12.x|🟦 13.x|

| Clang |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
|🟥 <4.x|🟪 4.x|🟪 5.x|🟨 6.x|🟨 7.x|🟨 8.x|🟨 9.x|🟨 10.x|🟨 11.x|🟢 12.x|🟨 13.x|🟢 14.x|🟦 15.x|🟦 16.x|

| Intel |
|----|----|----|
|🟨 2021.x|🟨 2022.x|🟢 2023.x|

## Libraries

In some instances the version number is linked to the GitHub issue in which support was/is being introduced.

| Boost |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
|🟥 <1.62|🟪 1.62|🟪 1.63|🟪 1.64|🟥 1.65|🟪 1.66|🟢 1.67|🟨 1.68|🟩 1.69|🟨 1.70|🟩 1.71|🟨 1.72|🟩 1.73|🟢1.74|🟨 1.75|🟨 1.76|🟨 1.77|🟨 1.78|🟦 1.79|🟦 1.80|🟦 1.81|🟦 1.82|🟦 1.83|

| HDF5 |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
|🟥 1.8.x|🟪 <1.10.4|🟢 1.10.4|🟩 1.10.5|🟩 1.10.6|🟢 1.10.7|🟩 1.10.8|🟦 1.10.9|🟦 1.10.10|🟦 1.10.11|🟨 1.12.0|🟨 1.12.1|🟩 1.12.2|🟦 1.12.3|🟦 1.14.0|🟦 1.14.1|🟦 1.14.2|🟦 1.14.3|

| ParMETIS |
|----|----|
|🟥 3.x|🟢 4.0|

| PETSc |
|----|----|----|----|----|----|----|----|----|----|----|
|🟥 <3.5|🟪 <3.11|🟢 3.12|🟩 3.13|🟩 3.14|🟢 3.15|🟦 3.16|🟦 3.17|🟦 3.18|🟦 3.19|

| SUNDIALS |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
|🟥 2.x|🟪 3.0|🟢 3.1|🟩 3.2|🟨 4.0|🟩 4.1|🟨 5.0|🟨 5.1|🟨 5.2|🟨 5.3|🟨 5.4|🟨 5.5|🟨 5.6|🟨 5.7|🟢 5.8|🟩 6.0|🟦 6.1|🟦 6.2|🟦 6.3|🟦 6.4|🟦 6.5|🟦 6.6|

| VTK |
|----|----|----|----|----|----|----|----|----|----|----|----|----|
|🟥 <6.2|🟪 6.2|🟩 6.3|🟨 7.0|🟢 7.1|🟨 8.0|🟨 8.1|🟩 8.2|🟩 9.0|🟢 9.1|🟩 9.2|🟦 9.3|

| Xerces |
|----|----|----|----|----|----|
|🟥 3.1|🟩 3.2.1|🟢 3.2.2|🟢 3.2.3|🟩 3.2.4|

| XSD |
|----|----|
|🟥 3.x|🟢 4.0|

