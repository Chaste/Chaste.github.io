---
title: "How-to index"
description: "Chaste how-tos, automatically generated from the test files"
draft: false
images: []
toc: true
layout: "single"
---

As well as ensuring that Chaste functions as expected, the many Chaste tests can be effective for learning how to use Chaste.
There are often aspects of Chaste's capabilities that do not warrant a full user tutorial, but are still worth noting.
Equally, users often ask "how do I do...", and in many cases there is already a test that does something similar and can be used as a basis.

This page contains a (probably partial) index of links to useful code.
Some of the links are to code in tutorials.
The others are links to test code.
For the latter, note that since tests are written primarily for checking functionality, they are not commented to the same degree as user tutorials.
Nevertheless, they should be reasonably readable and useful.

Note that this page is generated automatically based on tags in the Chaste code.
Do not edit it manually, as your changes will be overwritten!

## Cardiac

### Cell Models
- Get a cardiac cell model to (roughly) a steady state, given a regular stimulus, using the `SteadyStateRunner` class.
  - [line 98 of TestSteadyStateRunner.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/ionicmodels/TestSteadyStateRunner.hpp#L98)

### Electro-mechanics
- Set heterogeneous contraction models by using a contraction cell factory.
  - [line 148 of TestAbstractContractionCellFactory.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/TestAbstractContractionCellFactory.hpp#L148)
- Run electro-mechanics with mechano-electric feedback
  - [line 100 of TestAnotherCardiacElectroMechanicsTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/tutorials/TestAnotherCardiacElectroMechanicsTutorial.hpp#L100)
- Run electro-mechanics with inflation pressures
  - [line 270 of TestAnotherCardiacElectroMechanicsTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/tutorials/TestAnotherCardiacElectroMechanicsTutorial.hpp#L270)
- Run electro-mechanical simulations using bidomain instead of monodomain
  - [line 215 of TestCardiacElectroMechanicsProblem.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/mechanics/TestCardiacElectroMechanicsProblem.hpp#L215)
- Run basic electro-mechanics simulations; specify different models, boundary conditions, fibres
  - [line 117 of TestCardiacElectroMechanicsTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/tutorials/TestCardiacElectroMechanicsTutorial.hpp#L117)
- Visualise results in Cmgui (very brief description)
  - [line 205 of TestCardiacElectroMechanicsTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/tutorials/TestCardiacElectroMechanicsTutorial.hpp#L205)

### Output
- Specify output formats (for different visualisers)
  - [line 136 of TestAnotherBidomainSimulationTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/tutorials/TestAnotherBidomainSimulationTutorial.hpp#L136)
- Collect and print timings to benchmark different parts of the cardiac code.
  - [line 124 of TestBidomain3D.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/bidomain/TestBidomain3D.hpp#L124)
- Only output data for particular nodes
  - [line 578 of TestBidomainProblem.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/bidomain/TestBidomainProblem.hpp#L578)
- Output data using a light-weight output modifier.  This can be used in addition to regular HDF5 output or can replace it.
  - [line 588 of TestBidomainProblem.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/bidomain/TestBidomainProblem.hpp#L588)
- Output all cell model state variables for the cell model used in a particular simulation
  - [line 951 of TestBidomainProblem.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/bidomain/TestBidomainProblem.hpp#L951)
- Use the `SingleTraceOutputModifier` to output based on a global index (index AFTER any permutation has been applied)
  - [line 1046 of TestBidomainProblem.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/bidomain/TestBidomainProblem.hpp#L1046)
- Calculating and outputting ionic currents ('derived quantities') in a single cell simulation using [OdeSolution](/doxygen-latest/classOdeSolution.html) - see also [chaste_codegen documentation](/docs/user-guides/code-generation-from-cellml/#derived-quantities).
  - [line 395 of TestCvodeCells.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/ionicmodels/TestCvodeCells.hpp#L395)
- Calculating and outputting ionic currents ('derived quantities') in a tissue simulation using [HeartConfig](/doxygen-latest/classHeartConfig.html) - see also [chaste_codegen documentation](/docs/user-guides/code-generation-from-cellml/#derived-quantities).
  - [line 236 of TestMonodomainProblem.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/monodomain/TestMonodomainProblem.hpp#L236)
- On large-scale parallel simulations it is advantageous to cache HDF5 output and only write to disk at end of simulation (or at checkpoint).  This is achieved with `SetUseHdf5DataWriterCache()`
  - [line 1648 of TestMonodomainProblem.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/monodomain/TestMonodomainProblem.hpp#L1648)

### Post-processing
- Compute action potential properties (APD50, APD90, max upstroke velocities, etc) given voltage traces.
  - [line 56 of TestCellProperties.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/postprocessing/TestCellProperties.hpp#L56)
- Convert already generated simulation (HDF5) results to text, VTK or Meshalyzer format.
  - [line 64 of TestHdf5Converters.hpp](https://github.com/Chaste/Chaste/blob/develop/pde/test/utilities/TestHdf5Converters.hpp#L64)
- Convert already generated simulation (HDF5) results to Cmgui format.
  - [line 61 of TestHdf5ToVisualizerConverters.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/postprocessing/TestHdf5ToVisualizerConverters.hpp#L61)
- Compute pseudo-ECGs
  - [line 59 of TestPseudoEcgCalculator.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/postprocessing/TestPseudoEcgCalculator.hpp#L59)

### Problem definition
- Use a CVODE adaptor solver in a tissue simulation
  - [line 121 of Test1dMonodomainShannonCvodeBenchmarks.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/performance/Test1dMonodomainShannonCvodeBenchmarks.hpp#L121)
- Use a native CVODE cell in a tissue simulation
  - [line 168 of Test1dMonodomainShannonCvodeBenchmarks.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/performance/Test1dMonodomainShannonCvodeBenchmarks.hpp#L168)
- Specify fibre directions
  - [line 90 of TestAnotherBidomainSimulationTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/tutorials/TestAnotherBidomainSimulationTutorial.hpp#L90)
- Fix phi_e at particular nodes (note: this is not required)
  - [line 264 of TestBidomainProblem.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/bidomain/TestBidomainProblem.hpp#L264)
- Set discrete **ellipsoid** areas to have heterogeneous (intra- and/or extra-cellular) conductivity tensors.
  - [line 325 of TestBidomainTissue.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/bidomain/TestBidomainTissue.hpp#L325)
- Run bidomain simulations with a perfusing bath, and apply shocks using electrodes
  - [line 47 of TestBidomainWithBathTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/tutorials/TestBidomainWithBathTutorial.hpp#L47)
- Tell Chaste that a mesh has been modified
  - [line 174 of TestBidomainWithBathTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/tutorials/TestBidomainWithBathTutorial.hpp#L174)
- Save ('checkpoint') and reload simulations
  - [line 49 of TestCardiacCheckpointingAndRestartingTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/tutorials/TestCardiacCheckpointingAndRestartingTutorial.hpp#L49)
- Do a monodomain simulation with equivalent conductivities to a bidomain simulation.
  - [line 172 of TestEquivalentMonoAndBidomainTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/tutorials/TestEquivalentMonoAndBidomainTutorial.hpp#L172)
- Set discrete **cuboid** areas to have heterogeneous (intra- and/or extra-cellular) conductivity tensors.
  - [line 82 of TestHeterogeneousConductivities.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/TestHeterogeneousConductivities.hpp#L82)
- Generate a slab (cuboid) mesh rather than read a mesh in, and pass it to solver
  - [line 102 of TestMonodomain3dExampleTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/tutorials/TestMonodomain3dExampleTutorial.hpp#L102)
- Read in a mesh from file, via `HeartConfig`.
  - [line 114 of TestMonodomain3dRabbitHeartTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/tutorials/TestMonodomain3dRabbitHeartTutorial.hpp#L114)
- Use a genuinely Neumann intracellular stimulus, rather than default volume stimulus
  - [line 54 of TestNeumannStimulus.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/stimuli/TestNeumannStimulus.hpp#L54)
- Set up and run basic bidomain simulations
  - [line 48 of TestRunningBidomainSimulationsTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/tutorials/TestRunningBidomainSimulationsTutorial.hpp#L48)
- Use different cell models, defined using CellML files
  - [line 74 of TestRunningBidomainSimulationsTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/tutorials/TestRunningBidomainSimulationsTutorial.hpp#L74)
- Generate fibre field definitions for cardiac geometries using a mathematical rule approach
  - [line 48 of TestStreeterFibreGenerator.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/fibres/TestStreeterFibreGenerator.hpp#L48)

### Solver
- Using specialised Backward Euler implementation to solve the cell models (allows for much larger timesteps)
  - [line 64 of TestBidomainWithBathTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/tutorials/TestBidomainWithBathTutorial.hpp#L64)
- Use [state-variable interpolation](/docs/user-guides/state-variable-interpolation/) to improve accuracy
  - [line 118 of TestBidomainWithSvi.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/bidomain/TestBidomainWithSvi.hpp#L118)
- Run using (simple, user-defined) time-adaptivity
  - [line 51 of TestMonodomainWithTimeAdaptivity.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/monodomain/TestMonodomainWithTimeAdaptivity.hpp#L51)
- Run using operator-splitting
  - [line 58 of TestOperatorSplittingMonodomainSolver.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/monodomain/TestOperatorSplittingMonodomainSolver.hpp#L58)

## Cell Based

### Simulation
- Time various aspects of a cell-based simulation using `CellBasedEventHandler`.
  - [line 434 of TestCryptSimulation2dNightly.hpp](https://github.com/Chaste/Chaste/blob/develop/crypt/test/simulation/TestCryptSimulation2dNightly.hpp#L434)
- Save and load ('checkpoint') a cell-based simulation to file.
  - [line 135 of TestGenerateSteadyStateCrypt.hpp](https://github.com/Chaste/Chaste/blob/develop/crypt/test/simulation/TestGenerateSteadyStateCrypt.hpp#L135)

## Continuum mechanics
- Write strain after solve
  - [line 944 of TestCompressibleNonlinearElasticitySolver.hpp](https://github.com/Chaste/Chaste/blob/develop/continuum_mechanics/test/TestCompressibleNonlinearElasticitySolver.hpp#L944)
- Get or output stresses during a solve
  - [line 634 of TestIncompressibleNonlinearElasticitySolver.hpp](https://github.com/Chaste/Chaste/blob/develop/continuum_mechanics/test/TestIncompressibleNonlinearElasticitySolver.hpp#L634)
- Solve nonlinear elasticity problems
  - [line 107 of TestSolvingElasticityProblemsTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/continuum_mechanics/test/TestSolvingElasticityProblemsTutorial.hpp#L107)
- Visualise nonlinear elasticity problems solutions, including visualisng strains
  - [line 222 of TestSolvingElasticityProblemsTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/continuum_mechanics/test/TestSolvingElasticityProblemsTutorial.hpp#L222)
- Specify more complicated boundary conditions in elasticity problems
  - [line 77 of TestSolvingMoreElasticityProblemsTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/continuum_mechanics/test/TestSolvingMoreElasticityProblemsTutorial.hpp#L77)
- Solve Stokes' flow problems (this functionality is work-in-progress).
  - [line 51 of TestStokesFlowSolver.hpp](https://github.com/Chaste/Chaste/blob/develop/continuum_mechanics/test/TestStokesFlowSolver.hpp#L51)

### Ventilation
- Solve a simple ventilation problem with no time variation.
  - [line 272 of TestMatrixVentilationProblem.hpp](https://github.com/Chaste/Chaste/blob/develop/lung/test/ventilation/TestMatrixVentilationProblem.hpp#L272)
- Solve a simple ventilation problem defined in a file.
  - [line 390 of TestMatrixVentilationProblem.hpp](https://github.com/Chaste/Chaste/blob/develop/lung/test/ventilation/TestMatrixVentilationProblem.hpp#L390)
- Solve a simple ventilation problem with no time variation.
  - [line 299 of TestVentilationProblem.hpp](https://github.com/Chaste/Chaste/blob/develop/lung/test/ventilation/TestVentilationProblem.hpp#L299)
- Solve a simple ventilation problem defined in a file.
  - [line 416 of TestVentilationProblem.hpp](https://github.com/Chaste/Chaste/blob/develop/lung/test/ventilation/TestVentilationProblem.hpp#L416)

## General
- Read and use parameters from the command line
  - [line 46 of TestCommandLineArguments.hpp](https://github.com/Chaste/Chaste/blob/develop/global/test/TestCommandLineArguments.hpp#L46)
- Use mock (pretend) command line arguments
  - [line 260 of TestCommandLineArguments.hpp](https://github.com/Chaste/Chaste/blob/develop/global/test/TestCommandLineArguments.hpp#L260)

### Archiving
- Use a binary rather than ascii boost archive format, for speed and smaller file sizes.
  - [line 392 of TestArchiving.hpp](https://github.com/Chaste/Chaste/blob/develop/global/test/TestArchiving.hpp#L392)

## Lung

### Anatomy definition
- Generate a complete conducting airway model given segmentations of CT airways and lobes.
  - [line 47 of TestAirwayGenerationTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/lung/test/tutorials/TestAirwayGenerationTutorial.hpp#L47)

### Simulation
- Simulate ventilation on a full lung geometry with acinar dynamics over a breathing cycle.
  - [line 47 of TestDynamicVentilationTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/lung/test/tutorials/TestDynamicVentilationTutorial.hpp#L47)
- Calculate transfer impedance of an airway tree using a simple impedance model
  - [line 47 of TestSimpleImpedanceProblemTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/lung/test/tutorials/TestSimpleImpedanceProblemTutorial.hpp#L47)
- Calculate ventilation distribution in an airway tree for a given flow rate at the trachea
  - [line 47 of TestStaticVentilationTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/lung/test/tutorials/TestStaticVentilationTutorial.hpp#L47)

## Mesh
- Construct a distributed regular mesh (rectangle in 2D or cuboid in 3D) which does not have a default split plane.  The default is for parallel code to split 2-D meshes into slices in the y-dimension and 3-D meshes in the z-dimension.
  - [line 2283 of TestDistributedTetrahedralMesh.hpp](https://github.com/Chaste/Chaste/blob/develop/mesh/test/TestDistributedTetrahedralMesh.hpp#L2283)
- Write meshes to file
  - [line 58 of TestMeshWriters.hpp](https://github.com/Chaste/Chaste/blob/develop/mesh/test/writer/TestMeshWriters.hpp#L58)
- Convert a linear tetrahedral mesh to quadratic and write back to file.
  - [line 790 of TestQuadraticMesh.hpp](https://github.com/Chaste/Chaste/blob/develop/mesh/test/TestQuadraticMesh.hpp#L790)
- Apply transformations to meshes
  - [line 49 of TestTransformations.hpp](https://github.com/Chaste/Chaste/blob/develop/mesh/test/TestTransformations.hpp#L49)

## PDE
- Evaluate integrals (using a solution from a PDE solve say) over a finite element mesh
  - [line 49 of TestAbstractFunctionalCalculator.hpp](https://github.com/Chaste/Chaste/blob/develop/pde/test/utilities/TestAbstractFunctionalCalculator.hpp#L49)
- Write a solver for coupled nonlinear PDEs (advanced)
  - [line 53 of TestSolvingCoupledNonlinearPdes.hpp](https://github.com/Chaste/Chaste/blob/develop/pde/test/TestSolvingCoupledNonlinearPdes.hpp#L53)
- Define and solve a particular type of coupled ODE/PDE system
  - [line 47 of TestSolvingLinearParabolicPdeSystemsWithCoupledOdeSystemsTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/pde/test/tutorials/TestSolvingLinearParabolicPdeSystemsWithCoupledOdeSystemsTutorial.hpp#L47)
- Define and solve linear elliptic or parabolic PDEs
  - [line 47 of TestSolvingLinearPdesTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/pde/test/tutorials/TestSolvingLinearPdesTutorial.hpp#L47)
- Output results to file for time-dependent PDE solvers
  - [line 342 of TestSolvingLinearPdesTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/pde/test/tutorials/TestSolvingLinearPdesTutorial.hpp#L342)
- Define and solve nonlinear elliptic PDEs
  - [line 52 of TestSolvingNonlinearPdesTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/pde/test/tutorials/TestSolvingNonlinearPdesTutorial.hpp#L52)
- Write new PDE solvers (especially for linear coupled elliptic/parabolic systems)
  - [line 52 of TestWritingPdeSolversTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/pde/test/tutorials/TestWritingPdeSolversTutorial.hpp#L52)

## Creating new how-tos

Any C-style block comment found in a test file that looks like the following will be given an entry in the index:

 * HOW_TO_TAG Section/Subsection
 * Short description (ideally one-liner)

The short description may run over multiple lines; it will be considered to end either at the end of the comment, or at a blank comment line, whichever comes first.
This index is automatically updated by a GitHub Actions workflow triggered by any new commit pushed to the `develop` branch.
