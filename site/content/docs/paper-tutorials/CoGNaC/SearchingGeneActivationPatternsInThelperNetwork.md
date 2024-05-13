This tutorial was generated from the file projects/CoGNaC/test/TestSearchingGeneActivationPatternsInThelperNetworkLiteratePaper.hpp at revision r27518.
Note that the code is given in full at the bottom of the page.



# Searching gene activation patterns in T-helper cell differentiation

## Introduction

In this class we show how to search gene activation patterns starting from a network,
calculate its Attractor Transition Network (Figure 3).

We begin by including the necessary header files.


```cpp
#include <cxxtest/TestSuite.h>

#include "RandomBooleanNetwork.hpp"
#include "DifferentiationTree.hpp"
#include "DifferentiationTreeNode.hpp"
#include "ThresholdErgodicSetDifferentiationTree.hpp"
//This test is always run sequentially (never in parallel)
#include "FakePetscSetup.hpp"
```

Next, we define the test class.

```cpp
class TestSearchingGeneActivationPatternsInThelperNetwork : public CxxTest::TestSuite
{
public:
```


## Finding attractors and calculating the ATN from 'thelper' network

In this example we search the attractors of the thelper network. We test that
the network has three single-point attractors and calculate the ATN.


```cpp
    void testThelper() throw (Exception)
    {
```

First of all we initialise Buddy.

```cpp
        bdd_init(10000,1000);
        try
        {
```

We instantiate a
```
[RandomBooleanNetwork](https://github.com/Chaste/trac_archive/wiki/Random-Boolean-Network)
```
 object using a
```
[ThresholdErgodicSetDifferentiationTree](https://github.com/Chaste/trac_archive/wiki/Threshold-Ergodic-Set-Differentiation-Tree)
```

which is used for generate a
```
[DifferentiationTree](https://github.com/Chaste/trac_archive/wiki/Differentiation-Tree)
```
 object. In the constructor, the
```
[ThresholdErgodicSetDifferentiationTree](https://github.com/Chaste/trac_archive/wiki/Threshold-Ergodic-Set-Differentiation-Tree)
```
 object initialise a
```
[RandomBooleanNetwork](https://github.com/Chaste/trac_archive/wiki/Random-Boolean-Network)
```
 from the
'thelper.net' network, and then it search the attractors of the network.


```cpp
        	ThresholdErgodicSetDifferentiationTree TES_tree ("projects/CoGNaC/networks_samples/thelper.net");
```

We test that the number of attractors found is three.

```cpp
            TS_ASSERT_EQUALS(TES_tree.getBooleanNetwork()->getAttractorsNumber(),3u);
```

We test that the attractors found are all single-point.

```cpp
            std::vector<unsigned> attractors_lengths = TES_tree.getBooleanNetwork()->getAttractorLength();
            for (unsigned i=0; i<attractors_lengths.size(); i++){
            	TS_ASSERT_EQUALS(attractors_lengths.at(i),1u);
            }
```

We export the stochastic matrix in a file, where we can
visualise data shown in Figure 3 (Attractor Transition Network).

```cpp
            TES_tree.printStochasticMatrixAndAttractorLengthsToDatFile("networks_generated","stochastic_matrix_thelper.dat");
        }
        catch (Exception& e)
        {
            TS_FAIL(e.GetMessage());
            bdd_done();
        }
```

We release Buddy.

```cpp
        bdd_done();
    }
};
```



# Code
The full code is given below


## File name `TestSearchingGeneActivationPatternsInThelperNetworkLiteratePaper.hpp`


```cpp
#include <cxxtest/TestSuite.h>

#include "RandomBooleanNetwork.hpp"
#include "DifferentiationTree.hpp"
#include "DifferentiationTreeNode.hpp"
#include "ThresholdErgodicSetDifferentiationTree.hpp"
//This test is always run sequentially (never in parallel)
#include "FakePetscSetup.hpp"

class TestSearchingGeneActivationPatternsInThelperNetwork : public CxxTest::TestSuite
{
public:
    void testThelper() throw (Exception)
    {
        bdd_init(10000,1000);
        try
        {
        	ThresholdErgodicSetDifferentiationTree TES_tree ("projects/CoGNaC/networks_samples/thelper.net");

            TS_ASSERT_EQUALS(TES_tree.getBooleanNetwork()->getAttractorsNumber(),3u);

            std::vector<unsigned> attractors_lengths = TES_tree.getBooleanNetwork()->getAttractorLength();
            for (unsigned i=0; i<attractors_lengths.size(); i++){
            	TS_ASSERT_EQUALS(attractors_lengths.at(i),1u);
            }

            TES_tree.printStochasticMatrixAndAttractorLengthsToDatFile("networks_generated","stochastic_matrix_thelper.dat");
        }
        catch (Exception& e)
        {
            TS_FAIL(e.GetMessage());
            bdd_done();
        }
        bdd_done();
    }
};
```


