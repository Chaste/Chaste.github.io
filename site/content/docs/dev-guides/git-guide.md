---
title: "Git Guide"
description: "Git Guide"
draft: false
images: []
toc: true
layout: "single"
---

This page is a brief guide on using Git, designed primarily for developers
that are already used to Subversion.

{{< callout context="tip" title="See Also" icon="outline/rocket" >}}
[Pro Git](https://git-scm.com/book/en/): Everything
you need to know about Git.
{{< /callout >}}

## Cloning a repository

Cloning a Git repository is similar to checking out a subversion repository, but
instead of getting only a particular subversion commit, you end up with a full
independent Git repository that contains the **entire** history of the Git
repository that you are cloning.

### Official Chaste repository locations
|Repository |Description |
|---|---|
|`https://github.com/Chaste/Chaste.git`| Main Chaste repository for development; contains history since version 3.0.|
|`https://chaste.cs.ox.ac.uk/git/chaste_history.git`| Old Chaste repository; contains older history.|
|`https://chaste.cs.ox.ac.uk/git/project/<project_name>.git`| Old Chaste project repositories.|

### Code developer

If you want to have your default local branch point to `develop`, so you can
start using this branch straight away, you can use the `-b` flag to specify a
branch to clone:

```sh
git clone -b develop https://github.com/Chaste/Chaste.git
```

Note that all development work should proceed from a new branch off `develop` as
per the [Pull Request Strategy](../chaste-strategies/pull-request-strategy).

### Code user

These commands will setup your local branch to point to a specific release
tag from the remote repository, which is what we would recommend if you are
using Chaste for the basis of a paper and want your paper to use a specific
release of Chaste at the time of publication. 

```sh
git clone -b <release-tag> https://github.com/Chaste/Chaste.git
```

where `<release-tag>` is for a specific Chaste release e.g. `2024.1`.

There are other options you can use. You may want to use the `develop`
branch, which should pass all tests but will have some newer features -- you will
have to update your code more frequently to keep it in sync with the latest
Chaste code.

| Branch | What it's for |
|---|---|
| `develop` | Bleeding-edge development code, new feature (issue) branches should branch off here to minimise conflicts. |
| Release Tags | Released code for past Chaste versions (e.g. `2024.1`), also accessible from [GitHub](https://github.com/Chaste/Chaste/releases) with nice instructions and zip/tar files. | |

Unlike Subversion, Git does not use directories to manage branches. Git branches
are lightweight and considerably faster to use and merge with each other. Each
branch is simply a pointer to the commit at the head of the branch.

Note that Git does not have a `trunk`; you are always working on a branch,
although typically one branch fulfils the role of the `trunk` -- for Chaste, this
is the `develop` branch.

## Local repository changes

This is just like svn -- you commit to one repository (the local copy/clone of a
git repository).

### Committing

Inspecting your current local changes:

```sh
git status
git diff
```

You can add and remove files using the `add` and `rm` commands:

```sh
git add <file>
git rm <file>
```

If you want to commit **all** your local changes, you can use:

```sh
git commit -a -m "message"
```

The `-a` tells git to commit all changes. However, if you use this method you
are missing out on the benefits of Git's staging area, which allows you to add
individual files (or lines of a file) to the staging area. This allows you to,
for example, only add changes that belong to a particular issue.

```sh
git add <file1> <file2>
git add <directory>
git add -p <file3>
```

Committing your changes does not send them to the remote repository.
To do this you must use the `push` command. Assuming you want to
push back to the repository you have cloned, you can use `push` with no
arguments

```sh
git push
```

### Inspecting the history

- Use `log` to inspect history. Use `--oneline` for a brief summary.

```sh
git log
git log --oneline

```

- Use the `diff` command to see the differences between the working directory
  and the staging area.
- The `--staged` option shows changes between the staging area and the last
  commit.
- Use the `HEAD` pointer to see the changes between the working directory and
  the last commit

```sh
git diff <file>
git diff --staged
git diff HEAD
```

### Undoing changes

- Reset <file> (not yet added to staging area) to the last committed version:

```sh
git checkout <file>
```

- You can amend the current commit (e.g. change commit message, commit new changes etc)

```sh
git commit --amend
```

- You can remove a file from the staging area (i.e. after using `git add`)

```sh
git reset HEAD <file>
```

### Altering your history -- reset vs revert

- You can reset your history (soft reset) and optionally your working directory
  (hard reset) to a specified <commit>:

```sh
git reset <commit>
git reset --hard <commit>
```

- You can remove a specified commit from the history (a new commit is made with
  the necessary changes)

```sh
git revert <commit>
```

Altering your history is best avoided unless you know what you are doing! And
should DEFINITELY be avoided if you are messing with any commits that have
already made it to the Chaste remote repositories.

### Merging changes

You can provide the name of the branch you want to integrate to the `git merge`
command

```sh
git checkout <this-branch>
git merge <name-of-other-branch-to-merge-into-this-one>
```

For example, say you are working on the `develop` branch and want to write a new
feature. So you create a new branch to work on and make and commit a few changes
like so

```sh
git checkout -b new_feature_name develop
edit file1.cpp
git commit -a -m "my wow new feature"
```

Now assume new code has been pushed to the remote `develop` branch while you
were working on your feature. You want to merge the new code into your feature
branch, so you go back to the `develop` branch and get the new commits (see
[pull](#pull-and-fetch) below)

```sh
git checkout develop
git pull
```

Then you go back to your feature branch and merge in the new changes from develop

```sh
git checkout new_feature_name
git merge develop
```

### Merge conflicts

If there are no conflicting changes to `develop` then merging will work fine.
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
This is the new line in new_feature_name
=======
This is the new line in develop
>>>>>>> develop
```

Now you need to edit the file to resolve the merge, and then commit the result

```sh
git add file1.cpp
git commit -m "merged develop into new_feature_branch"
```

or

```sh
git commit -a -m "merged develop into new_feature_branch"
```

- If you want to see which files are still unmerged at any point, you can use
  `git status` to see the current state of the merge

## Working with remote repositories

Git is a distributed version control system. You can happily commit, branch and
merge to your heart's content on your own local Git repository. But eventually
you will want to send these changes to the main Chaste repository or to another
developer.

### Setting remotes

These will be set automatically if you clone a remote repository, but you can
manually change them too.

Your local repository has links to a number of remote repositories, you can get
a list using

```sh
git remote -v
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
git remote add <name> <url>
```

### Getting and sending changes

Firstly, you should make sure you've done all the local changes you want (i.e.
committed, see above).

#### Pull and fetch

You can get commits from a remote using the `pull` command

```sh
git pull
```

To get commits from a remote **without** merging them into your local
repository, use the `fetch` command instead

```sh
git fetch
```

The `branch` command will then show both the local and remote branches

```sh
git fetch
git branch -a
* master
remotes/origin/master
```

You can then merge any changes the remote branch (`origin/master`) into the
current local branch (`master`)

```sh
git merge origin/master
```

#### Push

To send your new commits to the default remote (normally `origin`), you can use
the `push` command

```sh
git push
```

Say you have created a new branch `<branch>` that you want to share, then you
can push it to `<remote>` using

```sh
git push <remote> <branch>
```

If you want to get a new branch pushed by another developer, you can use the
`checkout` command to create a new branch and set it up to track the correct
remote branch

For convenience on your own machine you can get git to remember your username
for the Chaste repositories. (Search for `git credential` to find out how to
store passwords securely on your OS too.)

```sh
git config --global credential.https://chaste.cs.ox.ac.uk.username <your-username>
```

## User projects

See [User Projects](../../user-guides/user-projects/) for a guide on how to make new git user
projects, or to convert existing svn ones to git.

## Tips, tricks and troubleshooting

- **Ignoring changes to local files in the git repo**
  
  The `.gitignore` file
  tells a repository the names of any files that should always be ignored for
  any/all copies of the repository. But sometimes it's useful to have some local
  changes that you don't want to involve in commits, or force on everyone with
  `.gitignore`. In this case, a command like this does the trick:

  ```sh
  git update-index --assume-unchanged <file>
  ```

- **Ignoring new files not in the git repo**
  
  Use the `.git/info/excludes` file
  [as explained here](http://stackoverflow.com/questions/1753070/git-ignore-files-only-locally).

{{< callout context="tip" title="See Also" icon="outline/rocket" >}}
[Pull Request Strategy](../chaste-strategies/pull-request-strategy)
{{< /callout >}}
