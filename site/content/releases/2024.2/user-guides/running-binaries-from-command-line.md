---
title: "Running Binaries From Command Line"
description: "Running binaries from command line"
draft: false
images: []
toc: true
layout: "single"
version: "2024.2"
---

This page explains how to run binaries directly rather than via `ctest`.

{{< callout context="note" title="Note" icon="outline/info-circle" >}}

The recommended way to run test suite binaries is via `ctest`. See the
[CMake Build Guide](../../dev-guides/cmake-build-guide#testing-step)
for more information.

{{< /callout >}}

The information on this page assumes you are using a build directory
`BUILD_DIR`, and that you have created a binary by first running `cmake` and
then building a target using `make`.

Binaries for each component are created in

```sh
$BUILD_DIR/component/test
```

regardless of any directory structure within the component itself. For instance,
let us assume you have built the `mesh` component and wish to run the test suite
`/mesh/test/writer/TestMeshWriters.hpp`. The binary will be found at

```sh
$BUILD_DIR/mesh/test/TestMeshWriters
```
