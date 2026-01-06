---
title : "Solving More Elasticity Problems"
summary: "Introduction"
draft: false
images: []
toc: true
---
This tutorial is automatically generated from [TestSolvingMoreElasticityProblemsTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/continuum_mechanics/test/TestSolvingMoreElasticityProblemsTutorial.hpp) at revision [7fa8a1fe59f6](https://github.com/Chaste/Chaste/commit/7fa8a1fe59f6d98cbf1cb5cc25a5f4c0fd6f1198). Note that the code is given in full at the bottom of the page.
### Introduction

In this second solid mechanics tutorial, we illustrate some other possibilities: using tractions
that are defined with a function, or tractions that depend on the deformed body (eg normal pressure
boundary conditions), specifying non-zero displacement boundary conditions, and then
displacement boundary conditions only in some directions, and doing compressible solves.

These includes are the same as before

```cpp
#include <cxxtest/TestSuite.h>
#include "TrianglesMeshReader.hpp"
```

The incompressible solver

```cpp
#include "IncompressibleNonlinearElasticitySolver.hpp"
```

An incompressible material law

```cpp
#include "ExponentialMaterialLaw.hpp"
```

These two are specific to compressible problems

```cpp
#include "CompressibleNonlinearElasticitySolver.hpp"
#include "CompressibleMooneyRivlinMaterialLaw.hpp"
```

This include should generally go last to avoid issues on old library versions

```cpp
#include "PetscSetupAndFinalize.hpp"
```

This function is used in the first test

```cpp
c_vector<double,2> MyTraction(c_vector<double,2>& rX, double time)
{
    c_vector<double,2> traction = zero_vector<double>(2);
    traction(0) = rX(0);
    return traction;
}
```

```cpp
class TestSolvingMoreElasticityProblemsTutorial : public CxxTest::TestSuite
{
public:
```

### Incompressible deformation: non-zero displacement boundary conditions, functional tractions

We now consider a more complicated example. We prescribe particular new locations for the nodes
on the Dirichlet boundary, and also show how to prescribe a traction that is given in functional form
rather than prescribed for each boundary element.

```cpp
    void TestIncompressibleProblemMoreComplicatedExample()
    {
```

Create a mesh

```cpp
        QuadraticMesh<2> mesh;
        mesh.ConstructRegularSlabMesh(0.1 /*stepsize*/, 1.0 /*width*/, 1.0 /*height*/);
```

Use a different material law this time, an exponential material law.
The material law needs to inherit from `AbstractIncompressibleMaterialLaw`,
and there are a few implemented, see `continuum_mechanics/src/problem/material_laws`

```cpp
        ExponentialMaterialLaw<2> law(1.0, 0.5); // First parameter is 'a', second 'b', in W=a*exp(b(I1-3))
```

Now specify the fixed nodes, and their new locations. Create `std::vector`s for each.

```cpp
        std::vector<unsigned> fixed_nodes;
        std::vector<c_vector<double,2> > locations;
```

Loop over the mesh nodes

```cpp
        for (unsigned i=0; i<mesh.GetNumNodes(); i++)
        {
```

If the node is on the Y=0 surface (the LHS)

```cpp
            if (fabs(mesh.GetNode(i)->rGetLocation()[1]) < 1e-6)
            {
```

Add it to the list of fixed nodes

```cpp
                fixed_nodes.push_back(i);
```

and define a new position x=(X,0.1*X^2^)

```cpp
                c_vector<double,2> new_location;
                double X = mesh.GetNode(i)->rGetLocation()[0];
                new_location(0) = X;
                new_location(1) = 0.1*X*X;
                locations.push_back(new_location);
            }
        }
```

Now collect all the boundary elements on the top surface, as before, except
here we don't create the tractions for each element

```cpp
        std::vector<BoundaryElement<1,2>*> boundary_elems;
        for (TetrahedralMesh<2,2>::BoundaryElementIterator iter = mesh.GetBoundaryElementIteratorBegin();
             iter != mesh.GetBoundaryElementIteratorEnd();
             ++iter)
        {
```

If Y=1, have found a boundary element

```cpp
            if (fabs((*iter)->CalculateCentroid()[1] - 1.0)<1e-6)
            {
                BoundaryElement<1,2>* p_element = *iter;
                boundary_elems.push_back(p_element);
            }
        }
```

Create a problem definition object, and this time calling `SetFixedNodes`
which takes in the new locations of the fixed nodes.

```cpp
        SolidMechanicsProblemDefinition<2> problem_defn(mesh);
        problem_defn.SetMaterialLaw(INCOMPRESSIBLE,&law);
        problem_defn.SetFixedNodes(fixed_nodes, locations);
```

Now call `SetTractionBoundaryConditions`, which takes in a vector of
boundary elements as in the previous test. However this time the second argument
is a *function pointer* (just the name of the function) to a
function returning traction in terms of position (and time [see below]).
This function is defined above, before the tests. It has to take in a `c_vector` (position)
and a double (time), and returns a `c_vector` (traction), and will only be called
using points in the boundary elements being passed in. The function `MyTraction`
(defined above, before the tests) above defines a horizontal traction (ie a shear stress, since it is
applied to the top surface) which increases in magnitude across the object.

```cpp
        problem_defn.SetTractionBoundaryConditions(boundary_elems, MyTraction);
```

Note: You can also call `problem_defn.SetBodyForce(MyBodyForce)`, passing in a function
instead of a vector, although isn't really physically useful, it is only really useful
for constructing problems with exact solutions.

Create the solver as before

```cpp
        IncompressibleNonlinearElasticitySolver<2> solver(mesh,
                                                          problem_defn,
                                                          "IncompressibleElasticityMoreComplicatedExample");
```

Call `Solve()`

```cpp
        solver.Solve();
```

Another quick check

```cpp
        TS_ASSERT_EQUALS(solver.GetNumNewtonIterations(), 6u);
```

Visualise as before.

 **Advanced:** Note that the function `MyTraction` takes in time, which it didn't use. In the above it would have been called
 with t=0. The current time can be set using `SetCurrentTime()`. The idea is that the user may want to solve a
 sequence of static problems with time-dependent tractions (say), for which they should allow `MyTraction` to
 depend on time, and put the solve inside a time-loop, for example:

```cpp
        //for (double t=0; t<T; t+=dt)
        //{
        //    solver.SetCurrentTime(t);
        //    solver.Solve();
        //}
```

In this the current time would be passed through to `MyTraction`

Create Cmgui output

```cpp
        solver.CreateCmguiOutput();
```

This is just to check that nothing has been accidentally changed in this test

```cpp
        TS_ASSERT_DELTA(solver.rGetDeformedPosition()[98](0), 1.4543, 1e-3);
        TS_ASSERT_DELTA(solver.rGetDeformedPosition()[98](1), 0.5638, 1e-3);
    }
```

### Sliding boundary conditions

It is common to require a Dirichlet boundary condition where the displacement/position in one dimension
is fixed, but the displacement/position in the others are free. This can be easily done when
collecting the new locations for the fixed nodes, as shown in the following example. Here, we
take a unit square, apply gravity downward, and suppose the Y=0 surface is like a frictionless boundary,
so that, for the nodes on Y=0, we specify y=0 but leave x free (Here (X,Y)=old position, (x,y)=new position).
(Note though that this wouldn't be enough to uniquely specify the final solution - an arbitrary
translation in the Y direction could be added a solution to obtain another valid solution, so we
fully fix the node at the origin.)

```cpp
    void TestWithSlidingDirichletBoundaryConditions()
    {
        QuadraticMesh<2> mesh;
        mesh.ConstructRegularSlabMesh(0.1 /*stepsize*/, 1.0 /*width*/, 1.0 /*height*/);

        ExponentialMaterialLaw<2> law(1.0, 0.5); // First parameter is 'a', second 'b', in W=a*exp(b(I1-3))
```

Create fixed nodes and locations...

```cpp
        std::vector<unsigned> fixed_nodes;
        std::vector<c_vector<double,2> > locations;
```

Fix node 0 (the node at the origin)

```cpp
        fixed_nodes.push_back(0);
        locations.push_back(zero_vector<double>(2));
```

For the rest, if the node is on the Y=0 surface..

```cpp
        for (unsigned i=1; i<mesh.GetNumNodes(); i++)
        {
            if (fabs(mesh.GetNode(i)->rGetLocation()[1]) < 1e-6)
            {
```

..add it to the list of fixed nodes..

```cpp
                fixed_nodes.push_back(i);
```

..and define y to be 0 but x is fixed

```cpp
                c_vector<double,2> new_location;
                new_location(0) = SolidMechanicsProblemDefinition<2>::FREE;
                new_location(1) = 0.0;
                locations.push_back(new_location);
            }
        }
```

Set the material law and fixed nodes, add some gravity, and solve

```cpp
        SolidMechanicsProblemDefinition<2> problem_defn(mesh);
        problem_defn.SetMaterialLaw(INCOMPRESSIBLE,&law);
        problem_defn.SetFixedNodes(fixed_nodes, locations);
        c_vector<double,2> gravity = zero_vector<double>(2);
        gravity(1) = -0.5;
        problem_defn.SetBodyForce(gravity);

        IncompressibleNonlinearElasticitySolver<2> solver(mesh,
                                                          problem_defn,
                                                          "ElasticitySlidingBcsExample");
        solver.Solve();
        solver.CreateCmguiOutput();
```

Check the node at (1,0) has moved but has stayed on Y=0

```cpp
        TS_ASSERT_LESS_THAN(1.0, solver.rGetDeformedPosition()[10](0));
        TS_ASSERT_DELTA(solver.rGetDeformedPosition()[10](1), 0.0, 1e-3);
    }
```

### Compressible deformation, and other bits and pieces

In this test, we will show the (very minor) changes required to solve a compressible nonlinear
elasticity problem, we will describe and show how to specify 'pressure on deformed body'
boundary conditions, we illustrate how a quadratic mesh can be generated using a linear mesh
input files, and we also illustrate how `Solve()` can be called repeatedly, with loading
changing between the solves.

Note: for other examples of compressible solves, including problems with an exact solution, see the
file `continuum_mechanics/test/TestCompressibleNonlinearElasticitySolver.hpp`

```cpp
    void TestSolvingCompressibleProblem()
    {
```

All mechanics problems must take in quadratic meshes, but the mesh files for
(standard) linear meshes in Triangles/Tetgen can be automatically converted
to quadratic meshes, by simply doing the following. (The mesh loaded here is a disk
centred at the origin with radius 1).

```cpp
        QuadraticMesh<2> mesh;
        TrianglesMeshReader<2,2> reader("mesh/test/data/disk_522_elements");
        mesh.ConstructFromLinearMeshReader(reader);
```

Compressible problems require a compressible material law, ie one that
inherits from `AbstractCompressibleMaterialLaw`. The `CompressibleMooneyRivlinMaterialLaw`
is one such example; instantiate one of these

```cpp
        CompressibleMooneyRivlinMaterialLaw<2> law(1.0, 0.5);
```

For this problem, we fix the nodes on the surface for which Y < -0.9

```cpp
        std::vector<unsigned> fixed_nodes;
        for ( TetrahedralMesh<2,2>::BoundaryNodeIterator iter = mesh.GetBoundaryNodeIteratorBegin();
              iter != mesh.GetBoundaryNodeIteratorEnd();
              ++iter)
        {
            double Y = (*iter)->rGetLocation()[1];
            if (Y < -0.9)
            {
                fixed_nodes.push_back((*iter)->GetIndex());
            }
        }
```

We will (later) apply Neumann boundary conditions to surface elements which lie below Y=0,
and these are collected here. (Minor, subtle, comment: we don't bother here checking Y>-0.9,
so the surface elements collected here include the ones on the Dirichlet boundary. This doesn't
matter as the Dirichlet boundary conditions to the nonlinear system essentially overwrite
an Neumann-related effects).

```cpp
        std::vector<BoundaryElement<1,2>*> boundary_elems;
        for (TetrahedralMesh<2,2>::BoundaryElementIterator iter
              = mesh.GetBoundaryElementIteratorBegin();
            iter != mesh.GetBoundaryElementIteratorEnd();
            ++iter)
        {
           BoundaryElement<1,2>* p_element = *iter;
           if (p_element->CalculateCentroid()[1]<0.0)
           {
               boundary_elems.push_back(p_element);
           }
        }
        assert(boundary_elems.size()>0);
```

Create the problem definition class, and set the law again, this time
stating that the law is compressible

```cpp
        SolidMechanicsProblemDefinition<2> problem_defn(mesh);
        problem_defn.SetMaterialLaw(COMPRESSIBLE,&law);
```

Set the fixed nodes and gravity

```cpp
        problem_defn.SetZeroDisplacementNodes(fixed_nodes);
```

The elasticity solvers have two nonlinear solvers implemented, one hand-coded and one which uses PETSc's SNES
solver. The latter is not the default but can be more robust (and will probably be the default in later
versions). This is how it can be used. (This option can also be called if the compiled binary is run from
the command line (see [Running Binaries From Command Line](/docs/user-guides/running-binaries-from-command-line/))
using the option "-mech_use_snes").

```cpp
        problem_defn.SetSolveUsingSnes();
```

This line tells the solver to output info about the nonlinear solve as it progresses, and can be used with
or without the SNES option above. The corresponding command line option is "-mech_verbose"

```cpp
        problem_defn.SetVerboseDuringSolve();

        c_vector<double,2> gravity;
        gravity(0) = 0;
        gravity(1) = 0.1;
        problem_defn.SetBodyForce(gravity);
```

Declare the compressible solver, which has the same interface as the incompressible
one, and call `Solve()`

```cpp
        CompressibleNonlinearElasticitySolver<2> solver(mesh,
                                                        problem_defn,
                                                        "CompressibleSolidMechanicsExample");
        solver.Solve();
```

Now we call add additional boundary conditions, and call `Solve() again. Firstly: these
Neumann conditions here are not specified traction boundary conditions (such BCs are specified
on the undeformed body), but instead, the (more natural) specification of a pressure
exactly in the *normal direction on the deformed body*. We have to provide a set of boundary
elements of the mesh, and a pressure to act on those elements. The solver will automatically
compute the deformed normal directions on which the pressure acts. Note: with this type of
BC, the ordering of the nodes on the boundary elements needs to be consistent, otherwise some
normals will be computed to be inward and others outward. The solver will check this on the
original mesh and throw an exception if this is not the case. (The required ordering is such that:
in 2D, surface element nodes are ordered anticlockwise (looking at the whole mesh); in 3D, looking
at any surface element from outside the mesh, the three nodes are ordered anticlockwise. (Triangle/tetgen
automatically create boundary elements like this)).

```cpp
        double external_pressure = -0.4; // negative sign => inward pressure
        problem_defn.SetApplyNormalPressureOnDeformedSurface(boundary_elems, external_pressure);
```

Call `Solve()` again, so now solving with fixed nodes, gravity, and pressure. The solution from
the previous solve will be used as the initial guess. Although at the moment the solution from the
previous call to `Solve()` will be over-written, calling `Solve()` repeatedly may be useful for
some problems: sometimes, Newton's method will fail to converge for given force/pressures etc, and it can
be (very) helpful to *increment* the loading. For example, set the gravity to be (0,-9.81/3), solve,
then set it to be (0,-2*9.81/3), solve again, and finally set it to be (0,-9.81) and solve for a
final time

```cpp
        solver.Solve();
        solver.CreateCmguiOutput();
    }
};
```

## Full code

```cpp
#include <cxxtest/TestSuite.h>
#include "TrianglesMeshReader.hpp"
#include "IncompressibleNonlinearElasticitySolver.hpp"
#include "ExponentialMaterialLaw.hpp"
#include "CompressibleNonlinearElasticitySolver.hpp"
#include "CompressibleMooneyRivlinMaterialLaw.hpp"
#include "PetscSetupAndFinalize.hpp"

c_vector<double,2> MyTraction(c_vector<double,2>& rX, double time)
{
    c_vector<double,2> traction = zero_vector<double>(2);
    traction(0) = rX(0);
    return traction;
}

class TestSolvingMoreElasticityProblemsTutorial : public CxxTest::TestSuite
{
public:

    void TestIncompressibleProblemMoreComplicatedExample()
    {
        QuadraticMesh<2> mesh;
        mesh.ConstructRegularSlabMesh(0.1 /*stepsize*/, 1.0 /*width*/, 1.0 /*height*/);

        ExponentialMaterialLaw<2> law(1.0, 0.5); // First parameter is 'a', second 'b', in W=a*exp(b(I1-3))
        std::vector<unsigned> fixed_nodes;
        std::vector<c_vector<double,2> > locations;
        for (unsigned i=0; i<mesh.GetNumNodes(); i++)
        {
            if (fabs(mesh.GetNode(i)->rGetLocation()[1]) < 1e-6)
            {
                fixed_nodes.push_back(i);
                c_vector<double,2> new_location;
                double X = mesh.GetNode(i)->rGetLocation()[0];
                new_location(0) = X;
                new_location(1) = 0.1*X*X;
                locations.push_back(new_location);
            }
        }

        std::vector<BoundaryElement<1,2>*> boundary_elems;
        for (TetrahedralMesh<2,2>::BoundaryElementIterator iter = mesh.GetBoundaryElementIteratorBegin();
             iter != mesh.GetBoundaryElementIteratorEnd();
             ++iter)
        {
            if (fabs((*iter)->CalculateCentroid()[1] - 1.0)<1e-6)
            {
                BoundaryElement<1,2>* p_element = *iter;
                boundary_elems.push_back(p_element);
            }
        }

        SolidMechanicsProblemDefinition<2> problem_defn(mesh);
        problem_defn.SetMaterialLaw(INCOMPRESSIBLE,&law);
        problem_defn.SetFixedNodes(fixed_nodes, locations);
        problem_defn.SetTractionBoundaryConditions(boundary_elems, MyTraction);
        IncompressibleNonlinearElasticitySolver<2> solver(mesh,
                                                          problem_defn,
                                                          "IncompressibleElasticityMoreComplicatedExample");

        solver.Solve();

        TS_ASSERT_EQUALS(solver.GetNumNewtonIterations(), 6u);
        //for (double t=0; t<T; t+=dt)
        //{
        //    solver.SetCurrentTime(t);
        //    solver.Solve();
        //}
        solver.CreateCmguiOutput();

        TS_ASSERT_DELTA(solver.rGetDeformedPosition()[98](0), 1.4543, 1e-3);
        TS_ASSERT_DELTA(solver.rGetDeformedPosition()[98](1), 0.5638, 1e-3);
    }

    void TestWithSlidingDirichletBoundaryConditions()
    {
        QuadraticMesh<2> mesh;
        mesh.ConstructRegularSlabMesh(0.1 /*stepsize*/, 1.0 /*width*/, 1.0 /*height*/);

        ExponentialMaterialLaw<2> law(1.0, 0.5); // First parameter is 'a', second 'b', in W=a*exp(b(I1-3))

        std::vector<unsigned> fixed_nodes;
        std::vector<c_vector<double,2> > locations;

        fixed_nodes.push_back(0);
        locations.push_back(zero_vector<double>(2));

        for (unsigned i=1; i<mesh.GetNumNodes(); i++)
        {
            if (fabs(mesh.GetNode(i)->rGetLocation()[1]) < 1e-6)
            {
                fixed_nodes.push_back(i);
                c_vector<double,2> new_location;
                new_location(0) = SolidMechanicsProblemDefinition<2>::FREE;
                new_location(1) = 0.0;
                locations.push_back(new_location);
            }
        }

        SolidMechanicsProblemDefinition<2> problem_defn(mesh);
        problem_defn.SetMaterialLaw(INCOMPRESSIBLE,&law);
        problem_defn.SetFixedNodes(fixed_nodes, locations);
        c_vector<double,2> gravity = zero_vector<double>(2);
        gravity(1) = -0.5;
        problem_defn.SetBodyForce(gravity);

        IncompressibleNonlinearElasticitySolver<2> solver(mesh,
                                                          problem_defn,
                                                          "ElasticitySlidingBcsExample");
        solver.Solve();
        solver.CreateCmguiOutput();

        TS_ASSERT_LESS_THAN(1.0, solver.rGetDeformedPosition()[10](0));
        TS_ASSERT_DELTA(solver.rGetDeformedPosition()[10](1), 0.0, 1e-3);
    }

    void TestSolvingCompressibleProblem()
    {
        QuadraticMesh<2> mesh;
        TrianglesMeshReader<2,2> reader("mesh/test/data/disk_522_elements");
        mesh.ConstructFromLinearMeshReader(reader);

        CompressibleMooneyRivlinMaterialLaw<2> law(1.0, 0.5);

        std::vector<unsigned> fixed_nodes;
        for ( TetrahedralMesh<2,2>::BoundaryNodeIterator iter = mesh.GetBoundaryNodeIteratorBegin();
              iter != mesh.GetBoundaryNodeIteratorEnd();
              ++iter)
        {
            double Y = (*iter)->rGetLocation()[1];
            if (Y < -0.9)
            {
                fixed_nodes.push_back((*iter)->GetIndex());
            }
        }

        std::vector<BoundaryElement<1,2>*> boundary_elems;
        for (TetrahedralMesh<2,2>::BoundaryElementIterator iter
              = mesh.GetBoundaryElementIteratorBegin();
            iter != mesh.GetBoundaryElementIteratorEnd();
            ++iter)
        {
           BoundaryElement<1,2>* p_element = *iter;
           if (p_element->CalculateCentroid()[1]<0.0)
           {
               boundary_elems.push_back(p_element);
           }
        }
        assert(boundary_elems.size()>0);

        SolidMechanicsProblemDefinition<2> problem_defn(mesh);
        problem_defn.SetMaterialLaw(COMPRESSIBLE,&law);

        problem_defn.SetZeroDisplacementNodes(fixed_nodes);

        problem_defn.SetSolveUsingSnes();
        problem_defn.SetVerboseDuringSolve();

        c_vector<double,2> gravity;
        gravity(0) = 0;
        gravity(1) = 0.1;
        problem_defn.SetBodyForce(gravity);

        CompressibleNonlinearElasticitySolver<2> solver(mesh,
                                                        problem_defn,
                                                        "CompressibleSolidMechanicsExample");
        solver.Solve();

        double external_pressure = -0.4; // negative sign => inward pressure
        problem_defn.SetApplyNormalPressureOnDeformedSurface(boundary_elems, external_pressure);
        solver.Solve();
        solver.CreateCmguiOutput();
    }
};
```
