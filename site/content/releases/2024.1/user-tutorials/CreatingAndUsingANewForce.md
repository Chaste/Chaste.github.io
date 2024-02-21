---
title : "Creating And Using A New Force"
summary: "An example showing how to create and use a new force"
draft: false
images: []
toc: true
version: "2024.1"
version: "2024.1"
---
This tutorial is automatically generated from [TestCreatingAndUsingANewForceTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/cell_based/test/tutorial/TestCreatingAndUsingANewForceTutorial.hpp) at revision [1dfba06b4d82](https://github.com/Chaste/Chaste/commit/1dfba06b4d8265be2322817e6dfe1536071d9a0a). Note that the code is given in full at the bottom of the page.
## An example showing how to create and use a new force

### Introduction

In previous cell-based Chaste tutorials, we used existing force classes to define
how cells interact mechanically. In this tutorial we show
how to create a new force class, and how this can be used in a cell-based
simulation.

### 1. Including header files

As in previous cell-based Chaste tutorials, we begin by including the necessary header files.

```cpp
#include <cxxtest/TestSuite.h>
#include "CheckpointArchiveTypes.hpp"
#include "AbstractCellBasedTestSuite.hpp"
```

The next header defines a base class for forces, from which the new class will inherit.

```cpp
#include "AbstractForce.hpp"
```

The remaining header files define classes that will be used in the cell-based
simulation test. We have encountered each of these header files in previous cell-based
Chaste tutorials.

```cpp
#include "HoneycombMeshGenerator.hpp"
#include "FixedG1GenerationalCellCycleModel.hpp"
#include "GeneralisedLinearSpringForce.hpp"
#include "OffLatticeSimulation.hpp"
#include "CellsGenerator.hpp"
#include "TransitCellProliferativeType.hpp"
#include "SmartPointers.hpp"
```

This header ensures that this test is only run on one process, since it doesn't support parallel execution.

```cpp
#include "FakePetscSetup.hpp"
```

### Defining the force class

As an example, let us consider a force for a two-dimensional cell-based
simulation, that mimics gravity. To implement this we define a force
boundary condition class, `MyForce`, which inherits from
`AbstractForce` and overrides the methods `AddForceContribution()` and
`OutputForceParameters()`.

Note that usually this code would be separated out into a separate declaration
in a .hpp file and definition in a .cpp file.

```cpp
class MyForce : public AbstractForce<2>
{
private:
```

This force class includes a member variable, `mStrength`, which
defines the strength of the force. This member variable will be set
in the constructor.

```cpp
    double mStrength;
```

We only need to include the next block of code if we wish to be able
to archive (save or load) the force model object in a cell-based simulation.
The code consists of a `serialize()` method, in which we first archive the force
using the serialization code defined in the base class `AbstractForce`,
then archive the member variable.

```cpp
    friend class boost::serialization::access;
    template<class Archive>
    void serialize(Archive & archive, const unsigned int version)
    {
        archive & boost::serialization::base_object<AbstractForce<2> >(*this);
        archive & mStrength;
    }

public:
```

The first public method is a default constructor, which calls the base
constructor. There is a single input argument, which defines the strength
of the force. We provide a default value of 1.0 for this argument. Inside
the method, we add an assertion to make sure that the strength is strictly
positive.

```cpp
    MyForce(double strength=1.0)
        : AbstractForce<2>(),
          mStrength(strength)
    {
        assert(mStrength > 0.0);
    }
```

The second public method overrides `AddForceContribution()`.
This method takes in one arguments, a reference to the cell population itself.

```cpp
    void AddForceContribution(AbstractCellPopulation<2>& rCellPopulation)
    {
```

Inside the method, we loop over nodes, and add a constant vector to
each node, in the negative y-direction and of magnitude `mStrength`.

```cpp
        c_vector<double, 2> force = zero_vector<double>(2);
        force(1) = -mStrength;

        for (unsigned node_index=0; node_index<rCellPopulation.GetNumNodes(); node_index++)
        {
            rCellPopulation.GetNode(node_index)->AddAppliedForceContribution(force);
        }
    }
```

We also add a get method for `mStrength`, to allow for testing.

```cpp
    double GetStrength()
    {
        return mStrength;
    }
```

Just as we encountered in [Creating And Using A New Cell Killer](/docs/user-tutorials/creatingandusinganewcellkiller/), here we must override
a method that outputs any member variables to a specified results file `rParamsFile`.
In our case, we output the member variable `mStrength`, then call the method on the base class.

```cpp
    void OutputForceParameters(out_stream& rParamsFile)
    {
        *rParamsFile << "\t\t\t<Strength>" << mStrength << "</Strength>\n";
        AbstractForce<2>::OutputForceParameters(rParamsFile);
    }
};
```

As mentioned in previous cell-based Chaste tutorials, we need to include the next block
of code to be able to archive the force object in a cell-based
simulation, and to obtain a unique identifier for our new force for writing
results to file.

```cpp
#include "SerializationExportWrapper.hpp"
CHASTE_CLASS_EXPORT(MyForce)
#include "SerializationExportWrapperForCpp.hpp"
CHASTE_CLASS_EXPORT(MyForce)
```

This completes the code for `MyForce`. Note that usually this code
would be separated out into a separate declaration in a .hpp file and definition
in a .cpp file.

#### The Tests

We now define the test class, which inherits from `AbstractCellBasedTestSuite`.

```cpp
class TestCreatingAndUsingANewForceTutorial : public AbstractCellBasedTestSuite
{
public:
```

### Testing the force

We now test that our new force is implemented correctly.

```cpp
    void TestMyForce()
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

Initialise all node forces to zero

```cpp
        for (unsigned i=0; i<cell_population.GetNumNodes(); i++)
        {
             cell_population.GetNode(i)->ClearAppliedForce();
        }
```

We now create a force object of strength 5.0.

```cpp
        MyForce force(5.0);
```

We test that the force calculation is correct.

```cpp
        force.AddForceContribution(cell_population);

        for (unsigned node_index=0; node_index<cell_population.GetNumNodes(); node_index++)
        {
            TS_ASSERT_DELTA(cell_population.GetNode(node_index)->rGetAppliedForce()[0], 0.0, 1e-4);
            TS_ASSERT_DELTA(cell_population.GetNode(node_index)->rGetAppliedForce()[1], -5.0, 1e-4);
        }
```

The last block of code provides an archiving test for the force class,
in a similar way to previous cell-based Chaste tutorials:

Note that it is important to test archiving by using an abstract
pointer, so that you check that boost can identify and record which
concrete class it should be dealing with.
This tests the `CHASTE_CLASS_EXPORT(MyForce)` lines are implemented correctly.

```cpp
        OutputFileHandler handler("archive", false);
        std::string archive_filename = handler.GetOutputDirectoryFullPath() + "my_force.arch";
        {
            AbstractForce<2>* const p_force = new MyForce(2.6);
            std::ofstream ofs(archive_filename.c_str());
            boost::archive::text_oarchive output_arch(ofs);

            output_arch << p_force;
            delete p_force;
        }
        {
            std::ifstream ifs(archive_filename.c_str(), std::ios::binary);
            boost::archive::text_iarchive input_arch(ifs);

            AbstractForce<2>* p_force;
            input_arch >> p_force;

            TS_ASSERT_DELTA(dynamic_cast<MyForce*>(p_force)->GetStrength(), 2.6, 1e-4);

            delete p_force;
        }
    }
```

### Using the force in a cell-based simulation

We now provide a test demonstrating how `MyForce` can be used
in a cell-based simulation.

```cpp
    void TestOffLatticeSimulationWithMyForce()
    {
```

Once again we create a `MeshBasedCellPopulation`.

```cpp
        HoneycombMeshGenerator generator(5, 5);
        boost::shared_ptr<MutableMesh<2,2> > p_mesh = generator.GetMesh();

        std::vector<CellPtr> cells;
        MAKE_PTR(TransitCellProliferativeType, p_transit_type);
        CellsGenerator<FixedG1GenerationalCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasicRandom(cells, p_mesh->GetNumNodes(), p_transit_type);

        MeshBasedCellPopulation<2> cell_population(*p_mesh, cells);
```

We then pass in the cell population into an `OffLatticeSimulation`,
and set the output directory, output multiple, and end time.

```cpp
        OffLatticeSimulation<2> simulator(cell_population);
        simulator.SetOutputDirectory("TestOffLatticeSimulationWithMyForce");
        simulator.SetSamplingTimestepMultiple(12);
        simulator.SetEndTime(5.0);
```

We create our force law and pass it to the `OffLatticeSimulation`.

```cpp
        MAKE_PTR_ARGS(MyForce, p_force, (0.5));
        simulator.AddForce(p_force);
```

We also create a force law to say how the cells interact and pass it to the `OffLatticeSimulation`.

```cpp
        MAKE_PTR(GeneralisedLinearSpringForce<2>, p_linear_force);
        p_linear_force->SetCutOffLength(1.5);
        simulator.AddForce(p_linear_force);
```

To run the simulation, we call `Solve()`.

```cpp
        simulator.Solve();
    }
};
```

When you visualize the results with

`java Visualize2dCentreCells /tmp/$USER/testoutput/TestOffLatticeSimulationWithMyForce/results_from_time_0`

you should see a collection of cells moving downwards and proliferating.

## Full code

```cpp
#include <cxxtest/TestSuite.h>
#include "CheckpointArchiveTypes.hpp"
#include "AbstractCellBasedTestSuite.hpp"

#include "AbstractForce.hpp"
#include "HoneycombMeshGenerator.hpp"
#include "FixedG1GenerationalCellCycleModel.hpp"
#include "GeneralisedLinearSpringForce.hpp"
#include "OffLatticeSimulation.hpp"
#include "CellsGenerator.hpp"
#include "TransitCellProliferativeType.hpp"
#include "SmartPointers.hpp"

#include "FakePetscSetup.hpp"

class MyForce : public AbstractForce<2>
{
private:

    double mStrength;

    friend class boost::serialization::access;
    template<class Archive>
    void serialize(Archive & archive, const unsigned int version)
    {
        archive & boost::serialization::base_object<AbstractForce<2> >(*this);
        archive & mStrength;
    }

public:
    MyForce(double strength=1.0)
        : AbstractForce<2>(),
          mStrength(strength)
    {
        assert(mStrength > 0.0);
    }

    void AddForceContribution(AbstractCellPopulation<2>& rCellPopulation)
    {
        c_vector<double, 2> force = zero_vector<double>(2);
        force(1) = -mStrength;

        for (unsigned node_index=0; node_index<rCellPopulation.GetNumNodes(); node_index++)
        {
            rCellPopulation.GetNode(node_index)->AddAppliedForceContribution(force);
        }
    }

    double GetStrength()
    {
        return mStrength;
    }

    void OutputForceParameters(out_stream& rParamsFile)
    {
        *rParamsFile << "\t\t\t<Strength>" << mStrength << "</Strength>\n";
        AbstractForce<2>::OutputForceParameters(rParamsFile);
    }
};

#include "SerializationExportWrapper.hpp"
CHASTE_CLASS_EXPORT(MyForce)
#include "SerializationExportWrapperForCpp.hpp"
CHASTE_CLASS_EXPORT(MyForce)

class TestCreatingAndUsingANewForceTutorial : public AbstractCellBasedTestSuite
{
public:

    void TestMyForce()
    {
        HoneycombMeshGenerator generator(7, 7);
        boost::shared_ptr<MutableMesh<2,2> > p_mesh = generator.GetMesh();

        std::vector<CellPtr> cells;
        CellsGenerator<FixedG1GenerationalCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasic(cells, p_mesh->GetNumNodes());

        MeshBasedCellPopulation<2> cell_population(*p_mesh, cells);

        for (unsigned i=0; i<cell_population.GetNumNodes(); i++)
        {
             cell_population.GetNode(i)->ClearAppliedForce();
        }

        MyForce force(5.0);

        force.AddForceContribution(cell_population);

        for (unsigned node_index=0; node_index<cell_population.GetNumNodes(); node_index++)
        {
            TS_ASSERT_DELTA(cell_population.GetNode(node_index)->rGetAppliedForce()[0], 0.0, 1e-4);
            TS_ASSERT_DELTA(cell_population.GetNode(node_index)->rGetAppliedForce()[1], -5.0, 1e-4);
        }

        OutputFileHandler handler("archive", false);
        std::string archive_filename = handler.GetOutputDirectoryFullPath() + "my_force.arch";
        {
            AbstractForce<2>* const p_force = new MyForce(2.6);
            std::ofstream ofs(archive_filename.c_str());
            boost::archive::text_oarchive output_arch(ofs);

            output_arch << p_force;
            delete p_force;
        }
        {
            std::ifstream ifs(archive_filename.c_str(), std::ios::binary);
            boost::archive::text_iarchive input_arch(ifs);

            AbstractForce<2>* p_force;
            input_arch >> p_force;

            TS_ASSERT_DELTA(dynamic_cast<MyForce*>(p_force)->GetStrength(), 2.6, 1e-4);

            delete p_force;
        }
    }

    void TestOffLatticeSimulationWithMyForce()
    {
        HoneycombMeshGenerator generator(5, 5);
        boost::shared_ptr<MutableMesh<2,2> > p_mesh = generator.GetMesh();

        std::vector<CellPtr> cells;
        MAKE_PTR(TransitCellProliferativeType, p_transit_type);
        CellsGenerator<FixedG1GenerationalCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasicRandom(cells, p_mesh->GetNumNodes(), p_transit_type);

        MeshBasedCellPopulation<2> cell_population(*p_mesh, cells);

        OffLatticeSimulation<2> simulator(cell_population);
        simulator.SetOutputDirectory("TestOffLatticeSimulationWithMyForce");
        simulator.SetSamplingTimestepMultiple(12);
        simulator.SetEndTime(5.0);

        MAKE_PTR_ARGS(MyForce, p_force, (0.5));
        simulator.AddForce(p_force);

        MAKE_PTR(GeneralisedLinearSpringForce<2>, p_linear_force);
        p_linear_force->SetCutOffLength(1.5);
        simulator.AddForce(p_linear_force);

        simulator.Solve();
    }
};
```
