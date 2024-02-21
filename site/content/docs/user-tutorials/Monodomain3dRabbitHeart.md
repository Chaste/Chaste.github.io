---
title : "Monodomain Rabbit Heart"
summary: "3D monodomain rabbit heart example"
draft: false
images: []
toc: true
---
This tutorial is automatically generated from [TestMonodomain3dRabbitHeartTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/tutorials/TestMonodomain3dRabbitHeartTutorial.hpp) at revision [1dfba06b4d82](https://github.com/Chaste/Chaste/commit/1dfba06b4d8265be2322817e6dfe1536071d9a0a). Note that the code is given in full at the bottom of the page.
## 3D monodomain rabbit heart example

This tutorial runs a simulation on a whole rabbit heart mesh. Note that this
mesh is far too coarse for converged simulations, but provides a useful example.

First include the headers, `MonodomainProblem` this time.

```cpp
#include <cxxtest/TestSuite.h>
#include "MonodomainProblem.hpp"
#include "LuoRudy1991BackwardEulerOpt.hpp"
#include "GenericMeshReader.hpp"
#include "SimpleStimulus.hpp"
#include "DistributedTetrahedralMesh.hpp"
#include "PetscSetupAndFinalize.hpp"

/** TEMPORARY FOR DEBUGGING */
///\todo #2739
#include <unistd.h>
#include <sys/resource.h>
//#include "Debug.hpp"
```

Here we define a cell factory that gives stimuli to all cells
below height z = 0.042... this corresponds to the apex of the heart.

```cpp
class RabbitHeartCellFactory : public AbstractCardiacCellFactory<3> // <3> here
{
private:
    boost::shared_ptr<SimpleStimulus> mpStimulus;

public:
    RabbitHeartCellFactory()
        : AbstractCardiacCellFactory<3>(), // <3> here as well!
          mpStimulus(new SimpleStimulus(-80000.0, 2))
    {
    }

    AbstractCardiacCell* CreateCardiacCellForTissueNode(Node<3>* pNode)
    {
        double z = pNode->rGetLocation()[2];

        if (z <= 0.05)
        {
            return new CellLuoRudy1991FromCellMLBackwardEulerOpt(mpSolver, mpStimulus);
        }
        else
        {
            return new CellLuoRudy1991FromCellMLBackwardEulerOpt(mpSolver, mpZeroStimulus);
        }
    }
};
```

Now define the test

```cpp
class TestMonodomain3dRabbitHeartTutorial : public CxxTest::TestSuite
{
public:
    double GetMemoryUsage()
    {
       struct rusage rusage;
       getrusage( RUSAGE_SELF, &rusage );

       return (double)(rusage.ru_maxrss)/(1024);// Convert KB to MB
    }

    void TestMonodomain3dRabbitHeart()
    {
```

```cpp
        HeartConfig::Instance()->SetMeshFileName("apps/texttest/weekly/Propagation3d/OxfordRabbitHeart_482um",
                                                 cp::media_type::Axisymmetric);

//        HeartConfig::Instance()->SetMeshFileName("OxfordRabbitHeart_ascii",
//                                                         cp::media_type::Axisymmetric);
```

Specify the conductivity vector to use in the simulation. Since this is going to be
a monodomain simulation, we only specify intra-cellular conductivities.
Additionally, because this is an Axi-symmetric mesh then we must specify
conductivity along the sheet and normal directions to be the same (an exception will be
thrown if not).

The 3rd entry would be different for an orthotropic mesh with fibre, sheet and
normal directions. For a simulation without fibre directions, there should be one value.

```cpp
        HeartConfig::Instance()->SetIntracellularConductivities(Create_c_vector(1.75, 0.19, 0.19));
```

Set the simulation duration, output directory, filename and VTK visualization.

We have set the simulation duration to be very short here so this tutorial runs
quickly, increase it to see decent propagation of the wavefront.

```cpp
        HeartConfig::Instance()->SetSimulationDuration(2); //ms
        HeartConfig::Instance()->SetOutputDirectory("Monodomain3dRabbitHeart");
        HeartConfig::Instance()->SetOutputFilenamePrefix("results");
        HeartConfig::Instance()->SetVisualizeWithVtk(true);
```

The ODE and PDE timesteps should be refined when using this code for real
scientific simulations. The values here are sufficient to ensure stability
in this case, but not sufficient for converged numerical behaviour.

```cpp
        HeartConfig::Instance()->SetOdePdeAndPrintingTimeSteps(0.02, 0.1, 0.2);
```

Here we create an instance of our cell factory, which will tell the `MonodomainProblem`
class which action potential models to use at which nodes. The rest of the problem is set up
identically to the tutorial [Monodomain 3D Example](../monodomain3dexample/).

```cpp
        RabbitHeartCellFactory cell_factory;
        MonodomainProblem<3> monodomain_problem( &cell_factory );
        monodomain_problem.SetWriteInfo();
        monodomain_problem.Initialise();
        monodomain_problem.Solve();
```

We can access nodes in the mesh using a `NodeIterator`. Here, we check that each node
has not been assigned to bath, and throw an error if it has. This is not a particularly useful test,
but it does demonstrate the principle.

```cpp
        AbstractTetrahedralMesh<3,3>* p_mesh = &(monodomain_problem.rGetMesh());

        /** \todo #2739
        double before_init = GetMemoryUsage();
        monodomain_problem.Initialise();
        double after_init = GetMemoryUsage();
        PRINT_VARIABLE(after_init - before_init);
        */
        for (AbstractTetrahedralMesh<3,3>::NodeIterator iter = p_mesh->GetNodeIteratorBegin();
                         iter != p_mesh->GetNodeIteratorEnd(); ++iter)
        {
            TS_ASSERT_EQUALS(HeartRegionCode::IsRegionBath( iter->GetRegion() ), false);
        }
    }
};
```

 **Note** if you were doing a 'real' scientific simulation you would want to use a higher
 resolution mesh. A version of this can be found on the [http://www.cs.ox.ac.uk/chaste/download.html Chaste download website]
 
Navigate to the "Data" tab, and download either
 * [source:/data/public/OxfordRabbitHeart/OxfordRabbitHeart_binary.tgz OxfordRabbitHeart_binary.tgz]  - 599MB, or
 * [source:/data/public/OxfordRabbitHeart/OxfordRabbitHeartWithBath_binary.tgz OxfordRabbitHeartWithBath_binary.tgz]  - 846MB.
 
These will probably require HPC resources, and finer ODE and PDE time steps than we used here.

To visualize these results, see ChasteGuides/VisualisationGuides/ParaviewForCardiac. The colour axes in Paraview
may need to be rescaled in order to see the voltage changes.

## Full code

```cpp
#include <cxxtest/TestSuite.h>
#include "MonodomainProblem.hpp"
#include "LuoRudy1991BackwardEulerOpt.hpp"
#include "GenericMeshReader.hpp"
#include "SimpleStimulus.hpp"
#include "DistributedTetrahedralMesh.hpp"
#include "PetscSetupAndFinalize.hpp"

/** TEMPORARY FOR DEBUGGING */
///\todo #2739
#include <unistd.h>
#include <sys/resource.h>
//#include "Debug.hpp"

class RabbitHeartCellFactory : public AbstractCardiacCellFactory<3> // <3> here
{
private:
    boost::shared_ptr<SimpleStimulus> mpStimulus;

public:
    RabbitHeartCellFactory()
        : AbstractCardiacCellFactory<3>(), // <3> here as well!
          mpStimulus(new SimpleStimulus(-80000.0, 2))
    {
    }

    AbstractCardiacCell* CreateCardiacCellForTissueNode(Node<3>* pNode)
    {
        double z = pNode->rGetLocation()[2];

        if (z <= 0.05)
        {
            return new CellLuoRudy1991FromCellMLBackwardEulerOpt(mpSolver, mpStimulus);
        }
        else
        {
            return new CellLuoRudy1991FromCellMLBackwardEulerOpt(mpSolver, mpZeroStimulus);
        }
    }
};

class TestMonodomain3dRabbitHeartTutorial : public CxxTest::TestSuite
{
public:
    double GetMemoryUsage()
    {
       struct rusage rusage;
       getrusage( RUSAGE_SELF, &rusage );

       return (double)(rusage.ru_maxrss)/(1024);// Convert KB to MB
    }

    void TestMonodomain3dRabbitHeart()
    {
        HeartConfig::Instance()->SetMeshFileName("apps/texttest/weekly/Propagation3d/OxfordRabbitHeart_482um",
                                                 cp::media_type::Axisymmetric);

//        HeartConfig::Instance()->SetMeshFileName("OxfordRabbitHeart_ascii",
//                                                         cp::media_type::Axisymmetric);

        HeartConfig::Instance()->SetIntracellularConductivities(Create_c_vector(1.75, 0.19, 0.19));

        HeartConfig::Instance()->SetSimulationDuration(2); //ms
        HeartConfig::Instance()->SetOutputDirectory("Monodomain3dRabbitHeart");
        HeartConfig::Instance()->SetOutputFilenamePrefix("results");
        HeartConfig::Instance()->SetVisualizeWithVtk(true);

        HeartConfig::Instance()->SetOdePdeAndPrintingTimeSteps(0.02, 0.1, 0.2);

        RabbitHeartCellFactory cell_factory;
        MonodomainProblem<3> monodomain_problem( &cell_factory );
        monodomain_problem.SetWriteInfo();
        monodomain_problem.Initialise();
        monodomain_problem.Solve();

        AbstractTetrahedralMesh<3,3>* p_mesh = &(monodomain_problem.rGetMesh());

        /** \todo #2739
        double before_init = GetMemoryUsage();
        monodomain_problem.Initialise();
        double after_init = GetMemoryUsage();
        PRINT_VARIABLE(after_init - before_init);
        */
        for (AbstractTetrahedralMesh<3,3>::NodeIterator iter = p_mesh->GetNodeIteratorBegin();
                         iter != p_mesh->GetNodeIteratorEnd(); ++iter)
        {
            TS_ASSERT_EQUALS(HeartRegionCode::IsRegionBath( iter->GetRegion() ), false);
        }
    }
};
```
