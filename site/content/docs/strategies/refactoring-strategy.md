---
title: "Refactoring Strategy"
description: "Refactoring Strategy"
draft: false
images: []
toc: true
layout: "single"
---

Problem: The code base can contain duplication, commented out code, and generally [smell](http://c2.com/cgi/wiki?CodeSmell).
We are using Test driven development and the solution to this is to refactor. *But when?*

Solution: At all times developers should be on the look out for smelly code where refactoring could be applied. When such code is found,
the developer is obliged to either:

* Refactor the code there and then
* Raise a ticket for the refactoring work


Alternative Solutions: Insisting that one always refactors as soon as smelly code is found. This is too restrictive because it upsets the developer's flow. The option to raise a ticket is desirable.

