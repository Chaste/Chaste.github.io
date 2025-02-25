---
title: "Action Potential Prediction Project"
description: "Prediction of action potential changes under drug-block of ion channels"
draft: false
images: []
toc: true
layout: "single"
---

ApPredict is a free open source program for prediction of action potential
changes under drug-block of ion channels. The ion channel block is modelled as
_conductance block_, see [Gary Mirams' book chapter](https://doi.org/10.1007/978-3-030-73317-9_137-1) for details of this,
and it can be used with a number of action potential models
(specified using CellML), different pacing rates, and blockade of the following
ion channels can be included: 
 * IKr (hERG), 
 * ICaL (CaV1.2),
 * INa (NaV1.5), 
 * INaL (NaV1.5, late or persistent),
 * IKs (KCNQ1), 
 * Ito (Kv4.3), 
 * IK1 (KCNN4).

If you have any questions/comments, please get in touch with
`gary.mirams@nottingham.ac.uk`.

{{< callout context="note" title="Web Portal" icon="outline/info-circle" >}}

A web-based portal interface to this program is now available:
[https://chaste.cs.ox.ac.uk/ActionPotential/](https://chaste.cs.ox.ac.uk/ActionPotential/)
(feedback welcome), if you use this you can ignore all the instructions below --
it's all set up for you!

{{< /callout >}}

## The Science

For an overview of what ApPredict is doing, why, and how well it is performing,
please see the user guide which is hosted [on
Figshare](http://dx.doi.org/10.6084/m9.figshare.1039436) and the [ApPredict
paper](http://dx.doi.org/10.1016/j.vascn.2015.05.002).

## Using ApPredict

### Installation

**N.B.** you don't need to do any of the below to use the [web portal version of
ApPredict](https://chaste.cs.ox.ac.uk/ActionPotential/).

#### Pre-requisites

ApPredict requires a 'Code User' or 'Code Developer' version of Chaste to be
installed and compiled. See [GettingStarted](/docs) for a guide on what we mean,
and how to do this.

#### Code User: Stable Release Version

A stable version of ApPredict, compatible with the latest release of Chaste, is
available either to download, or as a tag within github.

#### Option 1: Download

Download both:

- the latest release of Chaste from
  [https://github.com/Chaste/Chaste/releases](https://github.com/Chaste/Chaste/releases),
  and
- the corresponding release of ApPredict from
  [https://github.com/Chaste/ApPredict/releases](https://github.com/Chaste/ApPredict/releases).

#### Option 2: Get from Github

To get both the release of Chaste and ApPredict do:

```sh
git clone -b 2024.1 https://github.com/Chaste/Chaste.git
cd Chaste/projects
git clone --recursive -b v2024.1 https://github.com/Chaste/ApPredict.git
```

#### Code Developer: Development Version

Alternatively the development version can be downloaded using git, using the
following instructions (as per the [Repository Access
Guide](/docs/dev-guides/access-code-repository/)):

```sh
git clone -b develop https://github.com/Chaste/Chaste.git
```

If you are not using the [Ubuntu package](/docs/installguides/ubuntu-package)
then the environment settings will need to be updated to give the correct paths
to all of Chaste's dependencies. See the [Developer Install Guide](/docs/dev-guides/developer-install-guide).

then similarly in the same folder

```sh
git clone --recursive https://github.com/Chaste/ApPredict.git
cd Chaste/projects
ln -s ../../ApPredict
cd ..
```

The project can be kept up to date by simply navigating to the `Chaste` folder
and running

```sh
git pull
cd projects/ApPredict
git pull
```

The [External Developer Guide](/docs/dev-guides/external-developer-guide)
provides a guide as to the latest revision that passed all tests.

### Compilation

See Step 4 of [the user project guide](/docs/user-guides/user-projects/) for instructions on how to compile ApPredict (where `<your_project_name>` is `ApPredict`).

### Running

```sh
./projects/ApPredict/apps/src/ApPredict
```

The executable will then display a list of command line arguments.

(**N.B.** you may have to add Chaste libraries under the Chaste libs folder to your `LD_LIBRARY_PATH` variable)

### Error Codes

When you start blocking ion channels, various funny things can happen and lead
to error codes in action potential evaluation. Here is a schematic of the errors
you can get back from ApPredict's main methods.

<img src=/fig/appredict_error_codes.jpg alt="ApPredict error codes" style=height:600px class=chaste-figure>

## Using your own CellML models

{{< callout context="note" title="Model Tagging" icon="outline/info-circle" >}}

Whichever method you use, you will need to "tag" the CellML file with our RDF metadata, to tell ApPredict which variable represents which current, etc. See the next section for instructions on how to do this.

{{< /callout >}}

There are a number of ways to use CellML models with ApPredict:

 * **Pre-compiled**: the fastest method is to provide a CellML file when building the ApPredict executable. This is then automatically converted to C++ hpp and cpp files just once, at ApPredict's compile time, and compiled-in to the ApPredict library for instant use. 

    To do this, you simply need to put your CellML file into your local clone of the `ApPredict/src/extra_models` folder ([here on github](https://github.com/Chaste/ApPredict/tree/main/src/extra_models)), before beginning the compilation process. These pre-compiled models can be used by providing the argument `--model <name of cellml file (without .cellml on the end)>`.
  
    A handful of the most commonly-used models for drug studies are already compiled into ApPredict, and these can be accessed by the `--model N` argument, where `N` is the model number (or their name as above). These models are:

    | N    | Model Name    | species and cell type | Reference |
    | ---- | -----------   | --------------------- | --------- |
    | 1    | Shannon       | rabbit ventricle      |           |
    | 2    | Ten Tusscher  | human ventricle       |           |

 * **Runtime conversion and compilation**: the most flexible method is to convert a CellML file to C++ at runtime, and compile it on the fly. This is slower, but allows any CellML file to be used with a pre-existing ApPredict binary executable, note you do need a working Chaste installation/dependencies and source tree to do the on-the-fly compilation step.

   To do this option, simply provide the argument `--cellml <relative or absolute path to cellml file (including .cellml on the end)>`.

## Tagging CellML models

Chaste needs to know:

1) what variable is `Voltage`, `Stimulus Current`, `Capacitance` etc., so that the model can be converted to a consistent interface for Chaste (behind the scenes, with automatic units conversion, thanks to a piece of software called [chaste_codegen](https://github.com/ModellingWebLab/chaste-codegen)). 

ApPredict also needs to know:

2) which variables in a CellML model represent the currents that it is going to block. 

Both of these sets of info are communicated by adding some metadata 'tags' or 'annotations' to the CellML file. 

The tags themselves take the form of [RDF metadata](https://en.wikipedia.org/wiki/Resource_Description_Framework) (but that's not so important to know!), and the list of recognised tags is given in our [oxmeta ontology](www.github.com/ModellingWebLab/ontology), which is shared by Chaste, ApPredict and [Web Lab](https://chaste.cs.ox.ac.uk/WebLab).

There are a number of ways to do this:

 * ***Easiest***: Some 'heavily annotated' models that will probably already have all the necessary metadata annotated/tagged are available at [https://github.com/Chaste/cellml](https://github.com/Chaste/cellml). So check here first as it may contain the model you want, already tagged with the necessary metadata for ApPredict to work with it.

 * **Fairly Easy**: the [Cardiac Electrophysiology Web Lab](https://chaste.cs.ox.ac.uk/WebLab) contains an annotation tool, so that you can drag and drop metadata terms onto variables/parameters in the CellML model. To do this you'll need to [register](https://scrambler.cs.ox.ac.uk/accounts/register/) then contact [gary.mirams@nottingham.ac.uk](mailto:gary.mirams@nottingham.ac.uk) to ask for 'Modeller' permissions for the account you just created, and then when we've granted that you can upload your CellML model and annotate it. 
   * My Files ->  Models -> Create New Model. Put in a name and upload your CellML file as a Private file. This becomes version 1.
   * Navigate to the model (My files -> Models) and click on it.
   * Now click on the little blue molecule symbol which takes you to the annotation tool: 
  <img src=/fig/annotating_cellml.png alt="Button to Annotate CellML files on Web Lab" style=width:700px class=chaste-figure>
   * You can then drag terms from the ontology on the right onto variables in the model on the left.
   * Once you're done, click 'Save Model Annotations' which creates version 2, and then you can click the green arrow to the right of the annotation tool to download your annotated CellML file.

 * **More involved**: 'manual' annotation can be done by inserting some text into the CellML files themselves. See [Code Generation from CellML](/docs/user-guides/code-generation-from-cellml/#model-annotation-with-rdf) as well as the ontology terms.

## Release Notes

* ApPredict is still in active development. More recent release notes are on [https://github.com/Chaste/ApPredict/releases](https://github.com/Chaste/ApPredict/releases).

### Old Release Notes

* October 2017 - there are now some new error codes to get more fine-grained information out when APD evaluations fail, or there is unusual behaviour that might want to be classed separately (see above).
* April 2017 - [fa8a3a4](https://github.com/Chaste/ApPredict/commit/fa8a3a455001184bd0479ffca75ab1862a2962f1) The `LookupTableGenerator` (for uncertainty quantification calculations) is now a bit better at detecting 'No depolarization' because it does a pre-run with sodium channel blocked and sets the threshold for an action potential to be higher than the voltage achieved here.
* Nov 2016 - the code has moved to a [github repository](https://github.com/Chaste/ApPredict)
    * In [2361a19](https://github.com/Chaste/ApPredict/commit/2361a19be47b15cd6389fdad971076bc097bbdd3) downsampling was improved to provide nicer visual plots.
* Feb 2016 - Release 3.4 of ApPredict is available to download. Important changes since the Release 3.3 version of ApPredict are listed here:
    * In r25668:
        * New command line arguments have been added that allow the 'saturation level' of a dose response curve to be specified with options like `--saturation-herg` or `--saturation-na` etc.. The value(s) that follow are given as percentages, where 0% is the default (full block of the ion channel), 50% would mean an infinite amount of drug can only halve the conductance. Additionally, this allows agonists (activators) to be modelled by specifying saturation levels above 100% (in which case the IC50 is really an EC50, but interface still says IC50).
    * As of r24408: A number of additional options to:
        * Allow any CellML model to be used (when tagged with Chaste metadata - all the ones included in ApPredict/src/cellml are ready to use).
        * Allow the downsampling associated with voltage traces to be switched off (it is on as default to make online plotting fast).
        * Allow the stimulus current properties to be changed.
    * The new flags for these options can be seen by running the executable with no arguments.
