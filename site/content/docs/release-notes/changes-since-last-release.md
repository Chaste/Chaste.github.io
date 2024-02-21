---
title : "Changes since last release"
date: 2020-10-06T08:47:36+00:00
draft: false
images: []
toc: true
---



**Users:** If you are working with the develop branch and your local code or project has been broken
by a recent interface change then please see here for fix suggestions.

**Developers:** Please mention any changes to the code which will break users' code here - to be put in the release notes for the next release.  Also mention any significant improvements or new features.  The real definitive release notes will be written in [release notes](../release-notes)  at the time of release.  To make that process easier, please structure this page in the same manner.


## Changes since last release appear below
---

## (changes since Release 2024.1)

### Headline features

### Dependency changes

### Core

### Heart

### Cell Based

#### July 2023
* [#3089](https://github.com/Chaste/trac_archive/blob/master/issues/3077.md) [#142](https://github.com/Chaste/Chaste/issues/142) You can now have voids in bounded voronoi tesselations of cylindrical meshes.

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
* [#3069](https://github.com/Chaste/trac_archive/blob/master/issues/3069.md) You can now output the location (and other information Including the cell killer that removed it) of cell removals by immediate killing or apoptosis. To do this use the new `CellRemovalLocationsWriter`, this will give you the file `removals.dat`. To make sure the information is output you will need to update your cell killer (if not in the core code) to use the helper methods `KillCell()` and `StartApoptosisOnCell()` See [TestCreatingAndUsingANewCellKillerTutorial](../../user-tutorials/creatingandusinganewcellkiller/) for examples.
* [#3069](https://github.com/Chaste/trac_archive/blob/master/issues/3069.md) and [#2578](https://github.com/Chaste/trac_archive/blob/master/issues/2578.md) you can now output the division locations by using the `CellDivisionLocationWriter` (Formatting has been preserved see [#3070](https://github.com/Chaste/trac_archive/blob/master/issues/3070.md))



### Future Plans


### Cell Based
