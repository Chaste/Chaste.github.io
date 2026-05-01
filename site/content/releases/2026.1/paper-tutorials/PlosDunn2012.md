---
title: "A Two-Dimensional Model of the Colonic Crypt Accounting for the Role of the Basement Membrane and Pericryptal Fibroblast Sheath"
draft: false
layout: "single"
paperTutorialProject: "https://github.com/Chaste/project_PlosDunn2012"
version: "2026.1"
---

This project contains code to accompany the 2012 paper by Sara-Jane Dunn et al.,
"[A Two-Dimensional Model of the Colonic Crypt Accounting for the Role of the Basement Membrane and Pericryptal Fibroblast Sheath](http://dx.doi.org/10.1371/journal.pcbi.1002515)", in PLOS Computational Biology.

The code in this project was developed to run with revision 13354 of Chaste.
It will need modification to work with released versions, especially recent releases.

*2026 Note:* the oldest commit in the [Chaste GitHub repository](https://github.com/Chaste/Chaste/) is newer than the revision this paper tutorial was tested with.
Please get in touch if you need to access the old SVN repository.
The following commands may not work. 

To install it and get something to run, try the following commands:

```bash
#!sh
svn checkout https://chaste.cs.ox.ac.uk/svn/chaste/trunk -r 13354 Chaste_r13354
cd Chaste_r13354
cd projects
svn checkout https://chaste.cs.ox.ac.uk/svn/chaste/projects/PlosDunn2012
cd ..
scons -j4 b=GccOpt_warn projects/PlosDunn2012/test/TestCrossSectionModel.hpp
```


You may find that such an old revision of Chaste does not have suitable hostconfig capabilities to build on your machine.
In case of compiler errors, try the following commands from within the Chaste folder.

```bash
#!sh
svn up python */SConscript
cp projects/PlosDunn2012/SConstruct .
scons -j4 b=GccOpt_warn projects/PlosDunn2012/test/TestCrossSectionModel.hpp
```
