---
title: "State-variable Interpolation"
description: "State-variable Interpolation"
draft: false
images: []
toc: true
layout: "single"
version: "2024.1"
---

State-variable interpolation is an alternative way of computing the ionic
current in tissue simulations, which can improve accuracy, in particular in the
conduction velocity, without too great a loss in efficiency.

## What is State Variable Interpolation (SVI)?

In solving the monodomain/bidomain equations using the finite element method,
the ionic current needs to be evaluated in the interior of the elements [^a]
(onto the quadrature points). Since we store the cell models at the nodes, we
only know the ionic current at the nodes. The obvious approach for computing the
current in the interior of the elements: compute the current at the nodes using
the cell models, and interpolate into the interior. This is the default
behaviour in Chaste, and referred to as *ionic current interpolation (ICI)*.

An alternative approach is to interpolate **all the state variables** from the
cell models ODEs at the nodes, into the interior of the elements. We refer to
this as _state-variable interpolation (SVI)_. This has been shown to have a
surprisingly large effect, especially on conduction velocity, and even on meshes
that are considered high-resolution (100 micrometre spatial resolution) - see
below for a discussion.

## How do I use it?

### Cardiac executable

In the `<Numerical>` part of the XML input file, add

```xml
<UseStateVariableInterpolation>yes</UseStateVariableInterpolation>
```

_after_ the mesh partitioning block. For example:

```xml
<Numerical>
   ...

   <!-- How to partition the mesh when running in parallel -->
   <MeshPartitioning>metis</MeshPartitioning>

   <!-- How to integrate the ionic current term (defaults to no) -->
   <UseStateVariableInterpolation>yes</UseStateVariableInterpolation>

   ...
</Numerical>
```

### Source code

Simply call

```c++
HeartConfig::Instance()->SetUseStateVariableInterpolation();
```

## How does SVI affect computation time, and how is it implemented?

Implementing SVI naively would _massively_ increase computation time (even more
than might originally be expected). Instead, it has been implemented in Chaste
in an efficient manner where SVI is only used on elements around the wavefront.
This slows down computation (in a cell model and problem dependent manner), but
not massively.

For further details on the method, see `[1]`. The form of SVI implemented in
Chaste is what is referred to as the _hybrid_ method in this paper [^b].

## When should it be used?

The paper `[1]` describes in detail the effect of SVI over ICI. In brief

- ICI erroneously decreases conduction velocity on coarse meshes (~500
  micrometres), and can massively decrease CV in the cross-fibre direction
- ICI erroneously _increases_ conduction velocity in the fibre direction on
  mediumly fine meshes (~100 micrometres)
- ICI and SVI give the same results on very fine meshes

We recommend using SVI if refining the mesh would be too costly and either (i)
good CV accuracy is required in the fibre direction (ii) decent cross-fibre CV
accuracy is required in anisotropic simulations.

A recent survey of several cardiac electrophysiology solvers `[2]` used
conduction velocity as a metric for comparison. It should be noted that Chaste
used SVI for the results in this paper. (Without SVI switched on, the Chaste
results would have been similar to the Sundnes et al results in this paper).

One complication that should be noted: the SVI results are closer to the true
finite element solution, which, if the mesh is too coarse, may be oscillatory
around the upstroke. ICI numerically smooths out these oscillations (effectively
two sources of error cancelling out to make the result 'look' more accurate). So
switching on SVI may lead to the action potential looking less accurate, and may
in fact lead to the simulation failing if these oscillations are too large.

## References

`[1]` P. Pathmanathan, G. Mirams, J. Southern, J. Whiteley, "The significant
effect of the choice of ionic current integration method in cardiac
electro-physiological simulations", International Journal for Numerical Methods
in Biomedical Engineering, **27**(11), 1751-1770 (2011)
[link](http://dx.doi.org/10.1002/cnm.1438)

`[2]` S. Niederer et al. "Verification of cardiac tissue electrophysiology
simulators using an N-version benchmark", Royal Society Philosophical
Transactions A, **369**(1954) 4331-4351 (2011)
[link](http://dx.doi.org/10.1098/rsta.2011.0139).

## Footnotes

[^a]: Other solvers use \*operator splitting\* of the reaction term (ionic
current) from the PDEs, for which the ionic current is not required in the
interior. The simplest form of operator splitting (Godunov splitting) is
formally equivalent to ICI. Other forms such as Strang splitting are temporally
different but spatially the same. However, SVI cannot be applied to operator
splitting methods to improve accuracy.

[^b]:
    The criterion for which elements to use SVI on is based on the maximum
    difference in nodal ionic current values, and can be read off from
    `AbstractCorrectionTermAssembler<ELEMENT_DIM,SPACE_DIM,PROBLEM_DIM>::ElementAssemblyCriterion()`
