---
title : "Bidomain With Conductivity Modifier"
summary: "A bidomain simulation with spatially varying conductivities."
draft: false
images: []
toc: true
version: "2024.1"
---
This tutorial is automatically generated from [TestBidomainWithConductivityModifierTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/heart/test/tutorials/TestBidomainWithConductivityModifierTutorial.hpp) at revision [0a2ab4e09adf](https://github.com/Chaste/Chaste/commit/0a2ab4e09adf884a22cb443bfb10d94d8efb5ed3). Note that the code is given in full at the bottom of the page.
## A bidomain simulation with spatially varying conductivities.

Tissue conductivity can be altered in simple (cuboid and ellipsoid) regions using
the `HeartConfig` `SetConductivityHeterogeneities` methods. This tutorial describes a
much more powerful way which lets us change the conductivity of any element arbitrarily
by exploiting the machinery in `AbstractConductivityModifier` (which is normally
used in mechanics simulations for stretch-dependence).

In this example we have cooked up a modifier that:
 * for most elements returns the original conductivity tensor (from `HeartConfig`)
 scaled by some factor, which is different for intracellular or extracellular
 conductivities,
 * but for one particular element returns some constant matrix.
 
The first thing to do is include the usual headers, plus ones for the conductivity
modifier and an example cell factory (not needed if you're using a custom one).

```cpp
#include <cxxtest/TestSuite.h>
#include "BidomainProblem.hpp"
#include "LuoRudy1991.hpp"
#include "PetscSetupAndFinalize.hpp"
#include "DistributedTetrahedralMesh.hpp"
#include "AbstractConductivityModifier.hpp"
#include "ZeroStimulusCellFactory.hpp"
```

Here we define our conductivity modifier. It inherits from the abstract class.
Make sure to use the right element/space dims.

```cpp
class SimpleConductivityModifier : public AbstractConductivityModifier<2,2>
{
```

We'll use a c_matrix called mTensor as "working memory" to hold the returned
modified tensor. This is needed because we return by reference to the problem class,
so we need to make sure the memory isn't overwritten before it's done with.

mSpecialMatrix will be some constant one.

```cpp
private:

    c_matrix<double,2,2> mTensor;
    c_matrix<double,2,2> mSpecialMatrix;

public:
```

The constructor.

In Chaste, all conductivity tensors are diagonal, so if we initialise our "constant
matrix" to zero then we only need to set the diagonal entries in the constructor.
Strange things will happen if the off-diagonal entries aren't zeroed!

```cpp
    SimpleConductivityModifier()
        : AbstractConductivityModifier<2,2>(),
          mSpecialMatrix( zero_matrix<double>(2,2) )
          {
              mSpecialMatrix(0,0) = 3.14;
              mSpecialMatrix(1,1) = 0.707;
          }
```

`rCalculateModifiedConductivityTensor` returns a reference to the "processed" conductivity tensor.

```cpp
    c_matrix<double,2,2>& rCalculateModifiedConductivityTensor(unsigned elementIndex, const c_matrix<double,2,2>& rOriginalConductivity, unsigned domainIndex)
    {
        if (elementIndex == 0)
        {
            // For element 0 let's return the "special matrix", regardless of intra/extracellular.
            return mSpecialMatrix;
        }

        // Otherwise, we change the behaviour depending on the `domainIndex` (intra/extracellular).
        double domain_scaling;
        if (domainIndex == 0)
        {
            domain_scaling = 1.0; // domainIndex==0 implies intracellular
        }
        else
        {
            domain_scaling = 1.5; // domainIndex==1 implies extracellular
        }

        // Modify the current conductivity according to some expression by running along the diagonal,
        // save to the "working memory", and return.
        for ( unsigned i=0; i<2; i++ )
        {
            mTensor(i,i) = domain_scaling*elementIndex*rOriginalConductivity(i,i);
        }
        return mTensor;
    }
};
```

Now the usual test structure.

```cpp
class TestBidomainWithConductivityModifierTutorial : public CxxTest::TestSuite
{
public:
    void TestConductivityModifier()
    {
```

Generate a mesh.

```cpp
        DistributedTetrahedralMesh<2,2> mesh;
        mesh.ConstructRegularSlabMesh(0.5, 1.0, 0.5); // Mesh has 4 elements
```

Here we're using a trivial cell factory for simplicity, but usually you'll provide your own one.
Set up the problem with the factory as usual.

```cpp
        ZeroStimulusCellFactory<CellLuoRudy1991FromCellML,2> cell_factory;
        BidomainProblem<2> bidomain_problem( &cell_factory );
        bidomain_problem.SetMesh( &mesh );
```

We need to apply the modifier directly to the tissue, which comes from the problem, but is only
accessible after `Initialise()`, so let's do that now.

```cpp
        bidomain_problem.Initialise();
        BidomainTissue<2>* p_bidomain_tissue = bidomain_problem.GetBidomainTissue();
```

Get the original conductivity tensor values. We haven't set them using
`HeartConfig->SetIntra/ExtracellularConductivities` so they'll just be the defaults.

The first argument below is the element ID (we just check the first element we own here). The second accesses
the diagonal elements. We just do (0,0), as (1,1) should be the same (no fibre orientation).
Off-diagonal elements will be 0.

As we don't have many elements, when we run on more than two processors some processors
will not own any elements. We only try to access the conductivity tensors if the process
owns at least one element.

We then check that we have the correct (default) conductivity values.

```cpp
        double orig_intra_conductivity_0 = 0.0;
        double orig_extra_conductivity_0 = 0.0;
        if (mesh.GetElementIteratorBegin() != mesh.GetElementIteratorEnd())
        {
            unsigned first_element = mesh.GetElementIteratorBegin()->GetIndex();
            orig_intra_conductivity_0 = p_bidomain_tissue->rGetIntracellularConductivityTensor(first_element)(0,0);
            orig_extra_conductivity_0 = p_bidomain_tissue->rGetExtracellularConductivityTensor(first_element)(0,0);

            TS_ASSERT_DELTA(orig_intra_conductivity_0, 1.75, 1e-9); // hard-coded using default
            TS_ASSERT_DELTA(orig_extra_conductivity_0, 7.0, 1e-9); // hard-coded using default
        }
```

Now we can make the modifier and apply it to the tissue using `SetConductivityModifier`.

```cpp
        SimpleConductivityModifier modifier;
        p_bidomain_tissue->SetConductivityModifier( &modifier );
```

To confirm that the conductivities have changed, let's iterate over all elements owned by this process
and check their conductivity against what we expect.

```cpp
        for (AbstractTetrahedralMesh<2,2>::ElementIterator elt_iter=mesh.GetElementIteratorBegin();
             elt_iter!=mesh.GetElementIteratorEnd();
             ++elt_iter)
        {
            unsigned index = elt_iter->GetIndex();
            if (index == 0u)
            {
                TS_ASSERT_DELTA(p_bidomain_tissue->rGetIntracellularConductivityTensor(0)(0,0), 3.14, 1e-9);
                TS_ASSERT_DELTA(p_bidomain_tissue->rGetExtracellularConductivityTensor(0)(0,0), 3.14, 1e-9);
                TS_ASSERT_DELTA(p_bidomain_tissue->rGetIntracellularConductivityTensor(0)(1,1), 0.707, 1e-9);
                TS_ASSERT_DELTA(p_bidomain_tissue->rGetExtracellularConductivityTensor(0)(1,1), 0.707, 1e-9);
            }
            else
            {
                TS_ASSERT_DELTA(p_bidomain_tissue->rGetIntracellularConductivityTensor(index)(0,0), 1.0*index*orig_intra_conductivity_0, 1e-9);
                TS_ASSERT_DELTA(p_bidomain_tissue->rGetExtracellularConductivityTensor(index)(0,0), 1.5*index*orig_extra_conductivity_0, 1e-9);
            }
        }
    }
};
```

## Full code

```cpp
#include <cxxtest/TestSuite.h>
#include "BidomainProblem.hpp"
#include "LuoRudy1991.hpp"
#include "PetscSetupAndFinalize.hpp"
#include "DistributedTetrahedralMesh.hpp"
#include "AbstractConductivityModifier.hpp"
#include "ZeroStimulusCellFactory.hpp"

class SimpleConductivityModifier : public AbstractConductivityModifier<2,2>
{
private:

    c_matrix<double,2,2> mTensor;
    c_matrix<double,2,2> mSpecialMatrix;

public:
    SimpleConductivityModifier()
        : AbstractConductivityModifier<2,2>(),
          mSpecialMatrix( zero_matrix<double>(2,2) )
          {
              mSpecialMatrix(0,0) = 3.14;
              mSpecialMatrix(1,1) = 0.707;
          }

    c_matrix<double,2,2>& rCalculateModifiedConductivityTensor(unsigned elementIndex, const c_matrix<double,2,2>& rOriginalConductivity, unsigned domainIndex)
    {
        if (elementIndex == 0)
        {
            // For element 0 let's return the "special matrix", regardless of intra/extracellular.
            return mSpecialMatrix;
        }

        // Otherwise, we change the behaviour depending on the `domainIndex` (intra/extracellular).
        double domain_scaling;
        if (domainIndex == 0)
        {
            domain_scaling = 1.0; // domainIndex==0 implies intracellular
        }
        else
        {
            domain_scaling = 1.5; // domainIndex==1 implies extracellular
        }

        // Modify the current conductivity according to some expression by running along the diagonal,
        // save to the "working memory", and return.
        for ( unsigned i=0; i<2; i++ )
        {
            mTensor(i,i) = domain_scaling*elementIndex*rOriginalConductivity(i,i);
        }
        return mTensor;
    }
};

class TestBidomainWithConductivityModifierTutorial : public CxxTest::TestSuite
{
public:
    void TestConductivityModifier()
    {
        DistributedTetrahedralMesh<2,2> mesh;
        mesh.ConstructRegularSlabMesh(0.5, 1.0, 0.5); // Mesh has 4 elements

        ZeroStimulusCellFactory<CellLuoRudy1991FromCellML,2> cell_factory;
        BidomainProblem<2> bidomain_problem( &cell_factory );
        bidomain_problem.SetMesh( &mesh );

        bidomain_problem.Initialise();
        BidomainTissue<2>* p_bidomain_tissue = bidomain_problem.GetBidomainTissue();

        double orig_intra_conductivity_0 = 0.0;
        double orig_extra_conductivity_0 = 0.0;
        if (mesh.GetElementIteratorBegin() != mesh.GetElementIteratorEnd())
        {
            unsigned first_element = mesh.GetElementIteratorBegin()->GetIndex();
            orig_intra_conductivity_0 = p_bidomain_tissue->rGetIntracellularConductivityTensor(first_element)(0,0);
            orig_extra_conductivity_0 = p_bidomain_tissue->rGetExtracellularConductivityTensor(first_element)(0,0);

            TS_ASSERT_DELTA(orig_intra_conductivity_0, 1.75, 1e-9); // hard-coded using default
            TS_ASSERT_DELTA(orig_extra_conductivity_0, 7.0, 1e-9); // hard-coded using default
        }

        SimpleConductivityModifier modifier;
        p_bidomain_tissue->SetConductivityModifier( &modifier );

        for (AbstractTetrahedralMesh<2,2>::ElementIterator elt_iter=mesh.GetElementIteratorBegin();
             elt_iter!=mesh.GetElementIteratorEnd();
             ++elt_iter)
        {
            unsigned index = elt_iter->GetIndex();
            if (index == 0u)
            {
                TS_ASSERT_DELTA(p_bidomain_tissue->rGetIntracellularConductivityTensor(0)(0,0), 3.14, 1e-9);
                TS_ASSERT_DELTA(p_bidomain_tissue->rGetExtracellularConductivityTensor(0)(0,0), 3.14, 1e-9);
                TS_ASSERT_DELTA(p_bidomain_tissue->rGetIntracellularConductivityTensor(0)(1,1), 0.707, 1e-9);
                TS_ASSERT_DELTA(p_bidomain_tissue->rGetExtracellularConductivityTensor(0)(1,1), 0.707, 1e-9);
            }
            else
            {
                TS_ASSERT_DELTA(p_bidomain_tissue->rGetIntracellularConductivityTensor(index)(0,0), 1.0*index*orig_intra_conductivity_0, 1e-9);
                TS_ASSERT_DELTA(p_bidomain_tissue->rGetExtracellularConductivityTensor(index)(0,0), 1.5*index*orig_extra_conductivity_0, 1e-9);
            }
        }
    }
};
```
