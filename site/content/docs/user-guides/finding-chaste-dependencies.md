---
title: "Finding Chaste Dependencies"
description: "Finding Chaste Dependencies"
draft: false
images: []
toc: true
layout: "single"
---

Running the Chaste configure step

```sh
cmake /path/to/Chaste
```

should find all Chaste dependencies automatically. This should certainly be the
case on supported Ubuntu versions, and if you have followed the
[Install Guides](../../installguides/).

This is a troubleshooting page with information for manually setting hints for
dependency locations if they are not found automatically, or if you wish to
use specific dependency versions when you have multiple versions installed.

## Windows

For Windows you need to specify a generator (using `-G`) and the location of the
third party libraries (using `-DCHASTE_DEPS_ROOT_DIR=`) e.g.

```powershell
cmake ^
  -DCHASTE_DEPS_ROOT_DIR=D:\chaste_windows\build\install\third_party_libs ^
  -DChaste_USE_PETSC_HDF5=OFF ^
  -DHAVE_PARMETIS=ON ^
  -GVisual Studio 10 Win64 \path\to\source
```

You need `-DChaste_USE_PETSC_HDF5=OFF` because this example uses
"PETSc for Windows" for PETSc, which doesn't include HDF5 libraries.

You need `-DHAVE_PARMETIS=ON` to skip the step which checks that Parmetis is
working -- it works for the main Chaste build, so not to worry (for now).

## Specifying a Compiler

You can specify a C++ and C compiler by setting the `CXX` and `CC` environment
variables. eg.

```sh
CXX=icpc CC=icc cmake /path/to/source
```

or

```sh
CXX=clang++ CC=clang cmake /path/to/source
```

## Specifying PETSc

You can specify a PETSc folder and Arch by setting the `PETSC_DIR` and `PETSC_ARCH`
environment variables. eg.

```sh
PETSC_DIR=/path/to/petsc PETSC_ARCH=linux-intel cmake /path/to/source
```

OR setting the `PETSC_DIR` and `PETSC_ARCH` CMake variables. eg.

```sh
cmake -DPETSC_DIR=/path/to/petsc -DPETSC_ARCH=linux-intel /path/to/source
```

Once CMake has successfully found and tested the PETSc setup, this find/test
setup will not be run on subsequent calls to `cmake` unless either the `PETSC_DIR`
or `PETSC_ARCH` CMake variables are changed, or the `PETSC_CURRENT` variable is set
to `NO`. e.g.

```sh
cmake -DPETSC_CURRENT=NO .
```

## Specifying SUNDIALS

You can specify a SUNDIALS folder by setting the `SUNDIALS_ROOT` environment
variables.

## Specifying HDF5

You can specify a HDF5 folder by setting the `HDF5_ROOT` environment variables.

## Specifying VTK

You can specify a VTK directory by using the `VTK_DIR` CMake variable (note: NOT
an environment variable). eg.

```sh
cmake -DVTK_DIR=/path/to/vtk /path/to/source
```

## Specifying Boost

You can specify a Boost directory by using the `BOOST_ROOT` CMake variable (note:
NOT an environment variable).

## Notes for CHASTE_DEPS_ROOT_DIR

(Windows only) Note that using this CMake option overwrites any specified
library locations

## Shell configuration

You can, of course, configure your machine to set these environment variables
automatically in every session. In bash, for example, you can do this by adding
`export VARIABLE=VALUE` to your `~/.bashrc`.

For instance, you may like to use clang and a specific PETSc install, so could
add the following:

```sh
export CXX=clang++
export CC=clang

export PETSC_DIR=/path/to/favourite/petsc
export PETSC_ARCH=linux-gnu
```
