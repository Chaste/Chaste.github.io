---
title: "FEM Implementations"
description: "FEM Implementations"
draft: false
images: []
toc: true
layout: "single"
---

The finite element implementations in the various Chaste solvers are described
in the attached pdf.

Contents:

```

1 Finite element solution of simple equations
1.1 Poisson's equation
1.1.1 Applying Dirichlet boundary conditions
1.2 The heat equation

2 Chaste PDE solvers
2.1 SimpleLinearEllipticSolver
2.2 SimpleLinearParabolicSolver
2.3 SimpleNonlinearEllipticSolver

3 Cardiac electrophysiology
3.1 The monodomain equations
3.2 The bidomain equations
3.3 The bidomain equations with a perfusing bath
3.3.1 The bidomain problem with a bath, including stimuli and parameters

4 Solid mechanics
4.1 Formulation
4.1.1 Kinematics
4.1.2 Stress
4.1.3 Equilibrium equations
4.2 Hyper-elasticity and material laws
4.3 Weak form
4.4 Normal pressure on deformed surface boundary conditions
4.5 Finite element discretisation
4.6 Actual ordering of unknowns
4.7 FE residual/Jacobian for the case of normal pressure on deformed surface BCs
4.8 Test problems
4.9 Other implementation calculations

5 Cardiac electro-mechanics
5.1 Formulation
5.1.1 Test problem
5.2 Implicit or explicit schemes
5.3 Anisotropic passive material laws
5.4 Active stress generated in sheet direction

6 Fluid dynamics
6.1 Stokes' Flow

```

{{< inline-svg "file-type-pdf" >}} [Finite Element Implementations](../fem_implementation.pdf)
