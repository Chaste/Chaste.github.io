

# Chaste Guides

Before reading this have a look at [GettingStarted](https://github.com/Chaste/trac_archive/wiki/Getting-Started) to decide whether you are a *user* [releases](of) or a *developer* [back to Chaste core code](contributing).

*Users* can download the latest release of the source code from our [GitHub releases page](https://github.com/Chaste/Chaste/releases) to get a stable version, or check out a [tested development branch](https://github.com/Chaste/Chaste/branches) to get the latest features.

New *developers* should, rather than downloading the release, follow the installation instructions below, including the part on checking-out the latest version of the code.

# 1. User Guides

## Installation

* [InstallGuides](https://github.com/Chaste/trac_archive/wiki/Install-Guides) - How to install Chaste and its dependencies.
* ChasteGuides/CmakeFirstRun - How to configure, build, and run tests to check the installation.


## Running Chaste Simulations

* [ReleaseNotes](https://github.com/Chaste/trac_archive/wiki/Release-Notes) and [LatestNews](https://github.com/Chaste/trac_archive/wiki/Latest-News) on changes since the last release
* [Tutorials](https://github.com/Chaste/trac_archive/wiki/User-Tutorials)
* [Visualisation guides](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Visualisation-Guides)
* ['How to' index](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-How-To) -- links to test code illustrating how various things can be done
* [Cmake first-run guide](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Cmake-First-Run). For all available options, including compiling optimised code, see [full Cmake build guide](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Cmake-Build-Guide).
* [Troubleshooting](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Trouble-Shooting) -- solutions to some common or difficult problems are given here
* [Public API documentation for the latest revision](https://chaste.cs.ox.ac.uk/public-docs/) and [API documentation for release versions](//chaste/tutorials/)  style=display:none;


## Writing your own code that uses Chaste

* [User Projects](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-User-Projects) -- for creating (or cloning an existing) personal user project which can use the core code and build/testing framework.


## Miscellaneous information

* File format information is given in the file `docs/FileFormats.html`, supplied with the release. (The latest version of this file may also be viewed [here](/git_repo/docs/FileFormats.html) - click on the 'download in original format' link at the bottom of the page).
* [Units of parameters used in Chaste](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Chaste-Units)
* [Equations and finite element implementations](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Finite-Element-Implementations) -- the pdf file attached to this page describes the exact PDEs being solved in various parts of Chaste and the finite element methods used to solve them.
* [Default parameter values](/git_repo/heart/src/problem/HeartConfigDefaults.hpp) -- read off from this file, ignore the `Simulation` block, which only applies to the old cardiac executable.


# 2. Further information for developers
New developers (including users based in Compbio/CMB with full wiki and svn access) should read the 'users of the source code' section above, and also see

* [Helpful resources for external users of development versions of Chaste](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-External-Developer-Guide)
* [Some best practices for developers to follow](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Best-Practice-Guide)
* [GitGuide](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Git-Guide) -- how to use the git Chaste repository, in particular see [the ticket workflow section](https://github.com/Chaste/trac_archive/wiki/ChasteGuides_GitGuide#TicketWorkflow).
* [CmakeBuildGuide](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Cmake-Build-Guide) for a detailed guide of all the cmake options.
* [BuildingExecutableApps](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Building-Executable-Apps) - making standalone executables that don't use the CxxTest framework.
* [Fixing "bad" commits](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Automated-Build-Guide)
* [ChasteStrategies](https://github.com/Chaste/trac_archive/wiki/Chaste-Strategies) -- see in particular the coding standards guide
* It is also worth familiarising yourself with [UsefulNotes](https://github.com/Chaste/trac_archive/wiki/Useful-Notes)
*  style=display:none; [Full API documentation for the latest revision](https://chaste.cs.ox.ac.uk/docs/) (not accessible to anonymous login)
* [RunningAcceptanceTests](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Running-Acceptance-Tests)
* [SconsArchive](https://github.com/Chaste/trac_archive/wiki/Scons-Archive) - a listing of pages relating to the old scons build system, irrelevant if you are using `cmake` (recommended).
* [ModulesSetupGuide](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Modules-Setup-Guide) - How to locally replicate a portability setup with environment modules


# 3. Advanced

* [How to run Chaste binaries directly from the command line](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Running-Binaries-From-Command-Line)
* [Repository access for non-core developers](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Access-Code-Repository) (see also ChasteGuides/ExternalDeveloperGuide)
* [HPC Install Guide](https://github.com/Chaste/trac_archive/wiki/Install-Guides_HPC-Install-Guide)
* [State-variable Interpolation](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-State-Variable-Interpolation) -- state-variable interpolation is a way of improving conduction velocity accuracy in large cardiac electro-physiology simulations
* [FEM assemblers and solvers](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Finite-Element-Assemblers-And-Solvers) -- this page describes how the finite element solvers work internally
* [Lecture notes](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Nmood-Lecture-Notes) -- lectures on a course on *Numerical methods and object-oriented design*, which includes various sections on Chaste architecture (especially on PDE solving)
* [Solving cardiac problems](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Solving-Cardiac-Problems) -- describes the implementation of the cardiac solvers for developers (see [tutorials](https://github.com/Chaste/trac_archive/wiki/User-Tutorials) for user guides)
* [Cardiac mechanics solvers](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Cardiac-Mechanics-Solvers) -- a bit of information on how the cardiac mechanics solvers are connected to the main mechanics solvers.
* InstallGuides/TestingMultipleVersions -- how to add new versions of libraries, for going into the testing rotation on lofty.


# 4. Chaste Administrators

* [ChasteAdmin](https://github.com/Chaste/trac_archive/wiki/Chaste-Admin) Root admin info page
* [MakingARelease](https://github.com/Chaste/trac_archive/wiki/Chaste-Admin-_-Making-A-Release) --- including how to release a tag of a user project.
* [ServerSetup](https://github.com/Chaste/trac_archive/wiki/Chaste-Admin-_-Server-Setup) Configuration of `chaste.cs`.
* [MachineNames](https://github.com/Chaste/trac_archive/wiki/Machine-Names) List of build machines
* [AutomatedBuilds](https://github.com/Chaste/trac_archive/wiki/Chaste-Admin-_-Automated-Builds) How the accounts used for automated builds on chaste machines are set up
* [ManagingUbuntuPackage](https://github.com/Chaste/trac_archive/wiki/Chaste-Admin-_-Managing-Ubuntu-Package) - How to manage the Ubuntu debian package for Chaste dependencies.
* [UpdatingTheWebsite](https://github.com/Chaste/trac_archive/wiki/Chaste-Admin-_-Updating-The-Website) - How to manage the Chaste web pages.
* [UserPermissions](https://github.com/Chaste/trac_archive/wiki/Chaste-Admin-_-User-Permissions) - How to set user permissions for trac, the chaste git server, who can see infrastructure scripts etc.
* [InfrastructureScripts](https://github.com/Chaste/trac_archive/wiki/Chaste-Admin-_-Infrastructure-Scripts) - How to get the infrastructure repo.
* [ModulesAdminGuide](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Modules-Admin-Guide) - How to setup portability tests with environment modules and github actions


-----

# Automatically generated alphabetical listing of guide pages

[SubWiki(ChasteGuides/)](SubWiki(ChasteGuides/))
