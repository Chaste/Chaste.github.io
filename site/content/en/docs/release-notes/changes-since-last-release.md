---
title : "Changes since last release"
date: 2020-10-06T08:47:36+00:00
draft: false
images: []
toc: true
---



**Users:** If you are working with the develop branch and your local code or project has been broken
by a recent interface change then please see here for fix suggestions.

**Developers:** Please mention any changes to the code which will break users' code here - to be put in the release notes for the next release.  Also mention any significant improvements or new features.  The real definitive release notes will be written in [release notes](/release-notes/release-notes)  at the time of release.  To make that process easier, please structure this page in the same manner.


## Changes since last release appear below
---

## (changes since Release 2021.1)

### Headline features
### New dependency support


### Core
* [#153](https://github.com/Chaste/Chaste/pull/153) Mesh generators now return meshes wrapped in a `boost::shared_ptr`. Existing tests that retrieve a mesh from a mesh generator should be rewritten to accept this return type. For example, a test that expected a raw mesh pointer such as `AbstractMesh<2,2>* p_mesh = generator.GetMesh()` should now be changed to `boost::shared_ptr<AbstractMesh<2,2> > p_mesh = generator.GetMesh()`. Use `p_mesh.get()` to get the raw pointer from the smart pointer if needed e.g. in assertions. See `TestRunningMeshBasedCryptSimulationsTutorial` for more examples.

### Heart
### Cell Based

* #3069 See [LatestNews](https://github.com/Chaste/trac_archive/wiki/Latest-News)  **Please replace URL with summary**


### Future Plans

