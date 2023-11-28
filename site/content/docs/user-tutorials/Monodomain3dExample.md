---
title : "Monodomain Example"
summary: "3D monodomain example"
draft: false
images: []
toc: true
---
This tutorial is automatically generated from [TestMonodomain3dExampleTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/tutorials/TestMonodomain3dExampleTutorial.hpp) at revision [8081f57380d8](https://github.com/Chaste/Chaste/commit/8081f57380d857b24947a7a4a70e55ddfef322da). Note that the code is given in full at the bottom of the page.
## 3D monodomain example

In this tutorial we show how to run a 3D simulation using the monodomain equation.
To go from monodomain to bidomain or vice versa is trivial, and for 2d to 3d is
also very easy.

First include the headers, `MonodomainProblem` this time.

```cpp
#include <cxxtest/TestSuite.h>
#include "MonodomainProblem.hpp"
#include "LuoRudy1991.hpp"
#include "SimpleStimulus.hpp"
#include "TetrahedralMesh.hpp"
#include "PetscSetupAndFinalize.hpp"
```

Here we define a cell factory that gives stimuli to cells in the block
0<x<0.1, 0<y<0.1, 0<z<0.1. Note that it inherits from `AbstractCardiacCellFactory<3>`
this time (not `<2>`).

```cpp
class BenchmarkCellFactory : public AbstractCardiacCellFactory<3> // <3> here
{
private:
    boost::shared_ptr<SimpleStimulus> mpStimulus;

public:
    BenchmarkCellFactory()
        : AbstractCardiacCellFactory<3>(), // <3> here as well!
          mpStimulus(new SimpleStimulus(-100000.0, 2))
    {
    }

    AbstractCardiacCell* CreateCardiacCellForTissueNode(Node<3>* pNode)
    {
        double x = pNode->rGetLocation()[0];
        double y = pNode->rGetLocation()[1];
        double z = pNode->rGetLocation()[2];

        if ((x<0.1+1e-6) && (y<0.1+1e-6) && (z<0.1+1e-6))
        {
            return new CellLuoRudy1991FromCellML(mpSolver, mpStimulus);
        }
        else
        {
            return new CellLuoRudy1991FromCellML(mpSolver, mpZeroStimulus);
        }
    }
};
```

Now define the test

```cpp
class TestMonodomain3dExampleTutorial : public CxxTest::TestSuite
{
public:
    void TestMonodomain3d()
    {
```

We will auto-generate a mesh this time, and pass it in, rather than
provide a mesh file name. This is how to generate a cuboid mesh with
a given spatial stepsize h.

Using a `DistributedTetrahedralMesh` is faster than `TetrahedralMesh` when running on multiple processes.
However, it permutes the node ordering for output. Most of time time this won't matter, but later in this
test we want to access specific node indices. One method of doing this is to ask `HeartConfig` to use the
original node ordering for the output.

```cpp
        DistributedTetrahedralMesh<3,3> mesh;
        double h=0.02;
        mesh.ConstructRegularSlabMesh(h, 0.8 /*length*/, 0.3 /*width*/, 0.3 /*depth*/);
        HeartConfig::Instance()->SetOutputUsingOriginalNodeOrdering(true);
```

(In 2D the call is identical, but without the depth parameter).

Set the simulation duration, etc, and create an instance of the cell factory.
One thing that should be noted for monodomain problems, the ''intracellular
conductivity'' is used as the monodomain effective conductivity (not a
harmonic mean of intra and extracellular conductivities). So if you want to
alter the monodomain conductivity call
`HeartConfig::Instance()->SetIntracellularConductivities`

```cpp
        HeartConfig::Instance()->SetSimulationDuration(5); //ms
        HeartConfig::Instance()->SetOutputDirectory("Monodomain3dExample");
        HeartConfig::Instance()->SetOutputFilenamePrefix("results");
        HeartConfig::Instance()->SetOdePdeAndPrintingTimeSteps(0.005, 0.01, 0.1);

        BenchmarkCellFactory cell_factory;
```

Now we declare the problem class, `MonodomainProblem<3>` instead of `BidomainProblem<2>`.
The interface for both is the same.

```cpp
        MonodomainProblem<3> monodomain_problem( &cell_factory );
```

If a mesh-file-name hasn't been set using `HeartConfig`, we have to pass in
a mesh using the `SetMesh` method (must be called before `Initialise`).

```cpp
        monodomain_problem.SetMesh(&mesh);
```

By default data for all nodes is output, but for big simulations, sometimes this
might not be required, and the action potential only at certain nodes required.
The following code shows how to output the results at the first, middle and last
nodes, for example. (The output is written to the HDF5 file; regular visualisation output
will be turned off. HDF5 files can be read using Matlab). We are not using this in this
simulation however (hence the boolean being set to false).

```cpp
        bool partial_output = false;
        if (partial_output)
        {
            std::vector<unsigned> nodes_to_be_output;
            nodes_to_be_output.push_back(0);
            nodes_to_be_output.push_back((unsigned)round( (mesh.GetNumNodes()-1)/2 ));
            nodes_to_be_output.push_back(mesh.GetNumNodes()-1);
            monodomain_problem.SetOutputNodes(nodes_to_be_output);
        }
```

`SetWriteInfo` is a useful method that means that the min/max voltage is
printed as the simulation runs (useful for verifying that cells are stimulated
and the wave propagating, for example)

```cpp
        monodomain_problem.SetWriteInfo();
```

Finally, call `Initialise` and `Solve` as before

```cpp
        monodomain_problem.Initialise();
        monodomain_problem.Solve();
```

This part is just to check nothing has accidentally been changed in this example

```cpp
        ReplicatableVector voltage(monodomain_problem.GetSolution());
        TS_ASSERT_DELTA(voltage[0], 34.9032, 1e-2);
    }
};
```

## Full code

```cpp
#include <cxxtest/TestSuite.h>
#include "MonodomainProblem.hpp"
#include "LuoRudy1991.hpp"
#include "SimpleStimulus.hpp"
#include "TetrahedralMesh.hpp"
#include "PetscSetupAndFinalize.hpp"

class BenchmarkCellFactory : public AbstractCardiacCellFactory<3> // <3> here
{
private:
    boost::shared_ptr<SimpleStimulus> mpStimulus;

public:
    BenchmarkCellFactory()
        : AbstractCardiacCellFactory<3>(), // <3> here as well!
          mpStimulus(new SimpleStimulus(-100000.0, 2))
    {
    }

    AbstractCardiacCell* CreateCardiacCellForTissueNode(Node<3>* pNode)
    {
        double x = pNode->rGetLocation()[0];
        double y = pNode->rGetLocation()[1];
        double z = pNode->rGetLocation()[2];

        if ((x<0.1+1e-6) && (y<0.1+1e-6) && (z<0.1+1e-6))
        {
            return new CellLuoRudy1991FromCellML(mpSolver, mpStimulus);
        }
        else
        {
            return new CellLuoRudy1991FromCellML(mpSolver, mpZeroStimulus);
        }
    }
};

class TestMonodomain3dExampleTutorial : public CxxTest::TestSuite
{
public:
    void TestMonodomain3d()
    {
        DistributedTetrahedralMesh<3,3> mesh;
        double h=0.02;
        mesh.ConstructRegularSlabMesh(h, 0.8 /*length*/, 0.3 /*width*/, 0.3 /*depth*/);
        HeartConfig::Instance()->SetOutputUsingOriginalNodeOrdering(true);
        HeartConfig::Instance()->SetSimulationDuration(5); //ms
        HeartConfig::Instance()->SetOutputDirectory("Monodomain3dExample");
        HeartConfig::Instance()->SetOutputFilenamePrefix("results");
        HeartConfig::Instance()->SetOdePdeAndPrintingTimeSteps(0.005, 0.01, 0.1);

        BenchmarkCellFactory cell_factory;

        MonodomainProblem<3> monodomain_problem( &cell_factory );

        monodomain_problem.SetMesh(&mesh);

        bool partial_output = false;
        if (partial_output)
        {
            std::vector<unsigned> nodes_to_be_output;
            nodes_to_be_output.push_back(0);
            nodes_to_be_output.push_back((unsigned)round( (mesh.GetNumNodes()-1)/2 ));
            nodes_to_be_output.push_back(mesh.GetNumNodes()-1);
            monodomain_problem.SetOutputNodes(nodes_to_be_output);
        }

        monodomain_problem.SetWriteInfo();

        monodomain_problem.Initialise();
        monodomain_problem.Solve();

        ReplicatableVector voltage(monodomain_problem.GetSolution());
        TS_ASSERT_DELTA(voltage[0], 34.9032, 1e-2);
    }
};
```
