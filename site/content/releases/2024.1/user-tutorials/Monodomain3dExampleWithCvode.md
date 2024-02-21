---
title : "Monodomain 3d Example With Cvode"
summary: "3D monodomain example using CVODE for ODE solution"
draft: false
images: []
toc: true
version: "2024.1"
version: "2024.1"
---
This tutorial is automatically generated from [TestMonodomain3dExampleWithCvodeTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/tutorials/TestMonodomain3dExampleWithCvodeTutorial.hpp) at revision [1dfba06b4d82](https://github.com/Chaste/Chaste/commit/1dfba06b4d8265be2322817e6dfe1536071d9a0a). Note that the code is given in full at the bottom of the page.
## 3D monodomain example using CVODE for ODE solution

This tutorial is based on [Monodomain 3D Example](/docs/user-tutorials/monodomain3dexample/) except this time we will
use CVODE solvers. To highlight the changes needed to run with CVODE we omit the usual
explanations of the rest of the code - see [Monodomain 3D Example](/docs/user-tutorials/monodomain3dexample/) for these.

First include the headers

```cpp
#include <cxxtest/TestSuite.h>
#include "MonodomainProblem.hpp"
```

Chaste actually has two ways of using CVODE for solution of cardiac action potential model ODEs:

1. via a `CvodeAdaptor` solver - this would work on the usual cell model as in the previous tutorial.

2. via an `AbstractCvodeCell` instead of an `AbstractCardiacCell` - this class uses native CVODE vectors and is preferred.

In order to generate CVODE cells please see [Code Generation From CellML](/docs/chaste-guides/code-generation-from-cell-ml/).

 **NB:** recent improvements (available from release 2021.1) mean that
 an *analytic jacobian* is automatically made available to CVODE via the
 native `AbstractCvodeCell`, and this will provide a speed up of between 5-30% (depending on the size of
 the ODE system).
 
So here we do the `#include` to import the native CVODE version of the cell model.

```cpp
#include "LuoRudy1991Cvode.hpp"
```

then include the rest of the headers as usual

```cpp
#include "TetrahedralMesh.hpp"
#include "SimpleStimulus.hpp"
#include "PetscSetupAndFinalize.hpp"
```

Since CVODE is an optional extra dependency for Chaste - albeit now
one that is highly recommended - see the [wiki:InstallGuides/InstallGuide InstallGuide].

We guard any code that relies upon it with the following `#ifdef`.
This `CHASTE_CVODE` flag is set automatically by `cmake` during the build process.

```cpp
#ifdef CHASTE_CVODE
```

The major changes required to run with CVODE cells are in the cell factory.

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
```

The following method definition changes to return an `AbstractCvodeCell`
instead of an `AbstractCardiacCell`.

```cpp
    AbstractCvodeCell* CreateCardiacCellForTissueNode(Node<3>* pNode)
    {
        AbstractCvodeCell* p_cell;
```

Purely in order to maintain a consistent interface,
an `AbstractCvodeCell` expects an `AbstractIvpOdeSolver` in its
constructor, but it is not used (CVODE is instead). So an empty
pointer can be passed.

```cpp
        boost::shared_ptr<AbstractIvpOdeSolver> p_empty_solver;

        double x = pNode->rGetLocation()[0];
        double y = pNode->rGetLocation()[1];
        double z = pNode->rGetLocation()[2];
```

We then create a 'native' CVODE cell - each cell has its own solver embedded within it.
Each cell needs its own solver because CVODE saves information about the solver state
between runs to perform its adaptive scheme.

 **NB:** this will use more memory than the standard approach of sharing one solver
 object between all of the action potential models on a processor.

```cpp
        if ((x<0.1+1e-6) && (y<0.1+1e-6) && (z<0.1+1e-6))
        {
            p_cell = new CellLuoRudy1991FromCellMLCvode(p_empty_solver, mpStimulus);
        }
        else
        {
            p_cell = new CellLuoRudy1991FromCellMLCvode(p_empty_solver, mpZeroStimulus);
        }
```

We can also set the tolerances of the ODE solver (in this case,
the method is just setting them to the same as the default, but is shown for completeness).

If you ever get a state variable going out of range with CVODE, then tighten these tolerances .
(but we haven't had that problem with these settings -
that are better than anything but a ridiculously small Forward Euler step).

```cpp
        p_cell->SetTolerances(1e-5,1e-7);

        return p_cell;
    }
};

#endif // CHASTE_CVODE
```

The rest of the test is almost identical to the non-CVODE cell case (just note the `#ifdef` tag).

```cpp
class TestMonodomain3dExampleWithCvodeTutorial : public CxxTest::TestSuite
{
public:
    void TestMonodomain3d()
    {
#ifdef CHASTE_CVODE
        DistributedTetrahedralMesh<3,3> mesh;
        double h=0.02;
        mesh.ConstructRegularSlabMesh(h, 0.8 /*length*/, 0.3 /*width*/, 0.3 /*depth*/);
        HeartConfig::Instance()->SetOutputUsingOriginalNodeOrdering(true);

        HeartConfig::Instance()->SetSimulationDuration(5); //ms
        HeartConfig::Instance()->SetOutputDirectory("Monodomain3dExampleWithCvode");
        HeartConfig::Instance()->SetOutputFilenamePrefix("results");
```

Note - when using CVODE in cardiac tissue simulations the ODE timestep
should be set to the same as the PDE timestep.

CVODE will take as many adaptive internal timesteps as it requires each time
it is called, so we should just call it once per PDE timestep - i.e. set the
ODE and PDE timesteps to be the same.

 **NB**: CVODE will only give you a big speedup when the ODE/PDE timestep is larger than
 a typical Forward Euler timestep would be for that model. But it doesn't
 seem to be any slower than Forward Euler, even at this PDE resolution.
 
A convergence analysis should be performed to ensure that the PDE is being solved
accurately before reducing the step just to get faster ODE solution!

```cpp
        HeartConfig::Instance()->SetOdePdeAndPrintingTimeSteps(0.01, 0.01, 0.1);
```

The rest of the code is unchanged.

```cpp
        BenchmarkCellFactory cell_factory;
        MonodomainProblem<3> monodomain_problem( &cell_factory );
        monodomain_problem.SetMesh( &mesh );

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
```

 **NB**: CVODE almost certainly gives a more accurate ODE solution than
 Forward Euler, so this result has been tweaked from previous tutorial (34.9032mV previously).

```cpp
        TS_ASSERT_DELTA(voltage[0], 34.7740, 1e-1); // Slack tolerance for different CVODE versions.
```

Here we add a visual warning in case CVODE is not installed and/or set up.
If you want to make sure CVODE is run in your own tests you could add in
the `TS_ASSERT(false);` line.

Since CVODE is still optional for Chaste we allow the test to pass without it,
but note that if this is the case, then the test is not doing anything!

```cpp
#else
        std::cout << "CVODE is not installed, or CHASTE is not configured to use it, check your hostconfig settings." << std::endl;
        // TS_ASSERT(false); // uncomment if you want to ensure CVODE is set up on your system.
#endif // CHASTE_CVODE
    }
};
```

## Full code

```cpp
#include <cxxtest/TestSuite.h>
#include "MonodomainProblem.hpp"
#include "LuoRudy1991Cvode.hpp"
#include "TetrahedralMesh.hpp"
#include "SimpleStimulus.hpp"
#include "PetscSetupAndFinalize.hpp"

#ifdef CHASTE_CVODE

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

    AbstractCvodeCell* CreateCardiacCellForTissueNode(Node<3>* pNode)
    {
        AbstractCvodeCell* p_cell;
        boost::shared_ptr<AbstractIvpOdeSolver> p_empty_solver;

        double x = pNode->rGetLocation()[0];
        double y = pNode->rGetLocation()[1];
        double z = pNode->rGetLocation()[2];

        if ((x<0.1+1e-6) && (y<0.1+1e-6) && (z<0.1+1e-6))
        {
            p_cell = new CellLuoRudy1991FromCellMLCvode(p_empty_solver, mpStimulus);
        }
        else
        {
            p_cell = new CellLuoRudy1991FromCellMLCvode(p_empty_solver, mpZeroStimulus);
        }
        p_cell->SetTolerances(1e-5,1e-7);

        return p_cell;
    }
};

#endif // CHASTE_CVODE

class TestMonodomain3dExampleWithCvodeTutorial : public CxxTest::TestSuite
{
public:
    void TestMonodomain3d()
    {
#ifdef CHASTE_CVODE
        DistributedTetrahedralMesh<3,3> mesh;
        double h=0.02;
        mesh.ConstructRegularSlabMesh(h, 0.8 /*length*/, 0.3 /*width*/, 0.3 /*depth*/);
        HeartConfig::Instance()->SetOutputUsingOriginalNodeOrdering(true);

        HeartConfig::Instance()->SetSimulationDuration(5); //ms
        HeartConfig::Instance()->SetOutputDirectory("Monodomain3dExampleWithCvode");
        HeartConfig::Instance()->SetOutputFilenamePrefix("results");

        HeartConfig::Instance()->SetOdePdeAndPrintingTimeSteps(0.01, 0.01, 0.1);

        BenchmarkCellFactory cell_factory;
        MonodomainProblem<3> monodomain_problem( &cell_factory );
        monodomain_problem.SetMesh( &mesh );

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

        TS_ASSERT_DELTA(voltage[0], 34.7740, 1e-1); // Slack tolerance for different CVODE versions.

#else
        std::cout << "CVODE is not installed, or CHASTE is not configured to use it, check your hostconfig settings." << std::endl;
        // TS_ASSERT(false); // uncomment if you want to ensure CVODE is set up on your system.
#endif // CHASTE_CVODE
    }
};
```
