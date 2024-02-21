---
title: "User tutorials"
description: "Chaste user tutorials"
date: 2020-08-27T19:23:18+02:00
lastmod: 2020-08-27T19:23:18+02:00
draft: false
layout: "single"
images: []
---

{{< callout context="note" title="Note" icon="info-circle" >}} 
If you are viewing this on the Chaste wiki, **the tutorials here are automatically updated to work with the latest development version of Chaste**.
They are not guaranteed to work with any release version, in fact they are unlikely to!
If you are working with a release version of the code then this page is archived upon releases; the tutorials corresponding to each release version of Chaste can be found at [https://chaste.cs.ox.ac.uk/chaste/tutorials/](https://chaste.cs.ox.ac.uk/chaste/tutorials/).
{{< /callout >}}

## The basics

These tutorials assume prior knowledge or understanding of various C++ language features and some libraries, including (at least): 
`std::vector`s, `c_vector`s, and object-oriented inheritance including abstract classes and virtual methods.

If you don't know anything about these we recommend a first course in C++, there are plenty online (here is one from [cplusplus.com](http://www.cplusplus.com/doc/tutorial/)).
There is also a [Scientific Computing in C++ book](http://www.springer.com/computer/swe/book/978-1-4471-2735-2) by some of our team available too.

To run any of these tutorials, it is assumed you have first configured Chaste using `CMake`:
```
cmake /path/to/chaste/src
```

Then, run
```
make <NAME_OF_TUTORIAL_FILE>
```
(without the .hpp on the end) to compile the tutorial source code, and
```
ctest -V -R <NAME_OF_TUTORIAL_FILE>
```
to run it. The `-V` is a flag to give *verbose* output, i.e. show the full output from the test on screen. The `-R` allows you to run all tests matching a 'regular expression', if you don't know what that means don't worry, if you just write the full tutorial class name it tells ctest to run that one in particular.

For instance:
```
make TestSolvingOdesTutorial
ctest -V -R TestSolvingOdesTutorial
```

## Before you do anything else

* Start with [**UserTutorials/WritingTests**](/docs/user-tutorials/writingtests/) 
* Then choose from the headings below [Core](#core-functionality), [Cardiac](#cardiac), [Cell-based](#cell-based), or [Lung](#lung).

----

## Core functionality

### Solving ODEs

* [UserTutorials/SolvingOdes](/docs/user-tutorials/solvingodes/)

### Solving PDEs

* [UserTutorials/SolvingLinearPdes](/docs/user-tutorials/solvinglinearpdes/)
* [UserTutorials/SolvingNonlinearPdes](/docs/user-tutorials/solvingnonlinearpdes/)
* [UserTutorials/SolvingLinearParabolicPdeSystemsWithCoupledOdeSystems](/docs/user-tutorials/solvinglinearparabolicpdesystemswithcoupledodesystems/)

### Writing new PDE solvers (advanced)

* [UserTutorials/WritingPdeSolvers](/docs/user-tutorials/writingpdesolvers/)
* [UserTutorials/WritingPdeSolversTwo](/docs/user-tutorials/writingpdesolverstwo/)

### Solid Mechanics

* [UserTutorials/SolvingElasticityProblems](/docs/user-tutorials/solvingelasticityproblems/) - computing the deformation of a nonlinearly elastic body
* [UserTutorials/SolvingMoreElasticityProblems](/docs/user-tutorials/solvingmoreelasticityproblems/)

----

## Cardiac

### Executable users

* [UserTutorials/CardiacExecutable](cardiac-executable) - a submenu with links to various tutorials for users of the cardiac executable binary where settings are specified via an XML file (not the source code).

### Single Cardiac Cell Simulations
* [UserTutorials/SingleCellSimulation](/docs/user-tutorials/singlecellsimulation/) - how to run ODE simulations for action potential models, handy methods for getting to steady pacing response.

### Mono/Biodomain Simulations
* [UserTutorials/RunningBidomainSimulations](/docs/user-tutorials/runningbidomainsimulations/) - **basic bidomain simulation**; note monodomain is virtually the same
* [UserTutorials/AnotherBidomainSimulation](/docs/user-tutorials/anotherbidomainsimulation/)  - shows how to use **varying fibre directions** and **different output formats** in particular
* [UserTutorials/Monodomain3dExample](/docs/user-tutorials/monodomain3dexample/)  - illustrates the (trivial) changes required to go from 2d to **3d**, or bidomain to **monodomain**
* [UserTutorials/Monodomain3dExampleWithCvode](/docs/user-tutorials/monodomain3dexamplewithcvode/) - illustrates how to adapt the previous tutorial to create cells with **CVODE solvers**, which can provide increased speed and accuracy.
* [UserTutorials/Monodomain3dRabbitHeart](/docs/user-tutorials/monodomain3drabbitheart/) - illustrates loading meshes from file, and specifying fibre and cross-fibre conductivities, on a realistic (but low res) rabbit whole ventricles mesh.
* [UserTutorials/BidomainWithBath](/docs/user-tutorials/bidomainwithbath/) - illustrates the use of **Backward Euler** ODE solvers (very stable), and solving a bidomain problem in tissue surrounded by (extra-cellular domain) bath.
* [UserTutorials/BidomainWithBathAndFibres](/docs/user-tutorials/bidomainwithbathandfibres/)
* [UserTutorials/BidomainWithConductivityModifier](/docs/user-tutorials/bidomainwithconductivitymodifier/) - shows how to use **conductivity modifiers** in a bidomain simulation.

### Checkpointing (saving/loading)

* [UserTutorials/CardiacCheckpointingAndRestarting](/docs/user-tutorials/cardiaccheckpointingandrestarting/)

### Electro-mechanics
* [UserTutorials/CardiacElectroMechanics](/docs/user-tutorials/cardiacelectromechanics/)
* [UserTutorials/AnotherCardiacElectroMechanics](/docs/user-tutorials/anothercardiacelectromechanics/)

<!--
See also [cardiac Chaste practical](https://github.com/Chaste/trac_archive/wiki/Cardiac-Chaste-Practical) for details of a practical we have used to teach cardiac Chaste.
-->

----

## Cell-based

Where to start with cell-based simulations:

* [UserTutorials/CellBasedDemo](/docs/user-tutorials/cellbaseddemo/) - a quick introduction to the basics of cell-based simulations in Chaste.
* [UserTutorials/VisualizingWithParaview](/docs/user-tutorials/visualizingwithparaview/)

### Running basic simulation types:

* [UserTutorials/RunningMeshBasedSimulations](/docs/user-tutorials/runningmeshbasedsimulations/) - the first type of cell-based simulation included in Chaste, start here!
* [UserTutorials/RunningNodeBasedSimulations](/docs/user-tutorials/runningnodebasedsimulations/) - includes details of how to simplify cell-based tests
* [UserTutorials/RunningVertexBasedSimulations](/docs/user-tutorials/runningvertexbasedsimulations/) - includes adding boundary conditions and removing cells from simulations
* [UserTutorials/RunningPottsBasedSimulations](/docs/user-tutorials/runningpottsbasedsimulations/) - lattice-based simulations

### Running crypt-specific simulations:

* [UserTutorials/RunningMeshBasedCryptSimulations](/docs/user-tutorials/runningmeshbasedcryptsimulations/)
* [UserTutorials/RunningVertexBasedCryptSimulations](/docs/user-tutorials/runningvertexbasedcryptsimulations/)
* [UserTutorials/RunningCryptSimulationsWithMutations](/docs/user-tutorials/runningcryptsimulationswithmutations/)


### More advanced examples:

* [UserTutorials/RunningContactInhibitionSimulations](/docs/user-tutorials/runningcontactinhibitionsimulations/)
* [UserTutorials/RunningDeltaNotchSimulations](/docs/user-tutorials/runningdeltanotchsimulations/)
* [UserTutorials/RunningDifferentialAdhesionSimulations](/docs/user-tutorials/runningdifferentialadhesionsimulations/)
* [UserTutorials/RunningTumourSpheroidSimulations](/docs/user-tutorials/runningtumourspheroidsimulations/)

### Adding new functionality:

To do new things in Chaste that haven't been coded before you'll often have to add your own new C++ classes. Here are a set of examples to use as a basis for that.

* [UserTutorials/CreatingAndUsingANewCellCycleModel](/docs/user-tutorials/creatingandusinganewcellcyclemodel/)
* [UserTutorials/CreatingAndUsingANewCellKiller](/docs/user-tutorials/creatingandusinganewcellkiller/)
* [UserTutorials/CreatingAndUsingANewCellPopulationBoundaryCondition](/docs/user-tutorials/creatingandusinganewcellpopulationboundarycondition/)
* [UserTutorials/CreatingAndUsingANewForce](/docs/user-tutorials/creatingandusinganewforce/)
* [UserTutorials/CreatingAndUsingANewCellMutationState](/docs/user-tutorials/creatingandusinganewcellmutationstate/)
* [UserTutorials/CreatingAndUsingANewCellProperty](/docs/user-tutorials/creatingandusinganewcellproperty/)
* [UserTutorials/CreatingAndUsingNewCellBasedWriters](/docs/user-tutorials/creatingandusingnewcellbasedwriters/)
* [UserTutorials/CreatingAndUsingANewCellBasedSimulationModifier](/docs/user-tutorials/creatingandusinganewcellbasedsimulationmodifier/)

<!-- See also [cell-based Chaste practical](https://github.com/Chaste/trac_archive/wiki/Cell-Based-Chaste-Practical) for details of a practical we have used to teach cell-based Chaste.
-->
----

## Lung
Generation and manipulation of airway geometries

* [UserTutorials/AirwayGeneration](/docs/user-tutorials/airwaygeneration/)


Simulating ventilation and impedance

* [UserTutorials/StaticVentilation](/docs/user-tutorials/staticventilation/)
* [UserTutorials/DynamicVentilation](/docs/user-tutorials/dynamicventilation/)
* [UserTutorials/SimpleImpedanceProblem](/docs/user-tutorials/simpleimpedanceproblem)


