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

{{< callout context="note" title="Web Portal" icon="info-circle" >}}

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
