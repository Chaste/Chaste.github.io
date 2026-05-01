---
title: "Study the convergence of reference monodomain tissue simulation solutions"
draft: false
layout: "single"
weight: 4
paperTutorialTestFile: "https://github.com/Chaste/project_Frontiers2014/blob/e495d4d2f7ae14f988de496f659f5056470c0434/test/TestMonodomainConvergenceLiteratePaper.hpp"
version: "2026.1"
---


On this wiki page we describe in detail the code that is used to run this example from the paper.

This test can be used to run a 1D monodomain simulation with a handful of the models,
taking the space and PDE time step to use from command line arguments.  It stimulates the fibre at
the left hand end, and saves the voltage trace at the right hand end to file for viewing/comparing
at different step settings.  It also checks that the excitation wave has propagated along the fibre,
and calculates some summary properties of the action potential, again writing these to file.


## Code overview

The first thing to do is to include the necessary header files.


```cpp
#include <cxxtest/TestSuite.h>

#include <vector>
#include <string>
#include <sstream>
#include <boost/assign/list_of.hpp>
#include <boost/foreach.hpp>

// Headers specific to this project
#include "CellModelUtilities.hpp"
#include "DynamicModelCellFactory.hpp"

// Chaste 'heart' headers
#include "MonodomainProblem.hpp"
#include "CellProperties.hpp"
#include "AbstractCvodeCell.hpp"

// Other Chaste headers
#include "FileFinder.hpp"
#include "OutputFileHandler.hpp"
#include "CommandLineArguments.hpp"

// This header is needed to allow us to prevent being run in parallel
#include "PetscSetupAndFinalize.hpp"

class TestMonodomainConvergenceLiteratePaper : public CxxTest::TestSuite
{
public:
    void TestMonodomainConvergence() throw (Exception)
    {
        // We don't want to find this confusing matters!!
        EXIT_IF_PARALLEL;
```

This command line argument says whether to reset the CVODE solver fully at each PDE time step.

```cpp
        bool reset_cvode = false;
        if (CommandLineArguments::Instance()->OptionExists("--reset"))
        {
            reset_cvode = true;
        }
```

This test was run with the following values for PDE time step inserted here:

- 0.001 ms (much finer than normal)
- 0.01 ms (typically a fine timestep)
- 0.1 ms (about average)
- 1 ms (coarse)


```cpp
        double pde_timestep;
        if (CommandLineArguments::Instance()->OptionExists("--timestep"))
        {
            pde_timestep = CommandLineArguments::Instance()->GetDoubleCorrespondingToOption("--timestep");
        }
        else
        {
            EXCEPTION("Please enter an argument '--timestep', probably from [0.001, 0.01, 0.1, 1].");
        }
```

This test was run with the following values for mesh spacing inserted here:

- 0.01 cm (fine)
- 0.001 cm (much finer than normal)


```cpp
        double h;
        if (CommandLineArguments::Instance()->OptionExists("--spacestep"))
        {
            h = CommandLineArguments::Instance()->GetDoubleCorrespondingToOption("--spacestep");
        }
        else
        {
            EXCEPTION("Please enter an argument '--spacestep', probably from [0.001, 0.01].");
        }
```

Next we loop over the following list of models that we want to do tissue simulations with.

```cpp
        std::vector<std::string> models_to_use = boost::assign::list_of("luo_rudy_1991")
                                                                       ("beeler_reuter_model_1977")
                                                                       ("nygren_atrial_model_1998")
                                                                       ("ten_tusscher_model_2004_epi")
                                                                       ("grandi_pasqualini_bers_2010_ss")
                                                                       ("shannon_wang_puglisi_weber_bers_2004")
                                                                       ("iyer_model_2007");

        // Model file locations
        FileFinder this_file(__FILE__);
        FileFinder model_folder("../cellml", this_file);

        // Loop over models
        BOOST_FOREACH(std::string model, models_to_use)
        {
```

Find the CellML file for this model, and set up a cell factory that uses this model for the whole mesh.

```cpp
            FileFinder model_to_use(model + ".cellml", model_folder);

            std::stringstream output_folder_stream;
            output_folder_stream << "Frontiers/MonodomainConvergence/" << model << "_pde_" << pde_timestep << "_h_" << h;
            if (reset_cvode)
            {
                output_folder_stream << "_Reset";
            }
            std::string output_folder = output_folder_stream.str();

            OutputFileHandler base_model_handler(output_folder);
            DynamicModelCellFactory cell_factory(model_to_use,
                                                 base_model_handler,
                                                 Solvers::CVODE_ANALYTIC_J,
                                                 false, // Whether to use lookup tables.
                                                 true); // true for making reference solution
```

We will auto-generate a mesh this time, and pass it in, rather than provide a mesh file name.
This is how to generate a cuboid mesh with a given spatial stepsize *h*.

Using a `DistributedTetrahedralMesh` is faster than `TetrahedralMesh` when running on multiple processes.
However, it permutes the node ordering for output. Most of time time this won't matter, but later in this
test we want to access specific node indices. One method of doing this is to ask `HeartConfig` to use the
original node ordering for the output.


```cpp
            DistributedTetrahedralMesh<1,1> mesh;
            mesh.ConstructRegularSlabMesh(h, 1 /*length*/);
            HeartConfig::Instance()->SetOutputUsingOriginalNodeOrdering(true);
```

We need to change the printing time steps if going to be less than 0.1 ms output, but note
that the AP calculations will necessarily be affected by this. We could do them all
at 1ms output, then they would be more consistent, but far less accurate!


```cpp
            if (pde_timestep < 0.1)
            {
                HeartConfig::Instance()->SetOdePdeAndPrintingTimeSteps(pde_timestep, pde_timestep, 0.1);
            }
            else
            {
                HeartConfig::Instance()->SetOdePdeAndPrintingTimeSteps(pde_timestep, pde_timestep, pde_timestep);
            }
```

Set the simulation duration, etc.
One thing that should be noted for monodomain problems, the *intracellular
conductivity* is used as the monodomain effective conductivity (not a
harmonic mean of intra and extracellular conductivities). So if you want to
alter the monodomain conductivity call `HeartConfig::Instance()->SetIntracellularConductivities()`.


```cpp
            HeartConfig::Instance()->SetSimulationDuration(500); //ms
            HeartConfig::Instance()->SetOutputDirectory(output_folder + "/results");
            HeartConfig::Instance()->SetOutputFilenamePrefix("results");
            HeartConfig::Instance()->SetVisualizeWithVtk(true);
```

Now we declare the problem class.

```cpp
            MonodomainProblem<1> monodomain_problem( &cell_factory );
```

If a mesh-file-name hasn't been set using `HeartConfig`, we have to pass in
a mesh using the `SetMesh` method (which must be called before `Initialise`).

```cpp
            monodomain_problem.SetMesh(&mesh);
```

`SetWriteInfo` is a useful method that means that the min/max voltage is
printed as the simulation runs (useful for verifying that cells are stimulated
and the wave is propagating, for example). Note that `scons` does buffer output
before printing to screen, so don't worry if you don't see any output for a while!

```cpp
            monodomain_problem.SetWriteInfo();
```

Finally, call `Initialise` to finish the problem setup.

```cpp
            monodomain_problem.Initialise();

            if (reset_cvode)
            {
```

The cells should now be set up.
We have to hack in to call a method on each one.

```cpp
                // TODO: use FinaliseCellCreation instead!
                DistributedVectorFactory* p_factory = mesh.GetDistributedVectorFactory();
                Vec monodomain_vec = p_factory->CreateVec();
                DistributedVector monodomain_distributed_vec = p_factory->CreateDistributedVector(monodomain_vec);

                for (DistributedVector::Iterator index=monodomain_distributed_vec.Begin();
                     index != monodomain_distributed_vec.End();
                     ++index)
                {
                    AbstractCardiacCellInterface* p_cell = monodomain_problem.GetMonodomainTissue()->GetCardiacCell(index.Global);
                    static_cast<AbstractCvodeCell*>(p_cell)->SetForceReset(true);
                }
            }

            try
            {
                monodomain_problem.Solve();
            }
            catch (Exception& e)
            {
                WARNING("Model '" << model << "' simulation failed with: " << e.GetMessage());
                continue;
            }
```

Having simulated the system, we now read some of the results data (which gets written to disk) back in,
and evaluate AP properties at the last node, as per the single cell simulations.


```cpp
            Hdf5DataReader data_reader = monodomain_problem.GetDataReader();
            std::vector<double> times = data_reader.GetUnlimitedDimensionValues();
            std::vector<double> last_node = data_reader.GetVariableOverTime("V", mesh.GetNumNodes()-1u);
```

First we write the raw AP data to file, in the same folder as the full results.  To do so we need to get a
handler for that folder, but pass `false` as the second argument to avoid removing the existing results!


```cpp
            OutputFileHandler handler(output_folder, false);
            std::stringstream file_suffix;
            file_suffix << "_tissue_pde_" << pde_timestep << "_h_" << h;
            if (reset_cvode)
            {
                file_suffix << "_Reset";
            }
            out_stream p_file = handler.OpenOutputFile(model + file_suffix.str() + ".dat");
            for (unsigned i=0; i<times.size(); i++)
            {
                *p_file << times[i] << "\t" << last_node[i] << "\n";
            }
            p_file->close();
```

Now we copy this file into the repository, finding the data folder relative to this test file.

```cpp
            FileFinder this_file(__FILE__);
            FileFinder repo_data("data/reference_traces", this_file);
            FileFinder ref_data = handler.FindFile(model + file_suffix.str() + ".dat");
            ref_data.CopyTo(repo_data);
```

Next, check that the solution looks like an action potential, and save summary statistics to file.

```cpp
            try
            {
                CellProperties props(last_node, times);
                std::vector<std::pair<std::string, double> > properties;

                // Calculate some summary statistics of the AP that was produced
                properties.push_back(std::pair<std::string, double>("APD90",props.GetLastActionPotentialDuration(90.0)));
                properties.push_back(std::pair<std::string, double>("APD50",props.GetLastActionPotentialDuration(50.0)));
                properties.push_back(std::pair<std::string, double>("APD30",props.GetLastActionPotentialDuration(30.0)));
                properties.push_back(std::pair<std::string, double>("V_max",props.GetLastPeakPotential()));
                properties.push_back(std::pair<std::string, double>("V_min",props.GetLastRestingPotential()));
                properties.push_back(std::pair<std::string, double>("dVdt_max",props.GetLastMaxUpstrokeVelocity()));

                // Save these to a dedicated file for this model, and output to reference data folder in the repository.
                out_stream p_summary_file = handler.OpenOutputFile(model + file_suffix.str() + ".summary");
                for (unsigned i=0; i<properties.size(); i++)
                {
                    std::cout << properties[i].first  << " = " << properties[i].second << std::endl;
                    *p_summary_file << properties[i].first << "\t" << properties[i].second << std::endl;
                }
                p_summary_file->close();
                FileFinder summary_info = handler.FindFile(model + file_suffix.str() + ".summary");
                summary_info.CopyTo(repo_data);
            }
            catch (const Exception& r_e)
            {
                WARNING("Action potential properties calculation failed for model " << model);
            }
        }
    }
};
```


## Full code

```cpp {title="TestMonodomainConvergenceLiteratePaper.hpp"}
#include <cxxtest/TestSuite.h>

#include <vector>
#include <string>
#include <sstream>
#include <boost/assign/list_of.hpp>
#include <boost/foreach.hpp>

// Headers specific to this project
#include "CellModelUtilities.hpp"
#include "DynamicModelCellFactory.hpp"

// Chaste 'heart' headers
#include "MonodomainProblem.hpp"
#include "CellProperties.hpp"
#include "AbstractCvodeCell.hpp"

// Other Chaste headers
#include "FileFinder.hpp"
#include "OutputFileHandler.hpp"
#include "CommandLineArguments.hpp"

// This header is needed to allow us to prevent being run in parallel
#include "PetscSetupAndFinalize.hpp"

class TestMonodomainConvergenceLiteratePaper : public CxxTest::TestSuite
{
public:
    void TestMonodomainConvergence() throw (Exception)
    {
        // We don't want to find this confusing matters!!
        EXIT_IF_PARALLEL;

        bool reset_cvode = false;
        if (CommandLineArguments::Instance()->OptionExists("--reset"))
        {
            reset_cvode = true;
        }

        double pde_timestep;
        if (CommandLineArguments::Instance()->OptionExists("--timestep"))
        {
            pde_timestep = CommandLineArguments::Instance()->GetDoubleCorrespondingToOption("--timestep");
        }
        else
        {
            EXCEPTION("Please enter an argument '--timestep', probably from [0.001, 0.01, 0.1, 1].");
        }

        double h;
        if (CommandLineArguments::Instance()->OptionExists("--spacestep"))
        {
            h = CommandLineArguments::Instance()->GetDoubleCorrespondingToOption("--spacestep");
        }
        else
        {
            EXCEPTION("Please enter an argument '--spacestep', probably from [0.001, 0.01].");
        }

        std::vector<std::string> models_to_use = boost::assign::list_of("luo_rudy_1991")
                                                                       ("beeler_reuter_model_1977")
                                                                       ("nygren_atrial_model_1998")
                                                                       ("ten_tusscher_model_2004_epi")
                                                                       ("grandi_pasqualini_bers_2010_ss")
                                                                       ("shannon_wang_puglisi_weber_bers_2004")
                                                                       ("iyer_model_2007");

        // Model file locations
        FileFinder this_file(__FILE__);
        FileFinder model_folder("../cellml", this_file);

        // Loop over models
        BOOST_FOREACH(std::string model, models_to_use)
        {
            FileFinder model_to_use(model + ".cellml", model_folder);

            std::stringstream output_folder_stream;
            output_folder_stream << "Frontiers/MonodomainConvergence/" << model << "_pde_" << pde_timestep << "_h_" << h;
            if (reset_cvode)
            {
                output_folder_stream << "_Reset";
            }
            std::string output_folder = output_folder_stream.str();

            OutputFileHandler base_model_handler(output_folder);
            DynamicModelCellFactory cell_factory(model_to_use,
                                                 base_model_handler,
                                                 Solvers::CVODE_ANALYTIC_J,
                                                 false, // Whether to use lookup tables.
                                                 true); // true for making reference solution

            DistributedTetrahedralMesh<1,1> mesh;
            mesh.ConstructRegularSlabMesh(h, 1 /*length*/);
            HeartConfig::Instance()->SetOutputUsingOriginalNodeOrdering(true);

            if (pde_timestep < 0.1)
            {
                HeartConfig::Instance()->SetOdePdeAndPrintingTimeSteps(pde_timestep, pde_timestep, 0.1);
            }
            else
            {
                HeartConfig::Instance()->SetOdePdeAndPrintingTimeSteps(pde_timestep, pde_timestep, pde_timestep);
            }

            HeartConfig::Instance()->SetSimulationDuration(500); //ms
            HeartConfig::Instance()->SetOutputDirectory(output_folder + "/results");
            HeartConfig::Instance()->SetOutputFilenamePrefix("results");
            HeartConfig::Instance()->SetVisualizeWithVtk(true);

            MonodomainProblem<1> monodomain_problem( &cell_factory );

            monodomain_problem.SetMesh(&mesh);

            monodomain_problem.SetWriteInfo();

            monodomain_problem.Initialise();

            if (reset_cvode)
            {
                // TODO: use FinaliseCellCreation instead!
                DistributedVectorFactory* p_factory = mesh.GetDistributedVectorFactory();
                Vec monodomain_vec = p_factory->CreateVec();
                DistributedVector monodomain_distributed_vec = p_factory->CreateDistributedVector(monodomain_vec);

                for (DistributedVector::Iterator index=monodomain_distributed_vec.Begin();
                     index != monodomain_distributed_vec.End();
                     ++index)
                {
                    AbstractCardiacCellInterface* p_cell = monodomain_problem.GetMonodomainTissue()->GetCardiacCell(index.Global);
                    static_cast<AbstractCvodeCell*>(p_cell)->SetForceReset(true);
                }
            }

            try
            {
                monodomain_problem.Solve();
            }
            catch (Exception& e)
            {
                WARNING("Model '" << model << "' simulation failed with: " << e.GetMessage());
                continue;
            }

            Hdf5DataReader data_reader = monodomain_problem.GetDataReader();
            std::vector<double> times = data_reader.GetUnlimitedDimensionValues();
            std::vector<double> last_node = data_reader.GetVariableOverTime("V", mesh.GetNumNodes()-1u);

            OutputFileHandler handler(output_folder, false);
            std::stringstream file_suffix;
            file_suffix << "_tissue_pde_" << pde_timestep << "_h_" << h;
            if (reset_cvode)
            {
                file_suffix << "_Reset";
            }
            out_stream p_file = handler.OpenOutputFile(model + file_suffix.str() + ".dat");
            for (unsigned i=0; i<times.size(); i++)
            {
                *p_file << times[i] << "\t" << last_node[i] << "\n";
            }
            p_file->close();

            FileFinder this_file(__FILE__);
            FileFinder repo_data("data/reference_traces", this_file);
            FileFinder ref_data = handler.FindFile(model + file_suffix.str() + ".dat");
            ref_data.CopyTo(repo_data);

            try
            {
                CellProperties props(last_node, times);
                std::vector<std::pair<std::string, double> > properties;

                // Calculate some summary statistics of the AP that was produced
                properties.push_back(std::pair<std::string, double>("APD90",props.GetLastActionPotentialDuration(90.0)));
                properties.push_back(std::pair<std::string, double>("APD50",props.GetLastActionPotentialDuration(50.0)));
                properties.push_back(std::pair<std::string, double>("APD30",props.GetLastActionPotentialDuration(30.0)));
                properties.push_back(std::pair<std::string, double>("V_max",props.GetLastPeakPotential()));
                properties.push_back(std::pair<std::string, double>("V_min",props.GetLastRestingPotential()));
                properties.push_back(std::pair<std::string, double>("dVdt_max",props.GetLastMaxUpstrokeVelocity()));

                // Save these to a dedicated file for this model, and output to reference data folder in the repository.
                out_stream p_summary_file = handler.OpenOutputFile(model + file_suffix.str() + ".summary");
                for (unsigned i=0; i<properties.size(); i++)
                {
                    std::cout << properties[i].first  << " = " << properties[i].second << std::endl;
                    *p_summary_file << properties[i].first << "\t" << properties[i].second << std::endl;
                }
                p_summary_file->close();
                FileFinder summary_info = handler.FindFile(model + file_suffix.str() + ".summary");
                summary_info.CopyTo(repo_data);
            }
            catch (const Exception& r_e)
            {
                WARNING("Action potential properties calculation failed for model " << model);
            }
        }
    }
};
```
