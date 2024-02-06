# Solving a cardiac problem

This page gives a high-level overview of the code execution flow when solving a cardiac problem.  To run simulations, see UserTutorials. For an overview of the PDE solver hierarchy, see [FiniteElementAssemblersAndSolvers](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Finite-Element-Assemblers-And-Solvers). The steps that occur are as follows

* The user calls `AbstractCardiacProblem::Solve()` on their monodomain or bidomain problem object (after calling `Initialise`)
* The `AbstractCardiacProblem` owns a particular mono/bidomain finite element *solver* (of base-class type `AbstractDynamicLinearPdeSolver`; the concrete class can be matrix-based or not; see [FiniteElementAssemblersAndSolvers](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Finite-Element-Assemblers-And-Solvers) for more details); and for each printing timestep, does the following:
    * sets the current time and end time on the solver
    * sets the latest voltage solution on the solver as the initial condition
    * calls `Solve` on the solver.


-----

The `Solve` method on `AbstractDynamicLinearPdeSolver` does the following, for each PDE timestep

* calls `PrepareForSetupLinearSystem` -- *solves cell models, see below*
* calls `SetupLinearSystem`  -- *see below*
* calls `FinaliseLinearSystem`  -- relevant for bidomain solves, things like checking compatibility, setting up a null space
* solves the linear system to obtain the solution (voltage, and phi_e in bidomain setting) at the next timestep


-----

1. `PrepareForLinearSystem` is where the cell models are solved. It is implemented in `AbstractMonodomainSolver`/`AbstractBidomainSolver`, where it just calls `SolveCellSystems` on the `MonodomainTissue`/`BidomainTissue`. This is implemented in `AbstractCardiacTissue::SolveCellSystems`, which essentially does the following for each cell:
   1. Set *V* from the current PDE solution
   2. Call the cell's `ComputeExceptVoltage` to solve for all state variables except *V* until the next PDE time step
   3. Call `UpdateCaches`. This calls the cell's `GetIIonic` to compute the *I_ion* term and stores it in `mIionicCacheReplicated` (replicated over each process so no parallel communication is required later). It similarly also calculates and caches the intracellular stimulus at each cell.

-----

2. `SetupLinearSystem` uses any assemblers it has to set up the linear system *Ax=b* that will be solved that timestep. *A* is just assembled once the first timestep. For *b* the solver (or its assemblers) will require the ionic current and stimulus at each cell; this is obtained by calling, for example, `mpMonodomainTissue->rGetIionicCacheReplicated()[index]`. For more details on setting up *b* and the method `SetupLinearSystem` see [FiniteElementAssemblersAndSolvers](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Finite-Element-Assemblers-And-Solvers).



