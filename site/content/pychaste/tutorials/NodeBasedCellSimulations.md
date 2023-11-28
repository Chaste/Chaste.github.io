---
title : "Node Based Cell Simulations Tutorial"
summary: ""
draft: false
images: []
toc: true
---
This tutorial is automatically generated from the file test/python/cell_based/tutorials/TestNodeBasedCellSimulationsPythonTutorial.ipynb.

```
# Jupyter notebook specific imports 
import matplotlib as mpl 
from IPython import display 
%matplotlib inline
```
## Introduction
In this tutorial we show how Chaste can be used to create, run and visualize node-based simulations. Full details of the mechanical model can be found in Pathamathan et
al "A computational study of discrete mechanical tissue models", Physical Biology. Vol. 6. No. 3. 2009.. DOI (10.1088/1478-3975/6/3/036001).
### The Test

```
import matplotlib.pyplot as plt # Plotting
import numpy as np # Matrix tools
import chaste # The PyChaste module
chaste.init() # Set up MPI
import chaste.cell_based # Contains cell populations
import chaste.mesh # Contains meshes
import chaste.visualization # Visualization tools
```
### Test 1 - A basic node-based simulation
In the first test, we run a simple node-based simulation, in which we create a monolayer of cells,
using a nodes only mesh. Each cell is assigned a uniform cell-cycle model.

```
# Set up the test 
chaste.cell_based.SetupNotebookTest()
```
The first thing we do is generate a nodes only mesh. To do this we first create a `MutableMesh` to use as a generating mesh.
To do this we can use the `HoneycombMeshGenerator`. This generates a honeycomb-shaped mesh, in which all nodes are equidistant.
Here the first and second arguments define the size of the mesh - we have chosen a mesh that is 2 nodes (i.e. cells) wide, and 2 nodes high.

```
file_handler = chaste.core.OutputFileHandler("Python/TestNodeBasedCellSimulationsTutorial")
generator = chaste.mesh.HoneycombMeshGenerator(2, 2)
generating_mesh = generator.GetMesh()
```
Once we have a MutableMesh we can generate a NodesOnlyMesh from it using the following commands.
Note you can also generate the NodesOnlyMesh from a collection of nodes.

```
mesh = chaste.mesh.NodesOnlyMesh2()
```
To run node-based simulations you need to define a cut off length (second argument in `ConstructNodesWithoutMesh`),
which defines the connectivity of the nodes by defining a radius of interaction.

```
mesh.ConstructNodesWithoutMesh(generating_mesh, 1.5)
```
Having created a mesh, we now create a (wrapped) vector of CellPtrs. To do this, we use the `CellsGenerator` helper class,
which is specialized for the type of cell model required (here `UniformCellCycleModel`) and the dimension.
We create an empty vector of cells and pass this into the method along with the mesh.
The second argument represents the size of that the vector cells should become - one cell for each node,
the third argument specifies the proliferative type of the cell.

```
cells = chaste.cell_based.VecCellPtr()
transit_type = chaste.cell_based.TransitCellProliferativeType()
cell_generator = chaste.cell_based.CellsGeneratorUniformCellCycleModel_2()
cell_generator.GenerateBasicRandom(cells, mesh.GetNumNodes(), transit_type)
```
Now we have a mesh and a set of cells to go with it, we can create a `CellPopulation`.
In general, this class associates a collection of cells with a mesh. For this test,
because we have a `NodesOnlyMesh`, we use a particular type of cell population called a `NodeBasedCellPopulation`.

```
cell_population = chaste.cell_based.NodeBasedCellPopulation2(mesh, cells)
```
We can set up a `VtkScene` to do a quick visualization of the population before running the analysis.

```
scene = chaste.visualization.VtkScene2()
scene.SetCellPopulation(cell_population)
nb_manager = chaste.visualization.JupyterNotebookManager()
nb_manager.vtk_show(scene, height=600)
```

   
We then pass in the cell population into an `OffLatticeSimulation`, and set the output directory, output multiple and end time

```
simulator = chaste.cell_based.OffLatticeSimulation2_2(cell_population)
simulator.SetOutputDirectory("Python/TestNodeBasedCellSimulationsTutorial")
simulator.SetSamplingTimestepMultiple(100)
simulator.SetEndTime(10.0)
```
We now pass a force law to the simulation.

```
force = chaste.cell_based.GeneralisedLinearSpringForce2_2()
simulator.AddForce(force)
```
Save snapshot images of the population during the simulation

```
scene_modifier = chaste.visualization.JupyterSceneModifier2(nb_manager)
scene_modifier.SetVtkScene(scene)
scene_modifier.SetUpdateFrequency(100)
simulator.AddSimulationModifier(scene_modifier)
```
To run the simulation, we call `Solve()`. We can again do a quick rendering of the population at the end of the simulation
scene.Start()

```
simulator.Solve()
scene.End()
```

The next two lines are for test purposes only and are not part of this tutorial.
If different simulation input parameters are being explored the lines should be removed.

```
## Tear down the test 
chaste.cell_based.TearDownNotebookTest()
```
### Test 2 - a basic node-based simulation in 3D
In the second test we run a simple node-based simulation in 3D. This is very similar to the 2D test with the dimension changed from 2 to 3 and
instead of using a mesh generator we generate the nodes directly.

```
# Set up the test 
chaste.cell_based.SetupNotebookTest()
```
First, we generate a nodes only mesh. This time we specify the nodes manually by first creating a vector of nodes

```
file_handler = chaste.core.OutputFileHandler("Python/TestNodeBasedCellSimulationsSpheroidTutorial")
nodes = []
nodes.append(chaste.mesh.Node3(0, False, 0.5, 0.0, 0.0))
nodes.append(chaste.mesh.Node3(1, False, -0.5, 0.0, 0.0))
nodes.append(chaste.mesh.Node3(2, False, 0.0, 0.5, 0.0))
nodes.append(chaste.mesh.Node3(3, False, 0.0, -0.5, 0.0))
```
Finally a NodesOnlyMesh is created and the vector of nodes is passed to the ConstructNodesWithoutMesh method.

```
mesh = chaste.mesh.NodesOnlyMesh3()
```
To run node-based simulations you need to define a cut off length (second argument in ConstructNodesWithoutMesh),
which defines the connectivity of the nodes by defining a radius of interaction.

```
mesh.ConstructNodesWithoutMesh(nodes, 1.5)
```
Having created a mesh, we now create a std::vector of CellPtrs.
As before, we do this with the CellsGenerator helper class (this time with dimension 3).

```
cells = chaste.cell_based.VecCellPtr()
transit_type = chaste.cell_based.TransitCellProliferativeType()
cell_generator = chaste.cell_based.CellsGeneratorUniformCellCycleModel_3()
cell_generator.GenerateBasicRandom(cells, mesh.GetNumNodes(), transit_type)
```
Now we have a mesh and a set of cells to go with it, we can create a `CellPopulation`.
In general, this class associates a collection of cells with a mesh. For this test,
because we have a `NodesOnlyMesh`, we use a particular type of cell population called a `NodeBasedCellPopulation`.

```
cell_population = chaste.cell_based.NodeBasedCellPopulation3(mesh, cells)
```
We can set up a `VtkScene` to do a quick visualization of the population before running the analysis.

```
scene = chaste.visualization.VtkScene3()
scene.SetCellPopulation(cell_population)
nb_manager.vtk_show(scene, height=600)
```

We then pass in the cell population into an `OffLatticeSimulation`, and set the output directory, output multiple and end time

```
simulator = chaste.cell_based.OffLatticeSimulation3_3(cell_population)
simulator.SetOutputDirectory("Python/TestNodeBasedCellSimulationsSpheroidTutorial")
simulator.SetSamplingTimestepMultiple(12)
simulator.SetEndTime(10.0)
```
We now pass a force law to the simulation.

```
force = chaste.cell_based.GeneralisedLinearSpringForce3_3()
simulator.AddForce(force)
```
Save snapshot images of the population during the simulation

```
scene_modifier = chaste.visualization.JupyterSceneModifier3(nb_manager)
scene_modifier.SetVtkScene(scene)
scene_modifier.SetUpdateFrequency(100)
simulator.AddSimulationModifier(scene_modifier)
```
To run the simulation, we call `Solve()`. We can again do a quick rendering of the population at the end of the simulation

```
scene.Start()
simulator.Solve()
scene.End()
```

The next two lines are for test purposes only and are not part of this tutorial.
If different simulation input parameters are being explored the lines should be removed.

```
## Tear down the test 
chaste.cell_based.TearDownNotebookTest()
```
### Test 3 - a node-based simulation on a restricted geometry
In the second test we run a simple node-based simulation in 3D. This is very similar to the 2D test with the dimension changed from 2 to 3 and
instead of using a mesh generator we generate the nodes directly.

```
# Set up the test 
chaste.cell_based.SetupNotebookTest()
```
In the third test we run a node-based simulation restricted to the surface of a sphere.

```
file_handler = chaste.core.OutputFileHandler("Python/TestNodeBasedCellSimulationsRestrictedSpheroidTutorial")
nodes = []
nodes.append(chaste.mesh.Node3(0, False, 0.5, 0.0, 0.0))
nodes.append(chaste.mesh.Node3(1, False, -0.5, 0.0, 0.0))
nodes.append(chaste.mesh.Node3(2, False, 0.0, 0.5, 0.0))
nodes.append(chaste.mesh.Node3(3, False, 0.0, -0.5, 0.0))
mesh = chaste.mesh.NodesOnlyMesh3()
```
To run node-based simulations you need to define a cut off length (second argument in ConstructNodesWithoutMesh),
which defines the connectivity of the nodes by defining a radius of interaction.

```
mesh.ConstructNodesWithoutMesh(nodes, 1.5)
cells = chaste.cell_based.VecCellPtr()
transit_type = chaste.cell_based.TransitCellProliferativeType()
cell_generator = chaste.cell_based.CellsGeneratorUniformCellCycleModel_3()
cell_generator.GenerateBasicRandom(cells, mesh.GetNumNodes(), transit_type)
cell_population = chaste.cell_based.NodeBasedCellPopulation3(mesh, cells)
```
We can set up a `VtkScene` to do a quick visualization of the population before running the analysis.

```
scene = chaste.visualization.VtkScene3()
scene.SetCellPopulation(cell_population)
nb_manager.vtk_show(scene, height=600)
simulator = chaste.cell_based.OffLatticeSimulation3_3(cell_population)
simulator.SetOutputDirectory("Python/TestNodeBasedCellSimulationsRestrictedSpheroidTutorial")
simulator.SetSamplingTimestepMultiple(12)
simulator.SetEndTime(10.0)
```
We now pass a force law to the simulation.

```
force = chaste.cell_based.GeneralisedLinearSpringForce3_3()
simulator.AddForce(force)
```
This time we create a CellPopulationBoundaryCondition and pass this to the OffLatticeSimulation.
Here we use a SphereGeometryBoundaryCondition which restricts cells to lie on a sphere (in 3D) or circle (in 2D).
For a list of possible boundary conditions see subclasses of AbstractCellPopulationBoundaryCondition.
Note that some of these boundary conditions are not compatible with node-based simulations see the specific class documentation
for details, if you try to use an incompatible class then you will receive a warning.
First we set the centre (0,0,1) and radius of the sphere (1).

```
centre = (0.0, 0.0, 1.0)
radius = 5.0
boundary_condition = chaste.cell_based.SphereGeometryBoundaryCondition3(cell_population, centre, radius)
simulator.AddCellPopulationBoundaryCondition(boundary_condition)
```
Save snapshot images of the population during the simulation
scene_modifier = chaste.cell_based.VtkSceneModifier3()

```
scene_modifier.SetVtkScene(scene)
scene_modifier.SetUpdateFrequency(100)
simulator.AddSimulationModifier(scene_modifier)
```
To run the simulation, we call `Solve()`. We can again do a quick rendering of the population at the end of the simulation
scene.Start()

```
simulator.Solve()
scene.End()
```
    
The next two lines are for test purposes only and are not part of this tutorial.
If different simulation input parameters are being explored the lines should be removed.

```
## Tear down the test 
chaste.cell_based.TearDownNotebookTest()
```
