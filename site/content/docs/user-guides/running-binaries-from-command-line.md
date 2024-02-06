---
title: "How to run binaries directly rather than via ctest"
description: "How to run binaries directly rather than via ctest"
draft: false
images: []
toc: true
layout: "single"
---

The recommended way to run test suite binaries is via `ctest`.
See the [CmakeBuildGuide](https://github.com/Chaste/trac_archive/wiki/ChasteGuides_CmakeBuildGuide#TestingStep) for more information.
This information assumes you are using a build directory `BUILD_DIR`, and that you have created a binary by first running `cmake` and then building a target using `make`.

Binaries for each component are created in

```

$BUILD_DIR/component/test

```

regardless of any directory structure within the component itself.
For instance, let us assume you have built the `mesh` component and wish to run the test suite `/mesh/test/writer/TestMeshWriters.hpp`.
The binary will be found at

```

$BUILD_DIR/mesh/test/TestMeshWriters

```




## Previous instructions
This page replaces the previous instructions for running binaries built with scons, now available here: [SconsArchive/RunningBinariesFromCommandLine](https://github.com/Chaste/trac_archive/wiki/Scons-Archive-_-Running-Binaries-From-Command-Line).
