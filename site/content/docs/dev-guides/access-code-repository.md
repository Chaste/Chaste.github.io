---
title: "Access Code Repository"
description: "Access Code Repository"
draft: false
images: []
toc: true
layout: "single"
---

We offer read-only access to the Chaste repository for anyone. This access is provided with the caveat that the code is always in development (and the `develop` branch is not guaranteed to be passing all tests), and we will not be able to provide full support for between-release versions of the code. New users should therefore download one of the source releases, or instructions are given here on how to use git to get a released version. If you want to develop Chaste and contribute back to the project you have to use the `develop` branch.

The repository uses [Git](https://git-scm.com/) to manage code versioning.  You can clone from Git via an IDE plug-in, or by using a command-line client. To create a new directory called Chaste with a copy of the Chaste repository do:


```
$ git clone -b develop https://github.com/Chaste/Chaste.git Chaste
```


Note that this command will setup your local branch to point to the `develop` branch of the remote repository. There are other options:

| **Branch** | **What it's for** |
|---|---|
| `develop` | Bleeding-edge development code, new feature (ticket) branches should branch off here to minimise conflicts |
| `release` | Latest released code - updated roughly every 6 months |
| Release Tags | Released code for a certain Chaste version (e.g. v2021.1), also accessible from [GitHub](https://github.com/Chaste/Chaste/releases) with nice instructions! |


Which branch you use is up to you, if you are using Chaste for the basis of a paper we'd suggest either using:

* `develop` -- you might have to wait a few months for an official release, but will get most of the latest features; or
* `release` -- for the latest full release of Chaste. Past releases are all tagged in the git repository, or you can download them from the main Chaste website.


To get the latest release via the source code do the above `git clone` command then:

```
cd Chaste
git checkout release
```


To get a past release via the source code do the above `git clone` command then:

```
cd Chaste
git tag
```

This will list all available release tags. It should be evident which is which and you can get a copy with e.g.

```
git checkout tags/release_2021.1
```
