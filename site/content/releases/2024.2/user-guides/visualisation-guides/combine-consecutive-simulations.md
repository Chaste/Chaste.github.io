---
title: "Combining consecutive cell-based simulations"
description: "Combining consecutive cell-based simulations"
draft: false
images: []
toc: true
layout: "single"
version: "2024.2"
---

Multiple calls to `AbstractCellSimulation::Solve` produce a collection of files
named `results_from_time_T` where `T` is the start time of the simulation. These
results may be combined for easier analysis or visualisation in ParaView using a
simple script in the `anim` folder of the `develop` branch of Chaste.

```sh
ctest -j4 -V -R TestOffLatticeSimulation.hpp
python anim/notforrelease/MergeCellBasedResults.py $CHASTE_TEST_DIRECTORY/TestOffLatticeSimulationWithMultipleCellKillers
```

This will combine the result in the files `results_from_time_0` and
`results_from_time_0.5` into a single set of results in `merged_results`

The script depends on the following python packages: `glob`, `shutil`, `os` and `sys`.
