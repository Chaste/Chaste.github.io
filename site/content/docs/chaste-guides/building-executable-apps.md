# Building Executable Applications

By *Executable Applications* or *app*, we mean any `.cpp` file with its own `main` function, making use of Chaste functionality.


The [Chaste build system](/chaste-guides/cmake-build-guide) assumes that the following locations may contain apps:

* `Chaste/apps/src` (contains the Cardiac executable)
* `Chaste/projects/<project_name>/apps/src` (see [ChasteGuides/UserProjects](/chaste-guides/user-projects) if you are unfamiliar with user projects)


To build an app, first configure Chaste as normal:

```
cmake /path/to/Chaste

```


If you are building an app in `Chaste/apps/src`, you should something similar to the following as part of the output:

```
...
Configuring main Chaste apps
Configuring MeshConvert app
Configuring Chaste app
...

```


and if your app is in a project, you should see something similar to:


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

```
make -j4 <app_name>

```


The executable app will be created in either:

* `/path/to/build_dir/apps`
* `/path/to/build_dir/projects/<project_name>/apps`


depending on whether the app is in the main Chaste apps directory, or a project directory.

# Previous instructions
This page supersedes the previous instructions for building the Cardiac Executable, now available here: [SconsArchive/BuildingCardiacExecutable](/scons-archive/building-cardiac-executable).
