---
title: "Paper tutorials"
draft: false
layout: "single"
disable_adjacent_navigation: true
version: "2024.2"
---

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
**The tutorials here are static, and are only likely to work with the specific version of Chaste indicated. They are unlikley to work with the development version of Chaste**.
{{< /callout >}}


## Paper Tutorials

This is the home page for what we call *Paper Tutorials*.

Open-source releasing code that has been used to generate results in papers increases the credibility of the paper results, and enables other researchers to more easily build upon the results. Our aim here is to extend this idea to make it very easy to reproduce results in papers generated using Chaste.

Each paper listed below links to wiki pages associated with that paper. Here, you will find a brief introduction to the paper (including instructions on how to obtain the code and supporting data files used for the paper), and links to 'walk-throughs' of the code used to generate the paper results. These walk-throughs are in the same style as the main Chaste tutorials. (They are also auto-generated from comments in the actual code.) For a quick example, choose *[G. Mirams et al. Chaste: an open source...](plos2013)*, and then click on one of the images.

The results of each paper are then reproducible by simply downloading the code, and running with the relevant version of Chaste.  See [Getting Started](/docs) for more documentation on using Chaste.

Since we tend to use the Chaste build infrastructure to do our science, as well as develop Chaste itself, code like these tutorials that generates results for publication is itself a 'test' in the Chaste framework.
It is thus easy to check the results obtained when re-running against the published reference results, to ensure that the quantities of interest are unchanged (to within tolerances).
This is done, for instance, in the [functional curation](functionalcuration) and [ICCS2013](wisc2013) papers.

*Note that this is a new feature: the framework for setting up these paper tutorials is still being finalised, and more papers will be added in time. In the future we envisage external users, who wish to release their own documented Chaste code, also being able to contribute to these pages.*


### 2018

* [Almet et al. (2018) "A multicellular model of intestinal crypt fission"](epithelialfission)
* [Osborne JM and Bernabeu MO (2018) "A fully discrete open source framework for the simulation of vascular remodelling"](embc2018)
* [Daly et al. (2018) "Inference-based assessment of parameter identifiability in nonlinear biological models"](dalyid)


### 2017

* [Osborne JM, Fletcher AG, et al. (2017) "Comparing individual-based approaches to modelling the self-organization of multicellular tissues". PLoS Computational Biology](cellbasedcomparison2017)
* [Daly AC, Cooper J, Gavaghan DJ, Holmes C (2017) "Comparing two sequential Monte Carlo samplers for exact and approximate Bayesian inference on biological models". J. Roy. Soc. Interface](dalysmc)
* [Grogen, JA et al. (2017) "Microvessel Chaste: An Open Library for Spatial Modeling of Vascularized Tissues". Biophys J.](microvessel)


### 2016

* [Mahoney et al. (2016) "Connexin 43 contributes to electrotonic conduction across scar tissue in the intact heart", ​Scientific Reports](mouselesion)
* [Langlands et al (2016) "Paneth cell-rich regions separated by a cluster of Lgr5+ cells initiate fission in the intestinal stem cell niche", PLoS Biology](cryptfissionplos2016).
* [S-J. Dunn et al (2016) "Combined changes in Wnt signaling response and contact inhibition induce altered proliferation in radiation-treated intestinal crypts", Mol. Biol. Cell](cryptproliferationdistribution).


### 2015

* [Daly et al. ​Hodgkin-Huxley revisited: reparameterization and identifiability analysis of the classic action potential model with approximate Bayesian methods, J. R. Soc. Interface, 2015](hodgkinhuxleyabc).
* [Osborne. Multiscale Model of Colorectal Cancer Using the Cellular Potts Framework, Cancer Informatics, 2015](pottscrypt2015).
* [Rubinacci et al. CoGNaC: A Chaste Plugin for the Multiscale Simulation of Gene Regulatory Networks Driving the Spatial Dynamics of Tissues and Cancer, Cancer Informatics, 2015](cognac).
* [Samanta et al. Ca2+ Channel Re-localization to Plasma-Membrane Microdomains Strengthens Activation of Ca2+-Dependent Nuclear Gene Expression, Cell Reports, 2015](cadiffusion).
* [Capel et al. Hydroxychloroquine reduces heart rate by modulating the hyperpolarisation-activated current 'If': Novel electrophysiological insights and therapeutic potential, Heart Rhythm, 2015](hr2015).
* [Harvey, Fletcher, Osborne and Pitt-Francis. A parallel implementation of an off-lattice individual-based model of multicellular populations, Computer Physics Communications, 2015](harvey2015).
* [Bordas, R et al. Development and Analysis of Patient-Based Complete Conducting Airways Models, PLoS ONE, 2015](airwaygeneration2015)


### 2014

* [J. Cooper, R. Spiteri and G. Mirams. Cellular cardiac electrophysiology modelling with Chaste and CellML, Frontiers in Physiology, 2014](frontiers2014).


### 2013

* [Figueredo et al. On-lattice agent-based simulation of populations of cells within the open-source Chaste framework, Interface Focus, 2013](interfacefocus2013).
* [Pathmanathan and Gray. Verification of computational models of cardiac electro-physiology, Int. J. Numerical Methods in Bioengineering, 2013](cardiacepverification).
* [Britton et al. Experimentally calibrated population of models predicts and explains inter-subject variability in cardiac cellular electrophysiology. PNAS, 2013](pnaspopulationofmodels).
* [Walmsley et al. mRNA Expression Levels Predict Cellular Electrophysiological Remodeling in Failing Human Hearts: A Population-Based Simulation Study. PLoS ONE, 2013](plosone).
* [Cooper and Osborne. Connecting models to data in multiscale multicellular tissue simulations. International Conference on Computational Science, 2013](wisc2013).
* [Mirams et al. Chaste: an open source C++ library for computational physiology and biology. PLoS Computational Biology, 2013](plos2013).


### 2012

* [Dunn et al. A Two-Dimensional Model of the Colonic Crypt Accounting for the Role of the Basement Membrane and Pericryptal Fibroblast Sheath. PLoS Computational Biology, 2012](plosdunn2012).


### 2011

* [Cooper, Mirams, Niederer. High throughput functional curation of cellular electrophysiology models. Prog Biophys Mol Biol, 2011](functionalcuration).


----


### Writing paper tutorials

For instructions on how to create a new paper tutorial, see [Writing Paper Tutorials](writingpapertutorials).
