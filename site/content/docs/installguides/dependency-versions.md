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

| CMake         |            |         |         |         |         |         |         |         |         |         |         |         |         |
| ------------- | ---------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
| 🟥 &lt;3.16.3 | 🟩 3.16.3+ | 🟨 3.17 | 🟨 3.18 | 🟨 3.19 | 🟨 3.20 | 🟨 3.21 | 🟢 3.22 | 🟨 3.23 | 🟨 3.24 | 🟨 3.25 | 🟨 3.26 | 🟨 3.27 | 🟨 3.28 |

{{< callout context="note" title="Note" icon="info-circle" >}}
Scons was the legacy build system and is no longer supported.
{{< /callout >}}

## Compilers

Preferred compiler versions are the default versions of GCC and Clang on Ubuntu
LTS releases, and specific versions of the Intel compiler that we regularly test
Chaste with. We expect all other C++17-capable versions of GCC, Clang and Intel
to compile Chaste with no problems.

| GCC     | Clang   | Intel oneAPI |
|:--------|:--------|:-------------|
| 🟦 13.x | 🟦 17.x | 🟢 2024.x    |
| 🟢 12.x | 🟦 16.x | 🟨 2023.x    |
| 🟨 11.x | 🟦 15.x | 🟨 2022.x    |
| 🟢 10.x | 🟢 14.x | 🟨 2021.x    |
| 🟩 9.x  | 🟨 13.x |              |
| 🟨 8.x  | 🟢 12.x |              |
| 🟨 7.x  | 🟨 11.x |              |
| 🟥 <7.0 | 🟨 10.x |              |
|         | 🟨 9.x  |              |
|         | 🟨 8.x  |              |
|         | 🟨 7.x  |              |
|         | 🟨 6.x  |              |
|         | 🟥 <6.0 |              |

## Libraries

Preferred library versions are the default versions on Ubuntu LTS releases, and
specific versions that we regularly test Chaste with.

{{< callout context="note" title="Note" icon="info-circle" >}}
In some instances the version number is linked to the GitHub issue in which support was/is being introduced.
{{< /callout >}}

| Boost          | HDF5              | ParMETIS | PETSc          | SUNDIALS | VTK           | Xerces    | XSD     |
|:---------------|:------------------|:---------|:---------------|:---------|:--------------|:----------|:--------|
| 🟦 1.84        | 🟦 1.14.3         | 🟢 4.0   | 🟦 3.20        | 🟦 6.7   | 🟦 9.3        | 🟦 3.2.5  | 🟢 4.0  |
| 🟦 1.83        | 🟦 1.14.2         | 🟥 <4.0  | 🟦 3.19        | 🟦 6.6   | 🟩 [9.2][i36] | 🟩 3.2.4  | 🟥 <4.0 |
| 🟦 1.82        | 🟦 1.14.1         |          | 🟦 3.18        | 🟦 6.5   | 🟢 [9.1][i36] | 🟢 3.2.3  |         |
| 🟦 1.81        | 🟦 1.14.0         |          | 🟦 3.17        | 🟦 6.4   | 🟩 [9.0][i36] | 🟢 3.2.2  |         |
| 🟦 1.80        | 🟦 1.12.3         |          | 🟦 3.16        | 🟦 6.3   | 🟩 8.2        | 🟩 3.2.1  |         |
| 🟦 1.79        | 🟩 [1.12.2][i163] |          | 🟢 [3.15][i37] | 🟦 6.2   | 🟨 8.1        | 🟥 <3.2.1 |         |
| 🟨 [1.78][i28] | 🟨 [1.12.1][i163] |          | 🟩 3.14        | 🟦 6.1   | 🟨 8.0        |           |         |
| 🟨 [1.77][i28] | 🟨 [1.12.0][i163] |          | 🟩 3.13        | 🟩 6.0   | 🟢 7.1        |           |         |
| 🟨 [1.76][i28] | 🟦 1.10.11        |          | 🟢 3.12        | 🟢 5.8   | 🟨 7.0        |           |         |
| 🟨 [1.75][i28] | 🟦 1.10.10        |          | 🟥 <3.12       | 🟨 5.7   | 🟩 6.3        |           |         |
| 🟢 1.74        | 🟦 1.10.9         |          |                | 🟨 5.6   | 🟥 <6.3       |           |         |
| 🟩 1.73        | 🟩 1.10.8         |          |                | 🟨 5.5   |               |           |         |
| 🟨 1.72        | 🟢 1.10.7         |          |                | 🟨 5.4   |               |           |         |
| 🟩 1.71        | 🟩 1.10.6         |          |                | 🟨 5.3   |               |           |         |
| 🟨 1.70        | 🟩 1.10.5         |          |                | 🟨 5.2   |               |           |         |
| 🟩 1.69        | 🟢 1.10.4         |          |                | 🟨 5.1   |               |           |         |
| 🟨 1.68        | 🟥 <1.10.4        |          |                | 🟨 5.0   |               |           |         |
| 🟢 1.67        |                   |          |                | 🟩 4.1   |               |           |         |
| 🟥 <1.67       |                   |          |                | 🟨 4.0   |               |           |         |
|                |                   |          |                | 🟩 3.2   |               |           |         |
|                |                   |          |                | 🟢 3.1   |               |           |         |
|                |                   |          |                | 🟥 <3.1  |               |           |         |

{{< callout context="caution" title="Caution" icon="alert-triangle" >}}
Some versions of dependencies have quirks that may not be documented on this
page, but you may find hints in the documentation for the dependency.
{{< /callout >}}


[//]: # "Reference Links"
[i28]: https://github.com/Chaste/Chaste/issues/28
[i36]: https://github.com/Chaste/Chaste/issues/36
[i37]: https://github.com/Chaste/Chaste/issues/37
[i163]: https://github.com/Chaste/Chaste/issues/163
