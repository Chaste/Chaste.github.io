---
title: "External Developer Guide"
description: "Helpful resources for users of development versions of Chaste"
draft: false
images: []
toc: true
layout: "single"
---

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
Before you start -- if you are Chaste User, and never want to contribute back to
the source code, you might want to consider just downloading one of the
[release versions](https://github.com/Chaste/Chaste/releases) of Chaste.
{{< /callout >}}

This page is intended to assist those external to the core Chaste team who still
want to develop with the "bleeding edge" latest development code, rather than
merely the last official release.

Since some parts of the Chaste code-base are not released (e.g. those relating
specifically to papers in preparation), some of the developer resources, such as
results from the automated tests and full documentation for the latest revision,
are not made publicly available. We have now created some additional resources
to improve this situation.

## The most recent "good revision"

Occasionally broken code is committed to branches on the Chaste repository, or some
unexpected tests fail. This can be frustrating if users do not know if it's
something they've broken, or if the fault lies with the repository code. We now
offer a range of git branches to help developers choose how stable they want
their code to be:

| Branch | What it's for |
|---|---|
| `develop` | Bleeding-edge development code, new feature (issue) branches should branch off here to minimise conflicts |
| Release Tags | Released code for past Chaste versions (e.g. `2024.1`), also accessible from [GitHub](https://github.com/Chaste/Chaste/releases) with nice instructions and zip/tar files | |

You can get these revisions by cloning the repository and then doing

```sh
git checkout <branch>
```

e.g.

```sh
git checkout develop
```

## Contributing Code Back to Chaste

### Before you start

If you intend to submit code back to the main Chaste repository, please see
the [Best Practice Guide](../best-practice-guide).

### Coding Standards

To understand why Chaste variables, methods and classes are named like they are
please see our
[Coding Standards Strategy](../chaste-strategies/coding-standards-strategy).

We also lay out and document our code in a particular way -- see our
[Code Structure Strategy](../chaste-strategies/code-structure-strategy).

You may also want to read through the other
[Chaste Strategies](../chaste-strategies/) that we use to keep things consistent
and well tested.

### Creating an Issue

First [create a new issue](https://github.com/Chaste/Chaste/issues) on GitHub
and describe the problem you are trying to solve.

### Working in a new branch

Please see the [Pull Request Strategy](../chaste-strategies/pull-request-strategy) for how to work in
a new branch -- you should branch off `develop` if you want to contribute code
back to the main Chaste repository.

Make sure you merge in the latest `develop` branch into your issue branch
regularly to keep up to date and avoid lots of changes before merging back into
our main repo.

Ideally, write a comment on your issue about any commits that you have done and
pushed to your branch.

### Testing

[GitHub actions](https://github.com/Chaste/Chaste/actions) will automatically
run tests (`Continuous`, `Nightly`, `Parallel`, `coverage`, `memtest`) on a pull
request. All tests should pass before merging into `develop`. Tests can be
run locally as per the
[CMake Build Guide](../cmake-build-guide#test-packs).
