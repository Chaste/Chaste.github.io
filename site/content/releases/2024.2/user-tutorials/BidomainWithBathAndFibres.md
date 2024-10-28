---
title : "Bidomain With Bath And Fibres"
summary: "Running a bidomain simulation with a bath and fibres"
draft: false
images: []
toc: true
version: "2024.2"
---
This tutorial is automatically generated from [TestBidomainWithBathAndFibresTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/tutorials/TestBidomainWithBathAndFibresTutorial.hpp) at revision [0a2ab4e09adf](https://github.com/Chaste/Chaste/commit/0a2ab4e09adf884a22cb443bfb10d94d8efb5ed3). Note that the code is given in full at the bottom of the page.
## Running a bidomain simulation with a bath and fibres

In this tutorial we run a bidomain simulation with both a bath and fibres

We include the same headers as in the previous fibre tutorial

```cpp
#include <cxxtest/TestSuite.h>
#include "BidomainProblem.hpp"
#include "LuoRudy1991BackwardEulerOpt.hpp"
#include "PetscSetupAndFinalize.hpp"
#include "PlaneStimulusCellFactory.hpp"
```

Define the test class as before

```cpp
class TestBidomainWithBathAndFibresTutorial : public CxxTest::TestSuite
{
public:
    void TestSimulation()
    {
        HeartConfig::Instance()->SetSimulationDuration(5.0);  //ms
        HeartConfig::Instance()->SetOutputDirectory("BidomainTutorialWithBathAndFibres");
        HeartConfig::Instance()->SetOutputFilenamePrefix("results");
```

Bath problems seem to require decreased ODE timesteps. We use the
Backward Euler version of the Luo-Rudy model (see below) instead to
improve code performance.

```cpp
        HeartConfig::Instance()->SetOdeTimeStep(0.01);  //ms
```

Use the `PlaneStimulusCellFactory` to define a set of Luo-Rudy cells, in this
case with a Backward Euler solver. We pass the stimulus magnitude as 0.0
as we don't want any stimulated cells.

```cpp
        PlaneStimulusCellFactory<CellLuoRudy1991FromCellMLBackwardEulerOpt,2> cell_factory(0.0);
```

Note that in the previous bath example, a mesh was read in and elements where then set to be
bath elements in the test. With fibres as well, in a bath simulation, it is better to read in a
mesh that has all the information: this mesh has bath elements defined as an extra column in the
.ele file, and a .ortho file which defines the fibre direction for each element. Note that the
.ortho file should include fibre information for bath elements as well, but they won't be used
in the simulation. (The fibres read here are the same 'kinked' fibres as in the previous fibre
tutorial).

```cpp
        HeartConfig::Instance()->SetMeshFileName("mesh/test/data/2D_0_to_1mm_800_elements_bath_sides", cp::media_type::Orthotropic);
```

Set anistropic conductivities.

```cpp
        HeartConfig::Instance()->SetIntracellularConductivities(Create_c_vector(1.75, 0.175));
        HeartConfig::Instance()->SetExtracellularConductivities(Create_c_vector(7.0, 0.7));
```

and now we define the electrodes..

```cpp
        double magnitude = -9.0e3; // uA/cm^2
        double start_time = 0.0;
        double duration = 2; //ms
        HeartConfig::Instance()->SetElectrodeParameters(false, 0, magnitude, start_time, duration);
```

Now create the problem class, using the cell factory and passing
in `true` as the second argument to indicate we are solving a bath
problem, and solve.

```cpp
        BidomainProblem<2> bidomain_problem( &cell_factory, true );
        bidomain_problem.Initialise();
        bidomain_problem.Solve();
    }
};
```

## Full code

```cpp
#include <cxxtest/TestSuite.h>
#include "BidomainProblem.hpp"
#include "LuoRudy1991BackwardEulerOpt.hpp"
#include "PetscSetupAndFinalize.hpp"
#include "PlaneStimulusCellFactory.hpp"

class TestBidomainWithBathAndFibresTutorial : public CxxTest::TestSuite
{
public:
    void TestSimulation()
    {
        HeartConfig::Instance()->SetSimulationDuration(5.0);  //ms
        HeartConfig::Instance()->SetOutputDirectory("BidomainTutorialWithBathAndFibres");
        HeartConfig::Instance()->SetOutputFilenamePrefix("results");

        HeartConfig::Instance()->SetOdeTimeStep(0.01);  //ms

        PlaneStimulusCellFactory<CellLuoRudy1991FromCellMLBackwardEulerOpt,2> cell_factory(0.0);

        HeartConfig::Instance()->SetMeshFileName("mesh/test/data/2D_0_to_1mm_800_elements_bath_sides", cp::media_type::Orthotropic);

        HeartConfig::Instance()->SetIntracellularConductivities(Create_c_vector(1.75, 0.175));
        HeartConfig::Instance()->SetExtracellularConductivities(Create_c_vector(7.0, 0.7));

        double magnitude = -9.0e3; // uA/cm^2
        double start_time = 0.0;
        double duration = 2; //ms
        HeartConfig::Instance()->SetElectrodeParameters(false, 0, magnitude, start_time, duration);

        BidomainProblem<2> bidomain_problem( &cell_factory, true );
        bidomain_problem.Initialise();
        bidomain_problem.Solve();
    }
};
```
