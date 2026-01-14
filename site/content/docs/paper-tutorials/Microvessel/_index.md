## Microvessel Project

The Microvessel project is a Chaste add-on library with functionality for modelling blood flow, angiogenesis and nutrient transport in microvessels.
It is overviewed in the [pre-print here](/chaste/projects/Microvessel/paper/chaste_microvessel_plos_cb.pdf). Detailed [installation instructions](#Installation) are below.
Quiries via the [Chaste mailing list](mailto:chaste-users@maillist.ox.ac.uk) are welcome.

Click on the images below to see some example applications.

{{< img src="https://raw.githubusercontent.com/Chaste/project_Microvessel/9a87df2f16da8b433914025dab92ce2324394dc6/test/tutorials/images/haematocrit.png" alt="haematocrit" h="200px" >}}
{{< img src="https://raw.githubusercontent.com/Chaste/project_Microvessel/9a87df2f16da8b433914025dab92ce2324394dc6/test/tutorials/images/LatticeTutorialSampleGrowth.png" alt="LatticeTutorialSampleGrowth" h="200px" >}}
{{< img src="https://raw.githubusercontent.com/Chaste/project_Microvessel/9a87df2f16da8b433914025dab92ce2324394dc6/test/tutorials/images/OffLatticeMidPoint.png" alt="OffLatticeMidPoint" h="200px" >}}


## Installation = #Installation
The project can be used directly as a typical C++ Chaste project. First, Chaste dependencies need to be built following the [Chaste Install Guide](https://github.com/Chaste/trac_archive/wiki/Install-Guides-_-Install-Guide).
The project only supports the development version of Chaste. This can be obtained by doing:

```bash
git clone https://chaste.cs.ox.ac.uk/git/chaste.git $CHASTE_SOURCE_DIR
```


The project code itself can be obtained by doing:

```bash
svn co "https://chaste.cs.ox.ac.uk/svn/chaste/projects/Microvessel" $MICROVESSEL_PROJECT_SOURCE_DIR
```


The Microvessel project code needs to be included in the main Chaste source. This can be done with a symbolic link:

```bash
cd $CHASTE_SOURCE_DIR/projects
ln -s $MICROVESSEL_PROJECT_SOURCE_DIR
```


The C++ libraries can be built using the [Chaste CMake build system](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Cmake-Build-Guide). First, create a build directory outside the source tree and proceed as:

```bash
cd $CHASTE_BUILD_DIR
cmake $CHASTE_SOURCE_DIR
make project_Microvessel -j $NUM_AVAILABLE_CPUS
```


This will build the C++ library and all tests. To avoid building tests do:

```bash
make chaste_project_Microvessel -j $NUM_AVAILABLE_CPUS
```


as the final command. The [Chaste CMake build system guide](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Cmake-Build-Guide) should be consulted for options related to generating optimized builds, running
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
A [conda](http://conda.pydata.org/docs/intro.html) Python package for Linux is currently under development. In the meantime this package needs to be built from source as a [PyChaste](https://github.com/Chaste/trac_archive/wiki/Py-Chaste) module. First, build [PyChaste](https://github.com/Chaste/trac_archive/wiki/Py-Chaste) following the instructions [here](https://github.com/Chaste/trac_archive/wiki/Paper-Tutorials-_-Py-Chaste).
Then, follow the above C++ instructions to build the Microvessel project, but with the additional CMake flag `-DBUILD_MICROVESSEL_PYTHON=ON`. The final steps should look like:

```bash
cmake -DBUILD_MICROVESSEL_PYTHON=ON $CHASTE_SOURCE_DIR
make project_Microvessel
make project_Microvessel_Python
```


The Python package `microvessel` will be in `$BUILD_DIR` under `Chaste/projects/Microvessel/python`. The finished package should be copied into the `chaste/projects` module of PyChaste.

### Python Usage
The Python source and tests are in the `src/python` and `test/python` folders. The [Python tutorials](https://github.com/Chaste/trac_archive/wiki/Paper-Tutorials-_-Microvessel-_-Python-Build-Vessel-Network) should be followed next.

To run the Python tutorial do:

```bash
ctest -R TestPythonBuildVesselNetworkLiteratePaper.py
```


To run all Python tests do:

```bash
ctest -L project_Microvessel
```


A full list of tutorials is given at the bottom of this page.


-----
### Section contents
[SubWiki()](SubWiki())

