---
title: "Best Practices for Chaste Developers"
description: "Best Practices for Chaste Developers"
draft: false
images: []
toc: true
layout: "single"
---

This page enumerates some best practices that have developed over the lifetime
of Chaste, and help to make all developers' lives happier. They are similar to
[Chaste Strategies](../chaste-strategies), but less formal.

## Writing new code

Much information on coding style can be found in the
[Chaste Strategies](../chaste-strategies), in particular
[Coding Standards Strategy](../chaste-strategies/coding-standards-strategy) and
[Code Structure Strategy](../chaste-strategies/code-structure-strategy).

Two important features of Chaste code is that it should be **(i) well
documented** and **(ii) [well tested](#writing-tests)**. We use
[Doxygen](https://www.doxygen.nl/) to generate
[hyperlinked documentation for Chaste](../../doxygen) automatically. Remember to
add Doxygen comments to all your member variables and methods, and make them as
informative as possible without being overly verbose. The
[Doxygen manual](https://www.doxygen.nl/manual/) is a helpful resource for
syntax, in particular the
[list of special commands](https://www.doxygen.nl/manual/commands.html). When
documenting a whole class, try to give some higher level information on how the
class can be useful. Consider whether a [tutorial](#writing-tutorials) might also
be helpful.

The [`Doxygen`](https://github.com/Chaste/Chaste/actions/workflows/doxygen.yml)
automatated test will show up any missing documentation or incorrect syntax.

## Writing tests

All functionality in Chaste must be tested. Writing good tests is an art, but
well worth practising. A test suite will generally consist of many small unit
tests that check specific methods, rather than one huge test.

One point to note is that tests shouldn't just cover the trivial case. Try to
consider what 'corner' or 'edge' cases might arise, and check for those. If a
numerical algorithm should have particular error or convergence properties,
check this. You should also test that code throws appropriate exceptions for
error conditions.

Make sure that `Continuous` tests are as short as possible, since these are run
frequently. Longer tests, when required, should go in the `Nightly` or `Weekly`
test packs.

Tests must cover every line of Chaste source code wherever possible. This is
checked by the
[`Coverage`](https://github.com/Chaste/Chaste/actions/workflows/coverage.yml)
automated test.

{{< callout context="tip" title="See Also" icon="rocket" >}}
[Testing Strategy](../chaste-strategies/testing-strategy)
{{< /callout >}}

## Not annoying your fellow developers

Chaste is developed collaboratively. However, due to the nature of academic
life, not all development on the Chaste trunk occurs in iterations, and so there
are occasions when you may have to commit to trunk individually. When you do so,
it is still important to consider your fellow developers. For example,

- When you have pushed commits to a pull request, check the automated
  [test results](https://github.com/Chaste/Chaste/actions) to see if you broke
  any of the tests.
- Try not to commit major changes late on Friday afternoon or before going on
  holiday, just in case something breaks. Note that even if `Continuous` tests
  pass, there could be errors that only appear in other tests that take longer
  to run.
- Of course, before making massive changes it's good to consult with other
  Chaste developers to get a second opinion!
- The automated tests will send an email if a commit breaks the build or any
  tests. Please respond to these promptly.
  <!--; see ChasteGuides/AutomatedBuildGuide for more information on the kinds of problems that arise and how to fix them. -->

## Keeping up with what's happening

The [Changes Since Last Release](../../release-notes/changes-since-last-release/)
page is used to update other developers on changes that might affect their work
-- for example, changes to an interface that mean user projects would have to be
modified to match, or the addition of useful new functionality. This helps those
who don't have time to view every commit made. Please keep it up-to-date, and
keep track of changes.

Significant changes that should be highlighted will be copied across to
[Release Notes](../../release-notes/release-notes) at the time of release so
please structure your changes in the same manner.

## Writing tutorials

Tutorials are special tests designed to help new developers get familiar with
the code. They therefore need special care when being written!

- Tutorials are tests with a name of the form "`TestWhateverTutorial.hpp`"
- As well as being compiled and run automatically as for normal tests, these are
  processed by a script and uploaded to the website under
  [User Tutorials](../../../docs/user-tutorials/), with a page name derived from
  the file name.
- Since new users will typically work their way through several tutorials in
  sequence, they should be written with this in mind. When adding a new
  tutorial, edit the [User Tutorials](../../../docs/user-tutorials/) page to
  link to it at an appropriate location. Also, don't copy'n'paste content from
  other tutorials that users are likely to have already read.
