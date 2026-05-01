---
title: "Measure memory use per process (Figure 4)"
draft: false
layout: "single"
weight: 3
paperTutorialTestFile: "https://github.com/Chaste/project_Harvey2015/blob/a0fc3c6879e9b4bf55f507f3727560cdce653f23/test/TestMemoryUseLiteratePaper.hpp"
version: "2026.1"
---

This class was used to produce the results in Figure 4.
It constructs a large cell population and measures the amount of memory
in use. By running on larger numbers of processes, a proportionally
smaller amount of memory is used by each process.

The geometry for the construction of the population is contained in

```text
projects/Harvey2015/test/data/1024000_2d_cells.dat
```


## Use

This test suite should be run in parallel.  It should be run on several numbers of processes (from 1 to 32 processes in figure
in the paper.)

A useful for loop (in `bash`) would be

```bash
for i in {1..32}; do echo $i "processes ===";scons build=GccOptNative_$i projects/Harvey2015/test/TestMemoryUseLiteratePaper.hpp | grep memory; done
```


This runs the test on increasingly larger number of processes and only outputs the lines which state
the individual memory use.  Some post-processing will be needed in order to select the maximum memory use to
plot on the vertical axis.


```cpp
// The testing framework
#include <cxxtest/TestSuite.h>
#include "AbstractCellBasedTestSuite.hpp"

// Includes for printing out memory
#include <unistd.h>
#include <sys/resource.h>

// Cell-based includes
#include "FixedDurationGenerationBasedCellCycleModel.hpp"
#include "ParallelCellsGenerator.hpp"
#include "CellPropertyRegistry.hpp"
#include "DifferentiatedCellProliferativeType.hpp"

// Needed to run in parallel
#include "PetscSetupAndFinalize.hpp"
```

This function prints the memory usage at the time it is called.
`rPrefix` contains the rank (identifier) of the process


```cpp
void PrintMemoryUsage(const std::string& rPrefix)
{
    struct rusage rusage;
    getrusage( RUSAGE_SELF, &rusage );

    double max_res = (double)(rusage.ru_maxrss)/(1024);// Convert KB to MB

    std::cout << rPrefix << ": memory use = " << max_res <<  " MB.\n";
}
```


## The test suite

This class was used to produce the results in Figure 4.
It constructs a large cell population and measures the amount of memory
in use. By running on larger numbers of processes, a proportionally
smaller amount of memory is used by each process.


```cpp
class TestMemoryUse : public AbstractCellBasedTestSuite
{
public:

    void TestProfile2dSimulation() throw (Exception)
    {
```


Record the rank of each process so that it can be output


```cpp
        std::ostringstream rank;
        rank << PetscTools::GetMyRank();
```

Make a `NodesOnlyMesh` in which to store the nodes which are to be read from file


```cpp
        NodesOnlyMesh<2> mesh;
        mesh.SetCalculateNodeNeighbours(false);
```


There is a 1024 y-range over which this mesh is split.  This means that each of 32 processes will take a y-range of 32.
The maximum interaction distance will define the size of the indexing boxes and thus define
the size of the strips which are the unit of parallel distribution


```cpp
        mesh.SetMaximumInteractionDistance(4);
```

Here we call a parallel helper method which reads the cell locations
from a file on disk.  This is a uniformly spread rectangle which is 1000 cells in the
x direction  and 1024 cells wide in the y direction.

The proliferative type ensures that the cells are not growing, although this information is never
used.  No simulations are run.


```cpp
        std::vector<CellPtr> cells;
        ParallelCellsGenerator<FixedDurationGenerationBasedCellCycleModel, 2> generator;
        generator.GenerateParallelCells("projects/Harvey2015/test/data/1024000_2d_cells.dat",
                                        cells,
                                        mesh,
                                        CellPropertyRegistry::Instance()->Get<DifferentiatedCellProliferativeType>());
```

Print the approximate memory use


```cpp
        PrintMemoryUsage(rank.str());
    }
};
```


## Full code

```cpp {title="TestMemoryUseLiteratePaper.hpp"}
// The testing framework
#include <cxxtest/TestSuite.h>
#include "AbstractCellBasedTestSuite.hpp"

// Includes for printing out memory
#include <unistd.h>
#include <sys/resource.h>

// Cell-based includes
#include "FixedDurationGenerationBasedCellCycleModel.hpp"
#include "ParallelCellsGenerator.hpp"
#include "CellPropertyRegistry.hpp"
#include "DifferentiatedCellProliferativeType.hpp"

// Needed to run in parallel
#include "PetscSetupAndFinalize.hpp"

void PrintMemoryUsage(const std::string& rPrefix)
{
    struct rusage rusage;
    getrusage( RUSAGE_SELF, &rusage );

    double max_res = (double)(rusage.ru_maxrss)/(1024);// Convert KB to MB

    std::cout << rPrefix << ": memory use = " << max_res <<  " MB.\n";
}

class TestMemoryUse : public AbstractCellBasedTestSuite
{
public:

    void TestProfile2dSimulation() throw (Exception)
    {
        std::ostringstream rank;
        rank << PetscTools::GetMyRank();

        NodesOnlyMesh<2> mesh;
        mesh.SetCalculateNodeNeighbours(false);
        mesh.SetMaximumInteractionDistance(4);

        std::vector<CellPtr> cells;
        ParallelCellsGenerator<FixedDurationGenerationBasedCellCycleModel, 2> generator;
        generator.GenerateParallelCells("projects/Harvey2015/test/data/1024000_2d_cells.dat",
                                        cells,
                                        mesh,
                                        CellPropertyRegistry::Instance()->Get<DifferentiatedCellProliferativeType>());

        PrintMemoryUsage(rank.str());
    }
};
```
