---
title: "Releasing User Projects"
description: "Releasing User Projects"
draft: false
images: []
toc: true
layout: "single"
---

This page discusses the procedure for 'releasing' a user project based on Chaste ('bolt-on project'). Typically you'll want to do this when there is a particular version of code associated with a paper/project that you want to provide as a download.

## Git projects (2016 onwards)

Git projects should be made as detailed on ChasteGuides/UserProjects. Once they are ready for release, the recommended route is simply to [follow the github release guide](https://help.github.com/articles/creating-releases/).

### Archiving

Since Git repos can be deleted by their owner at any point, it is also good practice to permanently archive a copy of your repo somewhere. There are a few routes for this:

* [Zenodo](https://zenodo.org/) is one tool for doing this [instructions here](https://guides.github.com/activities/citable-code/).
* [Figshare](https://figshare.com/) is another, [instructions here](https://support.figshare.com/support/solutions/articles/6000150264-how-to-connect-figshare-with-your-github-account).

Both have the benefit of providing you with a [doi](https://en.wikipedia.org/wiki/Digital_object_identifier) to enable people to cite your code.

## SVN projects (pre 2016)

We often release the code that generated the results of a paper as a 'bolt-on project'. This is usually done as a 'tag' of a particular revision of a user project in the repository, rather than making the user project itself public. This ensures that no confidential history is released, and makes clear that we aren't going to maintain compatibility for the project with the development version of Chaste indefinitely.

The rough work-flow is this (obviously change the name and release numbers appropriately!):

* [Check out the project](https://github.com/Chaste/trac_archive/wiki/ChasteGuides_UserProjects?version=51#Oldinformation)
* Make sure that it compiles and continuous is clean (usually for a particular [release version of Chaste](https://github.com/Chaste/trac_archive/wiki/Release-Names)).
* *Does your project pull in the current revision of the remote cellml project using `svn:externals`?* If so, then you will probably want to ensure that a certain revision of the cellml project is used too, in case anyone checks out your tag in future and expects the same CellML files. Do something like the following (more details in the cellml project readme: [projects/cellml/README.txt](/projects/cellml/README.txt)):
    * Navigate to where in your project the cellml project is referenced.
    * Run the command (note the full stop): `svn propedit svn:externals .`
    * Change the line so that it says which revision of the cellml project to use, e.g. "`cellml -r19716 https://chaste.cs.ox.ac.uk/svn/chaste/projects/cellml/cellml`"
* Change directory into the root of the checked out project
* Create an svn tag (note the '.'):

```

#!sh
svn copy . https://chaste.cs.ox.ac.uk/svn/chaste/tags/PhilTransA2009_release_1.1 \
    -m "Tag for PhilTransA2009 release"


```


* If you made any local modifications, e.g. to fix a revision of the cellml project as described above, now is a good point to revert them before you forget!

```

#!sh
svn revert -R .


```


* Grab a copy of the tag locally, without `.svn` folders:

```

#!sh
mkdir /tmp/projects
cd /tmp/projects
svn export https://chaste.cs.ox.ac.uk/svn/chaste/tags/PhilTransA2009_release_1.1 PhilTransA2009
cd ..


```


* Tar and gzip:

```

#!sh
tar cvfz PhilTransA2009_release_1_1.tgz projects/PhilTransA2009/


```


If you want to host on the Chaste website, ask an admin to follow the instructions on [an old version of the MakingARelease page](https://github.com/Chaste/trac_archive/wiki/ChasteAdmin_MakingARelease?version=125#Bolt-onprojects).
