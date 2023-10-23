
---
title : "TestCreatingAndUsingANewCellMutationStateTutorial.hpp"
description: "This tutorial is automatically generated from the file cell_based/test/tutorial/TestCreatingAndUsingANewCellMutationStateTutorial.hpp at revision [dc0fc851da33](https://github.com/Chaste/Chaste/commit/dc0fc851da33d398a30adf6f0a3033ba159c438b). Note that the code is given in full at the bottom of the page."
draft: false
images: []
toc: true
---

# An example showing how to create a new cell mutation state and use it in a cell-based simulation 

## Introduction 

In the tumour spheroid tutorial we noted that a cell mutation state is always required
when constructing a cell. In this tutorial, we show how to create a new cell mutation
state class, and how this can be used in a cell-based simulation.

## 1. Including header files 

As in previous cell-based Chaste tutorials, we begin by including the necessary
header file and archiving headers.

~~~cpp
#include <cxxtest/TestSuite.h>
#include "CheckpointArchiveTypes.hpp"
#include "AbstractCellBasedTestSuite.hpp"

~~~
The next header defines a base class for cell mutation states. Our new
cell mutation state will inherit from this abstract class.
~~~cpp
#include "AbstractCellMutationState.hpp"
~~~
The remaining header files define classes that will be used in the cell-based
simulation test. We have encountered each of these header files in previous cell-based
Chaste tutorials.
~~~cpp
#include "HoneycombMeshGenerator.hpp"
#include "WildTypeCellMutationState.hpp"
#include "FixedG1GenerationalCellCycleModel.hpp"
#include "GeneralisedLinearSpringForce.hpp"
#include "OffLatticeSimulation.hpp"
#include "CellMutationStatesCountWriter.hpp"
#include "CellsGenerator.hpp"
#include "SmartPointers.hpp"
#include "FakePetscSetup.hpp"

~~~
## Defining the cell mutation state class 

As an example, let us consider a cell mutation state representing the p53
172R-H gain-of-function mutant, which is equivalent to the common 175R-H
human breast cancer mutant; for further details on this mutant, see for
example Murphy et al, FASEB J. 14:2291-2302 (2000).

Wild-type p53 has been referred to as the "guardian of the genome",
responding to DNA damage or checkpoint failure by either arresting cell
cycle progression to facilitate DNA repair or initiating an apoptotic
pathway to remove damaged cells. Approximately 40% of human breast cancers
contain alterations in p53.

As we can see, apart from a serialize() method and a constructor, this class
does not contain any member variables or methods. This is because generally
a cell's mutation state is used, much like a flag, by other classes when
determining a cell's behaviour (whether a cell should undergo
apoptosis following prolonged stress, for example, or alter its proliferative
behaviour).

~~~cpp
class P53GainOfFunctionCellMutationState : public AbstractCellMutationState
{
private:

    friend class boost::serialization::access;
    template<class Archive>
    void serialize(Archive & archive, const unsigned int version)
    {
        archive & boost::serialization::base_object<AbstractCellMutationState>(*this);
    }

public:
~~~
The only public method is a default constructor, which just calls the base
constructor with a single unsigned parameter. This sets the value of the
base class member variable `mColour`{.cpp}, which can be used by visualization tools
to paint cells with this mutation state a distinct colour if required.
~~~cpp
    P53GainOfFunctionCellMutationState()
        : AbstractCellMutationState(5)
    {
    }
};

~~~
As mentioned in previous cell-based Chaste tutorials, we need to include the next block
of code to be able to archive the cell mutation state object in a cell-based
simulation, and to obtain a unique identifier for our new cell mutation state for writing
results to file.

~~~cpp
#include "SerializationExportWrapper.hpp"
CHASTE_CLASS_EXPORT(P53GainOfFunctionCellMutationState)
#include "SerializationExportWrapperForCpp.hpp"
CHASTE_CLASS_EXPORT(P53GainOfFunctionCellMutationState)

~~~
This completes the code for `P53GainOfFunctionCellMutationState`{.cpp}. Note that usually this code would
be separated out into a separate declaration in a .hpp file and definition in a .cpp file.

### The Tests 

We now define the test class, which inherits from `AbstractCellBasedTestSuite`{.cpp}.

~~~cpp
class TestCreatingAndUsingANewCellMutationStateTutorial : public AbstractCellBasedTestSuite
{
public:

~~~
## Testing the cell mutation state 

We begin by testing that our new cell mutation state is implemented correctly.

~~~cpp
    void TestP53GainOfFunctionCellMutationState()
    {
~~~
We begin by testing that some of the base class methods work correctly.
We typically use shared pointers to create and access cell mutation states, as
follows. This is because it makes sense for all cells that have the same mutation
to share a pointer to the same cell mutation state object (although strictly speaking,
they are not required to).
~~~cpp
        MAKE_PTR(P53GainOfFunctionCellMutationState, p_state);

~~~
Each cell mutation state has a member variable, `mCellCount`{.cpp}, which
stores the number of cells with this mutation state. In fact, `mCellCount`{.cpp}
is defined in the class `AbstractCellProperty`{.cpp}, from which
`AbstractCellMutationState`{.cpp} inherits, as well as other cell properties
such as `CellLabel`{.cpp}. We can test whether `mCellCount`{.cpp} is being
updated correctly by our cell mutation state, as follows.
~~~cpp
        TS_ASSERT_EQUALS(p_state->GetCellCount(), 0u);
        p_state->IncrementCellCount();
        TS_ASSERT_EQUALS(p_state->GetCellCount(), 1u);
        p_state->DecrementCellCount();
        TS_ASSERT_EQUALS(p_state->GetCellCount(), 0u);
        TS_ASSERT_THROWS_THIS(p_state->DecrementCellCount(),
                "Cannot decrement cell count: no cells have this cell property");

~~~
We can also test that {{{mColour}}} has been set correctly by our constructor, as follows.
~~~cpp
        TS_ASSERT_EQUALS(p_state->GetColour(), 5u);

~~~
We can also test whether our cell mutation state is of a given type, as follows.
~~~cpp
        TS_ASSERT_EQUALS(p_state->IsType<WildTypeCellMutationState>(), false);
        TS_ASSERT_EQUALS(p_state->IsType<P53GainOfFunctionCellMutationState>(), true);

~~~
We can also test that archiving is implemented correctly for our cell
mutation state, as follows (further details on how to implement and
test archiving can be found at ChasteGuides/BoostSerialization).
~~~cpp
        OutputFileHandler handler("archive", false);
        std::string archive_filename = handler.GetOutputDirectoryFullPath() + "p53_mutation.arch";

        {
            AbstractCellProperty* const p_const_state = new P53GainOfFunctionCellMutationState();
            p_const_state->IncrementCellCount();

            TS_ASSERT_EQUALS(p_const_state->GetCellCount(), 1u);
            TS_ASSERT_EQUALS(dynamic_cast<AbstractCellMutationState*>(p_const_state)->GetColour(), 5u);

            std::ofstream ofs(archive_filename.c_str());
            boost::archive::text_oarchive output_arch(ofs);

            output_arch << p_const_state;

            delete p_const_state;
        }

        {
            AbstractCellProperty* p_arch_state;

            std::ifstream ifs(archive_filename.c_str());
            boost::archive::text_iarchive input_arch(ifs);

            input_arch >> p_arch_state;

            TS_ASSERT_EQUALS(p_arch_state->GetCellCount(), 1u);

            P53GainOfFunctionCellMutationState* p_real_state = dynamic_cast<P53GainOfFunctionCellMutationState*>(p_arch_state);
            TS_ASSERT(p_real_state != NULL);
            TS_ASSERT_EQUALS(p_real_state->GetColour(), 5u);

            delete p_arch_state;
        }
    }

~~~
## Using the cell mutation state in a cell-based simulation 

We conclude with a brief test demonstrating how `P53GainOfFunctionCellMutationState`{.cpp} can be used
in a cell-based simulation.

~~~cpp
    void TestOffLatticeSimulationWithP53GainOfFunctionCellMutationState()
    {
~~~
We use the `HoneycombMeshGenerator`{.cpp} to create a honeycomb mesh covering a
circular domain of given radius, as follows.
~~~cpp
        HoneycombMeshGenerator generator(10, 10);
        boost::shared_ptr<MutableMesh<2,2> > p_mesh = generator.GetCircularMesh(5);

~~~
We now create a shared pointer to our new cell mutation state, as follows.
~~~cpp
        MAKE_PTR(P53GainOfFunctionCellMutationState, p_state);

~~~
Next, we create some cells, as follows.
~~~cpp
        std::vector<CellPtr> cells;
        CellsGenerator<FixedG1GenerationalCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasicRandom(cells, p_mesh->GetNumNodes());

~~~
We now assign the mutation to the 11th and 51st cells.
~~~cpp
        cells[10]->SetMutationState(p_state);
        cells[50]->SetMutationState(p_state);

~~~
Now that we have defined the mesh and cells, we can define the cell population. The constructor
takes in the mesh and the cells vector.
~~~cpp
        MeshBasedCellPopulation<2> cell_population(*p_mesh, cells);

~~~
In order to visualize labelled cells we need to use the following command.
~~~cpp
        cell_population.AddCellPopulationCountWriter<CellMutationStatesCountWriter>();

~~~
We then pass in the cell population into an `OffLatticeSimulation`{.cpp},
and set the output directory, output multiple, and end time.
~~~cpp
        OffLatticeSimulation<2> simulator(cell_population);
        simulator.SetOutputDirectory("TestOffLatticeSimulationWithNewMutationState");
        simulator.SetSamplingTimestepMultiple(12);
        simulator.SetEndTime(10.0);

~~~
We create a force law and pass it to the {{{OffLatticeSimulation}}}.
~~~cpp
        MAKE_PTR(GeneralisedLinearSpringForce<2>, p_linear_force);
        p_linear_force->SetCutOffLength(3);
        simulator.AddForce(p_linear_force);

~~~
To run the simulation, we call {{{Solve()}}}.
~~~cpp
        simulator.Solve();
    }
~~~

When you visualize the results with

`java Visualize2dCentreCells /tmp/$USER/testoutput/TestOffLatticeSimulationWithNewMutationState/results_from_time_0`{.cpp}

you should see two cells in black which are the cells with the new mutation. If we want these cells to behave differently we
would need to write an new `CellCycleModel`{.cpp}, `CellKiller`{.cpp}, `Force`{.cpp}, or `CellPopulationBoundaryCondition`{.cpp}
which checks for the new mutation.

~~~cpp
};

~~~


# Code
The full code is given below


## File name `TestCreatingAndUsingANewCellMutationStateTutorial.hpp` 

~~~cpp
#include <cxxtest/TestSuite.h>
#include "CheckpointArchiveTypes.hpp"
#include "AbstractCellBasedTestSuite.hpp"

#include "AbstractCellMutationState.hpp"
#include "HoneycombMeshGenerator.hpp"
#include "WildTypeCellMutationState.hpp"
#include "FixedG1GenerationalCellCycleModel.hpp"
#include "GeneralisedLinearSpringForce.hpp"
#include "OffLatticeSimulation.hpp"
#include "CellMutationStatesCountWriter.hpp"
#include "CellsGenerator.hpp"
#include "SmartPointers.hpp"
#include "FakePetscSetup.hpp"

class P53GainOfFunctionCellMutationState : public AbstractCellMutationState
{
private:

    friend class boost::serialization::access;
    template<class Archive>
    void serialize(Archive & archive, const unsigned int version)
    {
        archive & boost::serialization::base_object<AbstractCellMutationState>(*this);
    }

public:
    P53GainOfFunctionCellMutationState()
        : AbstractCellMutationState(5)
    {
    }
};

#include "SerializationExportWrapper.hpp"
CHASTE_CLASS_EXPORT(P53GainOfFunctionCellMutationState)
#include "SerializationExportWrapperForCpp.hpp"
CHASTE_CLASS_EXPORT(P53GainOfFunctionCellMutationState)

class TestCreatingAndUsingANewCellMutationStateTutorial : public AbstractCellBasedTestSuite
{
public:

    void TestP53GainOfFunctionCellMutationState()
    {
        MAKE_PTR(P53GainOfFunctionCellMutationState, p_state);

        TS_ASSERT_EQUALS(p_state->GetCellCount(), 0u);
        p_state->IncrementCellCount();
        TS_ASSERT_EQUALS(p_state->GetCellCount(), 1u);
        p_state->DecrementCellCount();
        TS_ASSERT_EQUALS(p_state->GetCellCount(), 0u);
        TS_ASSERT_THROWS_THIS(p_state->DecrementCellCount(),
                "Cannot decrement cell count: no cells have this cell property");

        TS_ASSERT_EQUALS(p_state->GetColour(), 5u);

        TS_ASSERT_EQUALS(p_state->IsType<WildTypeCellMutationState>(), false);
        TS_ASSERT_EQUALS(p_state->IsType<P53GainOfFunctionCellMutationState>(), true);

        OutputFileHandler handler("archive", false);
        std::string archive_filename = handler.GetOutputDirectoryFullPath() + "p53_mutation.arch";

        {
            AbstractCellProperty* const p_const_state = new P53GainOfFunctionCellMutationState();
            p_const_state->IncrementCellCount();

            TS_ASSERT_EQUALS(p_const_state->GetCellCount(), 1u);
            TS_ASSERT_EQUALS(dynamic_cast<AbstractCellMutationState*>(p_const_state)->GetColour(), 5u);

            std::ofstream ofs(archive_filename.c_str());
            boost::archive::text_oarchive output_arch(ofs);

            output_arch << p_const_state;

            delete p_const_state;
        }

        {
            AbstractCellProperty* p_arch_state;

            std::ifstream ifs(archive_filename.c_str());
            boost::archive::text_iarchive input_arch(ifs);

            input_arch >> p_arch_state;

            TS_ASSERT_EQUALS(p_arch_state->GetCellCount(), 1u);

            P53GainOfFunctionCellMutationState* p_real_state = dynamic_cast<P53GainOfFunctionCellMutationState*>(p_arch_state);
            TS_ASSERT(p_real_state != NULL);
            TS_ASSERT_EQUALS(p_real_state->GetColour(), 5u);

            delete p_arch_state;
        }
    }

    void TestOffLatticeSimulationWithP53GainOfFunctionCellMutationState()
    {
        HoneycombMeshGenerator generator(10, 10);
        boost::shared_ptr<MutableMesh<2,2> > p_mesh = generator.GetCircularMesh(5);

        MAKE_PTR(P53GainOfFunctionCellMutationState, p_state);

        std::vector<CellPtr> cells;
        CellsGenerator<FixedG1GenerationalCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasicRandom(cells, p_mesh->GetNumNodes());

        cells[10]->SetMutationState(p_state);
        cells[50]->SetMutationState(p_state);

        MeshBasedCellPopulation<2> cell_population(*p_mesh, cells);

        cell_population.AddCellPopulationCountWriter<CellMutationStatesCountWriter>();

        OffLatticeSimulation<2> simulator(cell_population);
        simulator.SetOutputDirectory("TestOffLatticeSimulationWithNewMutationState");
        simulator.SetSamplingTimestepMultiple(12);
        simulator.SetEndTime(10.0);

        MAKE_PTR(GeneralisedLinearSpringForce<2>, p_linear_force);
        p_linear_force->SetCutOffLength(3);
        simulator.AddForce(p_linear_force);

        simulator.Solve();
    }
};

~~~

