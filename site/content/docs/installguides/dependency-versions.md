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
    🟦 3.31 
    <br>
    🟦 3.30 
    <br>
    🟨 3.29 
    <br>
    🟢 3.28 <sup>3</sup> 
    <br>
    🟨 3.23 -- 3.27 
    <br>
    🟢 3.22 <sup>2</sup> 
    <br>
    🟨 3.17 -- 3.21 
    <br>
    🟩 3.16.3 (Minimum supported version)
    <br>
    🟥 &lt;3.16.3
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
    <th>GCC</th>
    <th>Clang</th>
    <th>Intel oneAPI</th>
  </tr>
  <tr>
    <!-- GCC -->
    <td>
      🟩 14.x
      <br>
      🟢 13.x <sup>3</sup>
      <br>
      🟢 12.x <sup>2</sup> 
      <br>
      🟨 11.x <sup>2</sup> 
      <br>
      🟢 10.x <sup>1</sup> <sup>2</sup> 
      <br>
      🟩 9.x <sup>1</sup> <sup>2</sup> 
      <br>
      🟪 8.x <sup>1</sup> 
      <br>
      🟪 7.x <sup>1</sup> 
      <br>
      🟥 &lt;7.0 
    </td>
    <!-- Clang -->
    <td>	
      🟦 19.x <sup>3</sup> 
      <br>
      🟩 18.x <sup>3</sup> 
      <br>
      🟩 17.x <sup>3</sup> 
      <br>
      🟩 16.x <sup>3</sup> 
      <br>
      🟩 15.x <sup>3</sup> 
      <br>
      🟩 14.x <sup>2</sup> <sup>3</sup> 
      <br>
      🟩 13.x <sup>2</sup> 
      <br>
      🟨 12.x <sup>1</sup> <sup>2</sup> 
      <br>
      🟨 11.x <sup>2</sup> 
      <br>
      🟪 10.x <sup>1</sup> 
      <br>
      🟪 9.x <sup>1</sup> 
      <br>
      🟪 8.x <sup>1</sup> 
      <br>
      🟪 7.x <sup>1</sup> 
      <br>
      🟪 6.x <sup>1</sup> 
      <br>
      🟥 &lt;6.0 
    </td>
    <!-- Intel oneAPI -->
    <td>
      🟩 2025.x
      <br>
      🟨 2024.x
      <br>
      🟨 2023.x
      <br>
      🟨 2022.x
      <br>
      🟨 2021.x
    </td>
 </tr>
</table>

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
    <th>PETSc</th>
    <th>SUNDIALS</th>
    <th>VTK</th>
    <th>Xerces-C</th>
    <th>XSD</th>
  </tr>
  <tr>
     <!-- Boost -->
    <td>
      🟦 1.87
      <br>
      🟦 1.86
      <br>
      🟦 1.85
      <br>
      🟦 1.84
      <br>
      🟢 <a href="https://github.com/Chaste/Chaste/issues/257">1.83</a> <sup>3</sup>
      <br>
      🟨 1.82
      <br>
      🟨 1.81
      <br>
      🟩 1.80
      <br>
      🟨 1.79
      <br>
      🟨 <a href="https://github.com/Chaste/Chaste/issues/28">1.78</a>
      <br>
      🟨 <a href="https://github.com/Chaste/Chaste/issues/28">1.77</a>
      <br>
      🟨 <a href="https://github.com/Chaste/Chaste/issues/28">1.76</a>
      <br>
      🟩 <a href="https://github.com/Chaste/Chaste/issues/28">1.75</a>
      <br>
      🟢 1.74 <sup>2</sup>
      <br>
      🟪 1.73 
      <br>
      🟪 1.72
      <br>
      🟪 1.71 <sup>1</sup>
      <br>
      🟥 &lt;1.71
    </td>
    <!-- HDF5 -->
    <td>
      🟦 <a href="https://github.com/Chaste/Chaste/issues/375">1.14.6</a> 
      <br>
      🟦 <a href="https://github.com/Chaste/Chaste/issues/375">1.14.5</a> 
      <br>
      🟦 <a href="https://github.com/Chaste/Chaste/issues/375">1.14.4</a>
      <br>
      🟦 <a href="https://github.com/Chaste/Chaste/issues/375">1.14.3</a>
      <br>
      🟦 <a href="https://github.com/Chaste/Chaste/issues/375">1.14.2</a>
      <br>
      🟦 <a href="https://github.com/Chaste/Chaste/issues/375">1.14.1</a>
      <br>
      🟦 <a href="https://github.com/Chaste/Chaste/issues/375">1.14.0</a>
      <br>
      🟦 1.12.3 
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
      🟨 1.10.9 
      <br>
      🟩 1.10.8 
      <br>
      🟢 1.10.7 <sup>2</sup>
      <br>
      🟪 1.10.6 
      <br>
      🟪 1.10.5 
      <br>
      🟪 1.10.4 <sup>1</sup>
      <br>
      🟥 &lt;1.10.4
    </td>
    <!-- ParMETIS -->
    <td>
      🟢 4.0 <sup>1</sup> <sup>2</sup> <sup>3</sup>
      <br>
      🟥 &lt;4.0
    </td>
    <!-- PETSc -->
    <td>
      🟦 <a href="https://github.com/Chaste/Chaste/issues/327">3.22</a>  
      <br>
      🟦 <a href="https://github.com/Chaste/Chaste/issues/327">3.21</a>
      <br>
      🟩 3.20 
      <br>
      🟢 <a href="https://github.com/Chaste/Chaste/issues/257">3.19</a> <sup>3</sup> 
      <br>
      🟩 3.18 
      <br>
      🟩 3.17 
      <br>
      🟩 3.16 
      <br>
      🟢 <a href="https://github.com/Chaste/Chaste/issues/37">3.15</a> <sup>2</sup> 
      <br>
      🟪 3.14 
      <br>
      🟪 3.13 
      <br>
      🟪 3.12 <sup>1</sup> 
      <br>
      🟥 &lt;3.12 
    </td>
    <!-- SUNDIALS -->
    <td>
      🟦 <a href="https://github.com/Chaste/Chaste/issues/266">7.2</a> 
      <br>
      🟦 <a href="https://github.com/Chaste/Chaste/issues/266">7.1</a> 
      <br>
      🟦 <a href="https://github.com/Chaste/Chaste/issues/266">7.0</a> 
      <br>
      🟩 6.7 
      <br>
      🟨 6.6 
      <br>
      🟨 6.5 
      <br>
      🟢 <a href="https://github.com/Chaste/Chaste/issues/257">6.4</a> <sup>3</sup> 
      <br>
      🟨 6.3 
      <br>
      🟨 6.2 
      <br>
      🟨 6.1 
      <br>
      🟨 6.0 
      <br>
      🟢 5.8 <sup>2</sup> 
      <br>
      🟪 5.7 
      <br>
      🟪 5.6 
      <br>
      🟪 5.5 
      <br>
      🟪 5.4 
      <br>
      🟪 5.3 
      <br>
      🟪 5.2 
      <br>
      🟪 5.1 
      <br>
      🟪 5.0 
      <br>
      🟪 4.1 
      <br>
      🟪 4.0 
      <br>
      🟪 3.2 
      <br>
      🟪 3.1 <sup>1</sup> 
      <br>
      🟥 &lt;3.1
    </td>
    <!-- VTK -->
    <td>
      🟦 9.4
      <br>
      🟢 <a href="https://github.com/Chaste/Chaste/issues/257">9.3</a>
      <br>
      🟩 <a href="https://github.com/Chaste/Chaste/issues/36">9.2</a> 
      <br>
      🟢 <a href="https://github.com/Chaste/Chaste/issues/36">9.1</a>  <sup>2</sup> <sup>3</sup> 
      <br>
      🟩 <a href="https://github.com/Chaste/Chaste/issues/36">9.0</a>  
      <br>
      🟩 8.2 
      <br>
      🟨 8.1 
      <br>
      🟨 8.0 
      <br>
      🟢 7.1 <sup>1</sup> <sup>2</sup> 
      <br>
      🟪 7.0 
      <br>
      🟪 6.3 <sup>1</sup> 
      <br>
      🟥 &lt;6.3
    </td>
    <!-- Xerces-C  -->
    <td>
      🟦 3.3
      <br>
      🟢 3.2 <sup>1</sup> <sup>2</sup> <sup>3</sup>
      <br>
      🟥 &lt;3.2
    </td>
    <!-- XSD  -->
    <td>
      🟦 4.2
      <br>
      🟦 4.1
      <br>
      🟢 4.0 <sup>2</sup> <sup>3</sup> 
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
</small>
