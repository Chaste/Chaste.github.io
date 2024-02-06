---
title: "Time Stepping Algorithms"
description:  "Time Stepping Algorithms"
draft: false
images: []
toc: true
layout: "single"
---

Many places in Chaste need to take discrete steps through time: the ODE and PDE solvers are prime examples!  We want to refactor common logic into a single location (TimeStepper class), and experiment with different ways to implement time stepping logic.  See also #313 #152.

It would be interesting to have a hierarchy of TimeStepper classes, with a singleton abstract factory implementation deciding which stepper was used for a given simulation (the advantage of making the factory a singleton is that it is easier to handle a default factory, without needing to pass around pointers to factories).  I think the stepper should encapsulate the printing/sampling logic as well.  The stepper (or a reference to it) can be passed around, rather than passing multiple doubles to methods that need to know about time.

Also have the stepper constructor call a CheckParameters private method, in case subclasses need to check such things as whether the time step divides the interval.

Note that the time stepper can't be a singleton, since we will need multiple steppers for coupled problems (eg one for PDE, one for ODEs).

For most steppers, we want to do 
```
currentTime = startTime + currentTimeStepNumber * dt
```
 to avoid a build-up of floating point errors.  However, it might be useful to also have a '`FastStepper`' which does 
```
currentTime += dt
```
 that could be used in places where we don't perform many timesteps, or where the current time is reset externally, such as in an ODE stepper controlled by a PDE stepper.  This may not have a noticeable impact on performance, but it'd be interesting to try :)
