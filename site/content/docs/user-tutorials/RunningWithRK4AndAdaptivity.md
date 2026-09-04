---
title : "Running With R K 4A Adaptivity"
summary: "Using RK4 and adaptive time-stepping in off-lattice simulations"
draft: false
images: []
toc: true
---
This tutorial is automatically generated from [TestRunningWithRK4AndAdaptivityTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/cell_based/test/tutorial/TestRunningWithRK4AndAdaptivityTutorial.hpp) at revision [dafb8eec7f7e](https://github.com/Chaste/Chaste/commit/dafb8eec7f7e753bd1443f2df6250eb642c13b98). Note that the code is given in full at the bottom of the page.
## Using RK4 and adaptive time-stepping in off-lattice simulations

### Introduction

This tutorial demonstrates how to use the `RK4NumericalMethod` and the **adaptive
timestep** feature with off-lattice cell-based simulations in Chaste.

Off-lattice simulations advance node positions by solving the overdamped equations
of motion

dr/dt = F(r) / nu

where F(r) is the net force on a cell and nu is a drag coefficient. Two integration
schemes are available:

 * `ForwardEulerNumericalMethod` (the default): a first-order explicit scheme.
 * `RK4NumericalMethod`: the classic 4th-order Runge-Kutta scheme, which evaluates
 forces at four intermediate positions per step and combines them as
 
k1 = F(r^t) / nu
k2 = F(r^t + dt*k1/2) / nu
k3 = F(r^t + dt*k2/2) / nu
k4 = F(r^t + dt*k3) / nu
r^(t+1) = r^t + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)

#### Adaptive time-stepping

When cells overlap or a node moves too far in a single step, the numerical method
calls `AbstractOffLatticeCellPopulation::CheckForStepSizeException()`, which throws a
`StepSizeException` carrying a suggested smaller step size.

The control loop inside `OffLatticeSimulation::UpdateCellLocationsAndTopology()` then

1. reverts all node positions to their state at the start of the sub-step, and
2. retries the step with the suggested smaller sub-step size which is a power of 2 smaller.
i.e. the timestep is halved until the movement threshold is met.

Each macro time step `dt` may therefore be completed in several sub-steps that sum to
`dt`. If more than `mMaxAdaptiveTimeSteps` consecutive sub-steps fail, the simulation
terminates with an error.

Adaptive time-stepping is enabled by calling

p_numerical_method->SetUseAdaptiveTimestep(true);

The maximum movement threshold for a single sub-step can be set with

population.SetAbsoluteMovementThreshold(maxMovement);

The maximum number of consecutive failed sub-steps can be set with

simulator.SetMaxAdaptiveTimeStep(n);

### The test

We begin by including the necessary header files.

```cpp
#include <cxxtest/TestSuite.h>
#include "CheckpointArchiveTypes.hpp"
```

The following header is included in all cell-based test suites.

```cpp
#include "AbstractCellBasedTestSuite.hpp"
#include "PetscSetupAndFinalize.hpp"
```

Standard cell-based simulation headers.

```cpp
#include "CellsGenerator.hpp"
#include "DifferentiatedCellProliferativeType.hpp"
#include "UniformCellCycleModel.hpp"
#include "HoneycombMeshGenerator.hpp"
#include "PathmanathanInteractionForce.hpp"
#include "OffLatticeSimulation.hpp"
#include "SmartPointers.hpp"
#include "NodesOnlyMesh.hpp"
#include "NodeBasedCellPopulation.hpp"
```

The following header gives us the RK4 numerical method used in this tutorial.

```cpp
#include "RK4NumericalMethod.hpp"
```

Next, we define the test class.

```cpp
class TestRunningWithRK4AndAdaptivityTutorial : public AbstractCellBasedTestSuite
{
public:
```

### Test 1 - a node-based simulation using `RK4NumericalMethod`

In the first test we run a simple node-based simulation and replace the default
Forward Euler integrator with the 4th-order Runge-Kutta (`RK4`) method.
The simulation is otherwise identical to the basic node-based tutorial so that
the substitution is as clear as possible.

```cpp
    void TestRK4NodeBasedSimulation()
    {
        /** The next line is needed because HoneycombMeshGenerator is not designed to be run in parallel */
        EXIT_IF_PARALLEL;
```

First we generate a small honeycomb mesh to use as the generating mesh for a
`NodesOnlyMesh`. We choose a cut-off radius of 1.5 cell diameters to define
which pairs of cells interact via the spring force.

```cpp
        HoneycombMeshGenerator generator(3, 3);
        boost::shared_ptr<MutableMesh<2,2> > p_generating_mesh = generator.GetMesh();
        NodesOnlyMesh<2> mesh;
        mesh.ConstructNodesWithoutMesh(*p_generating_mesh, 1.5);
```

Create one cell per node using a uniform cell-cycle model.

```cpp
        std::vector<CellPtr> cells;
        MAKE_PTR(DifferentiatedCellProliferativeType, p_diff_type);
        CellsGenerator<UniformCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasicRandom(cells, mesh.GetNumNodes(), p_diff_type);
```

Assemble the cell population.

```cpp
        NodeBasedCellPopulation<2> cell_population(mesh, cells);
```

Set up the simulator.

```cpp
        OffLatticeSimulation<2> simulator(cell_population);
        simulator.SetOutputDirectory("NodeBasedRK4");
        simulator.SetSamplingTimestepMultiple(12);
        simulator.SetEndTime(2.0);
```

 **Switch to RK4.**
 
We create an `RK4NumericalMethod` object using `boost::make_shared` and pass
it to the simulator.  This replaces the default Forward Euler method for the
entire simulation.

```cpp
        boost::shared_ptr<RK4NumericalMethod<2> > p_numerical_method
            = boost::make_shared<RK4NumericalMethod<2> >();
        simulator.SetNumericalMethod(p_numerical_method);
```

Add a spring force between neighbouring cells.

```cpp
        MAKE_PTR(PathmanathanInteractionForce<2>, p_force);
        simulator.AddForce(p_force);
```

Run the simulation.

```cpp
        simulator.Solve();
```

The next two lines are for test purposes only and are not part of this tutorial.
If different simulation input parameters are being explored the lines should be removed.

```cpp
        TS_ASSERT_EQUALS(cell_population.GetNumRealCells(), 9u);
        TS_ASSERT_DELTA(SimulationTime::Instance()->GetTime(), 2.0, 1e-10);
    }
```

### Test 2 - adaptive time-stepping with `RK4NumericalMethod`

In this test we demonstrate the **adaptive timestep** feature.  We enable
adaptivity so that if a node tries to move further than allowed in a single
sub-step, the solver automatically reduces the sub-step, reverts the node
positions, and retries.

#### How the adaptive loop works

Inside `OffLatticeSimulation::UpdateCellLocationsAndTopology()` each macro
time step `dt` is completed by a `while` loop:
```
time_advanced = 0
sub_step = dt              // start with the full macro step
adaptive_timer = 0         // counts consecutive failures

while (time_advanced < dt):

try:
move nodes by sub_step             // may throw StepSizeException
apply boundary conditions
time_advanced += sub_step
adaptive_timer = 0                 // reset on success

catch StepSizeException e (i.e. node movement too large):
if adaptive_timer < max_adaptive_steps:
revert nodes to saved positions
sub_step = e.GetSuggestedNewStep()
adaptive_timer += 1
else:
EXCEPTION (too many consecutive failures)
```

The `StepSizeException` is raised inside the numerical method whenever
`AbstractOffLatticeCellPopulation::CheckForStepSizeException()` detects that a node
would move further than its permitted maximum displacement.  The exception
carries a smaller suggested step size.  `SetMaxAdaptiveTimeStep(n)` controls
how many consecutive failures are tolerated before the simulation aborts.

```cpp
    void TestAdaptiveTimestepWithRK4()
    {
        /** The next line is needed because HoneycombMeshGenerator is not designed to be run in parallel */
        EXIT_IF_PARALLEL;
```

Build a small node-based mesh.

```cpp
        HoneycombMeshGenerator generator(3, 3);
        boost::shared_ptr<MutableMesh<2,2> > p_generating_mesh = generator.GetMesh();
        NodesOnlyMesh<2> mesh;
        mesh.ConstructNodesWithoutMesh(*p_generating_mesh, 1.5);
```

Create one cell per node.

```cpp
        std::vector<CellPtr> cells;
        MAKE_PTR(DifferentiatedCellProliferativeType, p_diff_type);
        CellsGenerator<UniformCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasicRandom(cells, mesh.GetNumNodes(), p_diff_type);

        NodeBasedCellPopulation<2> cell_population(mesh, cells);
```

Set up the simulator with a moderately large time step.

```cpp
        OffLatticeSimulation<2> simulator(cell_population);
        simulator.SetOutputDirectory("NodeBasedRK4Adaptive");
        simulator.SetSamplingTimestepMultiple(10);
        simulator.SetEndTime(2.0);
        simulator.SetDt(0.1); // This is the macro time step that the simulation will try to take at each iteration.  The adaptive loop will reduce this as needed.
```

Create an RK4 numerical method and **enable adaptive time-stepping**.

With `SetUseAdaptiveTimestep(true)` the solver will automatically
reduce the sub-step whenever a `StepSizeException` is detected,
revert the node positions to those saved at the start of the sub-step,
and retry with the smaller step.

```cpp
        boost::shared_ptr<RK4NumericalMethod<2> > p_numerical_method
            = boost::make_shared<RK4NumericalMethod<2> >();
        p_numerical_method->SetUseAdaptiveTimestep(true);
        simulator.SetNumericalMethod(p_numerical_method);
```

Set a small movement threshold to trigger adaptivity.  Here we allow a maximum movement of 0.001 cell diameters per sub-step.

```cpp
        cell_population.SetAbsoluteMovementThreshold(0.001);
```

Optionally increase the maximum number of consecutive failed sub-steps
from the default of 5.  Here we allow up to 10 retries so that the
simulation can recover from larger overlaps if needed.

```cpp
        simulator.SetMaxAdaptiveTimeStep(10);
```

Add a spring force.

```cpp
        MAKE_PTR(PathmanathanInteractionForce<2>, p_force);
        simulator.AddForce(p_force);
```

Run the simulation.  The adaptive loop will silently reduce the sub-step
whenever cells come too close and retry until the step succeeds.

```cpp
        simulator.Solve();
```

The next two lines are for test purposes only and are not part of this tutorial.
If different simulation input parameters are being explored the lines should be removed.

```cpp
        TS_ASSERT_EQUALS(cell_population.GetNumRealCells(), 9u);
        TS_ASSERT_DELTA(SimulationTime::Instance()->GetTime(), 2.0, 1e-10);
    }
};
```

To visualize the results, use Paraview. See the [Visualizing With Paraview](../visualizingwithparaview/) tutorial for more information.
Note data is only output at the end of each macro time step, so the adaptive sub-steps are not visible in the output files.

Load the file `$CHASTE_TEST_OUTPUT/NodeBasedRK4/results_from_time_0/results.pvd`
and add glyphs to represent cells.

## Full code

```cpp
#include <cxxtest/TestSuite.h>
#include "CheckpointArchiveTypes.hpp"

#include "AbstractCellBasedTestSuite.hpp"
#include "PetscSetupAndFinalize.hpp"

#include "CellsGenerator.hpp"
#include "DifferentiatedCellProliferativeType.hpp"
#include "UniformCellCycleModel.hpp"
#include "HoneycombMeshGenerator.hpp"
#include "PathmanathanInteractionForce.hpp"
#include "OffLatticeSimulation.hpp"
#include "SmartPointers.hpp"
#include "NodesOnlyMesh.hpp"
#include "NodeBasedCellPopulation.hpp"

#include "RK4NumericalMethod.hpp"

class TestRunningWithRK4AndAdaptivityTutorial : public AbstractCellBasedTestSuite
{
public:

    void TestRK4NodeBasedSimulation()
    {
        /** The next line is needed because HoneycombMeshGenerator is not designed to be run in parallel */
        EXIT_IF_PARALLEL;

        HoneycombMeshGenerator generator(3, 3);
        boost::shared_ptr<MutableMesh<2,2> > p_generating_mesh = generator.GetMesh();
        NodesOnlyMesh<2> mesh;
        mesh.ConstructNodesWithoutMesh(*p_generating_mesh, 1.5);

        std::vector<CellPtr> cells;
        MAKE_PTR(DifferentiatedCellProliferativeType, p_diff_type);
        CellsGenerator<UniformCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasicRandom(cells, mesh.GetNumNodes(), p_diff_type);

        NodeBasedCellPopulation<2> cell_population(mesh, cells);

        OffLatticeSimulation<2> simulator(cell_population);
        simulator.SetOutputDirectory("NodeBasedRK4");
        simulator.SetSamplingTimestepMultiple(12);
        simulator.SetEndTime(2.0);

        boost::shared_ptr<RK4NumericalMethod<2> > p_numerical_method
            = boost::make_shared<RK4NumericalMethod<2> >();
        simulator.SetNumericalMethod(p_numerical_method);

        MAKE_PTR(PathmanathanInteractionForce<2>, p_force);
        simulator.AddForce(p_force);

        simulator.Solve();

        TS_ASSERT_EQUALS(cell_population.GetNumRealCells(), 9u);
        TS_ASSERT_DELTA(SimulationTime::Instance()->GetTime(), 2.0, 1e-10);
    }

    void TestAdaptiveTimestepWithRK4()
    {
        /** The next line is needed because HoneycombMeshGenerator is not designed to be run in parallel */
        EXIT_IF_PARALLEL;

        HoneycombMeshGenerator generator(3, 3);
        boost::shared_ptr<MutableMesh<2,2> > p_generating_mesh = generator.GetMesh();
        NodesOnlyMesh<2> mesh;
        mesh.ConstructNodesWithoutMesh(*p_generating_mesh, 1.5);

        std::vector<CellPtr> cells;
        MAKE_PTR(DifferentiatedCellProliferativeType, p_diff_type);
        CellsGenerator<UniformCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasicRandom(cells, mesh.GetNumNodes(), p_diff_type);

        NodeBasedCellPopulation<2> cell_population(mesh, cells);

        OffLatticeSimulation<2> simulator(cell_population);
        simulator.SetOutputDirectory("NodeBasedRK4Adaptive");
        simulator.SetSamplingTimestepMultiple(10);
        simulator.SetEndTime(2.0);
        simulator.SetDt(0.1); // This is the macro time step that the simulation will try to take at each iteration.  The adaptive loop will reduce this as needed.

        boost::shared_ptr<RK4NumericalMethod<2> > p_numerical_method
            = boost::make_shared<RK4NumericalMethod<2> >();
        p_numerical_method->SetUseAdaptiveTimestep(true);
        simulator.SetNumericalMethod(p_numerical_method);

        cell_population.SetAbsoluteMovementThreshold(0.001);

        simulator.SetMaxAdaptiveTimeStep(10);

        MAKE_PTR(PathmanathanInteractionForce<2>, p_force);
        simulator.AddForce(p_force);

        simulator.Solve();

        TS_ASSERT_EQUALS(cell_population.GetNumRealCells(), 9u);
        TS_ASSERT_DELTA(SimulationTime::Instance()->GetTime(), 2.0, 1e-10);
    }
};
```
