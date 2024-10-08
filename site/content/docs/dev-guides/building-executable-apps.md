---
title: "Building Executable Applications"
description: "Building Executable Applications"
draft: false
images: []
toc: true
layout: "single"
---

This page is a guide on making standalone executable applications that don’t use
the CxxTest framework. By _executable application_ or _app_, we mean any `.cpp`
file with its own `main` function, making use of Chaste functionality.

## App locations

The [Chaste build system](../cmake-build-guide) assumes that the following
locations may contain apps:

- `Chaste/apps/src` (contains the Cardiac executable)
- `Chaste/projects/<project_name>/apps/src` (see
  [User Projects](../../user-guides/user-projects) if you are unfamiliar with user projects)

## Building the app

To build an app, first configure Chaste as normal:

```sh
cmake /path/to/Chaste
```

{{< callout context="note" title="Note" icon="outline/info-circle" >}}

You may wish to switch on an optimised build - longer to compile, faster to run - when compiling executables for repeated/production use, see [cmake build guide](../cmake-build-guide/) and the options for `CMAKE_BUILD_TYPE` for how to switch on these compiler flags.

{{< /callout >}}


If you are building an app in `Chaste/apps/src`, you should see something
similar to the following as part of the output:

```
...
Configuring main Chaste apps
Configuring MeshConvert app
Configuring Chaste app
...

```

The `Chaste` app is the "cardiac executable", see [Cardiac Executable Tutorials](../../user-tutorials/cardiac-executable/) for how to use it.
If you have made a new app within a [user project](../../user-guides/user-projects/), you should see something similar to:

```
...
Configuring project project_<project_name>
Configuring tests for project project_<project_name>
Configuring apps for project project_<project_name>
Configuring <app_name_1> app for project_<project_name>
Configuring <app_name_2> app for project_<project_name>
...

```

You then simply build the app as you would any other target:

```sh
make -j4 <app_name>
```

The executable app will be created in either:

- `/path/to/build_dir/apps`
- `/path/to/build_dir/projects/<project_name>/apps`

depending on whether the app is in the main Chaste apps directory, or a project
directory.
