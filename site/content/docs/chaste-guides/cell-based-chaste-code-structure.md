---
title: "Cell-based Chaste Code Structure"
description: "Cell-based Chaste Code Structure"
date: 2020-08-27T19:23:18+02:00
lastmod: 2020-08-27T19:23:18+02:00
draft: false
images: []
toc: true
layout: "single"
---
# Overview of the cell-based Chaste code structure

This page is intended for new cell-based Chaste users/developers. For information, see the technical [Chaste papers](/publications).

## Language and external libraries

The main Chaste code has been written in C++ because it is a fast, object-oriented language. Object-oriented languages lead naturally to more modular code - software which is easier to abstract, to modify, and to document. All functional code developed for Chaste has a corresponding test suite. Since we use test-driven development, the test suites are written at the same time as the functionality and are of comparable length. The test suites are written using the C++ library [CxxTest](http://cxxtest.tigris.org), which is a light-weight portable testing framework. A typical test suite file for a Chaste C++ class will include approximately 10 individual test methods. Each method will instantiate and set up relevant classes, check that no exceptions are thrown and then check that any numerical output is correct within some given tolerance.

In order to make the best use of mature linear algebra routines and to ease the route to rapid parallelisation of parts of the code, we use [PETSc](http://www.mcs.anl.gov/petsc/) for sparse large-scale linear algebra and [MPI](http://www.mcs.anl.gov/mpi/) for parallelisation. Since the core linear algebra used within Chaste is a small subset of PETSc, we have provide light-weight wrappers to common routines such as the creation of sparse matrices, choice of pre-conditioners and iterative solution of linear systems.

Also used throughout the code are: the Standard Template Library (for extensible vector structures and iterators); [Boost](http://www.boost.org) uBLAS (for small-scale sequential vectors and matrices); Boost serialisation (for check-pointing and parameter definitions in the cell-based code); and [CodeSynthesis XSD](http://www.codesynthesis.com/products/xsd/) (for XML parameter input in cardiac-related code). In the area of ODE solvers, we provide an option to use light-weight interfaces to link against the CVODE solvers provided by [Sundials](http://www.llnl.gov/CASC/sundials/). In the area of fault-tolerance and check-pointing there is, at present, only limited functionality in Chaste.  We currently use the Boost serialisation library to
provide portable check-point files for crypt simulations.

## Chaste libraries

Computational modelling of both the `heart` and `cell_based` domains relies heavily on


* accurate representation of a complex, realistic geometry provided primarily through unstructured finite-element meshes;
* conversion, using the finite element method (FEM), of PDEs from a given domain into a sparse system of linear (or non-linear) equations, known as assembly;
* the iterative solution of large sparse systems via PETSc; and
* the numerical solution of ODE systems.


These four common features of the code become four component libraries: `mesh`, `pde`, `linalg` and `ode` respectively. They are supported by two lower-level libraries, `global` (which is responsible for initialisation and book-keeping calls to PETSc as well as taking care of exceptions) and `io` (which handles input and output, mainly via wrapped calls to HDF5 functionality). Built upon these are the two modelling components of Chaste, `heart` and `cell_based`. Each of the six core components and the two main modelling components comprise a number of interacting C++ classes, each in their own source file, together with a set of CxxTest test suites. Coverage of the functionality of each component by its test suites is verified on a daily basis using gcov, which is part of the [Gnu gcc project](http://gcc.gnu.org).

The build system used is [Scons](http://www.scons.org). When a developer compiles the code of Chaste, they typically build and test either a single test-suite, a library component or an entire raft of test-suites - known as the continuous test pack. In every case, code is compiled as necessary and executables are constructed corresponding to each test-suite. These test-suite executables are run as they become available and summary pass-fail web-pages are produced for the entire set of tests. This system makes it easy for a developer to understand the impact that a change in source code has across the entire archive of test-suites.

## Frequently used classes

A few classes are frequently used throughout the code-base:


* **Singleton classes**: There are a number of C++ objects used in physiological simulations for which there ought to be at most one instantiation per simulation. Notably, if simulation parameters are needed it is important that they are recorded and used in a consistent way. For this reason these classes use a **singleton design pattern**. Such classes are accessed not by a constructor as usual, but by an `Instance()` method. When the `Instance()` method is first called, then either the singleton object is taken and modified or, if no object exists, a new one is created using a set of default configuration parameters. At the end of each test, a `Destroy()` method must be called on the singleton object. Singleton classes used by the `cell_based` code include: `SimulationTime`, which provides a consistent current time to the multiple time-dependent components of cell-based simulations; `RandomNumberGenerator`, which records how pseudo-random numbers are seeded and logs every use, so can produce repeatable streams of random numbers even if the generator is stored in a check-point and restarted; and `CellwiseData`, which stores higher-level information that is accessible by each cell (such as the local oxygen concentration).



* **Time-stepping**: The use of time-stepping is common within all physiological models. The idea behind the time-stepper is to provide a robust way to deal with time loops. A naive programmer might explicitly state the number of steps in a simulation and iterate using fixed point numbers or they might iterate using a floating point loop and trust that an inequality test will always give the expected answer. Since neither of these alternatives is ideal, the timestepper uses an incremented integer counter to store its state (and to calculate the current time) and will always finish at the correct end time. This may be achieved by making the final time-step smaller than others.



* **Meshes**: All mesh geometry within Chaste is based on simplices (triangles in 2D, tetrahedra in 3D). There is a hierarchy of meshes inheriting from an `AbstractMesh` class which are templated over the dimensionality of their elements (1 for beams, 2 for triangles or 3 for tetrahedra) and over the space in which they are embedded. Normally the dimensions of the elements and of the embedding space will be the same, but it is possible to introduce a 1D mesh in 3D or a 2D mesh in 3D (say, to model a monolayer of cells in a colonic crypt). There are mesh readers and writers available for a variety of file formats. The default concrete mesh class is `TetrahedralMesh` but there are three notable others: `MutableMesh`, which supports changes in mesh geometry and topology, as well as re-meshing via external library calls ([Triangle](http://www.cs.cmu.edu/~quake/triangle.html) and [Tetgen](http://tetgen.berlios.de/) provide re-meshing functionality in 2D and 3D respectively); `ParallelTetrahedralMesh` which partitions the geometry using [METIS](http://www.cs.umn.edu/~metis) and then loads only a required part of the mesh (and corresponding halo nodes) into each process; and `QuadraticMesh`, which has more nodes per element than the meshes made from linear simplices.



* **Finite element solvers**: A hierarchy of finite element assemblers and solvers exist within the Chaste `pde` library. The role of the assemblers and solvers, between them, is to take a mathematical description of a set of PDEs together with their boundary conditions on a relevant mesh, to form a corresponding linear system and solve it. A straightforward assembler-solver would take a tetrahedral mesh and the weak form of a static (time-independent) PDE together with appropriate boundary conditions, form a linear system and solve it via a wrapped call to a PETSc linear system solver.


## `cell_based`-specific classes

We now provide an overview of the structure of the `cell_based` codebase:


* **Cell-cycle models and cells**: At the lowest level in the code are the cell-cycle models. Examples of cell-cycle models include those where division occurs after a fixed time, or after a normally-distributed time, and those where cell-division is dependent on the local oxygen concentration. A `Cell` object then takes in a cell-cycle model, and provides all the functionality required of a single cell, in particular: functionality relating to age, type, generation, and mutational status; functionality to undergo mitosis; and functionality to undergo apoptosis (programmed cell death).



* **Cylindrical mesh and cell population classes**: Crypt simulations on cylindrical geometries make use of the `Cylindrical2dMesh`class, which inherits from `MutableMesh` but implements the extra functionality required for enforcing periodic boundaries, including the ability to remesh on a cylindrical domain. This means that no other component has to deal with issues relating to the imposition of periodic boundary conditions. The `MeshBasedCellPopulation` class then takes in a set of cells and a mesh, which may be cylindrical or not, and maintains coherence between the two as cells are added or deleted as part of cell-birth or cell-death. Note that the `MeshBasedCellPopulation` class is for off-lattice models where cell-connectivity is determined through triangulation - a number of other cell population classes exist that consider alternative ways to define cell-based models. These include `NodeBasedCellPopulation`, which defines 'overlapping spheres' models, where connectivity is based on relative distance, and `VertexBasedCellPopulation`, in which each cell is represented by a finite set of vertices that define its boundary.



* **Force and update-rule objects**: Several force objects have been defined, the simplest being `GeneralisedLinearSpringForce`. This inherits from the `AbstractForce` class, which defines an interface for all force objects. Further force classes have been implemented, each inheriting from `AbstractForce`, and each only implementing the relevant contribution to the force, not the total force. Since cell-based simulation objects (defined below) can take in any number of `AbstractForce` classes, simulations using a wide range of (total) force laws can be put together in a straightforward manner by picking the required contributory force classes. Just as off-lattice simulations incorporate force laws, on-lattice simulations use a `UpdateRule` class hierarchy.



* **Cell-killer objects**: Cell-killer objects contain rules used to determine which cells should be removed from the simulation and when. For example, a `SloughingCellKiller` has been introduced to identify cells for sloughing in the crypt by virtue of their position - cells above a certain height are removed to simulate sloughing into the lumen. Additionally, an `OxygenBasedCellKiller` is used in tumour spheroid simulations to eliminate cells whose local nutrient concentration is too low for them to remain alive.



* **Cell-based simulation classes**: At the highest level are the cell-based simulation classes, such as `CryptSimulation2d`. These inherit common functionality from a `AbstractCellBasedSimulation` class, which deals with cell-birth and death, and is written to run in all spatial dimensions, so that the same code is used to simulate a 2D crypt or a 3D tumour spheroid. Derived classes, such as `CryptSimulation2d`, deal with application-specific concerns only (such as boundary conditions or integrating the PDE governing nutrient concentration, respectively). These objects take in a cell population, any number of force classes, and any number of cell killers. Tumour spheroid simulations are set up in a similar manner.


The object-based structure, in addition to being amenable to component-wise testing as described above, is especially advantageous in such discrete cell-based models, since it allows several different simulations to be created in a straightforward manner, by using whichever components are desired, and prevent unnecessary repetition of code shared by the crypt and tumour spheroid models. More examples are available as tutorials.
