---
title: "User Projects"
description: "User Projects"
draft: false
images: []
toc: true
layout: "single"
version: "2024.1"
---

There are a few ways to use Chaste's source code:

- Professional C++ developers may wish to link to
  [Chaste as an external C++ library](../../dev-guides/cmake-build-guide#using-chaste-like-a-standard-library)
  rather than use the User Project framework described below.
- People new to C++ may be tempted to directly alter code in the Chaste source
  folders. This should generally be avoided as we won't know whether any
  problems you may run into are down to Chaste or your changes to it!

Instead of these options, **User Projects** allow you to use Chaste source code
and have the benefit of using the Chaste build/testing framework, by putting
User Projects under the
[`projects`](https://github.com/Chaste/Chaste/tree/develop/projects) directory.
User Projects work exactly like new Chaste modules
(`global`,`heart`,`cell-based`, etc.) and can depend on any of the Chaste
modules (or indeed other User Projects). We tend to supply User Projects to
accompany and reproduce [research articles](../../../publications) e.g.
[CellBasedComparison2017](https://github.com/Chaste/CellBasedComparison2017).

## Prerequisites

This guide assumes that you:

- have already
  [installed Chaste](../../installguides/)
  on your machine
- have a [GitHub](https://github.com/) account
- have a version of [git](https://git-scm.com/) installed on your machine

## Obtaining the template user project

We strongly recommend first obtaining the template user project, as this comes
complete with the necessary CMake infrastructure.

### Recommended: import the repository directly to your GitHub account

Visit
[https://github.com/Chaste/template_project](https://github.com/Chaste/template_project)
and click the big green "Use this template" button, and GitHub will let you
choose a new name for your project.

### Alternative: mirror the repository

This method allows you to host your repository somewhere other than GitHub, and
assumes that you have an empty repository prepared at some location called
`<url_of_your_repo>`:

```sh
git clone --bare https://github.com/Chaste/template_project.git
cd template_project.git
git push --mirror <url_of_your_repo>
cd ..
rm -rf template_project.git
```

## User project guide

1. Navigate to the Chaste projects folder:

```sh
cd /path/to/Chaste/projects
```

2. Clone your new version of the template project. To do this from the command line, run

```sh
git clone https://github.com/<your_github_username>/<your_project_name>.git
```

where you should replace `<your_github_username>` with your user name on GitHub,
and `<your_project_name>` with the name you chose for your project repository.

3. Navigate to your cloned user project repository at the command line, and run

```sh
python setup_project.py
```

answering the prompts given.

4. To check that your user project compiles correctly, at the command line
   navigate to a build folder (outside the Chaste or project source folder -- see
   the [CMake Build Guide](../../dev-guides/cmake-build-guide)) and run

```sh
ccmake path/to/Chaste
```

Type `c` to configure; when this process is complete, type `e` to exit the
configuration. You should find that four additional lines have been added to
`cmake`. These are

- `Chaste_ENABLE_project_<your_project_name>`
- `Chaste_ENABLE_project_<your_project_name>_APPS`
- `Chaste_ENABLE_project_<your_project_name>_INSTALL`
- `Chaste_ENABLE_project_<your_project_name>_TESTING`

Type `c` to configure once more, then `e` to exit and `g` to generate. When this process is complete, type

```sh
make TestHello
ctest -R TestHello$
```

and check that `TestHello` passes.

You can now start altering the code, adding your own tests, source and updating
the Readme!

### Releasing a User Project

Typically you'll want to do this when there is a particular version of code
associated with a paper/project that you want to provide as a download. Once
your user project is ready for release, the recommended route is simply to
follow the
[GitHub release guide](https://help.github.com/articles/creating-releases/).

#### Archiving

Since Git repos can be deleted by their owner at any point, it is also good
practice to permanently archive a copy of your repo somewhere. There are a few
routes for this:

- [Zenodo](https://zenodo.org/) is one tool for doing this -- 
  [instructions here](https://guides.github.com/activities/citable-code/).
- [Figshare](https://figshare.com/) is another --
  [instructions here](https://help.figshare.com/article/how-to-connect-figshare-with-your-github-account).

Both have the benefit of providing you with a
[doi](https://en.wikipedia.org/wiki/Digital_object_identifier) to enable people
to cite your code.


### Converting an old SVN user project to a GitHub repository

This guide is a strategy for converting an existing old-style Chaste SVN user
project to a GitHub repository, keeping all commit history and author
contributions.

It assumes you have `git svn` installed, and that you have a personal GitHub
account.

1. Set up an empty GitHub repository of the same name as the user project you wish to convert.

2. Create an 'authors file' that maps svn user names with git users' email addresses. It
   should contain a line for each contributor to your user project:

```sh
SvnUsername = Firstname Lastname <email_address@cs.ox.ac.uk>
```

3. Run the following

```sh
git svn clone https://chaste.cs.ox.ac.uk/svn/chaste/projects/<user_project_name> --authors-file=users.txt
cd <user_project_name>
git remote add origin git@github.com:<your_github_username>/<user_project_name>.git
git push -u origin master
```

4. Clone this new git repository, and follow
   [user project guide above](#user-project-guide) above to check everything is
   working.
