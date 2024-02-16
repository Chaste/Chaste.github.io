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

The manual instructions below detail an installation using preferred versions of
our dependencies, for a non-root user.

These instructions have been tried successfully on:
* Fedora 39 (Nov 2023)

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

### Setup

{{< tabs "setup" >}}
{{< tab "Manual" >}}

First define the directory where you want to manually install the libraries that
Chaste depends on. It is generally best if this is on a local hard disk for
speed. We will also add the binary directory to the path right away, so we can
run `cmake` (which we are about to install) without having to type the full path
to this directory. How to do this depends on your shell, but if you are running
bash the easiest way is to add it to your `.bashrc` file, e.g. using

```sh
gedit ~/.bashrc
```

At the end of the file add the following lines:

```sh
export CHASTE_LIBS=$HOME/apps/chaste-libs
export PATH=$CHASTE_LIBS/bin:$PATH
```

Save, quit and then re-load `.bashrc` (or log out and back in again):

```sh
source ~/.bashrc
```

If it doesn't already exist, create the directory:

```sh
mkdir -p $CHASTE_LIBS
```

The following instructions assume that:

* `wget` is installed.
* You are connected to the internet.

If either of these is not true, then download the https links in your browser
and copy them onto the machine you wish to install on.

{{< /tab >}}
{{< tab "Modules" >}}

This uses scripts from the
[dependency-modules](https://github.com/Chaste/dependency-modules) repository to
install Chaste dependencies as environment modules, which makes it possible to
install multiple versions of the dependencies side-by-side and enables switching
between them. If you do not already have an environment modules system
installed, you can install one e.g.

```sh
sudo apt-get install environment-modules # Ubuntu
sudo dnf install environment-modules # Fedora
```

Log out and back in again to activate the environment modules in the shell;
alternatively, run

```sh
source  /etc/profile.d/modules.sh
```

To check that environment modules have been activated, run 

```sh
module avail
```

If all has gone well, you should see output similar to the following:

```
----------------------- /usr/share/modules/modulefiles -----------------------
dot  module-git  module-info  modules  null  use.own  

Key:
modulepath
```

Define the directory where you want to install the libraries that
Chaste depends on, and create a `modulefiles` directory in it e.g.

```sh
export CHASTE_LIBS=$HOME/apps/chaste-libs
mkdir -p $CHASTE_LIBS/modulefiles
```

Register the `modulefiles` directory with the environment modules system.

```sh
module use $CHASTE_LIBS/modulefiles
```

It is recommended that you add the above line to your `.bashrc` (or similar) so
the `modulefiles` directory is registered every time you log in e.g.

```sh
echo "module use $CHASTE_LIBS/modulefiles" >> ~/.bashrc
```

The following instructions assume that:

* `git` is installed.
* `wget` is installed.
* You are connected to the internet.

If any of these is not true, then download the links in your browser
and copy them onto the machine you wish to install on.


Clone the [dependency-modules](https://github.com/Chaste/dependency-modules)
repository.

```sh
git clone https://github.com/Chaste/dependency-modules.git
cd dependency-modules/scripts
```

{{< /tab >}}
{{< tab "Fedora" >}}

See the manual setup instructions.

{{< /tab >}}
{{< tab "Ubuntu" >}}

```sh
sudo apt-get update
```

{{< /tab >}}
{{< /tabs >}}

### CMake
CMake is the recommended build system for Chaste, and is needed to build several
of the dependencies listed below.

{{< tabs "install-cmake" >}}
{{< tab "Manual" >}}

```sh
wget https://www.cmake.org/files/v3.22/cmake-3.22.6.tar.gz
tar -zxf cmake-3.22.6.tar.gz
cd cmake-3.22.6
./bootstrap --prefix=$CHASTE_LIBS --parallel=4 && make -j4 && make install
cd ..
rm -rf cmake-3.22.6.tar.gz cmake-3.22.6
```

{{< /tab >}}
{{< tab "Modules" >}}

From the `dependency-modules/scripts` directory, run

```sh
./install_cmake.sh  --version=3.22.6  --modules-dir=$CHASTE_LIBS --parallel=4
```

{{< /tab >}}
{{< tab "Fedora" >}}

```sh
sudo dnf install cmake
```

{{< /tab >}}
{{< tab "Ubuntu" >}}

```sh
sudo apt-get install cmake cmake-curses-gui
```

{{< /tab >}}
{{< /tabs >}}

### Boost

{{< tabs "install-boost" >}}
{{< tab "Manual" >}}

```sh
wget https://boostorg.jfrog.io/artifactory/main/release/1.74.0/source/boost_1_74_0.tar.gz
tar -zxf boost_1_74_0.tar.gz
cd boost_1_74_0
./bootstrap.sh --prefix=$CHASTE_LIBS --with-libraries=system,serialization,program_options
./b2 install
cd ..
rm -rf boost_1_74_0.tar.gz boost_1_74_0
```

{{< /tab >}}
{{< tab "Modules" >}}

From the `dependency-modules/scripts` directory, run

```sh
./install_boost.sh --version=1.74.0 --modules-dir=$CHASTE_LIBS --parallel=4
```

{{< /tab >}}
{{< tab "Fedora" >}}

```sh
sudo dnf install boost-system boost-serialization boost-program-options
```

{{< /tab >}}
{{< tab "Ubuntu" >}}

```sh
sudo apt-get install libboost-system-dev libboost-serialization-dev libboost-program-options-dev
```

{{< /tab >}}
{{< /tabs >}}

### PETSc

{{< tabs "install-petsc" >}}
{{< tab "Manual" >}}

PETSc can install a lot of Chaste's dependencies for us.

(There is a `--download-boost` option, but this doesn't include the particular
libraries we need, so we can't use that.)

These steps can take some time (potentially an hour or more).

```sh
cd $CHASTE_LIBS
wget https://ftp.mcs.anl.gov/pub/petsc/release-snapshots/petsc-lite-3.18.6.tar.gz
tar -zxf petsc-lite-3.18.6.tar.gz
rm -f petsc-lite-3.18.6.tar.gz
cd petsc-3.18.6
export PETSC_DIR=`pwd`
```

Define package versions for MPICH and HDF5

```sh
mpich=https://www.mpich.org/static/downloads/4.1.2/mpich-4.1.2.tar.gz
hdf5=https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10/hdf5-1.10.11/src/hdf5-1.10.11.tar.bz2
```

If you want to build PETSc with hypre, optionally remove `--with-fc=0` and add
`--download-hypre=1` in the following code blocks. If you are not sure whether
you want to build PETSc with hypre, leave the following as is.

```sh
export PETSC_ARCH=linux-gnu
./configure \
  --with-make-np=4 \
  --with-cc=gcc \
  --with-cxx=g++ \
  --with-fc=0 \
  --with-x=false \
  --with-ssl=false \
  --download-f2cblaslapack=1 \
  --download-mpich=$mpich \
  --download-hdf5=$hdf5 \
  --download-parmetis=1 \
  --download-metis=1 \
  --with-shared-libraries
make all
make test # optional
```

Optional -- install optimised PETSc build too.

```sh
export PETSC_ARCH=linux-gnu-opt
./configure \
  --with-make-np=4 \
  --with-cc=gcc \
  --with-cxx=g++ \
  --with-fc=0 \
  --with-x=false \
  --with-ssl=false \
  --download-f2cblaslapack=1 \
  --download-mpich=$mpich \
  --download-hdf5=$hdf5 \
  --download-parmetis=1 \
  --download-metis=1 \
  --with-shared-libraries \
  --with-debugging=0
make all
make test # optional
```

```sh
unset PETSC_ARCH
unset PETSC_DIR
```

{{< /tab >}}
{{< tab "Modules" >}}

From the `dependency-modules/scripts` directory, run

```sh
./install_petsc_hdf5.sh \
    --petsc-version=3.18.6 \
    --hdf5-version=1.10.11 \
    --petsc-arch=linux-gnu \
    --modules-dir=$CHASTE_LIBS \
    --parallel=4
```

Optional -- install optimised PETSc build too.

```sh
./install_petsc_hdf5.sh \
    --petsc-version=3.18.6 \
    --hdf5-version=1.10.11 \
    --petsc-arch=linux-gnu-opt \
    --modules-dir=$CHASTE_LIBS \
    --parallel=4
```

{{< /tab >}}
{{< tab "Fedora" >}}

See the manual instructions for [PETSc](#petsc).

Fedora provides a PETSc package, but unfortunately this does not currently
contain all the files required to use PETSc with Chaste.

{{< /tab >}}
{{< tab "Ubuntu" >}}

Search for PETSc in the Ubuntu repository:

```sh
apt-cache search libpetsc-real
```

Install e.g PETSc 3.15

```sh
sudo apt-get install libpetsc-real3.15 libpetsc-real3.15-dev libpetsc-real3.15-dbg
```

{{< /tab >}}
{{< /tabs >}}

### HDF5

{{< tabs "install-hdf5" >}}
{{< tab "Manual" >}}

See the manual instructions for [PETSc](#petsc).

{{< /tab >}}
{{< tab "Modules" >}}

See the module install instructions for [PETSc](#petsc).

{{< /tab >}}
{{< tab "Fedora" >}}

See the manual instructions for [PETSc](#petsc).

{{< /tab >}}
{{< tab "Ubuntu" >}}

```sh
sudo apt-get install hdf5-tools libhdf5-openmpi-dev
```

{{< /tab >}}
{{< /tabs >}}

### ParMETIS

{{< tabs "install-parmetis" >}}
{{< tab "Manual" >}}

See the manual instructions for [PETSc](#petsc).

{{< /tab >}}
{{< tab "Modules" >}}

See the module install instructions for [PETSc](#petsc).

{{< /tab >}}
{{< tab "Fedora" >}}

See the manual instructions for [PETSc](#petsc).

{{< /tab >}}
{{< tab "Ubuntu" >}}

```sh
sudo apt-get install libmetis-dev libparmetis-dev
```

{{< /tab >}}
{{< /tabs >}}

### SUNDIALS

{{< tabs "install-parmetis" >}}
{{< tab "Manual" >}}

```sh
wget https://github.com/LLNL/sundials/releases/download/v5.8.0/sundials-5.8.0.tar.gz
tar -zxf sundials-5.8.0.tar.gz
mkdir build-sundials-5.8.0 && cd build-sundials-5.8.0
cmake \
  -DCMAKE_INSTALL_PREFIX=$CHASTE_LIBS \
  -DBUILD_SHARED_LIBS=ON \
  -DCMAKE_BUILD_TYPE=Release \
  -DEXAMPLES_ENABLE=OFF ../sundials-5.8.0
make -j4 && make install
cd ..
rm -rf build-sundials-5.8.0 sundials-5.8.0 sundials-5.8.0.tar.gz
```

{{< /tab >}}
{{< tab "Modules" >}}

Load the CMake module

```sh
module load cmake/3.22.6
```

From the `dependency-modules/scripts` directory, run

```sh
./install_sundials.sh --version=5.8.0 --modules-dir=$CHASTE_LIBS --parallel=4
```

{{< /tab >}}
{{< tab "Fedora" >}}

```sh
sudo dnf install sundials-devel
```

{{< /tab >}}
{{< tab "Ubuntu" >}}

```sh
sudo apt-get install libsundials-dev
```

{{< /tab >}}
{{< /tabs >}}

### XSD

{{< tabs "install-xsd" >}}
{{< tab "Manual" >}}

```sh
cd $CHASTE_LIBS
wget https://www.codesynthesis.com/download/xsd/4.0/linux-gnu/x86_64/xsd-4.0.0-x86_64-linux-gnu.tar.bz2
tar -xjf xsd-4.0.0-x86_64-linux-gnu.tar.bz2
ln -s $CHASTE_LIBS/xsd-4.0.0-x86_64-linux-gnu/bin/xsd $CHASTE_LIBS/bin/xsd
rm -f xsd-4.0.0-x86_64-linux-gnu.tar.bz2
```

{{< /tab >}}
{{< tab "Modules" >}}

From the `dependency-modules/scripts` directory, run

```sh
./install_xsd.sh --version=4.0.0 --modules-dir=$CHASTE_LIBS
```

{{< /tab >}}
{{< tab "Fedora" >}}

```sh
sudo dnf install xsd
```

{{< /tab >}}
{{< tab "Ubuntu" >}}

```sh
sudo apt-get install xsdcxx
```

{{< /tab >}}
{{< /tabs >}}

### Xerces

{{< tabs "install-xerces" >}}
{{< tab "Manual" >}}

```sh
wget https://archive.apache.org/dist/xerces/c/3/sources/xerces-c-3.2.3.tar.gz
tar -zxf xerces-c-3.2.3.tar.gz
cd xerces-c-3.2.3/
export XERCESCROOT=`pwd`
./configure --prefix=$CHASTE_LIBS
make -j4 all
make install
cd ..
rm -rf xerces-c-3.2.3 xerces-c-3.2.3.tar.gz
```

{{< /tab >}}
{{< tab "Modules" >}}

From the `dependency-modules/scripts` directory, run

```sh
./install_xercesc.sh  --version=3.2.3  --modules-dir=$CHASTE_LIBS --parallel=4
```

{{< /tab >}}
{{< tab "Fedora" >}}

```sh
sudo dnf install xerces-c xerces-c-devel
```

{{< /tab >}}
{{< tab "Ubuntu" >}}

```sh
sudo apt-get install libxerces-c-dev
```

{{< /tab >}}
{{< /tabs >}}

### VTK

{{< tabs "install-vtk" >}}
{{< tab "Manual" >}}

```sh
wget https://www.vtk.org/files/release/9.1/VTK-9.1.0.tar.gz
tar -zxf VTK-9.1.0.tar.gz
mkdir build_VTK-9.1.0 && cd build_VTK-9.1.0
cmake -DCMAKE_INSTALL_PREFIX=$CHASTE_LIBS ../VTK-9.1.0 && make -j4 && make install
cd ..
rm -rf build_VTK-9.1.0 VTK-9.1.0 VTK-9.1.0.tar.gz
```

**Troubleshooting**

* Install OpenGL e.g. `sudo dnf install mesa-libGL-devel` on Fedora (or
  similar) to get OpenGL headers installed before this point, if you get a
  configure error stating that these headers have not been found
* Install RPM Config e.g. `sudo dnf install redhat-rpm-config` (or similar) if you
  get
  `gcc: error: /usr/lib/rpm/redhat/redhat-hardened-cc1: No such file or directory`
* Install X11 e.g. `sudo dnf install libxt-devel` (or similar) if you get an
  error about X11

{{< /tab >}}
{{< tab "Modules" >}}

Load the CMake module

```sh
module load cmake/3.22.6
```

From the `dependency-modules/scripts` directory, run

```sh
./install_vtk.sh --version=9.1.0 --modules-dir=$CHASTE_LIBS --parallel=4
```

{{< /tab >}}
{{< tab "Fedora" >}}

```sh
sudo dnf install vtk-devel
```

{{< /tab >}}
{{< tab "Ubuntu" >}}

Search for VTK in the Ubuntu repository:

```sh
apt-cache search libvtk
```

Install e.g VTK 9.1

```sh
sudo apt-get install libvtk9.1 libvtk9-dev
```

{{< /tab >}}
{{< /tabs >}}

### chaste_codegen 

{{< tabs "install-codegen" >}}
{{< tab "Manual" >}}

chaste_codegen requires:

- `python3`
- `python3-venv`
- `python3-pip`
- an internet connection at least during the initial build

The build process will create a Python virtual environment and install
chaste_codegen from [PyPI](https://pypi.org/project/chaste-codegen/)

If required, a manual copy can also be installed as follows:

```sh
python3 -m venv <name_of_new_venv_folder>
python3 -m <name_of_new_venv_folder>/bin/python -m pip install --upgrade pip setuptools wheel
python3 -m <name_of_new_venv_folder>/bin/python -m pip install chaste_codegen
```

For more details see [Installing chaste_codegen](../../user-guides/install-codegen).

{{< /tab >}}
{{< tab "Modules" >}}

See the manual instructions for chaste_codegen.

{{< /tab >}}
{{< tab "Fedora" >}}

See the manual instructions for chaste_codegen.

{{< /tab >}}
{{< tab "Ubuntu" >}}

See the manual instructions for chaste_codegen.

{{< /tab >}}
{{< /tabs >}}

### Post-installation

{{< tabs "post-installation" >}}
{{< tab "Manual" >}}

For manually installed dependencies, you probably then want to add various
environment variables specifying the installed dependency locations to your
`.bashrc` file, e.g. using

```sh
gedit ~/.bashrc
```

At the end of the file add the lines (leaving out packages you installed via a package manager):

```sh
export PETSC_DIR=$CHASTE_LIBS/petsc-3.18.6
export PETSC_ARCH=linux-gnu

export SUNDIALS_ROOT=$CHASTE_LIBS

export HDF5_ROOT=$PETSC_DIR/$PETSC_ARCH

export XERCES_INCLUDE_DIR=$CHASTE_LIBS/include
export XERCES_LIBRARY_DIR=$CHASTE_LIBS/lib

export XSD_ROOT=$CHASTE_LIBS/xsd-4.0.0-x86_64-linux-gnu
```

Save, quit and then re-load `.bashrc` (or log out and back in again):

```sh
source ~/.bashrc
```

{{< /tab >}}
{{< tab "Modules" >}}

To view installed modules, run

```sh
module avail
```

The output should be similar to:

```
--------------------- /home/runner/chaste-libs/modulefiles ---------------------
cmake/3.22.6      boost/1.74.0    petsc_hdf5/3.18.6_1.10.11/linux-gnu
sundials/5.8.0    vtk/9.1.0       xercesc/3.2.3
xsd/4.0.0  

------------------------ /usr/share/modules/modulefiles ------------------------
dot  module-git  module-info  modules  null  use.own  

Key:
modulepath 
```

The installed modules need to be loaded into the environment before configuring
Chaste. To do this, run

```sh
module load cmake/3.22.6
module load boost/1.74.0
module load petsc_hdf5/3.18.6_1.10.11/linux-gnu
module load sundials/5.8.0
module load vtk/9.1.0
module load xercesc/3.2.3
module load xsd/4.0.0
```

{{< /tab >}}
{{< tab "Fedora" >}}

See the manual post-installation instructions.

{{< /tab >}}
{{< tab "Ubuntu" >}}

You are ready to go. The dependencies will be located automatically.

{{< /tab >}}
{{< /tabs >}}

## Configuring Chaste

Once you've installed the dependencies as above, you need to get hold of the
Chaste code. See [Getting Started](../..) for the options to pick here. Once
you've done this, you are ready to build and run the test suite -- see the
[CMake First Run Guide](../../user-guides/cmake-first-run).

{{< callout context="tip" title="See Also" icon="rocket" >}}
* [Code Repository Access](../access-code-repository)
* [CMake First Run Guide](../../user-guides/cmake-first-run)
{{< /callout >}}
