---
title : "Release notes"
description: "Release notes"
lead: "All previous release notes"
date: 2020-10-06T08:47:36+00:00
draft: false
images: []
toc: true
---

## Release 2024.1 (changes since Release 2021.1)

### Headline features
* The **Immersed Boundary Method** - a new cell-based modelling paradigm has been added, alongside the existing ones (node, mesh, vertex, Potts, cellular automata).
* **New website** at [https://chaste.github.io/](https://chaste.github.io/), and a new automated build system based on Github actions.
* **New Q&A forum** replaces mailing list for user queries: [https://github.com/Chaste/Chaste/discussions](https://github.com/Chaste/Chaste/discussions)
* **Docker images** for easy install on multiple architectures - see [Docker Readme](https://github.com/Chaste/chaste-docker).

### Dependency changes
* Chaste can now only be built with `cmake` and not our old build system `scons`. Please see [Cmake First Run Guide](../../user-guides/cmake-first-run/) for how to swap over.
* Please see [Dependency Versions](../../installguides/dependency-versions/) for a list of dependencies that are now supported, and planned to be dropped in the next release.

### Core
* [#153](https://github.com/Chaste/Chaste/pull/153) Mesh generators now return meshes wrapped in a `boost::shared_ptr`. Existing tests that retrieve a mesh from a mesh generator should be rewritten to accept this return type. For example, a test that expected a raw mesh pointer such as `AbstractMesh<2,2>* p_mesh = generator.GetMesh()` should now be changed to `boost::shared_ptr<AbstractMesh<2,2> > p_mesh = generator.GetMesh()`. Use `p_mesh.get()` to get the raw pointer from the smart pointer if needed e.g. in assertions. See `TestRunningMeshBasedCryptSimulationsTutorial` for more examples.
* [#106](https://github.com/Chaste/Chaste/issues/106) [#138](https://github.com/Chaste/Chaste/pull/138)  A change to meshes makes edges first class objects within the mesh.  This is so that quantities can be assigned to edges and, specifically, so that systems of ODEs can be solved on cell-cell boundaries in the cell-based code.
* Many minor C++ modernisation changes have taken place, including [#80](https://github.com/Chaste/Chaste/pull/80) [#108](https://github.com/Chaste/Chaste/pull/108)

### Heart
* CellML files that are [tagged with suitable metadata](../../user-guides/code-generation-from-cellml/#model-annotation-with-rdf) will automatically generate C++ ODE systems that have checks for things like gating variables/probabilities going outside `[0,1]` or concentrations going negative, and will throw an error when running in debug mode if that happens ([with a suitable tolerance if using CVODE](https://sundials.readthedocs.io/en/latest/cvode/Usage/index.html#advice-on-controlling-unphysical-negative-values)). This uses the [Oxmeta ontology](https://github.com/ModellingWebLab/ontologies) so that you no longer have to manually specify these checks, and anything that the ontology identifies as a gating variable or concentration will get the methods automatically.  See [#46](https://github.com/Chaste/Chaste/issues/46)
* Cmake can fetch cellml files from the repo [Chaste/cellml](https://github.com/Chaste/cellml) at compile time, although a handful of CellML files are still in the main source code for testing. If you want to run with lots of different CellML files, please [see how ApPredict's CmakeLists.txt requests just certain CelLML files](https://github.com/Chaste/ApPredict/blob/2e5f95660609c5e2f8ed21be3b71455a6b1744b2/CMakeLists.txt), the advantage of this is you don't need to clone the whole repo in a submodule and compile all the CellML files any more, but can just get the ones you need.

### Cell Based

* [#3089](https://github.com/Chaste/trac_archive/blob/master/issues/3077.md) [#142](https://github.com/Chaste/Chaste/issues/142) You can now have voids in bounded voronoi tesselations of cylindrical meshes.
* [#106](https://github.com/Chaste/Chaste/issues/106) [#138](https://github.com/Chaste/Chaste/pull/138)  A change to meshes makes edges first class objects within the mesh.  This is so that quantities can be assigned to edges and, specifically, so that systems of ODEs can be solved on cell-cell boundaries in the cell-based code.
* [#121](https://github.com/Chaste/Chaste/issues/121)  Forces requiring target areas have been streamlined, and this involves a new `CellData::HasItem()` which searches for a given variable.
* [#135](https://github.com/Chaste/Chaste/issues/135) `HoneycombVertexMeshGenerator` fixed to use the argument `isFlatBottom` correctly.
* [#130](https://github.com/Chaste/Chaste/issues/130) The `Cell` class can now be subclassed and the `Divide` machinery overloaded.
* [#103](https://github.com/Chaste/Chaste/issues/103)  includes new features: `VonMisesVertexBasedDivisionRule BiasedBernoulliTrialCellCycleModel DivisionBiasTrackingModifer ConstantTargetAreaModifier` and `SlidingBoundaryCondition`.
* [#13](https://github.com/Chaste/Chaste/pull/13) [#3089](https://github.com/Chaste/trac_archive/blob/master/issues/3089.md) Properties of halo nodes with cylindrical meshes can now be changed.
* [#95](https://github.com/Chaste/Chaste/issues/95) A bug associated with creating large bounding boxes for the `NodesOnlyMesh` has been identified and fixed.
* [#3077](https://github.com/Chaste/trac_archive/blob/master/issues/3077.md) You can now add new and remove ghost nodes from mesh based tissue simulations.
* [#3078](https://github.com/Chaste/trac_archive/blob/master/issues/3078.md) You can now bound the bound the Voronoi Tessellation's on Cylindrical and Toroidal meshes.
* [#3076](https://github.com/Chaste/trac_archive/blob/master/issues/3076.md) you can now output the underlying mesh during simulations with `MeshBasedPopulationWithGhostNodes` use `SetWriteVtkAsPoints(true)`.
* [#3043](https://github.com/Chaste/trac_archive/blob/master/issues/3043.md) added a `Toroidal2dMesh` which allows 2d mesh based simulations (with or without ghost nodes) with periodicity in x and y.
* [#3071](https://github.com/Chaste/trac_archive/blob/master/issues/3071.md) Can now bound the voronoi tesselation in mesh based simulations by using the method `SetBoundVoronoiTessellation(true)` on the cell population. This works by creating a finite voronoi tesselation for each bounday cell, as described in Appendix A of [https://doi.org/10.1007/s11538-023-01214-8](https://doi.org/10.1007/s11538-023-01214-8). The extra nodes (used to bound the Voronoi Tesselation) are placed 1CD away from the tissue boundary to maintian an approximate voronoi cell diameter of 1CD.
* [#3071](https://github.com/Chaste/trac_archive/blob/master/issues/3071.md) You can now output both the Voronoi tesselation (add `VoronoiDataWriter`) and mesh (`SetWriteVtkAsPoints(true)`) in mesh based simulations, the output files are now `voronoi_results_xxx.vtu` and `mesh_results_xxx.vtu`.
* [#3069](https://github.com/Chaste/trac_archive/blob/master/issues/3069.md) You can now output the location (and other information Including the cell killer that removed it) of cell removals by immediate killing or apoptosis. To do this use the new `CellRemovalLocationsWriter`, this will give you the file `removals.dat`. To make sure the information is output you will need to update your cell killer (if not in the core code) to use the helper methods `KillCell()` and `StartApoptosisOnCell()` See [TestCreatingAndUsingANewCellKillerTutorial](../../user-tutorials/creatingandusinganewcellkiller/) for examples.
* [#3069](https://github.com/Chaste/trac_archive/blob/master/issues/3069.md) and [#2578](https://github.com/Chaste/trac_archive/blob/master/issues/2578.md) you can now output the division locations by using the `CellDivisionLocationWriter` (Formatting has been preserved see [#3070](https://github.com/Chaste/trac_archive/blob/master/issues/3070.md))



## Release 2021.1 (changes since Release 2019.1)

### Headline features

* Chaste has now been **updated to Python3 (3.5+)**.
    * New dependencies (which most systems will already have):
        * python3
        * python3-venv
        * python3-pip
    * The following Python2 dependencies are no longer required:
        * python-devel
        * python-lxml
        * python-amara
        * python-rdflib
        * python-dateutil
    * Chaste now supports Ubuntu 20.04 LTS (Focal).


### New dependency support


* Chaste now supports PETSc up to 3.12, Boost up to 1.74, SUNDIALS up to 4.1.0 and VTK up to 8.2.


### Core

### Heart

* The CellML to Chaste hpp/cpp converter was `PyCML` (based on Python 2) this has been replaced by `chaste_codegen` (https://github.com/ModellingWebLab/chaste-codegen, based on Python 3). See ChasteGuides/CodeGenerationFromCellML for info on how to use this new library at the command line, but no changes needed unless you were using PyCML manually before. There are a couple of nice new features with this:
    * You no longer need to manually use the proprietary software Maple to compute Analytic Jacobians for CVODE to get speed ups, we now use the free software [SymPy](https://www.sympy.org/en/index.html) behind the scenes to do this on the fly. **N.B. these are now generated and used automatically, but are known to cause issues in a handful of models, so use the `ForceUseOfNumericalJacobian()` method if CVODE errors suddenly appear and you hadn't heard of using Maple or analytic Jacobians before. See https://chaste.cs.ox.ac.uk/trac/wiki/UserTutorials/SingleCellSimulation for more info.**
    * We now automatically analyse your model to detect singularities in [GHK equations](https://en.wikipedia.org/wiki/Goldman%E2%80%93Hodgkin%E2%80%93Katz_flux_equation), and apply an interpolation fix so that they don't cause any problems at the voltages of concern (often, but not always, V=0). From now on, **manual fixes for these singularities should be removed from CellML files**. We'll be writing a note on how exactly we've done this, but you can examine the results of the fixes [here](https://github.com/ModellingWebLab/chaste-codegen/blob/assets/singularity_fixes.md) for a range of models (grey=original, red=fix, orange shaded region=voltage range where interpolation is used). As a nice side-effect, lookup tables no longer need to go from offset voltages like -150.00001mV to 100.00001mV to avoid hitting these singularities, and have been moved to nice round numbers!


### Cell Based

* You can now specify any dimension to have a periodic boundary condition in 3-D `NodeBased` simulations. This also works in parallel.  See for example `TestOffLatticeSimulationWithNodeBasedCellPopulationIn3d::TestSimple3dTissueYPeriodic`





* Fixed to output of cell proliferative type to stop this output being overwritten by mutations state or label id.



* Bug fix on daughter cell placement in off-lattice centre-based simulations. Daughter cells are now correctly placed equal distances from the parent cell centre location.



* Changes to performance and correctness of `VertexBased` code.
    * Bug in `MutableVertexMesh::PerformIntersectionSwap()` working at boundary of `VertexMesh` found and fixed. Previous code expected there to be four elements surrounding the intersection whereas, at the boundary, there are several other cases.
    * Bug fix to `MutableVertexMesh::PerformT2Swap()` in the case where a small triangular element has no neighbours.
    * Performance optimization to `MutableVertexMesh::CheckForIntersections()`.


### Future Plans

This will be the last release of Chaste to support Ubuntu 16.04 LTS and its dependencies. The following will not be supported in future releases:


* Boost < 1.65.1
* CMake < 3.10.2
* HDF5 < 1.10.0
* PETSc < 3.7.7
* VTK < 6.3.0
* Xerces < 3.2.0
* SUNDIALS < 2.7.0



## Release 2019.1 (changes since Release 2018.1)

### Headline features


* Chaste is now compiled with [C++14](https://en.wikipedia.org/wiki/C%2B%2B14).
* Chaste now supports up to and including Ubuntu 19.04 (Disco).
* The minimum required CMake version for building Chaste is now 3.5.1.
* Installing Chaste is now even easier using the new [docker image for Chaste](https://github.com/Chaste/chaste-docker).


### New dependency support


* Chaste now supports PETSc up to 3.11, Boost up to 1.70, HDF5 up to 1.10.5, Xerces up to 3.2.2, SUNDIALS up to 3.1.0 and VTK up to 8.1.
* Chaste no longer supports PETSc < 3.6, Boost < 1.58, HDF5 < 1.8.16, XSD < 4.0.0, Xerces < 3.1.3, SUNDIALS < 2.5.0 and VTK < 6.2.


### Core


* Two new CMake build types have been added: `AggressiveOpt` which sets `-Ofast -march=native -DNDEBUG` and is good for release builds with more aggressive optimisation, and `DebugOpt` which sets `-Og -g` and is a good default for an edit-compile-debug workflow.
    * `TestChasteBuildInfo.hpp` is now displaying correct information for C++ compiler flags for both cmake and the old scons build system.
* Dropping support for XSD 3.x should prevent Chaste builds from emitting warnings about deprecated `std::auto_ptr`.
* The `docs` directory has been refactored to contain more relevant information, and now includes a [JOSS](https://joss.theoj.org/) paper about Chaste and recent publications it has enabled.
* The unused interface ` Hdf5DataWriter::DefineFixedDimensionUsingMatrix()` was **deleted**.

### Heart

* Intracellular calcium is now converted consistently into milliMolar within the action potential models and so the method `AbstractCardiacCellInterface::GetIntracellularCalciumConcentration()` (used by mechanics models) always returns calcium in milliMolar. Note that this has changed the state variable ordering in the PyCML-generated C++ models, so any archives of these variables will need to be updated.
* Tweaks to `SteadyStateRunner` class which might provide a speed-up for getting certain action potential models to steady state, by removing maximum time step from CVODE and solving separately during stimulus and non-stimulus regions.
* The behaviour of `AbstractCardiacProblem<>::SetOutputNodes()` and `SingleTraceOutputModifier` has been altered. When running in parallel node indices into the original mesh are now automatically converted to indices into then permuted runtime mesh.


### Future Plans


* This is the last release of Chaste to support Xerces < 3.1.2.


## Release 2018.1 (changes since Release 2017.1)

### Headline features


* Chaste now supports Ubuntu 18.04 LTS (Bionic).


### New dependency support


* Chaste now supports Boost 1.66 and 1.67 (boosts 1.64 and 1.65 are a bit buggy for us and should be avoided if possible).
* Chaste now supports CVODE (Sundials versions) 3.0.0 and 3.1.0.
* Chaste now supports HDF5 versions 1.8.20 and 1.10.2.
* Chaste now supports PETSc versions 3.8 and 3.9.
* Chaste now supports VTK version 8.1.
* Chaste now supports Xerces versions 3.2.0 and 3.2.1.


### Core

* CVODE 3.0.0 has changed its interface for analytic Jacobians, dropping the `long int N` that was the first argument. We have followed suit in Chaste's `AbstractCvodeSystem::EvaluateAnalyticJacobian()` method, so **this may break user projects** if you have your own CVODE systems which override this method. To fix this just delete the argument and get the size directly from the vectors if you need it.


### Future Plans
This will be the last release of Chaste to support Ubuntu 14.04 LTS and its dependencies. The following will not be supported in future releases:

* Boost < 1.58
* CMake < 3.5
* HDF5 < 1.8.16
* Parmetis < 4.0
* PETSc < 3.6
* VTK < 6.2
* XSD < 4.0


## Release 2017.1 (changes since Release 3.4)

### Headline features


* Chaste's build system has moved from `scons` to `cmake` (although `scons` will work with this release, it may not be supported in future).
* Chaste now uses C++11 rather than C++98, and users and developers can begin to use the new features introduced in C++11.
* We have updated support for dependencies and new compilers, up to gcc 7.2, intel 17 and clang 5.0. Chaste 2017.1 is compatible with all Ubuntus up to 17.10 that are still in support.
* We have changed our version control system (from `svn` to `git`), which allows users more flexibility in choosing the stability of their Chaste version. Releases such as this are the most stable, but a host of other options now available, and listed at ChasteGuides/ExternalDeveloperGuide. The repository is mirrored at https://github.com/Chaste/Chaste.
* Chaste no longer supports cmake < 2.8.12, scons, PETSc < 3.4, Boost < 1.54, HDF5 < 1.8.11, XSD < 3.3, Xerces < 3.1.1, Sundials < 2.5.0, and VTK < 5.8, as these were dropped with Ubuntu 12.04.


### New functionality & code changes

#### Cell-based

* Member variables have been added to `NodeAttributes` to store neighbouring nodes, speeding up node-based simulations by a factor of between 2 and 3.
* Improvements to vertex robustness and speed:
    * The method `GetShortAxisOfElement()` has made more robust to cell size.
    * A member variable `mDistanceForT3SwapChecking` has been added to `MutableVertexMesh`, which can be used to speed up vertex model simulations with a free boundary.
    * The restriction on vertex displacements at each timestep of vertex model simulations has been made optional by the addition of a member variable `mRestrictVertexMovement` to `VertexBasedCellPopulation`.
* Some cell-cycle models have been renamed (`AbstractSimpleGenerationBasedCellCycleModel` to `AbstractSimpleGenerationalCellCycleModel`, `ExponentiallyDistributedStochasticDurationGenerationBasedCellCycleModel` to `ExponentialG1GenerationalCellCycleModel`, `FixedDurationGenerationBasedCellCycleModel` to `FixedG1GenerationalCellCycleModel`, `GammaDistributedStochasticDurationCellCycleModel` to `GammaG1CellCycleModel`, `StochasticDurationCellCycleModel` to `UniformCellCycleModel`, `StochasticDurationGenerationBasedCellCycleModel` to `UniformG1GenerationalCellCycleModel`).
* The cell-cycle model hierarchy has been refactored to allow models with no phase, with new classes `AbstractOdeBasedPhaseBasedCellCycleModel`, `AbstractPhaseBasedCellCycleModel`, `BernoulliTrialCellCycleModel`, `FixedSequenceCellCycleModel`, and `NoCellCycleModel` added.
* `DiagonalVertexBasedDivisionRule` has been renamed to `FixedVertexBasedDivisionRule`, and new cell division rules `AbstractCentreBasedDivisionRule`, `FixedCentreBasedDivisionRule`, `RandomDirectionCentreBasedDivisionRule`, and `ShovingCaBasedDivisionRule` have been added.
* Several methods for adding and removing update rules have changed location and name (e.g. `AddUpdateRule()`, `RemoveAllUpdateRules()` and `GetUpdateRuleCollection()`).
* Off-lattice models now allow for numerical integration schemes other than Forward Euler to be specified (see `AbstractNumericalMethod` and subclass).
* A bug relating to archiving of cell-based simulations has been fixed.
* Node attributes are now correctly copied upon mesh creation and cell division events in centre-based models.
* A new class `CellDataWriter` and method `OffLatticeSimulation::rGetForceCollection()` have been added.
* Labelled cells now by default have the default damping constant, not the mutant damping constant.
* To streamline the cell-based code, the methods `GetDefaultTimeStep()`, `WriteCellPopulationDataToVisualizerSetupFile()`, `WriterForceDataToVisualizerSetupFile()`, `CopySrnModelVariables()` and `SimulationSetupHook()` have been added.
* Target area modifiers are now permitted on non-vertex-based models.
* A profiling test has been added for 3D node-based simulations.




#### Cardiac

* The `CellProperties` postprocessing class can now return the times at which peak voltages occurred during each action potential.
* Mesh partitioning now defaults to parMETIS:
    * Use of METIS for mesh partitioning is deprecated - the code will drop through to parMETIS with a warning.
    * When the PETSc/partitioner is not available the code will also drop through to parMETIS with a warning (previously the drop-through in this case was to a dumb mesh partition).
* HDF5 output changes:
    * `Hdf5DataWriter` can now cache writes (to whole chunks), improving performance with high-latency I/O systems (i.e. in HPC systems). It can be enabled in cardiac problems with `SetUseHdf5DataWriterCache()`.
    * HDF5 writer chunk size & alignment parameters can now be set from cardiac problems using `<whatever>Problem.SetHdf5DataWriterTargetChunkSizeAndAlignment(...)`. This is useful, for example, on a striped filesystem where setting this method with the stripe size (in bytes) will mean chunks fit into and align with the stripes, resulting in best performance.
* A bug in the `CellProperties` APD calculation has been fixed, it was reporting spuriously large action potential durations in the event that a sub-threshold AP preceded a super-threshold AP.
* Some extra `NodeAttributes` been added (see "Cell-based" above) which have increased the memory footprint of large tissue simulations by about 0.5%, unlikely to be a problem for anyone, but mentioned here in case!
* We are unable to support and distribute a cardiac "standalone" executable.  Users who rely on it should understand that this functionality is still available but that the executable must be compiled from source.


#### Core

* The box collection classes have been refactored:
    * `BoxCollection` renamed to `ObsoleteBoxCollection`, which will be deprecated once functionality (including arbitrary periodicity) has been included in the default class (`DistributedBoxCollection`).
    * Methods `GetLocalBoxes()` have been renamed `rGetLocalBoxes()`.
* A Chaste docker file has been added.
* The `Identifiable->GetIdentifier()` method has been made more robust to segmentation faults.


### Future Plans
From now on we intend to follow the Ubuntu 6 monthly release schedule, tagging our `master` branch once it contains support for the latest Ubuntu.

## Release 3.4 (changes since Release 3.3)

### Headline features

#### General

* Support for Ubuntu up to 15.10 added. We aim to ensure compatibility for any Ubuntu that has not reached 'end of life'.
* Support for Boost up to 1.60 added.
* See InstallGuides/DependencyVersions for all supported versions of dependencies.
* The CMake builder has been extended to support compilation on Windows, Linux and Mac OS X with a range of compilers.  This is part of a planned migration to a unified build system on all platforms.


#### Cardiac

* A new class `AbstractCvodeCellWithDataClamp` allows the 'data clamp' proposed by [Dokos & Lovell (2004)](http://www.ncbi.nlm.nih.gov/pubmed/15142755) to be applied to any CellML model. Models inheriting from this class can be generated with `ConvertCellModel.py --cvode-data-clamp`.
* This is the last release of Chaste for which a pre-built cardiac *standalone executable* can be bundled.


#### Cell-based

* We have improved functionality for outputting results of cellular automaton (CA) and cellular Potts model simulations, as well as cell-based simulations on periodic domains, to VTK.
* We have extended functionality for CA simulations, including a new location "switching" rule and division rule class hierarchies.
* Each cell now contains a "subcellular reaction network model" as well as a cell-cycle model.  This mainly affects users of the `DeltaNotchCellCycleModel` class, which is now implemented using the `DeltaNotchSrnModel`, allowing the model to be coupled with any of the cell cycle models (see [UserTutorials/CreatingAndUsingANewSrnModel](../../user-tutorials/creatingandusinganewsrnmodel) for details).
* Much of the vertex model code has been refactored to improve efficiency. In addition, two new classes, `MutableVertexMeshWithRosettes` and `CellRosetteRankWriter`, have been added to implement the necessary functionality for simulating multicellular 'rosettes' (where more than three cells meet at a point).


#### Lung

* A new package for investigating ventilation in the lung using reduced dimensional models has been introduced.
* Key classes are
   1. `MultiLobeAirwayGenerator` allows anatomical models of the conducting airways to be created.
   2. `AbstractVentilationProblem` and related subclasses allow simulation of airflow on the conducting airway models using a Poiseuille flow model model with Pedley correction.
   3. `DynamicVentilationProblem` couples nonlinear elastic models of the acini (gas exchange area) to the ventilation model, allowing simulation of the full breathing cycle
* Tutorials for this functionality are available on the tutorials page UserTutorials#LungChaste.



### New functionality & code changes
New functionality and code changes, which may require changes to user code.

#### General


* An element argument has been added to `AbstractLinearParabolicPde::ComputeSourceTerm()`. If you have your own PDEs inheriting from `AbstractLinearParabolicPde` this argument will need adding to the method (it can be ignored), see e.g. [relevant change to the heat equation](https://chaste.cs.ox.ac.uk/trac/changeset?new=23885%40trunk%2Fpde%2Ftest%2Fpdes%2FHeatEquationWithSourceTerm.hpp&old=23343%40trunk%2Fpde%2Ftest%2Fpdes%2FHeatEquationWithSourceTerm.hpp).


#### Cardiac

* Classes inheriting from `AbstractCardiacCellWithModifiers` can now be archived/checkpointed.
* We have renamed the CellML metadata `leakage_current` to `membrane_leakage_current` as there is also an SR one sometimes... **This may break user projects using this metadata**. There have also been other updates to the metadata which will enable more advanced features in future versions.
* A light-weight output modifier allows the user to output specific traces during a simulation rather than at post-process time.  See ChasteGuides/HowTo#Output.
* A bug has been found in one method for partitioning of meshes in parallel code (Windows only).  This method has been switched off while we investigate further.


#### Cell-based

* A new tutorial ([UserTutorials/CreatingAndUsingANewCellBasedSimulationModifier](../../user-tutorials/creatingandusinganewcellbasedsimulationmodifier)) shows how to create and use cell-based simulation modifiers.
* The new class `VoronoiVertexMeshGenerator` uses Lloyd's Relaxation steps to generate random initial conditions for vertex model simulations.
* The `PlaneBasedBoundaryCondition` class can be used in a simulation where `ELEMENT_DIM != SPACE_DIM`.
* Two new force classes, `DiffusionForce` and `DifferentialAdhesionGeneralisedLinearSpringForce`, have been added.
* The new class `CellVecData` enables a vector (e.g. the solution to an intracellular PDE problem) to be associated with each cell.
* The default parameter values in `NagaiHondaForce` match those in the original publication.
* Two new writer classes, `CellDeltaNotchWriter` and `CellPopulationAdjacencyMatrixWriter`, have been added.



### Future Plans

* This is the last release of Chaste that will:
    * support Ubuntu 10.04 LTS;
    * support versions of PETSc < 3.0, or boost < 1.48;
    * bundle a pre-built cardiac *standalone executable* (the executable is dependent on third-party libraries which are to be deprecated).
* Work is progressing on switching the build infrastructure to use CMake and code repository to use Git.
    * The CMake build is available to test in this release; see ChasteGuides/CmakeBuildGuide for more details. (SCons will be deprecated at a later date.)
    * The switch of the code repository from Subversion to Git will happen after this release.  For information on migrating please see [GitMigration](https://chaste.cs.ox.ac.uk/chaste/tutorials/release_3.4/ChasteGuides/GitMigration.html).





## Release 3.3 (changes since Release 3.2)

This release is designed to coincide with several publications that have associated code projects, including [PaperTutorials/Frontiers2014](https://github.com/Chaste/trac_archive/wiki/Paper-Tutorials-_-Frontiers2014) and others under review; see [PaperTutorials](https://github.com/Chaste/trac_archive/wiki/Paper-Tutorials) for the latest list.
It also includes support for new library versions that have been released since Chaste 3.2, and for the latest version of Ubuntu.

### Headline features

#### General

* A new run time flag `-citations [file]` was implemented that generates a list of BibTeX-format citations for the libraries/algorithms used in a particular run. With no arguments the citations are printed to std::cout. With an optional argument they are printed to a file on disk (note: a relative or absolute path may be given but the directory must exist and be writeable).
* Chaste works with most recent PETSc versions up to and including PETSc 3.5.
* Recent releases of Boost (1.56 and newer) are now supported, and support for versions prior to 1.40 has been dropped.
* CodeSynthesis XSD version 4.0 is now supported.
* Ubuntu Utopic (14.10) is now supported.


#### Cardiac

* Meshalyzer output is now off by default, as more people are using VTK. It can be turned back on with `HeartConfig::Instance()->SetVisualizeWithMeshalyzer()`.
* A human heart mesh has been added to our public data repository: https://chaste.cs.ox.ac.uk/trac/browser/data/public


#### Cell-based

* The re-factoring of the way cell populations write data to file, begun in the last release, has been further refined. See below for more details.


### Major new functionality & code changes

#### General

* PETSc 3.5 support has been added. If you have been solving nonlinear systems with your own Jacobian matrices, then the method interface needs to change to work with PETSc 3.5. The commit r22721 gives lots of examples of how to do this.
* In Boost 1.56 the algorithm for generating normal random numbers has changed, to fix a bug in earlier Boost versions. Chaste now uses that algorithm across all Boost versions, giving consistent results, but this means **random numbers have changed from previous Chaste releases**, and this may change simulation results.


#### Cardiac

* The formulation for extended biodomain (tridomain) has been changed from solving for voltages (3 phi variables at each point in space) to transmembrane potentials (1 phi and 2 V_m variables at each point in space).  The new matrix formulation is symmetric and hence faster linear solvers (conjugate gradient) are now used by default. Checkpointing is backward compatible.
* The list of Oxford CellML metadata has been moved to a new file `oxford-metadata.ttl`, see [CodeGenerationFromCellML](https://chaste.cs.ox.ac.uk/trac/wiki/ChasteGuides/CodeGenerationFromCellML#Standardisednames) for more details.
* Lookup table settings can take advantage of automatic units conversion.
* A new lightweight output class has been added as an addition (or replacement) to HDF5 output and post-processing. There are currently two concrete implementations: class:SingleTraceOutputModifier which outputs time and voltage(s) at a single node to a named file during the simulation and ​class:ActivationOutputModifier which computes a limited number of activation/recovery times at every node with results being written to file at the end of the simulation.


#### Cell-based

* The method `OutputSimulationModifierParameters()` has been added to the simulation modifier class hierarchy. This is pure virtual in `AbstractCellBasedSimulationModifier` so must be provided by subclasses.
* For clarity, `CellLocationWriter` and `CellVariablesWriter` have been renamed to `CellLocationIndexWriter` and `CellCycleModelProteinConcentrationsWriter` respectively; their associated output filenames and VTK cell data names have also been updated.
* Writers which involve total counts of cells (`CellMutationStatesCountWriter`, `CellProliferativeTypesCountWriter` and `CellProliferativePhasesCountWriter`) form a new subclass which behaves differently to the `CellPopulationWriter` class.  They should be added to the population with `AddCellPopulationCountWriter<>()`.


### Minor
New functionality and code changes, which may still require changes to user code.

#### General

* Code timing should now be done with the class:Timer, rather than manual calls to `std::clock` or `MPI_Wtime`.
* Updated random normal distribution sampling using `RandomNumberGenerator` - it has been altered to match the results from the latest boost (no matter what version of boost you are using): a small bug fix introduced in boost 1.56.
* Fixed a bug in reseeding random normal numbers. If you had called a random normal distribution sample an odd number of times, the first number you got after reseeding was what the next one should have been before reseeding.
* We have replaced all occurrences of `PetscTruth` with `PetscBool`. New code should be written to use the newer type (`PetscBool`).
* Some new utility methods have been added: `OutputFileHandler::GetRelativePath`, `PetscTools::IsInitialised`, `FileComparison::IgnoreBlankLines`


#### Cardiac

* If using many different cell models with lookup tables, the memory used could become excessive. A new `FreeMemory()` method has been added to the class:AbstractLookupTableCollection class for releasing memory when a particular cell model is no longer needed. Note that if you are just using multiple instances of the same cell model there is no need for this, as the lookup tables are shared between instances.
* Running a parallel cardiac simulation on more processes than suitable for the size of the problem now produces an error which terminates the simulation (rather than a warning). This is to avoid potential deadlock later in the run.
* There is a new method `SetSolver()` on class:AbstractCardiacCellInterface, and a method `HasAnalyticJacobian` on class:AbstractCvodeSystem.
* The class:CellMLLoader now copies `.out` files if present, meaning it can generate analytic Jacobians for CVODE.
* When using CVODE in tissue simulations we now perform a reset on the rare occasions that it fails to solve.
* Added (somewhat slow) support for lookup tables in generalised Rush-Larsen models.


#### Cell-based

* There's now a new `AbstractCellBasedWithTimingsTestSuite` which uses `Timer`, and then calls the normal `AbstractCellBasedTestSuite` `setUp` and `tearDown` methods.
* There's now a `ReturnSimulationModifiers` method (on the simulation) to return the vector of simulation modifiers.
* The redundant `VertexElementMap` input argument has been removed from the `MutableVertexMesh` methods `CheckForSwapsFromShortEdges()` and `IdentifySwapType()`.


### Future Plans

* Tested support for various older versions of third party libraries will likely be dropped in the next release. See InstallGuides/DependencyVersions for up-to-date information as development progresses.


-----
## Release 3.2 (changes since Release 3.1)

This is a minor release, but includes new support for many recent versions of dependencies, wider cross-platform support, and a large number of fixes and small performance improvements in both cardiac and cell-based components. We recommend upgrading from any prior version of Chaste to 3.2.

### Headline features

#### General

* The non-cardiac portions of Chaste have now been ported to Windows.  See InstallGuides/Windows for install and usage instructions.
* Chaste has been ported to Mac OS X and continuous integration tests are performed on OS X v10.8 "Mountain Lion".
* The Ubuntu package now also supports up to Trusty Tahr (14.04 Long-Term Support edition).
* Chaste works with most recent PETSc versions up to and including PETSc 3.4.
* Chaste works with most recent VTK versions up to and including VTK 6.1.
* Chaste works with most recent Boost versions up to and including Boost 1.54.
* We no longer test Chaste on a 32-bit machine, so some tests may fail if run in a 32-bit context. We no longer provide a 32-bit stand-alone cardiac executable.
* We now allow access to the latest development version of the code (see ChasteGuides/AccessCodeRepository), provide resources for external developers (see ChasteGuides/ExternalDeveloperGuide), and allow public registration on the trac wiki to view and open 'tickets'.
* Chaste includes a CITATION.txt file for easy citation.


#### Cardiac

* Analytic Jacobians can now be auto-generated for cardiac cell models, using maple, and used by CVODE solvers to provide between 5-30% speed up in ODE solving. These can be used in single cell and tissue. If present, the analytic Jacobian is used by default (see #1795 for some benchmarking).
* HDF5 file access has been improved to use more appropriate 'chunk' sizes. This speeds up cardiac output file reading/writing/postprocessing in quite a lot of situations.
* Postprocessing maps can now be written to VTK as well as meshalyzer. They are now written via HDF5, so you can get them to any format you like with an appropriate HDF converter.


#### Cell-based

* There is a new cell-based modifier mechanism which allows you to modify the cell population. This replaces the old hierarchy where each modification involved making a new subclass of the population. Examples of use cases would include modifying the target area of cells, tracking Delta-Notch, calculating the volume of all cells, or outputting statistics. Methods such as `UpdateAfterSolve` and `UpdateAfterTimestep` have been moved from simulation classes and into the relevant modifiers.
* We have re-factored the way cell populations write data to file by creating a writer hierarchy. One of these writers is created for each file that needs to be written, and then the population visits each writer it owns when it writes to file. This shouldn't affect user projects as the interfaces in tests for simulations hadn't changed. User tests of populations may fail if `AbstractCellPopulation::OpenWritersFiles()` hasn't been called before writing.
* Cellular Automata class changes: `MultipleCaBasedCellPopulation` has been removed, as `CaBasedCellPopulation` now allows (optionally) for more than one species at a site.
* `NodesOnlyMesh` now works in parallel and uses a `DistributedBoxCollection` to select which nodes it owns based on the decomposition in the box collection. It is necessary to include the `PetscSetupAndFinalize.hpp` header in the test to use this type of mesh.


### Major new functionality & code changes

#### General

* To enable cross-platform support, we have removed all linux system calls to `rm` and `cp`, these are now done via `FileFinder`. The following are of note:
    * `FileFinder::Remove()` this operates like `rm` for a file, and `rm -r` for a folder. It will only delete things that are in a `testoutput` folder that contains the signature file (.chaste_deletable_folder denoting the fact Chaste made the folder in the first place).
    * `FileFinder::DangerousRemove()` this operates like `rm -f` for a file, and `rm -rf` for a folder. It will delete anything in the `testoutput` or chaste source folders (but not elsewhere), regardless of the presence of a signature file. This is used very very rarely in the code, and should be avoided if possible.
    * There is no command to remove files from anywhere else on your machine. If you did manage to set your `CHASTE_TEST_OUTPUT` to be "/" then `DangerousRemove()` could wipe large parts of your system, obviously this should be avoided.
* To enable cross-platform support, have moved from a `rand()` based random number algorithm, to `boost::random` (Mersenne Twister), this is supposed to be "more random", and has the benefit of getting the same answers on different platforms to facilitate testing. So any programs you have that use random numbers (this includes most of `cell_based` and `crypt`) will get subtly different results now.
* Reading of binary mesh files was scaling badly with mesh size (for file sizes of >0.5Gb) on some file systems. This has been fixed so that partitioning and loading binary meshes on supercomputers is now faster.
* All mesh element files now have floating point attributes by default.  Old binary element files with attributes **cannot be read** by Chaste.  A conversion utility 
```
./python/utils/ConvertBinaryElementAttributes.py
```
 is provided to assist users with this change.
* Simple airway tree ventilation models (Poiseuille flow and Pedley resistance) have been added to `continuum_mechanics`.
* `Node` now uses a `NodeAttributes` class to store its attributes. It is only created if the attributes are used so any code in projects that calls `Node::rGetNodeAttributes()` without having first set an attribute will encounter an error. If you need to check whether any attributes are set up, `Node::GetNumNodeAttributes` will return the number of attributes (0 if none set).


#### Cardiac

* 3D quadrature now uses second order (rather than first order) integration. This may change results slightly (for the better!).
* Fibre reading capability for extended bidomain problem has been implemented such that `ExtendedBidomainTissue` has modified conductivities in all 3 fields (thanks to Shameer).
* Heterogeneous contraction models can now be used in electro-mechanics simulations, on a per-element basis on the mechanics mesh. This is done by creating a factory inheriting from `AbstractContractionCellFactory`, and setting this in the electro-mechanics problem definition.
* Fixed a bug when using parMETIS partitioning (the default, 
```
PARMETIS_LIBRARY
```
) which often resulted in deadlock when using [state variable interpolation (SVI)](https://chaste.cs.ox.ac.uk/trac/wiki/ChasteGuides/StateVariableInterpolation) in 3-D.
* Changed cell factories from passing node indices to pointers to Node objects, and element indices to pointers to Element objects.
    * For most users this will mean updating all instances of `CreateCardiacCellForTissueNode` to have the correct argument (from e.g. `unsigned node` to e.g. `Node<DIM>* pNode` where `DIM` is probably 1, 2, or 3) and replacing all occurrences like `GetMesh()->GetNode(node)` with simply `pNode`.
    * Contraction cell factory (`AbstractContractionCellFactory` and `LabelBasedContractionCellFactory`) methods `CreateContractionCellForElement` have changed from taking an `unsigned` to an `Element<DIM,DIM>*`.
    * `AbstractPurkinjeCellFactory::CreatePurkinjeCellForTissueNode` has changed from taking an `unsigned` to a `Node<DIM>*`.
*  In Bidomain with bath simulations electrode 'on' and 'off' events are now required to coincide with printing time-steps. If they do not coincide then a run-time exception is thrown.
* A script `python/utils/AddVtuTimeAnnotations.py` has been added. This can convert VTK output so that it is easily animated in Paraview. Note that the resulting files are paraview-specific and not part of the generic VTK standard.


#### Cell-based

* Fixed bug in area and volume calculations for 3-d cell-centred mesh-based simulations and 3-d vertex mesh simulations
* The definition of the cut-off length in a `NodeBasedCellPopulation` has been moved to the underlying `NodesOnlyMesh`. Consequently it should be set when constructing the mesh using `ConstructNodesWithoutMesh(mesh, cut_off)` rather than calling `NodeBasedCellPopulation::SetMechanicsCutOffLength(cut_off)`.
* Cell radii in `NodeBasedCellPopulation` type simulations are now stored in the `NodeAttributes` of each `Node`. It should now be accessed directly through the node, rather than through `NodesOnlyMesh`.
* Forces on a node in `OffLatticeSimulation` are now stored in the `NodeAttributes` rather than a separate vector. This means that `AbstractForce::AddForceContribution` now only takes the cell population as an argument. For example, in a cell population or a force class `rForces[p_node->GetIndex()]` is replaced with `p_node->rGetAppliedForce()` and `rForces[p_node->GetIndex()] += force` is replaced with `p_node->AddAppliedForceContribution(force)`.
* `AbstractCellProperty` is more widely used throughout the code, and classes such as `ProliferativeType`s now use this framework.


### Minor
New functionality and code changes, which may still require changes to user code

#### General

* For developers, you no longer have to type "test_suite=" after `scons`, this makes it easier to use tab completion.
* `AbstractNonlinearElasticitySolver::WriteCurrentDeformationGradients` has been renamed, replace calls of `solver.WriteCurrentDeformationGradients(..)` with `solver.WriteCurrentStrains(DEFORMATION_GRADIENT_F,..)`. Other strains can also be written - see How To page.
* One dimensional meshes can now be written out to VTK format using the `VtkMeshWriter`, 2D and 3D were before.
* *Change to CVODE solving:* `AbstractCvodeSystem` and `CvodeAdaptor` have enabled the `CVodeSetStopTime` option to make sure that CVODE stops exactly where requested (before it solved up to where it felt like, and interpolated an answer back to you). Users should not notice much difference (you may get changes in e.g. 4th decimal place due to more accurate answers now). Because of this, we have also changed the default behaviour on repeated Solve calls to re-initialise CVODE only when it is evident something has changed (tStart != last time's tEnd, or state variables have changed), previously we re-initialised CVODE on every call to `Solve` as default. You can still re-initialise on every call by manually calling the method `AbstractCvodeSystem::SetForceReset(true);` if you need to.
* Additional time points are no longer permitted in `TimeStepper`.
* Auto-generated quadratic slab/rectangular meshes have different node/element indexing to release 3.1.
* Continuum mechanics solvers now reference `AbstractTetrahedralMesh` rather than (subclass) `QuadraticMesh` to allow use of a parallel version (`DistributedQuadraticMesh`). This may break any user projects that contain solver subclasses.


#### Cardiac

* What was called `DynamicRestitutionStimulus` has been renamed `SteadyStateRestitutionStimulus`, as we talked to some physiologists!
* Unfortunately, an error was discovered in a calculation behind the `CompressibleExponentialLaw` (a material law, and for compressible cardiac electro-mechanics the default law), which will have resulted in too small stresses and overly large deformations. The class has been fixed. This may change user projects results
* The coarsened version of the Oxford Rabbit mesh located at `apps/texttest/weekly/Propagation3d` has been renamed `OxfordRabbitHeart_481um`.
* When constraints are placed on valid values for cardiac cell model state variables (e.g. gating variables should stay between 0 and 1), CVODE is now allowed to break these to within a factor of its specified absolute tolerances, following the CVODE documentation on "Advice on controlling unphysical negative values".
* `AbstractCardiacCellInterface::UseCellMLDefaultStimulus()` now returns a `boost::shared_ptr<RegularStimulus>` to the stimulus instead of returning `void`. **This may break user projects if you are storing auto-generated models**. In this case the method should be updated as per r19552. This has the benefit of providing access to the `RegularStimulus` methods, without having to remember how to static cast a boost shared pointer to an `AbstractStimulusFunction`.
*  You can now print out additional action potential model variables in a `BidomainWithBath` simulation, previously this failed because a `FakeBathCell` doesn't have them.
* `HeartConfig::Instance()->SetVisualizeWithVtk();` will now work in 1D as well as 2D and 3D.
* The CVODE change (see general above) has led to a small improvement in accuracy for CVODE in heart tissue, since voltage was not being updated at precisely the correct time before.
* Fibre input and output in parallel has been improved. Binary fibre files are preferred.
* PyCML has the ability to produce cells that can be solved using *generalised* Rush-Larsen (release 3.1 added original Rush-Larsen).
* When constraints are placed on valid values for cardiac cell model state variables (e.g. gating variables should stay between 0 and 1), CVODE is now allowed to break these to within a tolerance, following the CVODE documentation on "Advice on controlling unphysical negative values".
* Altered the output from `PseudoEcgCalculator` to include the time value along with the ECG value. Also added the ability to skip time steps which allows an ECG graph to be computed more quickly.
* `PostprocessingWriter` and `PseudoEcgCalculator` now use `FileFinder`s in their constructors to specify directories (instead of a string and a bool).
* Code generation for Backward Euler cell models now uses a slightly different Maple routine (to allow for discontinuities on the right-hand side). This means code can now be generated for models where it used to fail. Note that a finer resolution in lookup tables can be required, so try reducing the table step if you find the Newton solver failing to converge.


#### Cell-based

* Bug in vertex-based simulations which involved cells not being counted as removed after T2 swaps has been fixed.
* When calculating the volume of cells in Node based simulations we now take into account the number of cells connected and its relation to the optimal packing of spheres.


### Future Plans

* **General**: The next release of Chaste will no longer support versions of boost < 1.40.
* **Cardiac**: The next release of Chaste will no longer output Meshalyzer format as default (it will remain an option to enable).



----
## Release 3.1 (changes since Release 3.0)

Release 3.1 is a minor release, which brings support for newer versions of libraries and a small number of new capabilities and bug fixes. It provides access to a release version of Chaste under the BSD licence (rather than the LGPL licence), to make it easier to use Chaste in industrial settings.

### Headline features

#### General

* Chaste is now released under the BSD licence, this is one of the major reasons for this release: http://opensource.org/licenses/BSD-3-Clause.
* The Ubuntu package now also supports Precise Pangolin (12.04 Long-Term Support edition).
* Support for PETSc version 3.2 has been added.  Some previously supported versions have been dropped so that the minimum required version of PETSc is now 2.3.2.  The minimum version of Boost is now 1.34.
* Support for up to GCC 4.7.0 and Intel 12.1 compilers.


#### Cardiac

* Cardiac electro-mechanics now works with bidomain as well as monodomain simulations.
* Cardiac cell models in tissue can now be solved using `CVODE` (versions 2.5-2.7), this can provide large speed-ups for problems that are small enough to get all the Cvode solvers in memory.

#### Cell-based

* The global singleton `CellWiseData` has been replaced by a much more general `CellData` component in each cell.
* The cell property hierarchy is now used much more extensively throughout the code.
* A new cell population class has been introduced to enable the simulation of cellular automata with multiple site occupancy.


### Major new functionality & code changes

#### General

* Chaste is now beginning to use the Boost Filesystem library for low-level file management. This means an extra third-party dependency; your builds will fail if the library is not installed. Updating to the latest version of the chaste-dependencies Ubuntu package will ensure the library is installed; many systems will have it anyway. Your `hostconfig` file may require editing to link against `boost_system` as well as `boost_filesystem` if using recent Boost versions. (Boost >= 1.34 is now required.)

#### Cardiac

* A `CellMLLoader` class is available which makes the dynamic loading of CellML files into (almost) a one line call.
* The Cmgui script that helps the user to load the simulation data has been adapted to Cmgui version 2.8 or later. It is still compatible with previous Cmgui versions 2.7 and 2.6. The name of the script is now LoadSolutions.com in both the undeformed and deformed cases.
* A CellML project has been created containing many annotated CellML files for use with Chaste. See the Chaste wiki ([CodeGenerationFromCellML](../../user-guides/code-generation-from-cellml)) for details of how to access it.


#### Cell-based

* The global singleton `CellWiseData` has been replaced by a `CellData` component in each cell.  These data are scalable and are accessed by name rather than index.  There is a helper method on cell populations for visiting all cells and setting constant data (
```
SetDataOnAllCells()
```
).  When using nutrient-dependent cell-cycle models or PDEs the `CellData` name must match with the name used in the class.
* Cell-based simulations, populations, forces and cell killers can now all be templated over element dimension as well as space dimension; this currently allows for mesh-based simulations of 2D surfaces in 3D space without cell division.
* Two serious bugs fixed in Delta-Notch code (the number of times that the ODE is solved and which variables get updated in the `CellData`).
* A new cell-population class, `MultipleCaBasedCellPopulation`, has replaced `CaBasedCellPopulation`. This enables cellular automata to be simulated which allow multiple site occupancy (more than one cell model at each lattice site).
* Centre-based simulations now have a movement threshold in order to check for numerical stability. You will need to manually call `SetAbsoluteMovementThreshold()` in simulations where large cell movements are typical.


### Minor
New functionality and code changes, which may still require changes to user code.
#### General

* The `testoutput` directory in the main trunk has been renamed `test_summary` to avoid confusion. For each build, it contains a generated webpage with a summary of test results and links to their console output, your actual test output goes elsewhere. This means you need to update any browser bookmarks to the test results summary.
* The method `AbstractElement::SetRegion` has been renamed to `SetAttribute`. Similarly, `GetRegion` has been renamed to `GetAttribute`.
* It is now possible to run Electromechanics problems where the electrical problem is a bidomain problem. The interface of `CardiacElectroMechanicsProblem` has changed. You now need to pass the electrics problem type as second parameter to the constructor (e.g., MONODOMAIN, BIDOMAIN) and the electrics problem dimension as second template (defaults to 1).
* We now pass fibre file names around using a `FileFinder` rather than a string, to allow loading from a wider variety of locations.
* A local.py settings file may be placed in python/hostconfig to be used in preference to any other hostconfig settings.

#### Cardiac

* Most of the heart solvers and cell factories now use `AbstractCardiacCellInterface`, not `AbstractCardiacCell` (to enable the use of CVODE solvers).
* In the version 3.1 XML parameters file, the `ConductivityHeterogeneities` element has been moved from inside `<Simulation>` to inside `<Physiological>`. New files written to this version of the schema will need to reflect this; old files still using a previous version can still be used unchanged.
* For simulations with *compressible* material laws, the electro-mechanics solver should have been scaling the active tension returned by the contraction model, by the determinant of the deformation gradient. This has now been fixed. (See ChasteGuides/FiniteElementImplementations for the (corrected) equations). Results using the compressible material law in the repository have barely changed, since this material law is nearly incompressible. However, simulation results with any user-defined highly compressible law might change.
* Pseudo ECG calculations for Bidomain-with-Bath simulations have been changed, as pointed out on the mailing list, these had a bug that meant the integral was performed over the whole mesh (including bath) instead of just cardiac tissue.
* Fixed a small bug in cardiac checkpointing, when loading and running a simulation from an archive to a new output folder the voltage at the final time step in the .h5 file was spuriously reported as "0".
* `FibreReader::GetNextFibreVector(vec)` has been changed to `FibreReader::GetFibreVector(index,vec)` and `GetNextFibreSheetAndNormalMatrix(mat)` to `GetFibreSheetAndNormalMatrix(index,mat)`.
* The `HeartConfig` class has undergone an extensive refactor internally. This shouldn't impact users (although you might notice that a `ChasteDefaults.xml` file is no longer written to checkpoints), but some "nonsensical" calls to Get methods may now return different or new errors.
* There have been changes the interface of the `VoltageInterpolaterOntoMechanicsMesh` class. Now you need to pass in the names of the electrics variables you want to interpolate onto the mechanics mesh (variable 'V' used to be hardcoded as the only one to be interpolated).

#### Cell-based

* Renamed the `AbstractCellBasedSimulation` methods `PostSolve()` and `AfterSolve()` to `UpdateAtEndOfTimeStep()` and `UpdateAtEndOfSolve()` respectively; also moved the code out of the existing `AbstractCellBasedSimulation` methods into the main `Solve()` method, so that these methods don't have to be called by every overridden version.
* Corrected the implementation of `StochasticDurationGenerationBasedCellCycleModel` by making use of parameters `mStemCellG1Duration` and `mTransitCellG1Duration` in the method `SetG1Duration()`. This won't break user projects, but may change results.
* Created a new `AbstractCellPopulation` method `GetVolumeOfCell()`, which is overridden in concrete subclasses; this method is now used in `VolumeTrackedOffLatticeSimulation`, which hence now works with any off-lattice cell-based population.
* Corrected initialisation of `CellwiseData` (now `CellData`; see above) in `VolumeTrackedOffLatticeSimulation`; it is now populated automatically when a simulation is set up, rather than having to be manually initialized.
* VTK output has been enabled for cell-based simulations that use a `MultipleCaBasedCellPopulation` or `PottsBasedCellPopulation`.
* Moved `mpBoxCollection` from `NodeBasedCellPopulation` to `NodesOnlyMesh`.
* Made `CellId` a concrete `CellProperty` to exploit the functionality of this class hierarchy.
* Created the class `CellAncestor`, which inherits from `AbstractCellProperty` and stores the unsigned variable associated with each ancestor. The `Cell` method `SetAncestor()` now takes a shared pointer to a `CellAncestor` rather than an unsigned.
* Extended the class `SurfaceAreaConstraintUpdateRule` and the `PottsMesh` method `DivideElement()` to work in 3D
* In node-based simulations cell radii are now inherited from parent cells; before this was hard-coded to 0.5. Also enabled updating of cells radii through `CellData`. This won't break user projects, but may change results.
* The `HoneycombMeshGenerator` was producing slightly irregular cell-cell spring lengths due to floating point truncation. This has been fixed, which means that all simulations using `HoneycombMeshGenerator` now give slightly different results, and monolayer simulations surrounded by layers of ghosts nodes pull the convex hull of the ghost nodes to a circle more rapidly than before. This won't break user projects, but may change results.
* We have renamed the cell killer methods `TestAndLabelSingleCellForApoptosis()` and `TestAndLabelCellsForApoptosisOrDeath()` to `CheckAndLabelSingleCellForApoptosis()` and `CheckAndLabelCellsForApoptosisOrDeath()` respectively, since it is not ideal to have a method with the prefix Test- outside a test suite.
* `OxygenBasedCellKiller` has been renamed `ApoptoticCellKiller` to more accurately reflect its functionality.
* `CryptCellsGenerator` now works with a `PottsBasedCellPopulation`.
* Refactored `VertexElement` and `PottsElement` to both inherit from a new class, `MutableElement`, and moved appropriate functionality up into this parent class. Also changed the order of the parameters in `MutableElement::AddNode()` so that `rIndex` can default in child classes. This will particularly affect `VertexElement` where users will need to change the order of the parameters, switching `pNode` and `rIndex`.
* The `divisions.dat` data file, if output, now includes an extra column containing the age of the parent cell just prior to division.
* Moved `mCellProliferativeType` from `AbstractCellCycleModel` back into `Cell`.
* Forces in node-based populations may now be made dependent on cell radii.
* Added a new force class, `NagaiHondaDifferentialAdhesionForce`, and associated tutorial `TestRunningDifferentialAdhesionSimulationsTutorial`. This class inherits from `NagaiHondaForce` and allows for different interaction energies depending on which (if any) of a pair of interacting cells have the property `CellLabel`.
* Removed an exception in `NodeBasedCellPopulation` that had prohibited a simulation from having a single cell.
* Added a new force class `DiffusionForce` to the trunk for simulating random movement.
* Added several 'removal' methods: `RemoveAllUpdateRules()` to `MultipleCaBasedCellPopulation` and `PottsBasedCellPopulation`; `RemoveAllCellKillers()` to `AbstractCellBasedSimulation`; `RemoveAllForces()` to `OffLatticeSimulation`; and `RemoveAllMultipleCaUpdateRules()` and `RemoveAllPottsUpdateRules()` to `OnLatticeSimulation`.
* The `CellBasedPdeHandler` method `UseCoarseMesh()` now takes a `ChasteCuboid` defining both the size and location of the coarse mesh to use, so that the user can specify the exact location of the coarse mesh rather than it defaulting to centering on the centre of the cell population. The user should either ensure this contains the population or set the extra flag to true to automatically centre this mesh on the centre of the cell population.
* In order to allow more than one cell per location index in `MultipleCaBasedCellPopulation`, the `GetCellResults()` method in `AbstractCellPopulation` has been modified to take in a `CellPtr` rather than a location index.


-----
## Release 3.0 (changes since Release 2.3)

### Headline features

#### General

* The Ubuntu package now also supports Oneiric Ocelot (11.10)
* Support for PETSc 3.1 has been added, and Chaste should also work with the latest versions of the Boost libraries.
* This is the last Chaste release that will officially support Boost 1.33.1 and PETSc 2.2.
* The mechanics (and cardiac electro-mechanics) solvers have been made significantly more flexible.
* It is relatively easy to write new solvers of coupled systems of linear PDEs, and tutorials on how to do this have been added.
* We now recommend using VTK with Chaste, and the default.py hostconfig assumes it is available; previously support for VTK input/output within Chaste defaulted to off.


#### Cardiac

* (Work has begun on solving fluid flow and electrophysiology with Purkinje fibres, but these features are not yet completed.)


#### Cell-based

* Lattice based cellular Potts models have been implemented.
* There has been a major refactor of the structure of the cell-based code to make the specification of multi-cell models (such as cell-centre, over-lapping spheres, vertex-based and cellular Potts) more consistent.
* The handling of PDEs has been improved allowing PDEs to be coupled to node-based simulations.
* More exceptions are thrown when incompatible classes are used.  Exception messages give information on how to fix the problem.


### Major new functionality & code changes

#### General

* An error is given if using Boost 1.41 due to a [bug](http://sourceforge.net/apps/trac/easystroke/ticket/21) in its serialization library.  Versions 1.44-1.46.1 also had a bug triggered when some tests exit, but the tests do run successfully.
* All the solid mechanics related functionality has been moved out of the `pde` component to a new component `continuum_mechanics`. These components should be considered as quite separate to each other.
* The interfaces to the solid mechanics solvers have changed considerably. They now take in a 'problem definition' object and are much more powerful. The tutorials describe the new interfaces in detail.
    * The incompressible solver is now called `IncompressibleNonlinearElasticitySolver`.
    * Further work has been done on the compressible solver.
    * Both the incompressible and compressible solvers take in a new class, `SolidMechanicsProblemDefinition`, on which the material law, body force, displacement and traction boundary conditions are defined. See the solid mechanics tutorial to see how these classes are used. They also now take in a reference to a mesh not a mesh pointer.
    * Sliding boundary conditions are now possible (i.e. displacement boundary conditions, for only some components of the displacement, at given nodes).
    * Solid mechanics problems can now use boundary conditions that specify that a particular pressure should act in the normal direction on deformed surfaces.  It may not be fully optimised yet though - the Jacobian in the nonlinear solve needs altering.
* PDE-related changes:
    * When solving general time-dependent PDEs the solution can now be written to file at a specified sampling interval, in a variety of formats (HDF5, cmgui, text).  See UserTutorials/SolvingLinearPdes for more details.
    * Renamed `AbstractFeObjectAssembler` to `AbstractFeVolumeIntegralAssembler`, moved the surface integral functionality from this class to `AbstractSurfaceIntegralAssembler`, and created a natural Neumann concrete child of `AbstractSurfaceIntegralAssembler` to be used in PDE solvers.
    * These changes allow solvers of *systems of PDEs* to be set up relatively easily (for PDEs for which it is appropriate to use linear basis functions, e.g. systems of coupled heat or diffusion equations). Tutorials on writing your own PDE solvers have been added: start with UserTutorials/WritingPdeSolvers.
    * Added new classes `AbstractLinearParabolicPdeSystemForCoupledOdeSystem` and `LinearParabolicPdeSystemWithCoupledOdeSystemSolver` for the numerical solution of coupled systems of reaction-diffusion PDEs and ODEs.  See the associated tutorial UserTutorials/SolvingLinearParabolicPdeSystemsWithCoupledOdeSystems.
    * The efficiency of `PetscMatTools::ZeroRowsAndColumnsWithValueOnDiagonal` has been significantly improved, which should improve performance when using Dirichlet boundary conditions.
* Due to floating point error, it was previously possible for `TimeStepper` to occasionally take a very small step in long simulations, when all steps should have been the same size, and hence break code that assumed a constant time-step.  The tests and calculations have now been made much more robust, by being based on machine precision rather than magic numbers.
    * Any time-stepping object will throw if stepped past its end time.  (Previously (i) the core/heart `TimeStepper` class silently remained at the end time and (ii) the cell_based `SimulationTime` singleton class silently stepped past the end time.)
* Mesh-related changes:
    * `GenericMeshReader` has been changed from a class to a function.  If you use it directly, you must now do something like "`std::auto_ptr<AbstractMeshReader<2,2> > p_reader = GenericMeshReader<2,2>(mesh_path);`".  The returned smart pointer will automatically destroy the reader when it goes out of scope, so any other changes to your code should be limited to replacing `reader` with `*p_reader`.
    * Some mixed dimension meshes may now be read in to Chaste, i.e. 1d elements embedded in a 2d or 3d mesh.  The 1d elements are defined in a separate `.cable` file, with the same format as the `.edge` file.
* Other new functionality:
    * Various additions to `CommandLineArguments` make it possible to pass in lists of arguments for a particular option. An option is now defined as starting with '-' followed by any non-numeric character to avoid confusion with negative numbers. Various helper methods have been added to avoid having to use `char*` and `atoi` etc.
    * There's a new class `CompareDoubles` in `MathsCustomFunctions` with static methods for comparing floating point numbers to absolute or relative tolerances.  This is now used in `NumericFileComparison` so that files can be compared to the looser of an absolute or relative tolerance.  The default is still to use just absolute as before.
    * Added methods `PetscMatTools::CheckSymmetry` and `PetscMatTools::CheckEquality`.
    * Where work can be split between isolated processes, it would be nice to be able to do so easily without worrying about collective calls made inside classes such as `OutputFileHandler` leading to deadlock.  A new method `PetscTools::IsolateProcesses` has been added to facilitate this.  Note that it doesn't guarantee safety - collective calls not resulting from the 3 methods affected will still cause deadlock.


#### Cardiac

* Changes accessible via the XML parameters file:
    * Allowed the precision with which Meshalyzer and Cmgui visualisation output is written to be specified from the XML configuration file and via `HeartConfig`. (Thanks to Megan Marsh.)
    * Added the ability to specify paths relative to the XML configuration file for elements with type `path_type` (e.g. `ArchiveDirectory` and cell model paths).  Use the attribute `relative_to="this_file"`.
* Electro-mechanics: See the cardiac electro-mechanics tutorials for examples/usage of the following changes:
    * Cardiac electro-mechanics solvers can now use compressible elasticity as well as incompressible elasticity.
    * The interface to `CardiacElectroMechanicsProblem` has completely changed, and the interface to `CardiacElectroMechProblemRegularGeom` has slightly changed. `CardiacElectroMechanicsProblem` now takes in a problem definition object (c.f. the mechanics solvers) which means it is now much more flexible. Anything that can be done in a mechanics simulation can now immediately be done in a electro-mechanics simulation.
    * For both `CardiacElectroMechanicsProblem` and `CardiacElectroMechProblemRegularGeom`: electrics PDE timestep if different to 0.01, and simulation end time, should be set using `HeartConfig`, and not in the constructor of the problem class.
    * `CardiacElectroMechProblemRegularGeom` constructor parameters are in a slightly different order, and it also can't be used with mechano-electric feedback or fibre files any longer (use `CardiacElectroMechanicsProblem` instead).
    * Some new tutorial tests have been added.
* Added functionality to solve extended bidomain problems (with two cell types at each control volume). This functionality is not yet available for the executable users.
* The ability to perform non-matrix-based assembly (of the RHS vector) has been removed; matrix-based assembly is now always used. The option `SetUseMatrixBasedRhsAssembly` no longer exists.
* The convenience method `GetAllOrtho` used to do VTK visualisation of ortho files was incorrect.  It was returning the *rows* of the conductivity tensor which represent a transpose of the original fibre data.
* Various cardiac post-processing operations scale poorly with the number of nodes.  This has been significantly improved, although dramatic slowdown will still be observed with very large simulations.  (Technical detail: the reason for this is that the output data is written to the HDF5 file at each printing time-step, and so the file layout is optimised for reading/writing every node at one time-step.  However, post-processing needs to read every time-step for a single node or subset of nodes, and so cannot access disk as efficiently.)
* Implemented calculating fibre orientations (Streeter) in a wedge preparation, for either left or right ventricle.  Previously both LV and RV endocardial surfaces were required.


#### Cell-based


* A major refactor of the cell population and cell-based simulation class hierarchies has taken place, based upon a distinction between on- and off-lattice models. This was done to integrate the code more thoroughly as on-lattice population and simulation classes were introduced, and to ensure that the use of update rules and forces is more consistent.
    * The `CellBasedSimulation` class has been split up into a hierarchy, with `OffLatticeSimulation` and `OnLatticeSimulation` inheriting from  `AbstractCellBasedSimulation`.
    * All cell populations now inherit from either `AbstractOffLatticeCellPopulation` or `AbstractOnLatticeCellPopulation` the former are used by `OffLatticeSimulation` and the later are used by `OnLatticeSimulation`.
* Cellular Potts models have been implemented in Chaste
    * The `PottsBasedCellPopulation` has been created with associated `PottsMesh` and `PottsElement` classes to store spatial information.
    * The `AbstractPottsBasedUpdateRule` hierarchy is used to define the dynamics of the simulation.
    * Simulations make use of the existing cell-cycle model and cell-killer hierarchies.
    * Added functionality for visualizing Potts-based cell simulations either using the visualizer `Visualize2dVertexCells.java` or using Paraview with VTK output.
* We have moved much of the cell-based code to use `boost::shared_ptr`s rather than plain pointers. This makes memory handling much more straightforward.
    * The `CellBasedSimulation` class and its subclasses now store collections of cell killers, boundary conditions, forces or update rules as `boost::shared_ptr`s.

 These are passed to cell-based simulations as  (e.g.) `std::vector<boost::shared_ptr<AbstractForce<DIM>>>` instead of `std::vector<AbstractForce<DIM>*>`.

* We also use helper macros such as `MAKE_PTR` a lot more in tests; these are defined in the header `SmartPointers.hpp`.
* A new overlapping spheres based force law, used by Buske *et al.* in their 2011 model of the crypt based on previous work by Galle *et al.*, has been implemented.
* Added `OdeLinearSystemSolver` for solving large systems of ODEs of the form M dr/dt = f(t,r), where M is large and sparse.
* Added two new force classes, `BuskeInteractionForce` and `BuskeCompressionForce`, to implement the model of cell-cell mechanical interactions used by Buske.
* Added the ability to set/get cell radii in `NodeBasedCellPopulation` (via a member of `NodesOnlyMesh`), and allowed these to be updated when cell division/death occurs.  Cell radii may also be written to VTK output.
* We have generalised the way that PDEs, coupled to cell-based simulations, are handled:
* Altered the input arguments to the method `CellBasedSimulationWithPdes::UseCoarsePdeMesh` and allowed output of the PDE solution on the coarse mesh.
* Enabled the numerical solution of one or more (steady) reaction-diffusion PDEs coupled to a `NodeBasedCellPopulation`, by introducing a "coarse" PDE mesh associated with the population.
* Extended `CellBasedEventHandler` so that it also records the time spent solving any coupled PDEs, for use in `CellBasedSimulationWithPdes`.
* Created an `AbstractCellBasedPde` class which contains the PDE, the solver, the boundary conditions and an interface to an `AbstractCellPopulation`. This class can be passed to a concrete instantiation of an `AbstractCellBasedSimulation` just as forces or update rules are; this change avoids having to implement PDEs in each of `OffLatticeSimulation` and `OnLatticeSimulation`.
* We have introduced a new method of imposing boundary conditions (such as restricted geometries) on cell-based simulations:
* The `CellBasedSimulation` method `ApplyCellPopulationBoundaryConditions` has been removed.
* Boundary conditions must now be implemented using the `CellPopulationBoundaryCondition` hierarchy. This change allows the use of multiple boundary conditions in a cell-based simulation, just as multiple force laws may be used.
* An example cell-cycle model class `ContactInhibitionCellCycleModel` has been added. This class may be used to simulate contact inhibition of cell division and assumes that the volume of each cell is stored in the singleton `CellwiseData`.
* The simulation class `VolumeTrackedOffLatticeSimulation` has been created to be used with the contact inhibition cell cycle model.
* Cell cycle phases can now be written to file for visualization if required, in the file `results.vizcellphases`.


### Minor
New functionality and code changes, which may still require changes to user code.

#### General

* Mesh-related changes:
    * The mesh reader now throws an `Exception` if attributes are declared in the header line but missing in the mesh files.
    * Added `AbstractTetrahedralElement::CalculateNormal` and `AbstractTetrahedralMesh::CheckOutwardNormals` to obtain normal vectors to boundary elements, and check they all face outwards, respectively.
    * Altered perimeter edges created in `TetrahedralMesh::ConstructRectangularMesh`  and `DistributedTetrahedralMesh::ConstructRectangularMesh` so that they are all oriented anticlockwise.  This makes sure that the normals are pointing outward.
    * Previously a `QuadraticMesh` had to read a tetrahedral mesh from file using a special converter (i.e. with the method `ConstructFromLinearMeshReader`). Now the usual method (`ConstructFromMeshReader`) may also be used.  It warns that extra work is done, since a mesher library has to be used to construct the extra nodes.
* Build system changes:
    * You can now do a coverage build for a single test in a project (e.g. `scons b=Coverage ts=projects/...`).
    * We have worked around an SCons issue that causes parallel builds (e.g. `-j3`) with `cl=0` to fail in parallel. However, it uses undocumented internal functionality in SCons, so please report an issue if it fails for you, and tell us what version of SCons you are using.
    * Removed broken support for the `SPECIAL_SERIAL` `#define`.  This is unlikely to break anything, since it would have already been broken...
* Miscellaneous other changes:
    * The `TERMINATE` and `NEVER_REACHED` macros have been moved into `Exception.hpp` (from `PetscTools.hpp`), and various includes tidied up.  Some macros have also been renamed for clarity and readability: `EXPECTNON0` -> `EXPECT_NON0`, `MPIABORTIFNON0` -> `ABORT_IF_NON0`.  (The latter macro now works correctly in non-MPI-using tests.)  Note also, if you are using `PetscTools::Terminate` directly rather than via a macro, that this method no longer exists - use `Exception::Terminate` instead.
    * The `EXCEPTION` and `WARNING` macros now allow 'streaming' within their message argument, so that you can write (for example)

```

EXCEPTION("Number of nodes " << num_nodes << " does not match expected value of " << ELEMENT_DIM+1);


```


* `Exception` subclasses may now change the error message after the base class is constructed.
* A `GetParent` method has been added to `FileFinder`.  A `FileFinder` can also now be created relative to some existing file or directory.
* Functions `CreateEmptyVector` and `IsEmptyVector` have been added to `VectorHelperFunctions.hpp`
* Moved the functions `SmallPow` and `Divides` from the `linalg` component into a new header `MathsCustomFunctions.hpp`.
* A new class `AbstractCvodeSystem` has been created between `AbstractCvodeCell` and `AbstractParameterisedSystem`, analogously to `AbstractOdeSystem`.
    * `AbstractCvodeSystem` has a new method `SetAutoReset`. If this is turned on then CVODE will not have its internal state reset between calls to `Solve` (unless the state variables or simulation time are changed by external code in the meantime).  A method `ResetSolver` has been added to force a reset if other changes are made externally that may require this (e.g. changing the RHS function by modifying a parameter).
* Moved all methods of `AbstractParameterisedSystem` which don't require the vector type up into a new base class `AbstractUntemplatedParameterisedSystem`.  This should not affect other code.
* Renamed `PetscMatTools::AssembleFinal` to `PetscMatTools::Finalise`, `PetscMatTools::AssembleIntermediate` to `PetscMatTools::SwitchWriteMode`, and `PetscVecTools::Assemble` to `PetscVecTools::Finalise`.  Similar name changes happened to the analogous `LinearSystem` convenience methods.
* Changed `AbstractLinearEllipticPde::ComputeConstantInUSourceTerm(rX)` to `AbstractLinearEllipticPde::ComputeConstantInUSourceTerm(rX, pElement)` so it can take in an element containing `rX` to make it consistent with `ComputeLinearInUCoeffInSourceTerm`.  You can pass in a `NULL` pointer for `pElement`.  Changed all associated classes.
* Method for writing strain per element added to `AbstractNonlinearElasticitySolver`. There is as yet no interface to it: to use it you must call it from the main output method.


#### Cardiac

* Changes to CellML support:
    * The cell model converter class is now more robust to certain errors, and gives more helpful error messages.  Temporary files are now saved when an error occurs during the conversion of a cell model from CellML.
    * Various performance improvements have been made to the cell model code generation in PyCml.
    * PyCml now includes support for generating cell models that can be solved using the Rush-Larsen method.  These are not available 'by default' but must be generated manually or loaded dynamically.  See `/heart/test/ionicmodels/TestRushLarsen.hpp` for some examples.
* A binary format has now been defined for fibre files, to enable random access into the file.


#### Cell-based

* Moved an uncaught exception (from the element Jacobian code) and turned it into a higher-level exception in `MeshBasedCellPopulation`, which is thrown when any element has zero area/volume.
* Added a method to perform vertex intersection swaps in the `VertexMesh` class.
* Resolved bug which prevented VTK or cell volume data at time-step zero being written to file.
* Calling `GetCircularMesh` on a `HoneycombMeshGenerator` that contains ghost nodes now throws an exception; previously the generator created a corrupt mesh.
* `HoneycombMeshGenerator` now defaults to not use ghost nodes.
* Moved the method `GetNeighbouringNodeIndices` from `DiscreteSystemForceCalculator` into `AbstractCellPopulation`, where it is pure virtual and hence overridden in subclasses.
* Added an overridden `WriteCellVolumeResultsToFile` method in all cell population subclasses.
* Added the `SerializableSingleton` class to allow for singleton classes and subclasses of `AbstractCellBasedSimulation` to be serialized more easily. This removed the need for the `CryptSimulationArchiver` class, which has been removed: simply use` CellBasedSimulationArchiver` instead.
* Added methods to get the centre of mass and dimensions of a cell population to `CellBasedSimulationWithPdes`.
* Added methods to `NodesOnlyMesh` to allow removal of nodes.


----

## Release 2.3 (changes since Release 2.2)

### Headline features

#### General

* Support for the latest version of CVODE (2.6.0)
* Reduced source download size (mainly through a reduction in the amount of data distributed with tests)


#### Cardiac

* A simple model of drug conductance block is now available in the standalone executable.
* A sequential implementation of adaptive mesh refinement has been added, using a library developed in collaboration with Imperial College London to reduce the computational load and memory footprint of large simulations.  This is not available within the standalone executable however.  Instructions for installing the required library are available on the Chaste wiki at InstallAdaptivityLibrary, and you will need to edit your hostconfig file to turn on support in Chaste (by setting `use_adaptivity = True` and adding appropriate paths etc.).


### New functionality & major code changes

#### General

* Archiving of ODE systems with parameters has been improved.  You can now add parameters without breaking archive backwards compatibility.
* A mixed-dimension mesh format has been defined and implemented (see the `MixedDimensionMesh` class) as the first step towards incorporating a Purkinje model in Chaste.
* Further improvements to the compressible elasticity solver (although this is still in the process of being implemented).


#### Cardiac

* Added an optional `ApplyDrug` element to the `Physiological` section of the XML parameters file.  This applies conductance block model to as many channels as required.  Note that conductances to block must be annotated in the CellML file with oxmeta names and as modifiable parameters.  This has been done for the LR91 model as an example.  If a channel is not found in the CellML file, a warning will be generated (once per node...).
    * **NB** This means that the parameter already in the LR91 model has changed name, which breaks archive backwards compatibility.  Run the `archive_convert.sed` script on your archives to make them usable again.  e.g. "`find . -name *arch.? -print | xargs sed -i -f archive_convert.sed`"
* The cardiac post-processing performance has been improved through greater use of caching.
* Alternative material laws for mechanics can now be set from a test (see the tutorials for an example).


### Code interface changes, which may require changes to user code

#### General

* The interface of `AbstractCvodeCell` has been changed to be more like `AbstractCardiacCell`.
    * Moved `SetStateVariables` to `AbstractParameterisedSystem`. This means that its behaviour for `AbstractCvodeCell` has changed: it just copies the contents now, rather than handing over ownership of the vector. So callers must now delete the vector they pass to this method.
        * Hence removed `AbstractCvodeCell::SetStateVariablesUsingACopyOfThisVector` - use `SetStateVariables` instead.
    * Moved initial conditions methods (`GetInitialConditions`, `SetDefaultInitialConditions`, `SetDefaultInitialCondition`, and `ResetToInitialConditions`) to `AbstractParameterisedSystem`.
    * Added helper functions `CreateVectorIfEmpty`, `CopyToStdVector`, and `CopyFromStdVector` to `VectorHelperFunctions.hpp`.
* Made `CalculateOnElement` public in `AbstractFunctionalCalculator` so users can compute contributions to integrals on each element.


#### Cardiac
#### Cell-based

* `NodeBasedCellPopulation` constructors now take in a `NodesOnlyMesh` instead of a vector of nodes.


-----

## Release 2.2 (changes since Release 2.1)

### Headline features

#### General

* Full default test pack should now pass on more configurations.
* Smarter chunking in HDF5 should reduce the time spent on I/O significantly for simulations with many output time steps.
* Mesh load is scalable in parallel only with our binary mesh format.  A conversion utility is provided.  Please refer to the MeshConvert tutorial.
* Performance of checkpointing with large meshes has been improved. We now archive permuted meshes without writing from memory to disc; instead the original files are copied.
* Further improvements to tutorials (including the addition of solid mechanics tutorials), and user documentation.  Executable tutorials (as well as tutorial tests) are now routinely tested.


#### Cardiac

* Added support for the definition of multiple bath/tissue regions. Based on whichever convention you followed in the elements file, you can inform Chaste of your choice of region identifiers with `HeartConfig::SetTissueIdentifiers(std::set<unsigned> )` and `HeartConfig::SetBathIdentifiers(std::set<unsigned> )`. One can also assign different conductivities to different bath regions with `HeartConfig::SetBathMultipleConductivities(std::map<unsigned, double> )`.
* State variable interpolation may now be used for cardiac simulations.  This can lead to improved conduction velocity accuracy on meshes with spatial resolutions typically used in simulation studies, and has been implemented in an efficient manner. See ChasteGuides/StateVariableInterpolation for more details.
* It is now possible to output visualisation in parallel VTK (.pvtu) format. To do this you need to set the `parallel_vtk` attribute to "yes" in the `OutputVisualizer` element in the parameters file.
* Fixed bug in fibre direction heterogeneities: when running in parallel some fibre directions were permuted between elements.  (This bug did not exist prior to release 2.1.)
* Fixed bug with conductivity heterogeneities in 1D and 2D causing a 'boost::numeric::ublas::bad_size' error.
* User may now specify a list of node indices where time traces of output variables are requested (see below for details).
* A (Strang) operator splitting solver has been implemented for monodomain. This is mainly for comparison of numerical methods - it is neither the default solver nor optimised. It can be switched on using the `HeartConfig` class: `HeartConfig::Instance()->SetUseDiffusionReactionOperatorSplitting()`.


#### Cell-based

* A new class `CylindricalHoneycombMeshGenerator` has been created and the existing `HoneycombMeshGenerator` class simplified. This included changing the arguments in the `HoneycombMeshGenerator` constructor. Also the class `HoneycombMutableVertexMeshGenerator` has been merged into `HoneycombVertexMeshGenerator` and the associated method `GetMutableMesh` renamed to `GetMesh` for consistency with the cell-centre code. These changes will break user projects.
* A new cell population boundary condition class hierarchy has been handled, to deal with boundary conditions for cell movement. Such objects are passed to and stored in a `CellBasedSimulation` object in a similar way to forces and cell killers.
* We have extended VTK functionality to allow for point data output from node- and mesh-based cell simulations for visualization in Paraview.
* We have updated user tutorials and added new tutorial on using cell population boundary condition objects.
* It has been made clear what code is needed in concrete `CreateCellCycleModel` methods.



### New functionality & major code changes

#### General

* We have a new algorithm for random samples from the normal distribution in the `RandomNumberGenerator`, for increased stability at very large numbers of calls. Any results dependent on this will change, even with the same seed.
* "Infrastructure tests" such as checking copyright notices and for duplicate file names are now not run by default (i.e. `do_inf_tests=0` is now the default setting), unless you have `do_inf_tests=1` in your hostconfig file.
* Some new helper methods have been added to `OutputFileHandler` and `FileFinder`:
    * `OutputFileHandler::FindFile` - get a `FileFinder` for a file in the output directory
    * `OutputFileHandler::CopyFileTo` - copy a file to the output directory
    * `FileFinder::GetLeafName` - get the leaf name of a file
* Support has been added for Boost version 1.44. However, note that due to a bug in this Boost version, many tests will crash after they have finished running (with the message "pure virtual method called. terminate called without an active exception")!
* A new header `SmartPointers.hpp` has been added containing a few helpful macros for working with `boost::shared_ptr`.
* Created new helper classes `PetscVecTools` and `PetscMatTools` in `linalg` that encapsulate many of the PETSc functions we use related to vectors and matrices. This isolates much of the PETSc-version-specific code within these classes, enabling cleaner user code. If new PETSc-version-specific code is written, suitable methods should be added to these classes in preference to using PETSc directly.
* Added named attribute functionality to `AbstractParameterisedSystem`, allowing arbitrary real-valued attributes to be attached to ODE classes. This is used by PyCml to support named attributes on CellML models.  Also added `Has...` methods to ODE system information, to avoid the need for `try...catch` statements in generic code.
* Changed the event handler classes to use `MPI_Wtime` rather than `std::clock` as underlying timer. This will give a more accurate wall clock time.
* Time adaptivity can now be implemented for PDE solvers by writing an `AbstractTimeAdaptivityController` subclass. `TestMonodomainWithTimeAdaptivity` does some very simple adaptivity to demonstrate this.
* Reduced parallel overhead associated with assembling PETSc objects. Since Chaste (almost always) ensures that data is generated only on the local process (and the helper methods in `PetscVecTools` and `PetscMatTools` enforce this), no data migration is required. We therefore by default set the PETSc option not to check whether migration is needed (`{VEC,MAT}_IGNORE_OFF_PROC_ENTRIES`).
* ODE solvers now inherit from `Identifiable` in order to provide reflection, so that the solver used can be written to results files by `OdeSolution`. Unfortunately, this means that on older Boost versions (<1.37) you need to include `CheckpointArchiveTypes.hpp` in any test which solves an ODE system to obtain an `OdeSolution` object, or you'll experience a segfault!


#### Cardiac

* New options in the XML parameters file:
    * A user may now specify a list of node indices where time traces of output variables are requested.  See `/heart/test/data/ChasteParametersFullFormat.xml` for an example of usage and the documentation of `PostProcessingWriter::WriteVariablesOverTimeAtNodes` for further information. The output files (one file per output variable) will have the nodal time traces arranged in columns (gnuplot-friendly), one column per requested node. The node numbers that the user requests are referred to the original (unpermuted) node numbering (hence it may differ from what the user sees - for example - when visualizing the output of a previous parallel simulation). No matter what permutation is used in the simulation, the output of the requested nodes will be the same.
    * A new post-processing step to calculate pseudo-ECGs has been added to the Chaste parameters file: the `PseudoEcgElectrodePosition` element, which specifies where the virtual probe electrode should be placed. This element may occur multiple times to calculate ECGs from different probe locations. Note that probe electrodes must be located outside the heart tissue!
    * A `MeshPartitioning` element has been added in the `Numerical` parameters section, allowing you to specify how a mesh gets partitioned in parallel (dumb/metis/parmetis/petsc). This maps to the `HeartConfig` methods `Set/GetMeshPartitioning`.
    * Stimuli section can use ellipsoid regions.
* Explicit instantiation is now used for `CardiacSimulationArchiver`, allowing this class and `CardiacSimulation` to be split into `.hpp` and `.cpp` files. This improves compile times (especially for the Intel compiler) but may break some projects or tests which use checkpointing when run with older Boost versions (<1.37).
* Various improvements to cell model generation from CellML:
    * Lookup table settings (table bounds and step size) can now be modified at run-time, not just code generation time. There is a new `AbstractLookupTableCollection` base class for lookup tables that provides this functionality, with a get method on `AbstractCardiacCellInterface` that is overridden by subclasses providing tables.
    * There have been some improvements to the performance of various cell model optimisations. Some are not yet enabled by default (PyCml flags `--include-dt-in-tables`, `--combine-commutative-tables`, `--no-member-vars`, `--pe-convert-power`) and others are "unsafe in general" (PyCml flag `--no-check-lt-bounds`).
    * Conversion issues between cardiac cell models and Chaste are now handled in a more generic fashion within PyCml by creating an interface component. This ensures that all quantities read or written by the Chaste tissue model, including ionic currents, are in the correct units.
    * There is now a constructor options which allows the cell model converter (`CellMLToSharedLibraryConverter`) to save generated C++ source files for inspection.
    * A new option `--expose-annotated-variables` has been added to PyCml, which exposes all oxmeta-annotated variables to the `GetAnyVariable` functionality, i.e. it annotates non-state variables as parameters or derived quantities, as appropriate.  There is also an `--expose-all-variables` option, which annotates every variable in the model.
    * Allowed certain computed variables (those which can be determined not to vary at run-time) to be metadata annotated constants. In particular, this allows the default stimulus current amplitude to be calculated within the cell model, rather than given as a fixed constant number.
    * Used the new named attribute functionality on `AbstractParameterisedSystem` to support named attributes on CellML models.
* Dedicated S1-S2 and dynamic restitution stimuli classes (mainly for single cell work) have been brought into the main trunk from a user project.
* Added `Has...` methods to cardiac modifiers, to avoid the need for `try...catch` statements in generic code.
* Implemented `SolveAndUpdateState` for backward Euler cells.
* The interface for `CardiacElectroMechanicsProblem` (and `CardiacElectroMechProbRegularGeom`) has changed slightly, instead of taking in the number of electrics solves per mechanics solve, it takes in the mechanics solve timestep (which should be a multiple of the electrics PDE solve).


#### Cell-based

* See above under "Headline features".


### Code interface changes that may require changes to user code

#### General

* The interface to the `SimpleLinearParabolicSolver` has changed: instead of calling `SetTimes(t0,t1,dt)`, you have to call two methods `SetTimes(t0,t1)` and `SetTimeStep(dt)`.
* `DistributedVectorFactory` now always sets `mpOriginalFactory` when loaded from an archive.
* Moved the partitioning type into its own header file, rather than being nested in `DistributedTetrahedralMesh`. You just need to change (e.g.) `DistributedTetrahedralMesh<1,1>::DUMB` to `DistributedTetrahedralMeshPartitionType::DUMB`.


#### Cardiac

* `VerifyStateVariables` is now not called in `NDEBUG` builds, which may lead to tests not 'failing' in optimised builds.
* Added an optional parameter `pStateVariables` to `GetIIonic`, which gives the state at which to evaluate the current. This will require a change to any manually written cell model to match the new interface.


#### Cell-based

* Every cell cycle model now needs an `OutputCellCycleModelParameters` method.  See existing models for what it should include.






-----


## Release 2.1 (changes since Release 2.0)

* [cell_based] All `CellKiller` classes now require a `OutputCellKillerParameters` method (r10687).
* [cell_based]  #1582 `CellBasedSimulation` and inherited classes now do not take in a force collection. To set the mechanics system call the `AddForce` Method.
* [cell_based] #1496: prior to restructuring how model parameters are accessed in the cell-based code, all of the `TissueConfig` members have been moved into the classes in which they are used.
* [heart] #1516: Cardiac PDE classes (which longer contain PDE information) have now been renamed to be tissues, e.g. `BidomainPde` is now `BidomainTissue`. Archives that used to contain a PDE will also change (and will **not** be backward compatible giving the error `unregistered class`). Old archives can be converted to the new format by replacing anything that says `Pde` with `Tissue` and by incrementing the integer immediately before the PDE name by 3. This can be done by typing the following two commands in the archive directory.

```

sed -i s/'39 pack<void (MonodomainPde<'/'42 pack<void (MonodomainTissue<'/ archive.arch
sed -i s/'35 pack<void (BidomainPde<'/'38 pack<void (BidomainTissue</'/ archive.arch


```

If you have the source, you can just run the sed script, `archive_convert.sed` located in the main Chaste directory, that can convert archives to the new format. Run it as

```

sed -i -f archive_convert.sed archive_file1 archive_file2 ...

```


* [heart] #1495: APD calculation has changed so that it detects the resting potential, and therefore upstroke, more accurately. APDs will change slightly when run with the new version of the code.
* [cell_based] #1294 As of r8949 the variables in `TissueConfig.hpp` relating to cell centre models have had the prefix `Meineke` added this may affect some user projects
* [mesh][cell_based,] #1075: As of r8771, the `mesh` classes `Face`, `VoronoiCell`, `VoronoiTessellation` and `InventorVoronoiWriter` have been deleted. This is because they are no longer used in the code. Now, when a `MeshBasedTissue` is required to construct the Voronoi tessellation that is dual to its mesh, this is stored as a `VertexMesh`. The main difference is how the `MeshBasedTissue` then accesses information about the Voronoi tessellation. Users should replace `MeshBasedTissue` calls to `rGetVoronoiTessellation().GetFaceArea()` with `GetAreaOfVoronoiElement()`, calls to `rGetVoronoiTessellation().GetFacePerimeter()` with `GetPerimeterOfVoronoiElement()`, and calls to `rGetVoronoiTessellation().GetEdgeLength()` with `GetVoronoiEdgeLength()`.
* [cell_based] #1075: `TissueConfig` members `mOutputCellAreas` and `mOutputTissueAreas` renamed to `mOutputCellVolumes` and `mOutputTissueVolumes` respectively; similarly for their get/set methods. `MeshBasedTissue` methods `SetOutputTissueAreas()`, `WriteTissueAreaResultsToFile()`, `WriteCellAreaResultsToFile()` similarly renamed. `VertexMesh` method `SolveVoronoiElementIndexMapping()` renamed to `GetVoronoiElementIndexCorrespondingToDelaunayNodeIndex()`. See r8794 and r8806.
* [cell_based] #1075/#1372: As of r8946, when a `MeshBasedTissue` creates a Voronoi tessellation, this is constructed out of all nodes in the mesh, including ghost nodes.
* [cell_based] #1276: Merged `VertexMesh` method `GetPerimeterOfVoronoiElement()` into `GetSurfaceAreaOfVoronoiElement()` and `GetAreaOfVoronoiElement()` into `GetVolumeOfVoronoiElement()` in r8968.
* [cell_based] #1375: Changed `MeshBasedTissue` method `rGetVoronoiTessellation()` to `GetVoronoiTessellation()` (i.e. return a pointer rather than a reference) in r8980 to avoid memory issues.
* [cell_based] #1267: As of r9002, `APOPTOTIC` is no longer a `CellProliferativeType` but has been replaced with a new class `ApoptoticCellMutationState` (this will eventually become a cell property - see #1285).
* [cell_based] #1419: `CellwiseData` has been generalised to cope with vertex-based tissues; some of its methods have changed names or arguments (see r9220)
* [cell_based] #1279: we now create and access `TissueCell` objects via Boost shared pointers, and have created the shorthand `TissueCellPtr`; the `TissueCell` copy constructor, `operator=` and method `CommonCopy()`  have been removed, and many methods that previously took in or returned `TissueCell`s now deal with `TissueCellPtr`s (r9542).
* [cell_based] #1285: the classes `Alarcon2004OxygenBasedCellCycleOdeSystem` and `Alarcon2004OxygenBasedCellCycleModel` have been modified (instead of storing a cell's mutation state, now they just store whether it is has the cell property `CellLabel`) - see r9657.
* [cell_based] #1285: Added classes `AbstractCellProperty`, `CellPropertyCollection` and `CellPropertyRegistry` (which replaces `CellMutationStateRegistry`). A `TissueCell` now has a `CellPropertyCollection` member, in which it stores its mutation state (which now inherits from `AbstractCellProperty`) as well as any other cell property the user chooses. Cell properties can be passed into the `TissueCell` constructor or using the new method `AddCellProperty()`. Similarly there are new methods `RemoveCellProperty()` and `rGetCellPropertyCollection()` on `TissueCell`. The mutation states `LabelledCellMutationState` and `ApoptoticCellMutationState` have been replaced with new cell property classes `CellLabel` and `ApoptoticCellProperty`. The output of some `Tissue` methods, such as `GetCellMutationStateCount()`, have been changed. See r9699, r9709, r9712, r9719, r9737.
* [core] r9858: assembler hierarchy completely changed and replaced with new assemblers and new solvers. See ChasteGuides/FiniteElementAssemblersAndSolvers. * [cell_based] #1496: prior to restructuring how model parameters are accessed in the cell-based code, many of the `TissueConfig` members have been moved into the classes in which they are used (see r9751, r9781, r9785, r9802)
* [cell_based] #1285: if writing cell mutation states to the file `cellmutationstates.dat` in a `TissueSimulation`, the name of each mutation state present is now taken from its extended type ID info using a new method `AbstractCellProperty::GetIdentifier()` (see r9766)
* [cell_based] #1427: added `AbstractCellCycleModelOdeSolver` and concrete singleton implementation `CellCycleModelOdeSolver` and use in ODE-based cell cycle models (r9839, r9905); default ODE-based cell cycle model constructors now take in an optional `shared_ptr<AbstractCellCycleModelOdeSolver>`, allowing the user to specify what ODE solver to use (r9875)
* [cell_based] #1491: cell cycle models have been made `noncopyable`, since cells are `noncopyable` (r10007)
* [cell_based] Removed unused `Alarcon2004OxygenBasedCellCycleModel` member variable `mIsLabelled` (r10007)
* [cell_based] All tissue classes now require a `OutputTissueParameters` method (r10071)
* [cell_based] All force classes now require a `OutputForceParameters` method (r10077)
* [cell_based] #1051: to reflect the general nature of the classes, we have renamed `TissueCell` to `Cell`, `Tissue` to `CellPopulation` and `TissueSimulation` to `CellBasedSimulation` - see r10212 (needless to say, this will break user projects).


-----

## Release 2.0 (changes since Release 1.1)
See `/docs/ReleaseNotes.html` for the definitive list.

* In the AssemblerTraits struct, the typenames 'CVT_CLS', 'CMT_CLS' and 'INTERPOLATE_CLS' have been renamed to 'CVT_CLASS', 'CMT_CLASS' and 'INTERPOLATE_CLASS' (r7041). These stand for 'ComputeVectorTerm class', 'ComputeMatrixTerm class' and 'Interpolate class' in case you are wondering, and the AssemblerTraits struct is used to state which classes these methods are implemented in.
* [executable][heart] The Chaste parameters file now uses an XML namespace to indicate which version of Chaste it is for.  This means that there are now multiple schemas in `heart/src/io`, one for release 1.1 and one for release 1.2.  To update your parameters XML files, simply add a namespace declaration by adding the following attributes to the root `ChasteParameters` element:
     
```

       xmlns="https://chaste.comlab.ox.ac.uk/nss/parameters/1_2"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="https://chaste.comlab.ox.ac.uk/nss/parameters/1_2 heart/src/io/ChasteParameters_1_2.xsd"
     
```

     See `ChasteParameters.xml` in the Chaste source folder for an example.  Chaste should still be able to read old parameters files, but you will need to use the new version to take advantage of new features (such as postprocessing and checkpointing).
* Chaste now has a YouTube channel for funky movies: http://www.youtube.com/user/ChasteProject
* [heart] #1169 r7350 changes the boundary conditions container in cardiac problem classes to be a `boost::shared_ptr`.  The PDE assembler hierarchy is still using normal pointers, however, so this should only affect people creating cardiac problem subclasses, or setting their own boundary conditions for cardiac problems: if you do these, you'll need to use a shared pointer instead.
* [heart] #1163 r7435 : what format to convert HDF5 output to can now be specified in the XML configuration file (using the `OutputVisualizer` element), and hence via `HeartConfig`.  The methods `ConvertOutputToMeshalyzerFormat`, `ConvertOutputToCmguiFormat` and `ConvertOutputToVtkFormat` have thus been removed from `AbstractCardiacProblem`.  Code using these should change to use the methods `SetVisualizeWithMeshalyzer`, `SetVisualizeWithCmgui` or `SetVisualizeWithVtk` on `HeartConfig`.  As part of this change, the default behaviour has also changed to outputting meshalyzer data; if you don't want this you have to explicitly turn it off.  There is an unfortunate conflict between visualizer output and outputting cell model state variables - you can't do both!  Calling `SetOutputVariables` on `HeartConfig` will automatically turn off visualizer output.  If you specify `OutputVariables` in the XML configuration file, however, you are responsible for also including an `<OutputVisualizer meshalyzer="no"/>` element.
* [cancer] #1175 (r7544, r7562): changed `cancer` folder to `cell_based` and `notforrelease_cancer` to `notforrelease_cell_based`. Think anyone using the `cancer` code in their user project will need to do a search and replace `cancer -> cell_based` in their SConscript file. If you still have `cancer` or `notforrelease_cancer` folders in your chaste directory after updating you may need to remove them manually.
* [cell_based] In r7885 changed the name of `TissueConfig::Get/SetTopOfLinearWntGradient()` to `Get/SetWntConcentrationParameter()`, so that an exponential Wnt concentration could be added.
* [ode] In r8000 changed `OdeSolution::WriteToFile()` so that it no longer takes the `AbstractOdeSystem` as an argument.
* [heart] #1164: the cardiac executable is gaining the ability to automatically load cell models encoded as CellML files at run-time, rather than needing them to be incorporated within Chaste when it is compiled.  In order to take advantage of this, you need (at present) to have built the executable from source yourself, as it uses your Chaste source tree to convert the CellML file into runnable code.  A side effect of this is that the continuous test pack now requires the prerequisites for PyCml to be installed in order for the tests of this new functionality to pass.  See [InstallPyCml](https://chaste.cs.ox.ac.uk/trac/wiki/InstallPyCml) for installation instructions.
* [cancer] If you were implementing serialization for classes, note that the interface has changed. The file `TemplatedExport.hpp` has been replaced with two files: `SerializationExportWrapper.hpp` and `SerializationExportWrapperForCpp.hpp`. You should include the first in .hpp files, after the class definition. The second should be included in .cpp files, after any other includes (I suggest putting it at the end of the file for consistency). In both cases, a suitable `CHASTE_CLASS_EXPORT` line should be used, the same in both .hpp and .cpp. (There are also the usual variant macros for common cases of templated classes.) See ChasteGuides/BoostSerialization for more info.
* [cell_based] #1145: The `CryptCellMutationState` enumeration has been replaced by a hierarchy of classes inheriting from `AbstractCellMutationState`. `TissueCell`s now have a shared pointer to a mutation state. To ensure proper counting of cells with each mutation, make sure that you give a cell a mutation state from its tissue's registry (`AbstractTissue::GetMutationRegistry`). Also, when passing a vector of cells to a tissue constructor, the passed-in vector is now cleared, to emphasize that these cells become owned by the tissue. Also removed `AbstractTissue::mCellMutationStateCount` and, as a result, changed `rGetCellMutationStateCount()` to `GetCellMutationStateCount()`.
* [cell_based] #1112: The `CellsGenerator` class hierarchy has been refactored to reduce code duplication. There is now a base class `CellsGenerator`, which is templated over cell cycle model classes and dimension, and comprises `GenerateBasic()` and `GenerateGivenLocationIndices()` methods; and a subclass `CryptCellsGenerator`, which has an additional method `Generate()` that sets up cells for a crypt simulation.
* [cell_based] To reduce the number of calls to `CreateCellPair`, the `MeshBasedTissue` methods `IsMarkedSpring`, `MarkSpring` and `UnmarkSpring` no longer call the `CreateCellPair` method, and now take in a reference to a `std::set<TissueCell*>` instead two `TissueCell` references (r8508).
* [cell_based] #1239: An extra cell cycle model class, `AbstractOdeBasedCellCycleModelWithStoppingEvent`, has been inserted into the cell cycle model hierarchy.
* [cell_based] #1276: `mesh` now contains an extra folder `vertex`, which includes classes for the construction and reading/writing of 'vertex meshes' (these are meshes in which the number of nodes per element is unrestricted) as well as associated tests.
* [cell_based] `AbstractCryptStatistics::GetWhetherCryptSectionCellsAreLabelled` renamed `AreCryptSectionCellsLabelled`
* [mesh] #1182: r8436 switches parMETIS partitioning on. METIS dependencies are replaced with parMETIS ones.
* TODO: talk about checkpointing, postprocessing, metadata, use of CVODE for single cell, and any other new features


-----

## Release 1.1 (changes since Release 1.0)
See `/docs/ReleaseNotes.html` for the definitive list.

* Improved doxygen documentation.
* Improved code portability.
    * (Some of) Chaste can now be run under Cygwin; see the ChasteInstallationOnCygwin wiki page for details.
    * Chaste now uses version 3.2.0 of [XSD](http://www.codesynthesis.com/products/xsd/) (although 2.3.1 and 3.1.1a3 are also supported for now).
* Interface changes that may require changes to user code:
    * Triangle and tetgen binaries no longer included with the code and must be installed and set in the `PATH`.  Most re-meshing still works since 2D re-mesh compiles Triangle code from source (which is included).
    * `this->mpMesh` is no longer directly available to cell factories, as it can be used accidentally while unset. Use the `GetMesh()` method instead.
    * `MonodomainProblem` is now templated on both `ELEMENT_DIM` and `SPACE_DIM`. It will default to using `ELEMENT_DIM = SPACE_DIM` if only one is supplied.
    * Cardiac cell models are now constructed using `boost::shared_ptr<>` instead of normal pointers for the 'stimulus' and 'ode solver' arguments (changes to `CellFactories`).
    * The `CancerParameters` singleton class has been renamed `TissueConfig` (to match the heart code).
    * `cancer/src/tissue/MeshArchiveInfo` has been replaced by `global/src/ArchiveLocationInfo`, which has slightly different usage.
    * Renamed `PetscTools::NumProcs` to `PetscTools::GetNumProcs`.
    * It is now impossible to create vectors (either PETSc `Vec`s or `DistributedVector`s) directly from a `DistributedVector`.  This must now be done via a `DistributedVectorFactory`.  If you have a mesh, a factory can be obtained using the `GetDistributedVectorFactory` method.  The cardiac PDEs also store a factory.
    * Static iterators are not available anymore in `DistributedVector`. You can access the iterator from a `DistributedVector` object. If there isn't one in scope, use `GetLow()` and `GetHigh()` in `DistributedVectorFactory` (accessible via any mesh object).
    * `#include` policy has changed. It might be the case that tests that used to compile are unable to find certain header files now. Please `#include` them as needed.
    * For a dynamic assembler, if the matrix is constant you must now call `this->SetMatrixIsConstant()` in the constructor otherwise the matrix will now be assembled each timestep. If your matrix is not constant in time, you were getting wrong answers before!
    * `CancerParameters` singleton class has been renamed to `TissueConfig`
    * In cancer, `WntConcentration` is now templated over dimension. You will have to pass in the dimension when constructing any Wnt-dependent cell cycle model.
    * `SloughingCellKiller` is also now templated over dimension.
    * `FixedCellCycleModel`, `StochasticCellCycleModel`, and the two corresponding `CellGenerators` have been renamed.
    * Renamed `AbstractMesh` to `AbstractTetrahedralMesh`, there is a new `AbstractMesh` class, which will handle non-tetrahedral meshes.
* Bidomain problems with Neumann intracellular stimuli shouldn't have a solution, and there was an implementation error before which allowed them to be solved. This has been fixed, so any test with Neumann stimuli will not work. The stimulus has to be changed to a (standard) volume stimulus.
* PyCml is now included in the main Chaste trunk (python/pycml).
* xsd should be defined in your hostconfig file (if it isn't on your `PATH`) in the form 
```
tools = {'xsd':'FILL_IN_PATH_TO_XSD_BINARY'
```
} as it regenerates `ChasteParameters.hpp/cpp` in `SConstruct`
* Bidomain problems with Neumann intracellular stimuli shouldn't have a solution, and there was an implementation error before which allowed them to be solved. This has been fixed, so all intracellular stimuli need to be volume stimuli now.
* Several helper macros have been written for debugging, see global/Debug.hpp.
* For `ELEMENT_DIM == 1` (in any `SPACE_DIM`) `MeshalyzerMeshWriter` will now output a .cnnx file rather than a .tri file for element connections.
* Added a `CombinedOdeSystem` class for simple coupling of ODE systems.
* `TimeStepper::GetTimeStepsElapsed()` has now become `TimeStepper::GetTotalTimeStepsTaken()`


