---
title : "Installing PyChaste"
description: "Installing PyChaste"
draft: false
images: []
layout: "single"
---

There are three ways to get PyChaste running on your system:

* Using the [Conda Package](#conda-package) -- supported on Linux.
* Using the [Docker Image](#docker-image) -- supported on any platform.
* [Building from Source](#build-from-source) -- supported on Linux.

## Conda Package

The conda package installs several dependencies automatically. Please install
[`mamba`](https://mamba.readthedocs.io) first, as dependency resolution can be
quite slow with `conda` itself.

We recommend that you install in a new environment. To do this, run:

```sh
mamba create -n <env-name> -c pychaste -c conda-forge -c bioconda chaste
```

where `<env-name>` is the name of the new environment. To activate the environment, run:

```sh
conda activate <env-name>
```

Alternatively, you can install in an existing conda environment. With the
environment activated, run:

```sh
mamba install -c pychaste -c conda-forge -c bioconda chaste
```

{{< callout context="note" title="Note" icon="info-circle" >}}

Trying to install in an existing environment may fail if it already has
conflicting dependencies installed!

{{< /callout >}}

Optionally, you can install and launch a [Jupyter](https://jupyter.org) notebook
from the environment:

```sh
mamba install -c conda-forge jupyterlab
jupyter lab
```

## Docker Image

The docker image comes with PyChaste and Jupyter pre-installed. If you do not
already have docker installed, please follow the instructions to
[get docker](https://docs.docker.com/get-docker/).

With docker installed, you can pull the image and launch a PyChaste container
with the following command:

```sh
docker run -it --rm -p 8888:8888 chaste/pychaste
```

You can open a Jupyter notebook from the container by launching a web
browser and going to the address `http://localhost::8888`.

## Build from Source

To build PyChaste from source, we first need to install Chaste. See the
[Chaste Install Guides](../../docs/installguides/) for information on installing
Chaste dependencies.

After installing the required dependencies, clone the Chaste repository:

```sh
git clone --recursive https://github.com/Chaste/Chaste.git
```

Clone the PyChaste repository into the Chaste projects directory:

```sh
git clone --recursive https://github.com/Chaste/PyChaste.git /path/to/Chaste/projects/PyChaste
```

{{< callout context="note" title="Note" icon="info-circle" >}}

`--recursive` is important for retrieving git submodules. The build will fail
without it!

{{< /callout >}}

From outside the source tree, create a build folder and generate the CMake
configuration:

```sh
mkdir build && cd build
cmake /path/to/Chaste
```

To build PyChaste, run:

```sh
make -j4 chaste_project_PyChaste
make -j4 chaste_project_PyChaste_Python
```

Finally, `pip install` the built package with these commands:

```sh
cd /path/to/build/projects/PyChaste/python/chaste
pip install .
```
