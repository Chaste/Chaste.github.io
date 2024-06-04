---
title : "Changes since last release"
date: 2020-10-06T08:47:36+00:00
draft: false
images: []
toc: true
---



**Users:** If you are working with the develop branch and your local code or project has been broken
by a recent interface change then please see here for fix suggestions.

**Developers:** Please mention any changes to the code which will break users' code here - to be put in the release notes for the next release.  Also mention any significant improvements or new features.  The real definitive release notes will be written in [release notes](../release-notes)  at the time of release.  To make that process easier, please structure this page in the same manner.


## Changes since last release appear below
---

## (changes since Release 2024.1)

### Headline features

- [#270](https://github.com/Chaste/Chaste/issues/270) The default location of test output is now the subdirectory `testoutput` of the build directory (the directory that `cmake` is run from). The old default behaviour was `tmp\${USER}\testoutput`. It is still recommended to set the environment variable `CHASTE_TEST_OUTPUT` to override this default behaviour.

### Dependency changes

### Core

### Heart

### Cell Based

### Future Plans
