---
title: "PyChaste Tutorials"
description: "PyChaste Tutorials"
draft: false
images: []
layout: "single"
---

It is recommended that you follow the tutorials in the order below.

{{< callout context="note" title="Note" icon="outline/info-circle" >}}

If you are using the [docker image](../installation#docker-image), you should
see a list of tutorials in your browser on launch.

{{< /callout >}}

## Demo Problems

These tutorials demonstrate some applications of biological interest, but do not
discuss functionality in detail.

- [Simulating a Scratch Assay](scratchassay) -- Setting up a simple
  cellular automaton, 3D visualization and real-time plotting.
- [Simulating Spheroid Growth](spheroid) -- Setting up an
  off-lattice cell population and reaction-diffusion PDEs.
- [Simulating an Epithelial Sheet Tensile Test](tensiletest) --
  Setting up a Vertex based cell population and using polymorphism for time
  varying boundary conditions.
- [Simulating Cell Sorting](cellsorting) -- Setting up a Potts based
  simulation and labelling cells.

## Basic Simulations

These tutorials demonstrate basic functionality. They are based on the C++
versions in Chaste. See the [Chaste User Tutorials](../../docs/user-tutorials/)
page for more detailed information.

- [Running Mesh Based Simulations](meshbasedcellsimulations)
  -- The simplest type of cell-based simulation (also the first to be
  implemented in Chaste).
- [Running Node Based Simulations](nodebasedcellsimulations)
  -- Includes details of how to simplify cell-based tests.
-
  [Running Vertex Based Simulations](vertexbasedcellsimulations)
  -- Includes adding boundary conditions and removing cells from simulations.
-
  [Running Potts Based Simulations](pottsbasedcellsimulations)
  -- Lattice-based simulations.
-
  [Running Immersed Boundary Simulations](immersedboundary)
  -- Running simulations using the immersed boundary method.
