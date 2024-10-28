---
title: "Notes on Fixing Memory Leaks"
description: "Notes on Fixing Memory Leaks"
draft: false
images: []
toc: true
layout: "single"
version: "2024.2"
---

This page lists some of the common sources of memory leaks and how to fix them
-- this is a work in progress.

- Check that you've deleted the pointer to a cell killer at the end of a test,
  if you've created one.<!-- (see e.g. `TestTissueSimulationWithNutrients`).-->

- You may need to delete the tissue created by a serializer.
 <!--(see e.g. `TestMeineke2001SpringSystem`) -->

- Check that `SimulationTime` has been properly initialised -- you may need to
  call `SetEndTimeAndNumberOfTimeSteps`

- Archiving -- if you're serialising a vector, check that you have put data in it.
  <!--(see e.g. `TestCellwiseData`) -->

- PETSc memory leak: you may need to free memory by calling [`VecDestroy`](https://petsc.org/release/manualpages/Vec/VecDestroy/).
