---
title: "CMake first-time user guide"
description: "Using cmake as a first-time user"
date: 2020-08-27T19:23:18+02:00
lastmod: 2020-08-27T19:23:18+02:00
draft: false
images: []
toc: true
layout: "single"
---

Chaste uses `cmake` to configure a build, `make` to compile the configured build, and `ctest` to run the resulting executables.  Each of these steps is described in more detail in other parts of this Wiki (e.g. see [the detailed CMake guide](/docs/chaste-guides/cmake-build-guide)), but this page serves simply as a quick-start guide to verify your installation.

This page will walk you through a *first run* of Chaste: building and running the *Continuous Test Pack*.

## Prerequisites
You must have obtained the source code and installed the dependencies.  See [GettingStarted](/getting-started) if you haven't yet.

## Setting up a build directory
Let us assume you have the Chaste source code in the directory:

```

/path/to/Chaste_source_code

```


Create an empty `chaste_build` directory outside the source directory, and change into it:

```

mkdir /path/to/chaste_build
cd /path/to/chaste_build

```


## Configure step
The first step is to configure Chaste using `cmake`.  This will locate all dependencies, and generate the build targets.


```

cmake /path/to/Chaste_source_code

```


This command will print a bunch of things to the terminal.  If it runs without any errors, the last lines of the output will be:


```

-- Configuring done
-- Generating done
-- Build files have been written to: /path/to/chaste_build

```


If you do see errors, you may need to set some paths to dependencies manually, see [Finding Chaste Dependencies](/docs/chaste-guides/finding-chaste-dependencies).

## Build step
Next, we compile Chaste using the `make` utility.
In this guide, we will compile the Continuous test pack; the core set of unit tests that will determine whether everything is working as expected.


```

make -j4 Continuous

```


(Note the capital C!) The `-j4` will speed up the compilation by using 4 cores on your processor; adjust this number if you have more or fewer cores available.  This step should take around 90 minutes, depending on your machine.

If this command runs with no errors, the last lines of the output will be:

```

[100%] Built target Continuous
program finished with exit code 0
elapsedTime=<some_amount_of_time>

```


## Testing step
Now that the Continuous test pack is compiled, we run the tests using `ctest`:


```

ctest -j4 -L Continuous

```


If all the tests pass, you should see the following towards the end of the output:


```

100% tests passed, 0 tests failed out of 366

Label Time Summary:
...
...

```


If you see this, you're good to go!
Head over to [the chaste guides](/docs/chaste-guides/running-chaste) for next steps.

## Troubleshooting

### Users of the Ubuntu package
If you installed Chaste with the [Ubuntu package](install-guides/ubuntu-package), it really ought to work out-of-the-box!

After re-trying these steps, please let us know on our [users' mailing list](https://web.maillist.ox.ac.uk/ox/subscribe/chaste-users).

### Users on non-Ubuntu Linux distributions
First, check that the version of each dependency is listed as *supported* on our [dependency versions page](/install-guides/dependency-versions).

If you are using supported package versions, you may need to provide CMake with some hints for finding dependencies, during the configure step.
You can find details in the more detailed [CMake build guide](/docs/chaste-guides/cmake-build-guide#ConfigureStep).

If you are still having problems, please let us know on our [users' mailing list](https://web.maillist.ox.ac.uk/ox/subscribe/chaste-users).

### Users on Mac OS X
Check out the [OS X installation instructions](/install-guides/ChasteInstallationOnOSXYosemite).
Please note that these instructions may become quickly out-of-date due to Home Brew always brewing the very latest package versions.

If you are still having problems, please let us know on our [users' mailing list](https://web.maillist.ox.ac.uk/ox/subscribe/chaste-users).

### Users on Windows
Good luck!

## See also
[CMake Build Guide](/docs/chaste-guides/cmake-build-guide) for a list of all available cmake configuration options - how to do optimised builds, parallel builds, run memory testing etc.
