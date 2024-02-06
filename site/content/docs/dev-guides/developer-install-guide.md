---
title: "Developer Install Guide"
description: "Developer Install Guide"
draft: false
images: []
toc: true
layout: "single"
---

The easiest ways to install Chaste are

* On Ubuntu - use the [Ubuntu .deb package](https://github.com/Chaste/trac_archive/wiki/Install-Guides-_-Ubuntu-Package)
* Other Linux systems - try following the minimal instructions on [InstallGuide](InstallGuides/InstallGuide)
* Non-Linux/Unix systems - install a virtual machine (e.g. using [VirtualBox](https://www.virtualbox.org/)) running Ubuntu Linux, and install the [Chaste package](https://github.com/Chaste/trac_archive/wiki/Install-Guides-_-Ubuntu-Package)


Then see the section on [checking out the code (below)](#Accessingthecode), and optional or optimised-code-related dependencies.

If you encounter any problems, or have an unusual setup, the following material may be useful.

InstallGuides/DependencyVersions lists the different versions of the dependencies that we test, know to work, think will work, won't work etc.

-----

The main instructions on this page assume you are setting up a machine identical to the core Chaste development machines. We also have guides for a variety of other situations that the Chaste team or users have tried, listed at InstallGuides.  Note that these may not be up-to-date, so some familiarity with installing software on Linux-like systems may be required.

***NB: When creating new install guides, please name the page like '`InstallGuides/GuideName`', so that it gets included in the public portion of the wiki.***

## Mandatory for running Chaste

All users of the source code, whether on a desktop, server or HPC, should ensure all of the below items are present.


* Install an operating system.  The core developer machines currently use Ubuntu 10.04 (see InstallGuides/DeveloperUbuntuReinstall). If you do choose Ubuntu then follow [Ubuntu .deb package](https://github.com/Chaste/trac_archive/wiki/Install-Guides-_-Ubuntu-Package). The below instructions should work for other flavours of Linux. Previous installs were:
    * [InstallFedoraCore](https://github.com/Chaste/trac_archive/wiki/Install-Fedora-Core)  -- **not** needed on the Fedora Core 6 install
    * [InstallingFromRedHatFedoraCoreSixDvd](https://github.com/Chaste/trac_archive/wiki/Installing-From-Red-Hat-Fedora-Core-Six-Dvd)



* [InstallIntelCompiler](https://github.com/Chaste/trac_archive/wiki/Install-Intel-Compiler) -- technically not needed to run Chaste but used for the best performance



* [InstallPetscAndMpi](https://github.com/Chaste/trac_archive/wiki/Install-Petsc-And-Mpi) and/or [InstallPetscAndMpiForProductionBuild](https://github.com/Chaste/trac_archive/wiki/Install-Petsc-And-Mpi-For-Production-Build) (which requires InstallIntelCompiler).



* [InstallBoost](https://github.com/Chaste/trac_archive/wiki/Install-Boost) -- **not** needed on the new (Ubuntu / Fedora Core 6) installs



* [InstallScons](https://github.com/Chaste/trac_archive/wiki/Install-Scons) (our build framework)



* [InstallXmlTools](https://github.com/Chaste/trac_archive/wiki/Install-Xml-Tools)



* [InstallHdf5](https://github.com/Chaste/trac_archive/wiki/Install-Hdf5) (for file output)



* [InstallParMetis](https://github.com/Chaste/trac_archive/wiki/Install-Par-Metis) (for mesh partitioning)



* [InstallCodegen](https://github.com/Chaste/trac_archive/wiki/Install-Codegen) -- chaste_codegen itself is distributed via pypi, but you'll need to install its dependencies



* [SetEnvironmentVariables](https://github.com/Chaste/trac_archive/wiki/Set-Environment-Variables)


## Highly recommended optional libraries


* [InstallCvode](https://github.com/Chaste/trac_archive/wiki/Install-Cvode) -- (fast and accurate ODE solver for `cell_based` and single-cell-cardiac simulations)


## For development machines

We use the following for development machines, but these can be skipped for servers and HPC installations that use a command-line interface to Chaste.


* [InstallSubversionJavahl](https://github.com/Chaste/trac_archive/wiki/Install-Subversion-Javahl)



* [InstallJava](https://github.com/Chaste/trac_archive/wiki/Install-Java)



* InstallGuides/EclipsePlugins



* [SetupEclipse](https://github.com/Chaste/trac_archive/wiki/Setup-Eclipse)


## Accessing the code


* [ChasteGuides/AccessCodeRepository](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Access-Code-Repository).



* [CheckoutUserProject](https://github.com/Chaste/trac_archive/wiki/Install-Guides-_-Checkout-User-Project) -- if you already have or want to create a user project.


## Optional (not needed to run the code)

* Testing
    * [InstallValgrind](https://github.com/Chaste/trac_archive/wiki/Install-Valgrind) -- only needed for memory testing, **not** needed on the new (Ubuntu / Fedora Core 6) installs
    * [InstallGooglePerformanceTools](https://github.com/Chaste/trac_archive/wiki/Install-Google-Performance-Tools) -- for profiling using Google's tools
    * [InstallTextTest](https://github.com/Chaste/trac_archive/wiki/Install-Text-Test) -- for running acceptance tests of the Chaste executable
* Visualization
    * [InstallParaview](https://github.com/Chaste/trac_archive/wiki/Install-Paraview) -- VTK visualizer
    * [InstallVtkStatic](https://github.com/Chaste/trac_archive/wiki/Install-Vtk-Static) -- special instructions for making with static libraries
    * [InstallMeshalyzer](https://github.com/Chaste/trac_archive/wiki/Install-Meshalyzer) -- for visualising cardiac simulations
    * [InstallInventor](https://github.com/Chaste/trac_archive/wiki/Install-Inventor) -- for visualisation in 3D (of `cell_based` simulations)
    * [InstallMplayer](https://github.com/Chaste/trac_archive/wiki/Install-Mplayer) -- movie player
* Optional/experimental additions
    * [InstallAdaptivityLibrary](https://github.com/Chaste/trac_archive/wiki/Install-Adaptivity-Library) -- for running adaptive meshing simulations (sequentially)
    * [Installing HYPRE/MUMPS with PETSc 3](https://github.com/Chaste/trac_archive/wiki/Installing-Hypre-And-Or-Mumps-With-Petsc-Three) -- installing the AMG preconditioner HYPRE or the direct solver MUMPS


## Historical items, no longer needed


* [InstallTetgenAndTetview](https://github.com/Chaste/trac_archive/wiki/Install-Tetgen-And-Tetview) -- now included in Chaste source.



* [InstallTriangle](https://github.com/Chaste/trac_archive/wiki/Install-Triangle) -- now included in Chaste source.



* [InstallNdiff](https://github.com/Chaste/trac_archive/wiki/Install-Ndiff) -- used to be used for comparing results files to a tolerance



* [InstallMetis](https://github.com/Chaste/trac_archive/wiki/Install-Metis) -- superseded by parMETIS.



* [InstallingDealii](https://github.com/Chaste/trac_archive/wiki/Installing-Dealii) -- not needed unless you wish to use the `dealii` project


