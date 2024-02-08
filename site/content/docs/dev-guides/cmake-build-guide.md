---
title: "CMake Build Guide"
description: "CMake Build Guide"
draft: false
images: []
toc: true
layout: "single"
---

This page details all the available options for CMake builds.

## General CMake Concepts

### File Layout

The main CMake file is `CMakeLists.txt`. All the cmake macros and finder scripts (apart from those in the main CMake distribution) are in `/cmake/`. Most of these are kept in `/cmake/Modules`, and there is a base CMake Configure script for Chaste in `/cmake/Config/`. The remainder in `/cmake/` are left over from the old CMake setup for windows (some are still in use).


### Workflow

If you aren't familiar with this, perhaps start with [CMake First Run](../cmake-first-run), and come back here for more detailed instructions...

CMake is a build system generator, so splits up the compilation process into two steps:

 1. [Configure](#configure-step)
 2. [Build](#build-step) (or 'make')

In the first you call `cmake` to [configure](#configure-step) your project. During this step you can specify a generator. By default this is a Makefile generator, so the configure step will output a bunch of Makefiles, with which you can build you project. Other generators include one for Microsoft Visual C++, which outputs MSVC project files during the configure step.

It is standard for CMake to build your project in a separate (empty) directory to your source tree (usually this can still be in a subdirectory within the source tree, but the Chaste CMake system will prevent you from doing in-source builds to avoid making a mess of the git repository).

The standard way (for Makefile generators) to compile the Chaste project using CMake is to make a build directory, call `cmake` on the root of the source tree and then use `make` to compile. For example,


```sh
mkdir /path/to/build/dir
cd /path/to/build/dir
cmake /path/to/source/dir
make
```

This will compile the Chaste libraries and all the tests. To run the tests you can either call `make` on the `test` target

```sh
make test
```

Or use `ctest`, which is part of CMake


```sh
ctest
```

Look under the [Testing Step](#testing-step) heading below for more information

Note: CMake, `cmake`, `ccmake` and `ctest` are general build managers, that have many more options than we have detailed in this document. For much more detailed documentation on these tools, please consult the CMake documentation here: [https://cmake.org/documentation/](https://cmake.org/documentation/)


## Configure Step

Run the [CMake configuration](https://cmake.org/runningcmake/) step using

```sh
cmake /path/to/source
```

This should work on (at least) Ubuntu with all required dependencies installed. Note that the `ccmake` graphical user interface provides a nice way to see what options are available.


### Chaste Configuration Options

These options can be set in the `ccmake` gui, or specified on the command line using `-DOPTION=$option`. eg.

```sh
cmake -DChaste_NUM_CPUS_TEST=2 /path/to/source
```

| Variable | Description |
|---|---|
| `BUILD_SHARED_LIBS` | Standard CMake option (used by Chaste) that indicates whether to build static or shared libraries (defaults to `OFF` for WIN32 and CYGWIN, `ON` for everything else). Only the defaults currently work.
| `CMAKE_BUILD_TYPE` | Choose the type of build, which sets specific compiler flags: `None` `Debug` `Release` `RelWithDebInfo` `MinSizeRel` `AggressiveOpt` `Coverage` `DebugOpt`. Used for single build configuration generators (e.g. Makefiles). Not used for multi build configuration generators (e.g. MSVC). `AggressiveOpt` sets `-Ofast -march=native -DNDEBUG` which is good for production use, and `DebugOpt` sets `-Og -g` which is a good default for an edit-compile-debug workflow. |
| `CMAKE_INSTALL_PREFIX` | Typing `make install` will install Chaste to this base directory |
| `Chaste_COVERAGE` | Build Chaste with coverage information |
| `Chaste_ENABLE_TESTING` | Enable building of tests (defaults to `ON`) |
| `Chaste_ENABLE_<component>_TESTING` | Enable building of tests for <component> (defaults to `ON`) |
| `Chaste_INSTALL_TESTS` | Install source files for tests along with header files and built libraries |
| `Chaste_MEMORY_TESTING` | Setup tests so they are run under valgrind |
| `Chaste_NUM_CPUS_TEST` | Number of cpus to use when running tests (using mpiexec). Defaults to 1 (note that parallel tests are always run with 2 or more cpus) |
| `Chaste_PROFILE_GPERFTOOLS` | Setup compile options and run all tests with Google CPU profiler (gperftools) |
| `Chaste_PROFILE_GPROF` | Setup compile options and run all tests with GNU gprof profiler |
| `Chaste_UPDATE_PROVENANCE` | Updates the build timestamp in the provenance (defaults to `ON`). Note that this will cause re-linking to the `global` library on every build. |
| `Chaste_USE_CVODE` | Compiles Chaste with Sundials support (defaults to `ON`) |
| `Chaste_USE_PETSC_HDF5` | Prefer to compile Chaste with HDF5 library used by PETSc (defaults to `ON`) |
| `Chaste_USE_PETSC_PARMETIS` | Prefer to compile Chaste with Parmetis library used by PETSc (defaults to `ON`) |
| `Chaste_USE_VTK` | Compiles Chaste with VTK support (defaults to `ON`) |
| `Chaste_USE_XERCES` | Compiles Chaste with Xerces and XSD support (defaults to `OFF` for WIN32 or CYGWIN, `ON` for everything else) |
| `Chaste_VERBOSE` | Provide extra info when building Chaste (default `OFF`). Only useful for windows, sets up verbose compilation for MSVC compiler. For Makefile generators (default on linux and mac) use `make VERBOSE=1` |
| `Chaste_VERSION_MAJOR` | Set Chaste major version  |
| `Chaste_VERSION_MINOR` | Set Chaste minor version  |
| `Chaste_CODEGEN_EXTRA_ARGS` | Add any extra arguments for chaste_codegen here (need to set this *before* cellml files are converted to source) |
|||


## Build Step

For Makefile generators (this is the default) the configure step will generate a bunch of Makefiles, so you just need to run

```sh
make -jN
```

for `N` cores.


### Building Specific Targets

#### Components

The configure step generates a number of targets which can be built. These targets can be libraries or executables (i.e. test executables). Each component (i.e. `global`, `pde`, `heart` etc) is compiled into a library, with a target name given by the name of the component (so the target name for `global` is `global`)

You can specify building a specific component library and all its tests by giving `make` the name of the component target. For example:


```sh
make global   # builds the global library and all dependencies
make io       # builds the io library and all dependencies
make linalg   # builds the linalg (linear algebra) library and all dependencies
make mesh     # builds the mesh library and all dependencies
make ode      # builds the ode library and all dependencies
make pde      # builds the pde library and all dependencies
make heart    # builds the heart library and all dependencies
make cell_based crypt  # builds the cell_based and crypt libraries and all their dependencies

make core     # builds all the core Chaste libraries (global, io, linalg, mesh, ode, pde and continuum_mechanics)
```


#### Test packs

If you wish to build a specific test pack then just type `make` and then the name of the test pack, for example:

```sh
make Continuous  # builds the Continuous test pack
make Nightly     # builds the Nightly test pack
make Weekly      # builds the Weekly test pack
make Parallel    # builds the Parallel test pack
```

And then run using, for example

```sh
ctest -L Continuous
```

or

```sh
ctest -L Continuous -j4
```

to run up to 4 tests in parallel (see below).


#### Intersecting components and test packs
If you want to run a test pack for just a specific component, for instance Continuous tests from cell_based, or Nightly tests from heart, you can invoke `ctest` with `<Testpack>_<component>`, for instance

```sh
make cell_based
ctest -L Continuous_cell_based
```

or

```sh
make heart
ctest -L Nightly_heart
```


#### Component library without tests

If you wish to build only the library (without tests) then you can type


```sh
make chaste_${component}
```

where `${component}` is the name of the component you wish to build.


#### Specific tests

You can build a specific test by using the target name for the test executable. The target name for a given test file `TestName.hpp` is given by `$TestName`. So for test file `heart/test/mechanics/TestCardiacElectroMechanicsOnAnnulus.hpp` the command will be


```sh
make TestCardiacElectroMechanicsOnAnnulus
```

This will build an executable `heart/test/TestCardiacElectroMechanicsOnAnnulus`, which you can run directly or use `ctest` to call the test

```sh
ctest -R TestCardiacElectroMechanicsOnAnnulus
```


#### Other Useful Targets

##### Doxygen

Type `make doxygen` to generate Doxygen documentation for the current code tree. The Doxygen documentation will be put in the `doxygen` sub-folder of the build folder


##### Coverage

Set the CMake variable `Chaste_COVERAGE` to `ON` and then re-configure Chaste. Once this is complete type `make coverage`. This will re-build the Continuous and Parallel test packs with coverage information, and then run these tests to collect their coverage. Once this is complete it uses Lcov to generate a html report on the coverage, placing it in the `coverage` sub-folder of the build directory.


##### Doxygen Coverage

Type `make doxygen_coverage` to generate a html report of the current Doxygen coverage. This report is placed in the `doxygen_coverage` subfolder.


##### Memory Testing

Set the CMake variable `Chaste_MEMORY_TESTING` to `ON` and then re-configure Chaste. Once this is complete type `make memtest`. This will run the Continuous test pack under valgrind and then generate a html report in the `memtest` sub-folder.

To run memory testing on a single test suite, set the CMake variable `Chaste_MEMORY_TESTING` to `ON` and then re-configure Chaste, then build and run the test as normal.  This will generate a plain text valgrind `.out` file for any test suites run, in the `memtest` subdirectory of the build directory.

For example, if you wish to run a memory test on the test `TestOdeBasedCellCycleModels`, first set your build folder to compile with memory testing, and compile the test

```sh
cmake -DChaste_MEMORY_TESTING=ON .
make TestOdeBasedCellCycleModels
```

Then run the test. After the test completes the valgrind output will will be in `memtest/TestOdeBasedCellCycleModels.valgrind.out`

```sh
ctest -R TestOdeBasedCellCycleModels
```


##### Profiling

The CMake setup support two methods of profiling, using GNU gprof and gperftools (Google CPU profiler). To enable the former, set the CMake variable `Chaste_PROFILE_GPROF` to `ON`. To enable the latter, set `Chaste_PROFILE_GPERFTOOLS` to `ON`. To run the profiling, type `make profile`. This will run the Profile and ProfileAssembly test packs using the chosen profiling tool and then generate a html report in the `profile` sub-folder.


##### Tutorials

To generate the markdown files from the tutorial source files, type `make tutorials`. This will create `tutorials/UserTutorials` and `tutorials/PaperTutorials`, generate the markdown files from the tutorial source files and put them in these directories.


### Windows

Windows uses the MSVC project file generator, so you can't use `make`. Instead, you can use the CMake interface to run the build

```sh
cmake --build . --config Debug

```

Note that the windows build currently only works for the `Debug` configuration

To build a particular target you can use the `--target` options. eg.

```sh
cmake --build . --config Debug --target heart
```


## Install Step

You can install the Chaste libraries to the CMAKE_INSTALL_PREFIX directory using

```sh
make install
```

Note that this step isn't necessary, you can just use the build folder.


## Packaging your build with CPack

Once you have built Chaste, you can package up your build using the `cpack` executable. Cpack uses a set of generators to package your build:

|DEB|                         = Debian packages|
|---|---|
|NSIS|                        = Null Soft Installer|
|NSIS64|                      = Null Soft Installer (64-bit)|
|RPM|                         = RPM packages|
|STGZ|                       = Self extracting Tar GZip compression|
|TBZ2|                        = Tar BZip2 compression|
|TGZ|                         = Tar GZip compression|
|TZ|                          = Tar Compress compression|
|ZIP|                         = ZIP file format|


To use, type `cpack -G <generator>` to use the specified generator to generate the package. Naturally you must have the correct dependencies installed to use each generator (e.g. Normally only Debian or Ubuntu systems will be able to use the `DEB` generator).


## Testing Step

### Run all tests
You can run all tests using

```sh
ctest
```

or

```sh
ctest -j10
```

to spread the tests over 10 cpus. Note that by default, each test only uses 1 cpu (except those with target names ending in `Parallel`, see below). You can change this behaviour but using the `Chaste_NUM_CPUS_TEST` cmake variable. Set this variable to the number of cpus uses by each test. For example, if you wish to still run 10 tests in parallel using the `-j10` flag, as above, but you now set `Chaste_NUM_CPUS_TEST=2`, then `cmake -j10` will use a total of `10*2=20` cpus.


### Running a test pack

To run the continuous test pack you can use

```sh
ctest -L Continuous
```

The `-L` option takes a regex expression and matches against the labels for each test. Each tests has multiple lables like `Continuous` `Nightly`, `Parallel`, 'heart', 'lung' etc. corresponding to the tests packs and components the test belongs to. So you could run all the global tests using


```sh
ctest -L global
```


### Running a particular test

To run **one particular test** use the `-R` option and add `$` to the end, e.g.

```sh
ctest -R TestCardiacSimulation$
```

(This works because what comes after `-R` is a regular expression and `$` means it only matches if this is the end of the string. You also can use `^` to match the start of the string, but that's always `Test` so not that helpful!)


### Running all tests that match a query

To run all tests that match any regular expression against the CMake target name you can use the `-R` option, this might run a few tests, e.g.:

```sh
ctest -R TestCardiacSimulation
```

will run the tests:

```
  Test #407: TestCardiacSimulation
  Test #408: TestCardiacSimulationArchiver
  Test #451: TestCardiacSimulationNightly
  Test #464: TestCardiacSimulationArchiverParallel
```

Rather than regex magic, you can simply use the `-E` option to exclude a term. e.g.

```sh
ctest -R TestCardiacSimulation -E Nightly
```

will run the tests:

```
  Test #407: TestCardiacSimulation
  Test #408: TestCardiacSimulationArchiver
  Test #464: TestCardiacSimulationArchiverParallel
```


Another useful trick to test your regex is to add the option `-N` which then just lists the tests that the command would run, but doesn't actually run them.


### Running parallel tests

You can add `Parallel` to the end of the target name to run the parallel version of that test (if the test is in the parallel test pack).


### Seeing the output

The `-V` option prints the output of tests to the terminal, so to run a particular test and see the output, you can do e.g.

```sh
ctest -V -R TestVoronoiVertexMeshGenerator
```


## Building Projects Using Chaste

There are two ways to use the Chaste libraries, using the test infrastructure to run your simulations, or using as a standard C++ library.


### Using the Chaste test infrastructure

You can build projects by adding a subdirectory to the `projects/` folder and then adding a `projects/myproject/CMakeLists.txt` file with something like

```cmake
find_package(Chaste COMPONENTS ${components})
chaste_do_project(myproject)
```

where `${components}` is a list of components your project depends on. You can use `core` to indicate all the core Chaste libraries, or leave off the COMPONENTS list entirely (the default is `core`). The build system then assumes you are using the standard Chaste layout for a project and builds your project accordingly

If you have a `test` subdirectory you want built, you again need to add a `projects/myproject/test/CMakeLists.txt` file containing something like

```cmake
chaste_do_test_project(myproject)
```

And if you have an `apps` subdirectory then you need to add a `projects/myproject/apps/CMakeLists.txt` file containing

```cmake
chaste_do_apps_project(myproject)
```

Assuming you are following the standard Chaste layout for your project, then the CMake configure step will find all your library files, tests and applications and setup build targets for them. These will be added to the default build target so they will be built along with all the other Chaste components (or you can build them individually).

You can also build projects outside the Chaste directory tree. This is useful if you are not editing the Chaste source code as part of your project and are just using Chaste as a library. Separating your project from the Chaste build tree results in a significantly faster configuration and build steps. Assuming you have already built Chaste and (optionally) installed it in a given directory, then simply add a `CMakeLists.txt` file in the root folder of your project as explained above, along with corresponding `CMakeLists.txt` files in the `test` and `apps` sub-folders. Note that if you have built (or installed) Chaste in more than one location on your computer, you might want to specify the particular build folder you wish to use. This can be done in the root `CMakeLists.txt` file like so:

```cmake
find_package(Chaste COMPONENTS ${components} PATHS path/to/build_folder NO_DEFAULT_PATH)
chaste_do_project(myproject)
```


### Using Chaste like a standard library

You can also use Chaste like a standard system library (see [Install Step](#install-step)). The CMake configure step will have registered Chaste on your system, so the find_package function should work from any location (if not, you can specify a path, see below). It provides the following variables once you run it

* `Chaste_LIBRARIES`: This variable contains the Chaste libraries you need to link against (for the components you specified in the find_package function)
* `Chaste_INCLUDE_DIRS`: This variable contains the Chaste include folders you need to include
* `Chaste_THIRD_PARTY_INCLUDE_DIRS`: This variable contains the third-party include folders you need to include
* `Chaste_THIRD_PARTY_LIBRARIES`: This variable contains the third-party libraries used to build Chaste (Note that unless you are using `Chaste_LINK_LIBRARIES_WITH_UNRESOLVED_SYMBOLS=ON` you won't need these)

So an example `CMakeLists.txt` script would go

```cmake
find_package(Chaste COMPONENTS ${components})
include_directories(${Chaste_INCLUDE_DIRS} ${Chaste_THIRD_PARTY_INCLUDE_DIRS})
add_executable(my_library \my\source\file.cpp)
target_link_libraries(my_library ${Chaste_LIBRARIES})
```

Note that if you have configured Chaste from more than one build folder, problems occur because you don't know which one CMake will give you. You can give a specific build directory to CMake by using the `NO_DEFAULT_PATH` option for find_package and the `PATHS` option to specify a path. e.g.

```cmake
find_package(Chaste COMPONENTS ${components} PATHS ${path} NO_DEFAULT_PATH)
```
