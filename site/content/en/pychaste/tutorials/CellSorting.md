---
title : "Cell Sorting Tutorial"
summary: ""
draft: false
images: []
toc: true
---
This tutorial is automatically generated from the file test/python/cell_based/tutorials/TestCellSortingTutorial.ipynb.
```python
## Jupyter notebook specific imports 
import matplotlib as mpl 
from IPython import display 
%matplotlib inline
```
## Introduction
This test is a demonstration of cell sorting using a Cellular Potts
based framework. It shows:
-   How to set up a Potts simulation
-   Working with labels
### The Test
```python
import matplotlib.pyplot as plt # Plotting
import numpy as np # Matrix tools
import chaste # The PyChaste module
chaste.init() # Set up MPI
import chaste.cell_based # Contains cell populations
import chaste.mesh # Contains meshes
import chaste.visualization # Visualization tools
```
### Test 1 - Cell sorting
The next test generates a collection of cells, there are two types of
cells, labelled ones and non labelled ones, there is differential
adhesion between the cell types. For the parameters specified, the cells
sort into separate types.
```python
# Set up the test 
chaste.cell_based.SetupNotebookTest()
```
First, we generate a `Potts` mesh. To create a `PottsMesh`, we can use
the `PottsMeshGenerator`. This generates a regular square-shaped mesh,
in which all elements are the same size. We have chosen an 8 by 8 block
of elements each consisting of 4 by 4 ( = 16) lattice sites.
```python
generator = chaste.mesh.PottsMeshGenerator2(50, 8, 4, 50, 8, 4)
mesh = generator.GetMesh()
```
Having created a mesh, we now create some cells. To do this, we the
`CellsGenerator` helper class, as before but this time the third
argument is set to make all cells non-proliferative.
```python
cells = chaste.cell_based.VecCellPtr()
differentiated_type = chaste.cell_based.DifferentiatedCellProliferativeType()
cell_generator = chaste.cell_based.CellsGeneratorUniformCellCycleModel_2()
cell_generator.GenerateBasicRandom(cells, mesh.GetNumElements(), differentiated_type)
```
Before we make a CellPopulation we make a cell label and then assign
this label to some randomly chosen cells.
```python
label = chaste.cell_based.CellLabel()
for eachCell in cells:
    if(chaste.core.RandomNumberGenerator.Instance().ranf()<0.5):
        eachCell.AddCellProperty(label)
```
Now we have a mesh and a set of cells to go with it, we can create a
`CellPopulation`.
```python
cell_population = chaste.cell_based.PottsBasedCellPopulation2(mesh, cells)
```
In order to visualize labelled cells we need to use the following
command.
```python
cell_population.AddCellWriterCellLabelWriter()
```
PyChaste can do simple 3D rendering with VTK. We set up a VtkScene so
that we can see the population evovle in real time.
```python
scene= chaste.visualization.VtkScene2()
scene.SetCellPopulation(cell_population)
scene.GetCellPopulationActorGenerator().SetShowPottsMeshEdges(True)
nb_manager = chaste.visualization.JupyterNotebookManager()
nb_manager.vtk_show(scene, height=600)
```
We then pass in the cell population into an `OffLatticeSimulation`, and
set the output directory and end time
```python
simulator = chaste.cell_based.OnLatticeSimulation2(cell_population)
simulator.SetOutputDirectory("Python/TestCellSorting")
simulator.SetEndTime(20.0)
simulator.SetSamplingTimestepMultiple(10)
```
We must now create one or more update rules, which determine the
Hamiltonian in the Potts simulation. For this test, we use two update
rules based upon a volume constraint (`VolumeConstraintPottsUpdateRule`)
and differential adhesion between cells
(`DifferentialAdhesionPottsUpdateRule`), set appropriate parameters, and
pass them to the `OnLatticeSimulation`.
```python
volume_constraint_update_rule = chaste.cell_based.VolumeConstraintPottsUpdateRule2()
volume_constraint_update_rule.SetMatureCellTargetVolume(16)
volume_constraint_update_rule.SetDeformationEnergyParameter(0.2)
simulator.AddUpdateRule(volume_constraint_update_rule)
```
We repeat the process for any other update rules.
```python
differential_adhesion_update_rule = chaste.cell_based.DifferentialAdhesionPottsUpdateRule2()
differential_adhesion_update_rule.SetLabelledCellLabelledCellAdhesionEnergyParameter(0.16)
differential_adhesion_update_rule.SetLabelledCellCellAdhesionEnergyParameter(0.11)
differential_adhesion_update_rule.SetCellCellAdhesionEnergyParameter(0.02)
differential_adhesion_update_rule.SetLabelledCellBoundaryAdhesionEnergyParameter(0.16)
differential_adhesion_update_rule.SetCellBoundaryAdhesionEnergyParameter(0.16)
simulator.AddUpdateRule(differential_adhesion_update_rule)
```
Set up plotting
```python
scene_modifier = chaste.visualization.JupyterSceneModifier2(nb_manager)
scene_modifier.SetVtkScene(scene)
scene_modifier.SetUpdateFrequency(1000)
simulator.AddSimulationModifier(scene_modifier)
```
To run the simulation, we call `Solve()`.
```python
scene.Start()
simulator.Solve()
# Tear down the test 
chaste.cell_based.TearDownNotebookTest()
```
