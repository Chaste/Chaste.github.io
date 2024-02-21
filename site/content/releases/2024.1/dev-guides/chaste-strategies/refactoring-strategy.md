---
title: "Refactoring Strategy"
description: "Refactoring Strategy"
draft: false
images: []
toc: true
layout: "single"
version: "2024.1"
---

## Problem
The code base can contain duplication, commented out code, and 
generally [smell](http://c2.com/cgi/wiki?CodeSmell).
We use [Test Driven Development](http://c2.com/cgi/wiki?TestDrivenDevelopment) 
and the solution to this is to refactor -- *but when?*

## Solution
At all times developers should be on the look out for smelly code where 
refactoring could be applied. When such code is found, the developer is 
obliged to either:

* Refactor the code there and then -- this may be too restrictive because it 
upsets the developer's flow.
* Open a [GitHub issue](https://github.com/Chaste/Chaste/issues) for the 
refactoring work -- this approach is desirable.

