---
title: "Comparing individual-based approaches to modelling the self-organization of multicellular tissues"
draft: false
layout: "single"
showPageLinks: true
paperTutorialProject: "https://github.com/Chaste/CellBasedComparison2017"
version: "2026.1"
---

This section contains pages generated automatically from the source code accompanying the paper "Comparing individual-based approaches to modelling the self-organization of multicellular tissues", *PLOS Comput. Biol.*, 2017, [doi: 10.1371/journal.pcbi.1005387](https://doi.org/10.1371/journal.pcbi.1005387).


## Videos


Adhesion:
> {{< youtube id="4YZp_WmBZTI" width="360" >}}

Proliferation
> {{< youtube id="F04IlE2PyY0" width="360" >}}

Short-range signalling
> {{< youtube id="SX2GFOr0Dus" width="360" >}}

Long-range signalling
> {{< youtube id="Yl2GT2x2ohc" width="360" >}}


## Getting the code and installing dependencies

Before running these examples you will need to [install Chaste's dependencies](../../installguides).
The easiest way to do this is using an Ubuntu machine (or an Ubuntu virtual machine) as discussed on [InstallGuides/UbuntuPackage](../../installguides/ubuntu-package/).
Note that Chaste is only fully supported on Linux/Unix systems, so users of Windows or Mac OS X are encouraged to follow the [Docker instructions](../../installguides/docker/).


To checkout the source code for the specific code revision use the command

```bash
git clone https://github.com/Chaste/Chaste.git Chaste
cd Chaste
```

This project must be built with CMake.
At this point you should configure Chaste with [CMake](/docs/dev-guides/cmake-build-guide/).

You will also need the (updated-since-publication) source for the CellBasedComparison2017 project.  This can be done by checking out the version from the repository by using the command

```bash
cd projects
git clone https://github.com/Chaste/CellBasedComparison2017.git
```

----

Now the project should be installed, and everything should compile and run correctly.
You can now run the tests or simulations, or create your own test suites.


## Documentation

There are two folders - `src` and `test`.

 1. The `src` folder contains classes which add functionality to the core Chaste code.
 2. The `test` folder contains:
     - [TestCellSortingLiteratePaper.hpp](cellsorting) - this file can be run to generate the results in Figures 2 and 3.
     - [TestCylindricalCryptLiteratePaper.hpp](cylindricalcrypt) - this file can be run to generate the results in Figures 4, 5 and 6.
     - [TestDeltaNotchLiteratePaper.hpp](deltanotch) - this file can be run to generate the results in Figures 7 and 8.
     - [TestMorphogenMonolayerLiteratePaper.hpp](morphogenmonolayer) - this file can be run to generate the results in Figures 9, 10 and 11.


**Clicking on the images below will take you to the code to run the corresponding simulation.**

|    | Adhesion                                                                                                                                                                                        | Proliferation                                                                                                                                                                                    | Short-range signalling                                                                                                                                                                 | Long-range signalling                                                                                                                                                                    |
|----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CA | [{{< img src="https://raw.githubusercontent.com/Chaste/project_CellBasedComparison2017/main/figures/Sorting_CA_1_t1000.png" alt="Sorting_CA_1_t1000" h="200px" >}}](cellsorting#ca)             | [{{< img src="https://raw.githubusercontent.com/Chaste/project_CellBasedComparison2017/main/figures/Crypt_CA_08_t100.png" alt="Crypt_CA_08_t100" h="200px" >}}](cylindricalcrypt#ca)             | [{{< img src="https://raw.githubusercontent.com/Chaste/project_CellBasedComparison2017/main/figures/DN_CA_01_t1000.png" alt="DN_CA_01_t1000" h="200px" >}}](deltanotch#ca)             | [{{< img src="https://raw.githubusercontent.com/Chaste/project_CellBasedComparison2017/main/figures/Morph_Ca_t100.png" alt="Morph_Ca_t100" h="200px" >}}](morphogenmonolayer#ca)         |
| CP | [{{< img src="https://raw.githubusercontent.com/Chaste/project_CellBasedComparison2017/main/figures/Sorting_Potts_1_t1000.png" alt="Sorting_Potts_1_t1000" h="200px" >}}](cellsorting#cp)       | [{{< img src="https://raw.githubusercontent.com/Chaste/project_CellBasedComparison2017/main/figures/Crypt_Potts_08_t100.png" alt="Crypt_Potts_08_t100" h="200px" >}}](cylindricalcrypt#cp)       | [{{< img src="https://raw.githubusercontent.com/Chaste/project_CellBasedComparison2017/main/figures/DN_Potts_01_t1000.png" alt="DN_Potts_01_t1000" h="200px" >}}](deltanotch#cp)       | [{{< img src="https://raw.githubusercontent.com/Chaste/project_CellBasedComparison2017/main/figures/Morph_Potts_t100.png" alt="Morph_Potts_t100" h="200px" >}}](morphogenmonolayer#cp)   |
| OS | [{{< img src="https://raw.githubusercontent.com/Chaste/project_CellBasedComparison2017/main/figures/Sorting_Node_1_t1000.png" alt="Sorting_Node_1_t1000" h="200px" >}}](cellsorting#os)         | [{{< img src="https://raw.githubusercontent.com/Chaste/project_CellBasedComparison2017/main/figures/Crypt_Node_08_t100.png" alt="Crypt_Node_08_t100" h="200px" >}}](cylindricalcrypt#os)         | [{{< img src="https://raw.githubusercontent.com/Chaste/project_CellBasedComparison2017/main/figures/DN_Node_01_t1000.png" alt="DN_Node_01_t1000" h="200px" >}}](deltanotch#os)         | [{{< img src="https://raw.githubusercontent.com/Chaste/project_CellBasedComparison2017/main/figures/Morph_Node_t100.png" alt="Morph_Node_t100" h="200px" >}}](morphogenmonolayer#os)     |
| VT | [{{< img src="https://raw.githubusercontent.com/Chaste/project_CellBasedComparison2017/main/figures/Sorting_Mesh_1_t1000.png" alt="Sorting_Mesh_1_t1000" h="200px" >}}](cellsorting#vt)         | [{{< img src="https://raw.githubusercontent.com/Chaste/project_CellBasedComparison2017/main/figures/Crypt_Mesh_08_t100.png" alt="Crypt_Mesh_08_t100" h="200px" >}}](cylindricalcrypt#vt)         | [{{< img src="https://raw.githubusercontent.com/Chaste/project_CellBasedComparison2017/main/figures/DN_Mesh_01_t1000.png" alt="DN_Mesh_01_t1000" h="200px" >}}](deltanotch#vt)         | [{{< img src="https://raw.githubusercontent.com/Chaste/project_CellBasedComparison2017/main/figures/Morph_Mesh_t100.png" alt="Morph_Mesh_t100" h="200px" >}}](morphogenmonolayer#vt)     |
| VM | [{{< img src="https://raw.githubusercontent.com/Chaste/project_CellBasedComparison2017/main/figures/Sorting_Vertex_1_t1000.png" alt="Sorting_Vertex_1_t1000" h="200px" >}}](cellsorting#vm)     | [{{< img src="https://raw.githubusercontent.com/Chaste/project_CellBasedComparison2017/main/figures/Crypt_Vertex_08_t100.png" alt="Crypt_Vertex_08_t100" h="200px" >}}](cylindricalcrypt#vm)     | [{{< img src="https://raw.githubusercontent.com/Chaste/project_CellBasedComparison2017/main/figures/DN_Vertex_01_t1000.png" alt="DN_Vertex_01_t1000" h="200px" >}}](deltanotch#vm)     | [{{< img src="https://raw.githubusercontent.com/Chaste/project_CellBasedComparison2017/main/figures/Morph_Vertex_t100.png" alt="Morph_Vertex_t100" h="200px" >}}](morphogenmonolayer#vm) |


## Running tests

To run the tests, starting from the main Chaste source directory:

```bash
mkdir chaste-build && cd chaste-build
cmake ..

## Make and run a test at a time:
make  TestCellSortingLiteratePaperRunner
ctest -R TestCellSortingLiteratePaper
## etc.

## Make and run all tests on 4 threads:
make -j 4 project_CellBasedComparison2017
ctest -j 4 -L project_CellBasedComparison2017
```

For further information on using Chaste, see the [extensive guide material](../../user-guides/).
You may also wish to look at some of the [user tutorials](../../user-tutorials).


## Section contents
