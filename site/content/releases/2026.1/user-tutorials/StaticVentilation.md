---
title : "Static Ventilation"
summary: "An example showing how to calculate ventilation distribution in an airway tree for a given flow rate at the trachea"
draft: false
images: []
toc: true
version: "2026.1"
---
This tutorial is automatically generated from [TestStaticVentilationTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/lung/test/tutorials/TestStaticVentilationTutorial.hpp) at revision [7fa8a1fe59f6](https://github.com/Chaste/Chaste/commit/7fa8a1fe59f6d98cbf1cb5cc25a5f4c0fd6f1198). Note that the code is given in full at the bottom of the page.
## An example showing how to calculate ventilation distribution in an airway tree for a given flow rate at the trachea

In this tutorial we demonstrate the use of !MatrixVentilationProblem to calculate airflow distribution in an airway
tree model. Homogeneous pressure boundary conditions are used at the terminals of the tree and a flow boundary condition
is used at the trachea. We demonstrate how to calculate the total bronchial pressure drop at different flow rates.

The usual headers are included

```cpp
#include <cxxtest/TestSuite.h>
#include "TrianglesMeshReader.hpp"
```

!MatrixVentilationProblem does most of the work in calculating a ventilation distribution.

```cpp
#include "MatrixVentilationProblem.hpp"
```

Note that this tutorial only works with UMFPACK or KLU -- we need to warn the user if it's not installed

```cpp
#include "Warnings.hpp"
```

!MatrixVentilationProblem uses the Petsc solver library. This setups up Petsc ready for use.

```cpp
#include "PetscSetupAndFinalize.hpp"
```

Define the test

```cpp
class TestStaticVentilationTutorial : public CxxTest::TestSuite
{
public: // Tests should be public!

    void TestCalculatePressureDrop()
    {
        EXIT_IF_PARALLEL;
```

First we setup a !MatrixVentilationProblem and tell it to load an airway centerline mesh.

Note that the airway centerline  mesh cannot have intermediate nodes/elements within an airway.
Typically intermediate nodes are found in imaging derived airways centerlines. These can be removed
using the !AirwayRemesher class.

### IMPORTANT
See the note below about use of UMFPACK or KLU. If UMFPACK or KLU are not available we use a different (not realistic) airways
mesh.

```cpp
#if defined(LUNG_USE_UMFPACK) || defined(LUNG_USE_KLU)
        MatrixVentilationProblem problem("lung/test/data/simplified_airways", 0u);
#else
        WARNING("Not compiled with UMFPACK or KLU.  Using non-realistic airway tree.");
        MatrixVentilationProblem problem("mesh/test/data/y_branch_3d_mesh", 0u);
#endif
```

Matrix ventilation problem uses SI units but the mesh is specified in mm. This method allows the solver
to handle this discrepancy.

```cpp
        problem.SetMeshInMilliMetres();
```

Airway meshes can have radii defined either on nodes (default) or on edges. Here we tell the solver
that the mesh has radii defined on edges.

```cpp
        problem.SetRadiusOnEdge();
```

The ventilation solver can use different flow models. By default it uses the simplest Poiseuille flow
model. Whilst this is quick to calculate the results are not accurate for high flow rates. Here we
tell the solver to use a more accurate flow model based on Pedley 1970. Whilst this is more accurate
simulations take longer!

```cpp
        problem.SetDynamicResistance();
```

We define some tracheal flow rates to test. The values are specified in m^3/s
These give a range from 10 L/min to 100 L/min.

```cpp
        std::vector<double> flows;
        flows.push_back(0.00017);
        flows.push_back(0.00083);
        flows.push_back(0.00167);
        flows.push_back(0.003);
```

Loop over the tracheal flow rates and solve

```cpp
        for (unsigned i = 0; i < flows.size(); ++i)
        {
```

This sets the boundary conditions: flow at the trachea and homogeneous zero pressure at the terminal airways

```cpp
            problem.SetOutflowFlux(flows[i]);
            problem.SetConstantInflowPressures(0.0);
```

Calculates flow on the tree

```cpp
            problem.Solve();
```

Here we obtain vectors containing the calculated pressures and fluxes at all nodes and elements in the mesh.

```cpp
            std::vector<double> flux, pressure;
            problem.GetSolutionAsFluxesAndPressures(flux, pressure);
```

The vectors can be used to analyse the flow distribution in detail.
However, for this example we just output the total bronchial pressure drop between the trachea and the terminal
airways.

```cpp
            std::cout << "Total bronchial pressure drop for a tracheal flow rate of " << flows[i] << " m^3/s is " << pressure[0] << " Pa.\n";

           // cout << pressure[1] << endl;

        }
    }
```

### IMPORTANT: Using UMFPACK/KLU

Ventilation problems lead to very badly conditioned matrices. Iterative solvers such as GMRES can stall on these
matrices. When running problems on large airway trees it is vital that to change the linear solver to a direct
solver such as UMFPACK or KLU. UMFPACK and KLU are not pre-requisites for installing Chaste, hence this is not (currently)
the default linear solver for ventilation problems.

''UMFPACK or KLU should be considered pre-requisites for large ventilation problems''

To use UMFPACK or KLU, you need to have PETSc installed with UMFPACK/KLU.

To switch on UMFPACK or KLU on within chaste, set "ccflags='-DLUNG_USE_UMFPACK'" or
"ccflags='-DLUNG_USE_KLU'" in your local.py or
open the file `lung/src/ventilation/MatrixVentilationProblem.hpp` and uncomment the line
#define LUNG_USE_UMFPACK near the top of the file.

```cpp
};
```

## Full code

```cpp
#include <cxxtest/TestSuite.h>
#include "TrianglesMeshReader.hpp"

#include "MatrixVentilationProblem.hpp"

#include "Warnings.hpp"

#include "PetscSetupAndFinalize.hpp"

class TestStaticVentilationTutorial : public CxxTest::TestSuite
{
public: // Tests should be public!

    void TestCalculatePressureDrop()
    {
        EXIT_IF_PARALLEL;

#if defined(LUNG_USE_UMFPACK) || defined(LUNG_USE_KLU)
        MatrixVentilationProblem problem("lung/test/data/simplified_airways", 0u);
#else
        WARNING("Not compiled with UMFPACK or KLU.  Using non-realistic airway tree.");
        MatrixVentilationProblem problem("mesh/test/data/y_branch_3d_mesh", 0u);
#endif

        problem.SetMeshInMilliMetres();

        problem.SetRadiusOnEdge();

        problem.SetDynamicResistance();

        std::vector<double> flows;
        flows.push_back(0.00017);
        flows.push_back(0.00083);
        flows.push_back(0.00167);
        flows.push_back(0.003);

        for (unsigned i = 0; i < flows.size(); ++i)
        {
            problem.SetOutflowFlux(flows[i]);
            problem.SetConstantInflowPressures(0.0);

            problem.Solve();

            std::vector<double> flux, pressure;
            problem.GetSolutionAsFluxesAndPressures(flux, pressure);

            std::cout << "Total bronchial pressure drop for a tracheal flow rate of " << flows[i] << " m^3/s is " << pressure[0] << " Pa.\n";

           // cout << pressure[1] << endl;

        }
    }

};
```
