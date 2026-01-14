This tutorial was generated from the file projects/Harvey2015/test/TestProfileSimulationLiteratePaper.hpp at revision r23521.
Note that the code is given in full at the bottom of the page.




```cpp
// Includes for the testing framework
#include <cxxtest/TestSuite.h>
#include "AbstractCellBasedTestSuite.hpp"

// Cell-based Chaste include files
#include "CellBasedEventHandler.hpp" //For extra timing information
#include "FixedDurationGenerationBasedCellCycleModel.hpp"
#include "OffLatticeSimulation.hpp"
#include "SmartPointers.hpp"

// Includes for code which is particular to this bolt-on project
// SEM refers to the subcellular element model
#include "SemCellsGenerator.hpp"
#include "SemForce.hpp"
#include "SemMesh.hpp"

// Parallel working
#include "PetscSetupAndFinalize.hpp"
```

## Measure compute-time performance for a large population to plot parallel speed-up (Figure 5)
This class was used to produce the results in Figure 5.
It constructs a population of 1,024,000 cells and simulates the population
dynamics for 100 time-steps, printing out the total compute time at the end.
It must be run multiple times in order to gauge the parallel efficiency/speed-up.

The geometry for the construction of the population is contained in

```text
projects/Harvey2015/test/data/2d_1024_cells.dat
```


### Use

This test suite should be run in parallel.  It should be run on several numbers of processes (from 1 to 32 processes in figure
in the paper.)

**Warning:** an individual run of this code is likely to take up to hour (actual wall-clock time) depending on
the number of processors, speed of your CPUs, amount of memory, network bandwidth, compiler optimization etc.
When run sequentially on a 2.7GHz machine with more than 8Gb of RAM this simulation takes about 40 minutes.
The program does not produce output to screen during the simulation.

A useful for loop (in `bash`) would be

```bash
for i in {1..32}; do echo $i "processes ===";scons build=GccOptNative_$i projects/Harvey2015/test/TestProfileSimulationLiteratePaper.hpp | grep ##Prof; done
```

This runs the test on increasingly larger number of processes and only outputs the lines which state
the total execution time for the simulation.

N.B. The results for the paper were generated using a large shared-memory computer, and this test
is not suitable for running on small desktop machines due to the large memory overhead.

### The test suite
This class was used to produce the results in Figure 5.

It constructs a population of 1,024,000 cells in a repeating pattern
of 1024 cells (to simplify construction) and simulates the system
for 100 integration time steps.

The maximum of the recorded wall time for all processes relative to the recorded
wall time for one process is used to produce the speed-up metric.

Note that SEM refers to the subcellular element model from the publication
*Modeling multicellular systems using subcellular elements, Newman, T.J, Math. Biosci. Eng. (2) 2005*.
This model was used as a scientific motivation during the work in this bolt-on project.


```cpp
class TestProfileSimulation : public AbstractCellBasedTestSuite
{
private:

    double mLastStartTime;
```


These methods are run before (setUp) and after (tearDown) the
test suite has completed to output the total time for the simulation.


```cpp
    void setUp()
    {
        mLastStartTime = std::clock();
        AbstractCellBasedTestSuite::setUp();
    }

    void tearDown()
    {
        double time = std::clock();
        double elapsed_time = (time - mLastStartTime)/(CLOCKS_PER_SEC);

        double max_time;
```


This functions pools all timing results onto a single process to
compute the maximum time taken by any single process.


```cpp
        MPI_Allreduce(&elapsed_time, &max_time, 1, MPI_DOUBLE, MPI_MAX, PETSC_COMM_WORLD);
        if (PetscTools::AmMaster())
        {
            std::cout << "##Prof " << PetscTools::GetNumProcs() << " " <<  max_time << std::endl;
        }
        AbstractCellBasedTestSuite::tearDown();
    }

public:

    void TestProfile2dSimulation() throw (Exception)
    {
```


The cell population is constructed in batches of 1024 cells,
whose geometry is defined in test/data/2d_1024_cells.dat.
This simplifies the construction of a large population of cells.


```cpp
        SemParameterScaler<2>::Instance()->SetNumElementsPerCell(1024);
        unsigned total_num_cells = 1000;

        c_vector<unsigned, 2> numCellsEachDirection;

        SemMesh<2> mesh;
        mesh.SetCalculateNodeNeighbours(false);
        mesh.SetMaximumInteractionDistance(0.1);

        std::vector<CellPtr> cells;
        SemCellsGenerator<FixedDurationGenerationBasedCellCycleModel, 2> generator;
        generator.SetNumCells(total_num_cells);
        for (unsigned i = 0; i < total_num_cells; ++i)
        {
```


Set a location for each batch of 1024 cells.


```cpp
            c_vector<double, 2> location = zero_vector<double>(2);
            location[0] = (double)(i % 10);
            location[1] = (double)((unsigned)(i / 10));
            generator.SetCellLocation(i, location);
        }
```

We use the `GenerateSemCells` method to create `total_num_cells` repeating patterns
of 1000 cells using the geometry defined in test/data/2d_1024_cells.dat.


```cpp
        generator.GenerateSemCells("projects/Harvey2015/test/data/2d_1024_cells.dat", cells, mesh);
```

This code block writes out the initial distribution of cell numbers
between processes to file. The round-robin directives enforce that only
a single process may execute this block of code concurrently, which prevents
concurrent writes to a single file.

This distribution file may be found relative to `CHASTE_TEST_OUTPUT` which by default is
`/tmp/$USER/testoutput`

```bash
cat /tmp/$USER/testoutput/DivisionResults/division_results.txt
```



```cpp
        PetscTools::BeginRoundRobin();
        OutputFileHandler output_file_handler("DivisionResults", false);
        out_stream stream = output_file_handler.OpenOutputFile("division_results.txt", std::ios::app);
        if (PetscTools::AmMaster())
        {
            *stream << "NodesPerProc " << PetscTools::GetNumProcs() << "\t";
        }

        *stream << mesh.GetNumNodes() << "\t";

        if (PetscTools::AmTopMost())
        {
            *stream << "\n";
        }
        stream->close();
        PetscTools::EndRoundRobin();
```

We create a cell population object from the mesh and the set of cells
generated above.


```cpp
        NodeBasedCellPopulation<2> node_based_cell_population(mesh, cells);
        node_based_cell_population.SetDampingConstantNormal((1 / 3600.0) * 1e-8);
        node_based_cell_population.SetOutputResultsForChasteVisualizer(false);
```

Create a simulation object from the cell population.
We set a flag to denote that no cell division takes place which
enables marginally greater efficiency.


```cpp
        OffLatticeSimulation<2> simulator(node_based_cell_population);
        simulator.SetNoBirth(true);
```

Output from the simulation may be found relative to `CHASTE_TEST_OUTPUT` which by default is
`/tmp/$USER/testoutput`


```cpp
        std::ostringstream procs;
        procs << PetscTools::GetNumProcs();
        std::string output_directory = "ProfileScEMSimulation" + procs.str();
        simulator.SetOutputDirectory(output_directory);
```

Create a cell-cell interaction force law, and pass it to the
simulator object. The force is set to have the same magnitude
between all cells in the population.


```cpp
        MAKE_PTR(SemForce<2>, p_sem_force);
        for (unsigned i = 0; i < total_num_cells; ++i)
        {
            p_sem_force->SetRelativeSpringStiffness(i, 1.0);
        }
        simulator.AddForce(p_sem_force);
```

Set the simulation to run for 100 time-steps. This
allows comparison of the running speed of this simulation
as the number of processes is increased.


```cpp
        double time_step = 1e-4 / 3600.0;
        simulator.SetDt(time_step);
        double end_time = 100.0 * time_step;
```

Solve the simulation and report the total execution time.


```cpp
        simulator.SetSamplingTimestepMultiple(100);
        simulator.SetEndTime(end_time);
        simulator.Solve();
        SemParameterScaler<2>::Instance()->Destroy();
```

These lines give a little extra information about which main functions used the time in the
simulation.


```cpp
        CellBasedEventHandler::Headings();
        CellBasedEventHandler::Report();
    }
};
```



## Code
The full code is given below


### File name `TestProfileSimulationLiteratePaper.hpp`


```cpp
// Includes for the testing framework
#include <cxxtest/TestSuite.h>
#include "AbstractCellBasedTestSuite.hpp"

// Cell-based Chaste include files
#include "CellBasedEventHandler.hpp" //For extra timing information
#include "FixedDurationGenerationBasedCellCycleModel.hpp"
#include "OffLatticeSimulation.hpp"
#include "SmartPointers.hpp"

// Includes for code which is particular to this bolt-on project
// SEM refers to the subcellular element model
#include "SemCellsGenerator.hpp"
#include "SemForce.hpp"
#include "SemMesh.hpp"

// Parallel working
#include "PetscSetupAndFinalize.hpp"

class TestProfileSimulation : public AbstractCellBasedTestSuite
{
private:

    double mLastStartTime;
    void setUp()
    {
        mLastStartTime = std::clock();
        AbstractCellBasedTestSuite::setUp();
    }

    void tearDown()
    {
        double time = std::clock();
        double elapsed_time = (time - mLastStartTime)/(CLOCKS_PER_SEC);

        double max_time;
        MPI_Allreduce(&elapsed_time, &max_time, 1, MPI_DOUBLE, MPI_MAX, PETSC_COMM_WORLD);
        if (PetscTools::AmMaster())
        {
            std::cout << "##Prof " << PetscTools::GetNumProcs() << " " <<  max_time << std::endl;
        }
        AbstractCellBasedTestSuite::tearDown();
    }

public:

    void TestProfile2dSimulation() throw (Exception)
    {
        SemParameterScaler<2>::Instance()->SetNumElementsPerCell(1024);
        unsigned total_num_cells = 1000;

        c_vector<unsigned, 2> numCellsEachDirection;

        SemMesh<2> mesh;
        mesh.SetCalculateNodeNeighbours(false);
        mesh.SetMaximumInteractionDistance(0.1);

        std::vector<CellPtr> cells;
        SemCellsGenerator<FixedDurationGenerationBasedCellCycleModel, 2> generator;
        generator.SetNumCells(total_num_cells);
        for (unsigned i = 0; i < total_num_cells; ++i)
        {
            c_vector<double, 2> location = zero_vector<double>(2);
            location[0] = (double)(i % 10);
            location[1] = (double)((unsigned)(i / 10));
            generator.SetCellLocation(i, location);
        }

        generator.GenerateSemCells("projects/Harvey2015/test/data/2d_1024_cells.dat", cells, mesh);

        PetscTools::BeginRoundRobin();
        OutputFileHandler output_file_handler("DivisionResults", false);
        out_stream stream = output_file_handler.OpenOutputFile("division_results.txt", std::ios::app);
        if (PetscTools::AmMaster())
        {
            *stream << "NodesPerProc " << PetscTools::GetNumProcs() << "\t";
        }

        *stream << mesh.GetNumNodes() << "\t";

        if (PetscTools::AmTopMost())
        {
            *stream << "\n";
        }
        stream->close();
        PetscTools::EndRoundRobin();

        NodeBasedCellPopulation<2> node_based_cell_population(mesh, cells);
        node_based_cell_population.SetDampingConstantNormal((1 / 3600.0) * 1e-8);
        node_based_cell_population.SetOutputResultsForChasteVisualizer(false);

        OffLatticeSimulation<2> simulator(node_based_cell_population);
        simulator.SetNoBirth(true);

        std::ostringstream procs;
        procs << PetscTools::GetNumProcs();
        std::string output_directory = "ProfileScEMSimulation" + procs.str();
        simulator.SetOutputDirectory(output_directory);

        MAKE_PTR(SemForce<2>, p_sem_force);
        for (unsigned i = 0; i < total_num_cells; ++i)
        {
            p_sem_force->SetRelativeSpringStiffness(i, 1.0);
        }
        simulator.AddForce(p_sem_force);

        double time_step = 1e-4 / 3600.0;
        simulator.SetDt(time_step);
        double end_time = 100.0 * time_step;

        simulator.SetSamplingTimestepMultiple(100);
        simulator.SetEndTime(end_time);
        simulator.Solve();
        SemParameterScaler<2>::Instance()->Destroy();

        CellBasedEventHandler::Headings();
        CellBasedEventHandler::Report();
    }
};
```


