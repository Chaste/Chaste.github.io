---
title: "Cardiac Mechanics Solvers"
description: "Cardiac Mechanics Solvers"
draft: false
images: []
toc: true
layout: "single"
version: "2024.2"
---

This page contains information on mechanics solvers for cardiac Chaste.

## Mechanics solvers

There are (as of the time of writing, Nov 2011) two mechanics solvers, an
incompressible nonlinear elasticity solver and a compressible nonlinear
elasticity solver, with the following hierarchy:

```c++
       AbstractNonlinearElasticitySolver
         ^                          ^
         |                          |
IncompressibleSolver        CompressibleSolver
```

(Here and throughout this page we shorten class names - for example
`CompressibleSolver` is actually called
`CompressibleNonlinearElasticitySolver`). See
[mechanics tutorials](../../user-tutorials/) for more information on these
classes.

## Cardiac mechanics solvers

Cardiac mechanics solvers solve mechanics problems for which the forcing comes
from active tension developed in the tissue. Both incompressible and
compressible versions are required, and the cardiac-specific part of a
`CardiacMechanicsSolver` doesn't really care whether it is a compressible or
incompressible problem.

To complicate matters, there are two types of `CardiacMechanicsSolver`, an
implicit solver and an explicit solver. The explicit solver basically uses
active tensions computed at the previous timestep, whereas the implicit solver
uses the current solution in computing the active tensions. (The appropriate
choice of solver depends on the types of contraction model used). For more
details on all of this see `[1]`.

There are therefore four combinations:
`{incompressible,compressible} x {implicit,explicit}`. The cardiac mechanics
solvers are templated over the solver they should inherit from.

```c++
                IncompressibleSolver or CompressibleSolver
                                     ^
                                     |
                     template<class SOLVER>
                     AbstractCardiacMechanicsSolver : public SOLVER
                      ^                    ^
                      |                    |
  template<class SOLVER>                  template<class SOLVER>
  ExplicitSolver                          ImplicitSolver
```

To avoid `CardiacElectroMechanicsProblem` (the class used by a user) also having
to be templated over the solver to use, which would be a pain for a user, all
declarations of the methods in `AbstractCardiacMechanicsSolver<SOLVER,DIM>` are
in `AbstractCardiacMechanicsSolverInterface<DIM>`, so that the problem class can
just hold a pointer to the latter:

```c++
           AbstractNonlinearElasticitySolver
                           ^
                           |
      IncompressibleSolver or CompressibleSolver       AbstractCardiacMechanicsSolverInterface
                           ^                               ^
                           |                               |
                template<class SOLVER>                     |
                AbstractCardiacMechanicsSolver ____________|
                  ^                    ^
                  |                    |
template<class SOLVER>                template<class SOLVER>
ExplicitSolver                        ImplicitSolver
```

`CardiacElectroMechanicsProblem<DIM>` holds pointer to
`AbstractCardiacMechanicsSolverInterface<DIM>` and allocates this to be one of

- `ExplicitSolver<IncompressibleSolver,DIM>`
- `ExplicitSolver<CompressibleSolver,DIM>`
- `ImplicitSolver<IncompressibleSolver,DIM>`
- `ImplicitSolver<CompressibleSolver,DIM>`

depending on whether the user wants compressible or incompressible, and based on
which contraction model is used.

## References

`[1]` Pathmanathan, Pras, et al. "Cardiac electromechanics: the effect of
contraction model on the mathematical problem and accuracy of the numerical
scheme." *The Quarterly Journal of Mechanics & Applied Mathematics* 63.3 (2010):
375-399. [link](http://dx.doi.org/10.1093/qjmam/hbq014)
