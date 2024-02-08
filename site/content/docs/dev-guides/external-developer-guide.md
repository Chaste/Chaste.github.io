---
title: "External Developer Guide"
description: "Helpful resources for users of development versions of Chaste"
draft: false
images: []
toc: true
layout: "single"
---

{{< callout context="note" title="Note" icon="info-circle" >}}
Before you start -- if you are Chaste User, and never want to contribute back to
the source code, you might want to consider just downloading one of the
[release versions](https://github.com/Chaste/Chaste/releases) of Chaste.
{{< /callout >}}

This page is intended to assist those external to the core Chaste team who still
want to develop with the "bleeding edge" latest development code, rather than
merely the last official release.

Since some parts of the Chaste code-base are not released (e.g. those relating
specifically to papers in preparation), some of the developer resources, such as
results from the automated tests and full documentation for the latest revision,
are not made publicly available. We have now created some additional resources
to improve this situation.

## The most recent "good revision"

Occasionally broken code is committed to branches on the Chaste repository, or some
unexpected tests fail. This can be frustrating if users do not know if it's
something they've broken, or if the fault lies with the repository code. We now
offer a range of git branches to help developers choose how stable they want
their code to be:

| **Branch** | **What it's for** |
|---|---|
| `develop` | Bleeding-edge development code, new feature (issue) branches should branch off here to minimise conflicts |
| `release` | The last full release of the code. |
| Release Tags | Released code for past Chaste versions (e.g. v3.4), also accessible from [GitHub](https://github.com/Chaste/Chaste/releases) with nice instructions and zip/tar files | |

You can get these revisions by cloning the repository and then doing

```sh
git checkout <branch>
```

e.g.

```sh
git checkout develop
```

## Contributing Code Back to Chaste

### Before you start

If you intend to submit code back to the main Chaste repository, please see
the [Best Practice Guide](../best-practice-guide).

### Coding Standards

To understand why Chaste variables, methods and classes are named like they are
please see our
[C++ Naming Strategy](../chaste-strategies/cpp-naming-strategy).

We also lay out and document our code in a particular way -- see our
[Code Structure Strategy](../chaste-strategies/code-structure-strategy).

You may also want to read through the other
[Chaste Strategies](../chaste-strategies/) that we use to keep things consistent
and well tested.

### Creating an Issue

First [create a new issue](https://github.com/Chaste/Chaste/issues) on GitHub
and describe the problem you are trying to solve.

### Working in a new branch

Please see the [Issue Workflow](#issue-workflow) for how to work in a new branch
-- you should branch off `develop` if you want to contribute code back to the
main Chaste repository.

Make sure you merge in the latest `develop` branch into your issue branch
regularly to keep up to date and avoid lots of changes before merging back into
our main repo.

Ideally, write a comment on your issue about any commits that you have done and
pushed to your branch.

### Testing

Run all tests (continuous, nightly, parallel, coverage, memory) as per the
[CMake Build Guide](../cmake-build-guide#other-useful-targets)

When you have run all tests locally, then we can run them on GitHub Actions
before merging your pull request into `develop` when all these pass.

## Using Git

This is a brief guide on using Git, designed primarily for developers that are
already used to Subversion.

Before you let yourself loose in the depths of Chaste and git, you might like to
read some of this
[Git Guide](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics).

### Quick Start

Assuming all you want to do is get the Chaste source code, make a few commits
and push these back to the main repo, you can do something like this

```sh
$ git clone -b develop https://github.com/Chaste/Chaste.git Chaste
$ cd Chaste
$ edit cell_based/src/cell/Cell.cpp
 ... compile and run tests ...
$ git commit -a -m "#1234 Fix problems with `Cell.cpp`"
$ git push
```

### Cloning a Repository

Cloning a Git repository is similar to checking out a subversion repository, but
instead of getting only a particular subversion commit, you end up with a full
independent Git repository that contains the **entire** history of the Git
repository that you are cloning.

#### Official Chaste Repository Locations

- https://github.com/Chaste/Chaste.git -- New Chaste repository for development,
  only contains history since Version 3.0
- https://chaste.cs.ox.ac.uk/git/chaste_history.git -- Full Chaste repository,
  contains all history
- https://chaste.cs.ox.ac.uk/git/project/<your_project_name_here>.git -- Project
  repositories

### Commands

#### Code developer

If you want to have your default local branch point to `develop`, so you can
start using this branch straight away, you can use the `-b` flag to specify a
branch to clone:

```sh
$ git clone -b develop https://github.com/Chaste/Chaste.git Chaste
```

Note that all development work should proceed from a new branch off `develop` as
per [the issue workflow](#issue-workflow).

#### Code user

```sh
$ git clone -b release https://github.com/Chaste/Chaste.git Chaste
```

Note that this command will setup your local branch to point to the `release`
branch of the remote repository, which is what we would recommend if you are
using Chaste for the basis of a paper and want your paper to use the latest
release of Chaste at the time of publication. There are other options you can
use.

You may also want to use a `develop` branch for one that should pass all tests
but will have some newer features - you may have to update your code more
frequently to keep it in sync with the latest chaste code.

### Local Repository Changes

You commit to one repository (the local copy/clone of a git repository).

#### Committing

Inspecting your current local changes:

```sh
$ git status
$ git diff
```

You can add and remove files using the `add` and `rm` commands:

```sh
$ git add <file>
$ git rm <file>
```

If you want to commit **all** your local changes, you can use:

```sh
$ git commit -a -m "message"
```

The `-a` tells git to commit all changes. However, if you use this method you
are missing out on the benefits of Git's staging area, which allows you to add
individual files (or lines of a file) to the staging area. This allows you to ,
for example, only add changes that belong to a particular issue.

```sh
$ git add <file1> <file2>
$ git add <directory>
$ git add -p <file3>
```

Committing your changes does not send them to the remote repository.
To do this you must use the `push` command. Assuming you want to
push back to the repository you have cloned, you can use `push` with no
arguments

```sh
$ git push
```

#### Inspecting the History

- Use `log` to inspect history. Use `--oneline` for a brief summary.

```sh
$ git log
$ git log --oneline

```

- Use the `diff` command to see the differences between the working directory
  and the staging area.
- The `--staged` option shows changes between the staging area and the last
  commit.
- Use the `HEAD` pointer to see the changes between the working directory and
  the last commit

```sh
$ git diff <file>
$ git diff --staged
$ git diff HEAD
```

#### Undoing Changes

- Reset <file> (not yet added to staging area) to the last committed version:

```sh
$ git checkout <file>
```

- You can amend the current commit (e.g. change commit message, commit new changes etc)

```sh
$ git commit --amend
```

- You can remove a file from the staging area (i.e. after using `git add`)

```sh
$ git reset HEAD <file>
```

#### Altering your history - Reset versus Revert

- You can reset your history (soft reset) and optionally your working directory
  (hard reset) to a specified <commit>:

```sh
$ git reset <commit>
$ git reset --hard <commit>
```

- You can remove a specified commit from the history (a new commit is made with
  the necessary changes)

```sh
$ git revert <commit>
```

Altering your history is best avoided unless you know what you are doing! And
should DEFINITELY be avoided if you are messing with any commits that have
already made it to the Chaste remote repositories.

### Merging Changes

You can provide the name of the branch you want to integrate to the `git merge`
command

```sh
$ git checkout <this-branch>
$ git merge <name-of-other-branch-to-merge-into-this-one>
```

For example, say you are working on the `develop` branch and want to write a new
feature. So you create a new branch to work on and make and commit a few changes
like so

```sh
$ git checkout -b new_feature_name develop
$ edit file1.cpp
$ commit -a -m "my wow new feature"
```

Now assume you have tested and are happy with the new changes. So you then go
back to the `develop` branch and merge the feature

```sh
$ git checkout develop
$ git merge new_feature_name
```

#### Merge Conflict

If you haven't been making new commits to `develop` then this will work fine.
However, if there are conflicting edits on `develop` and `new_feature_name` you
might get an error message like so

```
Auto-merging file1.cpp
CONFLICT (content): Merge conflict in file1.cpp
Automatic merge failed; fix conflicts and then commit the result.
```

If you open `file1.cpp`, you will see standard conflict-resolution markers like
this:

```
<<<<<<< HEAD
This is the new line in develop
=======
This is the new line in new_feature_name
>>>>>>> new_feature_name
```

Now you need to edit the file to resolve the merge, and then commit the result

```sh
$ git add file1.cpp
$ git commit -m "merged new_feature_branch into develop"
```

or

```sh
$  git commit -a -m "merged new_feature_branch into develop"
```

- If you want to see which files are still unmerged at any point, you can use
  `git status` to see the current state of the merge

## Working with Remote Repositories

Git is a distributed version control system. You can happily commit, branch and
merge to your heart's content on your own, local, Git repository. But eventually
you will want to send these changes to the main Chaste repository or to another
developer.

### Setting Remotes

These will be set automatically if you clone a remote repository, but you can
manually change them too.

Your local repository has links to a number of remote repositories, you can get
a list using

```sh
$ git remote -v
```

Assuming you cloned your local repository from the main Chaste repo, you should
see something like

```sh
origin https://github.com/Chaste/Chaste.git (fetch)
origin https://github.com/Chaste/Chaste.git (push)
```

`origin` is the name of the remote (the cloned repo is always given this name by
default).

You can add a remote repo using the `remote` command

```sh
$ git remote add <name> <url>
```

### Getting and Sending changes

Firstly, you should make sure you've done all the local changes you want (i.e.
committed, see above).

#### Pull and Fetch

You can get commits from a remote using the `pull` command

```sh
$ git pull
```

To get commits from a remote **without** merging them into your local
repository, use the `fetch` command instead

```sh
$ git fetch
```

The `branch` command will then show both the local and remote branches

```sh
$ git fetch
$ git branch -a
* master
remotes/origin/master
```

You can then merge any changes the remote branch (`origin/master`) into the
current local branch (`master`)

```sh
$ git merge origin/master
```

#### Push

To send your new commits to the default remote (normally `origin`), you can use
the `push` command

```sh
$ git push
```

Say you have created a new branch `<branch>` that you want to share, then you
can push it to `<remote>` using

```sh
$ git push <remote> <branch>
```

If you want to get a new branch pushed by another developer, you can use the
`checkout` command to create a new branch and set it up to track the correct
remote branch

For convenience on your own machine you can get git to remember your username
for the Chaste repositories. (Search for `git credential` to find out how to
store passwords securely on your OS too.)

```sh
$ git config --global credential.https://chaste.cs.ox.ac.uk.username <your-username>
```

## Issue workflow

Unlike Subversion, Git branches do not use directories to manage branches and
are lightweight and considerably faster to use and merge with each other. Each
branch is simply a pointer to the commit at the head of the branch.

Note that Git does not have a `trunk`, you are always working on a branch,
although typically the `master` branch fulfils the role of the `trunk`. Note
that for the Chaste project, all development must occur from the `develop` branch.

The rough idea is that from now on **every issue's commits will appear on a
feature branch (branched out from `develop`), until the issue is ready to be
closed, and then they'll be merged back in to develop**.

{{< callout context="tip" title="See Also" icon="rocket" >}}
[Pull Request Strategy](../chaste-strategies/pull-request-strategy)
{{< /callout >}}

### Opening a brand new issue

First, make sure you've made a new GitHub issue. This will have a number, let's
say XXXX. So the git branch will be called `XXXX_issue_description`, wherever
you see this below replace it with the number of your issue!

**Note:** only do this if the issue has never been worked on before, and an
`<XXXX_issue_description>` branch doesn't exist in the main repository already.
If you haven't just opened the GitHub issue so you aren't sure whether it
exists, you can type:

```sh
$ git branch -a
```

which will display all local and remote branches that are available. If
<XXXX_issue_description> does exist, skip down to the
[next section](#working-on-a-pre-existing-issue).

#### Local repo

When you start work on a new issue, you first need to create a branch on your
local repository, as discussed here. If instead you want to use a pre-existing
feature branch that's on the Chaste repo, see below.

You can pass the `-b` flag to the `git checkout` command to create and
switch to a new branch in one action:

```sh
$ git checkout -b <XXXX_issue_description> develop
```

To list all the available (local) branches:

```sh
$ git branch
```

#### Main repo

If you've made a new feature branch locally, you should then immediately make a
copy of that on the central Chaste git repository, so do:

```sh
$ git checkout <XXXX_issue_description>  # Just makes sure the branch you want to push is the one currently checked out locally.
$ git push -u <remote> <XXXX_issue_description> # Push a copy to the main Chaste repo. <remote> is probably just = origin. The -u should make git track the pushed branch as the new remote.
```

This will make a copy, with the same name, on the main Chaste repo that other
people can work on too, by checking it out as below.

### Working on a pre-existing issue

If an issue feature branch already exists, and you just want to grab a copy of
it on your local repository just do:

```sh
$ git checkout --track <remote>/<branch>
```

e.g.

```sh
$ git checkout --track origin/<XXXX_issue_description>
```

Note that after a branch is setup to `--track` a remote branch, every subsequent
use of `git pull` and `git push` with no additional arguments will pull/push
changes between the local and remote branches.

Note for all recent versions of Git (>1.6.6), as long as you have previously
fetched the remote branch (run the above commands once), you can simply use

```sh
$ git checkout <XXXX_issue_description>
$ git pull
```

Then make all the local commits you need and push them to the server, as above.

#### Commit Messages

All commits to the main repo to do with your issue should start with the issue
number, prefixed with a hash symbol, e.g.

```sh
git commit -m "#<XXXX> an informative message describing the changes."
```

e.g.

```sh
git commit -m "#3057 added special case for python3.5 to prevent upgrade of pip to incompatible version."
```

This means that things are nicely cross-referenced when looking at the timeline
and doing detective work!

### Merge the changes into develop

For the issue's changes to be shared with everyone, we automatically run through
the test suite and eventually merge them into `develop` when all tests pass.
Best to think of this in a few stages:

#### Test locally

Before you merge in changes from your issue branch, it probably makes sense to
locally test your code with any changes that have happened in `develop` since
you branched off. So get any changes to develop with:

```sh
$ git checkout develop
$ git pull
```

Now go to your issue branch, and merge in these changes

```sh
$ git checkout <XXXX_issue_description>
$ git pull     # Get any changes that other people have done in the meantime!
$ git merge develop
```

sort out any conflicts that arise, and run local test suite.

#### Local repo

Merges can become very messy (despite git's advocates telling you otherwise!) if
you are behind in the history, so do:

```sh
$ git checkout develop
$ git pull
```

To get your develop branch up to date (sort out any conflicts -- there shouldn't
be any if you've been doing work in issue branches!)

Then the main command is simply

```sh
$ git merge <XXXX_issue_description>
```

#### Main repo

Finally, send the change to `develop` to the main server with:

```sh
$ git push
```

### Closing an issue

After an issue branch passes all tests, it can be merged into `develop`. The
last thing we should do on each GitHub issue now should be to delete the
branches from the repo.

To make sure that the GitHub issue references all the relevant commits, all
commits to do with your issue should start with the issue number, prefixed with
a hash symbol as described in [commit messages](#commit-messages).

#### Local repo

```sh
$ git branch -d <XXXX_issue_description>

```

Note this only works if all the changes have been merged into `develop`
(clever!). If for any reason you have extra local changes, but definitely don't
want them merging in, you need to use an extra `--force` flag.

#### Main repo

There's a special command for this (because `git push` just refers to the branch
you're on, not the whole repo):

```sh
$ git push origin --delete <XXXX_issue_description>
```

works on recent git clients. If your `git --version` is < 1.7.0 you need to use
`git push origin :<XXXX_issue_description>`.

## User projects

See [User Projects](../user-projects/) for a guide on how to make new git user
projects, or to convert existing svn ones to git.

## Tips, tricks and troubleshooting

- **Ignoring changes to local files in the git repo**: The `.gitignore` file
  tells a repository the names of any files that should always be ignored for
  any/all copies of the repository. But sometimes it's useful to have some local
  changes that you don't want to involve in commits, or force on everyone with
  `.gitignore`. In this case, a command like this does the trick:

```sh
git update-index --assume-unchanged <file>
```

- **Ignoring new files not in the git repo**: Use the `.git/info/excludes` file
  [as explained here](http://stackoverflow.com/questions/1753070/git-ignore-files-only-locally).
