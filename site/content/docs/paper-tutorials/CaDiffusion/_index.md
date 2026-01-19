---
title: "Ca<sup>2+</sup> Channel Re-localization to Plasma-Membrane Microdomains Strengthens Activation of Ca<sup>2+</sup>-Dependent Nuclear Gene Expression"
draft: false
layout: "single"
showPageLinks: true
paperTutorialProject: "https://github.com/Chaste/project_CaDiffusion"
---

Welcome to the Chaste wiki.

This section contains pages generated automatically from the source code accompanying [Samanta et al. (2015)](http://dx.doi.org/10.1016/j.celrep.2015.06.018).

Before running these examples you will need to [install Chaste's dependencies](https://chaste.github.io/old_releases/release_3.4/InstallGuides/InstallGuide.html).
The easiest way to do this is using an Ubuntu machine (or an Ubuntu virtual machine) as discussed on InstallGuides/UbuntuPackage.
Note that cardiac Chaste is not supported on Windows, so users of Windows will need to follow the virtual machine route.
For manual installation of each dependency, on any version of Linux, see DeveloperInstallGuide.

The simulations featured in the paper supplement are explained and annotated below.
For further information on using Chaste to solve these and related problems, see our [extensive guide material](https://chaste.github.io/old_releases/release_3.4/ChasteGuides.html).

This work is licensed under the Chaste BSD 3 clause licence and the [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/). To comply with this licence, please cite the following papers if you re-use this code for an academic publication:


* K Samanta, P Kar, GR Mirams, AB Parekh (2015). Ca2+ channel re-localization to plasma membrane microdomains strengthens activation of Ca2+-dependent nuclear gene expression. Cell Reports 12(2), 203-216. [doi:10.1016/j.celrep.2015.06.018](http://dx.doi.org/10.1016/j.celrep.2015.06.018).

* GR Mirams, CJ Arthurs, MO Bernabeu, R Bordas, J Cooper, A Corrias, Y Davit, S-J Dunn, AG Fletcher, DG Harvey, ME Marsh, JM Osborne, P Pathmanathan, J Pitt-Francis, J Southern, N Zemzemi, DJ Gavaghan (2013). Chaste: an open source C++ library for computational physiology and biology. PLoS Computational Biology, 9(3), e1002970. [doi:10.1371/journal.pcbi.1002970](http://dx.doi.org/10.1371/journal.pcbi.1002970).


## Diffusion study

The steps required to reproduce the study are given in the following tutorial file: [C++ file for performing simulation](https://github.com/Chaste/project_CaDiffusion/blob/2013ec7101a1f24ddab6ec0396a918f597cd1433/test/TestCaDiffusionLiteratePaper.hpp).


## Sample commands to run everything

Install Chaste 3.4 and this project direct from our repository, you may do so from the command line as follows:

```bash
#!sh
git clone -b release_3.4 https://chaste.cs.ox.ac.uk/git/chaste.git Chaste
cd Chaste/projects
git clone https://github.com/Chaste/project_CaDiffusion.git CaDiffusion
```

To run the simulations, use:

```bash
#!sh
cd <path/to>/Chaste
scons chaste_libs=1 brief=1 build=GccOptNative projects/CaDiffusion
```


## Section contents
