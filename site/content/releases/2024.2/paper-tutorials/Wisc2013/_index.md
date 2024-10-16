## Connecting models to data in multiscale multicellular tissue simulations

This section of the Chaste wiki contains pages generated automatically from the source code accompanying
"[Connecting models to data in multiscale multicellular tissue simulations](http://dx.doi.org/10.1016/j.procs.2013.05.235)",
our paper in the [2013 International Conference on Computational Science](http://www.iccs-meeting.org/iccs2013).
(A [pre-print](https://github.com/Chaste/trac_archive/blob/master/attachment/ticket//paper627.pdf) is attached to this wiki page, but the published paper is open access.)

The paper describes a 'proof of concept' parameter sweep simulation performed using our [Functional Curation](https://github.com/Chaste/trac_archive/wiki/Functional-Curation)
tools on a model implemented in [cell-based Chaste](http://www.cs.ox.ac.uk/chaste/cell_based_index.html).
The code which achieves this, and enables reproduction of all the figures in the paper, is shown in [this sub-page](https://github.com/Chaste/trac_archive/wiki/Paper-Tutorials-_-Wisc2013-_-Crypt-Proliferation).

Before running this simulation you will need to [install Chaste's dependencies](https://github.com/Chaste/trac_archive/wiki/Install-Guides-_-Install-Guide).
The easiest way to do this is using an Ubuntu machine (or an Ubuntu virtual machine) as discussed on InstallGuides/UbuntuPackage.
Note that while Chaste 3.2 has support for cell-based Chaste on Windows and Mac OS X, the code for this paper *does not work*
on Windows, and has not been tested on Mac OS X, so the virtual machine route may be advisable in these instances.
In order to generate result figures automatically, you will also need to install [Gnuplot](http://www.gnuplot.info/).

You will also need the Chaste source code for this paper and the source for the extension [FunctionalCuration](https://github.com/Chaste/trac_archive/wiki/Functional-Curation) project.
These are available from the [main Chaste download page](http://www.cs.ox.ac.uk/chaste/download.html) as extensions to
Chaste release 3.2 under the projects heading,
or you can [access the source code direct from our repository](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Access-Code-Repository).
For the latter option, using a command-line subversion client, you can get the required code in a new folder called 'Chaste' with the commands:
```

#!sh
svn --username anonymous checkout https://chaste.cs.ox.ac.uk/svn/chaste/tags/release_3.2 Chaste
cd Chaste/projects
svn --username anonymous checkout https://chaste.cs.ox.ac.uk/svn/chaste/tags/FunctionalCuration_release_3.2 FunctionalCuration
svn --username anonymous checkout https://chaste.cs.ox.ac.uk/svn/chaste/tags/Wisc2013_release_3.2 Wisc2013
```

Use your email address as the password for the 'anonymous' account.

**NB**: Note that the code for this paper *will not work* with Chaste release 3.1 or earlier.
It has been tested with release 3.3, but will not be tested with future versions.

You are now ready to [run the simulations featured in the paper](https://github.com/Chaste/trac_archive/wiki/Paper-Tutorials-_-Wisc2013-_-Crypt-Proliferation).

For further information on using Chaste, see our [extensive guide material](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides).
You may also wish to look at some of the [basic user tutorials](https://github.com/Chaste/trac_archive/wiki/User-Tutorials).


version: "2024.2"
-----
### Section contents
[SubWiki()](SubWiki())

