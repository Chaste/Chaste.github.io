---
title: "Profiling Chaste Code"
description: "Generating CPU profiles of Chaste tests with gperftools or gprof"
draft: false
images: []
toc: true
layout: "single"
---

This page is a guide on profiling Chaste code, so that you can see where your
simulation is spending its time. The [Chaste build system](../cmake-build-guide)
supports two profiling tools:

- [gperftools](https://github.com/gperftools/gperftools) (the Google CPU
  profiler), which produces both a text report and an SVG call graph per test;
- [GNU gprof](https://sourceware.org/binutils/docs/gprof/), which produces a
  text report per test.

We recommend gperftools: it is a low-overhead sampling profiler and its call
graphs are easy to interpret. gprof remains supported, but its output is
unlikely to be very helpful (see [the gprof section](#profiling-with-gprof)
below).

## Choosing what gets profiled

Profiling runs the `Profile` test pack. Each component's `test` folder may
contain a `ProfileTestPack.txt` file listing the test files in that pack, e.g.
`heart/test/ProfileTestPack.txt`.

To profile your own test, simply add its path to the `ProfileTestPack.txt` file
in the relevant `test` folder (creating the file if necessary — this works in
[user projects](../../user-guides/user-projects) too). A test does not need any
modification to be profiled; the build system takes care of everything.

## Profiling with gperftools

### Installing the tools

Everything needed can be installed from the Ubuntu repositories, except the
`pprof` tool used to generate the reports, which is a single Go command away:

```sh
sudo apt install libgoogle-perftools-dev graphviz golang-go
go install github.com/google/pprof@latest
```

This installs `pprof` to `~/go/bin`, where the Chaste build system will find it
automatically (there is no need to add it to your `PATH`).

{{< callout context="caution" title="Caution" icon="outline/alert-triangle" >}}

The `google-perftools` apt package also provides a `google-pprof` executable.
That is the old, deprecated perl implementation: make sure you install the Go
`pprof` as above, which is what Chaste expects.

{{< /callout >}}

### Building and running

Configure a fresh build folder with gperftools profiling enabled:

```sh
cmake -DChaste_PROFILE_GPERFTOOLS=ON /path/to/Chaste
```

Enabling profiling automatically selects a suitable build type, so there is no
need to set `CMAKE_BUILD_TYPE` yourself. Then build and run the profiled tests
with:

```sh
make -j4 profile
```

This builds every test in the `Profile` test pack, runs each one with the CPU
profiler attached, and post-processes the results. If you would rather run the
profiled tests in parallel, configure with e.g.
`-DChaste_PROFILE_GPERFTOOLS_CPUS=4` instead (but note that timings are most
reliable when tests run one at a time).

### The output

Results appear in the `profile` sub-folder of your build folder:

- `<TestName>.txt`: a flat text report, with the functions taking the most time
  at the top;
- `<TestName>.svg`: a call graph, best viewed in a web browser — boxes are
  sized by the time spent in each function;
- `index.html`: an index page linking to the reports for every test;
- `<TestName>.prof`: the raw profile data.

The raw profile data can also be explored interactively — this is well worth
trying:

```sh
~/go/bin/pprof -http=:8080 /path/to/test_executable profile/<TestName>.prof
```

which opens a browser interface with flame graphs, source-line annotations and
more.

## Profiling with gprof

{{< callout context="caution" title="Caution" icon="outline/alert-triangle" >}}

gprof output is unlikely to be very helpful for typical Chaste simulations: it
only attributes time to code compiled with instrumentation, so time spent in
external libraries such as PETSc or Boost is poorly accounted for, and the flat
text output is much harder to interpret than a call graph. Prefer gperftools
unless you have a specific reason to use gprof.

{{< /callout >}}

gprof needs no extra dependencies (it is part of `binutils`, installed on any
system that can build Chaste). Configure a fresh build folder with:

```sh
cmake -DChaste_PROFILE_GPROF=ON /path/to/Chaste
```

then, as for gperftools:

```sh
make -j4 profile
```

Results again appear in the `profile` sub-folder, as a `<TestName>.txt` report
per test plus an `index.html` index page.

## Profiling on continuous integration

The `Profile` test pack is run regularly on GitHub Actions to track Chaste's
performance over time; see the
[testing strategy](../chaste-strategies/testing-strategy) for the published
results.
