---
title: "Using CellML electrophysiology models in Cardiac Chaste"
description: "Using CellML electrophysiology models in Cardiac Chaste"
draft: false
images: []
toc: true
layout: "single"
---

{{< callout context="note" title="Note" icon="info-circle" >}}

This is the guide for chaste_codegen, the **Python3** code generator. For the
Python2 code generator (PyCml) used up to release 2019.1, see the
[release 2019.1](https://github.com/Chaste/Chaste/releases/tag/release_2019.1)
version of this guide.

{{< /callout >}}

**Please note:** experienced Chaste users may want to skip to the
[Summary of changes compared to PyCml](#summary-of-changes-compared-to-pycml)

This page contains some notes on generating Chaste code for cardiac cell models
from CellML files, using
[chaste_codegen](https://github.com/ModellingWebLab/chaste-codegen), the Python3
Chaste CellML toolkit. chaste_codegen is developed in Python3 and distributed
via the
[Python Package Index (PyPI)](https://pypi.org/project/chaste-codegen/). The
Chaste build process automatically creates a Python3 virtual environment and
installs chaste_codegen in this for generating code from CellML files.

The process is mostly automatic, although some of the options require some human
intervention, and the CellML file itself may need to be
[annotated](#model-annotation-with-rdf) in order to allow successful conversion
(for example, to indicate which variables represent the transmembrane potential
and stimulus current). Many annotated CellML files may be found in the Chaste
repository, either in the
[`heart/src/odes/cellml`](https://github.com/Chaste/Chaste/tree/develop/heart/src/odes/cellml)
folder, or the [cellml project](https://github.com/Chaste/cellml).

There are two main ways of using CellML within Chaste. If you are a cardiac
executable user, then providing you compiled the executable from source
yourself, CellML files may be loaded on the fly, as
[described below](#use-of-cellml-in-the-cardiac-executable). If however you are
using the source release of Chaste directly, the sections on
[using dynamically loaded CellML models](#using-dynamically-loaded-cellml-models-in-chaste-tests-or-projects)
and
[using CellML files as sources in Chaste](#using-cellml-files-as-sources-directly-in-chaste)
will be relevant.

## Using CellML files as sources directly in Chaste

The Chaste build system uses chaste_codegen to generate source code from CellML
files 'on the fly'. CellML files located within the `src` or `test` folders will
generate code that can be used like normal C++ classes. It can be very helpful
to have access to a range of models, by using the
[Chaste cellml project](https://github.com/Chaste/cellml). This project contains
many of the common models, pre-annotated with metadata for automatic conversion,
and tagging of many of the common parameters you may wish to vary/investigate.
See the `README` at the previous link for instructions on including this
project within your own project.

{{< callout context="note" title="Note" icon="info-circle" >}}

Unlike its predecessor, chaste_codegen calculates its own
analytic jacobians and does not use `.out` files.

{{< /callout >}}

### Project-specific conversion options

You can also provide project-wide arguments for conversion of any CellML files
within that project. For example, to generate cell models that use modifiers for
metadata-annotated variables, add the following line to your project's
CMakeLists.txt:

```cmake
# Here we add extra arguments to force chaste_codegen to use this extra argument
# (make Get and Set methods for all metadata annotated variables).
set(Chaste_CODEGEN_EXTRA_ARGS "--use-modifiers")
```

### Model-specific conversion options

{{< callout context="note" title="Note" icon="info-circle" >}}

Unlike its predecessor, chaste_codegen does not make use of config files, instead
chaste_codegen uses [command line arguments](#command-line-arguments). In order
to specify conversion options which are different from the default or
project-specific options, please make use of dynamic loading (see
[using dynamically loaded CellML models](#using-dynamically-loaded-cellml-models-in-chaste-tests-or-projects)).

{{< /callout >}}

### Dynamic loading

If the CellML file is placed within a `dynamic` folder (e.g.
[`heart/dynamic`](https://github.com/Chaste/Chaste/tree/develop/heart/dynamic)), however, it will be compiled to a shared library
suitable for loading dynamically by the executable. In this case, only a single
output variant (.hpp & .cpp pair) can be generated, so by default normal cells
will be generated (see [command line arguments](#command-line-arguments)). If
other types are required, edit `CODEGEN_EXTRA_ARGS` (see
[project-specific conversion options](#project-specific-conversion-options)).

See the CellML files in [`heart/src/odes/cellml`](https://github.com/Chaste/Chaste/tree/develop/heart/src/odes/cellml) for examples.

### Using dynamically loaded CellML models in Chaste tests or projects

Your own code built on Chaste may also use dynamically compiled and loaded
CellML models. There is now a helper class ​[`CellMLLoader`](https://github.com/Chaste/Chaste/blob/develop/heart/src/odes/CellMLLoader.hpp) for this. An example
is given below:

```c++
#include "CellMLToSharedLibraryConverter.hpp"
#include "AbstractCvodeCell.hpp"
...
// create a stimulus and solver for creating a cardiac cell
double magnitude = -25.5;
double duration  = 2.0 ;  // ms
double when = 50.0; // ms
boost::shared_ptr<SimpleStimulus> p_stimulus(new SimpleStimulus(magnitude, duration, when));
boost::shared_ptr<EulerIvpOdeSolver> p_solver(new EulerIvpOdeSolver);

// convert a cellml model

// find cellml file in chaste source
FileFinder cellml_file("heart/src/odes/cellml/LuoRudy1991.cellml", RelativeTo::ChasteSourceRoot);
// location to put cellml file and conversion results
OutputFileHandler handler("converted_file_folder", true);
// copy cellml file to the output location
FileFinder copied_file = handler.CopyFileTo(cellml_file);
 // prepare converter
CellMLToSharedLibraryConverter converter(true);
// specify command line conversion options
converter.SetOptions({"--cvode", "--use-analytic-jacobian"});
 //perform the conversion
DynamicCellModelLoaderPtr p_loader = converter.Convert(copied_file);
// Create a (pointer to) a cardiac cell and cast to the correct type (in ths case AbstractCvodeCell)
AbstractCvodeCell* lr91 = dynamic_cast<AbstractCvodeCell*>(p_loader->CreateCell(p_solver, p_stimulus));

```

The [cellml project](https://github.com/Chaste/cellml) contains many annotated CellML files which you may use in this fashion.

## Model annotation with RDF

CellML files may include metadata through the use of
[RDF](http://en.wikipedia.org/wiki/Resource_Description_Framework), the Resource
Description Framework (see the
[CellML metadata specification](http://www.cellml.org/specifications/metadata)
for more information). The chaste_codegen generator makes use of several
different annotations when generating C++ source code for Chaste.

Some annotations are required to enable successful code generation. In
particular, chaste_codegen needs to know which variables represent voltage, the
transmembrane potential and stimulus current, in order to link the models into
the mono/bi-domain equations. (If the model does not have a stimulus current
because it represents a self-excitatory cell, it should be
[annotated to indicate this](#self-excitatory-models).) Unlike its predecessor,
chaste_codegen does not try to guess based on names in the model so
[name annotations](#standardised-names) must be used. You may also need to
annotate the membrane capacitance if its value is required for automatic units
conversions (if the model uses amps as the dimensions of transmembrane
currents).

All metadata annotations must occur within an
`<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">` element.
Such an element may occur within any CellML element, so you may place
annotations next to the variable being annotated, or in a single `rdf:RDF`
element at the top level of the model, as you prefer. Variables to be annotated
must have a `cmeta:id` attribute, which is used to identify the variable in the
annotation.

Each annotation takes the form of an `rdf:Description` element:

```xml
<rdf:Description rdf:about="#cmeta_id">
	<!-- Annotation element goes here -->
</rdf:Description>
```

where "`cmeta_id`" is replaced by the value of the `cmeta:id` attribute on the
variable being annotated.

The following annotations are understood by chaste_codegen. See the CellML files
in
[`heart/src/odes/cellml`](https://github.com/Chaste/Chaste/tree/develop/heart/src/odes/cellml)
for examples of their use.

### Standardised names

```xml
<bqbiol:is xmlns:bqbiol="http://biomodels.net/biology-qualifiers/"
           rdf:resource="https://chaste.comlab.ox.ac.uk/cellml/ns/oxford-metadata#standard-name"/>

```

This can be used to specify the 'standard' (to chaste_codegen) name of this
variable. Replace '`standard-name`' with the name in question.

The **full list of allowed names** can be found within the `oxford-metadata.ttl`
file in the
[Web Lab Ontology source code](https://github.com/ModellingWebLab/ontologies).

To update the 'official' metadata list -- Check with Gary first! -- you need to
update the `.ttl` file, and then run a build on a machine with a newish version of
python rdflib installed (to ensure that `oxford-metadata.rdf` is also updated to
match), preferably using Python 3.

Updating the official metadata should only be done for metadata that is
generally reusable.

Currently only a few of these names, shown below, have special meaning to the
Chaste CellML translation process.

- `membrane_voltage` -- the transmembrane potential. **Please note:** this is now
  required; chaste_codegen conversion will fail if it is not present
- `membrane_capacitance` -- this is useful if converting the model current units
  to those expected by Chaste; requires knowledge of the cell's membrane
  capacitance
- `cytosolic_calcium_concentration` -- if this variable is present, the generated
  class will define the `GetIntracellularCalciumConcentration` method
- `membrane_stimulus_current` -- specifies which variable represents the
  intracellular stimulus current
- `membrane_stimulus_current_amplitude`, `membrane_stimulus_current_duration`,
  `membrane_stimulus_current_period`, `membrane_stimulus_current_offset` -- if
  the stimulus coded in the model is a regular square wave, the relevant
  parameters may be annotated to allow chaste_codegen to define the
  `UseCellMLDefaultStimulus` method that uses a `RegularStimulus` class. The
  presence of `membrane_stimulus_current_offset` is optional.

{{< callout context="note" title="Note" icon="info-circle" >}}

- All non-state-variables, annotated in this way, are accessible as
  [parameters](#modifiable-parameters) or
  [derived quantities](#derived-quantities), as appropriate. This will thus make
  them accessible via the `GetAnyVariable` and `OutputVariables` functionality.
  This includes state variables annotated with new tags that otherwise do not
  have a meaning in the ontology.
- The code generation process expects annotation to be unique (only 1 variable
  annotated with any given metadata tag)
- Only tag source variables, instead of any dependant variables with not any
  dependant ‘in’ interface. Connection resolving may well remove other of the
  variable during processing.

{{< /callout >}}

Full example:

```xml
<variable name="V" units="millivolt" initial_value="-80" public_interface="out" cmeta:id="membrane_voltage">
   <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:bqbiol="http://biomodels.net/biology-qualifiers/">
      <rdf:Description rdf:about="#membrane_voltage">
         <bqbiol:is rdf:resource="https://chaste.comlab.ox.ac.uk/cellml/ns/oxford-metadata#membrane_voltage"/>
      </rdf:Description>
   </rdf:RDF>
</variable>
```

We also use these standardised names to interface between models and protocol
definitions in the [Functional Curation](https://scrambler.cs.ox.ac.uk) system.

### chaste_codegen conversion specific parameters

In addition to the standardised names there are a number of conversion specific
annotations that can be added to a CellML model, described below.

The namespace for this annotation is named
`https://chaste.comlab.ox.ac.uk/cellml/ns/pycml#` for historical reasons to
ensure compatibility with CellML models marked up for chaste_codegen's
predecessor.

#### Modifiable parameters

```xml
<modifiable-parameter xmlns="https://chaste.comlab.ox.ac.uk/cellml/ns/pycml#">yes</modifiable-parameter>
```

This specifies that the variable should become a named parameter within the C++
class, with name given by its `cmeta:id` (unless it has a
[standardised name](#standardised-names), in which case that is used). The
variable can then be altered at run-time, via calls to the `SetParameter`
method. Such parameters can also be set via the `ChasteParameters` XML file, as
described [below](#use-of-cellml-in-the-cardiac-executable), and selected for
output using the `OutputVariables` functionality.

Full example:

```xml
<variable units="dimensionless" name="ScaleFactorGkr" initial_value="1.0" cmeta:id="ScaleFactorGkr">
  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
	<rdf:Description rdf:about="#ScaleFactorGkr">
		<modifiable-parameter xmlns="https://chaste.comlab.ox.ac.uk/cellml/ns/pycml#">yes</modifiable-parameter>
    </rdf:Description>
  </rdf:RDF>
</variable>
```

#### Derived quantities

```xml
<derived-quantity xmlns="https://chaste.comlab.ox.ac.uk/cellml/ns/pycml#">yes</derived-quantity>
```

This specifies that the variable should become a derived quantity within the C++
class, with name given by its `cmeta:id` (unless it has a
[standardised name](#standardised-names), in which case that is used). Derived
quantities may be computed using the `ComputeDerivedQuantities` and
`ComputeDerivedQuantitiesFromCurrentState` methods, and selected for output
using the `OutputVariables` functionality. This is useful for quantities which
are not necessary for computing the time evolution of the model, but still of
interest.

Full example:

```xml
<variable name="F" units="coulomb_per_millimole" public_interface="in" cmeta:id="K_F">
  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:bqbiol="http://biomodels.net/biology-qualifiers/">
    <rdf:Description rdf:about="#K_F">
      <pycml:derived-quantity>yes</pycml:derived-quantity>
    </rdf:Description>
</rdf:RDF>
</variable>
```

#### Variable range checking

Chaste has the ability to check at each time step that cell model variables have
not gone out of an expected range. This is especially useful for gating
variables, which must lie between 0 and 1, being probabilities. In order to take
advantage of this, you must annotate your model to specify the expected range,
using the `pycml:range-low` and `pycml:range-high` annotations, e.g.

```xml
<range-low xmlns="https://chaste.comlab.ox.ac.uk/cellml/ns/pycml#">0</range-low>
<range-high xmlns="https://chaste.comlab.ox.ac.uk/cellml/ns/pycml#">1</range-high>
```

The range specified is treated as a closed interval.

Full example:

```xml
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about="#gating_variable">
        <range-low xmlns="https://chaste.comlab.ox.ac.uk/cellml/ns/pycml#">0</range-low>
        <range-high xmlns="https://chaste.comlab.ox.ac.uk/cellml/ns/pycml#">1</range-high>
    </rdf:Description>
</rdf:RDF>
```

#### Self-excitatory models

This stops chaste_codegen looking for a stimulus current in the model, so that
sino-atrial node models can be used in Chaste. In this case, you need to
annotate the model itself, i.e. the `cmeta:id` used should be that on the
`model` element. For example,

```xml
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about="#demir_model_1994">
        <is-self-excitatory xmlns="https://chaste.comlab.ox.ac.uk/cellml/ns/pycml#">yes</is-self-excitatory>
    </rdf:Description>
</rdf:RDF>
```

#### Named attributes

After release 2.1 Chaste has gained the ability to use real-valued named
attributes associated with ODE classes. chaste_codegen can use this
functionality to transfer named attributes from a CellML file into Chaste, so they
are available for querying by other Chaste code. This will not typically be of
use to executable users, but developers working with Chaste may find it useful.
For example, such annotations could specify various "typical values" for the
cell model, such as normal cycle length, or suggested forward Euler time step.

These are model annotations, i.e. the `cmeta:id` used should be that on the
`model` element. For example,

```xml
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
   <rdf:Description rdf:about="#luo_rudy_1991">
      <named-attribute xmlns="https://chaste.comlab.ox.ac.uk/cellml/ns/pycml#">
         <rdf:Description>
            <name rdf:datatype="http://www.w3.org/2000/10/XMLSchema#string">SuggestedCycleLength</name>
            <value rdf:datatype="http://www.w3.org/2000/10/XMLSchema#double">750</value>
         </rdf:Description>
      </named-attribute>
      <named-attribute xmlns="https://chaste.comlab.ox.ac.uk/cellml/ns/pycml#">
         <rdf:Description>
            <name rdf:datatype="http://www.w3.org/2000/10/XMLSchema#string">SuggestedForwardEulerTimestep</name>
            <value rdf:datatype="http://www.w3.org/2000/10/XMLSchema#double">0.005</value>
         </rdf:Description>
      </named-attribute>
   </rdf:Description>
</rdf:RDF>
```

### Combining annotations

It is possible to combine annotations. The example below shows a variable that
is a cytosolic_calcium_concentration but is also marked as derived quantity:

```xml
<variable name="Ca_i" units="mM" public_interface="out" cmeta:id="cytosolic_calcium_concentration">
   <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:bqbiol="http://biomodels.net/biology-qualifiers/">
      <rdf:Description rdf:about="#cytosolic_calcium_concentration">
         <derived-quantity xmlns="https://chaste.comlab.ox.ac.uk/cellml/ns/pycml#">yes</derived-quantity>
            <bqbiol:is rdf:resource="https://chaste.comlab.ox.ac.uk/cellml/ns/oxford-metadata#cytosolic_calcium_concentration"/>
         </rdf:Description>
   </rdf:RDF>
</variable>
```

## chaste_codegen command line arguments

chaste_codegen can be supplied with command line arguments directly, to specify
the desired conversion.

{{< callout context="note" title="Note" icon="info-circle" >}}

Unlike its predecessor, chaste_codegen does not make use of config files.

{{< /callout >}}

### activation

The chaste_codegen tool is developed in Python 3 and is best installed in a
Python 3 virtual environment. The Chaste build process automatically sets up
chaste_codegen in the build folder (in 
`<build_folder>/codegen_python3_venv`) but it can also be installed manually if
desired. See [Install Codegen](../install-codegen).

To use the commands below, you can first activate the environment as follows
from your build folder: 

```sh
source codegen_python3_venv/bin/activate
```

(If you manually installed a virtual environment use its name instead of
`codegen_python3_venv`, from the correct location).

Alternatively, you can prefix the chaste_codegen command with the full path to
the `bin` folder in the virtual environment e.g.

```sh
$HOME/chaste_build/codegen_python3_venv/bin/chaste_codegen
```

without the need to activate the environment.

### command line arguments

`chaste_codegen -h` displays the help giving a full overview of what is available.

There are a number of different arguments: [the cellml file](#the-cellml-file),
[model types](#model-types), [Chaste options](#chaste-options) and
[generated code options](#generated-code-options). Below is a summery of some of
the most common options.

### The cellml file

chaste_codegen takes what the help calls a "positional argument". This is the
CellML file being converted e.g.

```sh
chaste_codegen hodgkin_huxley_squid_axon_model_1952_modified.cellml`
```

Other arguments (preceded by `--` or `-`) can be placed before or after the CellML
file in any order.

### Model types

There are arguments that control what kind of model (CardiacCell) is being generated.

#### Generating a normal model, or standard *AbstractCardiacCell* subclass

This can be generated using the `--normal` argument e.g.

```sh
chaste_codegen hodgkin_huxley_squid_axon_model_1952_modified.cellml --normal
```

This is the default if no transformation type is indicated an `AbstractCardiacCell` will also be generated.

#### Generate CVODE cells, *AbstractCvodeCell* subclass.

CVODE cells can be generated using the `--cvode` argument. chaste_codegen can
generate its own analytic jacobian. To include an analytics jacobian combine
`--cvode` with `--use-analytic-jacobian` (or `-j`) e.g.

```sh
chaste_codegen hodgkin_huxley_squid_axon_model_1952_modified.cellml --cvode --use-analytic-jacobian
```

#### Generate CVODE cells with data clamp

A subclass `AbstractCvodeCellWithDataClamp` allows the 'data clamp' proposed by
[Dokos & Lovell (2004)](http://www.ncbi.nlm.nih.gov/pubmed/15142755) to be
applied to any CellML model. This can be generated using the
`--cvode-data-clamp` argument. If desired this can also be generated with an
analytic jacobian using the `--use-analytic-jacobian` (or `-j`) argument e.g.

```sh
chaste_codegen hodgkin_huxley_squid_axon_model_1952_modified.cellml --cvode-data-clamp --use-analytic-jacobian
```

This adds an additional current to the model, specified by:

```c++
I_data = g_data*(V - V_data);
```

{{< callout context="note" title="Note" icon="info-circle" >}}

This current affects `dV/dt` for single cell simulations only. It is not
reported by `GetIIonic()` so it assumes `I_data=0` in tissue simulations!

{{< /callout >}}

This can be used via the methods:

```c++
AbstractCvodeCellWithDataClamp::SetExperimentalData(std::vector<double> times, std::vector<double> voltages);
AbstractCvodeCellWithDataClamp::SetDataClampOn(double conductance);
AbstractCvodeCellWithDataClamp::SetDataClampOff();
```

#### Generating Backward Euler cells, *AbstractBackwardEulerCardiacCell* subclass

This can be generated using the `--backward-euler` argument e.g.

```sh
chaste_codegen hodgkin_huxley_squid_axon_model_1952_modified.cellml --backward-euler
```

#### Generating Rush Larsen cells, *AbstractRushLarsenCardiacCell* subclass

This can be generated using the `--rush-larsen` argument e.g.

```sh
chaste_codegen hodgkin_huxley_squid_axon_model_1952_modified.cellml --rush-larsen
```

#### Generating Generalized Rush Larsen cells, *AbstractGeneralizedRushLarsenCardiacCell* subclass

chaste_codegen can generate both a first-order generalisation as well as a
second order generalisation. The arguments that can be used for this are
`--grl1` and `--grl2` respectively so e.g.

```sh
chaste_codegen hodgkin_huxley_squid_axon_model_1952_modified.cellml --grl1
```

or

```sh
chaste_codegen hodgkin_huxley_squid_axon_model_1952_modified.cellml --grl2
```

### Chaste options

- `--dynamically-loadable` (or `-y` or `--dll`), generate the code allowing it
  to be dynamically loaded. **Please note:** This method is mainly useful for
  the build system to generate code in the `dynamic` folder or by the
  ​[`CellMLLoader`](https://github.com/Chaste/Chaste/blob/develop/heart/src/odes/CellMLLoader.hpp). It should not be used if generating code
  to include in the source of your project.
- `--opt` generate an optimised version of the specified models with partial
  evaluation and lookup tables. Can be combined with any model type above.
- `--use-modifiers` (or `-m`) adds modifier functions for metadata-annotated
  variables (except time & stimulus). Only works with `--normal`, `--cvode` and
  `--cvode-data-clamp`
- `--lookup-table <metadata tag> min max step` indicates a lookup table
  different from the default. The argument must be followed by a metadata tag to
  identify the variable, a minimum and maximum value and a step. The argument
  can be repeated to specify lookup tables for multiple different variables. The
  default is `membrane_voltage -250.0001, 549.9999, 0.001`. **Please note:**
  Using this argument disables the default, so if a lookup table is required for
  a variable tagged as `membrane_voltage` it will need to be re-specified. Tags
  which are not present in the model are skipped.

### Generated code options

These options do not affect what kind of cells get generated, but instead affect
some general logistics. Unless otherwise specified these can be combined with
other options. The arguments are:

- `-o OUTFILE` specifies the name of the generated code file. The outfile is
  expected to be header file (.hpp or .h), a code file (.cpp or .c) and the name
  given and its corresponding header/code file will be generated. **Cannot be
  combined with** `--output-dir`.
  - This can also be used with a CellML file, which will result in a .cpp and
    .hpp file with the name of the CellML file being generated. This is the
    **default behaviour** if `-o` is not specified.
- `--output-dir OUTPUT_DIR` specified an output folder for generated code.
  **Cannot be combined with** `-o`.
- `--show-outputs` instead of generating code this option shows what files would
  be generated (one per line) if the command was run without the option.
- `-c CLS_NAME` explicitly sets the name of the generated class. If this option
  is not used, the class name is based on the name of the CellML file.
- `--quiet` (or `-q`) disables warning and informational messages.

## Use of CellML in the cardiac executable

The [cardiac executable](../../dev-guides/building-executable-apps) has the ability to
automatically load cell models encoded as CellML files at run-time. In order to
take advantage of this, you need (at present) to have built the executable from
source yourself, as it uses your Chaste source tree to convert the CellML file
into runnable code.

To specify one of the models included within Chaste in the parameters file, you
now need to wrap it in a `<Hardcoded>` element, e.g.

```xml
<Hardcoded>FaberRudy2000</Hardcoded>
```

Specify a dynamically loaded model using the `<Dynamic>` element instead, e.g.

```xml
<Dynamic>
    <Path relative_to="chaste_build_root">heart/dynamic/libDynamicallyLoadableLr91.so</Path>
</Dynamic>
```

The path may either point to a pre-compiled shared library (as in the example),
or a CellML file. If the latter, a shared library will be created in the same
folder as the CellML file, and loaded by the executable at run-time. See
[`heart/test/data/xml/ChasteParametersFullFormat.xml`](https://github.com/Chaste/Chaste/tree/develop/heart/test/data/xml/ChasteParametersFullFormat.xml)​
for a full example parameters file.

Chaste allows modifying certain parameters of the models within user-defined
regions of the tissue. This is incorporated within the cell heterogeneity
support in the parameters file:

```xml
<CellHeterogeneity>
   <Location unit="cm">
      <Cuboid>
         <LowerCoordinates x="-2.0" y="-0.1" z="-1.0"/>
         <UpperCoordinates x="-0.5" y="0.1" z="1.0"/>
      </Cuboid>
   </Location>
   <SetParameter name="example" value="0.0"/>
   <SetParameter name="example2" value="2.0"/>
</CellHeterogeneity>
```

Parameters to be modified in this way must be annotated specially in the CellML
file -- you cannot just modify any variable in the model. Each variable must have
a `cmeta:id` specified (this gives the name used in the `<SetParameter>` element) and
an RDF annotation added, e.g.

```xml
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
   <rdf:Description rdf:about="#example">
      <modifiable-parameter xmlns="https://chaste.comlab.ox.ac.uk/cellml/ns/pycml#">yes</modifiable-parameter>
   </rdf:Description>
</rdf:RDF>
```

Such a block may be placed inside any CellML element, but placing it within or
next to the annotated variable is recommended. See
[Model Annotation with RDF](#model-annotation-with-rdf) for more. The older
scale factor support, which was hardcoded is no longer supported

Variable annotation as a parameter or derived quantity is also important to
support the `OutputVariables` functionality in the executable. Any variable thus
annotated, or any state variable, may be specified to be included in the output
data along with `V` and `phi_e`.

**Please note:** As chaste_codegen does not use config files, options
controlling the code generation process for the CellML file are as follows:

- Set
  [Project-specific conversion options](#project-specific-conversion-options).
- Use chaste_codegen to manually create .cpp and .hpp files (see
  [chaste_codegen command line arguments](#chaste_codegen-command-line-arguments)),
  include these in your project source and either directly include or point your
  parameters file at the shared library that results from its compilation.
- Use
  [dynamic loading](#using-dynamically-loaded-cellml-models-in-chaste-tests-or-projects)
  to convert the code and point the parameters file at the CellML file in the
  conversion folder, it will pick up the converted version.
- Use
  [dynamic loading](#using-dynamically-loaded-cellml-models-in-chaste-tests-or-projects)
  via code instead.

## Summary of changes compared to PyCml

This section highlights the main difference between chaste_codegen and its
predecessor PyCml. The two work in broadly similar ways, but there are some key
differences.

- chaste_codegen generates its own analytic jacobians and the
  `--use-analytic-jacobian` (or `-j`) argument is now used without specifying a
  `.out` file. Where a two-step process was required it is no longer required.
- chaste_codegen does not make use of config files.
  - The only way to specify what kind of code to generate is now via the command
    line arguments.
  - To generate different models from the default, use
    [dynamic loading](#using-dynamically-loaded-cellml-models-in-chaste-tests-or-projects)
    or set
    [project-specific conversion options](#project-specific-conversion-options).
  - Lookup table settings can also be specified via the command line -- see
    [Chaste options](#chaste-options)
- chaste_codegen is fully re-written for Python 3 and during the build process a
  virtual environment is set up with the required packages. See
  [Install Codegen](../install-codegen).
