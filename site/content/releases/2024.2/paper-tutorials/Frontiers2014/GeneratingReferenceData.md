This tutorial was generated from the file projects/Frontiers2014/test/TestGeneratingReferenceDataLiteratePaper.hpp at revision r23346.
Note that the code is given in full at the bottom of the page.



## Generate accurate reference traces and record a target error metric

On this wiki page we describe in detail the code that is used to run this example from the paper.

For each cell model, this runs a single action potential at high fidelity (CVODE with tight tolerance and small max timestep)
as a 'gold standard' result for later comparison.

Also, it runs a single action potential with looser tolerances as a "typical simulation" to give an accuracy benchmark used
to set time steps for other solvers in CalculateRequiredTimesteps.

At the end of this test this information is copied into the file `test/data/error_summary.txt` within the project.

### Code overview

The first thing to do is to include the necessary header files.


```cpp
// The testing framework we use
#include <cxxtest/TestSuite.h>

// Standard C++ libraries
#include <string>
#include <fstream>
#include <iostream>
#include <iomanip>
#include <boost/assign/list_of.hpp>
#include <boost/foreach.hpp>

// Headers specific to this project
#include "CellModelUtilities.hpp"

// General Chaste headers
#include "AbstractCvodeCell.hpp"
#include "CellProperties.hpp"
#include "PetscTools.hpp"
#include "Warnings.hpp"

// This header is needed to allow us to run in parallel
#include "PetscSetupAndFinalize.hpp"
```

Next, we have the class that contains the code to run.
As with most papers using Chaste, this is written as a test suite within our test framework.
The `TestGenerateTraces` method does the work.


```cpp
class TestGeneratingReferenceData : public CxxTest::TestSuite
{
public:
    void TestGenerateTraces() throw (Exception)
    {
```

Set up some references to various files and folders.

```cpp
        FileFinder this_file(__FILE__);
        // Where to copy reference traces within this project
        FileFinder repo_data("data/reference_traces", this_file);
        // Base folder for simulations to write output to
        OutputFileHandler test_base_handler("Frontiers/ReferenceTraces/", false);
```

`CellModelUtilities` is a class of utility functions specifically for this project.
This one gets a list of all the CellML models included.


```cpp
        std::vector<FileFinder> models = CellModelUtilities::GetListOfModels();
```

Iterate over the available models, handling each one on a separate process if running in parallel.

```cpp
        PetscTools::IsolateProcesses();

        for (unsigned i=0; i<models.size(); ++i)
        {
            if (i % PetscTools::GetNumProcs() != PetscTools::GetMyRank())
            {
                continue; // Let another process handle this model
            }
```

Generate the cell model from CellML.

```cpp
            FileFinder& r_model = models[i];
            std::string model_name = r_model.GetLeafNameNoExtension();
            OutputFileHandler handler(test_base_handler.FindFile(model_name));
            boost::shared_ptr<AbstractCardiacCellInterface> p_cell = CellModelUtilities::CreateCellModel(r_model, handler, Solvers::CVODE_NUMERICAL_J, false);
            boost::shared_ptr<AbstractCvodeCell> p_cvode_cell = boost::dynamic_pointer_cast<AbstractCvodeCell>(p_cell);

            // If there's an analytic Jacobian available, we'll switch it on.
            if (p_cvode_cell->HasAnalyticJacobian())
            {
                p_cvode_cell->ForceUseOfNumericalJacobian(false);
            }
```

Set up solver parameters.

```cpp
            p_cvode_cell->SetTolerances(1e-7 /* relative */, 1e-9 /* absolute */);
```

Create a reference solution with high tolerances, and fine output (sampling every 0.1ms).
Note that the sampling interval is also the maximum time step CVODE is allowed to use.


```cpp
            double period = CellModelUtilities::GetDefaultPeriod(p_cell);
            OdeSolution solution;
            try
            {
                solution = p_cvode_cell->Compute(0.0, period, 0.1);
            }
            catch (const Exception &e)
            {
                WARNING(model_name << " model failed to solve. It gave the error:\n" << e.GetMessage());
                continue;
            }
```

Write solution to file, and copy to repository folder.

```cpp
            solution.WriteToFile(handler.GetRelativePath(), model_name, "ms", 1, false, 16, false);
            FileFinder results_dat = handler.FindFile(model_name + ".dat");
            results_dat.CopyTo(repo_data);
            FileFinder results_info = handler.FindFile(model_name + ".info");
            results_info.CopyTo(repo_data);
```

Check that the solution looks like an action potential.

```cpp
            try
            {
                std::vector<double> voltages = solution.GetVariableAtIndex(p_cell->GetVoltageIndex());
                CellProperties props(voltages, solution.rGetTimes());
                std::vector<std::pair<std::string, double> > properties;
```

Calculate some summary statistics of the AP that was produced.

```cpp
                properties.push_back(std::pair<std::string, double>("Num_ODEs", (double)p_cvode_cell->GetNumberOfStateVariables()));
                properties.push_back(std::pair<std::string, double>("APD90", props.GetLastActionPotentialDuration(90.0)));
                properties.push_back(std::pair<std::string, double>("APD50", props.GetLastActionPotentialDuration(50.0)));
                properties.push_back(std::pair<std::string, double>("APD30", props.GetLastActionPotentialDuration(30.0)));
                properties.push_back(std::pair<std::string, double>("V_max", props.GetLastPeakPotential()));
                properties.push_back(std::pair<std::string, double>("V_min", props.GetLastRestingPotential()));
                properties.push_back(std::pair<std::string, double>("dVdt_max", props.GetLastMaxUpstrokeVelocity()));
```

Save these to a dedicated file for this model, and copy to reference data folder in the repository.

```cpp
                out_stream p_summary_file = handler.OpenOutputFile(model_name + ".summary");
                for (unsigned i=0; i<properties.size(); i++)
                {
                    std::cout << properties[i].first  << " = " << properties[i].second << std::endl;
                    *p_summary_file << properties[i].first << "\t" << properties[i].second << std::endl;
                }
                p_summary_file->close();
                FileFinder summary_info = handler.FindFile(model_name + ".summary");
                summary_info.CopyTo(repo_data);
            }
            catch (const Exception& r_e)
            {
                WARNING("Action potential properties calculation failed for model " << model_name);
                continue;
            }
        }
    }
};
```



## Code
The full code is given below


### File name `TestGeneratingReferenceDataLiteratePaper.hpp`


```cpp
// The testing framework we use
#include <cxxtest/TestSuite.h>

// Standard C++ libraries
#include <string>
#include <fstream>
#include <iostream>
#include <iomanip>
#include <boost/assign/list_of.hpp>
#include <boost/foreach.hpp>

// Headers specific to this project
#include "CellModelUtilities.hpp"

// General Chaste headers
#include "AbstractCvodeCell.hpp"
#include "CellProperties.hpp"
#include "PetscTools.hpp"
#include "Warnings.hpp"

// This header is needed to allow us to run in parallel
#include "PetscSetupAndFinalize.hpp"

class TestGeneratingReferenceData : public CxxTest::TestSuite
{
public:
    void TestGenerateTraces() throw (Exception)
    {
        FileFinder this_file(__FILE__);
        // Where to copy reference traces within this project
        FileFinder repo_data("data/reference_traces", this_file);
        // Base folder for simulations to write output to
        OutputFileHandler test_base_handler("Frontiers/ReferenceTraces/", false);

        std::vector<FileFinder> models = CellModelUtilities::GetListOfModels();

        PetscTools::IsolateProcesses();

        for (unsigned i=0; i<models.size(); ++i)
        {
            if (i % PetscTools::GetNumProcs() != PetscTools::GetMyRank())
            {
                continue; // Let another process handle this model
            }

            FileFinder& r_model = models[i];
            std::string model_name = r_model.GetLeafNameNoExtension();
            OutputFileHandler handler(test_base_handler.FindFile(model_name));
            boost::shared_ptr<AbstractCardiacCellInterface> p_cell = CellModelUtilities::CreateCellModel(r_model, handler, Solvers::CVODE_NUMERICAL_J, false);
            boost::shared_ptr<AbstractCvodeCell> p_cvode_cell = boost::dynamic_pointer_cast<AbstractCvodeCell>(p_cell);

            // If there's an analytic Jacobian available, we'll switch it on.
            if (p_cvode_cell->HasAnalyticJacobian())
            {
                p_cvode_cell->ForceUseOfNumericalJacobian(false);
            }

            p_cvode_cell->SetTolerances(1e-7 /* relative */, 1e-9 /* absolute */);

            double period = CellModelUtilities::GetDefaultPeriod(p_cell);
            OdeSolution solution;
            try
            {
                solution = p_cvode_cell->Compute(0.0, period, 0.1);
            }
            catch (const Exception &e)
            {
                WARNING(model_name << " model failed to solve. It gave the error:\n" << e.GetMessage());
                continue;
            }

            solution.WriteToFile(handler.GetRelativePath(), model_name, "ms", 1, false, 16, false);
            FileFinder results_dat = handler.FindFile(model_name + ".dat");
            results_dat.CopyTo(repo_data);
            FileFinder results_info = handler.FindFile(model_name + ".info");
            results_info.CopyTo(repo_data);

            try
            {
                std::vector<double> voltages = solution.GetVariableAtIndex(p_cell->GetVoltageIndex());
                CellProperties props(voltages, solution.rGetTimes());
                std::vector<std::pair<std::string, double> > properties;

                properties.push_back(std::pair<std::string, double>("Num_ODEs", (double)p_cvode_cell->GetNumberOfStateVariables()));
                properties.push_back(std::pair<std::string, double>("APD90", props.GetLastActionPotentialDuration(90.0)));
                properties.push_back(std::pair<std::string, double>("APD50", props.GetLastActionPotentialDuration(50.0)));
                properties.push_back(std::pair<std::string, double>("APD30", props.GetLastActionPotentialDuration(30.0)));
                properties.push_back(std::pair<std::string, double>("V_max", props.GetLastPeakPotential()));
                properties.push_back(std::pair<std::string, double>("V_min", props.GetLastRestingPotential()));
                properties.push_back(std::pair<std::string, double>("dVdt_max", props.GetLastMaxUpstrokeVelocity()));

                out_stream p_summary_file = handler.OpenOutputFile(model_name + ".summary");
                for (unsigned i=0; i<properties.size(); i++)
                {
                    std::cout << properties[i].first  << " = " << properties[i].second << std::endl;
                    *p_summary_file << properties[i].first << "\t" << properties[i].second << std::endl;
                }
                p_summary_file->close();
                FileFinder summary_info = handler.FindFile(model_name + ".summary");
                summary_info.CopyTo(repo_data);
            }
            catch (const Exception& r_e)
            {
                WARNING("Action potential properties calculation failed for model " << model_name);
                continue;
            }
        }
    }
};
```


