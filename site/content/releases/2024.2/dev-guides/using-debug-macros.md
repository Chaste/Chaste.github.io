---
title: "Using Debug Macros"
description: "Using Debug Macros"
draft: false
images: []
toc: true
layout: "single"
version: "2024.2"
---

If you are having trouble and want to debug without writing

```c++
std::cout << "blah" << std::endl << std::flush;
```

(etc) there is a handy helper macro list in
[`global/src/Debug.hpp`](https://github.com/Chaste/Chaste/blob/develop/global/src/Debug.hpp).

## Trace

For the above example

```c++
TRACE("Some trace");
```

prints this to the screen:

```
DEBUG: Some trace
```

## Printing variables

```c++
PRINT_VARIABLE(my_var);
PRINT_2_VARIABLES(my_var, another_var);
PRINT_3_VARIABLES(my_var, another_var, cancer_curing_constant);
PRINT_4_VARIABLES(my_var, another_var, cancer_curing_constant, heart_disease_ending_constant);
PRINT_VECTOR(vector); // std::vector of anything
```

will result in the following output

```
DEBUG: my_var = 3141
DEBUG: my_var = 3141, another_var = 2.81
DEBUG: my_var = 3141, another_var = 2.81, cancer_curing_constant = 0.0534502
DEBUG: my_var = 3141, another_var = 2.81, cancer_curing_constant = 0.0534502, heart_disease_ending_constant = -3e-141
DEBUG: vector = {0,1,2.7,3.1}
```

## Determining if lines are reached

```c++
MARK;
```

will do something like

```
DEBUG: ./global/test/TestDebug.hpp at line 95
```

and

```c++
for (unsigned i=0; i<3; i++)
{
   HOW_MANY_TIMES_HERE("my line");
}
```

outputs

```
DEBUG: Num times here (my line): 1
DEBUG: Num times here (my line): 2
DEBUG: Num times here (my line): 3
```

and

```c++
for (unsigned j=0; j<3; j++)
{
  TRACE_FROM_NTH_VISIT("hello",2);
}
```

will output

```
DEBUG: hello (visit 2)
DEBUG: hello (visit 3)
```

and finally,

```c++
QUIT_AFTER_N_VISITS(11);
```

will quit (`assert(0)`, with "User-forced quit." output), the 11th time that line is visited.
