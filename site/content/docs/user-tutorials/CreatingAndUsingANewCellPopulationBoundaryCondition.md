---
title : "Creating And Using A New Cell Population Boundary Condition"
summary: "An example showing how to create and use a new cell population boundary condition"
draft: false
images: []
toc: true
---
This tutorial is automatically generated from [TestCreatingAndUsingANewCellPopulationBoundaryConditionTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/cell_based/test/tutorial/TestCreatingAndUsingANewCellPopulationBoundaryConditionTutorial.hpp) at revision [96e6e662bf78](https://github.com/Chaste/Chaste/commit/96e6e662bf780f36e39eabcae9f3d4d843677a5b). Note that the code is given in full at the bottom of the page.
## An example showing how to create and use a new cell population boundary condition

### Introduction

In this tutorial we show how to create a new cell population boundary condition
class to specify a fixed domain within which cells are constrained to lie, and
how to use this in a cell-based simulation.

### 1. Including header files

As in previous cell-based Chaste tutorials, we begin by including the necessary header files.

```cpp
#include <cxxtest/TestSuite.h>
#include "CheckpointArchiveTypes.hpp"
#include "AbstractCellBasedTestSuite.hpp"

```

The next header defines a base class for cell population boundary conditions,
from which the new class will inherit.
```cpp
#include "AbstractCellPopulationBoundaryCondition.hpp"
```

The remaining header files define classes that will be used in the cell-based
simulation test. You will have encountered some these files already in previous
cell-based Chaste tutorials.
```cpp
#include "OffLatticeSimulation.hpp"
#include "HoneycombMeshGenerator.hpp"
#include "HoneycombVertexMeshGenerator.hpp"
#include "VertexBasedCellPopulation.hpp"
#include "CellsGenerator.hpp"
#include "FixedG1GenerationalCellCycleModel.hpp"
#include "GeneralisedLinearSpringForce.hpp"
#include "SmartPointers.hpp"
#include "FakePetscSetup.hpp"

```

### Defining the cell population boundary condition class

As an example, let us consider a boundary condition for a two-dimensional cell-based
simulation, in which all cells are constrained to lie within the domain given in
Cartesian coordinates by 0 <= y <= 5. To implement this we define a cell population
boundary condition class, `MyBoundaryCondition`, which inherits from
`AbstractCellPopulationBoundaryCondition` and overrides the methods
`ImposeBoundaryCondition()`, `VerifyBoundaryCondition()` and
`OutputCellPopulationBoundaryConditionParameters()`.

```cpp
class MyBoundaryCondition : public AbstractCellPopulationBoundaryCondition<2>
{
private:

    friend class boost::serialization::access;
    template<class Archive>
    void serialize(Archive & archive, const unsigned int version)
    {
        archive & boost::serialization::base_object<AbstractCellPopulationBoundaryCondition<2> >(*this);
    }

public:
```

The first public method is a default constructor, which calls the base
constructor. There is a single input argument, a pointer to a cell population.

```cpp
    MyBoundaryCondition(AbstractCellPopulation<2>* pCellPopulation)
        : AbstractCellPopulationBoundaryCondition<2>(pCellPopulation)
    {
    }

```

The second public method overrides `ImposeBoundaryCondition()`.
This method is called during the `Solve()` method in `OffLatticeSimulation`
at the end of each timestep, just after the position of each node
in the cell population has been updated according to its equation of motion.
The method iterates over all cells in the population, and moves any cell whose
centre has y coordinate less than 0 or greater than 5 back into the domain.

Implicit in this method is the assumption that, when a node hits the
boundary of the domain, it does so inelastically. This means, for example,
that a node hitting the boundary at y=0 has its location moved to y=0. A
more physically realistic modelling assumption might be to assume that
momentum is conserved in the collision.

Also implicit in this method is the assumption that we are using a cell-centre
based population. If we were using a vertex-based population then each node
would correspond not to a cell centre but to a vertex.

```cpp
    void ImposeBoundaryCondition(const std::map<Node<2>*, c_vector<double, 2> >& rOldLocations)
    {
        for (AbstractCellPopulation<2>::Iterator cell_iter = this->mpCellPopulation->Begin();
             cell_iter != this->mpCellPopulation->End();
             ++cell_iter)
        {
            unsigned node_index = this->mpCellPopulation->GetLocationIndexUsingCell(*cell_iter);
            Node<2>* p_node = this->mpCellPopulation->GetNode(node_index);
            double y_coordinate = p_node->rGetLocation()[1];

            if (y_coordinate > 5.0)
            {
                p_node->rGetModifiableLocation()[1] = 5.0;
            }
            else if (y_coordinate < 0.0)
            {
                p_node->rGetModifiableLocation()[1] = 0.0;
            }
        }
    }

```

The third public method overrides `VerifyBoundaryCondition()`.
This method is called during the `Solve()` method in `OffLatticeSimulation`
at the end of each timestep, just after `ImposeBoundaryCondition()`, and checks
that each cell in the population now satisfies `MyBoundaryCondition`.

```cpp
    bool VerifyBoundaryCondition()
    {
        bool condition_satisfied = true;

        for (AbstractCellPopulation<2>::Iterator cell_iter = this->mpCellPopulation->Begin();
             cell_iter != this->mpCellPopulation->End();
             ++cell_iter)
        {
            c_vector<double, 2> cell_location = this->mpCellPopulation->GetLocationOfCellCentre(*cell_iter);
            double y_coordinate = cell_location(1);

            if ((y_coordinate < 0.0) || (y_coordinate > 5.0))
            {
                condition_satisfied = false;
                break;
            }
        }
        return condition_satisfied;
    }

```

Just as we encountered in [wiki:UserTutorials/CreatingAndUsingANewCellKiller], here we must override
a method that outputs any member variables to a specified results file `rParamsFile`.
In our case, there are no parameters, so we simply call the method on the base class.
Nonetheless, we still need to override the method, since it is pure virtual in the base
class.

```cpp
    void OutputCellPopulationBoundaryConditionParameters(out_stream& rParamsFile)
    {
        AbstractCellPopulationBoundaryCondition<2>::OutputCellPopulationBoundaryConditionParameters(rParamsFile);
    }
};

```

As mentioned in previous cell-based Chaste tutorials, we need to include the next block
of code to be able to archive the cell population boundary condition object in a cell-based
simulation, and to obtain a unique identifier for our new boundary condition for writing
results to file.

```cpp
#include "SerializationExportWrapper.hpp"
CHASTE_CLASS_EXPORT(MyBoundaryCondition)
#include "SerializationExportWrapperForCpp.hpp"
CHASTE_CLASS_EXPORT(MyBoundaryCondition)

namespace boost
{
    namespace serialization
    {
        template<class Archive>
        inline void save_construct_data(
            Archive & ar, const MyBoundaryCondition * t, const unsigned int file_version)
        {
            const AbstractCellPopulation<2>* const p_cell_population = t->GetCellPopulation();
            ar << p_cell_population;
        }

        template<class Archive>
        inline void load_construct_data(
            Archive & ar, MyBoundaryCondition * t, const unsigned int file_version)
        {
            AbstractCellPopulation<2>* p_cell_population;
            ar >> p_cell_population;

            ::new(t)MyBoundaryCondition(p_cell_population);
        }
    }
}

```

This completes the code for `MyBoundaryCondition`. Note that usually this code
would be separated out into a separate declaration in a .hpp file and definition
in a .cpp file.

#### The Tests

We now define the test class, which inherits from `AbstractCellBasedTestSuite`.

```cpp
class TestCreatingAndUsingANewCellPopulationBoundaryConditionTutorial : public AbstractCellBasedTestSuite
{
public:

```

### Testing the cell population boundary condition

We now test that our new cell population boundary condition is implemented correctly.

```cpp
    void TestMyBoundaryCondition()
    {
```

We first create a `MeshBasedCellPopulation` using the helper
classes `HoneycombMeshGenerator` and `CellsGenerator`,
as in previous cell-based Chaste tutorials.

```cpp
        HoneycombMeshGenerator generator(7, 7);
        boost::shared_ptr<MutableMesh<2,2> > p_mesh = generator.GetMesh();

        std::vector<CellPtr> cells;
        CellsGenerator<FixedG1GenerationalCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasic(cells, p_mesh->GetNumNodes());

        MeshBasedCellPopulation<2> cell_population(*p_mesh, cells);

```

We now use the cell population to construct a cell population boundary condition object.

```cpp
        MyBoundaryCondition bc(&cell_population);

```

We start by verifying that some cells do not satisfy the boundary condition:

```cpp
        bool population_satisfies_bc = bc.VerifyBoundaryCondition();
        TS_ASSERT_EQUALS(population_satisfies_bc, false);

        std::map<Node<2>*, c_vector<double, 2> > old_node_locations;
        for (AbstractMesh<2,2>::NodeIterator node_iter = p_mesh->GetNodeIteratorBegin();
                node_iter != p_mesh->GetNodeIteratorEnd();
                ++node_iter)
        {
            old_node_locations[&(*node_iter)] = node_iter->rGetLocation();
        }

```

To test that we have implemented the cell population boundary condition correctly,
we call the overridden method `ImposeBoundaryCondition()`...

```cpp
        bc.ImposeBoundaryCondition(old_node_locations);

```

... and check that the cell population does indeed now satisfy the boundary condition:

```cpp
        population_satisfies_bc = bc.VerifyBoundaryCondition();
        TS_ASSERT_EQUALS(population_satisfies_bc, true);

```

The last block of code provides an archiving test for the cell population boundary
condition, in a similar way to previous cell-based Chaste tutorials:

```cpp
        OutputFileHandler handler("archive", false);
        std::string archive_filename = handler.GetOutputDirectoryFullPath() + "my_bc.arch";
        {
            std::ofstream ofs(archive_filename.c_str());
            boost::archive::text_oarchive output_arch(ofs);

            AbstractCellPopulationBoundaryCondition<2>* const p_bc = new MyBoundaryCondition(NULL);
            output_arch << p_bc;
            delete p_bc;
        }
        {
            std::ifstream ifs(archive_filename.c_str(), std::ios::binary);
            boost::archive::text_iarchive input_arch(ifs);

            AbstractCellPopulationBoundaryCondition<2>* p_bc;
            input_arch >> p_bc;

            delete p_bc;
        }
    }

```

### Using the boundary condition in a cell-based simulation

We now provide a test demonstrating how `MyBoundaryCondition` can be used
in a cell-based simulation.

```cpp
    void TestOffLatticeSimulationWithMyBoundaryCondition()
    {
```

Once again we create a `MeshBasedCellPopulation`.
```cpp
        HoneycombMeshGenerator generator(7, 7, 0);
        boost::shared_ptr<MutableMesh<2,2> > p_mesh = generator.GetMesh();

        std::vector<CellPtr> cells;
        CellsGenerator<FixedG1GenerationalCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasic(cells, p_mesh->GetNumNodes());

        MeshBasedCellPopulation<2> cell_population(*p_mesh, cells);

```

We use the cell population to construct a cell population boundary condition object.
```cpp
        MAKE_PTR_ARGS(MyBoundaryCondition, p_bc, (&cell_population));

```

We then pass in the cell population into an `OffLatticeSimulation`,
and set the output directory, output multiple, and end time.
```cpp
        OffLatticeSimulation<2> simulator(cell_population);
        simulator.SetOutputDirectory("TestOffLatticeSimulationWithMyBoundaryCondition");
        simulator.SetSamplingTimestepMultiple(12);
        simulator.SetEndTime(1.0);

```

We create a force law and pass it to the `OffLatticeSimulation`.
```cpp
        MAKE_PTR(GeneralisedLinearSpringForce<2>, p_linear_force);
        p_linear_force->SetCutOffLength(3);
        simulator.AddForce(p_linear_force);

```

We now pass the cell population boundary condition into the cell-based simulation.
```cpp
        simulator.AddCellPopulationBoundaryCondition(p_bc);

```

To run the simulation, we call `Solve()`.
```cpp
        simulator.Solve();
    }
```


When you visualize the results with

`java Visualize2dCentreCells /tmp/$USER/testoutput/TestOffLatticeSimulationWithMyBoundaryCondition/results_from_time_0`

you should see that cells are restricted to the domain 0 <= y <= 5.

```cpp
};

```



## Full code
```cpp
#include <cxxtest/TestSuite.h>
#include "CheckpointArchiveTypes.hpp"
#include "AbstractCellBasedTestSuite.hpp"

#include "AbstractCellPopulationBoundaryCondition.hpp"
#include "OffLatticeSimulation.hpp"
#include "HoneycombMeshGenerator.hpp"
#include "HoneycombVertexMeshGenerator.hpp"
#include "VertexBasedCellPopulation.hpp"
#include "CellsGenerator.hpp"
#include "FixedG1GenerationalCellCycleModel.hpp"
#include "GeneralisedLinearSpringForce.hpp"
#include "SmartPointers.hpp"
#include "FakePetscSetup.hpp"

class MyBoundaryCondition : public AbstractCellPopulationBoundaryCondition<2>
{
private:

    friend class boost::serialization::access;
    template<class Archive>
    void serialize(Archive & archive, const unsigned int version)
    {
        archive & boost::serialization::base_object<AbstractCellPopulationBoundaryCondition<2> >(*this);
    }

public:
    MyBoundaryCondition(AbstractCellPopulation<2>* pCellPopulation)
        : AbstractCellPopulationBoundaryCondition<2>(pCellPopulation)
    {
    }

    void ImposeBoundaryCondition(const std::map<Node<2>*, c_vector<double, 2> >& rOldLocations)
    {
        for (AbstractCellPopulation<2>::Iterator cell_iter = this->mpCellPopulation->Begin();
             cell_iter != this->mpCellPopulation->End();
             ++cell_iter)
        {
            unsigned node_index = this->mpCellPopulation->GetLocationIndexUsingCell(*cell_iter);
            Node<2>* p_node = this->mpCellPopulation->GetNode(node_index);
            double y_coordinate = p_node->rGetLocation()[1];

            if (y_coordinate > 5.0)
            {
                p_node->rGetModifiableLocation()[1] = 5.0;
            }
            else if (y_coordinate < 0.0)
            {
                p_node->rGetModifiableLocation()[1] = 0.0;
            }
        }
    }

    bool VerifyBoundaryCondition()
    {
        bool condition_satisfied = true;

        for (AbstractCellPopulation<2>::Iterator cell_iter = this->mpCellPopulation->Begin();
             cell_iter != this->mpCellPopulation->End();
             ++cell_iter)
        {
            c_vector<double, 2> cell_location = this->mpCellPopulation->GetLocationOfCellCentre(*cell_iter);
            double y_coordinate = cell_location(1);

            if ((y_coordinate < 0.0) || (y_coordinate > 5.0))
            {
                condition_satisfied = false;
                break;
            }
        }
        return condition_satisfied;
    }

    void OutputCellPopulationBoundaryConditionParameters(out_stream& rParamsFile)
    {
        AbstractCellPopulationBoundaryCondition<2>::OutputCellPopulationBoundaryConditionParameters(rParamsFile);
    }
};

#include "SerializationExportWrapper.hpp"
CHASTE_CLASS_EXPORT(MyBoundaryCondition)
#include "SerializationExportWrapperForCpp.hpp"
CHASTE_CLASS_EXPORT(MyBoundaryCondition)

namespace boost
{
    namespace serialization
    {
        template<class Archive>
        inline void save_construct_data(
            Archive & ar, const MyBoundaryCondition * t, const unsigned int file_version)
        {
            const AbstractCellPopulation<2>* const p_cell_population = t->GetCellPopulation();
            ar << p_cell_population;
        }

        template<class Archive>
        inline void load_construct_data(
            Archive & ar, MyBoundaryCondition * t, const unsigned int file_version)
        {
            AbstractCellPopulation<2>* p_cell_population;
            ar >> p_cell_population;

            ::new(t)MyBoundaryCondition(p_cell_population);
        }
    }
}

class TestCreatingAndUsingANewCellPopulationBoundaryConditionTutorial : public AbstractCellBasedTestSuite
{
public:

    void TestMyBoundaryCondition()
    {
        HoneycombMeshGenerator generator(7, 7);
        boost::shared_ptr<MutableMesh<2,2> > p_mesh = generator.GetMesh();

        std::vector<CellPtr> cells;
        CellsGenerator<FixedG1GenerationalCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasic(cells, p_mesh->GetNumNodes());

        MeshBasedCellPopulation<2> cell_population(*p_mesh, cells);

        MyBoundaryCondition bc(&cell_population);

        bool population_satisfies_bc = bc.VerifyBoundaryCondition();
        TS_ASSERT_EQUALS(population_satisfies_bc, false);

        std::map<Node<2>*, c_vector<double, 2> > old_node_locations;
        for (AbstractMesh<2,2>::NodeIterator node_iter = p_mesh->GetNodeIteratorBegin();
                node_iter != p_mesh->GetNodeIteratorEnd();
                ++node_iter)
        {
            old_node_locations[&(*node_iter)] = node_iter->rGetLocation();
        }

        bc.ImposeBoundaryCondition(old_node_locations);

        population_satisfies_bc = bc.VerifyBoundaryCondition();
        TS_ASSERT_EQUALS(population_satisfies_bc, true);

        OutputFileHandler handler("archive", false);
        std::string archive_filename = handler.GetOutputDirectoryFullPath() + "my_bc.arch";
        {
            std::ofstream ofs(archive_filename.c_str());
            boost::archive::text_oarchive output_arch(ofs);

            AbstractCellPopulationBoundaryCondition<2>* const p_bc = new MyBoundaryCondition(NULL);
            output_arch << p_bc;
            delete p_bc;
        }
        {
            std::ifstream ifs(archive_filename.c_str(), std::ios::binary);
            boost::archive::text_iarchive input_arch(ifs);

            AbstractCellPopulationBoundaryCondition<2>* p_bc;
            input_arch >> p_bc;

            delete p_bc;
        }
    }

    void TestOffLatticeSimulationWithMyBoundaryCondition()
    {
        HoneycombMeshGenerator generator(7, 7, 0);
        boost::shared_ptr<MutableMesh<2,2> > p_mesh = generator.GetMesh();

        std::vector<CellPtr> cells;
        CellsGenerator<FixedG1GenerationalCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasic(cells, p_mesh->GetNumNodes());

        MeshBasedCellPopulation<2> cell_population(*p_mesh, cells);

        MAKE_PTR_ARGS(MyBoundaryCondition, p_bc, (&cell_population));

        OffLatticeSimulation<2> simulator(cell_population);
        simulator.SetOutputDirectory("TestOffLatticeSimulationWithMyBoundaryCondition");
        simulator.SetSamplingTimestepMultiple(12);
        simulator.SetEndTime(1.0);

        MAKE_PTR(GeneralisedLinearSpringForce<2>, p_linear_force);
        p_linear_force->SetCutOffLength(3);
        simulator.AddForce(p_linear_force);

        simulator.AddCellPopulationBoundaryCondition(p_bc);

        simulator.Solve();
    }
};

```
