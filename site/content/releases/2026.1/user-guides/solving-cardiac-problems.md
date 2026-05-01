---
title: "Solving a Cardiac Problem"
description: "Solving a Cardiac Problem"
draft: false
images: []
toc: true
layout: "single"
version: "2026.1"
---

This page gives a high-level overview of the code execution flow when solving a
cardiac problem. To run simulations, see the
[User Tutorials](../../user-tutorials). For an overview of the PDE solver
hierarchy, see
[Finite Element Assemblers and Solvers](../finite-element-assemblers-and-solvers).
The steps that occur are as follows

- The user calls `AbstractCardiacProblem::Solve()` on their monodomain or
  bidomain problem object (after calling `Initialise`)
- The `AbstractCardiacProblem` owns a particular mono/bidomain finite element
  _solver_ (of base-class type `AbstractDynamicLinearPdeSolver`; the concrete
  class can be matrix-based or not; see
  [Finite Element Assemblers and Solvers](../finite-element-assemblers-and-solvers)
  for more details); and for each printing timestep, does the following:
  - sets the current time and end time on the solver
  - sets the latest voltage solution on the solver as the initial condition
  - calls `Solve` on the solver.

---

The `Solve` method on `AbstractDynamicLinearPdeSolver` does the following, for
each PDE timestep

- calls `PrepareForSetupLinearSystem` -- _solves cell models, see below_
- calls `SetupLinearSystem` -- _see below_
- calls `FinaliseLinearSystem` -- relevant for bidomain solves, things like
  checking compatibility, setting up a null space
- solves the linear system to obtain the solution (voltage, and phi_e in
  bidomain setting) at the next timestep

---

1. `PrepareForLinearSystem` is where the cell models are solved. It is
   implemented in `AbstractMonodomainSolver`/`AbstractBidomainSolver`, where it
   just calls `SolveCellSystems` on the `MonodomainTissue`/`BidomainTissue`.
   This is implemented in `AbstractCardiacTissue::SolveCellSystems`, which
   essentially does the following for each cell:
   1. Set _V_ from the current PDE solution
   2. Call the cell's `ComputeExceptVoltage` to solve for all state variables
      except _V_ until the next PDE time step
   3. Call `UpdateCaches`. This calls the cell's `GetIIonic` to compute the
      _I_ion_ term and stores it in `mIionicCacheReplicated` (replicated over
      each process so no parallel communication is required later). It similarly
      also calculates and caches the intracellular stimulus at each cell.

---

2. `SetupLinearSystem` uses any assemblers it has to set up the linear system
   _Ax=b_ that will be solved that timestep. _A_ is just assembled once the
   first timestep. For _b_ the solver (or its assemblers) will require the ionic
   current and stimulus at each cell; this is obtained by calling, for example,
   `mpMonodomainTissue->rGetIionicCacheReplicated()[index]`. For more details on
   setting up _b_ and the method `SetupLinearSystem` see
   [Finite Element Assemblers and Solvers](../finite-element-assemblers-and-solvers).
