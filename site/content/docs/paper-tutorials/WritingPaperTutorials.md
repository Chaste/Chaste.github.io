## Writing Paper Tutorials

The steps to create '[paper tutorial](https://github.com/Chaste/trac_archive/wiki/Paper-Tutorials)' wiki pages associated with a new or forthcoming publication are as follows.
For an example see the [source for the project Plos2013](/tags/Plos2013_release_3.1), which gets rendered as shown at [PaperTutorials/Plos2013](https://github.com/Chaste/trac_archive/wiki/Paper-Tutorials-_-Plos2013).


### Developing the project


* Create a new project for the paper, and move the appropriate source code and tests into the project.
* Create a file `Summary.wiki` in the top-level project directory and add an introduction to the project to this file, using [Trac wiki syntax](https://github.com/Chaste/trac_archive/wiki/Wiki-Formatting).
    * Include instructions on where to obtain the code.
    * Include a link to the paper, if available.
    * You can test out the syntax before committing by pretending to create a new wiki page, using 'Preview Page', but not actually submitting changes.
* For tests which you want to become tutorials, ensure they are named like `Test[Something]LiteratePaper.hpp`, and add [tutorial-style wiki comments](#Detailsofthetutorialfilesyntax).
    * For the benefit of science, it's a good idea if these tests check that the results match what you actually published (to within expected tolerances).
    * To see what the wiki text will look like (and check you won't get a parsing error on committing) run `./python/utils/CreateTutorial.py [input_file] -`
    * Commit and the wiki page will automatically be created or updated. (Note: if it doesn't appear, this is probably because `CreateTutorial.py` (see above) gave an error; check it locally and try again.)


#### Details of the tutorial file syntax

Briefly, any C-style comment (`/*` to `*/`) with no code on the same line gets converted into wiki text. See the code for [the main tutorials](https://github.com/Chaste/trac_archive/wiki/User-Tutorials) for examples.

For the definitive guide, see the [CreateTutorial.py script](/trunk/python/utils/CreateTutorial.py). The main features are:
 1. The script starts converting everything after the first `#define` line
 1. The script stops converting after then seeing an `#endif`. (If this isn't the last line then the script needs changing.)
 1. All C-style block comments '`/*`' to '`*/`' are converted to wiki text.
 1. All other lines, including C++ style comments '`//`', are kept as code lines
 1. To print an empty line in the wiki page, just leave a blank line between paragraphs in the comment, as for wiki pages.
 1. In C-style block comments (i.e. wiki text), initial and trailing whitespace is removed. Bulleted lists will work, but nested bulleted lists won't.
 1. Lines inside a block comment which start with a '`*`', i.e.

```cpp
     /* my comment is
      * two lines long */
```

   are ok, the initial '`*`' is removed.

The source code for the test is given in full (with wiki comments stripped) at the end of the page.
It is possible to specify additional files from your project which will also be listed, for instance configuration files or cell models used by the test.
To do so, you need a comment line (or multiple lines for multiple files) before the first `#define` which triggers wiki conversion, that looks like "`Requires: file_path`".
The `file_path` is relative to the folder the tutorial is in, *not* to your project.
See source:/tags/Wisc2013_release_3.2/test/TestCryptProliferationLiteratePaper.hpp?rev=22049#L36 for an example.

### Publishing

Once the paper is accepted, to publish the project:

* Make the wiki pages public, by requesting this of an admin (who will edit [/admin/accounts/pages]).
* Make the code and associated files available to view and/or download. Do one or both of the following (the first option below makes it easy to view code, the second easy to download, so it may be worth doing both):
    * Make the project public (ask an admin to do this). It is worth including a direct link to the project in the wiki pages for user convenience. This is a good option if you want users to see the history of the project.
    * Make a [tag of the project](https://github.com/Chaste/trac_archive/wiki/MakingARelease#Bolt-onprojects), tar and zip it and have it added as a bolt-on project to the [download](http://www.cs.ox.ac.uk/chaste/download.html) page. It's worth including links both to the downloads page and the Trac URL for your tag (e.g. source:tags/Plos2013_release_3.1) within the `Summary.wiki` page for your project, *before you tag*, to enable quick downloading and/or browsing. This is a good option if you just want to make a single version corresponding to a Chaste release available.



### Making the project available during submission

For papers about to be submitted, if you would like reviewers to be able to see unpublished wiki pages, ask an admin to send you details of the reviewer account, and ask for your wiki pages (and optionally your project code or a tag thereof) to be viewable from this account.
(Admins, this information can be found at #2022.)
