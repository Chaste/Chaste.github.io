---
title : "Simple Impedance Problem"
summary: "An example showing how to calculate transfer impedance of an airway tree using a simple impedance model"
draft: false
images: []
toc: true
---
This tutorial is automatically generated from [TestSimpleImpedanceProblemTutorial.hpp](https://github.com/Chaste/Chaste/blob/develop/lung/test/tutorials/TestSimpleImpedanceProblemTutorial.hpp) at revision [0a2ab4e09adf](https://github.com/Chaste/Chaste/commit/0a2ab4e09adf884a22cb443bfb10d94d8efb5ed3). Note that the code is given in full at the bottom of the page.
## An example showing how to calculate transfer impedance of an airway tree using a simple impedance model

In this tutorial we demonstrate the use of !SimpleImpedanceProblem to calculate transfer impedance on an
airway tree model. We further demonstrate post-processing of the output using !ImpedancePostProcessor to
calculate a number of clinically relevant measures.

Note that !SimpleImpedanceProblem uses Poiseuille formulas to calculate impedance
rather than more accurate acoustic impedance equations. For the more accurate version see !ImpedanceProblem.

The usual headers are included

```cpp
#include <cxxtest/TestSuite.h>
#include "TrianglesMeshReader.hpp"
```

!SimpleImpedanceProblem does most of the work in calculating impedance.

```cpp
#include "SimpleImpedanceProblem.hpp"
```

!ImpedancePostProcessor allows easy calculation of a number of clinically relevant measures.

```cpp
#include "ImpedancePostProcessor.hpp"
```

Define the test

```cpp
class TestSimpleImpedanceProblemTutorial : public CxxTest::TestSuite
{
public: // Tests should be public!

    void TestCalculateImpedance()
    {
        EXIT_IF_PARALLEL;
```

First, we load up a mesh containing the centre lines and radii of the a complete conducting airway tree.
The mesh will typically have been developed using a combination of computed tomography (CT) image segmentation
and algorithmic airway generation.

```cpp
        TetrahedralMesh<1,3> mesh;
        TrianglesMeshReader<1,3> mesh_reader("lung/test/data/TestSubject002");
        mesh.ConstructFromMeshReader(mesh_reader);
```

Note that the mesh defined above was developed using a CT scan taken at full inspiration. Impedance is more
commonly recorded during tidal breathing. Here we use a simple scaling to bring the airway radii down into the
tidal breathing range.

```cpp
        for (TetrahedralMesh<1,3>::NodeIterator node_iter = mesh.GetNodeIteratorBegin();
             node_iter != mesh.GetNodeIteratorEnd();
             ++node_iter)
        {
            node_iter->rGetNodeAttributes()[0] *= 0.7;
        }
```

Setup a !SimpleImpedanceProblem and tell it that the given mesh is defined in millimetres

```cpp
        SimpleImpedanceProblem problem(mesh, 0u);
        problem.SetMeshInMilliMetres();
```

This vector lists the input frequencies at which to calculate impedance. They must be
monotonically increasing.

```cpp
        std::vector<double> test_frequencies;
        test_frequencies.push_back(1.0);
        test_frequencies.push_back(2.0);
        test_frequencies.push_back(3.0);
        test_frequencies.push_back(5.0);
        test_frequencies.push_back(10.0);
        test_frequencies.push_back(20.0);
        test_frequencies.push_back(30.0);
        problem.SetFrequencies(test_frequencies);               //Set & get frequencies for coverage
```

The simple impedance model defines a linear spring at each terminal of the airway tree.
This method allows us to set the elastance of the whole lung (in Pa/m^3). This elastance
is then evenly distributed over the terminals.

```cpp
        problem.SetElastance(5.8*98.0665*1e3);
```

Calculates the impedance at the given frequencies

```cpp
        problem.Solve();
```

Get the calculated impedances. The impedance at each frequency is
made up of a real component (the resistance) and a complex component
(the elastance).

```cpp
        std::vector<std::complex<double> > impedances = problem.rGetImpedances();
```

The impedances calculated above could at this stage be written to a file
and plotted. Instead, we make use of !ImpedancePostProcessor to calculate
a number of common clinical summary statistics from the data.

```cpp
        ImpedancePostProcessor processor(test_frequencies, impedances);

        std::cout << "\n";
        std::cout << "R5       = " << real(impedances[3])*1e-6 << " kPa.s.L^-1" << std::endl;
        std::cout << "R20      = " << real(impedances[5])*1e-6 << " kPa.s.L^-1" << std::endl;
        std::cout << "R5 - R20 = " << processor.GetR5MinusR20()*1e-6 << " kPa.s.L^-1" << std::endl;
        std::cout << "Rrs      = " << processor.GetRrs()*1e-6 << " kPa.s.L^-1" << std::endl;
        std::cout << "\n";
        std::cout << "X5       = " << imag(impedances[5])*1e-6 << " kPa.s.L^-1" << std::endl;
        std::cout << "Fres     = " << processor.GetResonantFrequency() << " Hz " << std::endl;
        std::cout << "Ax       = " << processor.GetAx()*1e-6 << " kPa.L^-1" << std::endl;
        std::cout << "\n";
    }
};
```

## Full code

```cpp
#include <cxxtest/TestSuite.h>
#include "TrianglesMeshReader.hpp"

#include "SimpleImpedanceProblem.hpp"

#include "ImpedancePostProcessor.hpp"

class TestSimpleImpedanceProblemTutorial : public CxxTest::TestSuite
{
public: // Tests should be public!

    void TestCalculateImpedance()
    {
        EXIT_IF_PARALLEL;

        TetrahedralMesh<1,3> mesh;
        TrianglesMeshReader<1,3> mesh_reader("lung/test/data/TestSubject002");
        mesh.ConstructFromMeshReader(mesh_reader);

        for (TetrahedralMesh<1,3>::NodeIterator node_iter = mesh.GetNodeIteratorBegin();
             node_iter != mesh.GetNodeIteratorEnd();
             ++node_iter)
        {
            node_iter->rGetNodeAttributes()[0] *= 0.7;
        }

        SimpleImpedanceProblem problem(mesh, 0u);
        problem.SetMeshInMilliMetres();

        std::vector<double> test_frequencies;
        test_frequencies.push_back(1.0);
        test_frequencies.push_back(2.0);
        test_frequencies.push_back(3.0);
        test_frequencies.push_back(5.0);
        test_frequencies.push_back(10.0);
        test_frequencies.push_back(20.0);
        test_frequencies.push_back(30.0);
        problem.SetFrequencies(test_frequencies);               //Set & get frequencies for coverage

        problem.SetElastance(5.8*98.0665*1e3);

        problem.Solve();

        std::vector<std::complex<double> > impedances = problem.rGetImpedances();

        ImpedancePostProcessor processor(test_frequencies, impedances);

        std::cout << "\n";
        std::cout << "R5       = " << real(impedances[3])*1e-6 << " kPa.s.L^-1" << std::endl;
        std::cout << "R20      = " << real(impedances[5])*1e-6 << " kPa.s.L^-1" << std::endl;
        std::cout << "R5 - R20 = " << processor.GetR5MinusR20()*1e-6 << " kPa.s.L^-1" << std::endl;
        std::cout << "Rrs      = " << processor.GetRrs()*1e-6 << " kPa.s.L^-1" << std::endl;
        std::cout << "\n";
        std::cout << "X5       = " << imag(impedances[5])*1e-6 << " kPa.s.L^-1" << std::endl;
        std::cout << "Fres     = " << processor.GetResonantFrequency() << " Hz " << std::endl;
        std::cout << "Ax       = " << processor.GetAx()*1e-6 << " kPa.L^-1" << std::endl;
        std::cout << "\n";
    }
};
```
