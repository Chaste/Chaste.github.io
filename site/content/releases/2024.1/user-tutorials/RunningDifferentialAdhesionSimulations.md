---
title : "Running Differential Adhesion Simulations"
summary: "An example showing how to simulate cell sorting due to differential adhesion in a vertex-based model"
draft: false
images: []
toc: true
version: "2024.1"
version: "2024.1"
---
This tutorial is automatically generated from [TestRunningDifferentialAdhesionSimulationsTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/cell_based/test/tutorial/TestRunningDifferentialAdhesionSimulationsTutorial.hpp) at revision [1dfba06b4d82](https://github.com/Chaste/Chaste/commit/1dfba06b4d8265be2322817e6dfe1536071d9a0a). Note that the code is given in full at the bottom of the page.
## An example showing how to simulate cell sorting due to differential adhesion in a vertex-based model

### Introduction

In this tutorial we show how Chaste can be used to simulate a growing cell monolayer culture
comprising two distinct cell types, which exhibit differential adhesion. We encountered a
similar implementation in the second test in the TestRunningPottsBasedSimulationsTutorial,
which used a cellular Potts model of cell interactions; here we use a vertex-based model.

### The test

As in previous tutorials, we begin by including the necessary header files. We have
encountered these files already. Recall that often, either `CheckpointArchiveTypes.hpp`
or `CellBasedSimulationArchiver.hpp` must be included the first Chaste header.

```cpp
#include <cxxtest/TestSuite.h>
#include "CheckpointArchiveTypes.hpp"
#include "AbstractCellBasedTestSuite.hpp"
#include "HoneycombVertexMeshGenerator.hpp"
#include "CellsGenerator.hpp"
#include "FixedG1GenerationalCellCycleModel.hpp"
#include "CellLabel.hpp"
#include "DifferentiatedCellProliferativeType.hpp"
#include "VertexBasedCellPopulation.hpp"
#include "CellAgesWriter.hpp"
#include "CellVolumesWriter.hpp"
#include "CellMutationStatesCountWriter.hpp"
#include "CellProliferativePhasesWriter.hpp"
#include "CellProliferativeTypesCountWriter.hpp"
#include "CellProliferativePhasesCountWriter.hpp"
#include "OffLatticeSimulation.hpp"
#include "SmartPointers.hpp"
#include "FakePetscSetup.hpp"
```

The next header file defines a force law for describing the mechanical interactions
between neighbouring cells in the cell population, subject to each vertex. This force
law is a subclass of `NagaiHondaForce`, which we encountered in the `TestRunningVertexBasedSimulationsTutorial`,
that allows for different adhesion energy parameter values depending on the types of
interacting cells.

```cpp
#include "NagaiHondaDifferentialAdhesionForce.hpp"
```

Having included all the necessary header files, we proceed by defining the test class.

```cpp
class TestRunningDifferentialAdhesionSimulationsTutorial : public AbstractCellBasedTestSuite
{
public:
```

In this test, we demonstrate how to simulate a heterotypic monolayer that incorporates
differential adhesion, using a vertex-based approach. This may be compared with the
second test in the TestRunningPottsBasedSimulationsTutorial, which implements a similar
simulation using a cellular Potts model.

```cpp
    void TestVertexBasedDifferentialAdhesionSimulation()
    {
```

First we create a regular vertex mesh. Here we choose to set the value of the cell rearrangement threshold.

```cpp
        HoneycombVertexMeshGenerator generator(5, 5);
        boost::shared_ptr<MutableVertexMesh<2,2> > p_mesh = generator.GetMesh();
        p_mesh->SetCellRearrangementThreshold(0.1);
```

We then create some cells using the helper class `CellsGenerator`. Note that in this simulation
the cells are all differentiated, and thus no cell division occurs; if we wished, we could modify
the three lines below in a straightforward manner to incorporate cell proliferation and investigate
the effect of this on the cell sorting process.

```cpp
        std::vector<CellPtr> cells;
        MAKE_PTR(DifferentiatedCellProliferativeType, p_diff_type);
        CellsGenerator<FixedG1GenerationalCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasic(cells, p_mesh->GetNumElements(), std::vector<unsigned>(), p_diff_type);
```

Using the vertex mesh and cells, we create a cell-based population object, and specify which results to
output to file.

```cpp
        VertexBasedCellPopulation<2> cell_population(*p_mesh, cells);
        cell_population.AddCellPopulationCountWriter<CellMutationStatesCountWriter>();
        cell_population.AddCellPopulationCountWriter<CellProliferativeTypesCountWriter>();
        cell_population.AddCellPopulationCountWriter<CellProliferativePhasesCountWriter>();
        cell_population.AddCellWriter<CellProliferativePhasesWriter>();
        cell_population.AddCellWriter<CellAgesWriter>();
        cell_population.AddCellWriter<CellVolumesWriter>();
```

We randomly label some cells using the cell property `CellLabel`. We begin by creating a shared pointer to
this cell property using the helper singleton `CellPropertyRegistry`. We then loop over the cells and label
each cell independently with probability 0.5. Note that since the cells have been passed to the
`VertexBasedCellPopulation` object, the vector `cells` above is now empty, so we must use the
`Iterator` to loop over cells.

```cpp
         boost::shared_ptr<AbstractCellProperty> p_label(CellPropertyRegistry::Instance()->Get<CellLabel>());
        for (AbstractCellPopulation<2>::Iterator cell_iter = cell_population.Begin();
             cell_iter != cell_population.End();
             ++cell_iter)
        {
            if (RandomNumberGenerator::Instance()->ranf() < 0.5)
            {
                cell_iter->AddCellProperty(p_label);
            }
        }
```

We are now in a position to create and configure the cell-based simulation object.
We can make the simulation run for longer to see more cell sorting by increasing the end time.

```cpp
        OffLatticeSimulation<2> simulator(cell_population);
        simulator.SetOutputDirectory("TestVertexBasedDifferentialAdhesionSimulation");
        simulator.SetSamplingTimestepMultiple(10);
        simulator.SetEndTime(1.0);
```

Next we create the differential adhesion force law. This builds upon the model of Nagai, Honda and co-workers
encounted in the TestRunningVertexBasedSimulationsTutorial by allowing different values of the adhesion
energy parameters depending on the types of two neighbouring cells. Here we interpret the 'type' of a cell
as whether or not it has the cell property `CellLabel`; it would be straightforward to create a similar
force law that took account of a cell's mutation state, for example. Having created the force law, we set the
values of the parameters. If the adhesion energy for two neighbouring homotypic cells is less than that of two
heterotypic cells, then we may expect cell sorting to occur, in which the cells of each type will tend to locally
aggregate over time.

```cpp
        MAKE_PTR(NagaiHondaDifferentialAdhesionForce<2>, p_force);
        p_force->SetNagaiHondaDeformationEnergyParameter(55.0);
        p_force->SetNagaiHondaMembraneSurfaceEnergyParameter(0.0);
        p_force->SetNagaiHondaCellCellAdhesionEnergyParameter(1.0);
        p_force->SetNagaiHondaLabelledCellCellAdhesionEnergyParameter(6.0);
        p_force->SetNagaiHondaLabelledCellLabelledCellAdhesionEnergyParameter(3.0);
        p_force->SetNagaiHondaCellBoundaryAdhesionEnergyParameter(12.0);
        p_force->SetNagaiHondaLabelledCellBoundaryAdhesionEnergyParameter(40.0);
        simulator.AddForce(p_force);
```

Finally, we run the simulation.

```cpp
        simulator.Solve();
    }
};
```

To visualize the results, use Paraview. See the [Visualizing With Paraview](/docs/user-tutorials/visualizingwithparaview/) tutorial for more information.

Load the file `/tmp/$USER/testoutput/TestVertexBasedDifferentialAdhesionSimulation/results_from_time_0/results.pvd`.

## Full code

```cpp
#include <cxxtest/TestSuite.h>
#include "CheckpointArchiveTypes.hpp"
#include "AbstractCellBasedTestSuite.hpp"
#include "HoneycombVertexMeshGenerator.hpp"
#include "CellsGenerator.hpp"
#include "FixedG1GenerationalCellCycleModel.hpp"
#include "CellLabel.hpp"
#include "DifferentiatedCellProliferativeType.hpp"
#include "VertexBasedCellPopulation.hpp"
#include "CellAgesWriter.hpp"
#include "CellVolumesWriter.hpp"
#include "CellMutationStatesCountWriter.hpp"
#include "CellProliferativePhasesWriter.hpp"
#include "CellProliferativeTypesCountWriter.hpp"
#include "CellProliferativePhasesCountWriter.hpp"
#include "OffLatticeSimulation.hpp"
#include "SmartPointers.hpp"
#include "FakePetscSetup.hpp"

#include "NagaiHondaDifferentialAdhesionForce.hpp"

class TestRunningDifferentialAdhesionSimulationsTutorial : public AbstractCellBasedTestSuite
{
public:

    void TestVertexBasedDifferentialAdhesionSimulation()
    {
        HoneycombVertexMeshGenerator generator(5, 5);
        boost::shared_ptr<MutableVertexMesh<2,2> > p_mesh = generator.GetMesh();
        p_mesh->SetCellRearrangementThreshold(0.1);

        std::vector<CellPtr> cells;
        MAKE_PTR(DifferentiatedCellProliferativeType, p_diff_type);
        CellsGenerator<FixedG1GenerationalCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasic(cells, p_mesh->GetNumElements(), std::vector<unsigned>(), p_diff_type);

        VertexBasedCellPopulation<2> cell_population(*p_mesh, cells);
        cell_population.AddCellPopulationCountWriter<CellMutationStatesCountWriter>();
        cell_population.AddCellPopulationCountWriter<CellProliferativeTypesCountWriter>();
        cell_population.AddCellPopulationCountWriter<CellProliferativePhasesCountWriter>();
        cell_population.AddCellWriter<CellProliferativePhasesWriter>();
        cell_population.AddCellWriter<CellAgesWriter>();
        cell_population.AddCellWriter<CellVolumesWriter>();

         boost::shared_ptr<AbstractCellProperty> p_label(CellPropertyRegistry::Instance()->Get<CellLabel>());
        for (AbstractCellPopulation<2>::Iterator cell_iter = cell_population.Begin();
             cell_iter != cell_population.End();
             ++cell_iter)
        {
            if (RandomNumberGenerator::Instance()->ranf() < 0.5)
            {
                cell_iter->AddCellProperty(p_label);
            }
        }

        OffLatticeSimulation<2> simulator(cell_population);
        simulator.SetOutputDirectory("TestVertexBasedDifferentialAdhesionSimulation");
        simulator.SetSamplingTimestepMultiple(10);
        simulator.SetEndTime(1.0);

        MAKE_PTR(NagaiHondaDifferentialAdhesionForce<2>, p_force);
        p_force->SetNagaiHondaDeformationEnergyParameter(55.0);
        p_force->SetNagaiHondaMembraneSurfaceEnergyParameter(0.0);
        p_force->SetNagaiHondaCellCellAdhesionEnergyParameter(1.0);
        p_force->SetNagaiHondaLabelledCellCellAdhesionEnergyParameter(6.0);
        p_force->SetNagaiHondaLabelledCellLabelledCellAdhesionEnergyParameter(3.0);
        p_force->SetNagaiHondaCellBoundaryAdhesionEnergyParameter(12.0);
        p_force->SetNagaiHondaLabelledCellBoundaryAdhesionEnergyParameter(40.0);
        simulator.AddForce(p_force);

        simulator.Solve();
    }
};
```
