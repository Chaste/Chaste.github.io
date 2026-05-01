---
title: "Code Structure Strategy"
description: "Code Structure Strategy"
draft: false
images: []
toc: true
layout: "single"
version: "2026.1"
---

## Introduction

Coding standards are crucial to enable humans understand the code. Both code 
they wrote, and code written by other developers. This page documents 
code standards we adhere to in Chaste. If you are writing Chaste code, 
please follow them!

{{< callout context="tip" title="See Also" icon="outline/rocket" >}}
* [Coding Standards Strategy](../coding-standards-strategy)
* [Distributed and Replicated Vectors](../distributed-and-replicated-vectors)
* [How Not to Write FORTRAN in Any Language](http://queue.acm.org/detail.cfm?id=1039535)
{{< /callout >}}

## What to put in *.hpp* and *.cpp* files

A normal class should be declared in a `.hpp` file and implemented 
separately in a `.cpp` file. For example, the definition of `MyClass` 
in `MyClass.hpp` would look like:

```c++
class MyClass
{
private:
   int mVariable; // a member variable
public:
   MyClass(int i); // a constructor
}
```

and the implementation in `MyClass.cpp` would look like:

```c++
#include "MyClass.hpp"

MyClass::MyClass(int) : mVariable(i)
{
  // Do something here
}
```

Where possible, a templated class should also be defined in a `.hpp` file 
and implemented in a `.cpp` file, using explicit instantiation (see below). 
If this is not possible, then the class should be defined at the top of 
the `.hpp` file and implemented separately underneath, to avoid implicitly 
inlining methods where this is not appropriate, and to ease reading of the 
code (a method defined within a class declaration is implicitly marked 
as inline, although a compiler may choose to ignore this suggestion if 
it considers the method to be too large.)

## Policy on includes

Good use of the `#include` statement helps to keep code tidy, and results 
in shorter compilation times as a bonus.

 1. As a general rule of thumb, if a `.cpp` file (say `A.cpp`) makes use of 
 a class (say `B`), it should `#include` the header (`B.hpp`) for that class.

 2. One exception to this is if the class is also used in `A.hpp` (because 
 `B` is the base class of `A`, or `B` is used as an argument for one of 
 `A`'s methods). In that case the `#include` should appear in `A.hpp` and 
 may be omitted from `A.cpp`.

 3. Header files should not contain any `#include`s apart from those cases 
 indicated in the previous point. Really.  It may seem more convenient, but 
 it just makes life difficult later on (We've been bitten by this several times).

 4. Older versions of `g++` aren't very picky about whether you need to include 
 standard library headers (e.g. `<cstring>`). You should still try to remember 
 to include them, as otherwise your code won't compile on newer versions.

 5. You should include the C++ versions of C standard library headers, 
 e.g. `<ctime>` rather than `<time.h>`.

Point 2 can even be expanded upon.  Often you might not need to include 
`B.hpp` in `A.hpp`, even in the cases mentioned there -- instead just using 
a forward declaration of `B`: "`class B;`". In this case `A.cpp` will need 
to `#include` `B.hpp`. This technique is useful for breaking circular 
include chains, and this is currently the only situation in which we use it, 
as widespread use would mean many more `#include` lines. We may revisit 
this decision, as it can reduce compilation time.

Some includes, particularly of the Boost Ublas and Serialization libraries, 
also need to be given in a particular order. Generally Ublas headers 
(`#include "UblasIncludes.hpp"` or `#include "UblasCustomFunctions.hpp"`) 
should come first -- in particular they must appear before any PETSc headers 
(or some PETSc/Boost version combinations might break e.g. PETSc 2.2/Boost 1.33.1).

{{< callout context="tip" title="See Also" icon="outline/rocket" >}}
* [Boost Serialization](../../../user-guides/boost-serialization) for details on the archiving headers.
* [Include What You Use](https://code.google.com/p/include-what-you-use/wiki/WhyIWYU) for more about this kind of includes policy.
{{< /callout >}}

## Explicit instantiation for templated classes

We use explicit instantiation for templated classes wherever possible. 
For example, if `MyClass` is templated over spatial dimension:

```c++
template<unsigned DIM>
class MyClass
{
private:
   int mVariable; // a member variable
public:
   MyClass(int i); // a constructor
}
```

then in the `.cpp` file, we define the methods for all spatial dimensions expected:

```c++
#include "MyClass.hpp"

template<unsigned DIM>
MyClass<DIM>::MyClass(int) : mVariable(i)
{
  // Do something here
}

template class MyClass<1>;
template class MyClass<2>;
template class MyClass<3>;
```

## C++ initialisers

We use C++ initialisers to initialise member variables. This is because when 
a class is instantiated, all member variables are initialised before the 
constructor is called. If they aren't initialised by the initialiser list, 
they are given default values. For things like `int`s this isn't much of a 
problem, but for objects it then requires the corresponding class to have 
a default constructor, and you get the unnecessary overhead of creating an 
instance of the class twice.

As an example, we prefer this:

```c++
MyClass(int i) : mVariable(i)
{
  // Do something
}
```

to this

```c++
MyClass(int i)
{
  mVariable = i;
  // Do something
}
```

## Where to put common code that is used just for tests

If classes are only used by a single test file, they should remain in that 
test file. However, if multiple test files have very similar helper classes, 
then we should refactor the commonality into a class in a shared file. 
For tests only used by one component, this file can be located in the 
`tests` folder. If the code is of use to tests of multiple components, 
then a suitable location is within the `fortests` folder in the `src` folder.

## Documenting the code with Doxygen

We use the doxygen package to automatically generate HTML documentation 
from comments in the Chaste code. More information on doxygen commands 
can be found in the [doxygen manual](https://www.doxygen.nl/manual/commands.html). 

We document each class, as well as each member and method in that class, 
by adding a doxygen code block of the form:

```c++
/**
* This is a doxygen code block
*/
```

just before the code being documented (we tend to place all such documentation 
in the header file where the class is defined, although this doesn't matter). 
To document inputs and outputs to a particular method, we use the 
commands `@param` and `@return`, as shown by the following example 
from `AbstractElement.hpp`:

```c++
/**
* Get the node with a given local index in this element.
*
* @param localIndex local index of the node in this element
* @return a pointer to the node.
*/
Node<SPACE_DIM>* GetNode(unsigned localIndex) const;
```

In addition to the standard doxygen commands, we have added the ability to 
completely ignore auto-generated files (for example, those such 
as `BackwardEulerFoxModel2002Modified.hpp` that are processed by chaste_codegen). 
Such files should include the doxygen block

```c++
/** @autogenerated */
```

## Excluding lines from coverage testing

{{< callout context="caution" title="Caution" icon="outline/alert-triangle" >}}
Generally to be avoided. If at all possible, write a test to cover each 
line of code!
{{< /callout >}}

If you really need to exclude some code from coverage you can use special 
comments provided by [lcov](https://github.com/linux-test-project/lcov) settings:

```c++
// LCOV_EXCL_LINE
```

for a single line of code, or

```c++
// LCOV_EXCL_START
<uncovered code>
// LCOV_EXCL_STOP
```
for a block of code. For instance:

```c++
std::string GetCurrentWorkingDirectory()
{
  fs::path cwd;
  try
  {
    cwd = fs::current_path();
  }
// LCOV_EXCL_START
  catch (...)
  {
    // Not sure what could cause this, so not covered, but just in case...
    EXCEPTION("Unable to determine current working directory");
  }
// LCOV_EXCL_STOP
  return cwd.string();
}
```

A common use-case of this is a hard-exit which indicates an error 
(likely in programming rather than usage), which we indicate with 
`NEVER_REACHED` as per [Exception Strategy](../exception-strategy) -- this 
line is automatically excluded from coverage testing.

## Other Conventions

If no advice is offered on the [Chaste Strategies](../) pages, we informally 
follow many/most of the [Joint Strike Fighter C++ coding standards](https://www.stroustrup.com/JSF-AV-rules.pdf).
