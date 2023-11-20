
---
title : "Running Tumour Spheroid Simulations Tutorial"
summary: "This tutorial is automatically generated from the file cell_based/test/tutorial/TestRunningTumourSpheroidSimulationsTutorial.hpp at revision [c64c70046e25](https://github.com/Chaste/Chaste/commit/c64c70046e25e3f67b47ec3e92f29cb02d5e6830). Note that the code is given in full at the bottom of the page."
draft: false
images: []
toc: true
---

# An example showing how to run tumour spheroid simulations 

## Introduction 

In this tutorial we show how Chaste can be used to simulate a growing cell monolayer culture or
multicellular tumour spheroid. Like the crypt simulations, tumour spheroid simulations
include cell-cycle models and force laws to determine how cells divide and
move. In tumour spheroid simulations, however, these are also coupled to a
system of partial differential equations (PDEs) that determine the concentration
of specified nutrients (e.g. oxygen) throughout the cell population. Also, unlike
in a crypt simulation (for example), the cell population may grow substantially as the simulation
progresses.

In summary, the main difference between this tutorial and the other cell-based simulation
tutorials is that a PDE is defined, which is used in the simulation.

## The test 

As in the other cell-based simulation tutorials, we begin by including the necessary header files. We have
encountered some of these files already. Recall that often `CheckpointArchiveTypes.hpp`{.cpp}
or `CellBasedSimulationArchiver.hpp`{.cpp} must be included as the first Chaste header.

```cpp
#include <cxxtest/TestSuite.h>
#include "CheckpointArchiveTypes.hpp"
#include "AbstractCellBasedTestSuite.hpp"
#include "HoneycombMeshGenerator.hpp"
#include "GeneralisedLinearSpringForce.hpp"
#include "RandomNumberGenerator.hpp"
#include "SmartPointers.hpp"
```

The `SimpleOxygenBasedCellCycleModel`{.cpp} header file defines a cell-cycle model in which
a cell's rate of progress through G1 phase changes over time in a simple manner, according
to the local oxygen concentration. We also include the `WildTypeCellMutationState`{.cpp}
header file, which defines a wild type cell mutation state that we will use to construct
cells. A cell mutation state is always required when constructing a cell, however
in earlier simulation tutorial we used a helper classes ((`CellsGenerator`{.cpp} and `CryptCellsGenerator`{.cpp}) that
allowed us to avoid having to construct cells directly.

```cpp
#include "SimpleOxygenBasedCellCycleModel.hpp"
#include "WildTypeCellMutationState.hpp"
#include "StemCellProliferativeType.hpp"
```

The next three header files define: a PDE that describes how oxygen is transported via through the
domain via diffusion and is consumed by live cells; a constant-valued boundary condition to
associate with the PDE; and a PDE modifier class, which is passed to the simulation object and
handles the numerical solution of any PDEs.

```cpp
#include "CellwiseSourceEllipticPde.hpp"
#include "ConstBoundaryCondition.hpp"
#include "EllipticGrowingDomainPdeModifier.hpp"

```
We use an `OffLatticeSimulation`{.cpp}.

```cpp
#include "OffLatticeSimulation.hpp"
```

The header file `PetscSetupAndFinalize.hpp`{.cpp} must be included in all tests which use Petsc. This is
a suite of data structures and routines that are used in the finite element
PDE solvers, which is how we solve the oxygen transport PDE.

```cpp
#include "PetscSetupAndFinalize.hpp"

```
Having included all the necessary header files, we proceed by defining the test class.

```cpp
class TestRunningTumourSpheroidSimulationsTutorial : public AbstractCellBasedTestSuite
{
public:
    void TestSpheroidTutorial()
    {
```

This first line can be ignored: it is a macro which just says
don't run this test if in parallel.

```cpp
        EXIT_IF_PARALLEL;

```
First we want to create a '''non-periodic''' 'honeycomb' mesh.
We use the honeycomb mesh generator, as before, saying 10 cells wide
and 10 cells high. Note that the thickness of the ghost nodes layer is
0, i.e. there are no ghost nodes, and the `false`{.cpp} indicates that the
returned mesh is '''not''' cylindrical. In contrast to the crypt simulation
tutorial, here we call `GetMesh()`{.cpp} on the `HoneycombMeshGenerator`{.cpp}
object to return the mesh, which is of type `MutableMesh`{.cpp}.

```cpp
        HoneycombMeshGenerator generator(10, 10, 0);
        boost::shared_ptr<MutableMesh<2,2> > p_mesh = generator.GetMesh();

```
Next, we need to create some cells. Unlike in the the crypt simulation
tutorial, we don't just use a `CellsGenerator`{.cpp} class, but do it manually,
in a loop. First, we define a `std::vector`{.cpp} of cell pointers.

```cpp
        std::vector<CellPtr> cells;

```
This line defines a mutation state to be used for all cells, of type
`WildTypeCellMutationState` (i.e. 'healthy'):

```cpp
        MAKE_PTR(WildTypeCellMutationState, p_state);
        MAKE_PTR(StemCellProliferativeType, p_stem_type);

```
Now we loop over the nodes...

```cpp
        for (unsigned i=0; i<p_mesh->GetNumNodes(); i++)
        {
```

...then create a cell, giving it a `SimpleOxygenBasedCellCycleModel`{.cpp}.
The spatial dimension (1, 2 or 3) needs to be set on the cell-cycle model before it is passed to the cell.

```cpp
            SimpleOxygenBasedCellCycleModel* p_model = new SimpleOxygenBasedCellCycleModel;
            p_model->SetDimension(2);
            CellPtr p_cell(new Cell(p_state, p_model));
            p_cell->SetCellProliferativeType(p_stem_type);

```
We also alter the default cell-cycle times.

```cpp
            p_model->SetStemCellG1Duration(8.0);
            p_model->SetTransitCellG1Duration(8.0);

```
We now define a random birth time, chosen from [-T,0], where
T = t,,1,, + t,,2,,, where t,,1,, is a parameter representing the G,,1,, duration
of a 'stem' cell, and t,,2,, is the basic S+G,,2,,+M phases duration...

```cpp
            double birth_time = - RandomNumberGenerator::Instance()->ranf() *
                                 (  p_model->GetStemCellG1Duration()
                                  + p_model->GetSG2MDuration() );
```

...then we set the birth time and push the cell back into the vector
of cells.

```cpp
            p_cell->SetBirthTime(birth_time);
            cells.push_back(p_cell);
        }

```
Now that we have defined the cells, we can define the `CellPopulation`{.cpp}. We use a
`MeshBasedCellPopulation`{.cpp} since although the cell population is mesh-based, it does
not include any ghost nodes. The constructor takes in the mesh and the cells vector.

```cpp
        MeshBasedCellPopulation<2> cell_population(*p_mesh, cells);

```
Next we instantiate an instance of the PDE class which we defined above.
This will be passed into the `OffLatticeSimulationWithPdes`{.cpp} object. The
`CellwiseSourceEllipticPde`{.cpp} is a `PDE`{.cpp} class which inherits from
`AbstractLinearEllipticPde`{.cpp} and represents
the PDE ''u_xx'' + ''u_yy'' = ''k''(''x'',''y'') ''u'', where ''u''(''x'',''y'') denotes
the oxygen concentration at
position (''x'',''y'') and the function ''k''(''x'',''y'') specifies the rate of consumption by live cells
there. Here ''k''(''x'',''y'') takes the value -0.03 (the coefficient below) if
the cell located at (''x'',''y'') is a live cell, and zero if the cell has died due
to oxygen deprivation.

```cpp
        MAKE_PTR_ARGS(CellwiseSourceEllipticPde<2>, p_pde, (cell_population, -0.03));

```
We also create a constant-valued boundary condition to associate with the PDE.
This boundary condition object takes in a single argument in its constructor,
the value at the boundary. We also introduce a boolean to specify whether this value is the flux at the boundary
(a Neumann boundary condition) or the value of the state variable at the boundary
(a Dirichlet boundary condition) below.

```cpp
        MAKE_PTR_ARGS(ConstBoundaryCondition<2>, p_bc, (1.0));
        bool is_neumann_bc = false;

```
To pass the PDE to our simulator, it must first be encapsulated in a
cell-based PDE modifier object, together with the boundary condition for
the PDE. The latter is specified by the second and third arguments of the
constructor below: the second argument defines the value
of the boundary condition and the third argument defines whether it is of Neumann type
(true) or Dirichlet type (false). Thus, in our case, we are a specifying a constant-value
boundary condition. Note that we currently cannot impose more than one boundary
condition for each PDE (so that e.g. we cannot impose a zero-flux boundary condition
on some part of the boundary and a fixed-value boundary condition on the rest), although
the boundary condition itself can be made spatially varying or time-dependent.

The PDE is tagged to show that the quantity to be solved for (the quantity of interest in
the cells' data is "oxygen".

The `CellData`{.cpp} class, is used to stores the value of the current nutrient concentration for each cell.

```cpp
        MAKE_PTR_ARGS(EllipticGrowingDomainPdeModifier<2>, p_pde_modifier, (p_pde, p_bc, is_neumann_bc));
        p_pde_modifier->SetDependentVariableName("oxygen");

```
We are now in a position to construct an `OffLatticeSimulationWithPdes`{.cpp} object,
using the cell population. We then pass the PDE modifier object to the simulation.

```cpp
        OffLatticeSimulation<2> simulator(cell_population);
        simulator.AddSimulationModifier(p_pde_modifier);

```
We next set the output directory and end time.

```cpp
        simulator.SetOutputDirectory("SpheroidTutorial");
        simulator.SetEndTime(1.0);

```
We must now create one or more force laws, which determine the mechanics of
the cell population. As in the crypt simulation tutorial, we assume that a cell
experiences a force from each neighbour that can be represented as a linear overdamped
spring, so we use a `GeneralisedLinearSpringForce`{.cpp} object.
Note that we have called the method `SetCutOffLength`{.cpp} on the
`GeneralisedLinearSpringForce`{.cpp} before passing it to the simulator: this call
modifies the force law so that two neighbouring cells do not impose
a force on each other if they are located more than 3 units (=3 cell widths)
away from each other. This modification is necessary when no ghost nodes are used,
for example to avoid artificially large forces between cells that lie close together
on the spheroid boundary.

```cpp
        MAKE_PTR(GeneralisedLinearSpringForce<2>, p_linear_force);
        p_linear_force->SetCutOffLength(3);
        simulator.AddForce(p_linear_force);

```
We call `Solve()`{.cpp} on the simulator to run the simulation.

```cpp
        simulator.Solve();
    }
```

To visualize the results, open a new terminal, `cd`{.cpp} to the Chaste directory,
then `cd`{.cpp} to `anim`{.cpp}. Then do: `java Visualize2dCentreCells /tmp/$USER/testoutput/SpheroidTutorial/results_from_time_0`{.cpp}.

Or use Paraview, see [wiki:UserTutorials/VisualizingWithParaview] for details.

```cpp
};

```


# Code
The full code is given below


## File name `TestRunningTumourSpheroidSimulationsTutorial.hpp` 

```cpp
#include <cxxtest/TestSuite.h>
#include "CheckpointArchiveTypes.hpp"
#include "AbstractCellBasedTestSuite.hpp"
#include "HoneycombMeshGenerator.hpp"
#include "GeneralisedLinearSpringForce.hpp"
#include "RandomNumberGenerator.hpp"
#include "SmartPointers.hpp"
#include "SimpleOxygenBasedCellCycleModel.hpp"
#include "WildTypeCellMutationState.hpp"
#include "StemCellProliferativeType.hpp"
#include "CellwiseSourceEllipticPde.hpp"
#include "ConstBoundaryCondition.hpp"
#include "EllipticGrowingDomainPdeModifier.hpp"

#include "OffLatticeSimulation.hpp"
#include "PetscSetupAndFinalize.hpp"

class TestRunningTumourSpheroidSimulationsTutorial : public AbstractCellBasedTestSuite
{
public:
    void TestSpheroidTutorial()
    {
        EXIT_IF_PARALLEL;

        HoneycombMeshGenerator generator(10, 10, 0);
        boost::shared_ptr<MutableMesh<2,2> > p_mesh = generator.GetMesh();

        std::vector<CellPtr> cells;

        MAKE_PTR(WildTypeCellMutationState, p_state);
        MAKE_PTR(StemCellProliferativeType, p_stem_type);

        for (unsigned i=0; i<p_mesh->GetNumNodes(); i++)
        {
            SimpleOxygenBasedCellCycleModel* p_model = new SimpleOxygenBasedCellCycleModel;
            p_model->SetDimension(2);
            CellPtr p_cell(new Cell(p_state, p_model));
            p_cell->SetCellProliferativeType(p_stem_type);

            p_model->SetStemCellG1Duration(8.0);
            p_model->SetTransitCellG1Duration(8.0);

            double birth_time = - RandomNumberGenerator::Instance()->ranf() *
                                 (  p_model->GetStemCellG1Duration()
                                  + p_model->GetSG2MDuration() );
            p_cell->SetBirthTime(birth_time);
            cells.push_back(p_cell);
        }

        MeshBasedCellPopulation<2> cell_population(*p_mesh, cells);

        MAKE_PTR_ARGS(CellwiseSourceEllipticPde<2>, p_pde, (cell_population, -0.03));

        MAKE_PTR_ARGS(ConstBoundaryCondition<2>, p_bc, (1.0));
        bool is_neumann_bc = false;

        MAKE_PTR_ARGS(EllipticGrowingDomainPdeModifier<2>, p_pde_modifier, (p_pde, p_bc, is_neumann_bc));
        p_pde_modifier->SetDependentVariableName("oxygen");

        OffLatticeSimulation<2> simulator(cell_population);
        simulator.AddSimulationModifier(p_pde_modifier);

        simulator.SetOutputDirectory("SpheroidTutorial");
        simulator.SetEndTime(1.0);

        MAKE_PTR(GeneralisedLinearSpringForce<2>, p_linear_force);
        p_linear_force->SetCutOffLength(3);
        simulator.AddForce(p_linear_force);

        simulator.Solve();
    }
};

```

