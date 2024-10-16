---
title: "Installing chaste_codegen"
description: "Installing chaste_codegen"
draft: false
images: []
toc: true
layout: "single"
version: "2024.2"
---

This page describes installation of chaste_codegen. For usage information see
[Code Generation from CellML](../code-generation-from-cellml).

chaste_codegen is a Python 3 tool with a number of requirements:

- `python3`
- `python3-venv`
- `python3-pip`

When using the Chaste [Ubuntu package](../../installguides/ubuntu-package), the
prerequisites, should be installed for you automatically.


## Installing chaste_codegen with an internet connection

{{< callout context="note" title="Note" icon="outline/info-circle" >}}

The Chaste build process automatically creates a virtual environment and installs
chaste_codegen from [PyPI](https://pypi.org/project/chaste-codegen/) into
`<chaste_build_directory>/codegen_python3_venv`.

{{< /callout >}}

If required, a manual copy of chaste_codegen can be installed as follows:

```sh
python3 -m venv </path/to/new/venv>
python3 -m </path/to/new/venv>/bin/python -m pip install --upgrade pip setuptools wheel
python3 -m </path/to/new/venv>/bin/python -m pip install chaste_codegen
```

where `</path/to/new/venv>` is the path to the directory the virtual Python 3
environment with chaste_codegen is placed in. This directory must not exist prior
to creating the environment, but you can name it anything you like.

## Installing chaste_codegen without an internet connection

On systems that are isolated from the internet, chaste_codegen cannot be
installed directly from [PyPI](https://pypi.org/project/chaste-codegen/). The
following steps would enable a manual installation and allow building
Chaste.

Create a build directory and change into it e.g.

```sh
mkdir chaste_build
cd chaste_build
```

Create and activate a virtual environment as follows:

```sh
python3 -m venv codegen_python3_venv
source codegen_python3_venv/bin/activate
```

You should now see something like:
```sh
(codegen_python3_venv) me@machine:~/chaste_develop$
```

 To see what packages are currently installed, run
 
```sh
python3 -m pip list
``` 
 
`pip`, `setuptools` and `wheel` are likely to already be installed and you may
not need to reinstall them.

Manually download appropriate versions of the following packages from
[PyPI](https://pypi.org) and transfer them to the isolated system.

```toml
- pip > 20.2
- wheel > 0.35
- setuptools > 50.3
- pip > 20.2
- decorator >=4.4.2, <5
- importlib-metadata >=1.7, <2
- isodate >=0.6.0, <1
- lxml >=4.5.2, <5
- MarkupSafe >=1.1.1, <2
- mpmath >=1.1.0, <2
- networkx >=2.4, <3
- packaging >=20.4, <21
- Pint >=0.9, <1
- pyparsing >=2.4.7, <3
- rdflib >=5.0.0, <6
- six >=1.15.0, <2
- sympy >=1.6.1, <2
- zipp >=1.2.0, <2
- cellmlmanip >=0.2.0, <0.3
- Jinja2 >=2.11.2, <3
- chaste_codegen>=0.5.0, <0.6.0
```

Install the packages manually in the order above, with the virtual environment
activated:
- Uncompress the archive if needed.
- Change into the directory containing `setup.py`
- If there are any installation instructions contained in the documentation,
  follow them. Otherwise, use `python3 setup.py install`

{{< callout context="tip" title="See Also" icon="outline/rocket" >}}

[Code Generation from CellML](../code-generation-from-cellml)

{{< /callout >}}


