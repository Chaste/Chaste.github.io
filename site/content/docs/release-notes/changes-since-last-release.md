---
title : "Changes since last release"
date: 2020-10-06T08:47:36+00:00
draft: false
images: []
toc: true
---



**Users:** If you are working with the develop branch and your local code or project has been broken
by a recent interface change then please see here for fix suggestions.

**Developers:** Please mention any changes to the code which will break users' code here - to be put in the release notes for the next release.  Also mention any significant improvements or new features.  The real definitive release notes will be written in [release notes](/release-notes/release-notes)  at the time of release.  To make that process easier, please structure this page in the same manner.


## Changes since last release appear below
---

## (changes since Release 2021.1)

### Headline features
* The **Immersed Boundary Method** - a new cell-based modelling paradigm has been added, alongside the existing ones (node, mesh, vertex, Potts, cellular automata).
* **New website** at [https://chaste.github.io/](https://chaste.github.io/), and a new automated build system based on Github actions.
* **New Q&A forum** replaces mailing list for user queries: [https://github.com/Chaste/Chaste/discussions](https://github.com/Chaste/Chaste/discussions)
* **Docker images** for easy install on multiple architectures - see [Docker Readme](https://github.com/Chaste/chaste-docker).

### Dependency changes
* Chaste can now only be built with `cmake` and not our old build system `scons`. Please see [Cmake First Run Guide](/docs/user-guides/cmake-first-run/) for how to swap over.
* Please see [Dependency Versions](/docs/installguides/dependency-versions/) for a list of dependencies that are now supported, and planned to be dropped in the next release.

### Core
* [#153](https://github.com/Chaste/Chaste/pull/153) Mesh generators now return meshes wrapped in a `boost::shared_ptr`. Existing tests that retrieve a mesh from a mesh generator should be rewritten to accept this return type. For example, a test that expected a raw mesh pointer such as `AbstractMesh<2,2>* p_mesh = generator.GetMesh()` should now be changed to `boost::shared_ptr<AbstractMesh<2,2> > p_mesh = generator.GetMesh()`. Use `p_mesh.get()` to get the raw pointer from the smart pointer if needed e.g. in assertions. See `TestRunningMeshBasedCryptSimulationsTutorial` for more examples.
* [#106](https://github.com/Chaste/Chaste/issues/106) [#138](https://github.com/Chaste/Chaste/pull/138)  A change to meshes makes edges first class objects within the mesh.  This is so that quantities can be assigned to edges and, specifically, so that systems of ODEs can be solved on cell-cell boundaries in the cell-based code.
* Many minor C++ modernisation changes have taken place, including [#80](https://github.com/Chaste/Chaste/pull/80) [#108](https://github.com/Chaste/Chaste/pull/108)
### Heart
* CellML files that are [tagged with suitable metadata](/docs/user-guides/code-generation-from-cell-ml/#model-annotation-with-rdf) will automatically generate C++ ODE systems that have checks for things like gating variables/probabilities going outside `[0,1]` or concentrations going negative, and will throw an error when running in debug mode if that happens ([with a suitable tolerance if using CVODE](https://sundials.readthedocs.io/en/latest/cvode/Usage/index.html#advice-on-controlling-unphysical-negative-values)). This uses the [Oxmeta ontology](https://github.com/ModellingWebLab/ontologies) so that you no longer have to manually specify these checks, and anything that the ontology identifies as a gating variable or concentration will get the methods automatically.  See [#46](https://github.com/Chaste/Chaste/issues/46)
* Cmake can fetch cellml files from the repo [Chaste/cellml](https://github.com/Chaste/cellml) at compile time, although a handful of CellML files are still in the main source code for testing. If you want to run with lots of different CellML files, please [see how ApPredict's CmakeLists.txt requests just certain CelLML files](https://github.com/Chaste/ApPredict/blob/2e5f95660609c5e2f8ed21be3b71455a6b1744b2/CMakeLists.txt), the advantage of this is you don't need to clone the whole repo in a submodule and compile all the CellML files any more, but can just get the ones you need.

### Cell Based

#### July 2023
* [#3089](https://github.com/Chaste/trac_archive/blob/master/issues/3077.md) [#142](https://github.com/Chaste/Chaste/issues/142) You can now have voids in bounded voronoi tesselations of cylindrical meshes.
* [#106](https://github.com/Chaste/Chaste/issues/106) [#138](https://github.com/Chaste/Chaste/pull/138)  A change to meshes makes edges first class objects within the mesh.  This is so that quantities can be assigned to edges and, specifically, so that systems of ODEs can be solved on cell-cell boundaries in the cell-based code.
* [#121](https://github.com/Chaste/Chaste/issues/121)  Forces requiring target areas have been streamlined, and this involves a new `CellData::HasItem()` which searches for a given variable.
* [#135](https://github.com/Chaste/Chaste/issues/135) `HoneycombVertexMeshGenerator` fixed to use the argument `isFlatBottom` correctly.

#### June 2023
* [#130](https://github.com/Chaste/Chaste/issues/130) The `Cell` class can now be subclassed and the `Divide` machinery overloaded.
* [#103](https://github.com/Chaste/Chaste/issues/103)  includes new features: `VonMisesVertexBasedDivisionRule BiasedBernoulliTrialCellCycleModel DivisionBiasTrackingModifer ConstantTargetAreaModifier` and `SlidingBoundaryCondition`.
* [#13](https://github.com/Chaste/Chaste/pull/13) [#3089](https://github.com/Chaste/trac_archive/blob/master/issues/3089.md) Properties of halo nodes with cylindrical meshes can now be changed.

#### May 2023
* [#95](https://github.com/Chaste/Chaste/issues/95) A bug associated with creating large bounding boxes for the `NodesOnlyMesh` has been identified and fixed.


#### April 2022
* [#3077](https://github.com/Chaste/trac_archive/blob/master/issues/3077.md) You can now add new and remove ghost nodes from mesh based tissue simulations.
* [#3078](https://github.com/Chaste/trac_archive/blob/master/issues/3078.md) You can now bound the bound the Voronoi Tessellation's on Cylindrical and Toroidal meshes.

#### September 2021
* [#3076](https://github.com/Chaste/trac_archive/blob/master/issues/3076.md) you can now output the underlying mesh during simulations with `MeshBasedPopulationWithGhostNodes` use `SetWriteVtkAsPoints(true)`.
* [#3043](https://github.com/Chaste/trac_archive/blob/master/issues/3043.md) added a `Toroidal2dMesh` which allows 2d mesh based simulations (with or without ghost nodes) with periodicity in x and y.

#### August 2021
* [#3071](https://github.com/Chaste/trac_archive/blob/master/issues/3071.md) Can now bound the voronoi tesselation in mesh based simulations by using the method `SetBoundVoronoiTessellation(true)` on the cell population. This works by creating a finite voronoi tesselation for each bounday cell, as described in Appendix A of [https://doi.org/10.1007/s11538-023-01214-8](https://doi.org/10.1007/s11538-023-01214-8). The extra nodes (used to bound the Voronoi Tesselation) are placed 1CD away from the tissue boundary to maintian an approximate voronoi cell diameter of 1CD.
* [#3071](https://github.com/Chaste/trac_archive/blob/master/issues/3071.md) You can now output both the Voronoi tesselation (add `VoronoiDataWriter`) and mesh (`SetWriteVtkAsPoints(true)`) in mesh based simulations, the output files are now `voronoi_results_xxx.vtu` and `mesh_results_xxx.vtu`.

#### July 2021
* [#3069](https://github.com/Chaste/trac_archive/blob/master/issues/3069.md) You can now output the location (and other information Including the cell killer that removed it) of cell removals by immediate killing or apoptosis. To do this use the new `CellRemovalLocationsWriter`, this will give you the file `removals.dat`. To make sure the information is output you will need to update your cell killer (if not in the core code) to use the helper methods `KillCell()` and `StartApoptosisOnCell()` See [TestCreatingAndUsingANewCellKillerTutorial](docs/user-tutorials/creatingandusinganewcellkiller/) for examples.
* [#3069](https://github.com/Chaste/trac_archive/blob/master/issues/3069.md) and [#2578](https://github.com/Chaste/trac_archive/blob/master/issues/2578.md) you can now output the division locations by using the `CellDivisionLocationWriter` (Formatting has been preserved see [#3070](https://github.com/Chaste/trac_archive/blob/master/issues/3070.md))

