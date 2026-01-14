## Investigation of Buckling and Fission in an Epithelial Layer

This section contains pages generated automatically from the source code accompanying Almet et al. (2016)
"A multicellular model of intestinal crypt fission".

This model is an extension on a model originally presented in Langlands et al. (2017) http://dx.doi.org/10.1371/journal.pbio.1002491.
The code to run single simulations can be found at the Paper Tutorial for that paper, [TestCryptFissionLiteratePaper.hpp](https://github.com/Chaste/trac_archive/wiki/Paper-Tutorials-_-Crypt-Fission-Plos2016-_-Crypt-Fission)

Before looking at this, you may wish to look at some of the [basic user tutorials](https://github.com/Chaste/trac_archive/wiki/User-Tutorials) for Chaste.


### Getting the code and installing dependencies

Before running these examples you will need to [install Chaste's dependencies](https://github.com/Chaste/trac_archive/wiki/Install-Guides-_-Install-Guide) and the [source code for version 3.4](http://www.cs.ox.ac.uk/chaste/download.html).
The easiest way to do this is using an Ubuntu machine (or an Ubuntu virtual machine) as discussed on [InstallGuides/UbuntuPackage](https://github.com/Chaste/trac_archive/wiki/Install-Guides-_-Ubuntu-Package).
Note that Chaste is only fully supported on Linux/Unix systems, so users of Windows or Mac OS X may need to follow the virtual machine route.
For manual installation of each dependency, on any version of Linux, see DeveloperInstallGuide.

You will also need the source for the [EpithelialFission](https://github.com/Chaste/trac_archive/wiki/Epithelial-Fission) project.  This can be done by checking out the version from the repository by using the command

```bash
svn checkout https://chaste.cs.ox.ac.uk/svn/chaste/projects/EpithelialFission
```

in the projects folder of the Chaste directory. You will need to use the supplied username and password.

Now the project should be installed, and everything should compile and run correctly.
You can now run the tests or simulations, or create your own test suites.

### Documentation
There are two folders - `src` and `test`.
 1. The `src` folder contains the classes necesary to run the simulation. These define the additional forces and boundary conditions not in the core chaste code.

* `EpithelialLayerAnoikisCellKiller.xpp` - removes epithelial cells if they detach from the surrounding nonepithelial cells and enter the lumen.
* `EpithelialLayerBasementMembraneForce.xpp` - force that simulates the adhesion effect of the basement membrane.
* `EpithelialLayerDataTrackingModifier.xpp`- modifier class that records statistics on the layer's cell population and shape.
* `EpithelialLayerLinearSpringForc.xpp` - linear spring force that has a variable spring stiffness depending on the cell types that the spring connects.
* `FixedRegionPlaneBoundaryCondition.xpp` - boundary conditin that fixes cells past a certain region.
* `StochasticTargetProportionBasedCellCycleModel.xpp` - asymmetric-division-based cell cycle model to control the proportino of soft cells in the layer.

 2. The `test` folder contains:

* [TestCryptFissionSweepsLiteratePaper.hpp](https://github.com/Chaste/trac_archive/wiki/Paper-Tutorials-_-Epithelial-Fission-_-Crypt-Fission-Sweeps) - this file can be run to generate the results in Figures 6-11.

 == Running tests ==
You can then run tests and simulations with,

```bash
cd <Chaste3.4 path>
scons b=GccOpt cl=0 co=1 ts=projects/EpithelialFission/test/TestCryptFissionSweepsLiteratePaper.hpp
```

Note that this will only compile the test. The following commands will run the simulation over the random number generator seed range

```text
INIT_SEED
```

-

```text
FINAL_SEED
```

:

```bash
cd projects/EpithelialFission/test/
sh run_script_for_epithelial_layer_sweeps.sh INIT_SEED FINAL_SEED
```

----
**NB**: the paper was developed with release version 3.3, but will work on release version 3.4. It will not work with with release version 3.2 or under.

For further information on using Chaste, see the [extensive guide material](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides).
You may also wish to look at some of the [basic user tutorials](https://github.com/Chaste/trac_archive/wiki/User-Tutorials).


-----
### Section contents
[SubWiki()](SubWiki())

