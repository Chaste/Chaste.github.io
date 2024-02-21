---
title: "Distributed and Replicated Vectors"
description: "Distributed and Replicated Vectors"
draft: false
images: []
toc: true
layout: "single"
version: "2024.1"
version: "2024.1"
---

## Naming conventions for parallel data structures
If a local data structure is a part of larger global data structure there 
will be a mapping between the local and global indices. 
It's important to distinguish between the two, especially as in some 
loops (e.g. when replicating data), both indicies will need to be used.

{{< callout context="note" title="Verdict" icon="info-circle" >}}
Either local or global indices can be used. 
They must be named as such. 
If a loop body needs to refer to both global/local values, then a second 
variable ought to be declared. 
<!--This is evident in source:trunk/coupled/src/problem/cardiac/MonodomainPde.hpp!-->
{{< /callout >}}

## Naming conventions for VecGetArray

When PETSc vectors are read or written on a local process then the PETSc 
library uses [`VecGetArray`](https://petsc.org/main/manualpages/Vec/VecGetArray/) 
to provide a pointer to the actual storage.

Here is an example of non-intuitive names:

```c++
int lo, hi, size;
VecGetOwnershipRange(currentSolution, &lo, &hi);
VecGetSize(currentSolution, &size);

double current_solution[size], current_solution_replicated[size];
double *answer_elements;
VecGetArray(currentSolution, &answer_elements);
```

It will not be obvious later on that `currentSolution` and `answer_elements` 
are storing the same data.

{{< callout context="note" title="Verdict" icon="info-circle" >}}
All pointers that are used in calls to [`VecGetArray`](https://petsc.org/main/manualpages/Vec/VecGetArray/) 
ought to have the prefix `p` (for pointer). 
This will distinguish them from locally declared arrays also. 
Their root name ought to be the same as the original [`Vec`](https://petsc.org/main/manualpages/Vec/Vec/) 
(but change camel-case to lower case when the original `Vec` was an argument to 
the function call). Locally declared arrays should have the suffix `_array`. 
{{< /callout >}}

The above code becomes:

```c++
int lo, hi, size;
VecGetOwnershipRange(currentSolution, &lo, &hi);
VecGetSize(currentSolution, &size);

double current_solution_array[size], current_solution_array_replicated[size];
double *p_current_solution;
VecGetArray(currentSolution, &p_current_solution);
```

## Naming conventions for std::vectors

On most occasions where extensible `std::vector`s are used, then they hold 
information that is local to the process. However, there are occasions 
where `std::vector`s are distributed (ie. one process holds only the information 
that corresponds to the nodes which it owns, and no process knows the 
entire picture) or where `std::vector`s are replicated (ie. because processes 
need to share some information about from node neighbours they pool the 
information at each time-step).

Here's an example<!-- from source:trunk/coupled/src/common/AbstractCoupledPde.hpp-->. 
It's important here that the state variables of each ODE system are distributed 
(since most of the parallel speed-up comes from distributing the ODE solutions). 
However, the voltage solutions from one time step are used in the next, and 
it's possible that the voltage from a node which is nearby in the mesh may 
be on a remote process. Thus the voltages are replicated on all processes 
before they are needed.

```c++
  /** mOdeVarsAtNode[i] is a vector of the current values of the
  *  voltage, gating variables, intracellular Calcium concentration at node
  *  i. The voltage returned by the ode solver is not used later since the pde
  *  solves for the voltage.
  *
  * This is distributed, i.e. i should be a local index.
  */
  std::vector<odeVariablesType> mOdeVarsAtNode;

public:
  /** solutionCache stores the solutions to the ODEs (Icurrent) for
  *  each node in the global system.
  *
  * This is replicated, i.e. use a global index for access.
  */
  std::vector<double> solutionCacheReplicated;
```

{{< callout context="note" title="Verdict" icon="info-circle" >}}
By default, `std::vector`s are local. When they are replicated or 
distributed then they ought to have a name which reflects that fact. 
Following the patterns in the verdicts above, the following suffices: 
`_distributed` and `_replicated` (`Replicated` if the base is in camel case) should be used.
{{< /callout >}}
