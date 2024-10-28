---
title: "User tutorials"
description: "Chaste user tutorials"
date: 2020-08-27T19:23:18+02:00
lastmod: 2020-08-27T19:23:18+02:00
draft: false
layout: "single"
images: []
version: "2024.2"
---

{{< callout context="note" title="Note" icon="outline/info-circle" >}} 
If you are viewing this on the Chaste website, **the tutorials here are automatically updated to work with the latest development version of Chaste**.
They are not guaranteed to work with any release version, in fact they are unlikely to!
If you are working with a release version of the code then this page is archived upon releases; the tutorials corresponding to each release version of Chaste can be found on the [releases page](/releases/).
{{< /callout >}}

## The basics

These tutorials assume prior knowledge or understanding of various C++ language features and some libraries, including (at least): 
`std::vector`s, `c_vector`s, and object-oriented inheritance including abstract classes and virtual methods.

If you don't know anything about these we recommend a first course in C++, there are plenty online (here is one from [cplusplus.com](http://www.cplusplus.com/doc/tutorial/)).
There is also a [Scientific Computing in C++ book](http://www.springer.com/computer/swe/book/978-1-4471-2735-2) by some of our team available too.

To run any of these tutorials, it is assumed you have first configured Chaste using `CMake`:

```bash
cmake /path/to/chaste/src
```

Then, run
```bash
make <NAME_OF_TUTORIAL_FILE>
```
(without the .hpp on the end) to compile the tutorial source code, and
```bash
ctest -V -R <NAME_OF_TUTORIAL_FILE>
```
to run it. The `-V` is a flag to give *verbose* output, i.e. show the full output from the test on screen. The `-R` allows you to run all tests matching a 'regular expression', if you don't know what that means don't worry, if you just write the full tutorial class name it tells ctest to run that one in particular.

For instance:
```bash
make TestSolvingOdesTutorial
ctest -V -R TestSolvingOdesTutorial
```

### Where's my file output?

By default, Chaste will attempt to write any file output from tests and tutorials to the subdirectory `testoutput` of the build directory (the directory that you run `cmake` from).

It is recommended to redirect the output to a more permanent folder of your choosing. To do this you set an environment variable called `CHASTE_TEST_OUTPUT` in the terminal. We also recommend that you set this automatically and globally whenever you log in by adding a line like
```bash
export CHASTE_TEST_OUTPUT=/path/where/I/want/Chaste/to/write/files
```
to the bottom of your terminal login script (this should be in the file `~/.bashrc` if you are using a bash terminal, e.g. on Ubuntu or the Chaste Docker based on ubuntu. It could be `~/.zshrc` on a Mac). 
The Chaste docker has `CHASTE_TEST_OUTPUT` set by default to a sensible output location. 

The tutorials below will refer to `$CHASTE_TEST_OUTPUT` whether or not it is set. So if you aren't sure where test output is, just type 
```bash
echo $CHASTE_TEST_OUTPUT
```
in a terminal and it will return either a directory path or nothing -- in which case look in the subdirectory `testoutput` of the build directory.

---

## Before you do anything else

* Start with [**UserTutorials/WritingTests**](writingtests) 
* Then choose from the headings below [Core](#core-functionality), [Cardiac](#cardiac), [Cell-based](#cell-based), or [Lung](#lung).

---

## Core functionality

### Solving ODEs

* [UserTutorials/SolvingOdes](solvingodes)

### Solving PDEs

* [UserTutorials/SolvingLinearPdes](solvinglinearpdes/)
* [UserTutorials/SolvingNonlinearPdes](solvingnonlinearpdes/)
* [UserTutorials/SolvingLinearParabolicPdeSystemsWithCoupledOdeSystems](solvinglinearparabolicpdesystemswithcoupledodesystems/)

### Writing new PDE solvers (advanced)

* [UserTutorials/WritingPdeSolvers](writingpdesolvers/)
* [UserTutorials/WritingPdeSolversTwo](writingpdesolverstwo/)

### Solid Mechanics

* [UserTutorials/SolvingElasticityProblems](solvingelasticityproblems/) - computing the deformation of a nonlinearly elastic body
* [UserTutorials/SolvingMoreElasticityProblems](solvingmoreelasticityproblems/)

### Command line functionality
* [UserTutorials/CommandLineArguments](commandlinearguments/) - Utilising command line arguments as simulation parameters

---

## Cardiac

### Executable users

The cardiac executable is a compiled `CardiacSimulation` object that uses an XML file to specify the settings that C++ users would do via `HeartConfig`. It is therefore a bit easier to use but less flexible than using Chaste classes via C++.

* [UserTutorials/CardiacExecutable](cardiac-executable) - a submenu with links to various tutorials for users of the cardiac executable binary where settings are specified via an XML file (not the source code).

### Single Cardiac Cell Simulations
* [UserTutorials/SingleCellSimulation](singlecellsimulation/) - how to run ODE simulations for action potential models, handy methods for getting to steady pacing response.

### Mono/Biodomain Simulations
* [UserTutorials/RunningBidomainSimulations](runningbidomainsimulations/) - **basic bidomain simulation**; note monodomain is virtually the same
* [UserTutorials/AnotherBidomainSimulation](anotherbidomainsimulation/)  - shows how to use **varying fibre directions** and **different output formats** in particular
* [UserTutorials/Monodomain3dExample](monodomain3dexample/)  - illustrates the (trivial) changes required to go from 2d to **3d**, or bidomain to **monodomain**
* [UserTutorials/Monodomain3dExampleWithCvode](monodomain3dexamplewithcvode/) - illustrates how to adapt the previous tutorial to create cells with **CVODE solvers**, which can provide increased speed and accuracy.
* [UserTutorials/Monodomain3dRabbitHeart](monodomain3drabbitheart/) - illustrates loading meshes from file, and specifying fibre and cross-fibre conductivities, on a realistic (but low res) rabbit whole ventricles mesh.
* [UserTutorials/BidomainWithBath](bidomainwithbath/) - illustrates the use of **Backward Euler** ODE solvers (very stable), and solving a bidomain problem in tissue surrounded by (extra-cellular domain) bath.
* [UserTutorials/BidomainWithBathAndFibres](bidomainwithbathandfibres/)
* [UserTutorials/BidomainWithConductivityModifier](bidomainwithconductivitymodifier/) - shows how to use **conductivity modifiers** in a bidomain simulation.

### Checkpointing (saving/loading)

* [UserTutorials/CardiacCheckpointingAndRestarting](cardiaccheckpointingandrestarting/)

### Electro-mechanics
* [UserTutorials/CardiacElectroMechanics](cardiacelectromechanics/)
* [UserTutorials/AnotherCardiacElectroMechanics](anothercardiacelectromechanics/)

<!--
See also [cardiac Chaste practical](https://github.com/Chaste/trac_archive/wiki/Cardiac-Chaste-Practical) for details of a practical we have used to teach cardiac Chaste.
-->

---

## Cell-based

Where to start with cell-based simulations:

* [UserTutorials/CellBasedDemo](cellbaseddemo/) - a quick introduction to the basics of cell-based simulations in Chaste.
* [UserTutorials/VisualizingWithParaview](visualizingwithparaview/)

### Running basic simulation types:

* [UserTutorials/RunningMeshBasedSimulations](runningmeshbasedsimulations/) - the first type of cell-based simulation included in Chaste, start here!
* [UserTutorials/RunningNodeBasedSimulations](runningnodebasedsimulations/) - includes details of how to simplify cell-based tests
* [UserTutorials/RunningVertexBasedSimulations](runningvertexbasedsimulations/) - includes adding boundary conditions and removing cells from simulations
* [UserTutorials/RunningPottsBasedSimulations](runningpottsbasedsimulations/) - lattice-based simulations
* [UserTutorials/RunningImmersedBoundarySimulations](runningimmersedboundarysimulations/) - immersed boundary simulations

### Running crypt-specific simulations:

* [UserTutorials/RunningMeshBasedCryptSimulations](runningmeshbasedcryptsimulations/)
* [UserTutorials/RunningVertexBasedCryptSimulations](runningvertexbasedcryptsimulations/)
* [UserTutorials/RunningCryptSimulationsWithMutations](runningcryptsimulationswithmutations/)


### More advanced examples:

* [UserTutorials/RunningContactInhibitionSimulations](runningcontactinhibitionsimulations/)
* [UserTutorials/RunningDeltaNotchSimulations](runningdeltanotchsimulations/)
* [UserTutorials/RunningDifferentialAdhesionSimulations](runningdifferentialadhesionsimulations/)
* [UserTutorials/RunningTumourSpheroidSimulations](runningtumourspheroidsimulations/)

### Adding new functionality:

To do new things in Chaste that haven't been coded before you'll often have to add your own new C++ classes. Here are a set of examples to use as a basis for that.

* [UserTutorials/CreatingAndUsingANewCellCycleModel](creatingandusinganewcellcyclemodel/)
* [UserTutorials/CreatingAndUsingANewCellKiller](creatingandusinganewcellkiller/)
* [UserTutorials/CreatingAndUsingANewCellPopulationBoundaryCondition](creatingandusinganewcellpopulationboundarycondition/)
* [UserTutorials/CreatingAndUsingANewForce](creatingandusinganewforce/)
* [UserTutorials/CreatingAndUsingANewCellMutationState](creatingandusinganewcellmutationstate/)
* [UserTutorials/CreatingAndUsingANewCellProperty](creatingandusinganewcellproperty/)
* [UserTutorials/CreatingAndUsingNewCellBasedWriters](creatingandusingnewcellbasedwriters/)
* [UserTutorials/CreatingAndUsingANewCellBasedSimulationModifier](creatingandusinganewcellbasedsimulationmodifier/)

<!-- See also [cell-based Chaste practical](https://github.com/Chaste/trac_archive/wiki/Cell-Based-Chaste-Practical) for details of a practical we have used to teach cell-based Chaste.
-->
---

## Lung
Generation and manipulation of airway geometries

* [UserTutorials/AirwayGeneration](airwaygeneration/)


Simulating ventilation and impedance

* [UserTutorials/StaticVentilation](staticventilation/)
* [UserTutorials/DynamicVentilation](dynamicventilation/)
* [UserTutorials/SimpleImpedanceProblem](simpleimpedanceproblem)
