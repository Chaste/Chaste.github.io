---
title: Supported versions of our dependencies
description: Supported versions of our dependencies
draft: false
images: []
toc: true
layout: single
---

Chaste has a number of dependencies. If you are using the [Ubuntu package](../ubuntu-package)
then the best versions are selected and installed automatically for you. If you
are doing a manual Linux installation, then this page shows you the supported
and preferred versions of each dependency.

{{< callout context="note" title="Note" icon="info-circle" >}}
This page reflects the status of the current trunk code. If you are looking for
information about supported dependency versions for a
[previous release](https://github.com/Chaste/Chaste/releases) of Chaste, see
instead the copy of this page bundled with that release.
{{< /callout >}}

The [Developer Install Guide](../../dev-guides/developer-install-guide) should generally be
updated to reflect installation instructions for one of the preferred versions.

## Key to tables

| Symbol | Label         | Description       |
| :----- | :------------ | :---------------- |
| 🟢     | Preferred     | These are preferred versions which we regularly test and have no known problems with. We intend to maintain Chaste compatibility for as long as practical (usually longer than the package developers). Our preferred versions are normally the defaults in an Ubuntu LTS. |
| 🟩     | Supported     | These are versions that we test against regularly and so should pass all standard tests. They are not our preferred versions because they might have small bugs, or not have as many features, or won't be supported for as long (e.g. because they're not the default in an Ubuntu LTS). |
| 🟨     | Should Work   | These versions are expected to work. We've generally tested them at least once, but these versions are not regularly tested with the development code. |
| 🟦     | Future        | We do not yet support these versions, but plan to add support for them in the future. This may just mean we have not yet had the chance to test them for compatibility and adapt the code for them if needed. |
| 🟪     | Sunsetting    | These versions will not be supported in future releases. However, they may work with the current Chaste release, and perhaps/probably/parts-of the development version. |
| 🟥     | Not Supported | These versions are not compatible/supported, either because they have bugs, or are deprecated because they don't do everything we need now, or are too old to continue tested support for. |

## Build Systems

The supported build system is now CMake. Preferred versions are those that are
default on Ubuntu LTS releases, but we expect every version of CMake above the
minimum required to work fine.

| CMake      |
| ---------- | --------------- | ------- | ------- | ------- | ------- |
| 🟥 <3.16.3 | 🟩 3.16.3+ [^a] | 🟨 3.17 | 🟨 3.18 | 🟨 3.19 | 🟨 3.20 |
| 🟨 3.21    | 🟢 3.22 [^b]    | 🟨 3.23 | 🟨 3.24 | 🟨 3.25 | 🟨 3.26 |
| 🟨 3.27    | 🟨 3.28         |

{{< callout context="note" title="Note" icon="info-circle" >}}
Scons was the legacy build system and is no longer supported.
{{< /callout >}}

## Compilers

Preferred compiler versions are the default versions of GCC and Clang on Ubuntu
LTS releases, and specific versions of the Intel compiler that we regularly test
Chaste with. We expect all other C++17-capable versions of GCC, Clang and Intel
to compile Chaste with no problems.

|  GCC         |
| ------------ | ----------- | ------------ | ----------------- | ----------------- | ------------ |
| 🟥 <7.0      | 🟨 7.x [^a] |  🟨 8.x [^a] |  🟩 9.x [^b] [^a] | 🟢 10.x [^b] [^a] | 🟨 11.x [^b] |
| 🟢 12.x [^b] | 🟦 13.x     |

|  Clang       |
| ------------ | ----------------- | ------------ | ------------ | ----------- | ------------ |
| 🟥 <6.0      | 🟨 6.x [^a]       | 🟨 7.x [^a]  | 🟨 8.x [^a]  | 🟨 9.x [^a] | 🟨 10.x [^a] |
| 🟨 11.x [^b] | 🟢 12.x [^b] [^a] | 🟨 13.x [^b] | 🟢 14.x [^b] | 🟦 15.x     | 🟦 16.x      |
| 🟦 17.x      |

| Intel oneAPI |
| ------------ | ---------- | ---------- | --------- |
| 🟨 2021.x    |  🟨 2022.x |  🟨 2023.x | 🟢 2024.x |

## Libraries

Preferred library versions are the default versions on Ubuntu LTS releases, and
specific versions that we regularly test Chaste with.

{{< callout context="note" title="Note" icon="info-circle" >}}
In some instances the version number is linked to the GitHub issue in which support was/is being introduced.
{{< /callout >}}

| Boost          |
| -------------- | ------------ | ------------ | -------------- | -------------- | -------------- |
| 🟥 <1.67       | 🟢 1.67 [^a] | 🟨 1.68      | 🟩 1.69        | 🟨 1.70        | 🟩 1.71 [^a]   |
| 🟨 1.72        | 🟩 1.73      | 🟢 1.74 [^b] | 🟨 [1.75][i28] | 🟨 [1.76][i28] | 🟨 [1.77][i28] |
| 🟨 [1.78][i28] | 🟦 1.79      | 🟦 1.80      |  🟦 1.81       | 🟦 1.82        | 🟦 1.83 [^c]   |
| 🟦 1.84        | 🟦 1.85      |

| HDF5       |
| ---------- | --------------- | ---------- | ----------------- | ----------------- | ----------------- |
| 🟥 <1.10.4 | 🟢 1.10.4 [^a]  | 🟩 1.10.5  | 🟩 1.10.6         | 🟢 1.10.7 [^b]    | 🟩 1.10.8         |
| 🟦 1.10.9  | 🟦 1.10.10 [^c] | 🟦 1.10.11 | 🟨 [1.12.0][i163] | 🟨 [1.12.1][i163] | 🟩 [1.12.2][i163] |
| 🟦 1.12.3  | 🟦 1.14.0       | 🟦 1.14.1  | 🟦 1.14.2         | 🟦 1.14.3         | 🟦 1.14.4         |

| ParMETIS |
| -------- | ---------------------- |
| 🟥 <4.0  |  🟢 4.0 [^c] [^b] [^a] |

| PETSc    |
| -------- | ------------ | ------------ | ------- | ------------------- | ------- |
| 🟥 <3.12 | 🟢 3.12 [^a] | 🟩 3.13      | 🟩 3.14 | 🟢 [3.15][i37] [^b] | 🟦 3.16 |
| 🟦 3.17  | 🟦 3.18      | 🟦 3.19 [^c] | 🟦 3.20 | 🟦 3.21             |

| SUNDIALS    |
| ----------- | ------------ | ------- | ------- | -------------- | ------- |
| 🟥 <3.1     |  🟢 3.1 [^a] |  🟩 3.2 |  🟨 4.0 |  🟩 4.1        |  🟨 5.0 |
| 🟨 5.1      |  🟨 5.2      |  🟨 5.3 |  🟨 5.4 |  🟨 5.5        |  🟨 5.6 |
| 🟨 5.7      |  🟢 5.8 [^b] |  🟩 6.0 |  🟦 6.1 |  🟦 6.2        |  🟦 6.3 |
| 🟦 6.4 [^c] |  🟦 6.5      |  🟦 6.6 |  🟦 6.7 | 🟦 [7.0][i266] |

| VTK     |
| ------- | -------------- | ------------------------ | ----------------- | ------- | ------- |
| 🟥 <6.3 |  🟩 6.3 [^a]   |  🟨 7.0                  |  🟢 7.1 [^b] [^a] |  🟨 8.0 |  🟨 8.1 |
| 🟩 8.2  |  🟩 [9.0][i36] |  🟢 [9.1][i36] [^c] [^b] |  🟩 [9.2][i36]    |  🟦 9.3 |

| Xerces-C   |
| ---------- | --------- | -------------- | -------------- | -------------- | --------- |
|  🟥 <3.2.1 |  🟩 3.2.1 |  🟢 3.2.2 [^a] |  🟢 3.2.3 [^b] |  🟢 3.2.4 [^c] |  🟦 3.2.5 |

|  XSD     |
| -------- | ---------------------- | ------ |
|  🟥 <4.0 |  🟢 4.0 [^c] [^b] [^a] | 🟦 4.2 |

{{< callout context="caution" title="Caution" icon="alert-triangle" >}}
Some versions of dependencies have quirks that may not be documented on this
page, but you may find hints in the documentation for the dependency.
{{< /callout >}}

[^a]: Available on Ubuntu 20.04 LTS Focal Fossa.
[^b]: Available on Ubuntu 22.04 LTS Jammy Jellyfish.
[^c]: Available on Ubuntu 22.04 LTS Noble Numbat.

[//]: # "Reference Links"
[i28]: https://github.com/Chaste/Chaste/issues/28
[i36]: https://github.com/Chaste/Chaste/issues/36
[i37]: https://github.com/Chaste/Chaste/issues/37
[i163]: https://github.com/Chaste/Chaste/issues/163
[i266]: https://github.com/Chaste/Chaste/issues/266
