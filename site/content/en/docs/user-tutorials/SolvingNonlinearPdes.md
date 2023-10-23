
---
title : "TestSolvingNonlinearPdesTutorial.hpp"
description: "This tutorial is automatically generated from the file pde/test/tutorials/TestSolvingNonlinearPdesTutorial.hpp at revision [1288aa7fe4cc](https://github.com/Chaste/Chaste/commit/1288aa7fe4ccb5438b05f81253fe167e350cdc10). Note that the code is given in full at the bottom of the page."
draft: false
images: []
toc: true
---

# An example showing how to solve a nonlinear elliptic PDE. Also includes function-based boundary conditions. 

In this tutorial we show how Chaste can be used to solve nonlinear elliptic PDEs.
We will solve the PDE div.(u grad u) + 1 = 0, on a square domain, with boundary
conditions u=0 on y=0; and Neumann boundary conditions: (u grad u).n = 0 on x=0 and x=1;
and (u grad u).n = y on y=1.

For nonlinear PDEs, the finite element equations are of the form F(U)=0, where
U=(U,,1,, , ... , U,,N,,) is a vector of the unknowns at each node, and F is some
non-linear vector valued function. To solve this, a nonlinear solver is required.
Chaste can solve this with Newton's method, or (default) use PETSc's nonlinear solvers.
Solvers of such nonlinear problems usually require the Jacobian of the problem, i.e. the
matrix A = dF/dU, or at least an approximation of the Jacobian.

The following header files need to be included, as in the linear PDEs tutorial.

```cpp
#include <cxxtest/TestSuite.h>
#include "UblasIncludes.hpp"
#include "TrianglesMeshReader.hpp"
#include "TetrahedralMesh.hpp"
#include "BoundaryConditionsContainer.hpp"
#include "ConstBoundaryCondition.hpp"
#include "OutputFileHandler.hpp"
#include "PetscSetupAndFinalize.hpp"
```
This is the solver for nonlinear elliptic PDEs.
```cpp
#include "SimpleNonlinearEllipticSolver.hpp"
```
In this test we also show how to define Neumman boundary conditions which
depend on spatial location, for which the following class is needed.
```cpp
#include "FunctionalBoundaryCondition.hpp"
```
We will choose to use the Chaste Newton solver rather than PETSc's nonlinear
solver.
```cpp
#include "SimpleNewtonNonlinearSolver.hpp"

```
As in the linear PDEs tutorial, we have to define the PDE class we want to
solve (assuming one has not already been created). Nonlinear elliptic PDEs
should inherit from `AbstractNonlinearEllipticPde`{.cpp}, which has five pure
methods which have to be implemented in this concrete class. Here, we define
the PDE div.(u grad u) + 1 = 0.

```cpp
class MyNonlinearPde : public AbstractNonlinearEllipticPde<2>
{
public:

```
The first is the part of the source term that is independent of u.
```cpp
    double ComputeLinearSourceTerm(const ChastePoint<2>& rX)
    {
        return 1.0;
    }

```
The second is the part of the source term that is dependent on u.
```cpp
    double ComputeNonlinearSourceTerm(const ChastePoint<2>& rX, double u)
    {
        return 0.0;
    }

```
The third is the diffusion tensor, which unlike in the linear case can be
dependent on u. The diffusion tensor should be symmetric and positive definite.
```cpp
    c_matrix<double,2,2> ComputeDiffusionTerm(const ChastePoint<2>& rX, double u)
    {
        return identity_matrix<double>(2)*u;
    }

```
We also need to provide the derivatives with respect to u of the last two methods,
so that the Jacobian matrix can be assembled. The derivative of the nonlinear source
term is

```cpp
    double ComputeNonlinearSourceTermPrime(const ChastePoint<2>& , double )
    {
        return 0.0;
    }

```
And the derivative of the diffusion tensor is just the identity matrix.
```cpp
    c_matrix<double,2,2> ComputeDiffusionTermPrime(const ChastePoint<2>& rX, double u)
    {
        return identity_matrix<double>(2);
    }
};

```
We also need to define a (global) function that will become the Neumman boundary
conditions, via the `FunctionalBoundaryCondition`{.cpp} class (see below). This
function is f(x,y) = y.

```cpp
double MyNeummanFunction(const ChastePoint<2>& rX)
{
    return rX[1];
}

```
Next, we define the test suite, as before.
```cpp
class TestSolvingNonlinearPdesTutorial : public CxxTest::TestSuite
{
public:
```
Define a particular test. Note the ``{.cpp} at the end of the
declaration. This causes `Exception`{.cpp} messages to be printed out if an
`Exception`{.cpp} is thrown, rather than just getting the message "terminate
called after throwing an instance of 'Exception' "
```cpp
    void TestSolvingNonlinearEllipticPde()
    {
```
As usual, first create a mesh.
```cpp
        TrianglesMeshReader<2,2> mesh_reader("mesh/test/data/square_128_elements");
        TetrahedralMesh<2,2> mesh;
        mesh.ConstructFromMeshReader(mesh_reader);

```
Next, instantiate the PDE to be solved.
```cpp
        MyNonlinearPde pde;

```
Then we have to define the boundary conditions. First, the Dirichlet boundary
condition, u=0 on x=0, using the boundary node iterator.

```cpp
        BoundaryConditionsContainer<2,2,1> bcc;
        ConstBoundaryCondition<2>* p_zero_bc = new ConstBoundaryCondition<2>(0.0);
        for (TetrahedralMesh<2,2>::BoundaryNodeIterator node_iter = mesh.GetBoundaryNodeIteratorBegin();
             node_iter != mesh.GetBoundaryNodeIteratorEnd();
             node_iter++)
        {
            if (fabs((*node_iter)->GetPoint()[1]) < 1e-12)
            {
                bcc.AddDirichletBoundaryCondition(*node_iter, p_zero_bc);
            }
        }

```
And then the Neumman conditions. Neumann boundary condition are defined on
surface elements, and for this problem, the Neumman boundary value depends
on the position in space, so we make use of the `FunctionalBoundaryCondition`{.cpp}
object, which contains a pointer to a function, and just returns the value
of that function for the required point when the `GetValue`{.cpp} method is called.

```cpp
        FunctionalBoundaryCondition<2>* p_functional_bc = new FunctionalBoundaryCondition<2>(&MyNeummanFunction);
```
Loop over surface elements.
```cpp
        for (TetrahedralMesh<2,2>::BoundaryElementIterator elt_iter = mesh.GetBoundaryElementIteratorBegin();
             elt_iter != mesh.GetBoundaryElementIteratorEnd();
             elt_iter++)
        {
```
Get the y value of any node (here, the zero-th).
```cpp
            double y = (*elt_iter)->GetNodeLocation(0,1);
```
If y=1...
```cpp
            if (fabs(y-1.0) < 1e-12)
            {
```
... then associate the functional boundary condition, (Dgradu).n = y,
with the surface element...
```cpp
                bcc.AddNeumannBoundaryCondition(*elt_iter, p_functional_bc);
            }
            else
            {
```
...else associate the zero boundary condition (i.e. zero flux) with this
element.
```cpp
                bcc.AddNeumannBoundaryCondition(*elt_iter, p_zero_bc);
            }
        }
```
Note that in the above loop, the zero Neumman boundary condition was applied
to all surface elements for which y!=1, which included the Dirichlet surface
y=0. This is OK, as Dirichlet boundary conditions are applied to the finite
element matrix after Neumman boundary conditions, where the appropriate rows
in the matrix are overwritten.

This is the solver for solving nonlinear problems, which, as usual,
takes in the mesh, the PDE, and the boundary conditions.
```cpp
        SimpleNonlinearEllipticSolver<2,2> solver(&mesh, &pde, &bcc);

```
The solver also needs to be given an initial guess, which will be
a PETSc vector. We can make use of a helper method to create it.

```cpp
        Vec initial_guess = PetscTools::CreateAndSetVec(mesh.GetNumNodes(), 0.25);

```
'''Optional:''' To use Chaste's Newton solver to solve nonlinear vector equations that are
assembled, rather than the default PETSc nonlinear solvers, we can
do the following:
```cpp
        SimpleNewtonNonlinearSolver newton_solver;
        solver.SetNonlinearSolver(&newton_solver);
```
'''Optional:''' We can also manually set tolerances, and whether to print statistics, with
this nonlinear vector equation solver
```cpp
        newton_solver.SetTolerance(1e-10);
        newton_solver.SetWriteStats();

```
Now call {{{Solve}}}, passing in the initial guess
```cpp
        Vec answer = solver.Solve(initial_guess);

```
Note that we could have got the solver to not use an analytical Jacobian
and use a numerically-calculated Jacobian instead, by passing in false as a second
parameter:

```cpp
        //Vec answer = solver.Solve(initial_guess, false);

```
Once solved, we can check the obtained solution against the analytical
solution.
```cpp
        ReplicatableVector answer_repl(answer);
        for (unsigned i=0; i<answer_repl.GetSize(); i++)
        {
            double y = mesh.GetNode(i)->GetPoint()[1];
            double exact_u = sqrt(y*(4-y));
            TS_ASSERT_DELTA(answer_repl[i], exact_u, 0.15);
        }

```
Finally, we have to remember to destroy the PETSc {{{Vec}}}s.
```cpp
        PetscTools::Destroy(initial_guess);
        PetscTools::Destroy(answer);
    }
};

```


# Code
The full code is given below


## File name `TestSolvingNonlinearPdesTutorial.hpp` 

```cpp
#include <cxxtest/TestSuite.h>
#include "UblasIncludes.hpp"
#include "TrianglesMeshReader.hpp"
#include "TetrahedralMesh.hpp"
#include "BoundaryConditionsContainer.hpp"
#include "ConstBoundaryCondition.hpp"
#include "OutputFileHandler.hpp"
#include "PetscSetupAndFinalize.hpp"
#include "SimpleNonlinearEllipticSolver.hpp"
#include "FunctionalBoundaryCondition.hpp"
#include "SimpleNewtonNonlinearSolver.hpp"

class MyNonlinearPde : public AbstractNonlinearEllipticPde<2>
{
public:

    double ComputeLinearSourceTerm(const ChastePoint<2>& rX)
    {
        return 1.0;
    }

    double ComputeNonlinearSourceTerm(const ChastePoint<2>& rX, double u)
    {
        return 0.0;
    }

    c_matrix<double,2,2> ComputeDiffusionTerm(const ChastePoint<2>& rX, double u)
    {
        return identity_matrix<double>(2)*u;
    }

    double ComputeNonlinearSourceTermPrime(const ChastePoint<2>& , double )
    {
        return 0.0;
    }

    c_matrix<double,2,2> ComputeDiffusionTermPrime(const ChastePoint<2>& rX, double u)
    {
        return identity_matrix<double>(2);
    }
};

double MyNeummanFunction(const ChastePoint<2>& rX)
{
    return rX[1];
}

class TestSolvingNonlinearPdesTutorial : public CxxTest::TestSuite
{
public:
    void TestSolvingNonlinearEllipticPde()
    {
        TrianglesMeshReader<2,2> mesh_reader("mesh/test/data/square_128_elements");
        TetrahedralMesh<2,2> mesh;
        mesh.ConstructFromMeshReader(mesh_reader);

        MyNonlinearPde pde;

        BoundaryConditionsContainer<2,2,1> bcc;
        ConstBoundaryCondition<2>* p_zero_bc = new ConstBoundaryCondition<2>(0.0);
        for (TetrahedralMesh<2,2>::BoundaryNodeIterator node_iter = mesh.GetBoundaryNodeIteratorBegin();
             node_iter != mesh.GetBoundaryNodeIteratorEnd();
             node_iter++)
        {
            if (fabs((*node_iter)->GetPoint()[1]) < 1e-12)
            {
                bcc.AddDirichletBoundaryCondition(*node_iter, p_zero_bc);
            }
        }

        FunctionalBoundaryCondition<2>* p_functional_bc = new FunctionalBoundaryCondition<2>(&MyNeummanFunction);
        for (TetrahedralMesh<2,2>::BoundaryElementIterator elt_iter = mesh.GetBoundaryElementIteratorBegin();
             elt_iter != mesh.GetBoundaryElementIteratorEnd();
             elt_iter++)
        {
            double y = (*elt_iter)->GetNodeLocation(0,1);
            if (fabs(y-1.0) < 1e-12)
            {
                bcc.AddNeumannBoundaryCondition(*elt_iter, p_functional_bc);
            }
            else
            {
                bcc.AddNeumannBoundaryCondition(*elt_iter, p_zero_bc);
            }
        }
        SimpleNonlinearEllipticSolver<2,2> solver(&mesh, &pde, &bcc);

        Vec initial_guess = PetscTools::CreateAndSetVec(mesh.GetNumNodes(), 0.25);

        SimpleNewtonNonlinearSolver newton_solver;
        solver.SetNonlinearSolver(&newton_solver);
        newton_solver.SetTolerance(1e-10);
        newton_solver.SetWriteStats();

        Vec answer = solver.Solve(initial_guess);

        //Vec answer = solver.Solve(initial_guess, false);

        ReplicatableVector answer_repl(answer);
        for (unsigned i=0; i<answer_repl.GetSize(); i++)
        {
            double y = mesh.GetNode(i)->GetPoint()[1];
            double exact_u = sqrt(y*(4-y));
            TS_ASSERT_DELTA(answer_repl[i], exact_u, 0.15);
        }

        PetscTools::Destroy(initial_guess);
        PetscTools::Destroy(answer);
    }
};

```

