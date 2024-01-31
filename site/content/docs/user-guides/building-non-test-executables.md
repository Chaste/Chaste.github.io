---
title: "Building Non-Test Executables"
description: "Building Non-Test Executables"
draft: false
images: []
toc: true
layout: "single"
---

Sometimes one wants to create an executable which is not a test. ie. has a main function.

For the spiral wave project, we created `SpiralWaveProject.cpp` with a main function in the root of the source tree and ran the following

```sh
cd chaste

mpicxx -isystem ../../../petsc-2.3.2-p4/include -isystem ../../../petsc-2.3.2-p4/bmake/linux-gnu-opt -isystem ../../../xsd-2.3.1-i686-linux-gnu/libxsd -O3 -I. -Icxxtest -Imodels/src -Imodels/src/crypt -Iglobal/src -Ilinalg/src -Ilinalg/src/common -Idealii/src -Idealii/src/problem -Idealii/src/solver -Idealii/src/common -Idealii/src/problem/cancer -Idealii/src/problem/elasticity -Idealii/src/solver/elasticity -Idealii/src/solver/common -Icoupled/src -Icoupled/src/problem -Icoupled/src/solver -Icoupled/src/common -Icoupled/src/problem/cancer -Icoupled/src/problem/elasticity -Icoupled/src/problem/cardiac -Icoupled/src/solver/cancer -Icoupled/src/solver/elasticity -Icoupled/src/solver/cardiac -Imesh/src -Imesh/src/reader -Imesh/src/writer -Imesh/src/common -Imesh/src/decimator -Iode/src -Iode/src/problem -Iode/src/solver -Iode/src/common -Iode/src/problem/cancer -Iode/src/problem/cardiac -Iio/src -Iio/src/reader -Iio/src/writer -Ipde/src -Ipde/src/problem -Ipde/src/solver -Ipde/src/common -Ipde/src/problem/elasticity -Ipde/src/problem/common -Ipde/src/solver/elasticity -Ipde/src/solver/common -c -o SpiralWaveProject.o SpiralWaveProject.cpp

mpicxx -o SpiralWaveProject SpiralWaveProject.o -Llinklib -L/home/chaste/petsc-2.3.2-p4/lib/linux-gnu-opt -L/home/chaste/petsc-2.3.2-p4/externalpackages/f2cblaslapack/linux-gnu -L/opt/intel/cc/9.1.039/lib -lcoupled -lpde -lode -lmesh -llinalg -lio -lglobal -lpetscts -lpetscsnes -lpetscksp -lpetscdm -lpetscmat -lpetscvec -lpetsc -lf2clapack -lf2cblas -lboost_serialization -lxerces-c
```

