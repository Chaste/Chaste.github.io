---
title : "Installing PyChaste"
description: "Installing PyChaste"
draft: false
images: []
layout: "single"
---

There are a variety of methods to get PyChaste running on your system:

* Using the [Conda Package](#conda-package) -- supported on Linux.
* Using the [Docker Image](#docker-image) -- supported on any platform.
* [Building from Source](#build-from-source) -- supported on Linux.

## Conda Package

The conda package installs several dependencies automatically. Please install
[`mamba`](https://mamba.readthedocs.io) first, as dependency resolution can be
quite slow with `conda` itself.

Installing in a new environment is recommended. To create an environment named `<env-name>`:

```sh
mamba create -n <env-name> -c pychaste -c conda-forge chaste
```

To activate the newly created environment:

```sh
conda activate <env-name>
```

Alternatively, you can install in an existing conda environment. With the environment activated, run:

```sh
mamba install -c pychaste -c conda-forge chaste
```

{{< callout context="caution" title="Caution" icon="outline/alert-triangle" >}}

Installing in an existing environment may fail if there are conflicting dependencies.

{{< /callout >}}

Optionally, you can install and launch a Jupyter notebook from the environment:

```sh
mamba install -c conda-forge jupyterlab
jupyter lab
```

## Docker Image

The Chaste Docker image comes with PyChaste and Jupyter pre-installed. If you do not
already have Docker installed, please follow the instructions in the [Docker documentation](https://docs.docker.com/).

With Docker installed, you can pull the Chaste Docker image and launch a PyChaste container:

```sh
docker run -it --init --rm -p 8888:8888 chaste/pychaste
```

You can open a Jupyter notebook by launching a web browser to `http://localhost:8888`.

## Build from Source

To build PyChaste from source, we first need to install Chaste dependencies.
See the [Chaste Install Guides](../../docs/installguides/) for step-by-step instructions on how to do this.

PyChaste requires additional pre-installed dependencies: `castxml`, `clang`, `matplotlib`, `mpi4py`, `numpy`, `petsc4py`, `xvfb`, `xvfbwrapper`, and Python bindings for `vtk`.

To install these additional dependencies on Ubuntu 24.04, for example:

```sh
sudo apt-get install -y castxml clang python3-matplotlib python3-mpi4py \
  python3-numpy python3-petsc4py-real python3-vtk7 python3-xvfbwrapper xvfb
```

Optionally, activate a virtual environment for installing PyChaste (recommended).
Use `--system-site-packages` for access to Python dependencies installed via `apt` in Ubuntu as above.

```sh
python3 -m venv --system-site-packages venv
source venv/bin/activate
```

Clone the Chaste repository.

```sh
git clone https://github.com/Chaste/Chaste.git
cd Chaste
```

Create a build folder and configure Chaste with the `Chaste_ENABLE_PYCHASTE` flag switched on:

```sh
mkdir build && cd build
cmake -DChaste_ENABLE_PYCHASTE=ON ..
```

Build PyChaste:

```sh
make -j4 pychaste
```

Finally, `pip install` the built package:

```sh
python3 -m pip install pychaste/package
```

{{< callout context="tip" title="See Also" icon="outline/rocket" >}}

[PyChaste Tutorials](../tutorials/)

{{< /callout >}}
