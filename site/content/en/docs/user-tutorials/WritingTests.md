
---
title : "TestWritingTestsTutorial.hpp"
description: "This tutorial is automatically generated from the file global/test/TestWritingTestsTutorial.hpp at revision [1288aa7fe4cc](https://github.com/Chaste/Chaste/commit/1288aa7fe4ccb5438b05f81253fe167e350cdc10). Note that the code is given in full at the bottom of the page."
draft: false
images: []
toc: true
---

# Writing tests 
We do not use `int main()` methods in Chaste. Instead, we write ''tests'', which are run using !CxxTest.
Tests are used both as:
(i) part of the testing environment - every class in the source code has an equivalent test file which tests each aspect of its functionality, making use of the `TS_ASSERT`s as described below; and
(ii) for experimental work, which involve writing a 'test' as below but generally without `TS_ASSERT`s.

This tutorial shows how to write a test using !CxxTest. Note that the full code is given at the bottom of the page.

First, the following header file needs to be included.
```cpp
#include <cxxtest/TestSuite.h>

```
Now we have to define a class containing the tests. It is sensible to name the class with the same name as the file name. The class should inherit from `CxxTest::TestSuite`{.cpp}.

```cpp
class TestWritingTestsTutorial: public CxxTest::TestSuite
{
```

Now we define some tests, which must be '''public''', begin with the word 'Test', return `void`{.cpp}, and take in no parameters.

```cpp
public:
    void TestOnePlusOneEqualsTwo()
    {
```

To test whether two integers are equal, we can use the macro `TS_ASSERT_EQUALS`{.cpp}.

```cpp
        int some_number = 1 + 1;
        TS_ASSERT_EQUALS(some_number, 2);
```

To test whether two numbers are equal to within a certain (absolute) tolerance we can use `TS_ASSERT_DELTA`{.cpp}.
This should almost always be used when comparing two `double`{.cpp}s.  (See also class:CompareDoubles for more
advanced comparisons.)

```cpp
        double another_number = 1.000001 + 1.0001;
        TS_ASSERT_DELTA(another_number, 2.0, 1e-2);
    }
```

This second test shows some of the other `TS_ASSERT`{.cpp} macros that are available.
The {{{}} part of the signature is there to make sure that full details of any
uncaught exceptions are reported.

```cpp
    void TestSomeOtherStuff()
    {
        TS_ASSERT(1==1); // however, it is better to use TS_ASSERT_EQUALS, below
        TS_ASSERT_EQUALS((true||false), true);
        TS_ASSERT_DIFFERS(1.348329534564385643543957436, 1.348329534564395643543957436);
        TS_ASSERT_LESS_THAN(2.71828183, 3.14159265); // Note: to test if x is greater than y, use TS_ASSERT_LESS_THAN(y,x)
        TS_ASSERT_LESS_THAN_EQUALS(-1e100, 1e100);
        TS_ASSERT_THROWS_ANYTHING(throw 0;); // normally you would put a function call inside the brackets

        unsigned x;
        // The following TS_ASSERT_THROWS_NOTHING may be useful if you want to be certain that there are no uncaught exceptions
        TS_ASSERT_THROWS_NOTHING(x=1;);  // normally you would put a function call inside the brackets
        TS_ASSERT_EQUALS(x, 1u); //Note that x and 1u are of the same type: unsigned integer
    }

```
Other useful macros include `TS_ASSERT_THROWS_THIS` and `TS_ASSERT_THROWS_CONTAINS` for testing exception
messages.

Note that methods that don't start with 'Test' are compiled but not run. So, if you want to stop a single
test running, just put an 'x' or a 'donot' (for instance) before its name.

```cpp
    void donotTestThis()
    {
        TS_ASSERT_EQUALS(1,   2);
        TS_ASSERT_EQUALS(1u,  2u);
        TS_ASSERT_EQUALS(1.0, 2.0);
    }
};
```

To run this code, first copy it into a file, say, called `TestWritingTests.hpp` in the directory `global/test/`.
Second, add the full name of your new file to the relevant continuous test pack, say `[path/to/Chaste]/global/test/ContinuousTestPack.txt`.
Third, from the command line, run
{{{
#!sh
cd [path/to/ChasteBuild]
ccmake [path/to/Chaste]
}}}
Then press `c` to configure, `e` to exit, and `g` to generate. Finally, run
{{{
#!sh
make global
ctest -V -R TestWritingTests
}}}



# Code
The full code is given below


## File name `TestWritingTestsTutorial.hpp` 

```cpp
#include <cxxtest/TestSuite.h>

class TestWritingTestsTutorial: public CxxTest::TestSuite
{
public:
    void TestOnePlusOneEqualsTwo()
    {
        int some_number = 1 + 1;
        TS_ASSERT_EQUALS(some_number, 2);
        double another_number = 1.000001 + 1.0001;
        TS_ASSERT_DELTA(another_number, 2.0, 1e-2);
    }
    void TestSomeOtherStuff()
    {
        TS_ASSERT(1==1); // however, it is better to use TS_ASSERT_EQUALS, below
        TS_ASSERT_EQUALS((true||false), true);
        TS_ASSERT_DIFFERS(1.348329534564385643543957436, 1.348329534564395643543957436);
        TS_ASSERT_LESS_THAN(2.71828183, 3.14159265); // Note: to test if x is greater than y, use TS_ASSERT_LESS_THAN(y,x)
        TS_ASSERT_LESS_THAN_EQUALS(-1e100, 1e100);
        TS_ASSERT_THROWS_ANYTHING(throw 0;); // normally you would put a function call inside the brackets

        unsigned x;
        // The following TS_ASSERT_THROWS_NOTHING may be useful if you want to be certain that there are no uncaught exceptions
        TS_ASSERT_THROWS_NOTHING(x=1;);  // normally you would put a function call inside the brackets
        TS_ASSERT_EQUALS(x, 1u); //Note that x and 1u are of the same type: unsigned integer
    }

    void donotTestThis()
    {
        TS_ASSERT_EQUALS(1,   2);
        TS_ASSERT_EQUALS(1u,  2u);
        TS_ASSERT_EQUALS(1.0, 2.0);
    }
};
```

