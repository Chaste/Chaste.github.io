---
title: "Supported versions of our dependencies"
description:  "Supported versions of our dependencies"
draft: false
images: []
toc: true
layout: "single"
---

Chaste has a number of dependencies. If you are using the 
[Ubuntu package](../ubuntu-package) then the best versions are selected and 
installed automatically for you.

If you are doing a manual linux installation, then this page shows you the 
supported and preferred versions of each dependency. Note that it reflects the 
status of the current trunk code, rather than previous releases of Chaste; see 
instead the copy of this page associated with a release for that information.

The [main install guide](InstallGuides/InstallGuide) should generally be 
updated to reflect installation instructions for one of the preferred versions.

## Key to tables
|  Symbol | Label       | Description | 
| :------ | :---------- | :---------- | 
| 🟢      | Preferred   | These are preferred versions which we regularly test and have no known problems with. We intend to maintain Chaste compatibility for as long as practical (usually longer than the package developers). Our preferred versions are normally the defaults in an Ubuntu LTS. | 
| 🟩      | Supported   | These are versions that we test against regularly and so should pass all standard tests. They are not our preferred versions because they might have small bugs, or not have as many features, or won't be supported for as long (e.g. because they're not the default in an Ubuntu LTS). | 
| 🟨      | Should Work | These versions are expected to work. We've generally tested them at least once, but these versions are not regularly tested with the development code. | 
| 🟦      | Future      | We do not yet support these versions, but plan to add support for them in the future. This may just mean we have not yet had the chance to test them for compatibility and adapt the code for them if needed. | 
| 🟪      | Sunsetting  | These versions will work with the current Chaste release, and perhaps/probably/parts-of the development version, but will not be supported in future releases. | 
| 🟥      | Not Supported | These versions are not compatible/supported, either because they have bugs, or are deprecated because they don't do everything we need now, or are too old to continue tested support for. | 
