---
title: "Software Engineering Approach"
description: "Software Engineering Approach"
draft: false
images: []
toc: true
layout: "single"
---

## Overview

Chaste aims to demonstrate correctness through substantial testing and automation.
With new operating systems, platforms, architectures, compilers and dependency versions constantly being released, it is important that we continue to demonstrate that Chaste enables reproducible and replicable science.

Our [testing strategy](../testing-strategy) describes our approach to writing tests using the [CxxTest](https://github.com/CxxTest/cxxtest) unit testing framework, and how those tests are organised. This page describes how those tests are automated using [GitHub actions](https://github.com/features/actions) and other tools.

## Cross-platform support

Chaste is primarily tested on [Ubuntu Long Term Support](https://ubuntu.com/about/release-cycle) (LTS) versions.
These are released in April of every even-numbered year, and typically remain in support for 5 years.

Cross-platform support is recommended via our [pre-configured Docker images](https://github.com/Chaste/chaste-docker) which allow you to run Chaste on your local hardware whether you use Windows, macOS or Linux, and whether you have amd64 or arm64 hardware.

Alternatively, you can use Chaste in the browser via [GitHub codespaces](https://github.com/features/codespaces).

## Testing with different compilers

Our strategy is to compile Chaste with a wide range of warnings and diagnostics enabled, and to treat compilation warnings as errors.
Each C++ compiler provides different warnings and diagnostics, and results in different compiled code.

We compile Chaste with as many different compilers as possible, to ensure that we use a safe and modern subset of the C++ language, and that new warnings and diagnostics are enabled as they become available.

Chaste is compiled with:

- [GCC](https://gcc.gnu.org/): every version available on the latest [GitHub hosted Ubuntu runner](https://docs.github.com/en/actions/using-github-hosted-runners/using-github-hosted-runners/about-github-hosted-runners)
- [Clang](https://clang.llvm.org/): every version available on the latest [GitHub hosted Ubuntu runner](https://docs.github.com/en/actions/using-github-hosted-runners/using-github-hosted-runners/about-github-hosted-runners)
- [Intel](https://www.intel.com/content/www/us/en/developer/tools/oneapi/dpc-compiler.html): latest version

## Additional portability testing

We aim for Chaste to work, where reasonably possible, with all new versions of dependencies.
We test a range of dependency versions, including:

- Default versions on [Ubuntu Long Term Support](https://ubuntu.com/about/release-cycle)
- Default versions on current interim Ubuntu releases
- All newer versions, where we have been able to verify compatibility

We maintain a table of dependency versions that we expect to be compatible:
<https://chaste.github.io/docs/installguides/dependency-versions/>

## Other testing

In addition, we use GitHub actions workflows for the following purposes:

- Testing code coverage. Chaste aims for 100% line coverage with our extensive suite of unit tests. We upload coverage results to [Codecov](https://about.codecov.io/).
- Memory testing. We use [valgrind](https://valgrind.org/) to detect memory management and threading bugs, and automatically generate a report from each checked commit: <https://chaste.github.io/memory-testing/>
- Profiling. We use [GNU gprof](https://ftp.gnu.org/old-gnu/Manuals/gprof-2.9.1/html_mono/gprof.html) to profile and monitor performance of a subset of our unit tests, and generate a report from each checked commit: <https://chaste.github.io/profiling-gprof/>
- API documentation is automatically generated for each commit on the [develop](https://github.com/Chaste/Chaste/tree/develop/) branch, meaning our [latest doxygen](https://chaste.github.io/doxygen-latest/) is always up-to-date.
- [User tutorials](https://chaste.github.io/docs/user-tutorials/) and [how-tos](https://chaste.github.io/docs/how-tos/) are automatically generated, ensuring the webpages are always up-to-date with the [develop](https://github.com/Chaste/Chaste/tree/develop/) branch
