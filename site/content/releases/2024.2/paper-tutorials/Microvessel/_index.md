---
title: "Microvessel Project"
draft: false
layout: "single"
showPageLinks: true
paperTutorialProject: "https://github.com/Chaste/project_Microvessel"
version: "2024.2"
---


The Microvessel project is a Chaste add-on library with functionality for modelling blood flow, angiogenesis and nutrient transport in microvessels.
It is overviewed in "Microvessel Chaste: An Open Library for Spatial Modeling of Vascularized Tissues", *Biophys J.*, 2017, [doi: 10.1016/j.bpj.2017.03.036](https://doi.org/10.1016/j.bpj.2017.03.036).
Detailed [installation instructions](#installation) are below.

Click on the images below to see some example applications.

[{{< img src="https://raw.githubusercontent.com/Chaste/project_Microvessel/9a87df2f16da8b433914025dab92ce2324394dc6/test/tutorials/images/haematocrit.png" alt="haematocrit" h="200px" >}}](bloodflow)
[{{< img src="https://raw.githubusercontent.com/Chaste/project_Microvessel/9a87df2f16da8b433914025dab92ce2324394dc6/test/tutorials/images/LatticeTutorialSampleGrowth.png" alt="LatticeTutorialSampleGrowth" h="200px" >}}](latticebasedangiogenesis)
[{{< img src="https://raw.githubusercontent.com/Chaste/project_Microvessel/9a87df2f16da8b433914025dab92ce2324394dc6/test/tutorials/images/OffLatticeMidPoint.png" alt="OffLatticeMidPoint" h="200px" >}}](offlatticeangiogenesis)


## Installation

The project can be used directly as a typical C++ Chaste project. First, Chaste dependencies need to be built following the [Chaste Install Guide](https://github.com/Chaste/trac_archive/wiki/Install-Guides-_-Install-Guide).
The project only supports the development version of Chaste. This can be obtained by doing:

*2026 Note:* it may be necessary to check out a revision of Chaste from 2017.

```bash
git clone https://github.com/Chaste/Chaste.git $CHASTE_SOURCE_DIR
```


The project code itself can be obtained by doing:

```bash
git clone https://github.com/Chaste/project_Microvessel.git $MICROVESSEL_PROJECT_SOURCE_DIR
```

The Microvessel project code needs to be included in the main Chaste source. This can be done with a symbolic link:

```bash
cd $CHASTE_SOURCE_DIR/projects
ln -s $MICROVESSEL_PROJECT_SOURCE_DIR
```


The C++ libraries can be built using the [Chaste CMake build system](../../dev-guides/cmake-build-guide/). First, create a build directory outside the source tree and proceed as:

```bash
cd $CHASTE_BUILD_DIR
cmake $CHASTE_SOURCE_DIR
make project_Microvessel -j $NUM_AVAILABLE_CPUS
```


This will build the C++ library and all tests. To avoid building tests do:

```bash
make chaste_project_Microvessel -j $NUM_AVAILABLE_CPUS
```


as the final command. The [Chaste CMake build system guide](../../dev-guides/cmake-build-guide/) should be consulted for options related to generating optimized builds, running
other types of test and installation as a system library.


### C++ Usage

The source and test code are in the `src` and `test` folders respectively.  Unit tests can be built and run using the Chaste CMake framework [as detailed here](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Cmake-Build-Guide). It is recommended that the [tutorials](https://github.com/Chaste/trac_archive/wiki/Paper-Tutorials-_-Microvessel-_-Build-Vessel-Network) are followed. To run the first tutorial do:

```bash
ctest -R TestBuildVesselNetworkLiteratePaper
```


To run all C++ tests and tutorials do:

```bash
ctest -L project_Microvessel
```


### Python Package (Under Development)

A [conda](http://conda.pydata.org/docs/intro.html) Python package for Linux is currently under development. In the meantime this package needs to be built from source as a [PyChaste](/pychaste) module. First, build [PyChaste](/pychaste) following the instructions [here](/pychaste).
Then, follow the above C++ instructions to build the Microvessel project, but with the additional CMake flag `-DBUILD_MICROVESSEL_PYTHON=ON`. The final steps should look like:

```bash
cmake -DBUILD_MICROVESSEL_PYTHON=ON $CHASTE_SOURCE_DIR
make project_Microvessel
make project_Microvessel_Python
```

The Python package `microvessel` will be in `$BUILD_DIR` under `Chaste/projects/Microvessel/python`. The finished package should be copied into the `chaste/projects` module of PyChaste.


### Python Usage

The Python source and tests are in the `src/python` and `test/python` folders. The [Python tutorials](./buildvesselnetwork) should be followed next.

To run the Python tutorial do:

```bash
ctest -R TestPythonBuildVesselNetworkLiteratePaper.py
```


To run all Python tests do:

```bash
ctest -L project_Microvessel
```


A full list of tutorials is given at the bottom of this page.


## Section contents
