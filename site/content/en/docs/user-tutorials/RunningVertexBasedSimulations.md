
---
title : "TestRunningVertexBasedSimulationsTutorial.hpp"
description: "This tutorial is automatically generated from the file cell_based/test/tutorial/TestRunningVertexBasedSimulationsTutorial.hpp at revision [1288aa7fe4cc](https://github.com/Chaste/Chaste/commit/1288aa7fe4ccb5438b05f81253fe167e350cdc10). Note that the code is given in full at the bottom of the page."
draft: false
images: []
toc: true
---

# Examples showing how to create, run and visualize vertex-based simulations 

## Introduction 

In this tutorial we show how Chaste can be used to create, run and visualize vertex-based simulations.
Full details of the mechanical model proposed by T. Nagai and H. Honda ("A dynamic cell model for
the formation of epithelial tissues", Philosophical Magazine Part B 81:699-719).

## The test 

As in previous cell-based Chaste tutorials, we begin by including the necessary header files.

```cpp
#include <cxxtest/TestSuite.h>
#include "CheckpointArchiveTypes.hpp"
#include "AbstractCellBasedTestSuite.hpp"

```
The remaining header files define classes that will be used in the cell-based
simulation. We have encountered some of these header files in previous cell-based
Chaste tutorials.
```cpp
#include "CellsGenerator.hpp"
#include "OffLatticeSimulation.hpp"
#include "TransitCellProliferativeType.hpp"
#include "SmartPointers.hpp"
```
The next header file defines the cell cycle model.
```cpp
#include "UniformG1GenerationalCellCycleModel.hpp"
```
The next two header files define a helper class for generating suitable meshes: one planar and one periodic.
```cpp
#include "HoneycombVertexMeshGenerator.hpp"
#include "CylindricalHoneycombVertexMeshGenerator.hpp"
```
The next header file defines a vertex-based {{{CellPopulation}}} class.
```cpp
#include "VertexBasedCellPopulation.hpp"
```
The next header file defines a force law for describing the mechanical interactions
between neighbouring cells in the cell population, subject to each vertex.

```cpp
#include "NagaiHondaForce.hpp"
```
This force law assumes that cells possess a "target area" property which determines the size of each
cell in the simulation. In order to assign target areas to cells and update them in each time step, we need
the next header file.

```cpp
#include "SimpleTargetAreaModifier.hpp"
```
The next header file defines a boundary condition for the cells.
```cpp
#include "PlaneBoundaryCondition.hpp"
```
The next header file defines a cell killer, which specifies how cells are removed from the simulation.
```cpp
#include "PlaneBasedCellKiller.hpp"

```
Finally, we include a header that enforces running this test only on one process.
```cpp
#include "FakePetscSetup.hpp"

```
Next, we define the test class, which inherits from `AbstractCellBasedTestSuite`{.cpp}
and defines some test methods.

```cpp
class TestRunningVertexBasedSimulationsTutorial : public AbstractCellBasedTestSuite
{
public:
```

## Test 1 - a basic vertex-based simulation 

In the first test, we run a simple vertex-based simulation, in which we create a monolayer
of cells, using a mutable vertex mesh. Each cell is assigned a stochastic cell-cycle model.

```cpp
    void TestMonolayer()
    {
```
First, we generate a vertex mesh. To create a `MutableVertexMesh`{.cpp}, we can use
the `HoneycombVertexMeshGenerator`{.cpp}. This generates a honeycomb-shaped mesh,
in which all nodes are equidistant. Here the first and second arguments
define the size of the mesh - we have chosen a mesh that is 2 elements (i.e.
cells) wide, and 2 elements high.

```cpp
        HoneycombVertexMeshGenerator generator(2, 2);    // Parameters are: cells across, cells up
        boost::shared_ptr<MutableVertexMesh<2,2> > p_mesh = generator.GetMesh();

```
Having created a mesh, we now create a `std::vector`{.cpp} of `CellPtr`{.cpp}s.
To do this, we use the `CellsGenerator` helper class, which is templated over the type
of cell model required (here `UniformG1GenerationalCellCycleModel`{.cpp})
and the dimension. We create an empty vector of cells and pass this into the
method along with the mesh. The second argument represents the size of that the vector
`cells`{.cpp} should become - one cell for each element, the third argument specifies
the proliferative type of the cell.
```cpp
        std::vector<CellPtr> cells;
        MAKE_PTR(TransitCellProliferativeType, p_transit_type);
        CellsGenerator<UniformG1GenerationalCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasicRandom(cells, p_mesh->GetNumElements(), p_transit_type);

```
Now we have a mesh and a set of cells to go with it, we can create a `CellPopulation`{.cpp}.
In general, this class associates a collection of cells with a mesh.
For this test, because we have a `MutableVertexMesh`{.cpp}, we use a particular type of
cell population called a `VertexBasedCellPopulation`{.cpp}.

```cpp
        VertexBasedCellPopulation<2> cell_population(*p_mesh, cells);

```
We then pass the cell population into an `OffLatticeSimulation`{.cpp},
and set the output directory and end time.
```cpp
        OffLatticeSimulation<2> simulator(cell_population);
        simulator.SetOutputDirectory("VertexBasedMonolayer");
        simulator.SetEndTime(1.0);

```
For longer simulations, we may not want to output the results
every time step. In this case we can use the following method,
to print results every 50 time steps instead. As the default time step
used by the simulator (for vertex based simulations), is 0.02 hours, this method will cause the
simulator to print results every 6 minutes (i.e. 0.1 hours).

```cpp
        simulator.SetSamplingTimestepMultiple(50);

```
We must now create one or more force laws, which determine the mechanics of the vertices
of each cell in a cell population. For this test, we use one force law, based on the
Nagai-Honda mechanics, and pass it to the `OffLatticeSimulation`{.cpp}.
For a list of possible forces see subclasses of `AbstractForce`{.cpp}.
These can be found in the inheritance diagram, here, [class:AbstractForce AbstractForce].
Note that some of these forces are not compatible with vertex-based simulations see the specific class documentation for details,
if you try to use an incompatible class then you will receive a warning.

```cpp
        MAKE_PTR(NagaiHondaForce<2>, p_force);
        simulator.AddForce(p_force);

```
A `NagaiHondaForce`{.cpp} assumes that each cell has a target area. The target areas of cells are used to determine pressure
forces on each vertex and eventually determine the size of each cell in the simulation. In order to assign target areas to cells
and update them in each time step to model growth, we add a `SimpleTargetAreaModifier`{.cpp} to the simulation, which inherits from
`AbstractTargetAreaModifier`{.cpp}.

```cpp
        MAKE_PTR(SimpleTargetAreaModifier<2>, p_growth_modifier);
        simulator.AddSimulationModifier(p_growth_modifier);

```
To run the simulation, we call {{{Solve()}}}.
```cpp
        simulator.Solve();

```
The next two lines are for test purposes only and are not part of this tutorial. If different simulation input parameters are being explored
the lines should be removed.
```cpp
        TS_ASSERT_EQUALS(cell_population.GetNumRealCells(), 4u);
        TS_ASSERT_DELTA(SimulationTime::Instance()->GetTime(), 1.0, 1e-10);
    }

```
To visualize the results, open a new terminal, `cd`{.cpp} to the Chaste directory,
then `cd`{.cpp} to `anim`{.cpp}. Then do: `java Visualize2dVertexCells /tmp/$USER/testoutput/VertexBasedMonolayer/results_from_time_0`{.cpp}.
We may have to do: `javac Visualize2dVertexCells.java`{.cpp} beforehand to create the
java executable.

## Test 2 - introducing periodicity, boundaries and cell killers 

In the second test, we run a simple vertex-based simulation, in which we create a monolayer
of cells in a periodic geometry, using a cylindrical vertex mesh. We also include a fixed
boundary which cells can't pass through and a cell killer which removes cells once they leave
a region. As before each cell is assigned a stochastic cell-cycle model.

```cpp
    void TestPeriodicMonolayer()
    {
```
First, we generate a periodic vertex mesh. To create a `Cylindrical2dVertexMesh`{.cpp}, we can use
the `CylindricalHoneycombVertexMeshGenerator`{.cpp}. This generates a honeycomb-shaped mesh,
in which all nodes are equidistant and the right hand side is associated with the left hand side.
Here the first and second arguments define the size of the mesh - we have chosen a mesh that
is 4 elements (i.e. cells) wide, and 4 elements high.

```cpp
        CylindricalHoneycombVertexMeshGenerator generator(4, 4);    // Parameters are: cells across, cells up
        boost::shared_ptr<Cylindrical2dVertexMesh> p_mesh = generator.GetCylindricalMesh();

```
Having created a mesh, we now create a `std::vector`{.cpp} of `CellPtr`{.cpp}s.
This is exactly the same as the above test.
```cpp
        std::vector<CellPtr> cells;
        MAKE_PTR(TransitCellProliferativeType, p_transit_type);
        CellsGenerator<UniformG1GenerationalCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasicRandom(cells, p_mesh->GetNumElements(), p_transit_type);

```
Now we have a mesh and a set of cells to go with it, we can create a `CellPopulation`{.cpp}.
This is also the same as in the above test.

```cpp
        VertexBasedCellPopulation<2> cell_population(*p_mesh, cells);

```
As always we then pass the cell population into an `OffLatticeSimulation`{.cpp},
and set the output directory, output multiple and end time.
```cpp
        OffLatticeSimulation<2> simulator(cell_population);
        simulator.SetOutputDirectory("VertexBasedPeriodicMonolayer");
        simulator.SetSamplingTimestepMultiple(50);
        simulator.SetEndTime(1.0);

```
We now make a pointer to an appropriate force and pass it to the
`OffLatticeSimulation`{.cpp}.

```cpp
        MAKE_PTR(NagaiHondaForce<2>, p_force);
        simulator.AddForce(p_force);

```
We also make a pointer to a target area modifier and add it to the simulator.

```cpp
        MAKE_PTR(SimpleTargetAreaModifier<2>, p_growth_modifier);
        simulator.AddSimulationModifier(p_growth_modifier);

```
We now create one or more `CellPopulationBoundaryCondition`{.cpp}s, which determine
any conditions which each cell in a cell population must satisfy. For this test,
we use a `PlaneBoundaryCondition`{.cpp}, and pass it to the `OffLatticeSimulation`{.cpp}.
For a list of possible boundary condition see subclasses of `AbstractCellPopulationBoundaryCondition`{.cpp}.
These can be found in the inheritance diagram, here,
[class:AbstractCellPopulationBoundaryCondition AbstractCellPopulationBoundaryCondition].
Note that some of these boundary conditions are not compatible with vertex-based
simulations see the specific class documentation for details, if you try to use an
incompatible class then you will receive a warning.

The first step is to define a point on the plane boundary and a normal to the plane.

```cpp
        c_vector<double,2> point = zero_vector<double>(2);
        c_vector<double,2> normal = zero_vector<double>(2);
        normal(1) = -1.0;
```
We can now make a pointer to a `PlaneBoundaryCondition`{.cpp} (passing the point
and normal to the plane) and pass it to the {{{OffLatticeSimulation}}}.
```cpp
        MAKE_PTR_ARGS(PlaneBoundaryCondition<2>, p_bc, (&cell_population, point, normal));
        simulator.AddCellPopulationBoundaryCondition(p_bc);

```
We now create one or more `CellKiller`{.cpp}s, which determine how cells are removed
from the simulation. For this test, we use a `PlaneBasedCellKiller`{.cpp}, and pass
it to the `OffLatticeSimulation`{.cpp}. For a list of possible cell killers see subclasses
of `AbstractCellKiller`{.cpp}. These can be found in the inheritance diagram, here,
[class:AbstractCellKiller AbstractCellKiller].

The first step is to define a point on the plane boundary and a normal to the plane.
We reuse the point and normal from the `PlaneBoundaryCondition`{.cpp}.

```cpp
        point(1) = 3.0;
        normal(1) = 1.0;
```
Finally we now make a pointer to a `PlaneBasedCellKiller`{.cpp} (passing the point
and normal to the plane) and pass it to the {{{OffLatticeSimulation}}}.
```cpp
        MAKE_PTR_ARGS(PlaneBasedCellKiller<2>, p_killer, (&cell_population, point, normal));
        simulator.AddCellKiller(p_killer);

```
To run the simulation, we call {{{Solve()}}}.
```cpp
        simulator.Solve();

```
The next two lines are for test purposes only and are not part of this tutorial.

```cpp
        TS_ASSERT_EQUALS(cell_population.GetNumRealCells(), 12u);
        TS_ASSERT_DELTA(SimulationTime::Instance()->GetTime(), 1.0, 1e-10);
    }
```

To visualize the results, open a new terminal, `cd`{.cpp} to the Chaste directory,
then `cd`{.cpp} to `anim`{.cpp}. Then do: `java Visualize2dVertexCells /tmp/$USER/testoutput/VertexBasedPeriodicMonolayer/results_from_time_0`{.cpp}.

You should see that the edges of the mesh are identical on both sides; cells no
longer pass through the line y=0; and cells are removed at y=3.

```cpp
};

```


# Code
The full code is given below


## File name `TestRunningVertexBasedSimulationsTutorial.hpp` 

```cpp
#include <cxxtest/TestSuite.h>
#include "CheckpointArchiveTypes.hpp"
#include "AbstractCellBasedTestSuite.hpp"

#include "CellsGenerator.hpp"
#include "OffLatticeSimulation.hpp"
#include "TransitCellProliferativeType.hpp"
#include "SmartPointers.hpp"
#include "UniformG1GenerationalCellCycleModel.hpp"
#include "HoneycombVertexMeshGenerator.hpp"
#include "CylindricalHoneycombVertexMeshGenerator.hpp"
#include "VertexBasedCellPopulation.hpp"
#include "NagaiHondaForce.hpp"
#include "SimpleTargetAreaModifier.hpp"
#include "PlaneBoundaryCondition.hpp"
#include "PlaneBasedCellKiller.hpp"

#include "FakePetscSetup.hpp"

class TestRunningVertexBasedSimulationsTutorial : public AbstractCellBasedTestSuite
{
public:
    void TestMonolayer()
    {
        HoneycombVertexMeshGenerator generator(2, 2);    // Parameters are: cells across, cells up
        boost::shared_ptr<MutableVertexMesh<2,2> > p_mesh = generator.GetMesh();

        std::vector<CellPtr> cells;
        MAKE_PTR(TransitCellProliferativeType, p_transit_type);
        CellsGenerator<UniformG1GenerationalCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasicRandom(cells, p_mesh->GetNumElements(), p_transit_type);

        VertexBasedCellPopulation<2> cell_population(*p_mesh, cells);

        OffLatticeSimulation<2> simulator(cell_population);
        simulator.SetOutputDirectory("VertexBasedMonolayer");
        simulator.SetEndTime(1.0);

        simulator.SetSamplingTimestepMultiple(50);

        MAKE_PTR(NagaiHondaForce<2>, p_force);
        simulator.AddForce(p_force);

        MAKE_PTR(SimpleTargetAreaModifier<2>, p_growth_modifier);
        simulator.AddSimulationModifier(p_growth_modifier);

        simulator.Solve();

        TS_ASSERT_EQUALS(cell_population.GetNumRealCells(), 4u);
        TS_ASSERT_DELTA(SimulationTime::Instance()->GetTime(), 1.0, 1e-10);
    }

    void TestPeriodicMonolayer()
    {
        CylindricalHoneycombVertexMeshGenerator generator(4, 4);    // Parameters are: cells across, cells up
        boost::shared_ptr<Cylindrical2dVertexMesh> p_mesh = generator.GetCylindricalMesh();

        std::vector<CellPtr> cells;
        MAKE_PTR(TransitCellProliferativeType, p_transit_type);
        CellsGenerator<UniformG1GenerationalCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasicRandom(cells, p_mesh->GetNumElements(), p_transit_type);

        VertexBasedCellPopulation<2> cell_population(*p_mesh, cells);

        OffLatticeSimulation<2> simulator(cell_population);
        simulator.SetOutputDirectory("VertexBasedPeriodicMonolayer");
        simulator.SetSamplingTimestepMultiple(50);
        simulator.SetEndTime(1.0);

        MAKE_PTR(NagaiHondaForce<2>, p_force);
        simulator.AddForce(p_force);

        MAKE_PTR(SimpleTargetAreaModifier<2>, p_growth_modifier);
        simulator.AddSimulationModifier(p_growth_modifier);

        c_vector<double,2> point = zero_vector<double>(2);
        c_vector<double,2> normal = zero_vector<double>(2);
        normal(1) = -1.0;
        MAKE_PTR_ARGS(PlaneBoundaryCondition<2>, p_bc, (&cell_population, point, normal));
        simulator.AddCellPopulationBoundaryCondition(p_bc);

        point(1) = 3.0;
        normal(1) = 1.0;
        MAKE_PTR_ARGS(PlaneBasedCellKiller<2>, p_killer, (&cell_population, point, normal));
        simulator.AddCellKiller(p_killer);

        simulator.Solve();

        TS_ASSERT_EQUALS(cell_population.GetNumRealCells(), 12u);
        TS_ASSERT_DELTA(SimulationTime::Instance()->GetTime(), 1.0, 1e-10);
    }
};

```

