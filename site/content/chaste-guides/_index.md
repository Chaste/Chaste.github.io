---
title: "Chaste Guides"
description: "Guides for using chaste"
date: 2020-08-27T19:23:18+02:00
lastmod: 2020-08-27T19:23:18+02:00
draft: false
images: []
toc: true
layout: "single"
---

Before reading this have a look at [GettingStarted](/getting-started) to decide whether you are a *user* [releases](of) or a *developer* [back to Chaste core code](contributing).

*Users* can download the latest release of the source code from our [GitHub releases page](https://github.com/Chaste/Chaste/releases) to get a stable version, or check out a [tested development branch](https://github.com/Chaste/Chaste/branches) to get the latest features.

New *developers* should, rather than downloading the release, follow the installation instructions below, including the part on checking-out the latest version of the code.

# 1. User Guides

## Installation

* [InstallGuides](/install-guides) - How to install Chaste and its dependencies.
* ChasteGuides/CmakeFirstRun - How to configure, build, and run tests to check the installation.


## Running Chaste Simulations

* [ReleaseNotes](/release-notes) and [LatestNews](/Latest-News) on changes since the last release
* [Tutorials](/user-tutorials)
* [Visualisation guides](/chaste-guides/visualisation-guides)
* ['How to' index](/chaste-guides/how-to) -- links to test code illustrating how various things can be done
* [Cmake first-run guide](/chaste-guides/cmake-first-run). For all available options, including compiling optimised code, see [full Cmake build guide](/Chaste-Guides-_-Cmake-Build-Guide).
* [Troubleshooting](/chaste-guides/trouble-shooting) -- solutions to some common or difficult problems are given here
* [Public API documentation for the latest revision](https://chaste.cs.ox.ac.uk/public-docs/) and [API documentation for release versions](//chaste/tutorials/)  style=display:none;


## Writing your own code that uses Chaste

* [User Projects](/chaste-guides/user-projects) -- for creating (or cloning an existing) personal user project which can use the core code and build/testing framework.


## Miscellaneous information

* File format information is given in the file `docs/FileFormats.html`, supplied with the release. (The latest version of this file may also be viewed [here](/git_repo/docs/fileformats.html) - click on the 'download in original format' link at the bottom of the page).
* [Units of parameters used in Chaste](/chaste-guides/chaste-units)
* [Equations and finite element implementations](/chaste-guides/finite-element-implementations) -- the pdf file attached to this page describes the exact PDEs being solved in various parts of Chaste and the finite element methods used to solve them.
* [Default parameter values](/git_repo/heart/src/problem/heartconfigdefaults.hpp) -- read off from this file, ignore the `Simulation` block, which only applies to the old cardiac executable.


# 2. Further information for developers
New developers (including users based in Compbio/CMB with full wiki and svn access) should read the 'users of the source code' section above, and also see

* [Helpful resources for external users of development versions of Chaste](/chaste-guides/external-developer-guide)
* [Some best practices for developers to follow](/chaste-guides/best-practice-guide)
* [GitGuide](/chaste-guides/git-guide) -- how to use the git Chaste repository, in particular see [the ticket workflow section](/ChasteGuides_GitGuide#TicketWorkflow).
* [CmakeBuildGuide](/chaste-guides/cmake-build-guide) for a detailed guide of all the cmake options.
* [BuildingExecutableApps](/chaste-guides/building-executable-apps) - making standalone executables that don't use the CxxTest framework.
* [Fixing "bad" commits](/chaste-guides/automated-build-guide)
* [ChasteStrategies](/chaste-strategies) -- see in particular the coding standards guide
* It is also worth familiarising yourself with [UsefulNotes](/useful-notes)
*  style=display:none; [Full API documentation for the latest revision](https://chaste.cs.ox.ac.uk/docs/) (not accessible to anonymous login)
* [RunningAcceptanceTests](/chaste-guides/running-acceptance-tests)
* [SconsArchive](/scons-archive) - a listing of pages relating to the old scons build system, irrelevant if you are using `cmake` (recommended).
* [ModulesSetupGuide](/chaste-guides/modules-setup-guide) - How to locally replicate a portability setup with environment modules


# 3. Advanced

* [How to run Chaste binaries directly from the command line](/chaste-guides/running-binaries-from-command-line)
* [Repository access for non-core developers](/chaste-guides/access-code-repository) (see also ChasteGuides/ExternalDeveloperGuide)
* [HPC Install Guide](/install-guides_hpc-install-guide)
* [State-variable Interpolation](/chaste-guides/state-variable-interpolation) -- state-variable interpolation is a way of improving conduction velocity accuracy in large cardiac electro-physiology simulations
* [FEM assemblers and solvers](/chaste-guides/finite-element-assemblers-and-solvers) -- this page describes how the finite element solvers work internally
* [Lecture notes](/chaste-guides/nmood-lecture-notes) -- lectures on a course on *Numerical methods and object-oriented design*, which includes various sections on Chaste architecture (especially on PDE solving)
* [Solving cardiac problems](/chaste-guides/solving-cardiac-problems) -- describes the implementation of the cardiac solvers for developers (see [tutorials](/User-Tutorials) for user guides)
* [Cardiac mechanics solvers](/chaste-guides/cardiac-mechanics-solvers) -- a bit of information on how the cardiac mechanics solvers are connected to the main mechanics solvers.
* InstallGuides/TestingMultipleVersions -- how to add new versions of libraries, for going into the testing rotation on lofty.


# 4. Chaste Administrators

* [ChasteAdmin](/chaste-admin) Root admin info page
* [MakingARelease](/chaste-admin/making-a-release) --- including how to release a tag of a user project.
* [ServerSetup](/chaste-admin/server-setup) Configuration of `chaste.cs`.
* [MachineNames](/machine-names) List of build machines
* [AutomatedBuilds](/chaste-admin/automated-builds) How the accounts used for automated builds on chaste machines are set up
* [ManagingUbuntuPackage](/chaste-admin/managing-ubuntu-package) - How to manage the Ubuntu debian package for Chaste dependencies.
* [UpdatingTheWebsite](/chaste-admin/updating-the-website) - How to manage the Chaste web pages.
* [UserPermissions](/chaste-admin/user-permissions) - How to set user permissions for trac, the chaste git server, who can see infrastructure scripts etc.
* [InfrastructureScripts](/chaste-admin/infrastructure-scripts) - How to get the infrastructure repo.
* [ModulesAdminGuide](/chaste-guides/modules-admin-guide) - How to setup portability tests with environment modules and github actions


-----

# Automatically generated alphabetical listing of guide pages

[SubWiki(ChasteGuides/)](SubWiki(ChasteGuides/))
