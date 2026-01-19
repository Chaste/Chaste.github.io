---
title: "Cancer cell colonization of a colon crypt"
draft: false
layout: "single"
weight: 2
paperTutorialTestFile: "https://github.com/Chaste/project_CoGNaC/blob/44e32b4e42453762681831e3fa7a84e6b0d41dd4/test/TestCancerCellColonizationOfaColonCryptLiteratePaper.hpp"
---


## Introduction

In this test we show how Chaste can be used to simulate a model of a colon crypt
combining a center-based 2-D representation of cells at the spatial level and a
NRBN-based model underlying gene regulatory network.
Full details of the computational model can be found in
Rubinacci *et al.* (2015).

This class was used to produce Figure 5 and the differentiation tree
in Figure 4.


## Including header files

We begin by including the necessary header files.


```cpp
#include <cxxtest/TestSuite.h>
#include "AbstractCellBasedTestSuite.hpp"

#include <vector>
#include <set>
#include "float.h"
```

The next header defines the NRBN model.

```cpp
#include "ThresholdErgodicSetDifferentiationTree.hpp"
```

The next two headers are used to define a `DifferentiationTree` object.

```cpp
#include "DifferentiationTree.hpp"
#include "DifferentiationTreeNode.hpp"
```

The next header file defines a cell-cycle model which is based
on a `DifferentiationTree` object.

```cpp
#include "DifferentiationTreeBasedWithAsymmetricDivisionCellCycleModel.hpp"
```

The next header file is used in order to visualise the simulation using Paraview.

```cpp
#include "VoronoiDataWriter.hpp"
```

The next header file defines a property named 'Differentiation Colour' used
for visualise distinct cellular types having different colours using Paraview.

```cpp
#include "CellDifferentiationTypeWriter.hpp"
```

The next header file defines a helper class for generating cells.

```cpp
#include "CellsGenerator.hpp"
```

The next header file defines a proliferative type of the cells.

```cpp
#include "StemCellProliferativeType.hpp"
```

The next header file defines a helper class for generating a suitable mesh.

```cpp
#include "HoneycombMeshGenerator.hpp"
```

The next header file defines a fixed duration cell-cycle model class.

```cpp
#include "FixedDurationGenerationBasedCellCycleModel.hpp"
```

The next header file defines a `CellPopulation` class that uses a triangular mesh,
and allows for the inclusion of 'ghost nodes'. These are nodes in the mesh that do
not correspond to cells; instead they help ensure that a sensible Delaunay triangulation
is generated at each timestep. This is because the triangulation algorithm requires a
convex hull.


```cpp
#include "MeshBasedCellPopulationWithGhostNodes.hpp"
```

The next header file defines the class that simulates the evolution of an off-lattice `CellPopulation`

```cpp
#include "OffLatticeSimulation.hpp"
```

The next header file defines a cell killer class, which implements sloughing of cells into
the lumen once they reach the top of the crypt.


```cpp
#include "SloughingCellKiller.hpp"
```

The next header file defines a force law, based on a linear spring, for describing
the mechanical interactions between neighbouring cells in the crypt.


```cpp
#include "GeneralisedLinearSpringForce.hpp"
//This test is always run sequentially (never in parallel)
#include "FakePetscSetup.hpp"
```


## Creating the boundary condition

We create a new cell population boundary condition class to specify a fixed domain within which cells are constrained to lie.
For details, see [this tutorial](https://github.com/Chaste/trac_archive/wiki/User-Tutorials-_-Creating-And-Using-A-New-Cell-Population-Boundary-Condition).

We define a boundary condition for a two-dimensional cell-based simulation, in which all cells are constrained to lie within
the domain given in Cartesian coordinates by 0 <= x <= 20 and y >= 0.


```cpp
class BoundaryConditionWidthAndBottom : public AbstractCellPopulationBoundaryCondition<2>
{
private:

    friend class boost::serialization::access;
    template<class Archive>
    void serialize(Archive & archive, const unsigned int version)
    {
        archive & boost::serialization::base_object<AbstractCellPopulationBoundaryCondition<2> >(*this);
    }

public:
    BoundaryConditionWidthAndBottom(AbstractCellPopulation<2>* pCellPopulation)
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
            double x_coordinate = p_node->rGetLocation()[0];
            double y_coordinate = p_node->rGetLocation()[1];

            if (x_coordinate > 20.0)
            {
                p_node->rGetModifiableLocation()[0] = 20.0;
            }
            else if (x_coordinate < 0.0)
            {
                p_node->rGetModifiableLocation()[0] = 0.0;
            }

            if (y_coordinate < 0.0)
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
            double x_coordinate = cell_location(0);
            double y_coordinate = cell_location(1);

            if ((x_coordinate < 0.0) || (x_coordinate > 20.0))
            {
                condition_satisfied = false;
                break;
            }
            if ((y_coordinate < 0.0))
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
CHASTE_CLASS_EXPORT(BoundaryConditionWidthAndBottom)
#include "SerializationExportWrapperForCpp.hpp"
CHASTE_CLASS_EXPORT(BoundaryConditionWidthAndBottom)

namespace boost
{
    namespace serialization
    {
        template<class Archive>
        inline void save_construct_data(
            Archive & ar, const BoundaryConditionWidthAndBottom * t, const BOOST_PFTO unsigned int file_version)
        {
            const AbstractCellPopulation<2>* const p_cell_population = t->GetCellPopulation();
            ar << p_cell_population;
        }

        template<class Archive>
        inline void load_construct_data(
            Archive & ar, BoundaryConditionWidthAndBottom * t, const unsigned int file_version)
        {
            AbstractCellPopulation<2>* p_cell_population;
            ar >> p_cell_population;

            ::new(t)BoundaryConditionWidthAndBottom(p_cell_population);
        }
    }
}
```


## Testing the cell population boundary condition

First of all, we define the test class.


```cpp
class TestCancerCellColonizationOfaColonCryptLiteratePaper : public AbstractCellBasedTestSuite
{
public:
```

We test that our new cell population boundary
condition is implemented correctly. This test is
very similar to the test implemented in
[this tutorial](https://github.com/Chaste/trac_archive/wiki/User-Tutorials-_-Creating-And-Using-A-New-Cell-Population-Boundary-Condition).


```cpp
    void TestBoundaryCondition() throw(Exception)
    {
        HoneycombMeshGenerator generator(25, 4);
        MutableMesh<2,2>* p_mesh = generator.GetMesh();

        std::vector<CellPtr> cells;
        CellsGenerator<FixedDurationGenerationBasedCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasic(cells, p_mesh->GetNumNodes());

        MeshBasedCellPopulation<2> cell_population(*p_mesh, cells);

        BoundaryConditionWidthAndBottom bc(&cell_population);

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
    }
```


## Testing the properties of the network

Starting from 'fig4_atm.dat' containing a description of the ATN
and the attractors lengths of the network, we calculate a differentiation tree using
the TES theory. Here we test the topological properties of the differentiation
tree and the differentiation probabilities computed.


```cpp
    void TestFigure4NetworkProperties()
    {
```

We start instantiating a `ThresholdErgodicSetDifferentiationTree`
object from an ATN defined in the file `networks_samples/fig4_atn.dat`.


```cpp
        ThresholdErgodicSetDifferentiationTree TES_tree("projects/CoGNaC/networks_samples/fig4_atn.dat");
```

We get the differentiation tree of the network.

```cpp
        DifferentiationTree* diff_tree = TES_tree.getDifferentiationTree();
```

Test the topological properties of the tree.

```cpp
        TS_ASSERT_EQUALS(diff_tree->getRoot()->getNumberOfChildren(), 3u);
        TS_ASSERT_EQUALS(diff_tree->getLeaves().size(), 3u);
        TS_ASSERT_EQUALS(diff_tree->size(), 4u);
        std::vector<std::set<unsigned> > level_nodes = diff_tree->getLevelNodes();

        TS_ASSERT_EQUALS(level_nodes.size(), 2u);
        TS_ASSERT_EQUALS(level_nodes.at(0).size(), 1u);
        TS_ASSERT_EQUALS(level_nodes.at(1).size(), 3u);
```

We want also test the differentiation probabilities associated
to the root node.
We define an array of expected probabilities.

```cpp
        double* test_prob = new double[3];
        test_prob[0] = 0.946185;
        test_prob[1] = 0.0518302;
        test_prob[2] = 0.00198491;
```

We also get the differentiation probabilities from the root node
and we test the size of the vector.

```cpp
        std::vector<double> diff_prob_root = diff_tree->getRoot()->getDifferentiationProbability();
        TS_ASSERT_EQUALS(3u, diff_prob_root.size());
```

Convert the vector into an array.

```cpp
        double* array_diff_probs = &diff_prob_root[0];
```

Sort the array of probabilities in decreasing order.

```cpp
        for (unsigned i=0;i<2;i++)
        {
            for(unsigned j=i+1;j<3;j++)
            {
                if (array_diff_probs[j] > array_diff_probs[i])
                {
                    double temp = array_diff_probs[j];
                    array_diff_probs[j] = array_diff_probs[i];
                    array_diff_probs[i] = temp;
                }
            }
        }
```

Finally, we test that each probability has the correct
value.

```cpp
        for (unsigned i = 0; i<3; ++i)
        {
            TS_ASSERT_DELTA(test_prob[i], array_diff_probs[i], 1e-6);
        }
```

Release the memory.

```cpp
        delete diff_tree;
    }
```


## Simulating a cancer cell colonization (Figure 5)

Starting from 'fig4_atm.dat' containing a description of the ATN
and the attractors lengths, we calculate a differentiation tree using
the TES theory. Then, we use the differentiation tree to drive the
differentiation process during the simulation of a tissue built by
displaying 20 × 20 = 400 hexagonal stem cells at time t = 0
on a 2-D rectangular space with left-hand, right-hand and bottom
closed boundaries.


```cpp
    void TestSimulationCancerCellColonization()
    {
```

We start reseeding the `RandomNumberGenerator`. In
this case it is seeded with the seed zero, but if we
want to show distinct behaviours of the system,  we need
to seed it using a random number.
Two ways are:
`RandomNumberGenerator::Instance()->Reseed(time(NULL))`
where time() returns the number of seconds since January 1970.
`RandomNumberGenerator::Instance()->Reseed(getpid())`
where getpid() returns the system's process ID for the current program.


```cpp
        RandomNumberGenerator::Instance()->Reseed(0);
```

We instantiate a `ThresholdErgodicSetDifferentiationTree`
object from an ATN defined in the file `networks_samples/fig4_atn.dat`.


```cpp
        ThresholdErgodicSetDifferentiationTree TES_tree("projects/CoGNaC/networks_samples/fig4_atn.dat");
```

We get the differentiation tree of the network.

```cpp
        DifferentiationTree* diff_tree = TES_tree.getDifferentiationTree();
```

Save the differentiation tree in a .gml file, in order
to visualise it using graph visualisation tool (e.g. Cytoscape).
Figure 4 - Differentiation Tree.

```cpp
        diff_tree->printDifferentiationTreeToGmlFile("networks_generated","differentiation_tree.gml");
```

Call a method (defined below) which associates a distinct colour to
each node in the tree (cell type).


```cpp
        markLessProbableWithRedColour(diff_tree);
```

We normalise the cell cycle length of each cell type using
the average cell cycle length. In our paper it is indicated
with \Lambda (a NRBN time step corresponds to 0.25 hours).


```cpp
        diff_tree->normaliseLength(8.0);
```

Next, we generate a mutable mesh. To create a

```text
[MutableMesh](https://chaste.cs.ox.ac.uk/public-docs/classMutableMesh.html)
```

, we can use
the

```text
[HoneycombMeshGenerator](https://chaste.cs.ox.ac.uk/public-docs/classHoneycombMeshGenerator.html)
```

. This generates a honeycomb-shaped mesh,
in which all nodes are equidistant. Here the first and second arguments
define the size of the mesh - we have chosen a mesh that is 20 nodes (i.e.
cells) wide, and 20 nodes high. The third argument defines the number of ghost nodes.


```cpp
        HoneycombMeshGenerator generator(20, 20, 4);
        MutableMesh<2,2>* p_mesh = generator.GetMesh();
```

We only want to create cells to attach to real nodes, so we
use the method

```text
[GetCellLocationIndices](https://github.com/Chaste/trac_archive/wiki/Get-Cell-Location-Indices)
```

 to get the indices
of the real nodes in the mesh. This will be passed in to the
cell population later on.


```cpp
        std::vector<unsigned> location_indices = generator.GetCellLocationIndices();
```

Having created a mesh, we now create a

```cpp
std::vector
```

 of

```text
[CellPtr](https://github.com/Chaste/trac_archive/wiki/Cell-Ptr)
```

s.
To do this, we use the `CellsGenerator` helper class again. This time the second
argument is different and is the number of real nodes in the mesh.
All cells have

```text
[StemCellProliferativeType](https://chaste.cs.ox.ac.uk/public-docs/classStemCellProliferativeType.html)
```

.


```cpp
        std::vector<CellPtr> cells;
        MAKE_PTR(StemCellProliferativeType, p_stem_type);
        CellsGenerator<DifferentiationTreeBasedWithAsymmetricDivisionCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasicRandom(cells, location_indices.size(), p_stem_type);
```

Now we need to associate each cell with a

```text
[DifferentiationTreeBasedWithAsymmetricDivisionCellCycleModel](https://github.com/Chaste/trac_archive/wiki/Differentiation-Tree-Based-With-Asymmetric-Division-Cell-Cycle-Model)
```

and initialise it (each instance is different). So, for each cell we
initialise its cell cycle model and randomly set its birthtime.


```cpp
        for (unsigned i=0; i<cells.size(); i++)
        {
            DifferentiationTreeBasedWithAsymmetricDivisionCellCycleModel* p_cell_cycle_model =
                                new DifferentiationTreeBasedWithAsymmetricDivisionCellCycleModel(diff_tree,0);
            CellPtr p_cell = cells.at(i);
            p_cell->SetCellCycleModel(p_cell_cycle_model);
            p_cell->SetBirthTime(-diff_tree->getRoot()->getCellCycleLength()*RandomNumberGenerator::Instance()->ranf());
            p_cell->InitialiseCellCycleModel();
        }
```

Now we have a mesh and a set of cells to go with it, we can create a

```text
[CellPopulation](https://github.com/Chaste/trac_archive/wiki/Cell-Population)
```

.
In general, this class associates a collection of cells with a set of elements or a mesh.
For this test, because we have a

```text
[MutableMesh](https://chaste.cs.ox.ac.uk/public-docs/classMutableMesh.html)
```

, and ghost nodes we use a particular type of
cell population called a

```text
[MeshBasedCellPopulationWithGhostNodes](https://chaste.cs.ox.ac.uk/public-docs/classMeshBasedCellPopulationWithGhostNodes.html)
```

. The third
argument of the constructor takes a vector of the indices of the real nodes and should be the
same length as the vector of cell pointers.


```cpp
        MeshBasedCellPopulationWithGhostNodes<2> cell_population(*p_mesh, cells, location_indices);
```

Add writers used for visualise the simulation using Paraview.

```cpp
        cell_population.AddCellWriter<CellDifferentiationTypeWriter>();
        cell_population.SetWriteVtkAsPoints(false);
        cell_population.AddPopulationWriter<VoronoiDataWriter>();
```

We then pass in the cell population into an

```text
[OffLatticeSimulation](https://chaste.cs.ox.ac.uk/public-docs/classOffLatticeSimulation.html)
```

,
and set the output directory and end time.

```cpp
        OffLatticeSimulation<2> simulator(cell_population);
        simulator.SetOutputDirectory("SimulationCancerCellColonization");
        simulator.SetEndTime(16.0);
```

We create a force law, and pass it to the

```text
[OffLatticeSimulation](https://chaste.cs.ox.ac.uk/public-docs/classOffLatticeSimulation.html)
```

. This
force law ensures that ghost nodes don't exert forces on real nodes but real nodes
exert forces on ghost nodes.

```cpp
        MAKE_PTR(GeneralisedLinearSpringForce<2>, p_linear_force);
        p_linear_force->SetMeinekeSpringStiffness(30.0);
        p_linear_force->SetMeinekeSpringGrowthDuration(0.0);
        simulator.AddForce(p_linear_force);
```

Impose the boundary condition to the cell population object.

```cpp
        MAKE_PTR_ARGS(BoundaryConditionWidthAndBottom, p_bc, (&cell_population));
        simulator.AddCellPopulationBoundaryCondition(p_bc);
```

We also add a cell killer to the simulator. This object dictates under
what conditions cells die. For this test, we use a

```text
[SloughingCellKiller](https://chaste.cs.ox.ac.uk/public-docs/classSloughingCellKiller.html)
```

,
which kills cells above a certain height (passed as an argument to the constructor).


```cpp
        double tissue_height = 17.00;
        MAKE_PTR_ARGS(SloughingCellKiller<2>, p_killer, (&cell_population, tissue_height));
        simulator.AddCellKiller(p_killer);
```

To run the simulation, we call

```text
Solve()
```

. Please note that
in some cases the simulation could fail. The reason is that
cancer cells have a fast replication rate and this can cause
problems at the spatial level (managed by Chaste and not directly
by CoGNaC). In this case you can visualise the simulation until
the timestep which where the problem arise.


```cpp
        simulator.Solve();
```

Release the memory.

```cpp
        delete diff_tree;

    }
```

This method associate a colour to each cell type in a differentiation tree,
marking the less probable to have the highest value (from the range [0,4]).

```cpp
    void markLessProbableWithRedColour(DifferentiationTree* diff_tree)
    {
        diff_tree->setColour(0, 0.0);
        double minimum = DBL_MAX;
        unsigned minimum_index = 0;
        double maximum = 0.0;
        unsigned maximum_index = 0;

        for (unsigned i=1;i<diff_tree->size(); i++)
        {
            if (diff_tree->getNode(i)->getCellCycleLength() < minimum)
            {
                minimum = diff_tree->getNode(i)->getCellCycleLength();
                minimum_index = i;
            }
            if (diff_tree->getNode(i)->getCellCycleLength() > maximum)
            {
                maximum = diff_tree->getNode(i)->getCellCycleLength();
                maximum_index = i;
            }
        }
        if (minimum_index > 0)
        {
            for (unsigned i=1;i<diff_tree->size(); i++)
            {
                if (i == minimum_index)
                {
                    diff_tree->setColour(i, 4.0);
                }
                else if (i == maximum_index)
                {
                    diff_tree->setColour(i, 2.0);
                }
                else diff_tree->setColour(i, 1.0);
            }
        }
    }
```

To visualize the results, we must first open Paraview. We open the folder containing our test output using the 'file' menu at
the top. The output will be located in

```text
/tmp/$USER/testoutput/SimulationCancerCellColonization/results_from_time_0
```

.
There will be a .vtu file generated for every timestep, which must all be opened at once to view the simulation. To do this,
simply select

```text
results.pvd
```

. We should now see

```text
results.pvd
```

  in the pipeline browser. We click

```text
Apply
```

 in the properties tab
of the object inspector, and we should now see a visualization in the right hand window.  (An alternative to opening the

```text
results.pvd
```

file is to open all the time steps en masse where we open

```text
results_..vtu
```

 and see

```text
results_*
```

 appear in the pipeline browser.)

At this stage, it will be necessary to refine how we wish to view this particular visualisation. The viewing styles can be edited using
the display tab of the object inspector. In particular, under

```text
Style
```

, the representation drop down menu allows us to view
the cells as a surface with edges, or as simply a wireframe. It is advisable at this point to familiarize ourselves with the different
viewing options, colour and size settings.

At this stage, the viewer is showing all cells in the simulation, including the ghost nodes. In order to view only real cells, we must
apply a threshold. This is achieved using the threshold button on the third toolbar (the icon is a cube with a green 'T' inside). Once you
click the threshold button, you will see a new threshold appear below your results in the pipeline browser. Go to the properties tab and
reset the lower threshold to be less than 0, and the upper threshold to be between 0 and 1, ensuring that the 'Non-ghosts' option is
selected in the 'Scalars' drop down menu. Once we have edited this, we click apply (we may need to click it twice), and the visualisation on the
right window will have changed to eliminate ghost nodes.

In order to view cells with different colours, we must click in the drop down tab under

```text
Coloring
```

and select 'Differentiation Colour'. Once we have selected this, we click the 'Set Range' button in the

```text
Mapping Data
```

tab (on the right) and set 0 as minimum and 4 as maximum value.

To view the simulation, simply use the animation buttons located on the top toolbar. We can also save a screenshot, or an animation, using
the appropriate options from the file menu.


```cpp
};
```


## Full code

```cpp {title="TestCancerCellColonizationOfaColonCryptLiteratePaper.hpp"}

#include <cxxtest/TestSuite.h>
#include "AbstractCellBasedTestSuite.hpp"

#include <vector>
#include <set>
#include "float.h"

#include "ThresholdErgodicSetDifferentiationTree.hpp"

#include "DifferentiationTree.hpp"
#include "DifferentiationTreeNode.hpp"

#include "DifferentiationTreeBasedWithAsymmetricDivisionCellCycleModel.hpp"

#include "VoronoiDataWriter.hpp"

#include "CellDifferentiationTypeWriter.hpp"

#include "CellsGenerator.hpp"

#include "StemCellProliferativeType.hpp"

#include "HoneycombMeshGenerator.hpp"

#include "FixedDurationGenerationBasedCellCycleModel.hpp"

#include "MeshBasedCellPopulationWithGhostNodes.hpp"

#include "OffLatticeSimulation.hpp"

#include "SloughingCellKiller.hpp"

#include "GeneralisedLinearSpringForce.hpp"
//This test is always run sequentially (never in parallel)
#include "FakePetscSetup.hpp"

class BoundaryConditionWidthAndBottom : public AbstractCellPopulationBoundaryCondition<2>
{
private:

    friend class boost::serialization::access;
    template<class Archive>
    void serialize(Archive & archive, const unsigned int version)
    {
        archive & boost::serialization::base_object<AbstractCellPopulationBoundaryCondition<2> >(*this);
    }

public:
    BoundaryConditionWidthAndBottom(AbstractCellPopulation<2>* pCellPopulation)
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
            double x_coordinate = p_node->rGetLocation()[0];
            double y_coordinate = p_node->rGetLocation()[1];

            if (x_coordinate > 20.0)
            {
                p_node->rGetModifiableLocation()[0] = 20.0;
            }
            else if (x_coordinate < 0.0)
            {
                p_node->rGetModifiableLocation()[0] = 0.0;
            }

            if (y_coordinate < 0.0)
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
            double x_coordinate = cell_location(0);
            double y_coordinate = cell_location(1);

            if ((x_coordinate < 0.0) || (x_coordinate > 20.0))
            {
                condition_satisfied = false;
                break;
            }
            if ((y_coordinate < 0.0))
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
CHASTE_CLASS_EXPORT(BoundaryConditionWidthAndBottom)
#include "SerializationExportWrapperForCpp.hpp"
CHASTE_CLASS_EXPORT(BoundaryConditionWidthAndBottom)

namespace boost
{
    namespace serialization
    {
        template<class Archive>
        inline void save_construct_data(
            Archive & ar, const BoundaryConditionWidthAndBottom * t, const BOOST_PFTO unsigned int file_version)
        {
            const AbstractCellPopulation<2>* const p_cell_population = t->GetCellPopulation();
            ar << p_cell_population;
        }

        template<class Archive>
        inline void load_construct_data(
            Archive & ar, BoundaryConditionWidthAndBottom * t, const unsigned int file_version)
        {
            AbstractCellPopulation<2>* p_cell_population;
            ar >> p_cell_population;

            ::new(t)BoundaryConditionWidthAndBottom(p_cell_population);
        }
    }
}

class TestCancerCellColonizationOfaColonCryptLiteratePaper : public AbstractCellBasedTestSuite
{
public:

    void TestBoundaryCondition() throw(Exception)
    {
        HoneycombMeshGenerator generator(25, 4);
        MutableMesh<2,2>* p_mesh = generator.GetMesh();

        std::vector<CellPtr> cells;
        CellsGenerator<FixedDurationGenerationBasedCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasic(cells, p_mesh->GetNumNodes());

        MeshBasedCellPopulation<2> cell_population(*p_mesh, cells);

        BoundaryConditionWidthAndBottom bc(&cell_population);

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
    }

    void TestFigure4NetworkProperties()
    {
        ThresholdErgodicSetDifferentiationTree TES_tree("projects/CoGNaC/networks_samples/fig4_atn.dat");

        DifferentiationTree* diff_tree = TES_tree.getDifferentiationTree();

        TS_ASSERT_EQUALS(diff_tree->getRoot()->getNumberOfChildren(), 3u);
        TS_ASSERT_EQUALS(diff_tree->getLeaves().size(), 3u);
        TS_ASSERT_EQUALS(diff_tree->size(), 4u);
        std::vector<std::set<unsigned> > level_nodes = diff_tree->getLevelNodes();

        TS_ASSERT_EQUALS(level_nodes.size(), 2u);
        TS_ASSERT_EQUALS(level_nodes.at(0).size(), 1u);
        TS_ASSERT_EQUALS(level_nodes.at(1).size(), 3u);

        double* test_prob = new double[3];
        test_prob[0] = 0.946185;
        test_prob[1] = 0.0518302;
        test_prob[2] = 0.00198491;

        std::vector<double> diff_prob_root = diff_tree->getRoot()->getDifferentiationProbability();
        TS_ASSERT_EQUALS(3u, diff_prob_root.size());

        double* array_diff_probs = &diff_prob_root[0];

        for (unsigned i=0;i<2;i++)
        {
            for(unsigned j=i+1;j<3;j++)
            {
                if (array_diff_probs[j] > array_diff_probs[i])
                {
                    double temp = array_diff_probs[j];
                    array_diff_probs[j] = array_diff_probs[i];
                    array_diff_probs[i] = temp;
                }
            }
        }

        for (unsigned i = 0; i<3; ++i)
        {
            TS_ASSERT_DELTA(test_prob[i], array_diff_probs[i], 1e-6);
        }

        delete diff_tree;
    }

    void TestSimulationCancerCellColonization()
    {
        RandomNumberGenerator::Instance()->Reseed(0);

        ThresholdErgodicSetDifferentiationTree TES_tree("projects/CoGNaC/networks_samples/fig4_atn.dat");

        DifferentiationTree* diff_tree = TES_tree.getDifferentiationTree();

        diff_tree->printDifferentiationTreeToGmlFile("networks_generated","differentiation_tree.gml");

        markLessProbableWithRedColour(diff_tree);

        diff_tree->normaliseLength(8.0);

        HoneycombMeshGenerator generator(20, 20, 4);
        MutableMesh<2,2>* p_mesh = generator.GetMesh();

        std::vector<unsigned> location_indices = generator.GetCellLocationIndices();

        std::vector<CellPtr> cells;
        MAKE_PTR(StemCellProliferativeType, p_stem_type);
        CellsGenerator<DifferentiationTreeBasedWithAsymmetricDivisionCellCycleModel, 2> cells_generator;
        cells_generator.GenerateBasicRandom(cells, location_indices.size(), p_stem_type);

        for (unsigned i=0; i<cells.size(); i++)
        {
            DifferentiationTreeBasedWithAsymmetricDivisionCellCycleModel* p_cell_cycle_model =
                                new DifferentiationTreeBasedWithAsymmetricDivisionCellCycleModel(diff_tree,0);
            CellPtr p_cell = cells.at(i);
            p_cell->SetCellCycleModel(p_cell_cycle_model);
            p_cell->SetBirthTime(-diff_tree->getRoot()->getCellCycleLength()*RandomNumberGenerator::Instance()->ranf());
            p_cell->InitialiseCellCycleModel();
        }

        MeshBasedCellPopulationWithGhostNodes<2> cell_population(*p_mesh, cells, location_indices);

        cell_population.AddCellWriter<CellDifferentiationTypeWriter>();
        cell_population.SetWriteVtkAsPoints(false);
        cell_population.AddPopulationWriter<VoronoiDataWriter>();

        OffLatticeSimulation<2> simulator(cell_population);
        simulator.SetOutputDirectory("SimulationCancerCellColonization");
        simulator.SetEndTime(16.0);

        MAKE_PTR(GeneralisedLinearSpringForce<2>, p_linear_force);
        p_linear_force->SetMeinekeSpringStiffness(30.0);
        p_linear_force->SetMeinekeSpringGrowthDuration(0.0);
        simulator.AddForce(p_linear_force);

        MAKE_PTR_ARGS(BoundaryConditionWidthAndBottom, p_bc, (&cell_population));
        simulator.AddCellPopulationBoundaryCondition(p_bc);

        double tissue_height = 17.00;
        MAKE_PTR_ARGS(SloughingCellKiller<2>, p_killer, (&cell_population, tissue_height));
        simulator.AddCellKiller(p_killer);

        simulator.Solve();

        delete diff_tree;

    }

    void markLessProbableWithRedColour(DifferentiationTree* diff_tree)
    {
        diff_tree->setColour(0, 0.0);
        double minimum = DBL_MAX;
        unsigned minimum_index = 0;
        double maximum = 0.0;
        unsigned maximum_index = 0;

        for (unsigned i=1;i<diff_tree->size(); i++)
        {
            if (diff_tree->getNode(i)->getCellCycleLength() < minimum)
            {
                minimum = diff_tree->getNode(i)->getCellCycleLength();
                minimum_index = i;
            }
            if (diff_tree->getNode(i)->getCellCycleLength() > maximum)
            {
                maximum = diff_tree->getNode(i)->getCellCycleLength();
                maximum_index = i;
            }
        }
        if (minimum_index > 0)
        {
            for (unsigned i=1;i<diff_tree->size(); i++)
            {
                if (i == minimum_index)
                {
                    diff_tree->setColour(i, 4.0);
                }
                else if (i == maximum_index)
                {
                    diff_tree->setColour(i, 2.0);
                }
                else diff_tree->setColour(i, 1.0);
            }
        }
    }

};
```
