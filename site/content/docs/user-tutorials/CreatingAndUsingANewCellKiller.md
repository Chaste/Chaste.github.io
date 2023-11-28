---
title : "Creating And Using A New Cell Killer"
summary: "An example showing how to create a new cell killer and use it in a cell-based simulation"
draft: false
images: []
toc: true
---
This tutorial is automatically generated from [TestCreatingAndUsingANewCellKillerTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/cell_based/test/tutorial/TestCreatingAndUsingANewCellKillerTutorial.hpp) at revision [6ae21367d74b](https://github.com/Chaste/Chaste/commit/6ae21367d74bae0b21b25884bc6d70ec91bd1d14). Note that the code is given in full at the bottom of the page.
## An example showing how to create a new cell killer and use it in a cell-based simulation

### Introduction

In the crypt tutorial, we used an existing cell killer class to define
how cells were sloughed off the top of a crypt. In this tutorial we show
how to create a new cell killer class, and how this can be used in a cell-based
simulation.

### 1. Including header files

As in previous cell-based Chaste tutorials, we begin by including the necessary
header file and archiving headers.

```cpp
#include <cxxtest/TestSuite.h>
#include "CheckpointArchiveTypes.hpp"
#include "AbstractCellBasedTestSuite.hpp"

#include <boost/archive/text_oarchive.hpp>
#include <boost/archive/text_iarchive.hpp>
```

The next header defines a base class for cell killers, from which the new
cell killer class will inherit.

```cpp
#include "AbstractCellKiller.hpp"
```

The next header defines a writer which outputs information on cells killed to the file
`removals.dat` .

```cpp
#include "CellRemovalLocationsWriter.hpp"
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
#include "SmartPointers.hpp"
//This test is always run sequentially (never in parallel)
#include "FakePetscSetup.hpp"
```

### Defining the cell killer class

As an example, let us consider a cell killer that labels any cells in a
two-dimensional cell population which lie outside the elliptical domain given in
Cartesian coordinates by the equation $\left(\frac{x}{20}\right)^2 + \left(\frac{y}{10}\right)^2 < 1$.
To implement this we define a new cell killer class, `MyCellKiller`,
which inherits from `AbstractCellKiller` and overrides the
`CheckAndLabelCellsForApoptosisOrDeath()` method.

Note that usually this code would be separated out into a separate declaration in
a .hpp file and definition in a .cpp file.

```cpp
class MyCellKiller : public AbstractCellKiller<2>
{
private:

    friend class boost::serialization::access;
    template<class Archive>
    void serialize(Archive & archive, const unsigned int version)
    {
        archive & boost::serialization::base_object<AbstractCellKiller<2> >(*this);
    }
```

The first public method is a default constructor, which just calls the base
constructor.

```cpp
public:

    MyCellKiller(AbstractCellPopulation<2>* pCellPopulation)
        : AbstractCellKiller<2>(pCellPopulation)
    {}
```

The second public method overrides `CheckAndLabelCellsForApoptosisOrDeath()`.
This method iterates over all cells in the population, and calls `KillCell()` on
any cell whose centre is located outside the ellipse (''x''/20)^2^ + (''y''/10)^2^ < 1.

```cpp
    void CheckAndLabelCellsForApoptosisOrDeath()
    {
        for (AbstractCellPopulation<2>::Iterator cell_iter = this->mpCellPopulation->Begin();
            cell_iter != this->mpCellPopulation->End();
            ++cell_iter)
        {
            c_vector<double, 2> location;
            location = this->mpCellPopulation->GetLocationOfCellCentre(*cell_iter);

            if (pow(location[0]/20, 2) + pow(location[1]/10, 2) > 1.0)
            {
```

This line marks the cell as killed and stores removal information for use by
by the cell writers if the writer `CellRemovalLocationsWriter` is included.

```cpp
                this->mpCellPopulation->KillCell(*cell_iter, "MyCellKiller");
            }
        }
    }
```

The final public method overrides `OutputCellKillerParameters()`.
This method outputs any member variables to a specified results file `rParamsFile`.
In our case, there are no parameters, so we simply call the method on the base class.
Nonetheless, we still need to override the method, since it is pure virtual in the base
class.

```cpp
    void OutputCellKillerParameters(out_stream& rParamsFile)
    {
        AbstractCellKiller<2>::OutputCellKillerParameters(rParamsFile);
    }
};
```

As mentioned in [wiki:UserTutorials/CreatingAndUsingANewCellCycleModel], we need to include the next block
of code to be able to archive the cell killer object in a cell-based
simulation, and to obtain a unique identifier for our new cell killer for writing
results to file.

```cpp
#include "SerializationExportWrapper.hpp"
CHASTE_CLASS_EXPORT(MyCellKiller)
#include "SerializationExportWrapperForCpp.hpp"
CHASTE_CLASS_EXPORT(MyCellKiller)
```

We only need to include the next block of code if we wish to be able to archive (save or load)
the cell killer object in a cell-based simulation. We must define `save_construct_data` and
`load_construct_data` methods, which archive the cell killer constructor input argument(s)
(in this case, a `CellPopulation`).

```cpp
namespace boost
{
    namespace serialization
    {
        template<class Archive>
        inline void save_construct_data(
            Archive & ar, const MyCellKiller * t, const unsigned int file_version)
        {
            const AbstractCellPopulation<2>* const p_cell_population = t->GetCellPopulation();
            ar << p_cell_population;
        }

        template<class Archive>
        inline void load_construct_data(
            Archive & ar, MyCellKiller * t, const unsigned int file_version)
        {
            AbstractCellPopulation<2>* p_cell_population;
            ar >> p_cell_population;

            // Invoke inplace constructor to initialise instance
            ::new(t)MyCellKiller(p_cell_population);
        }
    }
}
```

This completes the code for `MyCellKiller`. Note that usually this code
would be separated out into a separate declaration in a .hpp file and definition
in a .cpp file.

#### The Tests

We now define the test class, which inherits from `AbstractCellBasedTestSuite`.

```cpp
class TestCreatingAndUsingANewCellKillerTutorial : public AbstractCellBasedTestSuite
{
public:
```

### Testing the cell killer

We begin by testing that our new cell-cycle model is implemented correctly.

```cpp
    void TestMyCellKiller()
    {
```

We use the honeycomb mesh generator to create a honeycomb mesh.

```cpp
        HoneycombMeshGenerator generator(20, 20, 0);
        boost::shared_ptr<MutableMesh<2,2> > p_mesh = generator.GetMesh();
```

We then construct and initialise some cells, each with a
`FixedG1GenerationalCellCycleModel`, using the helper class
`CellsGenerator`.

```cpp
        std::vector<CellPtr> cells;
        CellsGenerator<FixedG1GenerationalCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasic(cells, p_mesh->GetNumNodes());
```

Now that we have defined the mesh and cells, we can define the cell population. The
constructor takes in the mesh and the cells vector.

```cpp
        MeshBasedCellPopulation<2> cell_population(*p_mesh, cells);
```

We now use the cell population to construct a cell killer object.

```cpp
        MyCellKiller my_cell_killer(&cell_population);
```

To store information about the lovations and times of the killed cells use the
`CellRemovalLocationsWriter`

```cpp
        cell_population.AddCellPopulationEventWriter<CellRemovalLocationsWriter>();
```

To test that we have implemented the cell killer correctly, we call the
overridden method `CheckAndLabelCellsForApoptosisOrDeath`...

```cpp
        my_cell_killer.CheckAndLabelCellsForApoptosisOrDeath();
```

... and check that any cell whose centre is located outside the ellipse
(''x''/20)^2^ + (''y''/10)^2^ < 1 has indeed been labelled as dead.

```cpp
        for (AbstractCellPopulation<2>::Iterator cell_iter = cell_population.Begin();
             cell_iter != cell_population.End();
             ++cell_iter)
        {
            double x = cell_population.GetLocationOfCellCentre(*cell_iter)[0];
            double y = cell_population.GetLocationOfCellCentre(*cell_iter)[1];

            if (pow(x/20, 2) + pow(y/10, 2) > 1.0)
            {
                TS_ASSERT_EQUALS(cell_iter->IsDead(), true);
            }
            else
            {
                TS_ASSERT_EQUALS(cell_iter->IsDead(), false);
            }
        }
```

As an extra test, we now remove any dead cells and check that all
remaining cells are indeed located within the ellipse.

```cpp
        cell_population.RemoveDeadCells();

        for (AbstractCellPopulation<2>::Iterator cell_iter = cell_population.Begin();
             cell_iter != cell_population.End();
             ++cell_iter)
        {
            double x = cell_population.GetLocationOfCellCentre(*cell_iter)[0];
            double y = cell_population.GetLocationOfCellCentre(*cell_iter)[1];

            TS_ASSERT_LESS_THAN_EQUALS(pow(x/20, 2) + pow(y/10, 2) > 1.0, 1.0);
        }
```

The last chunk of code provides an archiving test for the cell killer.
We create an output archive, save the existing cell killer object via
a pointer, then create an input archive and load the cell killer. If
the cell killer had any member variables, then we would test that these
were correctly initialised when the cell killer is loaded.

```cpp
        OutputFileHandler handler("archive", false);
        std::string archive_filename = handler.GetOutputDirectoryFullPath() + "my_cell_killer.arch";

        {
            AbstractCellKiller<2>* const p_cell_killer = new MyCellKiller(NULL);

            std::ofstream ofs(archive_filename.c_str());
            boost::archive::text_oarchive output_arch(ofs);

            output_arch << p_cell_killer;
            delete p_cell_killer;
        }

        {
            std::ifstream ifs(archive_filename.c_str(), std::ios::binary);
            boost::archive::text_iarchive input_arch(ifs);

            AbstractCellKiller<2>* p_cell_killer;

            input_arch >> p_cell_killer;
            delete p_cell_killer;
        }
    }
```

### Using the cell killer in a cell-based simulation

We now provide a test demonstrating how `MyCellKiller` can be used
in a cell-based simulation.

```cpp
    void TestOffLatticeSimulationWithMyCellKiller()
    {
```

We proceed as before, creating a mesh-based cell population.

```cpp
        HoneycombMeshGenerator generator(20, 20, 0);
        boost::shared_ptr<MutableMesh<2,2> > p_mesh = generator.GetMesh();

        std::vector<CellPtr> cells;
        CellsGenerator<FixedG1GenerationalCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasic(cells, p_mesh->GetNumNodes());

        MeshBasedCellPopulation<2> cell_population(*p_mesh, cells);
```

We now use the cell population to construct a cell killer object. This object
must be added to the cell-based simulation as a boost::shared_ptr, so we make
use of the macro MAKR_PTR_ARGS (defined in the header `SmartPointers.hpp`).

```cpp
        MAKE_PTR_ARGS(MyCellKiller, p_killer, (&cell_population));
```

We then pass in the cell population into an `OffLatticeSimulation`,
and set the output directory and end time.

```cpp
        OffLatticeSimulation<2> simulator(cell_population);
        simulator.SetOutputDirectory("TestOffLatticeSimulationWithMyCellKiller");
        simulator.SetEndTime(1.0);
```

We create a force law and pass it to the `OffLatticeSimulation`.

```cpp
        MAKE_PTR(GeneralisedLinearSpringForce<2>, p_linear_force);
        p_linear_force->SetCutOffLength(3);
        simulator.AddForce(p_linear_force);
```

We now pass the cell killer into the cell-based simulation.

```cpp
        simulator.AddCellKiller(p_killer);
```

To run the simulation, we call `Solve()`.

```cpp
        simulator.Solve();
    }
```

When you visualize the results with

`java Visualize2dCentreCells /tmp/$USER/testoutput/TestOffLatticeSimulationWithMyCellKiller/results_from_time_0`

you should see that once cells move out of the ellipse they are removed from the simulation.

```cpp
};
```

## Full code

```cpp
#include <cxxtest/TestSuite.h>
#include "CheckpointArchiveTypes.hpp"
#include "AbstractCellBasedTestSuite.hpp"

#include <boost/archive/text_oarchive.hpp>
#include <boost/archive/text_iarchive.hpp>

#include "AbstractCellKiller.hpp"

#include "CellRemovalLocationsWriter.hpp"

#include "HoneycombMeshGenerator.hpp"
#include "FixedG1GenerationalCellCycleModel.hpp"
#include "GeneralisedLinearSpringForce.hpp"
#include "OffLatticeSimulation.hpp"
#include "CellsGenerator.hpp"
#include "SmartPointers.hpp"
//This test is always run sequentially (never in parallel)
#include "FakePetscSetup.hpp"

class MyCellKiller : public AbstractCellKiller<2>
{
private:

    friend class boost::serialization::access;
    template<class Archive>
    void serialize(Archive & archive, const unsigned int version)
    {
        archive & boost::serialization::base_object<AbstractCellKiller<2> >(*this);
    }

public:

    MyCellKiller(AbstractCellPopulation<2>* pCellPopulation)
        : AbstractCellKiller<2>(pCellPopulation)
    {}

    void CheckAndLabelCellsForApoptosisOrDeath()
    {
        for (AbstractCellPopulation<2>::Iterator cell_iter = this->mpCellPopulation->Begin();
            cell_iter != this->mpCellPopulation->End();
            ++cell_iter)
        {
            c_vector<double, 2> location;
            location = this->mpCellPopulation->GetLocationOfCellCentre(*cell_iter);

            if (pow(location[0]/20, 2) + pow(location[1]/10, 2) > 1.0)
            {
                this->mpCellPopulation->KillCell(*cell_iter, "MyCellKiller");
            }
        }
    }

    void OutputCellKillerParameters(out_stream& rParamsFile)
    {
        AbstractCellKiller<2>::OutputCellKillerParameters(rParamsFile);
    }
};

#include "SerializationExportWrapper.hpp"
CHASTE_CLASS_EXPORT(MyCellKiller)
#include "SerializationExportWrapperForCpp.hpp"
CHASTE_CLASS_EXPORT(MyCellKiller)

namespace boost
{
    namespace serialization
    {
        template<class Archive>
        inline void save_construct_data(
            Archive & ar, const MyCellKiller * t, const unsigned int file_version)
        {
            const AbstractCellPopulation<2>* const p_cell_population = t->GetCellPopulation();
            ar << p_cell_population;
        }

        template<class Archive>
        inline void load_construct_data(
            Archive & ar, MyCellKiller * t, const unsigned int file_version)
        {
            AbstractCellPopulation<2>* p_cell_population;
            ar >> p_cell_population;

            // Invoke inplace constructor to initialise instance
            ::new(t)MyCellKiller(p_cell_population);
        }
    }
}

class TestCreatingAndUsingANewCellKillerTutorial : public AbstractCellBasedTestSuite
{
public:

    void TestMyCellKiller()
    {
        HoneycombMeshGenerator generator(20, 20, 0);
        boost::shared_ptr<MutableMesh<2,2> > p_mesh = generator.GetMesh();

        std::vector<CellPtr> cells;
        CellsGenerator<FixedG1GenerationalCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasic(cells, p_mesh->GetNumNodes());

        MeshBasedCellPopulation<2> cell_population(*p_mesh, cells);

        MyCellKiller my_cell_killer(&cell_population);

        cell_population.AddCellPopulationEventWriter<CellRemovalLocationsWriter>();

        my_cell_killer.CheckAndLabelCellsForApoptosisOrDeath();

        for (AbstractCellPopulation<2>::Iterator cell_iter = cell_population.Begin();
             cell_iter != cell_population.End();
             ++cell_iter)
        {
            double x = cell_population.GetLocationOfCellCentre(*cell_iter)[0];
            double y = cell_population.GetLocationOfCellCentre(*cell_iter)[1];

            if (pow(x/20, 2) + pow(y/10, 2) > 1.0)
            {
                TS_ASSERT_EQUALS(cell_iter->IsDead(), true);
            }
            else
            {
                TS_ASSERT_EQUALS(cell_iter->IsDead(), false);
            }
        }

        cell_population.RemoveDeadCells();

        for (AbstractCellPopulation<2>::Iterator cell_iter = cell_population.Begin();
             cell_iter != cell_population.End();
             ++cell_iter)
        {
            double x = cell_population.GetLocationOfCellCentre(*cell_iter)[0];
            double y = cell_population.GetLocationOfCellCentre(*cell_iter)[1];

            TS_ASSERT_LESS_THAN_EQUALS(pow(x/20, 2) + pow(y/10, 2) > 1.0, 1.0);
        }

        OutputFileHandler handler("archive", false);
        std::string archive_filename = handler.GetOutputDirectoryFullPath() + "my_cell_killer.arch";

        {
            AbstractCellKiller<2>* const p_cell_killer = new MyCellKiller(NULL);

            std::ofstream ofs(archive_filename.c_str());
            boost::archive::text_oarchive output_arch(ofs);

            output_arch << p_cell_killer;
            delete p_cell_killer;
        }

        {
            std::ifstream ifs(archive_filename.c_str(), std::ios::binary);
            boost::archive::text_iarchive input_arch(ifs);

            AbstractCellKiller<2>* p_cell_killer;

            input_arch >> p_cell_killer;
            delete p_cell_killer;
        }
    }

    void TestOffLatticeSimulationWithMyCellKiller()
    {
        HoneycombMeshGenerator generator(20, 20, 0);
        boost::shared_ptr<MutableMesh<2,2> > p_mesh = generator.GetMesh();

        std::vector<CellPtr> cells;
        CellsGenerator<FixedG1GenerationalCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasic(cells, p_mesh->GetNumNodes());

        MeshBasedCellPopulation<2> cell_population(*p_mesh, cells);

        MAKE_PTR_ARGS(MyCellKiller, p_killer, (&cell_population));

        OffLatticeSimulation<2> simulator(cell_population);
        simulator.SetOutputDirectory("TestOffLatticeSimulationWithMyCellKiller");
        simulator.SetEndTime(1.0);

        MAKE_PTR(GeneralisedLinearSpringForce<2>, p_linear_force);
        p_linear_force->SetCutOffLength(3);
        simulator.AddForce(p_linear_force);

        simulator.AddCellKiller(p_killer);

        simulator.Solve();
    }
};
```
