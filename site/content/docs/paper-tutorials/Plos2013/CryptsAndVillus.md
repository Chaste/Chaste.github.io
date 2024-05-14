---
title: "Cell-based simulation: multiple crypts and a villus"
draft: false
layout: "single"
---

This tutorial was generated from the file [TestCryptsAndVillusLiteratePaper.hpp](https://github.com/Chaste/project_Plos2013/blob/5b522e0ce55ac81ce8728f858b10464e9d7cfb98/test/TestCryptsAndVillusLiteratePaper.hpp).
Note that the code is given in full at the bottom of the page.

{{< img src="/fig/paper-tutorials/combined.png" alt="Crypts and villus" h="200px" >}}

On this wiki page we describe in detail the code that is used to run this example from the paper.

The simulation is a node-based off-lattice simulation. In other words, cells are represented by points
in space (nodes) and are allowed to move without being confined to certain lattice sites.

This example is somewhat unusual, in that we enforce a boundary condition that limits the cells'
movement to a 2D surface in 3D space.

We show use of `CellKiller`s - both random and acting on a plane at the top of the villus.

We also show the use of lineage tracking, and cell-signalling leading to Delta-Notch patterning.

This example uses some source files that can be found in the [`Plos2013/src`](https://github.com/Chaste/project_Plos2013/tree/5b522e0ce55ac81ce8728f858b10464e9d7cfb98/src) folder.

Remember to run with `build=GccOptNative` for speed.
e.g.

```bash
scons build=GccOptNative test_suite=projects/project_Plos2013/test/TestCryptsAndVillusLiteratePaper.hpp
```

The easiest way to visualize this simulation is with Paraview, as follows. After opening Paraview,
load the file results.pvd, then click "Apply" in the object inspector panel. As this simulation
uses a `NodeBasedCellPopulation`, you must use glyphs to visualize cells: click the button marked
"Glyph" in the toolbar of common filters; specify cells to be displayed as spheres; then click "Apply".

### Code overview

The first thing to do is to include the necessary header files.


```cpp
#include <cxxtest/TestSuite.h>

// Must be included before any other cell_based headers
#include "CellBasedSimulationArchiver.hpp"

#include "OffLatticeSimulation.hpp"
#include "RandomCellKiller.hpp"
#include "SloughingCellKiller.hpp"
#include "AbstractCellBasedTestSuite.hpp"
#include "DeltaNotchSrnModel.hpp"
#include "SimpleWntCellCycleModel.hpp"
#include "DeltaNotchTrackingModifier.hpp"
#include "GeneralisedLinearSpringForce.hpp"
#include "CellProliferativeTypesCountWriter.hpp"
#include "CellBasedEventHandler.hpp"
#include "CellMutationStatesWriter.hpp"
#include "CellAncestorWriter.hpp"
#include "PlaneBasedCellKiller.hpp"

// Header files included in this project.
#include "MultipleCryptGeometryBoundaryCondition.hpp"

// Should usually be called last.
#include "PetscSetupAndFinalize.hpp"

class TestCryptsAndVillusLiteratePaper : public AbstractCellBasedTestSuite
{
private:
```


These methods are `cxx-test` instructions running before and after each test below.
They are just here to report the time the test took.


```cpp
    void setUp()
    {
        AbstractCellBasedTestSuite::setUp();
        CellBasedEventHandler::Reset();
    }
    void tearDown()
    {
        AbstractCellBasedTestSuite::tearDown();

        CellBasedEventHandler::Headings();
        CellBasedEventHandler::Report();
    }

public:
```

The following code is the `test` itself, we use the `scons` / `cxx-test` framework to run simulations, as it
provides a handy way to do all the necessary linking and library building.


```cpp
    void Test3dCrypt() throw (Exception)
    {
        EXIT_IF_PARALLEL;
```

First we set up some numbers that will define the crypt and villus geometry

```cpp
        double crypt_length = 4.0;
        double crypt_radius = 1.0;
        double villus_length = 10.0;
        double villus_radius = 2.0;
        double domain_width = 12.0;
        double domain_height = 2.0*crypt_radius+crypt_length+villus_length+2.0*villus_radius;
```

We then create a couple of cells at the base of each crypt.
(we put two cells in each crypt to set off delta-notch patterning)

```cpp
        std::vector<Node<3>*> nodes;
        nodes.push_back(new Node<3>(0u,  false,  0.5*domain_width, 0.0, 0.0));
        nodes.push_back(new Node<3>(1u,  false,  0.5*domain_width+0.1, 0.1, 0.0));
        nodes.push_back(new Node<3>(2u,  false,  0.0, 0.5*domain_width, 0.0));
        nodes.push_back(new Node<3>(3u,  false,  0.1, 0.5*domain_width+0.1, 0.0));
        nodes.push_back(new Node<3>(3u,  false,  0.5*domain_width, domain_width, 0.0));
        nodes.push_back(new Node<3>(5u,  false,  0.5*domain_width+0.1, domain_width-0.1, 0.0));
        nodes.push_back(new Node<3>(6u,  false,  domain_width, 0.5*domain_width, 0.0));
        nodes.push_back(new Node<3>(7u,  false,  domain_width-0.1, 0.5*domain_width+0.1, 0.0));
```

We then convert this list of nodes to a `NodesOnlyMesh`,
which doesn't do very much apart from keep track of the nodes.


```cpp
        NodesOnlyMesh<3> mesh;
        mesh.ConstructNodesWithoutMesh(nodes, 1.5);
```

Next we have to create the cells that will be associated with these nodes.
So we make an empty vector in which to store the cells and then loop over
each node, adding cells as we go.


```cpp
        std::vector<CellPtr> cells;
        MAKE_PTR(TransitCellProliferativeType, p_transit_type);
        MAKE_PTR(WildTypeCellMutationState, p_state);
        for (unsigned i=0; i<mesh.GetNumNodes(); i++)
        {
```


This cell cycle model carries a Delta-Notch signalling model,
and also a simple rule about division based on extracellular Wnt concentration.


```cpp
            SimpleWntCellCycleModel* p_cc_model = new SimpleWntCellCycleModel();
            p_cc_model->SetDimension(3);

            DeltaNotchSrnModel* p_srn_model = new DeltaNotchSrnModel();
```

We choose to initialise the Delta and Notch concentrations to random levels in each cell

```cpp
            std::vector<double> initial_conditions;
            initial_conditions.push_back(RandomNumberGenerator::Instance()->ranf());
            initial_conditions.push_back(RandomNumberGenerator::Instance()->ranf());
            p_srn_model->SetInitialConditions(initial_conditions);
```

We then create a cell with a mutation state (Wild Type in this case), a cell cycle model and an srn model

```cpp
            CellPtr p_cell(new Cell(p_state, p_cc_model, p_srn_model));
            double birth_time = 0.0;
            p_cell->SetBirthTime(birth_time);
            p_cell->SetCellProliferativeType(p_transit_type);
            cells.push_back(p_cell);
        }
```

We now create a cell population, which keeps track of a mesh and cells and the association between them.
In this case we need a `NodeBasedCellPopulation` in three dimensions.


```cpp
        NodeBasedCellPopulation<3> crypt(mesh, cells);
        crypt.SetCellAncestorsToLocationIndices();
```

We limit the absolute movement that cells can make to cause error messages if numerics become unstable

```cpp
        crypt.SetAbsoluteMovementThreshold(10);
```

We then instruct the cell population to output some useful information for plotting in VTK format in e.g. paraview

```cpp
        crypt.AddCellPopulationCountWriter<CellProliferativeTypesCountWriter>();
        crypt.AddCellWriter<CellMutationStatesWriter>();
        crypt.AddCellWriter<CellAncestorWriter>();
```

We now set up our cell-based simulation class.


```cpp
        OffLatticeSimulation<3> simulator(crypt);
        simulator.SetOutputDirectory("Plos2013_MultipleCrypt");
        simulator.SetDt(1.0/120.0);
```

We limit the output to every 120 time steps (1 hour) to reduce output file sizes

```cpp
        simulator.SetSamplingTimestepMultiple(120);
```

We now create a modifier, which updates the delta and notch levels on each timestep.


```cpp
        MAKE_PTR(DeltaNotchTrackingModifier<3>, p_modifier);
        simulator.AddSimulationModifier(p_modifier);
```

We now create a force law and pass it to the simulation
We use linear springs between cells up to a maximum of 1.5 ('relaxed' cell diameters) apart, and add this to the simulation class.


```cpp
        MAKE_PTR(GeneralisedLinearSpringForce<3>, p_linear_force);
        p_linear_force->SetMeinekeSpringStiffness(30.0); // default is 15.0;
        p_linear_force->SetCutOffLength(1.5);
        simulator.AddForce(p_linear_force);
```

The most complex part of this problem definition is that of the boundary condition that limits
cell locations to a 2D surface in 3D space. This has been defined in a separate class
`MultipleCryptGeometryBoundaryCondition` which can be found in this project's `src` folder.


```cpp
        MAKE_PTR_ARGS(MultipleCryptGeometryBoundaryCondition,
                      p_boundary_condition,
                      (&crypt, crypt_radius, crypt_length, villus_radius, villus_length, domain_width));
        simulator.AddCellPopulationBoundaryCondition(p_boundary_condition);

        // Main sink of cells is at the top of the villus - remove any cells reaching here
        MAKE_PTR_ARGS(PlaneBasedCellKiller<3>,
                      p_cell_killer_1,
                      (&crypt, (domain_height-0.25)*unit_vector<double>(3,2), unit_vector<double>(3,2)));
        simulator.AddCellKiller(p_cell_killer_1);
```

We now create an instance of a Wnt concentration.

```cpp
        WntConcentration<3>::Instance()->SetType(LINEAR);
        WntConcentration<3>::Instance()->SetCellPopulation(crypt);
        WntConcentration<3>::Instance()->SetCryptLength(crypt_length+2.0*crypt_radius);
```

We then set an end time and run the simulation

```cpp
        simulator.SetEndTime(250.0);
        simulator.Solve(); // to 250 hours
```

These methods provide some reports of how much computation time is spent in which parts of the code.
These would be done automatically at the beginning and end of the test, but we are interrupting mid-way through here.


```cpp
        CellBasedEventHandler::Headings();
        CellBasedEventHandler::Report();
        CellBasedEventHandler::Reset();
```

Having run the simulation to a roughly steady-state, and filled the villus with cells,
we now add a random cell killer to represent random death in the epithelial layer.


```cpp
        MAKE_PTR_ARGS(RandomCellKiller<3>, p_cell_killer_2,(&crypt, 0.005)); // prob of death in an hour
        simulator.AddCellKiller(p_cell_killer_2);
```

We also label each cell according to its current node index so we can track clonal spread

```cpp
        simulator.rGetCellPopulation().SetCellAncestorsToLocationIndices();
```

We now solve for a further 750 hours, up to a total of 1000 hours

```cpp
        simulator.SetEndTime(1000.0);
        simulator.Solve(); // to 1000 hours

    }
};
```



## Code
The full code is given below


### File name `TestCryptsAndVillusLiteratePaper.hpp`


```cpp
#include <cxxtest/TestSuite.h>

// Must be included before any other cell_based headers
#include "CellBasedSimulationArchiver.hpp"

#include "OffLatticeSimulation.hpp"
#include "RandomCellKiller.hpp"
#include "SloughingCellKiller.hpp"
#include "AbstractCellBasedTestSuite.hpp"
#include "DeltaNotchSrnModel.hpp"
#include "SimpleWntCellCycleModel.hpp"
#include "DeltaNotchTrackingModifier.hpp"
#include "GeneralisedLinearSpringForce.hpp"
#include "CellProliferativeTypesCountWriter.hpp"
#include "CellBasedEventHandler.hpp"
#include "CellMutationStatesWriter.hpp"
#include "CellAncestorWriter.hpp"
#include "PlaneBasedCellKiller.hpp"

// Header files included in this project.
#include "MultipleCryptGeometryBoundaryCondition.hpp"

// Should usually be called last.
#include "PetscSetupAndFinalize.hpp"

class TestCryptsAndVillusLiteratePaper : public AbstractCellBasedTestSuite
{
private:
    void setUp()
    {
        AbstractCellBasedTestSuite::setUp();
        CellBasedEventHandler::Reset();
    }
    void tearDown()
    {
        AbstractCellBasedTestSuite::tearDown();

        CellBasedEventHandler::Headings();
        CellBasedEventHandler::Report();
    }

public:

    void Test3dCrypt() throw (Exception)
    {
        EXIT_IF_PARALLEL;

        double crypt_length = 4.0;
        double crypt_radius = 1.0;
        double villus_length = 10.0;
        double villus_radius = 2.0;
        double domain_width = 12.0;
        double domain_height = 2.0*crypt_radius+crypt_length+villus_length+2.0*villus_radius;

        std::vector<Node<3>*> nodes;
        nodes.push_back(new Node<3>(0u,  false,  0.5*domain_width, 0.0, 0.0));
        nodes.push_back(new Node<3>(1u,  false,  0.5*domain_width+0.1, 0.1, 0.0));
        nodes.push_back(new Node<3>(2u,  false,  0.0, 0.5*domain_width, 0.0));
        nodes.push_back(new Node<3>(3u,  false,  0.1, 0.5*domain_width+0.1, 0.0));
        nodes.push_back(new Node<3>(3u,  false,  0.5*domain_width, domain_width, 0.0));
        nodes.push_back(new Node<3>(5u,  false,  0.5*domain_width+0.1, domain_width-0.1, 0.0));
        nodes.push_back(new Node<3>(6u,  false,  domain_width, 0.5*domain_width, 0.0));
        nodes.push_back(new Node<3>(7u,  false,  domain_width-0.1, 0.5*domain_width+0.1, 0.0));

        NodesOnlyMesh<3> mesh;
        mesh.ConstructNodesWithoutMesh(nodes, 1.5);

        std::vector<CellPtr> cells;
        MAKE_PTR(TransitCellProliferativeType, p_transit_type);
        MAKE_PTR(WildTypeCellMutationState, p_state);
        for (unsigned i=0; i<mesh.GetNumNodes(); i++)
        {
            SimpleWntCellCycleModel* p_cc_model = new SimpleWntCellCycleModel();
            p_cc_model->SetDimension(3);

            DeltaNotchSrnModel* p_srn_model = new DeltaNotchSrnModel();

            std::vector<double> initial_conditions;
            initial_conditions.push_back(RandomNumberGenerator::Instance()->ranf());
            initial_conditions.push_back(RandomNumberGenerator::Instance()->ranf());
            p_srn_model->SetInitialConditions(initial_conditions);

            CellPtr p_cell(new Cell(p_state, p_cc_model, p_srn_model));
            double birth_time = 0.0;
            p_cell->SetBirthTime(birth_time);
            p_cell->SetCellProliferativeType(p_transit_type);
            cells.push_back(p_cell);
        }

        NodeBasedCellPopulation<3> crypt(mesh, cells);
        crypt.SetCellAncestorsToLocationIndices();

        crypt.SetAbsoluteMovementThreshold(10);

        crypt.AddCellPopulationCountWriter<CellProliferativeTypesCountWriter>();
        crypt.AddCellWriter<CellMutationStatesWriter>();
        crypt.AddCellWriter<CellAncestorWriter>();

        OffLatticeSimulation<3> simulator(crypt);
        simulator.SetOutputDirectory("Plos2013_MultipleCrypt");
        simulator.SetDt(1.0/120.0);
        simulator.SetSamplingTimestepMultiple(120);

        MAKE_PTR(DeltaNotchTrackingModifier<3>, p_modifier);
        simulator.AddSimulationModifier(p_modifier);

        MAKE_PTR(GeneralisedLinearSpringForce<3>, p_linear_force);
        p_linear_force->SetMeinekeSpringStiffness(30.0); // default is 15.0;
        p_linear_force->SetCutOffLength(1.5);
        simulator.AddForce(p_linear_force);

        MAKE_PTR_ARGS(MultipleCryptGeometryBoundaryCondition,
                      p_boundary_condition,
                      (&crypt, crypt_radius, crypt_length, villus_radius, villus_length, domain_width));
        simulator.AddCellPopulationBoundaryCondition(p_boundary_condition);

        // Main sink of cells is at the top of the villus - remove any cells reaching here
        MAKE_PTR_ARGS(PlaneBasedCellKiller<3>,
                      p_cell_killer_1,
                      (&crypt, (domain_height-0.25)*unit_vector<double>(3,2), unit_vector<double>(3,2)));
        simulator.AddCellKiller(p_cell_killer_1);

        WntConcentration<3>::Instance()->SetType(LINEAR);
        WntConcentration<3>::Instance()->SetCellPopulation(crypt);
        WntConcentration<3>::Instance()->SetCryptLength(crypt_length+2.0*crypt_radius);

        simulator.SetEndTime(250.0);
        simulator.Solve(); // to 250 hours

        CellBasedEventHandler::Headings();
        CellBasedEventHandler::Report();
        CellBasedEventHandler::Reset();

        MAKE_PTR_ARGS(RandomCellKiller<3>, p_cell_killer_2,(&crypt, 0.005)); // prob of death in an hour
        simulator.AddCellKiller(p_cell_killer_2);

        simulator.rGetCellPopulation().SetCellAncestorsToLocationIndices();

        simulator.SetEndTime(1000.0);
        simulator.Solve(); // to 1000 hours

    }
};
```


