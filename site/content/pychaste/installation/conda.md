---
title : "Conda Package"
description: "Installing PyChaste using the conda package"
date: 2020-10-06T08:47:36+00:00
lastmod: 2020-10-06T08:47:36+00:00
draft: false
images: []
toc: true
---

## Overview
Installing the PyChaste package from the conda repository is the recommended method for getting PyChaste up and running on your system. As PyChaste has several dependencies that need to be installed along with it, the process of resolving package versions with `conda` can be quite slow. However, `mamba` can speed up the installation significantly. Mamba can be installed from [here](https://mamba.readthedocs.io). 

Although `mamba` is used in the steps below, `conda` can be used instead if `mamba` is not installed. However, the installation process will be much slower.

## Install PyChaste
To create a new `conda` environment and install PyChaste in it:

```
mamba create -n pychaste_env -c pychaste -c conda-forge -c bioconda chaste
conda activate pychaste_env
```

To install PyChaste in the current `conda` environment:
```
mamba install -c pychaste -c conda-forge -c bioconda chaste
```

## Install Jupyter (optional)
If you would like to use Pychaste in a notebook, you can install and launch jupyter from the conda enviroment:
```
mamba install notebook
jupyter notebook
```

