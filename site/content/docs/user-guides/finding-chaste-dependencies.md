# Finding Chaste Dependencies

Running the Chaste configure step

```

cmake /path/to/Chaste

```

should find all Chaste dependencies automatically.
This should certainly be the case on supported Ubuntu versions, and if you have followed the [InstallGuides/InstallGuide](https://github.com/Chaste/trac_archive/wiki/Install-Guides-_-Install-Guide), on all Mac and Linux distributions.

This is a troubleshooting page with information for manually setting hints for dependency locations if they are not be found automatically, or if you wish to specify specific dependency versions when you have multiple versions installed.

## Windows

For windows (on scratch at least) you need to specify a generator (using `-G`) and the location of the third party libraries (using `-DCHASTE_DEPS_ROOT_DIR=`). So on scratch the command is


```

cmake -DCHASTE_DEPS_ROOT_DIR=D:\chaste_windows\build\install\third_party_libs -DChaste_USE_PETSC_HDF5=OFF -DHAVE_PARMETIS=ON -GVisual Studio 10 Win64 \path\to\source

```


Note you need the `-DChaste_USE_PETSC_HDF5=OFF` because I'm using "Petsc for Windows" for Petsc, which doesn't include hdf5 libraries.

You need `-DHAVE_PARMETIS=ON` to skip the step which checks that Parmetis is working, it works for the main Chaste build, so not to worry (for now).


## Specifying a Compiler

You can specify a C++ and C compiler by setting the CXX and CC environment variables. eg.


```

CXX=icpc CC=icc cmake /path/to/source

```


or


```

CXX=clang++ CC=clang cmake /path/to/source

```


## Specifying PETSc

You can specify a PETSc folder and Arch by setting the PETSC_DIR and PETSC_ARCH environment variables. eg.


```

PETSC_DIR=/path/to/petsc PETSC_ARCH=linux-intel cmake /path/to/source

```


OR setting the PETSC_DIR and PETSC_ARCH cmake variables. eg.


```

cmake -DPETSC_DIR=/path/to/petsc -DPETSC_ARCH=linux-intel /path/to/source

```


Once CMake has successfully found and tested the PETSc setup, this find/test setup will not be run on subsequent calls to `cmake` unless either the PETSC_DIR or PETSC_ARCH cmake variables are changed, or the PETSC_CURRENT variable is set to `NO`. e.g.


```

cmake -DPETSC_CURRENT=NO .

```


## Specifying Sundials

You can specify a Sundials folder by setting the SUNDIALS_ROOT environment variables.

## Specifying HDF5

You can specify a HDF5 folder by setting the HDF5_ROOT environment variables.

## Specifying VTK

You can specify a VTK directory by using the VTK_DIR CMake variable (note: NOT an environment variable). eg.


```

cmake -DVTK_DIR=/path/to/vtk /path/to/source

```


## Specifying Boost

You can specify a Boost directory by using the BOOST_ROOT CMake variable (note: NOT an environment variable).

## Notes for CHASTE_DEPS_ROOT_DIR

(Windows only) Note that using this CMake option overwrites any specified library locations

# ~/.bashrc
You can, of course, configure your machine to set these environment variables automatically in every session.
You can, most likely, do this by adding `export VARIABLE=VALUE` to your `~/.bashrc`.

For instance, you may like to use clang and a specific petsc install, so could add the following:

```

export CXX=clang++
export CC=clang

export PETSC_DIR=/path/to/favourite/petsc
export PETSC_ARCH=linux-gnu

```


# Previous instructions
This page supersedes the previous instructions for specifying dependencies, now available here: [SconsArchive/HostconfigSystem](https://github.com/Chaste/trac_archive/wiki/Scons-Archive-_-Hostconfig-System).
