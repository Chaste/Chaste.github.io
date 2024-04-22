---
title: "PyChaste Tutorials"
description: "PyChaste Tutorials"
draft: false
images: []
layout: "single"
---

It is recommended that you follow the tutorials in the order below.

{{< callout context="note" title="Note" icon="info-circle" >}}

If you are using the [docker image](../installation#docker-image), you should
see a list of tutorials in your browser on launch.

{{< /callout >}}

## Demo Problems

These tutorials demonstrate some applications of biological interest, but do not
discuss functionality in detail.

- [Simulating a Scratch Assay](testscratchassaytutorial) -- Setting up a simple
  cellular automaton, 3D visualization and real-time plotting.
- [Simulating Spheroid Growth](testspheroidtutorial) -- Setting up an
  off-lattice cell population and reaction-diffusion PDEs.
- [Simulating an Epithelial Sheet Tensile Test](testtensiletesttutorial) --
  Setting up a Vertex based cell population and using polymorphism for time
  varying boundary conditions.
- [Simulating Cell Sorting](testcellsortingtutorial) -- Setting up a Potts based
  simulation and labelling cells.

## Basic Simulations

These tutorials demonstrate basic functionality. They are based on the C++
versions in Chaste. See the [Chaste User Tutorials](../../docs/user-tutorials/)
page for more detailed information.

- [Running Mesh Based Simulations](testmeshbasedcellsimulationspythontutorial)
  -- The simplest type of cell-based simulation (also the first to be
  implemented in Chaste).
- [Running Node Based Simulations](testnodebasedcellsimulationspythontutorial)
  -- Includes details of how to simplify cell-based tests.
-
  [Running Vertex Based Simulations](testvertexbasedcellsimulationspythontutorial)
  -- Includes adding boundary conditions and removing cells from simulations.
-
  [Running Potts Based Simulations](testpottsbasedcellsimulationspythontutorial)
  -- Lattice-based simulations.
-
  [Running Immersed Boundary Simulations](testimmersedboundarytutorial)
  -- Running simulations using the immersed boundary method.
