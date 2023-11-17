---
title : "Cardiac Chaste"
draft: false
images: []
toc: true
---

## Introduction and aims

Computational modelling of the heart is now recognised as a powerful technique in the detailed investigation of cardiac behaviour.
One of the major contributions of computational approaches to cardiovascular research has been the ability to dissect various effects and to tease out important relations between parameters, which are not possible using current experimental techniques.

Recently, advanced computer models of cardiac electro-mechanical activity have been developed.
The electrical properties of the myocardium are generally described by the bidomain equations, a set of coupled parabolic and elliptic partial differential equations (PDEs) that represents the tissue as two separate, distinct continua - one intracellular and the other extracellular.
The intracellular and the extracellular media are connected via the cell membrane, and thus the two PDEs are coupled at each point in space through a set of complex, non-linear ordinary differential equations (ODEs), which describe the ionic transport across the cell membrane.

Certain modelling environments use the monodomain representation of cardiac activity, which involves solving a single parabolic PDE, by assuming either that the extracellular potentials are negligible, or that the anisotropy ratios are equal in the intracellular and the extracellular domains.

Although current cardiac solvers have achieved very good efficiency for particular applications, they all share the following important limitations:
1. they are not generic - they have been developed for specific applications based on the particular scientific interests of the developers;
2. they have not been developed using state-of-the-art software engineering methods, and therefore have not been completely tested and validated;
3. they have not achieved maximum efficiency to run on HPC platforms because they have not been designed for this purpose;
4. they are not freely available to the scientific community; and
5. they do not include state-of-the-art numerical and computational techniques that could speed up the code by several orders of magnitude and would thus allow for full numerical convergence testing (in particular, current simulation tools cannot provide sufficient spatial resolution to test convergence).

The overall objective of the Chaste project is to develop a novel, generic and efficient cardiac software package, accurately tested and validated, and specifically designed to run on large scale, high performance systems such as HPCx and future generations of petascale computers.

The use of advanced software engineering techniques, and close interaction with academic and industrial collaborators as well as with end users, ensures that the resulting software forms a robust, user friendly, production level platform for the investigation of important scientific questions related to cardiac function in health and disease.

We expect this software to support the user community to move on to investigate the next generation of cardiac physiology research.

## User functionality

- Solution of both the monodomain and bidomain equations (including external baths representation).
- Solution of coupled electro-mechanical problems using stable numerical algorithms.
- Automatic implementation of cellular action potential models from the CellML repository (using PyCml).
- Ability to load any tetrahedral mesh (including anatomically-based meshes of any size) and to automatically generate simple geometry meshes (slabs, etc).
- Automatic generation of mathematical model for fibre orientation associated with both anatomically-based and simple geometry meshes.
- Ability to define tissue properties both globally and locally based on XML files (for instance, to describe heterogeneities in ionic current properties)
- Post-processing of simulation results to calculate electrophysiological properties such as action potential duration, conduction velocity, etc.
- Checkpoint of simulations midway through run and restart with altered parameters

## Example simulation results

Cardiac simulations can be viewed on the [Chaste YouTube channel](https://youtube.com/user/ChasteProject).

Output from the s1s2protocol subfolder of the application simulations:
{{< youtube id="q3yIJK4EnUM" title="Output from the s1s2protocol subfolder of the application simulations" >}}

Fibrillation induced by a two-step stimulation protocol (S1-S2) on the 4-million node Oxford Rabbit Heart Mesh:
{{< youtube id="5VY7wpHsezg" title="Fibrillation induced by a two-step stimulation protocol (S1-S2) on the 4-million node Oxford Rabbit Heart Mesh" >}}

Visualisation of propagation through a heart section:
{{< youtube id="-2A--fdaxFo" title="Visualisation of propagation through a heart section" >}}

Adaptive meshing during a bidomain simulation of electrical propagation in the heart:
{{< youtube id="PEKmBiQyAyA" title="Adaptive meshing during a bidomain simulation of electrical propagation in the heart" >}}
