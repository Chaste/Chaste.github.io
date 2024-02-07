---
title: "C++ Naming Strategy"
description: "C++ Naming Strategy"
draft: false
images: []
toc: true
layout: "single"
---

## Introduction

Coding standards are crucial to enable humans to understand the code -- Both 
code they wrote, and code written by other developers. This page documents 
naming conventions we adhere to in Chaste. If you are writing Chaste code, 
please follow them!

{{< callout context="tip" title="See Also" icon="rocket" >}}
* [Code Structure Strategy](../code-structure-strategy)
* [Distributed and Replicated Vectors](../distributed-and-replicated-vectors)
* [How Not to Write FORTRAN in Any Language](http://queue.acm.org/detail.cfm?id=1039535)
{{< /callout >}}

## Choosing names

Names are the key to program readability. If the name is appropriate everything 
fits together naturally, relationships are clear, meaning is derivable, and 
reasoning from common human expectations works as expected. Good names save 
time when debugging and save time when extending.

"Good" naming includes not using names which might be ambiguous in a 
particular situation:

```c++
// Does "complex" mean "complicated" 
// or "involving imaginary numbers"?
Problem complex_problem;

// Is this the solution of an electrical current 
// or the solution to the voltage/whatever *now*?
Vec mCurrentSolution; 

// Dangerous in situations where several objects are 
// indexed or there are global/local indices.
unsigned index;  
```

If you find all your names could be `Thing` and `DoIt` then you should 
probably revisit your design. Avoid the temptation to have short names 
everywhere, and avoid non-standard abbreviations.

**Source code is meant to be read by humans.** This is the most important 
thing to remember. As well as communicating your intent to the machine, 
you must make it clear what that intent is to those who will read the 
source code. This includes you! Code you've written more than about 3 
weeks ago may as well have been written by somebody else.

A cryptic example:

```c++
Dog d;
Lion l;
l.dvr(d);

```

A more descriptive version:

```c++
Dog my_pet_dog;
Lion escaped_lion;
escaped_lion.Devour(my_pet_dog);
```

## Class Names

Name the class after what it is. If you can't think of what it is that is 
a clue you have not thought through the design well enough.

* Use upper case letters as word separators, lower case for the rest of a word
* First character in a name must be upper case
* No underscores (`_`) are permitted

```c++
class OdeSolver
class ParameterFile
```

## Method and Function Names

Usually every method and function performs an action, so the name should 
make clear what it does: `CheckForErrors()` instead of `ErrorCheck()`, 
`DumpDataToFile()` instead of `DataFile()`. This will also make functions 
and data objects more distinguishable. Each method/function should begin 
with a verb.

* Classes are often nouns. By making function names verbs and following 
  other naming conventions programs can be read more naturally.

* Suffixes are sometimes useful:
    * `Max` - to mean the maximum value something can have.
    * `Count` - the current count of a running count variable.
    * `Key` - key value.

   For example: `RetryMax` to mean the maximum number of retries, 
   `RetryCount` to mean the current retry count.

* Prefixes are sometimes useful:
    * `Is/Has` - to ask a question about something. Whenever someone 
      sees `Is` or `Has` they will know it's a question.
    * `Get` - get a value.
    * `Set` - set a value.

   For example:

  ```c++
  if (HasHitRetryLimit())
  {
    // try something else
  }
  ```

* Use the same naming rules as for class names:

  ```c++
  class OdeSolver
  {
  public:
    int SolveEquation();
    void HandleError();
  }
  ```

## No All Upper Case Abbreviations

When confronted with a situation where you could use an all upper case 
abbreviation instead use an initial upper case letter followed by all 
lower case letters. No matter what.

Take for example

```c++
NetworkABCKey
```

Notice how the C from ABC and K from key are confused.

```c++
class FluidOz;       // NOT FluidOZ
class NetworkAbcKey; // NOT NetworkABCKey
```

## Pointer Variables

Pointers should be prepended by a `p` in most cases. Place the * close to 
the pointer type rather than the variable name.  Only one pointer type 
should be declared per line (with no non-pointer types) in order to avoid 
confusion. We generally only declare one variable per line.

```c++
Car my_car;
Car* p_your_car = new Car;

// NOT:
Car *p_your_car;

// AND NOT:
Car* p_your_car, p_my_car;
// since only p_your_car is a pointer here. 
// We declare only one pointer type at a time.
```

## Class Attribute Names

* Private attribute names should be prepended with the underscore character `m`.
* After the `m` use the same rules as for class names.
* `m` always precedes other name modifiers like `p` for pointer.

```c++
class CleaningDepartment
{
public:
  int ComputeErrorNumber();
private:
  int mCleanHouse;
  int mErrorNumber;
  String* mpName;
}
```

## Reference Variables and Functions Returning References

References should be prepended with `r`. This applies to input arguments 
as well as method names, and establishes the difference between a method 
returning by value and a method returning by reference.

```c++
class Test
{
public:
  void TestConveyorStart(StatusInfo& rStatus);

  // returns by reference so requires the `r` prefix
  StatusInfo& rGetStatus();

  // returns by value so doesn't have the `r` prefix
  StatusInfo GetStatus();

private:
  StatusInfo& mrStatus;
}
```

## Method Argument Names

The first character should be lower case. All word beginnings after the 
first letter should be upper case as with class names.

```c++
class WackyRace
{
public:
  int StartYourEngines(Engine& rSomeEngine, Engine anotherEngine);
}
```

## Variable Names on the Stack

When variables are created in a C++ program (when the variables are in scope) 
the memory required to hold the variable is allocated from the program stack, 
and when the variable goes out of scope, the memory which was taken on 
the stack is freed. When memory is allocated dynamically (by the 
programmer -- using the new keyword), or if variables are declared as 
class attributes memory is taken from the heap.

* Use all lower case letters
* Use `_` as the word separator.

With this approach the scope of the variable is clear in the code. And 
now all variables look different and are identifiable in the code.

```c++
int ProcessMonitor::HandleError(int errorNumber)
{
  int error = OsErr();
  Time time_of_error;
  ErrorProcessor error_processor;
}
```

## Global Constants

Global constants should be all caps with `_` separators.

```c++
const double TWO_PI = 6.28318531;
```

## Static Variables

Static variables should be prepended with `s`.

```c++
private:
  static StatusInfo msStatus;
```

<!--(The attached PDF document is the original of the above.)-->
