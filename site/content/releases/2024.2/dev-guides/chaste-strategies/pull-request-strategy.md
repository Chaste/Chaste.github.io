---
title: "Pull Request Strategy"
description: "Pull Request Strategy"
draft: false
images: []
toc: true
layout: "single"
version: "2024.2"
---

## High-level strategy

- Work on a new branch on a single feature that has an associated issue.
- Create a [pull request](https://github.com/Chaste/Chaste/pulls) on GitHub.
- When the feature is ready, check that all GitHub actions have passed and request a review.
- Merge pull request when it is approved.

## Work on a feature branch

The goal is to keep each pull request narrowly focussed:
* Each pull request should address one feature/bug, or at most a small 
number of closely-related features/bugs.
* Each pull request should be associated with a GitHub issue.

The rough idea is that every issue's commits will appear on a
feature branch (branched out from `develop`), until the issue is ready to be
closed, and then they'll be merged back in to develop.


### Opening a brand new issue

First, make sure you've made a new GitHub issue. This will have a number, let's
say `XXXX`. So the git branch can be called, for example,
`XXXX_issue_description`. Wherever you see `XXXX` below, replace it with the
number of your issue! The branch will eventually be deleted, so the name of the
branch is not hugely important; but aim for something short and descriptive.

**Note:** only do this if the issue has never been worked on before, and an
`<XXXX_issue_description>` branch doesn't exist in the main repository already.
If you haven't just opened the GitHub issue so you aren't sure whether it
exists, you can type:

```sh
git branch -a
```

which will display all local and remote branches that are available. If
`<XXXX_issue_description>` does exist, skip down to the
[next section](#working-on-a-pre-existing-issue).

#### Local repo

When you start work on a new issue, you first need to create a branch on your
local repository, as discussed here. If instead you want to use a pre-existing
feature branch that's on the Chaste repo, see below.

You can pass the `-b` flag to the `git checkout` command to create and
switch to a new branch in one action:

```sh
git checkout -b <XXXX_issue_description> develop
```

To list all the available (local) branches:

```sh
git branch
```

#### Remote repo

If you've made a new feature branch locally, you should then immediately make a
copy of that on the central Chaste git repository, so do:

```sh
# Just makes sure the branch you want to push is the one currently checked out locally.
git checkout <XXXX_issue_description>

# Push a copy to the main Chaste repo. <remote> is probably just = origin.
# The -u should make git track the pushed branch as the new remote.
git push -u <remote> <XXXX_issue_description>
```

This will make a copy, with the same name, on the main Chaste repo that other
people can work on too, by checking it out as below.

### Working on a pre-existing issue

If an issue feature branch already exists, and you just want to grab a copy of
it on your local repository just do:

```sh
git checkout --track <remote>/<branch>
```

e.g.

```sh
git checkout --track origin/<XXXX_issue_description>
```

Note that after a branch is setup to `--track` a remote branch, every subsequent
use of `git pull` and `git push` with no additional arguments will pull/push
changes between the local and remote branches.

Note for all recent versions of Git (>1.6.6), as long as you have previously
fetched the remote branch (run the above commands once), you can simply use

```sh
git checkout <XXXX_issue_description>
git pull
```

Then make all the local commits you need and push them to the server, as above.

#### Commit messages

To make sure that the GitHub issue references all the relevant commits, all
commits to do with your issue should start with the issue number, prefixed with
a hash symbol, e.g.

```sh
git commit -m "#<XXXX> an informative message describing the changes."
```

e.g.

```sh
git commit -m "#3057 added special case for python3.5 to prevent upgrade of pip to incompatible version."
```

This means that things are nicely cross-referenced when looking at the timeline
and doing detective work!

## Create a pull request

Create a [pull request](https://github.com/Chaste/Chaste/pulls) using the GitHub user interface. You can create the pull request at any time; you do not need to wait for the feature to be complete.

Each time you push new commits, the
[GitHub actions](https://github.com/Chaste/Chaste/actions) will be re-run giving
you feedback on the state of compilation/testing.

### Getting changes from develop

It probably makes sense to test your code with any changes that have happened in
`develop` since you branched off. So get any changes to develop with:

```sh
git checkout develop
git pull
```

Now go to your local issue branch, and merge in these changes

```sh
git checkout <XXXX_issue_description>
git pull     # Get any changes that other people have done in the meantime!
git merge develop
```

Sort out any conflicts that arise, and send the change to
`XXXX_issue_description` on the remote server with:

```sh
git push
```

## Wait for approval

Once the feature is complete and the GitHub actions are all passing, request a review.
This can be done via the pull request interface in the right-hand panel.
Either choose an appropriate reviewer or ask in Slack for who would be an appropriate reviewer.

## Merge pull request

Once the pull request is approved, merge it using the pull request interface. 
Do not choose the "squash commits" option as this eliminates all intermediate commit history.

After an issue branch passes all tests and is merged into `develop`, the last
thing we should do on each issue should be to delete the branches to
keep the repository clean. On GitHub, this can be done from the pull request
interface.

On your local repo,

```sh
git branch -d <XXXX_issue_description>
```

Note this only works if all the changes have been merged into `develop`
(clever!). If for any reason you have extra local changes, but definitely don't
want them merging in, you need to use an extra `--force` flag.

{{< callout context="tip" title="See Also" icon="outline/rocket" >}}
* [External Developer Guide](../../external-developer-guide)
* [Git Guide](../../git-guide)
{{< /callout >}}
