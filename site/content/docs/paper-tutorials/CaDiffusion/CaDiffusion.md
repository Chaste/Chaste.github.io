---
title: "Ca<sup>2+</sup> Channel Re-localization to Plasma-Membrane Microdomains Strengthens Activation of Ca<sup>2+</sup>-Dependent Nuclear Gene Expression"
draft: false
layout: "single"
paperTutorialTestFile: "https://github.com/Chaste/project_CaDiffusion/blob/2013ec7101a1f24ddab6ec0396a918f597cd1433/test/TestCaDiffusionLiteratePaper.hpp"
---

This tutorial was generated from the file projects/CaDiffusion/test/TestCaDiffusionLiteratePaper.hpp at revision r27328.
Note that the code is given in full at the bottom of the page.


Code to accompany the paper [Samanta et al. 2015](http://dx.doi.org/10.1016/j.celrep.2015.06.018).

### Code Walkthrough

The following wiki page provides a walk-through of the Chaste code
that was used to perform the simulations in this paper.

First we include some header files:


```cpp
#include <cxxtest/TestSuite.h>

#include "GmshMeshReader.hpp"
#include "UblasIncludes.hpp"
//#include "SimpleLinearEllipticSolver.hpp"
#include "SimpleLinearParabolicSolver.hpp"
#include "TetrahedralMesh.hpp"
#include "BoundaryConditionsContainer.hpp"
#include "ConstBoundaryCondition.hpp"
#include "OutputFileHandler.hpp"
#include "RandomNumberGenerator.hpp"

#include "PetscSetupAndFinalize.hpp"
```

#### Set up a diffusion equation with a source term

d[Ca]/dt = D_Ca Laplacian([Ca]) + Q

[Ca] in units of uM
D_Ca = 300 (nm)^2^/us
integral of Q per ion channel's worth of elements over which is to be applied = 2.5133e4 uM / us


```cpp
template <unsigned SPACE_DIM>
class DiffusionEquationWithSourceTerm : public AbstractLinearParabolicPde<SPACE_DIM>
{
private:
    const std::vector<c_vector<double, SPACE_DIM> >& mrChannelLocations;

    /** The elements that are source elements */
    std::vector<std::vector<unsigned> > mElementsEachChannel;

    std::vector<double> mConcentrationSourcePerUnitVolume; // in units of uM / us

public:
    DiffusionEquationWithSourceTerm(AbstractTetrahedralMesh<SPACE_DIM,SPACE_DIM>* pMesh,
                                    const std::vector<c_vector<double, SPACE_DIM> >& rChannelLocations)
     : AbstractLinearParabolicPde<SPACE_DIM>(),
       mrChannelLocations(rChannelLocations)
    {
        // We're going to work out the total volume of the elements that are going to have a source term
        // in them here.
        std::vector<double> source_volumes(mrChannelLocations.size(), 0.0);
        mConcentrationSourcePerUnitVolume.resize(mrChannelLocations.size());
        mElementsEachChannel.resize(mrChannelLocations.size());

        // Make a list of elements that we are going to say are source elements.
        for (typename TetrahedralMesh<SPACE_DIM,SPACE_DIM>::ElementIterator elt_iter = pMesh->GetElementIteratorBegin();
             elt_iter != pMesh->GetElementIteratorEnd();
             ++elt_iter)
        {
            // Decide whether this should be classed as a source element or not.
            c_vector<double, SPACE_DIM> location = elt_iter->CalculateCentroid();

            for (unsigned channel=0; channel < mrChannelLocations.size(); channel++)
            {
                if (norm_2(location-mrChannelLocations[channel]) <= 3.0) // If centroid is within 3nm of channel say it is a source.
                {
                    //std::cout << "Source Element Recorded\n";

                    // Make a note of this element
                    mElementsEachChannel[channel].push_back(elt_iter->GetIndex());

                    // And add its volume to the total volume of source.
                    c_matrix<double, 3, 3> jacob;
                    double det;
                    elt_iter->CalculateJacobian(jacob, det);
                    source_volumes[channel] += elt_iter->GetVolume(det);
                    //std::cout << "Total source volume[" << channel << "] = " << source_volumes[channel] << "\n";
                }
            }
        }
        // This number is magical and should not be changed unless ion current changed.
        const double total_source_required = 2.5133e4; // Fiddly conversion from ionic current in single channel.
        for (unsigned channel=0; channel<mrChannelLocations.size(); channel++)
        {
            mConcentrationSourcePerUnitVolume[channel] = total_source_required / source_volumes[channel];
        }

    }

    double ComputeSourceTerm(const ChastePoint<SPACE_DIM>& rPoint,
                             double u,
                             Element<SPACE_DIM,SPACE_DIM>* pElement)
    {
        for (unsigned channel=0; channel<mElementsEachChannel.size(); channel++)
        {
            if (std::find(mElementsEachChannel[channel].begin(), mElementsEachChannel[channel].end(), pElement->GetIndex())
                != mElementsEachChannel[channel].end())
            {
                return mConcentrationSourcePerUnitVolume[channel];
            }
        }
        return 0.0;
    }
```

The Diffusion constant for calcium is 300 um^2^ / s
This is equivalent to
300 (nm)^2^ / us


```cpp
    c_matrix<double, SPACE_DIM, SPACE_DIM> ComputeDiffusionTerm(const ChastePoint<SPACE_DIM>& rPoint,
                                                                Element<SPACE_DIM,SPACE_DIM>* pElement=NULL)
    {
        const double diffusion_constant = 300; // Units : 3000 (nm)^2/us
        return diffusion_constant*identity_matrix<double>(SPACE_DIM);
    }

    double ComputeDuDtCoefficientFunction(const ChastePoint<SPACE_DIM>& rPoint)
    {
        return 1.0;
    }
};
```

#### Test class and method to look at Calcium diffusion


```cpp
class TestCaDiffusion : public CxxTest::TestSuite
{
public:
```


We will solve
du/dt = div(grad u) + u, in 3d, with boundary conditions Ca=0 on the boundary, and initial
conditions Ca=0.     *

Our units throughout this are:
distance : nanometers nm
time : microseconds us


```cpp
    void TestSolvingDiffusionEquationForCalcium() throw(Exception)
    {

        TetrahedralMesh<3,3> mesh;
```

Either a 3D Disc shaped thing, centred at (0,0,0), radius 10, and height 1.5.
N.B. We're in slightly odd units of 10 nm or 1e-8 m (!)

Note a coarse version of the mesh is provided to test simulations, but the ones in
the paper were run on the refined version included here:


```cpp
        bool disc = true;
        if (disc)
        {

            GmshMeshReader<3,3> gmsh_reader("projects/CaDiffusion/test/meshes/CaDiffusion.msh"); // for accurate solution
            //GmshMeshReader<3,3> gmsh_reader("projects/CaDiffusion/test/meshes/CaDiffusionCoarse.msh"); // for quick estimate
            mesh.ConstructFromMeshReader(gmsh_reader);
        }
```


Or a square slab of membrane we construct on the fly

Create a 20 by 20 by 1.5 mesh in 3D, this time using the
```
[ConstructRegularSlabMesh](https://github.com/Chaste/trac_archive/wiki/Construct-Regular-Slab-Mesh)
```

method on the mesh. The first parameter is the cartesian space-step
and the other three parameters are the width, height and depth of the mesh.


```cpp
        else
        {
            mesh.ConstructRegularSlabMesh(0.25, 20.0, 20.0, 1.5);
            mesh.Translate(-10.0,-10.0,0.0); // Centre it in x-y plane at origin
        }
        mesh.Scale(10,10,10); // To get into units of nm, radius 100nm, height 15nm.
```

Create some ion channel locations

```cpp
        double z_location = 15.0; //nm - on the top / outer membrane.
        std::vector<c_vector<double, 3u> > channel_locations;

        // Create ion channels in a pentagon shape.
        {
            // 6.3 nm is the closest the channel pores could ever get from structures
            // 9.6 nm is a value that was just published (Pemi et al. PNAS (2015) Nanoscale patterning of STIM1 and Orai1 during store-operated Ca entry)
            // 47.5 nm is the mean nearest neighbour
            // 88.5 nm is the mean between any two points (unlikely to be this spread).
            double inter_channel_spacing = 9.6;
            double pentagon_circumradius = (1.0/10.0)*(sqrt(50.0 + 10.0*sqrt(5.0)))*inter_channel_spacing;
            std::cout << "Circumradius = " << pentagon_circumradius << std::endl;

            // co-ordinates of a pentagon's vertices
            double c1 = pentagon_circumradius*(cos(2.0*M_PI/5.0));
            double c2 = pentagon_circumradius*(cos(M_PI/5.0));
            double s1 = pentagon_circumradius*(sin(2.0*M_PI/5.0));
            double s2 = pentagon_circumradius*(sin(4.0*M_PI/5.0));

            c_vector<double, 3u> location;
            location[0] = pentagon_circumradius;
            location[1] = 0.0;
            location[2] = z_location;
            channel_locations.push_back(location);

            location[0] = c1;
            location[1] = s1;
            location[2] = z_location;
            channel_locations.push_back(location);

            location[0] = -c2;
            location[1] = s2;
            location[2] = z_location;
            channel_locations.push_back(location);

            location[0] = -c2;
            location[1] = -s2;
            location[2] = z_location;
            channel_locations.push_back(location);

            location[0] = c1;
            location[1] = -s1;
            location[2] = z_location;
            channel_locations.push_back(location);
        }
```

Create the PDE object (defined above)

```cpp
        DiffusionEquationWithSourceTerm<3u> pde(&mesh, channel_locations);
```

Create a new boundary conditions container and specify u=0.0 on the boundary.

```cpp
        BoundaryConditionsContainer<3u,3u,1u> bcc; // Templated over element dim, space dim, problem dim.

        ConstBoundaryCondition<3u>* p_bc_for_Ca = new ConstBoundaryCondition<3u>(0.0);
        for (TetrahedralMesh<3u,3u>::BoundaryNodeIterator node_iter = mesh.GetBoundaryNodeIteratorBegin();
             node_iter != mesh.GetBoundaryNodeIteratorEnd();
             ++node_iter)
        {
            double x = (*node_iter)->rGetLocation()[0];
            double y = (*node_iter)->rGetLocation()[1];
            //double z = (*node_iter)->rGetLocation()[2];

            if (disc)
            {
                // If we are on the rim of the disc
                if (x*x + y*y >= 100*100 - 1e-6)
                {
                    bcc.AddDirichletBoundaryCondition(*node_iter, p_bc_for_Ca, 0);
                }
            }
            else
            {
                // If we are on the edge of a slab
                if (fabs(x+100) < 1e-6 || fabs(x-100) < 1e-6 || fabs(y+100)<1e-6 || fabs(y-100)<1e-6)
                {
                    bcc.AddDirichletBoundaryCondition(*node_iter, p_bc_for_Ca, 0);
                }
            }
        }

        SimpleLinearParabolicSolver<3,3> solver(&mesh, &pde, &bcc);
```

For parabolic problems, initial conditions are also needed. The solver will expect
a PETSc vector, where the i-th entry is the initial solution at node i, to be passed
in. To create this PETSc
```
Vec
```
, we will use a helper function in the
```
[PetscTools](https://chaste.cs.ox.ac.uk/public-docs/classPetscTools.html)
```

class to create a
```
Vec
```
 of size num_nodes, with each entry set to 0.0. Then we
set the initial condition on the solver.

```cpp
        Vec initial_condition = PetscTools::CreateAndSetVec(mesh.GetNumNodes(), 0.0);
        solver.SetInitialCondition(initial_condition);
```

Next define the start time, end time, and timestep, and set them.

```cpp
        double t_start = 0; // micro seconds
        double t_end = 1; // micro seconds
        double dt = 0.001; // micro seconds
        solver.SetTimes(t_start, t_end);
        solver.SetTimeStep(dt);

        solver.SetOutputDirectoryAndPrefix("CaDiffusion/time_dependent","results");
        solver.SetOutputToVtk(true);
        Vec result = solver.Solve();

        // Write a copy of the mesh to examine in a different format.
        TrianglesMeshWriter<3,3> writer("CaDiffusion/mesh", "disc", false);
        writer.WriteFilesUsingMesh(mesh);
```

All PETSc vectors should be destroyed when they are no longer needed.

```cpp
        PetscTools::Destroy(initial_condition);
        PetscTools::Destroy(result);
    }
};
```



## Code
The full code is given below


### File name `TestCaDiffusionLiteratePaper.hpp`


```cpp
#include <cxxtest/TestSuite.h>

#include "GmshMeshReader.hpp"
#include "UblasIncludes.hpp"
//#include "SimpleLinearEllipticSolver.hpp"
#include "SimpleLinearParabolicSolver.hpp"
#include "TetrahedralMesh.hpp"
#include "BoundaryConditionsContainer.hpp"
#include "ConstBoundaryCondition.hpp"
#include "OutputFileHandler.hpp"
#include "RandomNumberGenerator.hpp"

#include "PetscSetupAndFinalize.hpp"

template <unsigned SPACE_DIM>
class DiffusionEquationWithSourceTerm : public AbstractLinearParabolicPde<SPACE_DIM>
{
private:
    const std::vector<c_vector<double, SPACE_DIM> >& mrChannelLocations;

    /** The elements that are source elements */
    std::vector<std::vector<unsigned> > mElementsEachChannel;

    std::vector<double> mConcentrationSourcePerUnitVolume; // in units of uM / us

public:
    DiffusionEquationWithSourceTerm(AbstractTetrahedralMesh<SPACE_DIM,SPACE_DIM>* pMesh,
                                    const std::vector<c_vector<double, SPACE_DIM> >& rChannelLocations)
     : AbstractLinearParabolicPde<SPACE_DIM>(),
       mrChannelLocations(rChannelLocations)
    {
        // We're going to work out the total volume of the elements that are going to have a source term
        // in them here.
        std::vector<double> source_volumes(mrChannelLocations.size(), 0.0);
        mConcentrationSourcePerUnitVolume.resize(mrChannelLocations.size());
        mElementsEachChannel.resize(mrChannelLocations.size());

        // Make a list of elements that we are going to say are source elements.
        for (typename TetrahedralMesh<SPACE_DIM,SPACE_DIM>::ElementIterator elt_iter = pMesh->GetElementIteratorBegin();
             elt_iter != pMesh->GetElementIteratorEnd();
             ++elt_iter)
        {
            // Decide whether this should be classed as a source element or not.
            c_vector<double, SPACE_DIM> location = elt_iter->CalculateCentroid();

            for (unsigned channel=0; channel < mrChannelLocations.size(); channel++)
            {
                if (norm_2(location-mrChannelLocations[channel]) <= 3.0) // If centroid is within 3nm of channel say it is a source.
                {
                    //std::cout << "Source Element Recorded\n";

                    // Make a note of this element
                    mElementsEachChannel[channel].push_back(elt_iter->GetIndex());

                    // And add its volume to the total volume of source.
                    c_matrix<double, 3, 3> jacob;
                    double det;
                    elt_iter->CalculateJacobian(jacob, det);
                    source_volumes[channel] += elt_iter->GetVolume(det);
                    //std::cout << "Total source volume[" << channel << "] = " << source_volumes[channel] << "\n";
                }
            }
        }
        // This number is magical and should not be changed unless ion current changed.
        const double total_source_required = 2.5133e4; // Fiddly conversion from ionic current in single channel.
        for (unsigned channel=0; channel<mrChannelLocations.size(); channel++)
        {
            mConcentrationSourcePerUnitVolume[channel] = total_source_required / source_volumes[channel];
        }

    }

    double ComputeSourceTerm(const ChastePoint<SPACE_DIM>& rPoint,
                             double u,
                             Element<SPACE_DIM,SPACE_DIM>* pElement)
    {
        for (unsigned channel=0; channel<mElementsEachChannel.size(); channel++)
        {
            if (std::find(mElementsEachChannel[channel].begin(), mElementsEachChannel[channel].end(), pElement->GetIndex())
                != mElementsEachChannel[channel].end())
            {
                return mConcentrationSourcePerUnitVolume[channel];
            }
        }
        return 0.0;
    }

    c_matrix<double, SPACE_DIM, SPACE_DIM> ComputeDiffusionTerm(const ChastePoint<SPACE_DIM>& rPoint,
                                                                Element<SPACE_DIM,SPACE_DIM>* pElement=NULL)
    {
        const double diffusion_constant = 300; // Units : 3000 (nm)^2/us
        return diffusion_constant*identity_matrix<double>(SPACE_DIM);
    }

    double ComputeDuDtCoefficientFunction(const ChastePoint<SPACE_DIM>& rPoint)
    {
        return 1.0;
    }
};

class TestCaDiffusion : public CxxTest::TestSuite
{
public:
    void TestSolvingDiffusionEquationForCalcium() throw(Exception)
    {

        TetrahedralMesh<3,3> mesh;

        bool disc = true;
        if (disc)
        {

            GmshMeshReader<3,3> gmsh_reader("projects/CaDiffusion/test/meshes/CaDiffusion.msh"); // for accurate solution
            //GmshMeshReader<3,3> gmsh_reader("projects/CaDiffusion/test/meshes/CaDiffusionCoarse.msh"); // for quick estimate
            mesh.ConstructFromMeshReader(gmsh_reader);
        }
        else
        {
            mesh.ConstructRegularSlabMesh(0.25, 20.0, 20.0, 1.5);
            mesh.Translate(-10.0,-10.0,0.0); // Centre it in x-y plane at origin
        }
        mesh.Scale(10,10,10); // To get into units of nm, radius 100nm, height 15nm.

        double z_location = 15.0; //nm - on the top / outer membrane.
        std::vector<c_vector<double, 3u> > channel_locations;

        // Create ion channels in a pentagon shape.
        {
            // 6.3 nm is the closest the channel pores could ever get from structures
            // 9.6 nm is a value that was just published (Pemi et al. PNAS (2015) Nanoscale patterning of STIM1 and Orai1 during store-operated Ca entry)
            // 47.5 nm is the mean nearest neighbour
            // 88.5 nm is the mean between any two points (unlikely to be this spread).
            double inter_channel_spacing = 9.6;
            double pentagon_circumradius = (1.0/10.0)*(sqrt(50.0 + 10.0*sqrt(5.0)))*inter_channel_spacing;
            std::cout << "Circumradius = " << pentagon_circumradius << std::endl;

            // co-ordinates of a pentagon's vertices
            double c1 = pentagon_circumradius*(cos(2.0*M_PI/5.0));
            double c2 = pentagon_circumradius*(cos(M_PI/5.0));
            double s1 = pentagon_circumradius*(sin(2.0*M_PI/5.0));
            double s2 = pentagon_circumradius*(sin(4.0*M_PI/5.0));

            c_vector<double, 3u> location;
            location[0] = pentagon_circumradius;
            location[1] = 0.0;
            location[2] = z_location;
            channel_locations.push_back(location);

            location[0] = c1;
            location[1] = s1;
            location[2] = z_location;
            channel_locations.push_back(location);

            location[0] = -c2;
            location[1] = s2;
            location[2] = z_location;
            channel_locations.push_back(location);

            location[0] = -c2;
            location[1] = -s2;
            location[2] = z_location;
            channel_locations.push_back(location);

            location[0] = c1;
            location[1] = -s1;
            location[2] = z_location;
            channel_locations.push_back(location);
        }

        DiffusionEquationWithSourceTerm<3u> pde(&mesh, channel_locations);

        BoundaryConditionsContainer<3u,3u,1u> bcc; // Templated over element dim, space dim, problem dim.

        ConstBoundaryCondition<3u>* p_bc_for_Ca = new ConstBoundaryCondition<3u>(0.0);
        for (TetrahedralMesh<3u,3u>::BoundaryNodeIterator node_iter = mesh.GetBoundaryNodeIteratorBegin();
             node_iter != mesh.GetBoundaryNodeIteratorEnd();
             ++node_iter)
        {
            double x = (*node_iter)->rGetLocation()[0];
            double y = (*node_iter)->rGetLocation()[1];
            //double z = (*node_iter)->rGetLocation()[2];

            if (disc)
            {
                // If we are on the rim of the disc
                if (x*x + y*y >= 100*100 - 1e-6)
                {
                    bcc.AddDirichletBoundaryCondition(*node_iter, p_bc_for_Ca, 0);
                }
            }
            else
            {
                // If we are on the edge of a slab
                if (fabs(x+100) < 1e-6 || fabs(x-100) < 1e-6 || fabs(y+100)<1e-6 || fabs(y-100)<1e-6)
                {
                    bcc.AddDirichletBoundaryCondition(*node_iter, p_bc_for_Ca, 0);
                }
            }
        }

        SimpleLinearParabolicSolver<3,3> solver(&mesh, &pde, &bcc);

        Vec initial_condition = PetscTools::CreateAndSetVec(mesh.GetNumNodes(), 0.0);
        solver.SetInitialCondition(initial_condition);

        double t_start = 0; // micro seconds
        double t_end = 1; // micro seconds
        double dt = 0.001; // micro seconds
        solver.SetTimes(t_start, t_end);
        solver.SetTimeStep(dt);

        solver.SetOutputDirectoryAndPrefix("CaDiffusion/time_dependent","results");
        solver.SetOutputToVtk(true);
        Vec result = solver.Solve();

        // Write a copy of the mesh to examine in a different format.
        TrianglesMeshWriter<3,3> writer("CaDiffusion/mesh", "disc", false);
        writer.WriteFilesUsingMesh(mesh);

        PetscTools::Destroy(initial_condition);
        PetscTools::Destroy(result);
    }
};
```


