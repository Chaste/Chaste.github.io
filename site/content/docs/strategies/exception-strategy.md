---
title: "Exception Strategy"
description: "Exception Strategy"
draft: false
images: []
toc: true
layout: "single"
---

Exceptions will not be affected by the NDEBUG flag (in contrast to asserts, which are turned off if it is defined).
Defining NDEBUG speeds up ublas, so is turned on for the weekly builds, and will likely be turned on for production builds as well.

Exceptions should be used where they might be caused by Chaste user error, so the user gets an error they can handle programmatically.

Asserts should be used for situations that should never occur despite what a library user does. Other than that, when to use an assert is to be taken on a case-by-case basis.

These are the levels of errors available:

 Level 0::
   **No error.**
   An error which can be fixed without informing the user. (e.g. the user calls a method with `x_min` and `x_max` switched -- there may be a case for switching them back without giving any output).
 Level 1::
   **Warning.**
   An error which can be fixed, but requires notification back to the user. (e.g. a solver has stagnated and has been restarted or some node positions have been perturbed).  See source:trunk/global/src/Warnings.hpp
 Level 2::
   **Exception.**
   An error which could arise in normal use and might be fixed by a higher level process or by the user. (e.g. EXCEPTION("Element's Jacobian determinant is negative.") -- the element's nodes may have swapped order in a topological edit.)  See source:trunk/global/src/Exception.hpp
 Level 3::
   **Assertion.**
   An error which should not happen under normal computing circumstances and cannot be fixed.  This is used for safety in testing code (in order to check that the preconditions of a method are satisfied at runtime).  Note that in production code (NDEBUG), assertions are no-longer checked.  This means that level 3 errors *silently become level 0 errors*. (e.g. 
```
assert(SPACE_DIM >= 2)
```
.)  Note that `EXCEPT_IF_NOT` can be used in the same way as `assert`, but is not turned off in `NDEBUG` builds.
 Level 4::
   **Termination.**
   (See #1486 for justification of including a hard assertion.)
   As assertion: an error which should not happen under normal computing circumstances and cannot be fixed.  However, this is used when production code may enter state space that is unexplored by all normal tests and where not checking the condition would cause a catastrophic error such as non-termination (e.g. `NEVER_REACHED`, `TERMINATE` or `ABORT_IF_NON0(system_command)`).
