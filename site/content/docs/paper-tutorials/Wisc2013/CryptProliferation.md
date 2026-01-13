---
title: "Connecting models to data in multiscale multicellular tissue simulations"
draft: false
layout: "single"
paperTutorialTestFile: "https://github.com/Chaste/project_Wisc2013/blob/8db731800a58c7ffb15b949c87cfd397adb4e5a7/test/TestCryptProliferationLiteratePaper.hpp"
---

Note that the code is given in full at the bottom of the page.

This Chaste test file runs the main protocols for the above
[paper published in ICCS2013](http://dx.doi.org/10.1016/j.procs.2013.05.235).

### How to run this code

For performance, it is recommended to build Chaste using the `GccOptNative` build type when using
the Functional Curation extension project, on which this code is built.  You can run the code shown
below using the commands:

```bash
cd path_to_Chaste
scons chaste_libs=1 build=GccOptNative projects/Wisc2013/test/TestCryptProliferationLiteratePaper.hpp
```

A clean build of Chaste takes a considerable amount of time.  If you have multiple cores available
then the process can be sped up greatly using the '-j' flag to scons, e.g.

```bash
scons -j4 chaste_libs=1 build=GccOptNative projects/Wisc2013/test/TestCryptProliferationLiteratePaper.hpp
```

to build on 4 cores.  You can additionally run the code itself in parallel, in order to run each value
in the main parameter sweep simultaneously, using 5 cores with the `GccOptNative_5` build type, e.g.

```bash
scons -j4 chaste_libs=1 build=GccOptNative_5 projects/Wisc2013/test/TestCryptProliferationLiteratePaper.hpp
```

With these settings on our test machine, reproducing the paper results takes about 19 hours.

### The code itself

The first step is to include the header files we need.  This code is written as a Chaste test suite, for
easy execution using the Chaste build framework.  We thus need to include the `TestSuite.h` header, along
with various system libraries, Functional Curation headers, and functionality from core Chaste.


```cpp
#include <cxxtest/TestSuite.h>

#include <vector>
#include <boost/assign/list_of.hpp>
#include <boost/make_shared.hpp>
#include <boost/foreach.hpp>

// Code in this project, defining the crypt model
#include "CryptProliferationModel.hpp"

// Functional Curation headers
#include "Protocol.hpp"
#include "ProtocolParser.hpp"
#include "ProtocolFileFinder.hpp"
#include "ValueExpression.hpp"

// Core Chaste headers
#include "FileFinder.hpp"
#include "OutputFileHandler.hpp"
#include "PetscTools.hpp"
#include "NumericFileComparison.hpp"
```

This final header, from core Chaste, is needed to enable running in parallel.

```cpp
#include "PetscSetupAndFinalize.hpp"

class TestCryptProliferationLiteratePaper : public CxxTest::TestSuite
{
```


The helper method below runs the given protocol on three different cell-based Chaste models,
writing protocol outputs to the given folder.

Optionally some of the protocol inputs may be overridden by providing a non-empty map
as the third argument.

The fourth argument modelsInParallel specifies whether, if multiple processes are available,
to run the protocol on multiple models simultaneously, or whether the protocol should try to
parallelise internally.

If the copyPlots argument is given as true, then all automatically generated results
plots in the sub-folder for each model will be copied to the parent results folder,
with names that include the model name, for easy inclusion in the paper.

If the rCheckResults vector is non-empty, then this list of results data files will be
checked against recorded values, in order to ensure that the simulation results have not changed.


```cpp
    void RunProtocol(const std::string& rProtocolName, const std::string& rOutputFolderName,
                     const std::map<std::string, double>& rProtocolInputs,
                     bool modelsInParallel,
                     bool copyPlots=false,
                     const std::vector<std::string>& rCheckResults=std::vector<std::string>())
    {
```

Create the folder to which outputs should be written.

```cpp
        OutputFileHandler handler(rOutputFolderName);
```

Locate the protocol definition on the file system.

```cpp
        FileFinder this_test(__FILE__, RelativeTo::ChasteSourceRoot);
        ProtocolFileFinder proto_file("protocols/" + rProtocolName + ".txt", this_test);

        if (modelsInParallel)
        {
```

Allow the different models to be run simultaneously, if multiple processes are available.

```cpp
            PetscTools::IsolateProcesses(true);
        }
```

Loop over available (cell cycle) models.

```cpp
        std::vector<CryptProliferationModel::ModelType> model_types = boost::assign::list_of
                (CryptProliferationModel::UNIFORM_WNT)
                (CryptProliferationModel::VARIABLE_WNT)
                (CryptProliferationModel::STOCHASTIC_GEN_BASED);
        for (unsigned i=0; i<model_types.size(); i++)
        {
            if (modelsInParallel && PetscTools::IsParallel() && i % PetscTools::GetNumProcs() != PetscTools::GetMyRank())
            {
                // Let another process run this model
                continue;
            }
```

Get a human readable name for the model to run in this loop iteration.

```cpp
            CryptProliferationModel::ModelType model_type = model_types[i];
            std::string model_name = CryptProliferationModel::GetModelName(model_type);
```

Output for each model gets written to a sub-folder of the main output folder, named after the model.

```cpp
            std::string sub_folder_name = model_name;
            FileFinder::ReplaceSpacesWithUnderscores(sub_folder_name);
            OutputFileHandler sub_handler(handler.FindFile(sub_folder_name));
```

Load the model to simulate.

```cpp
            boost::shared_ptr<AbstractSystemWithOutputs> p_model(new CryptProliferationModel(model_type));
```

Load the protocol to run on it.

```cpp
            ProtocolParser parser;
            ProtocolPtr p_protocol = parser.ParseFile(proto_file);
            p_protocol->SetOutputFolder(sub_handler);
            p_protocol->SetModel(p_model);
```

As an alternative to running different models on different processes, the Functional Curation system
can also parallelise nested simulation loops automatically in some circumstances.  This line turns
that functionality on if modelsInParallel is false, which is the case for the main parameter sweep.
Thus while generating the steady state plots can use at most 3 processes (corresponding to the 3 cell
cycle models) the parameter sweep can use up to 5 (the number of crypt heights to test).


```cpp
            p_protocol->SetParalleliseLoops(!modelsInParallel);
```

Override some of the protocol's inputs if requested.

```cpp
            typedef std::pair<std::string, double> StringDoublePair;
            BOOST_FOREACH(StringDoublePair input, rProtocolInputs)
            {
                p_protocol->SetInput(input.first, boost::make_shared<ValueExpression>(boost::make_shared<SimpleValue>(input.second)));
            }
```

By default the Functional Curation system uses the plot titles specified in the protocol, and names
the generated files after the title too.  However, where multiple models are being simulated under
the same protocol, it is more useful to title plots based on the model name.  We also add a sub-figure
index, and adjust the plot page size, so that the generated figures can be included directly in the paper.


```cpp
            std::string letter(1, 'a' + model_type);
            std::string plot_title = letter + ") " + model_name;
            BOOST_FOREACH(PlotSpecificationPtr p_plot_spec, p_protocol->rGetPlotSpecifications())
            {
                p_plot_spec->SetDisplayTitle(plot_title);
                p_plot_spec->SetGnuplotTerminal("postscript eps enhanced size 4,3 font 16");
            }
```

Finally, run the protocol on this model, using 'outputs' as the prefix for result file names.

```cpp
            try
            {
                p_protocol->RunAndWrite("outputs");
```

Optionally copy generated plots, as described above.  We find all .eps files in the sub-folder,
and copy them, with a different name, into the main output folder.


```cpp
                if (copyPlots && PetscTools::AmMaster())
                {
                    FileFinder model_output_folder = sub_handler.FindFile("");
                    BOOST_FOREACH(FileFinder graph, model_output_folder.FindMatches("*.eps"))
                    {
                        FileFinder dest = handler.FindFile(sub_folder_name + "-" + graph.GetLeafName());
                        graph.CopyTo(dest);
                    }
                }
```

Check against recorded values for specific results files.

```cpp
                BOOST_FOREACH(const std::string& r_result_name, rCheckResults)
                {
                    std::string csv_name = "outputs_" + r_result_name + ".csv";
                    FileFinder new_data = sub_handler.FindFile(csv_name);
                    FileFinder reference_data("data/" + sub_folder_name + "-" + csv_name, this_test);
                    NumericFileComparison comp(new_data, reference_data, false);
                    // The arguments to CompareFiles are absolute tolerance, number of header lines, relative tolerance
                    TS_ASSERT(comp.CompareFiles(1e-4, 1, 1e-6));
                }
            }
            catch (const Exception& r_error)
            {
```

If an error occurs while running the protocol etc. we display the error message,
but don't terminate execution (since the other models may run successfully).


```cpp
                std::cerr << r_error.GetMessage() << std::endl;
                TS_FAIL("Error running " + model_name);
            }
        }

        if (modelsInParallel)
        {
            // Stop isolating processes, to avoid problems running the next protocol.
            PetscTools::IsolateProcesses(false);
        }
    }

public:
```


This test runs the inner `CryptProliferation` protocol on each model, for the default crypt
height of 10 nominal cell diameters.  The raw results from the underlying cell-based Chaste
simulation can then be used with the Chaste visualisation tools to produce the crypt schematic
figure in the paper (Figure 1).

To visualise the results, open a new terminal, `cd` to the Chaste directory,
then `cd` to `anim`. Then do:

```bash
java -cp . Visualize2dCentreCells /tmp/$USER/testoutput/CryptProliferationSteadyState/Stochastic_Generation-based/raw_results/results_from_time_0
```

and

```bash
java -cp . Visualize2dCentreCells /tmp/$USER/testoutput/CryptProliferationSteadyState/Uniform_Wnt/raw_results/results_from_time_0
```


You may have to do "`javac Visualize2dCentreCells.java`" beforehand to create the java executable.
See ChasteGuides/RunningCellBasedVisualization for more detail on the visualisation tool.


```cpp
    void TestGenerateSteadyStatePlots() throw (Exception)
    {
        std::map<std::string, double> protocol_inputs;
        protocol_inputs["end_time"] = 130.0;
        protocol_inputs["steady_state_time"] = 0.0;
        RunProtocol("CryptProliferation", "CryptProliferationSteadyState", protocol_inputs, true, false);
    }
```

This test runs the main parameter sweep protocol on each of our three variant models, producing
plots (a)-(c) in Figure 2.


```cpp
    void TestParameterSweep() throw (Exception)
    {
        std::map<std::string, double> protocol_inputs;
        std::vector<std::string> outputs_to_check = boost::assign::list_of("heights")("freqs")("norm_freqs");
        RunProtocol("CryptProliferationSweep", "CryptProliferationSweep", protocol_inputs, false, true, outputs_to_check);
    }
};
```



## Code
The full code is given below


### File: `TestCryptProliferationLiteratePaper.hpp`


```cpp
#include <cxxtest/TestSuite.h>

#include <vector>
#include <boost/assign/list_of.hpp>
#include <boost/make_shared.hpp>
#include <boost/foreach.hpp>

// Code in this project, defining the crypt model
#include "CryptProliferationModel.hpp"

// Functional Curation headers
#include "Protocol.hpp"
#include "ProtocolParser.hpp"
#include "ProtocolFileFinder.hpp"
#include "ValueExpression.hpp"

// Core Chaste headers
#include "FileFinder.hpp"
#include "OutputFileHandler.hpp"
#include "PetscTools.hpp"
#include "NumericFileComparison.hpp"

#include "PetscSetupAndFinalize.hpp"

class TestCryptProliferationLiteratePaper : public CxxTest::TestSuite
{
    void RunProtocol(const std::string& rProtocolName, const std::string& rOutputFolderName,
                     const std::map<std::string, double>& rProtocolInputs,
                     bool modelsInParallel,
                     bool copyPlots=false,
                     const std::vector<std::string>& rCheckResults=std::vector<std::string>())
    {
        OutputFileHandler handler(rOutputFolderName);
        FileFinder this_test(__FILE__, RelativeTo::ChasteSourceRoot);
        ProtocolFileFinder proto_file("protocols/" + rProtocolName + ".txt", this_test);

        if (modelsInParallel)
        {
            PetscTools::IsolateProcesses(true);
        }

        std::vector<CryptProliferationModel::ModelType> model_types = boost::assign::list_of
                (CryptProliferationModel::UNIFORM_WNT)
                (CryptProliferationModel::VARIABLE_WNT)
                (CryptProliferationModel::STOCHASTIC_GEN_BASED);
        for (unsigned i=0; i<model_types.size(); i++)
        {
            if (modelsInParallel && PetscTools::IsParallel() && i % PetscTools::GetNumProcs() != PetscTools::GetMyRank())
            {
                // Let another process run this model
                continue;
            }

            CryptProliferationModel::ModelType model_type = model_types[i];
            std::string model_name = CryptProliferationModel::GetModelName(model_type);

            std::string sub_folder_name = model_name;
            FileFinder::ReplaceSpacesWithUnderscores(sub_folder_name);
            OutputFileHandler sub_handler(handler.FindFile(sub_folder_name));

            boost::shared_ptr<AbstractSystemWithOutputs> p_model(new CryptProliferationModel(model_type));

            ProtocolParser parser;
            ProtocolPtr p_protocol = parser.ParseFile(proto_file);
            p_protocol->SetOutputFolder(sub_handler);
            p_protocol->SetModel(p_model);

            p_protocol->SetParalleliseLoops(!modelsInParallel);

            typedef std::pair<std::string, double> StringDoublePair;
            BOOST_FOREACH(StringDoublePair input, rProtocolInputs)
            {
                p_protocol->SetInput(input.first, boost::make_shared<ValueExpression>(boost::make_shared<SimpleValue>(input.second)));
            }

            std::string letter(1, 'a' + model_type);
            std::string plot_title = letter + ") " + model_name;
            BOOST_FOREACH(PlotSpecificationPtr p_plot_spec, p_protocol->rGetPlotSpecifications())
            {
                p_plot_spec->SetDisplayTitle(plot_title);
                p_plot_spec->SetGnuplotTerminal("postscript eps enhanced size 4,3 font 16");
            }

            try
            {
                p_protocol->RunAndWrite("outputs");

                if (copyPlots && PetscTools::AmMaster())
                {
                    FileFinder model_output_folder = sub_handler.FindFile("");
                    BOOST_FOREACH(FileFinder graph, model_output_folder.FindMatches("*.eps"))
                    {
                        FileFinder dest = handler.FindFile(sub_folder_name + "-" + graph.GetLeafName());
                        graph.CopyTo(dest);
                    }
                }

                BOOST_FOREACH(const std::string& r_result_name, rCheckResults)
                {
                    std::string csv_name = "outputs_" + r_result_name + ".csv";
                    FileFinder new_data = sub_handler.FindFile(csv_name);
                    FileFinder reference_data("data/" + sub_folder_name + "-" + csv_name, this_test);
                    NumericFileComparison comp(new_data, reference_data, false);
                    // The arguments to CompareFiles are absolute tolerance, number of header lines, relative tolerance
                    TS_ASSERT(comp.CompareFiles(1e-4, 1, 1e-6));
                }
            }
            catch (const Exception& r_error)
            {
                std::cerr << r_error.GetMessage() << std::endl;
                TS_FAIL("Error running " + model_name);
            }
        }

        if (modelsInParallel)
        {
            // Stop isolating processes, to avoid problems running the next protocol.
            PetscTools::IsolateProcesses(false);
        }
    }

public:
    void TestGenerateSteadyStatePlots() throw (Exception)
    {
        std::map<std::string, double> protocol_inputs;
        protocol_inputs["end_time"] = 130.0;
        protocol_inputs["steady_state_time"] = 0.0;
        RunProtocol("CryptProliferation", "CryptProliferationSteadyState", protocol_inputs, true, false);
    }

    void TestParameterSweep() throw (Exception)
    {
        std::map<std::string, double> protocol_inputs;
        std::vector<std::string> outputs_to_check = boost::assign::list_of("heights")("freqs")("norm_freqs");
        RunProtocol("CryptProliferationSweep", "CryptProliferationSweep", protocol_inputs, false, true, outputs_to_check);
    }
};
```




### File:  `protocols/CryptProliferationSweep.txt`

```yaml
## A simple parameter sweep over the crypt proliferation protocol, varying crypt height

inputs {
    num_boxes = 10                  ## The number of boxes to use in the location histogram
    heights = [10, 15, 20, 25, 30]  ## The crypt heights to sweep over
}
import std = '../../../FunctionalCuration/src/proto/library/BasicLibrary.xml'
units { percent = dimensionless "%" }
tasks {
    simulation sweep = nested {
        range crypt_height units lengthUnits vector heights
        nests protocol 'CryptProliferation.txt' {
            num_boxes = num_boxes         ## Pass through
            crypt_height = crypt_height   ## Set crypt height for this iteration
            ## Output of interest, with shape [num_boxes] for a single protocol run
            select output freqs
        }? ## Turn on debug tracing, so the outputs of each run are saved separately
    }
}
post-processing {
    ## Compute box centres as % of crypt height, for plotting all crypts on the same axes
    centres_percent = [(100/num_boxes)*(box_num+0.5)  for box_num in 0:num_boxes]
    ## Normalise division counts for easier comparison
    total_divisions = std:Stretch(std:Sum(sweep:freqs, 1), num_boxes, 1)
    norm_freqs = map(lambda n, tot: n/tot*100, sweep:freqs, total_divisions)
}
outputs {
    freqs = sweep:freqs   units dimensionless  "Number of divisions per box"
    norm_freqs            units percent        "Percentage of divisions per box"
    centres_percent       units percent        "Percentage height up the crypt"
    heights               units dimensionless  "Crypt height"  ## Note: fake units for display
}
plots {
    plot 'Cell division locations' { norm_freqs against centres_percent key heights }
}
```




### File:  `protocols/CryptProliferation.txt`

```yaml
## Core protocol for the Crypt Proliferation project, containing a single cell-based simulation and post-processing thereof

## The 'ontology' to use for referencing model variables
namespace cellbased = 'https://chaste.cs.ox.ac.uk/nss/cellbased/0.1#'
inputs {    ## Protocol inputs
    num_boxes = 10       ## The number of boxes to use in the location histogram
    crypt_height = 20    ## The height of the crypt (in nominal cell diameters)
    end_time = 2200       ## The simulation end time (hours)
    ## The time at which the system is assumed to have reached quasi steady state (hours).
    ## We ignore division events occurring before this point.
    steady_state_time = 200
}
## Import the standard library of post-processing operations, using a relative path.
## Functions from this library may then be used by prefixing their names with 'std:'.
import std = '../../../FunctionalCuration/src/proto/library/BasicLibrary.xml'
library {   ## Define some extra utility functions
    def InBox(loc, boxLow, boxHigh) { return loc >= boxLow && loc < boxHigh }
    ## Extend an array by copying it a given number of times along a newly added dimension
    Stretch = lambda array, length, dim: [array for dim$i in 0:length]
}
units {     ## Units definitions for this protocol
    hours = 3600 second
    lengthUnits = 10 micro metre "Nominal cell diameters"
}
tasks {     ## The raw simulations to perform
    ## Just run the cell-based simulation as-is, setting a few parameters at the start
    simulation sim = oneStep {
        modifiers {
            at start set cellbased:end_time = end_time
            at start set cellbased:crypt_length = crypt_height
            at start set cellbased:cells_up = MathML:ceiling(crypt_height * 2 / MathML:root(3))
        }
    }
}
post-processing {
    ## The main simulation output is the 2d array of division data, with 4 columns:
    ## time, x, y, age.  We extract division y coordinates for events after the given time.
    locations = std:After(sim:divisions[1$2], sim:divisions[1$0], steady_state_time)
    num_divisions = locations.SHAPE[0]

    ## Determine the histogram boxes, noting that a few divisions can occur below or above the nominal crypt bounds
    box_size = crypt_height / num_boxes  ## y coordinates nominally start at zero
    box_lows = std:Join([MathML:min(std:Min(locations)[0], 0.0)],
                        [i*box_size for i in 1:num_boxes])
    box_highs = std:Join([(i+1)*box_size for i in 0:num_boxes-1],
                         [MathML:max(std:Max(locations)[0]*1.00001, crypt_height)])
    centres = map(lambda a, b: (a+b)/2, box_lows, box_highs)

    ## Figure out which histogram box each cell division occurred in, and count them up
    locations_ext = Stretch(locations, num_boxes, 0)       ## Make all the _ext arrays the same
    box_lows_ext = Stretch(box_lows, num_divisions, 1)     ## shape: [num_boxes, num_divisions]
    box_highs_ext = Stretch(box_highs, num_divisions, 1)
    in_box_pattern = map(InBox, locations_ext, box_lows_ext, box_highs_ext)
    freqs = std:RemoveDim(std:Sum(in_box_pattern), 1)            ## Shape [num_boxes]
    assert std:RemoveDim(std:Sum(freqs), 0) == num_divisions     ## Sanity check
}
outputs {
    divisions = sim:divisions     "Raw division data"            ## Shape [num_divisions, 4]
    freqs     units dimensionless "Number of divisions per box"  ## Shape [num_boxes]
    centres   units lengthUnits   "Box centres"                  ## Shape [num_boxes]
}
plots {
    plot 'Cell division locations' { freqs against centres }
}
```


