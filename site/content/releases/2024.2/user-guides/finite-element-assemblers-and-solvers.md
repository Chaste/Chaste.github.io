---
title: "FEM Assemblers and Solvers"
description: "FEM Assemblers and Solvers"
draft: false
images: []
toc: true
layout: "single"
version: "2024.2"
---

{{< callout context="note" title="Important Notes" icon="outline/info-circle" >}}

- New users should read the tutorial on solving linear PDEs before reading this;
  this page is more on how the assemblers and solvers work internally.
- This page only refers to the main assemblers and solvers, which use linear
  basis functions, ie **those in the** `pde` **folder**. The continuum mechanics
  assemblers (those in the `continuum_mechanics` folder) use quadratic basis
  functions and are outside this hierarchy, although they are going towards a
  similar design.

{{< /callout >}}

## Quick Summary

The old design involved classes that were both assemblers (of finite element
matrices/vectors), and solvers. Assemblers and solvers are now completely
seperate. See also the diagram at the bottom of this page.

### Assemblers

The class `AbstractFeVolumeIntegralAssembler` is a generic assembler class
(linear bases only) and provides the basic functionality for assembling finite
element matrices (for example, a stiffness matrix, or mass matrix, or the matrix
$A$ in $Ax=b$), or vectors (e.g. $b$ in $Ax=b$) based on volume integrals. Concrete
classes which inherit from `AbstractFeVolumeIntegralAssembler` say whether they
want to assemble a matrix or vector (or both); and if they are assembling a
matrix, implement the pure-like method `ComputeMatrixTerm()` which says exactly
what the matrix to be assembled should be. Similarly concrete assemblers that
assemble vectors implement `ComputeVectorTerm()`.

### Solvers

The main solvers now only solve linear PDEs. There is an abstract static an
abstract dynamic solver, defining the following interfaces:

`AbstractStaticLinearPdeSolver` has

- a `Solve()` method

`AbstractDynamicLinearPdeSolver` has

- a `SetTimes()` method
- a `SetInitialCondition()` method
- a `Solve()` method

Concrete classes need to implement the pure method `SetupLinearSystem()`, which
should completely setup the linear system to be solved (each timestep). How they
set it up will depend on both the PDE solved and the precise numerical scheme
used. They can now make use of as many assemblers as they want.

**Hybrid**

The class `AbstractAssemblerSolverHybrid` is a useful class for allowing
concrete classes of the old design: classes that are both assemblers and
solvers. `AbstractAssemblerSolverHybrid` inherits from
`AbstractFeVolumeIntegralAssembler`, and has a method for constructing a linear
system using its parent assembler. Concrete classes should inherit from it _and_
the static/dynamic solver (as appropriate). See below for more details.

**Cardiac assemblers and solvers**

See [section](#cardiac-assemblers-and-solvers) section in full description (more or less self-contained).

{{< callout context="tip" title="See Also" icon="outline/rocket" >}}

- [Solving Linear PDEs](../../user-tutorials/solvinglinearpdes/)
- [Numerical Methods and Object-oriented Design](/docs/nmood_slides.pdf) {{< inline-svg "outline/file-type-pdf" >}}

{{< /callout >}}

## Full Description

Finite element solution of PDEs involves solving a linear system, whether it is
(i) the single linear system solved in the FEM discretisation of a static linear
problem; or (ii) the linear system solved each timestep of a FEM discretisation
of a time-dependent linear problem; or (iii) the linear system solved each
newton iteration of a nonlinear problem.

The previous assembler hierachy was actually an assembler-solver hierachy, and
based on the notion that every problem involved defining how to do the _finite
element assembly_ of the left-hand-side (LHS) matrix and how to do the finite
element assembly of the right-hand side (RHS) vector, ie the matrix $A$ and vector
$b$ in the linear system $Ax=b$. Here, _finite element assembly_ means looping over
elements, doing numerical integration on each element, and adding small
matrices/vectors to $A$ or $b$. This led to the solver-assembler hierachy, where the
concrete solver-assemblers were partly a PDE solver interface and partly an
assembler of LHS matrix $A$ and RHS vector $b$.

This worked fine for simple FEM implementations. However, for more advanced
implementations, such as monodomain problems with matrix-based-RHS, where the
linear system is of the form $Ax=Mz$, where $A$ and $M$ (mass matrix) need to be
assembled in a finite element manner, but not $z$, this doesn't fit in very well.
An even worse example is monodomain with a 'correction' term, where the linear
system is $Ax=Mz+c$, where $A$, $M$ and $c$ need to be assembled in a finite element
manner.

This led to the new assemblers and solvers, which is no longer a complex
assembler-solver hierachy, but a simple assembler hierarchy, and a separate
solver hierarchy.

### AbstractFeVolumeIntegralAssembler

#### Introduction

This class is used for creating _any_ matrix or vector which needs to be
assembled in a finite element manner via volume integrals, ie, the matrix $A$ or
vector $b$ in $Ax=b$; or $A$ or $M$ or $c$ in $Ax=Mz+c$. It currently uses linear basis
functions only.

The class is templated over element, spatial and problem dimensions as usual,
but also on two booleans, `CAN_ASSEMBLE_VECTOR` and `CAN_ASSEMBLE_MATRIX`:

```c++
template<unsigned ELEM_DIM,unsigned SPACE_DIM,unsigned PROBLEM_DIM,bool
CAN_ASSEMBLE_VECTOR, bool CAN_ASSEMBLE_MATRIX, InterpolationLevel
INTERPOLATION_LEVEL> class AbstractFeVolumeIntegralAssembler
```

The methods which need to be implemented by the concrete classes are:

```c++
ComputeMatrixTerm();
ComputeVectorTerm();
ComputeVectorSurfaceTerm();
```

These methods are essentially the pure methods which need to be implemented by
the concrete class. Technically, though, they are not pure: they have a default
implementation (which is to throw an error), so that the concrete classes just
need to implement the ones that will be needed.

**For example:** To create a concrete class which is to be used for assembling
the mass matrix $M$ in 1d, the user has to write a concrete class inheriting from
`AbstractFeVolumeIntegralAssembler<1,1,1,false,true,NORMAL>`, and then implement
the `ComputeMatrixTerm()` methods (the other two methods don't need overloading
as no vectors are assembled). Similarly, to create a concrete class for
assembling a vector, we inherit from
`AbstractFeVolumeIntegralAssembler<1,1,1,true,false,NORMAL>` and implement
`ComputeVectorTerm()`. The calling code then needs to provide a constructed
`Mat` or `Vec`, and the assembler will assemble them. See
`pde/test/TestAbstractFeVolumeIntegralAssembler.hpp` for examples of concrete
classes and usage.

### ComputeMatrixTerm(), ComputeVectorTerm()

These are the methods the concrete assembler has to implement. They need to
provide the _integrand_ of the integral being evaluated at the current
quadrature point, which will be a vector/matrix of size `num_nodes_in_element`

**For example:** Suppose we are in 2d, and want to set up the vector $b$, where

$$
b_i = \int_{\Omega} f(x) \phi_i(x) dV
$$

which is the RHS vector needed to solve linear elliptic equations with source
term f.

We inherit from `AbstractFeVolumeIntegralAssembler<1,1,1,true,false,NORMAL>` and
implement `ComputeVectorTerm()`. This has parameters which include the
quadrature point `rX`, and the vector of basis functions evaluated at that quad
point `rPhi` ( = `[\phi_2(x), \phi_3(x)](\phi_1(x),)`):

```c++
c_vector<double,PROBLEM_DIM*(ELEMENT_DIM+1)> ComputeVectorTerm(
	        c_vector<double, ELEMENT_DIM+1>& rPhi,
	        c_matrix<double, SPACE_DIM, ELEMENT_DIM+1>& rGradPhi,
	        ChastePoint<SPACE_DIM>& rX,
	        c_vector<double,PROBLEM_DIM>& rU,
	        c_matrix<double, PROBLEM_DIM, SPACE_DIM>& rGradU,
	        Element<ELEMENT_DIM,SPACE_DIM>* pElement)
```

This implementation needs to return the vector
`[f(x)phi_2(x), f(x) phi_3(x)](f(x)phi_1(x),)`. It will therefore use `rX` and
`rPhi` from the parameters, but not any of the others.

`ComputeMatrixTerm()` is similar.

#### InterpolationLevel

In the above example the parameters `rU`, `rGradPhi`, `rGradU` are not needed by
the concrete class, and therefore didn't need interpolating onto the current
quadrature points. Some control is available over which quantities are
interpolated through the final template parameter of the abstract class

```c++
template<unsigned ELEM_DIM,unsigned SPACE_DIM,unsigned PROBLEM_DIM,bool CAN_ASSEMBLE_VECTOR, bool CAN_ASSEMBLE_MATRIX, InterpolationLevel INTERPOLATION_LEVEL>
class AbstractFeVolumeIntegralAssembler
```

For example if `InterpolationLevel` is _not_ equal to `NONLINEAR`, `rGradPhi` is
not computed for vectors. See class documentation for available options.
Non-interpolated parameters are just passed in which zeroed values, so choosing
an incorrect `InterpolationLevel` will lead to the solver _silently giving
completely incorrect answers_ if a quantity is used when it hasn't been
interpolated.

#### AbstractFeSurfaceIntegralAssembler - surface integrals

For integrals over surface elements (ie the terms coming from Neumann boundary
conditions), there is a similar abstract class
`AbstractFeSurfaceIntegralAssembler` which the same interface. For assembling
surface-integral contributions to a vector, the concrete class needs to provide
a `ComputeVectorSurfaceTerm()`. There is a concrete
`NaturalNeumannSurfaceTermAssembler` which is used in most problems.

### The solvers of linear PDEs

#### Introduction

There are three relatively simple solver classes for linear PDEs:
`AbstractStaticLinearPdeSolver` for solving linear time-independent problems,
`AbstractDynamicLinearPdeSolver` for solving linear time-dependent problems, and
a parent which includes some common functionality

```c++
                    AbstractLinearPdeSolver
                        ^            ^
                        |            |
                        |            |
AbstractStaticLinearPdeSolver     AbstractDynamicLinearPdeSolver
```

`AbstractStaticLinearPdeSolver` has

- a `Solve()` method

`AbstractDynamicLinearPdeSolver` has

- a `SetTimes()` method (for setting start time, end time and timestep).
- a `SetInitialCondition()` method
- a `Solve()` method

The three classes are abstract because of the following pure method in
`AbstractLinearPdeSolver`

- `void SetupLinearSystem()=0;`

This is the method that needs to be implemented by a concrete solver. It is
called by the two `Solve` methods, and should completely set up the linear
system to be solved (that timestep), using whichever assemblers it needs and
applying boundary conditions if necessary.

#### AbstractAssemblerSolverHybrid

Now, in principle, to solve a particular PDE, we need to create a concrete
assembler, `MyAssembler`, for that PDE, and then create a concrete solver,
`MySolver`, which implements `SetupLinearSystem` using `MyAssembler`. This would
be a "has-a" solver-assembler relationship ("solver has an assembler"), and is
the new design.

For convenience, the old "is-a" relationship ("solver is also an assembler") is
still allowed, through the class `AbstractAssemblerSolverHybrid`. This can be
used when an assembler will be written which will define the **whole** of the
LHS matrix $A$, and the **whole** of the RHS vector $b$.

`AbstractAssemblerSolverHybrid` inherits from

```c++
AbstractFeVolumeIntegralAssembler<..,true,true,..>
```

and has a method `SetupGivenLinearSystem(..,..,LinearSystem*)` which sets up the
given linear system using the parent-assembler part of the class.

Concrete classes should inherit from this and **one of**
`AbstractStaticLinearPdeSolver` or `AbstractDynamicLinearPdeSolver`. They would
then have the following pure methods

- `ComputeMatrixTerm()`
- `ComputeVectorTerm()`
- `SetupLinearSystem` (inherited from the parent solver)

The concrete class then has to implement the `Compute*Term` methods as
appropriate for its particular PDE. For `SetupLinearSystem` it simply has to
have a one-line function which just calls `SetupGivenLinearSystem`. See
`SimpleLinearEllipticSolver` as an example.

### Concrete solvers

#### Non-heart

- `SimpleLinearEllipticSolver`: inherits from `AbstractAssemblerSolverHybrid`
  and `AbstractStaticLinearPdeSolver` and implements `Compute*Term` methods
  appropriately.
- `SimpleLinearParabolicSolver`: inherits from `AbstractAssemblerSolverHybrid`
  and `AbstractDynamicLinearPdeSolver` and implements `Compute*Term` methods
  appropriately.
- `SimpleNonlinearEllipticSolver`: inherits from ("is-a")
  `AbstractFeVolumeIntegralAssembler` but is outside the solver hierarchy. See
  class documentation.

#### Cardiac assemblers and solvers

See the
[FE implementations document](../finite-element-implementations)
for the discretisations being set up and solved in the cardiac
electro-physiology solvers. For both monodomain and bidomain the linear system
can be written as $Ax=Mz$, where $A$ and $M$ require assembling (looping over
elements) but $z$ does not, or as $Ax=Mz+c$, where $c$ also has to be assembled. The
"is-a" solver-assembler approach therefore cannot be used and the "has-a" design
is used.

**Monodomain**

The assembler classes

- `MonodomainAssembler`
  - the main monodomain assembler: can construct both the matrix $A$, and the
    vector arising from surface stimuli contributions
- `MassMatrixAssembler`
  - for assembling the mass matrix, $M$
- a `NaturalNeumannSurfaceTermAssembler` for Neumann BCs
- also there is an assembler for assembling the correction term if SVI is used
  (see [here](../state-variable-interpolation))

The solver is:

- `MonodomainSolver`
  - inherits from `AbstractDynamicLinearPdeSolver`
  - owns a `MonodomainAssembler` and a `MassMatrixAssembler` (and if needed an
    assembler for the SVI term)
  - uses these assemblers to set up the linear system in `SetupLinearSystem()`

**Bidomain**

Bidomain is a bit more complicated, due to the possibility of a bath and extra
bidomain specific functions. See the
[FE implementations document](../finite-element-implementations)
for the discretisations. The basic ideas here are the same as with monodomain
though.

Assemblers:

- `BidomainAssembler`
  - the main bidomain assembler: can construct both the matrix $A$
- `BidomainMassMatrixAssembler`
  - A normal `MassMatrixAssembler` can't be used
  - can deal with both bath/non-bath problems.
- `BidomainWithBathAssembler`
  - inherits from `BidomainAssembler`, overloaded method to take into account
    the bath when computing the LHS matrix $A$.
- `BidomainNeumannSurfaceTermAssembler`, for the vector arising from surface
  stimuli contributions
- also there is an assembler for assembling the correction term if SVI is used
  (see
  [here](../state-variable-interpolation))

Solvers:

- `AbstractBidomainSolver`
  - inherits from `AbstractDynamicLinearPdeSolver`
  - contains a lot of common bidomain functionality (null-space; setting average
    phi=0; bath finalisation)
- `BidomainSolver`
  - inherits from `AbstractBidomainSolver`
  - owns a `BidomainAssembler` or `BidomainWithBathAssembler` as appropriate,
    and a `BidomainMassMatrixAssembler`, etc
  - uses these assemblers to set up the linear system in `SetupLinearSystem()`

```c++
                                                AbstractLinearPdeSolver /* pure SetUpLinearSystem() method */
                                                    ^            ^
                                                    |            |
                                                    |            |
                            AbstractStaticLinearPdeSolver     AbstractDynamicLinearPdeSolver /* SetTimes(), SetInitCondition(), Solve() methods */
                                    ^  /* Solve() method */      ^                 ^     ^
                                    |                            |                 |     |
 SimpleLinearEllipticSolver ________|                            |                 |     |__________________ SimpleLinearParabolicSolver
   /* is a assembler, ie also */                                 |                 |                           /* is a assembler, ie also */
   /* inherits from hybrid    */                                 |                 |                           /* inherits from hybrid    */
                                                                 |                 |
                                                                 |              AbstractBidomainSolver
                                                                 |                       ^
                                                                 |                       |
                                                                 |                       |
                                                    MonodomainSolver               BidomainSolver   /* both implement SetUpLinearSystem() */
                                                    //uses severals assemblers     // uses several assemblers
```
