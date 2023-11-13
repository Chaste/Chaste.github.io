---
title : "Build PyChaste from Source"
description: "PyChaste build guide"
date: 2020-10-06T08:47:36+00:00
lastmod: 2020-10-06T08:47:36+00:00
draft: false
images: []
toc: true
---

## Overview
To build from source, we need the wrappers from the PyChaste repository as well as the upstream C++ code from the Chaste repository. PyChaste is composed as a Chaste user project to make it easier to hook into the existingn CMake configuraton and test system that Chaste already uses.

## Get the source code
First, we need to install Chaste dependencies including `boost` and `petsc`. See the guidance on https://chaste.github.io/docs/installguides for a detailed walk through the process of getting Chaste dependencies set up on your system. The source code for Chaste and PyChaste can be obtained from their respective git repositories:

```
git clone --recursive https://github.com/Chaste/Chaste.git
```

Clone PyChaste into the Chaste projects directory. The `--recursive` option is important as PyChaste includes pybind11 as a submodule. The build will fail without this option.
```
git clone --recursive https://github.com/Chaste/PyChaste.git /path/to/Chaste/projects/PyChaste
```

## Configure, build and install
Create a build folder outside the source tree and generate the CMake configuration:
```
mkdir build && cd build
cmake /path/to/Chaste
```

Run `make` to build PyChaste:
```
make chaste_project_PyChaste
make chaste_project_PyChaste_Python
```

When the above commands have completed, PyChaste python package should now be ready to install. To install:
```
cd /path/to/build/projects/PyChaste/python/chaste
pip install .
```

PyChaste is now installed as a Python module on your system.