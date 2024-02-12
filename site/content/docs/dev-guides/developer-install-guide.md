---
title: "Developer Install Guide"
description: "Developer Install Guide"
draft: false
images: []
toc: true
layout: "single"
---

The easiest ways to install Chaste are:

* On Ubuntu -- using the [Ubuntu package](../../installguides/ubuntu-package).
* On any platform -- using [Docker](../../installguides/docker).
* On any platform -- using a virtual machine (e.g.
  [VirtualBox](https://www.virtualbox.org/)), install the latest
  [Ubuntu LTS](https://ubuntu.com) and use the
  [Ubuntu package](../../installguides/ubuntu-package).
* Other Linux systems -- try following the instructions provided below.

If you encounter any problems, or have an unusual setup, the following material
may be useful. Note that some familiarity with installing software on Linux-like
systems may be required.

## Basic installation

The following instructions detail an installation using the preferred versions
of our dependencies, for a non-root user.

These instructions have been tried successfully on:

<!-- TODO: test on recent Fedora
* Fedora 24 (May 2017)
* Fedora 25 (June 2017)
-->

### Some pre-requisites

The following tools are required or useful.
Most systems will already have these installed, or provide an easy way to set them up:

* `gcc` and `g++`
* `gfortran` --- if you want to build PETSc with HYPRE support (`--download-hypre` option [below](#petsc)).
* `wget`
* `python3`, `python3-venv` and `python3-pip`
* `git` --- for users of development branches.
* `valgrind` --- for memory testing (optional).

Since version 3.1, Chaste requires a 64-bit system. Almost all modern systems
will be 64-bit. In the terminal, type

```sh
uname -m
```

If this returns `i686`, you have a 32-bit system, and you will not be able to
use modern versions of Chaste.

Many systems will also include some of the below Chaste dependencies already.
You can usually have a look for them with `locate`, e.g.

```sh
locate petsc
```

If you find pre-existing versions, then check
[Dependency Versions](../../installguides/dependency-versions) to see if they
are compatible with Chaste. If so, you may be able to skip their installation
below, but make sure that you have the 'includes' and 'libraries' where required
(if you don't know what this means then just follow all the below
instructions!).

{{< callout context="note" title="Note" icon="info-circle" >}}
The newest versions of libraries may not have been tested yet, so don't
simply install latest version! Ideally follow these instructions, but if this
isn't possible (or you have pre-installed versions) then check
[Dependency Versions](../../installguides/dependency-versions) first.
{{< /callout >}}


### Define a folder to install all the dependencies in

First define the folder where you want to install the libraries that Chaste depends on.
It is generally best if this is on a local hard disk for speed.
We will also add the binary directory to the path right away, so we can run `cmake` (which we are about to install) without having to type the full path to this directory.
How to do this depends on your shell, but if you are running bash the easiest way is to add it to your `.bashrc` file, e.g. using

```sh
gedit ~/.bashrc
```


At the end of the file add the following lines:

```sh
export CHASTE_LIBS=/home/scratch/chaste-libs
```


Save, quit and then re-load `.bashrc` (or log out and back in again):

```sh
source ~/.bashrc
```


If it doesn't already exist, create this directory:

```sh
mkdir -p $CHASTE_LIBS
```


The following instructions assume that:

* `wget` is installed.
* You are connected to the internet.

If either of these is not true, then download the https links in your browser
and copy them onto the machine you wish to install on.

### CMake
CMake is the recommended build system for Chaste, and is needed to build several of the dependencies listed below.

On Fedora machines try the following line

```sh
sudo dnf install cmake
```


To install manually, use

```sh
wget https://www.cmake.org/files/v3.22/cmake-3.22.6.tar.gz
tar -zxf cmake-3.22.6.tar.gz
cd cmake-3.22.6
./bootstrap --prefix=$CHASTE_LIBS --parallel=4 && make -j4 && make install
cd ..
rm -rf cmake-3.22.6.tar.gz cmake-3.22.6
```

### Boost
On Fedora machines try the following line

```sh
sudo dnf install boost-system boost-serialization boost-program-options
```

To install manually, use

```sh
wget https://boostorg.jfrog.io/artifactory/main/release/1.74.0/source/boost_1_74_0.tar.gz
tar -zxf boost_1_74_0.tar.gz
cd boost_1_74_0
./bootstrap.sh --prefix=$CHASTE_LIBS --with-libraries=system,serialization,program_options
./b2 install
cd ..
rm -rf boost_1_74_0.tar.gz boost_1_74_0
```

### PETSc
Fedora provides a PETSc package, but unfortunately this does not currently contain all the files required to use PETSc with Chaste.

PETSc can install a lot of Chaste's dependencies for us.

(There is a `--download-boost` option, but this doesn't include the particular libraries we need, so we can't use that.)

These steps can take some time (potentially an hour or more).

```sh
cd $CHASTE_LIBS
wget https://ftp.mcs.anl.gov/pub/petsc/release-snapshots/petsc-lite-3.15.5.tar.gz
tar -zxf petsc-lite-3.15.5.tar.gz
rm -f petsc-lite-3.15.5.tar.gz
cd petsc-3.15.5
```

```sh
# Define package versions
MPICH=https://www.mpich.org/static/downloads/3.4.3/mpich-3.4.3.tar.gz
HDF5=https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10/hdf5-1.10.7/src/hdf5-1.10.7.tar.bz2

export PETSC_DIR=`pwd`
```

If you want to build PETSc with hypre, optionally remove `--with-fc=0` and add
`--download-hypre=1` in the following code blocks. If you are not sure whether
you want to build PETSc with hypre, leave the following as is.

```sh
export PETSC_ARCH=linux-gnu
./configure --with-make-np=4 --with-cc=gcc --with-cxx=g++ --with-fc=0 --with-x=false --with-ssl=false --download-f2cblaslapack=1 --download-mpich=$MPICH --download-hdf5=$HDF5 --download-parmetis=1 --download-metis=1 --download-sundials=1 --with-shared-libraries
make all test
```

```sh
# Optional - optimised petsc build too.
export PETSC_ARCH=linux-gnu-opt
./configure --with-make-np=4 --with-cc=gcc --with-cxx=g++ --with-fc=0 --with-x=false --with-ssl=false --download-f2cblaslapack=1 --download-mpich=$MPICH --download-hdf5=$HDF5 --download-parmetis=1 --download-metis=1 --download-sundials=1 --with-shared-libraries --with-debugging=0
make all test
```

```sh
unset PETSC_ARCH
unset PETSC_DIR
```

### XSD
On Fedora machines try the following line

```sh
sudo dnf install xsd
```

To install manually, use the distributed binaries.

```sh
cd $CHASTE_LIBS
wget https://www.codesynthesis.com/download/xsd/4.0/linux-gnu/x86_64/xsd-4.0.0-x86_64-linux-gnu.tar.bz2
tar -xjf xsd-4.0.0-x86_64-linux-gnu.tar.bz2
ln -s $CHASTE_LIBS/xsd-4.0.0-x86_64-linux-gnu/bin/xsd $CHASTE_LIBS/bin/xsd
rm -f xsd-4.0.0-x86_64-linux-gnu.tar.bz2
```

### Xerces
On Fedora machines try the following line

```sh
sudo dnf install xerces-c xerces-c-devel
```

For machines without a system Xerces package:

```sh
wget https://archive.apache.org/dist/xerces/c/3/sources/xerces-c-3.2.3.tar.gz
tar -zxf xerces-c-3.2.3.tar.gz
cd xerces-c-3.2.3/
export XERCESCROOT=`pwd`
./configure --prefix=$CHASTE_LIBS
make all
make install
cd $CHASTE_LIBS
rm -rf xerces-c-3.2.3 xerces-c-3.2.3.tar.gz
```

### chaste_codegen dependencies 
chaste_codegen requires:

- `python3`
- `python3-venv`
- `python3-pip`
- an internet connection at least during the initial build

The build process will create a Python virtual environment and install
chaste_codegen from [PyPI](https://pypi.org/project/chaste-codegen/)

If required a manual copy can also be installed as follows:

```sh
python3 -m venv <name_of_new_venv_folder>
python3 -m <name_of_new_venv_folder>/bin/python -m pip install --upgrade pip setuptools wheel
python3 -m <name_of_new_venv_folder>/bin/python -m pip install chaste_codegen
```

For more details see [Installing chaste_codegen](../../user-guides/install-codegen).

### VTK

On Fedora machines try the following line

```sh
sudo dnf install vtk-devel
```

To install manually, use

```sh
wget https://www.vtk.org/files/release/9.1/VTK-9.1.0.tar.gz
tar -zxf VTK-9.1.0.tar.gz
rm -f VTK-9.1.0.tar.gz
cd VTK-9.1.0
cmake -DCMAKE_INSTALL_PREFIX=$CHASTE_LIBS . && make -j4 && make install
cd ..
rm -rf VTK-9.1.0
```

You may need to:

* `sudo dnf install mesa-libGL-devel` (or similar) to get OpenGL headers installed before this point, if you get a configure error stating that these headers have not been found
* `sudo dnf install redhat-rpm-config` (or similar) if you get `gcc: error: /usr/lib/rpm/redhat/redhat-hardened-cc1: No such file or directory`
* `sudo dnf install libxt-devel` (or similar) if you get an error about X11

### Setting paths automatically

You probably then want to add various environment variables specifying these dependency locations to your `.bashrc` file, e.g. using

```sh
gedit ~/.bashrc
```

At the end of the file add the lines (leaving out packages you installed via a package manager):

```sh
export PETSC_DIR=$CHASTE_LIBS/petsc-3.6.2
export PETSC_ARCH=linux-gnu

export SUNDIALS_ROOT=$PETSC_DIR/$PETSC_ARCH

export HDF5_ROOT=$PETSC_DIR/$PETSC_ARCH

export XERCES_INCLUDE_DIR=$CHASTE_LIBS/include
export XERCES_LIBRARY_DIR=$CHASTE_LIBS/lib

export XSD_ROOT=$CHASTE_LIBS/xsd-4.0.0-x86_64-linux-gnu
```

Save, quit and then re-load `.bashrc` (or log out and back in again):

```sh
source ~/.bashrc
```

## Configuring Chaste

Once you've installed the dependencies as above, you need to get hold of the
Chaste code. See [Getting Started](../..) for the options to pick here. Once
you've done this, you are ready to build and run the test suite -- see the
[CMake First Run Guide](../../user-guides/cmake-first-run).

{{< callout context="tip" title="See Also" icon="rocket" >}}
* [Code Repository Access](../access-code-repository)
* [CMake First Run Guide](../../user-guides/cmake-first-run)
{{< /callout >}}
