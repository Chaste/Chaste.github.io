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

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
This page reflects the status of the current trunk code. If you are looking for
information about supported dependency versions for a
[previous release](https://github.com/Chaste/Chaste/releases) of Chaste, see
instead the copy of this page bundled with that release.
{{< /callout >}}

The [Developer Install Guide](../../dev-guides/developer-install-guide) should generally be
updated to reflect installation instructions for one of the preferred versions.

## Key to tables

| Symbol | Label         | Description                                                                                                                                                                                                                                                                               |
| :----- | :------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 🟢      | Preferred     | These are preferred versions which we regularly test and have no known problems with. We intend to maintain Chaste compatibility for as long as practical (usually longer than the package developers). Our preferred versions are normally the defaults in an Ubuntu LTS.                |
| 🟩      | Supported     | These are versions that we test against regularly and so should pass all standard tests. They are not our preferred versions because they might have small bugs, or not have as many features, or won't be supported for as long (e.g. because they're not the default in an Ubuntu LTS). |
| 🟨      | Should Work   | These versions are expected to work. We've generally tested them at least once, but these versions are not regularly tested with the development code.                                                                                                                                    |
| 🟦      | Future        | We do not yet support these versions, but plan to add support for them in the future. This may just mean we have not yet had the chance to test them for compatibility and adapt the code for them if needed.                                                                             |
| 🟪      | Sunsetting    | These versions will not be supported in future releases. However, they may work with the current Chaste release, and perhaps/probably/parts-of the development version.                                                                                                                   |
| 🟥      | Not Supported | These versions are not compatible/supported, either because they have bugs, or are deprecated because they don't do everything we need now, or are too old to continue tested support for.                                                                                                |

## Build Systems

The supported build system is now CMake. Preferred versions are those that are
default on Ubuntu LTS releases, but we expect every version of CMake above the
minimum required to work fine.

<table>
  <tr>
    <th>CMake</th>
  </tr>
  <tr>
    <!-- CMake -->
    <td>
    🟨 4.3
    <br>
    🟢 4.2 <sup>4</sup>
    <br>
    🟨 4.0 -- 4.1
    <br>
    🟨 3.29 -- 3.31
    <br>
    🟢 3.28 <sup>3</sup>
    <br>
    🟪 3.23 -- 3.27
    <br>
    🟪 3.22.1 <sup>2</sup> (minimum supported version)
    <br>
    🟥 &lt;3.22.1
    </td>
 </tr>
</table>

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
Scons was the legacy build system and is no longer supported.
{{< /callout >}}

## Compilers

Preferred compiler versions are the default versions of GCC and Clang on Ubuntu
LTS releases, and specific versions of the Intel compiler that we regularly test
Chaste with. We expect all other C++17-capable versions of GCC, Clang and Intel
to compile Chaste with no problems.

<table>
  <tr>
    <th>GCC<sup>†</sup></th>
    <th>Clang<sup>†</sup></th>
    <th>Intel oneAPI</th>
  </tr>
  <tr>
    <!-- GCC -->
    <td>
      🟦 16.x
      <br>
      🟢 15.x <sup>4</sup>
      <br>
      🟢 14.x
      <br>
      🟢 13.x <sup>3</sup>
      <br>
      🟪 &lt;13
      <br>
      🟥 &lt;9
    </td>
    <!-- Clang -->
    <td>	
      🟦 22.x
      <br>
      🟦 21.x <sup>4</sup>
      <br>
      🟦 20.x
      <br>
      🟦 19.x
      <br>
      🟢 18.x <sup>3</sup>
      <br>
      🟪 &lt;18
      <br>
      🟥 &lt;11
    </td>
    <!-- Intel oneAPI -->
    <td>
      🟢 2026.x
      <br>
      🟨 2025.x
      <br>
      🟨 2024.x
      <br>
      🟨 2023.x
      <br>
      🟨 2022.x
      <br>
      🟨 2021.x
      <br>
      🟥 &lt;2021
    </td>
 </tr>
</table>

<sup>†</sup> Recent Ubuntu versions provide numerous compilers, including older versions and backports of newer ones when available. Therefore we indicate the default versions of GCC and Clang in each Ubuntu LTS, and use that when determining what is sunsetting and unsupported. The "preferred" versions are either available in a supported Ubuntu LTS, or are regularly tested.


## Libraries

Preferred library versions are the default versions on Ubuntu LTS releases, and
specific versions that we regularly test Chaste with.

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
In some instances the version number is linked to the GitHub issue in which support was/is being introduced.
{{< /callout >}}

<table>
  <tr>
    <th>Boost</th>
    <th>HDF5</th>
    <th>ParMETIS</th>
    <th>PT-Scotch</th>
    <th>PETSc</th>
    <th>SUNDIALS</th>
    <th>VTK</th>
    <th>Xerces-C</th>
    <th>XSD</th>
  </tr>
  <tr>
     <!-- Boost -->
    <td>
      🟩 <a href="https://github.com/Chaste/Chaste/issues/520">1.91</a>
      <br>
      🟢 <a href="https://github.com/Chaste/Chaste/issues/517">1.90</a> <sup>4</sup>
      <br>
      🟩 <a href="https://github.com/Chaste/Chaste/issues/465">1.89</a>
      <br>
      🟩 <a href="https://github.com/Chaste/Chaste/issues/453">1.88</a>
      <br>
      🟨 <a href="https://github.com/Chaste/Chaste/issues/453">1.87</a>
      <br>
      🟨 <a href="https://github.com/Chaste/Chaste/issues/453">1.86</a>
      <br>
      🟨 <a href="https://github.com/Chaste/Chaste/issues/453">1.85</a>
      <br>
      🟨 <a href="https://github.com/Chaste/Chaste/issues/453">1.84</a>
      <br>
      🟢 <a href="https://github.com/Chaste/Chaste/issues/257">1.83</a> <sup>3</sup>
      <br>
      🟪 &lt;1.83
      <br>
      🟥 &lt;1.74
    </td>
    <!-- HDF5 -->
    <td>
      🟦 2.1
      <br>
      🟦 2.0
      <br>
      🟢 <a href="https://github.com/Chaste/Chaste/issues/375">1.14.6</a> <sup>4</sup>
      <br>
      🟨 <a href="https://github.com/Chaste/Chaste/issues/375">1.14.5</a>
      <br>
      🟨 <a href="https://github.com/Chaste/Chaste/issues/375">1.14.4</a>
      <br>
      🟨 <a href="https://github.com/Chaste/Chaste/issues/375">1.14.3</a>
      <br>
      🟩 <a href="https://github.com/Chaste/Chaste/issues/375">1.14.2</a>
      <br>
      🟨 <a href="https://github.com/Chaste/Chaste/issues/375">1.14.1</a>
      <br>
      🟨 <a href="https://github.com/Chaste/Chaste/issues/375">1.14.0</a>
      <br>
      🟨 1.12.3
      <br>
      🟨 <a href="https://github.com/Chaste/Chaste/issues/163">1.12.2</a>
      <br>
      🟩 <a href="https://github.com/Chaste/Chaste/issues/163">1.12.1</a>
      <br>
      🟩 <a href="https://github.com/Chaste/Chaste/issues/163">1.12.0</a>
      <br>
      🟨 1.10.11
      <br>
      🟢 <a href="https://github.com/Chaste/Chaste/issues/257">1.10.10</a> <sup>3</sup>
      <br>
      🟪 &lt;1.10.10
      <br>
      🟥 &lt;1.10.7
    </td>
    <!-- ParMETIS -->
    <td>
      🟢 4.0 <sup>1,2,3</sup>
      <br>
      🟥 &lt;4.0
    </td>
    <!-- PT-Scotch -->
    <td>
      🟢 <a href="https://github.com/Chaste/Chaste/issues/424#issuecomment-3339310468">7.0 (≥7.0.9)</a> <sup>4</sup>
      <br>
      🟩 <a href="https://github.com/Chaste/Chaste/issues/424#issuecomment-3339310468">7.0 (&lt;7.0.9)</a>
      <br>
      🟥 &lt;7.0
    </td>
    <!-- PETSc -->
    <td>
      🟩 <a href="https://github.com/Chaste/Chaste/issues/522">3.25</a>
      <br>
      🟢 <a href="https://github.com/Chaste/Chaste/issues/456">3.24</a> <sup>4</sup>
      <br>
      🟩 <a href="https://github.com/Chaste/Chaste/issues/405">3.23</a>
      <br>
      🟩 <a href="https://github.com/Chaste/Chaste/issues/327">3.22</a>  
      <br>
      🟩 <a href="https://github.com/Chaste/Chaste/issues/327">3.21</a>
      <br>
      🟩 3.20 
      <br>
      🟢 <a href="https://github.com/Chaste/Chaste/issues/257">3.19</a> <sup>3</sup>
      <br>
      🟪 &lt;3.19
      <br>
      🟥 &lt;3.15
    </td>
    <!-- SUNDIALS -->
    <td>
      🟩 <a href="https://github.com/Chaste/Chaste/issues/457">7.7</a>
      <br>
      🟨 <a href="https://github.com/Chaste/Chaste/issues/457">7.6</a>
      <br>
      🟦 <a href="https://github.com/Chaste/Chaste/issues/457">7.5</a>
      <br>
      🟦 <a href="https://github.com/Chaste/Chaste/issues/457">7.4</a>
      <br>
      🟦 <a href="https://github.com/Chaste/Chaste/issues/457">7.3</a>
      <br>
      🟩 <a href="https://github.com/Chaste/Chaste/issues/266">7.2</a>
      <br>
      🟢 <a href="https://github.com/Chaste/Chaste/issues/266">7.1</a> <sup>4</sup>
      <br>
      🟩 <a href="https://github.com/Chaste/Chaste/issues/266">7.0</a>
      <br>
      🟩 6.7
      <br>
      🟨 6.6
      <br>
      🟨 6.5
      <br>
      🟢 <a href="https://github.com/Chaste/Chaste/issues/257">6.4</a> <sup>3</sup>
      <br>
      🟪 &lt;6.4
      <br>
      🟥 &lt;5.8
    </td>
    <!-- VTK -->
    <td>
      🟩 <a href="https://github.com/Chaste/Chaste/issues/523">9.6</a>
      <br>
      🟢 <a href="https://github.com/Chaste/Chaste/issues/458">9.5</a>  <sup>4</sup>
      <br>
      🟩 <a href="https://github.com/Chaste/Chaste/issues/458">9.4</a>
      <br>
      🟢 <a href="https://github.com/Chaste/Chaste/issues/257">9.3</a>
      <br>
      🟩 <a href="https://github.com/Chaste/Chaste/issues/36">9.2</a>
      <br>
      🟢 <a href="https://github.com/Chaste/Chaste/issues/36">9.1</a>  <sup>2,3</sup>
      <br>
      🟪 &lt;9.1
      <br>
      🟥 &lt;7.1
    </td>
    <!-- Xerces-C  -->
    <td>
      🟩 <a href="https://github.com/Chaste/Chaste/issues/524">3.3</a>
      <br>
      🟢 3.2 <sup>1,2,3,4</sup>
      <br>
      🟥 &lt;3.2
    </td>
    <!-- XSD  -->
    <td>
      🟩 <a href="https://github.com/Chaste/Chaste/issues/526">4.2</a>
      <br>
      <s>⬛ <a href="https://codesynthesis.com/download/xsd/4.1/README">4.1</a></s>
      <br>
      🟢 4.0 <sup>2,3,4</sup>
      <br>
      🟥 &lt;4.0
    </td>
 </tr>
</table>

{{< callout context="caution" title="Caution" icon="outline/alert-triangle" >}}
Some versions of dependencies have quirks that may not be documented on this
page, but you may find hints in the documentation for the dependency.
{{< /callout >}}

<small>
<p>1. Available on Ubuntu 20.04 LTS Focal Fossa.</p>
<p>2. Available on Ubuntu 22.04 LTS Jammy Jellyfish.</p>
<p>3. Available on Ubuntu 24.04 LTS Noble Numbat.</p>
<p>4. Available on Ubuntu 26.04 LTS Resolute Raccoon.</p>
</small>
