---
title: "Getting started"
description: "Information on getting started with Chaste"
draft: false
images: []
toc: true
layout: "single"
---

## Using Chaste

If you're considering using Chaste in your research, or you're applying for funding that might make use of Chaste, please read our [guidlines](/community/using-chaste/).
These are simply some suggestions that will help with the onboarding process and ensure the core development team are available to help you.

Chaste is a software library. To use it you need to obtain and compile the
_source code_, which can then be used to build and run cardiac
electro-physiological and electro-mechanical simulations, discrete tissue
simulations (including intestinal crypt simulations), and more.

## Supported Operating Systems

- **Linux**: Chaste is primarily developed on
  [Ubuntu Linux](https://www.ubuntu.com/) (recommended), and is regularly tested
  on all Long Term Support (LTS) versions of Ubuntu, but should also work on
  other Linux/Unix systems.
- **MacOS**: Chaste is not currently tested on Mac OS.
- **Windows**: It is currently not recommended to use Chaste on Windows.

The recommended route for unsupported systems is to install Chaste via
[Docker](installguides/docker) or virtual machine running Ubuntu Linux.

## Getting The Code

If you are primarily interested in using the code as it is, and don't plan to
contribute new code or changes back to the core Chaste code you can either:

1. Download a fixed release of Chaste, found on the
   [releases page](https://github.com/Chaste/Chaste/releases).
2. Checkout the latest release tag (to stay up to date with 6-monthly
   releases) using [git](https://git-scm.com/).
3. Stay right up to date with latest developments using our git `develop`
   branch.

and follow subsequent [User guides](/docs/user-guides/). The first option is most stable, and
recommended for new users so the code doesn't change underneath you. The second
option will let you stay up to date with the latest release, which can be a good
idea so that your code will also work on the latest versions of Chaste
dependencies. The third option will give you full access to the latest features,
but will require changes to your code as you go along to stay up to date with
changes to Chaste. Note: using this approach you can only download/get updates
of the code, but can't contribute new code or changes back to the core Chaste
code.

Alternatively, if you are planning on contributing back to the codebase, you
should check out Chaste from the developer repository and follow the
[Developer Guides](dev-guides/). Reading the
[External Developer Guide](dev-guides/external-developer-guide) is highly
recommended, and then you can check out a copy of the development code as per the 
[Code Repository Access](dev-guides/access-code-repository) page.

---

Perusing the [release notes](release-notes/release-notes) and
[changes since last release](release-notes/changes-since-last-release) can
give you a good overview of what features are in each release, and what has been
added since.

---

If you have been forwarded here from the old <www.cs.ox.ac.uk/chaste/downloads> page (no longer valid) you can find the archived contents of that site at the following URL: <https://chaste.cs.ox.ac.uk/old-chaste-data/downloads/>
Note that the [projects](https://chaste.cs.ox.ac.uk/old-chaste-data/downloads/projects/) folder contains code associated with older research paper 'projects'.

## Installing Dependencies

Chaste has several dependencies, including `MPI`, `PETSc`, `HDF5` and others,
which should be installed prior to compilation. If you are using Ubuntu Linux it
is easiest to do this using the Chaste Debian package -- see
[Ubuntu Package](installguides/ubuntu-package).

Otherwise you should use the manual
[Install Guide](dev-guides/developer-install-guide) and follow the
instructions on installing dependencies (or use the installation guide supplied
with the release).

In addition to software dependencies, if you wish to do programming yourself,
then we recommend using a C++ integrated development environment such as
[VSCode](https://code.visualstudio.com/),
[Eclipse](http://www.eclipse.org/cdt/) or
[Clion](https://www.jetbrains.com/clion/).

## Next Steps

Once you have installed the dependencies and obtained the source code, go to
[User Guides](user-guides) and read and run the [tutorials](user-tutorials) on
the kind of simulation you wish to run.

## Getting Help

For general discussion about Chaste, and questions regarding usage, we provide
the [Chaste users' mailing list](/community/mailing-list).

Bug reports and feature requests may be submitted by opening an
[issue](https://github.com/Chaste/Chaste/issues) on GitHub.
