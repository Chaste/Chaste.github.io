# Best practices for Chaste developers

This page enumerates some best practices that have developed over the lifetime of Chaste, and help to make all developers' lives happier.  They are similar to ChasteStrategies, but less formal.



## Writing new code

Much information on coding style can be found in the ChasteStrategies, in particular [CodingStandardsStrategy](https://github.com/Chaste/trac_archive/wiki/Coding-Standards-Strategy) and CodeStructureStrategy.

Two important features of Chaste code is that it should be **well documented** and **[well tested](#Writingtests)**.  We use [Doxygen](http://www.stack.nl/~dimitri/doxygen/) to generate [hyperlinked documentation for Chaste](//docs) automatically.  Remember to add Doxygen comments to all your member variables and methods, and make them as informative as possible without being overly verbose.  The [Doxygen manual](http://www.stack.nl/~dimitri/doxygen/manual.html) is a helpful resource for syntax, in particular the [list of special commands](http://www.stack.nl/~dimitri/doxygen/commands.html).  When documenting a whole class, try to give some higher level information on how the class can be useful.  Consider whether a [tutorial](#Writingtutorials) might also be helpful.

The `DoxygenCoverage` nightly build will show up any missing documentation or incorrect syntax; see ChasteGuides/AutomatedBuildGuide#Doxygencoverage for more information.

## Writing tests

All functionality in Chaste must be tested; see also the TestingStrategy.  Writing good tests is an art, but well worth practising.  A test suite will generally consist of many small unit tests that check specific methods, rather than one huge test.

One point to note is that tests shouldn't just cover the trivial case.  Try to consider what 'corner' or 'edge' cases might arise, and check for those.  If a numerical algorithm should have particular error or convergence properties, check this.  You should also test that code throws appropriate exceptions for error conditions.

Tests must cover every line of Chaste source code wherever possible.  This is checked by the `Coverage` nightly build - see ChasteGuides/AutomatedBuildGuide#Coverage.

Make sure that continuous tests are as short as possible, since these are run frequently, and will be killed if too long (see ChasteGuides/AutomatedBuildGuide#Testskilledoff).  Longer tests, when required, should go in the Nightly or Weekly test packs.

## Not annoying your fellow developers

Chaste is developed collaboratively.  However, due to the nature of academic life, not all development on the Chaste trunk occurs in iterations, and so there are occasions when you may have to commit to trunk individually.  When you do so, it is still important to consider your fellow developers.  For example,

* Run tests before committing to check you haven't broken anything.
* Try not to commit major changes late on Friday afternoon or before going on holiday, just in case something breaks.  Note that even if a default build passes, there could be other errors that only appear in a nightly or weekly build.
    * Of course, before making massive changes it's good to consult with other Chaste developers to get a second opinion!
* The automated continuous builds will send an email if a commit breaks the build or any tests.  Please respond to these promptly; see ChasteGuides/AutomatedBuildGuide for more information on the kinds of problems that arise and how to fix them.
* When you have committed to trunk, check the [nightly tests results](//tests.py/recent?type=nightly) each morning over the following week, especially the following day, to see if you broke any of these tests.  (Note that some nightly tests, in particular those on 'lofty' that check compatibility with different library versions, only run once per week with each configuration.)
    *  style=color: red;


## Keeping up with what's happening

The [LatestNews](https://github.com/Chaste/trac_archive/wiki/Latest-News) wiki page is used to update other developers on changes that might affect their work, for example changes to an interface that mean user projects would have to be modified to match, or the addition of useful new functionality.  This helps those who don't have time to view every commit made.  Please keep it up-to-date, and keep track of changes.

Also, significant changes that should be highlighted when the next release is made should be recorded in ReleaseNotes.  Note that you don't need to edit both [LatestNews](https://github.com/Chaste/trac_archive/wiki/Latest-News) and [ReleaseNotes](https://github.com/Chaste/trac_archive/wiki/Release-Notes) for minor changes; the content will be copied across when a release is made.

## Writing tutorials

Tutorials are special tests designed to help new developers get familiar with the code.  They therefore need special care when being written!


* Tutorials are tests with a name of the form "`TestWhateverTutorial.hpp`"
* As well as being compiled and run automatically as for normal tests, these are processed by a script and uploaded to the wiki under UserTutorials, with a page name derived from the file name.
* Since new users will typically work their way through several tutorials in sequence, they should be written with this in mind.  When adding a new tutorial, edit the [UserTutorials](https://github.com/Chaste/trac_archive/wiki/User-Tutorials) page to link to it at an appropriate location.  Also, don't copy'n'paste content from other tutorials that users are likely to have already read.
