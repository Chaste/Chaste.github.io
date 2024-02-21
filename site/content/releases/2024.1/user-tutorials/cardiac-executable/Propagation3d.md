---
title: "3D on a realistic cardiac geometry"
draft: false
layout: "single"
images: []
version: "2024.1"
version: "2024.1"
---

{{< callout context="note" title="Getting the data" icon="folder" >}}
Download and save the attached file: [Propagation3d.tgz](/docs/Propagation3d.tgz).
Either use an Archive Manager to extract the contents to disk or save it and then unpack it with

```bash
tar xvfz Propagation3d.tgz
```
{{< /callout >}}


### Running the simulation

Change directory to `Propagation3d`:

```bash
cd Propagation3d
```


In this folder you will find the following files:

* `ChasteParameters.xml` -- this file describes the simulation, and can be used to override the [default parameter values](https://chaste.github.io/doxygen-latest/HeartConfigDefaults_8hpp.html) (in releases of the executable up to and including version 2.0, the default parameters were read in from another xml file, `ChasteDefaults.xml`).
* `ChasteParameters_2_1.xsd` -- XML schema for input validation (in general never has to be altered or touched).


Run the simulation by doing

```
<path_to_chaste>/Chaste ChasteParameters.xml
```

A folder called `testoutput` will appear once the simulation has finished.

### Visualising the results

Move into the newly created output folder

```bash
cd testoutput/ChasteResults
```


In this folder you will find the following files and folders:

* `progress_status.txt`  -- this file can be viewed whilst the simulation is running to gauge how long it will take
* `3dResults.h5` -- the output of the simulation, in HDF5 format
* `output` (folder) -- contains the output converted into Meshalyzer format
* `cmgui_output` (folder) -- contains the output converted into CMGUI format
* `vtk_output` (folder) -- contains the output converted into Paraview (VTK) format


There are more details on visualising your results at ChasteGuides/VisualisationGuides.

### Visualising with Meshalyzer
For Meshalyzer visualisation, now move into the Meshalyzer-compatible output folder

```bash
cd output
```

Launch Meshalyzer with

```
<path_to_meshalyzer>/meshalyzer 3dResults_mesh
```

and visualise the results by loading the `3dResults_V.dat` file.

### Visualising with Cmgui
For Cmgui visualisation, now move into the Cmgui-compatible output folder

```bash
cd cmgui_output
```

Launch the cmgui visualiser with

```
<path_to_cmgui>/cmgui script.com
```

The script will ensure that all the time-step files are loaded into Cmgui.

### Visualising the VTK data with Paraview
For Paraview visualisation, now move into the VTK output folder

```bash
cd vtk_output
```


For easy animation of cardiac simulations, we have written a Python script to add Paraview-specific
time annotation features to the standard VTK output.  Run this with

```
<path_to_Chaste>/python/utils/AddVtuTimeAnnotations.py 3dResults.vtu 3dResultsAnnotated.vtu
```

Launch Paraview with

```bash
paraview --data=3dResultsAnnotated.vtu
```


### Understanding the XML parameters file

Open `ChasteParameters.xml` (it is sensible to do this in a web-browser or XML editor in order to get syntax highlighting).
The file should be reasonably readable; it defines:

* a 3D simulation that lasts for 5ms
* the use of the monodomain model
    * to use bidomain, the only thing that needs to be done is to change `Mono` to `Bi`
* a `LuoRudyIBackwardEuler` cell model as the default cell model
* a 3D mesh generated from an anatomical geometry. The are three files defining the mesh `OxfordRabbitHeart_482um`(`.node`, `.ele`, `.face`) representing respectively nodes elements and faces files.
* an axisymmetric orientation of the fibres is used and is given in the file `OxfordRabbitHeart_482um.axi` where the longitudinal direction of the fibres is defined in each element.
* a stimulated region  is defined in the apex. It starts at the beginning of the simulation and its duration is 2ms.
* output directory and filenames
* an `OutputVisualizer` element giving which visualiser formats to write
* physiological parameters: conductivities, capacitance, surface-area-to-volume ratio
    * in monodomain problems, the defined intracellular conductivity is used, **not** a harmonic mean of intra and extracellular conductivities.
* Numerical parameters including ODE, PDE and printing timesteps
