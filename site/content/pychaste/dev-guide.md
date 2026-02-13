---
title: "PyChaste Developer Guide"
description: "PyChaste Developer Guide"
draft: false
images: []
layout: "single"
---

This is a developer guide on generating Python wrappers for cell-based Chaste and fixing common problems related to wrappers.

## Running tests

To get started, see the [install guide](../installation/#build-from-source) for detailed instructions on building PyChaste from source.

From the build directory run all PyChaste tests with:

```sh
ctest -L pychaste
```

If working in a docker container or other headless environment, run the above with `xvfb-run` for off-screen rendering:

```sh
xvfb-run --server-args="-screen 0 1024x768x24" ctest -L pychaste
```

To check for C++ classes that are missing Python wrappers, run:

```sh
ctest -V -R TestPyWrapperChanges$
```

This will flag any classes in cell-based Chaste that need wrappers. For example:

```console
Unknown class NewCellCycleModel from /Chaste/cell_based/NewCellCycleModel.hpp
```

## Wrapping classes

During cmake configuration, Python wrappers are automatically generated from the settings in `Chaste/pychaste/dynamic/config.yaml`. The generated wrappers are stored under the `build` directory in `build/pychaste/wrappers`.

### Wrapping a new class

To add a new class, put a new entry with the name of the class in the `config.yaml` settings. For example, to create Python wrappers for a `NewCellCycleModel` class, put in the following entry under `classes`:

```yaml
- name: NewCellCycleModel
```

Next, add an import for the class (or its template instantiations) in the appropriate `__init__.py` under `pychaste/src/py/chaste`. For example, if it is templated on spatial dimensions and belongs in `cell_based`, add the following to the imports list in `pychaste/src/py/chaste/cell_based/__init__.py`:

```py
from ... import (
  ...
  NewCellCycleModel_2
  NewCellCycleModel_3
  ...
)
```

If the class is templated, add a template syntax entry for it further down in the same `__init__.py`. For example:

```py
NewCellCycleModel = TemplateClassDict(
    {
        ("2",): NewCellCycleModel_2,
        ("3",): NewCellCycleModel_3,
    }
)
```

This enables using the class via the more convenient `ccm = NewCellCycleModel[2]` notation.

If cmake configuration has already been run, re-generate the wrappers with:

```sh
make pychaste_wrappers
```

The new wrappers will now be stored under `build/pychaste/wrappers` as `NewCellCycleModel.cppwg.[c|h]pp`.

### Excluding a class from wrapping

To exclude a class from wrapping, add an `excluded` flag to the entry for the class e.g.

```yaml
- name: NewCellCycleModel
  excluded: True
```

This will ensure that wrappers are not created for the class. It will also prevent tests from flagging it as a class that is missing Python wrappers.

### Removing or renaming an existing class

If a class has been removed or renamed in the main codebase, it should be removed or renamed in `config.yaml` as well. Otherwise, errors will arise during cmake configuration such as:

```console
fatal error: 'NewCellCycleModel.hpp' file not found
```

All other references to the removed/renamed class and its instantiations should be removed from the code as well.

## Troubleshooting Problems

### Reproducing PyChaste CI Errors

Start a docker container
```sh
docker run -it --init --rm ubuntu:noble
```

Install system dependencies
```sh
apt-get update
apt-get install -y castxml clang cmake pkg-config libx11-dev xvfb libosmesa6-dev libpthread-stubs0-dev wget git build-essential
```

Install conda
```sh
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

Start a new shell to activate conda
```sh
bash
```

Clone Chaste
```sh
git clone https://github.com/Chaste/Chaste.git
```

Create a conda environment
```sh
conda env create -n py311 -f Chaste/pychaste/src/py/conda/envs/env_python3.11.yaml
conda activate py311
```

Configure and build PyChaste
```sh
cd Chaste
mkdir build
cd build

cmake \
-DChaste_ENABLE_PYCHASTE=ON \
-DCMAKE_BUILD_TYPE=Release \
-DBUILD_SHARED_LIBS=ON \
-DCMAKE_INSTALL_PREFIX="${CONDA_PREFIX}" \
-DCMAKE_PREFIX_PATH="${CONDA_PREFIX}" \
-DCMAKE_LIBRARY_PATH="${CONDA_PREFIX}/lib" \
-DBOOST_ROOT="${CONDA_PREFIX}" \
-DHDF5_C_COMPILER_EXECUTABLE="${CONDA_PREFIX}/bin/h5pcc" \
-DPETSC_DIR="${CONDA_PREFIX}" \
-DPYTHON_EXECUTABLE="$(which python)" \
-DVTK_DIR="${CONDA_PREFIX}" \
-DXERCESC_INCLUDE="${CONDA_PREFIX}/include" \
-DXERCESC_LIBRARY="${CONDA_PREFIX}/lib/libxerces-c.so" \
-DXSD_EXECUTABLE="${CONDA_PREFIX}/bin/xsd" \
..

make -j4 pychaste
```

Install the built package
```sh
python3 -m pip install -v pychaste/package
```

Run PyChaste tests
```
xvfb-run --server-args="-screen 0 1024x768x24" ctest -j $(nproc) -L pychaste --output-on-failure
```

### PETSc-related Errors

**Error:**

```console
/usr/include/c++/11/type_traits: 
In instantiation of ‘struct std::is_base_of<pybind11::detail::pyobject_tag, _p_Vec>’:
/.../Chaste/build/_deps/pybind11-src/include/pybind11/cast.h:2098:68:   
recursively required by substitution of 
‘template<class T> class pybind11::detail::type_caster<T, typename std::enable_if<
  std::is_base_of<
    pybind11::detail::pyobject_tag, typename std::remove_reference<_Tp>::type>::value, void>::type> 
[with T = _p_Vec]’
```

**Solution:**

In `config.yaml`, add the following to `Foo`

```yaml
- name: Foo
  source_includes:
    - PybindPetscTypeCaster.hpp
```

### UBLAS-related Errors

**Error:**

```console
TypeError: Unregistered type : boost::numeric::ublas::c_vector<double, 3ul>

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  ...
TypeError: Unable to convert function return value to a Python type! The signature was
	(self: chaste._pychaste_lib.Foo_3) -> boost::numeric::ublas::c_vector<double, 3ul>
Failed
```

**Solution:**

In `config.yaml`, add the following to `Foo`

```yaml
- name: Foo
  source_includes:
    - PybindUblasTypeCaster.hpp
```

### VTK-related Errors

**Error:**

```console
TypeError: Unregistered type : vtkSmartPointer<vtkRenderer>

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  ...
TypeError: Unable to convert function return value to a Python type! The signature was
	(self: chaste._pychaste_lib.Foo) -> vtkSmartPointer<vtkRenderer>
Failed
```

**Solution:**

Ensure that your system VTK version matches the version installed in Python.

In `config.yaml`, add the following to `Foo`

```yaml
- name: Foo
  source_includes:
    - PybindVTKTypeCaster.hpp
```

### Other Errors

**Error:**

```console
pygccxml.declarations.runtime_errors.declaration_not_found_t: Unable to find declaration. 
Matcher: [(decl type==class_t) and (name==Foo)]
```

**Solution:**

Check if the template args of class `Foo` are in the `template_substitutions` list of `config.yaml` and add it if missing.

For example, if `Foo` is defined as `<unsigned DIMENSIONS> class Foo {...}`, and `Foo` is explicitly instantiated for `DIMENSIONS=2` and `DIMENSIONS=3`:

```yaml
template_substitutions:
  - signature: <unsigned FOO_DIM>
    replacement: [[2], [3]]
```

**Error**

```python
import chaste
```

```console
ImportError: /.../lib.so: undefined symbol: _ZN11Foo7BarEv
```

`Foo::Bar` has been declared but not implemented. If `Foo::Bar` is not implemented, it can be excluded from wrapping by modifying `config.yaml`:

```yaml
- name: Foo
  excluded_methods:
    - Bar
```

{{< callout context="tip" title="See Also" icon="outline/rocket" >}}

* [Settings in `config.yaml`](https://github.com/Chaste/cppwg/blob/develop/examples/shapes/wrapper/package_info.yaml)
* [PyChaste Installation](../installation/)

{{< /callout >}}

