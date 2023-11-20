---
title : "Spheroid Tutorial"
summary: ""
draft: false
images: []
toc: true
---
This tutorial is automatically generated from the file test/python/cell_based/tutorials/TestSpheroidTutorial.ipynb.

```
# Jupyter notebook specific imports 
import matplotlib as mpl 
from IPython import display 
%matplotlib inline
```
## Introduction
This tutorial is an example of modelling spheroid growth with a nutrient.
It covers:
 * Setting up an off-lattice cell population
 * Setting up a cell cycle model with oxygen dependence
 * Setting up and solving an oxygen transport PDE
 * Setting up a cell killer
 ### Imports and Setup

```
import matplotlib.pyplot as plt # Plotting
import numpy as np # Matrix tools
import chaste # The PyChaste module
chaste.init() # Set up MPI
import chaste.cell_based # Contains cell populations
import chaste.mesh # Contains meshes
import chaste.visualization # Visualization tools
import chaste.pde ## PDEs 
```
### Test 1 - a 2D mesh-based spheroid
In this test we set up a spheroid with a plentiful supply of oxygen on the boundary and watch it grow
over time. Cells can gradually become apoptotic if the oxygen tension is too low.

```
# Set up the test 
chaste.cell_based.SetupNotebookTest()
```
This time we will use on off-lattice `MeshBased` cell population. Cell centres are joined with
springs with a Delauney Triangulation used to identify neighbours. Cell area is given by the dual
(Voronoi Tesselation). We start off with a small number of cells. We use a `MutableMesh` which
can change connectivity over time and a `HoneycombMeshGenerator` to set it up with a simple
honeycomb pattern. Here the first and second arguments define the size of the mesh -
we have chosen a mesh that is 5 nodes (i.e. cells) wide, and 5 nodes high. The extra '2' argument puts
two layers of non-cell elements around the mesh, which help to form a nicer voronoi tesselation
for area calculations.

```
file_handler = chaste.core.OutputFileHandler("Python/TestSpheroidTutorial")
generator = chaste.mesh.HoneycombMeshGenerator(5, 5)
mesh = generator.GetMesh()
```
We create some cells next, with a stem-like proliferative type. This means they will continually
proliferate if there is enough oxygen, similar to how a tumour spheroid may behave.

```
cells = chaste.cell_based.VecCellPtr()
stem_type = chaste.cell_based.StemCellProliferativeType()
cell_generator = chaste.cell_based.CellsGeneratorSimpleOxygenBasedCellCycleModel_2()
cell_generator.GenerateBasicRandom(cells, mesh.GetNumNodes(), stem_type)
```
Define when cells become apoptotic

```
for eachCell in cells:
    cell_cycle_model = eachCell.GetCellCycleModel()
    cell_cycle_model.SetDimension(2)
    cell_cycle_model.SetStemCellG1Duration(4.0)
    cell_cycle_model.SetHypoxicConcentration(0.1)
    cell_cycle_model.SetQuiescentConcentration(0.3)
    cell_cycle_model.SetCriticalHypoxicDuration(8)
    g1_duration = cell_cycle_model.GetStemCellG1Duration()
    sg2m_duration = cell_cycle_model.GetSG2MDuration()
    rnum = chaste.core.RandomNumberGenerator.Instance().ranf()
    birth_time = -rnum * (g1_duration + sg2m_duration)
    eachCell.SetBirthTime(birth_time);
```
Now we have a mesh and a set of cells to go with it, we can create a `CellPopulation` as before.

```
cell_population = chaste.cell_based.MeshBasedCellPopulation2_2(mesh, cells)
```
To view the results of this and the next test in Paraview it is necessary to explicitly generate the required .vtu files.

```
cell_population.AddPopulationWriterVoronoiDataWriter()
```
We then pass in the cell population into an `OffLatticeSimulation`, and set the output directory and end time.

```
simulator = chaste.cell_based.OffLatticeSimulation2_2(cell_population)
simulator.SetOutputDirectory("Python/TestSpheroidTutorial")
simulator.SetEndTime(5.0)
```
We ask for output every 12 increments

```
simulator.SetSamplingTimestepMultiple(100)
```
We define how the springs between cells behave using a force law.

```
force = chaste.cell_based.GeneralisedLinearSpringForce2_2()
simulator.AddForce(force)
```
We set up a PDE for oxygen diffusion and consumption by cells, setting the rate of consumption to 0.1

```
pde = chaste.cell_based.CellwiseSourceEllipticPde2(cell_population, -0.5)
```
We set a constant amount of oxygen on the edge of the spheroid

```
bc = chaste.pde.ConstBoundaryCondition2(1.0)
is_neumann_bc = False
```
Set up a pde modifier to solve the PDE at each simulation time step

```
pde_modifier = chaste.cell_based.EllipticGrowingDomainPdeModifier2(pde, bc, is_neumann_bc)
pde_modifier.SetDependentVariableName("oxygen")
simulator.AddSimulationModifier(pde_modifier)
```
As before, we set up a scene modifier for real-time visualization

```
scene = chaste.visualization.VtkScene2()
scene.SetCellPopulation(cell_population)
scene.GetCellPopulationActorGenerator().SetColorByCellData(True)
scene.GetCellPopulationActorGenerator().SetDataLabel("oxygen")
scene.GetCellPopulationActorGenerator().SetShowCellCentres(True)
scene.GetCellPopulationActorGenerator().SetShowVoronoiMeshEdges(False)
nb_manager = chaste.visualization.JupyterNotebookManager()
scene_modifier = chaste.visualization.JupyterSceneModifier2(nb_manager)
scene_modifier.SetVtkScene(scene)
scene_modifier.SetUpdateFrequency(100)
simulator.AddSimulationModifier(scene_modifier)
```
Eventually remove apoptotic cells

```
killer = chaste.cell_based.ApoptoticCellKiller2(cell_population)
simulator.AddCellKiller(killer)
```
To run the simulation, we call `Solve()`. We can again do a quick rendering of the population at the end of the simulation

```
scene.Start()
simulator.Solve()
## Tear down the test 
chaste.cell_based.TearDownNotebookTest()
```
    
Full results can be visualized in Paraview from the `file_handler.GetOutputDirectoryFullPath()` directory.
