# Installing chaste_codegen to generate Chaste code from CellML


**Note: this page describes installation of chaste_codegen for Python3.** See [InstallPyCml](https://github.com/Chaste/trac_archive/wiki/Install-Py-Cml) for the Python2 code generator used up to release 2019.1.

For usage information see [ChasteGuides/CodeGenerationFromCellML](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Code-Generation-From-Cell-ML).

chaste_codegen itself is a Python3 tool. It has a number of requirements:

- `python3`
- `python3-venv`
- `python3-pip`


When using the `chaste-source` Ubuntu package, the prerequisites, should be installed for you automatically.

**The build process will create a virtual environment and install chaste_codegen from [pypi](https://pypi.org/project/chaste-codegen/) into `<build_folder>/codegen_python3_venv`**

# Installing a manual copy of chaste_codegen (with internet connection)

If required a manual copy can also be installed as follows.

**Please note:** `<name_of_new_venv_folder>` is the name of the folder the virtual python3 environment with chaste_codegen is placed in. This folder must not exist prior to creating the environment, but you can name it anything you like.


```

#!sh
python3 -m venv `<name_of_new_venv_folder>`
python3 -m `<name_of_new_venv_folder>/bin/python -m pip install --upgrade pip setuptools wheel`
python3 -m `<name_of_new_venv_folder>/bin/python -m pip install chaste_codegen

```


# Installing chaste_codegen and building chaste without internet connection
When no internet connection is available chaste_codegen can't be installed from [pypi](https://pypi.org/project/chaste-codegen/). The following steps would enable a fully manual installation and allow building chaste:


- Create and cd into a build folder e.g. `chaste_build`
- Create the virtual environment as follows: `python3 -m venv codegen_python3_venv`
- Activate the virtual environment `source codegen_python3_venv/bin/activate` you sould now see something like: `(codegen_python3_venv) uczmh2@pmlapgmi01:~/chaste_develop$`
- run `python -m pip list` to see what packages are currently installed. Especially pip, setuptools and wheel are likley to already be installed and you may not need to reinstall them
- Download, transfer and install the required python packages (with the virtual environment activated) manually.
    - Manual instalation:
        - Download appropriavte version of package from [pypi](https://pypi.org).
        - Unzip it if it
        - cd into the directory containing setup.py
        - If there are any installation instructions contained in documentation contained herein, read and follow the instructions OTHERWISE type in `python setup.py install`
    - Codegen is tested with the following python package versions (install in this order):
        - pip > 20.2
        - wheel > 0.35
        - setuptools > 50.3
        - pip > 20.2
        - decorator >=4.4.2, <5
        - importlib-metadata >=1.7, <2
        - isodate >=0.6.0, <1
        - lxml >=4.5.2, <5
        - [MarkupSafe](https://github.com/Chaste/trac_archive/wiki/Markup-Safe) >=1.1.1, <2
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


