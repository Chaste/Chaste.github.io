---
title: "User Projects"
description: "User Projects"
draft: false
images: []
toc: true
layout: "single"
---

There are a few ways to use Chaste's source code. Professional C++ developers may wish to link to [Chaste as an external C++ library](https://github.com/Chaste/trac_archive/wiki/ChasteGuides_CmakeBuildGuide#UsingChastelikeastandardlibrary) rather than use the User Project framework described below. People new to C++ may be tempted to directly alter code in the Chaste source folders, this should generally be avoided as we won't know whether any problems you may run into are down to Chaste or your changes to it!

Instead of these options, **User Projects** allow you to use Chaste source code and have the benefit of using the Chaste build/testing framework, by putting User Projects under the [projects folder](/projects/). **User Projects** work exactly like new Chaste modules (`global`,`heart`,`cell-based`, etc.) and can depend on any of the Chaste modules (or indeed other User Projects). We tend to supply User Projects to accompany and reproduce research articles (some of these additionally have special wiki pages under [PaperTutorials](https://github.com/Chaste/trac_archive/wiki/Paper-Tutorials) that act as walk-throughs of the codes).

## Prerequisites
This guide assumes that you:

* have already [installed Chaste](https://chaste.cs.ox.ac.uk/trac/wiki/InstallGuides/InstallGuide) on your machine
* have a [GitHub](https://github.com/) account
* have a version of [git](https://git-scm.com/) installed on your machine


## Obtaining the template user project
We strongly recommend first obtaining the template user project, as this comes complete with the necessary CMake infrastructure.

### Recommended: import the repository directly to your GitHub account

Visit https://github.com/Chaste/template_project and click the big green "Use this template" button, and github will let you choose a new name for your project.

### Alternative: mirror the repository
This method allows you to host your repository somewhere other than GitHub, and assumes that you have an empty repository prepared at some location called `<url_of_your_repo>`:

```

git clone --bare https://github.com/Chaste/template_project.git
cd template_project.git
git push --mirror <url_of_your_repo>
cd ..
rm -rf template_project.git

```


## User project guide

1. Navigate to the Chaste projects folder:

```

cd /path/to/Chaste/projects

```


2. Clone your new version of the template project. To do this from the command line, run

```

git clone https://github.com/[YourGitHubUserName]/[YourProjectName].git

```

where you should replace `[YourGitHubUserName](https://github.com/Chaste/trac_archive/wiki/Your-Git-Hub-User-Name)` with your user name on GitHub, and `[YourProjectName](https://github.com/Chaste/trac_archive/wiki/Your-Project-Name)` with the name you chose for your project repository.

3. Navigate to your cloned user project repository at the command line, and run

```

python setup_project.py

```

answering the prompts given.

4. To check that your user project compiles correctly, at the command line navigate to a build folder (outside the Chaste or project source folder - see ChasteGuides/CmakeBuildGuide) and run

```

ccmake path/to/Chaste

```

Type `c` to configure; when this process is complete, type `e` to exit the configuration.
You should find that four additional lines have been added to `cmake`.
These are

* `Chaste_ENABLE_project_[YourProjectName](https://github.com/Chaste/trac_archive/wiki/Your-Project-Name)`
* `Chaste_ENABLE_project_[YourProjectName](https://github.com/Chaste/trac_archive/wiki/Your-Project-Name)_APPS`
* `Chaste_ENABLE_project_[YourProjectName](https://github.com/Chaste/trac_archive/wiki/Your-Project-Name)_INSTALL`
* `Chaste_ENABLE_project_[YourProjectName](https://github.com/Chaste/trac_archive/wiki/Your-Project-Name)_TESTING`


Type `c` to configure once more, then `e` to exit and `g` to generate. When this process is complete, type

```

make TestHello
ctest -R TestHello$

```

and check that `TestHello` passes.

You can now start altering the code, adding your own tests, source and updating the Readme!

## Releasing a User Project

See [Releasing User Projects](releasing-user-projects).

## Old SVN information

[old strategy](https://github.com/Chaste/trac_archive/wiki/ChasteGuides_UserProjects?version=51#Oldinformation) for user projects on the subversion repository and sconscript build system.

### Creating a tag and tarball of an SVN project to release with a paper

See [Releasing User Projects](releasing-user-projects).

### Converting an existing SVN user project  to a GitHub repository

This guide is a strategy for converting an existing old-style svn user project to a GitHub repository, keeping all commit history and author contributions.

It assumes you have `git svn` installed, and that you have a personal GitHub account.

1. Set up an empty GitHub repository of the same name as the user project you wish to convert.

2. An 'authors file' maps svn user names with git users' email addresses. If you have access to the main Chaste `users.txt` file, place this in a temporary directory.
  a. If you do not have the Chaste `users.txt`, create one in a temporary directory.  It should contain a line for each contributor to your user project:

```

SvnUsername = Firstname Lastname <email_address@cs.ox.ac.uk>

```


3. Run the following

```

git svn clone https://chaste.cs.ox.ac.uk/svn/chaste/projects/<UserProjectName> --authors-file=users.txt
cd <UserProjectName>
git remote add origin git@github.com:<YourGitHubName>/<UserProjectName>.git
git push -u origin master

```


4. Clone this new git repository, and follow [user project guide above](https://chaste.cs.ox.ac.uk/trac/wiki/ChasteGuides/UserProjects#Userprojectguide) to check everything is working.


