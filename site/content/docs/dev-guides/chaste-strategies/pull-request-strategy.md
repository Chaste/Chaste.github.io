---
title: "Pull Request Strategy"
description: "Pull Request Strategy"
draft: false
images: []
toc: true
layout: "single"
---

## High-level strategy

- Work on a new branch on a single feature that has an associated issue.
- Create a [pull request](https://github.com/Chaste/Chaste/pulls) on GitHub.
- When the feature is ready, check that all GitHub actions have passed and request a review.
- Merge pull request when it is approved.

{{< callout context="tip" title="See Also" icon="rocket" >}}
* [External Developer Guide](../../external-developer-guide)
{{< /callout >}}


### Work on a new branch

The goal is to keep each pull request narrowly focussed:
* Each pull request should address one feature/bug, or at most a small 
number of closely-related features/bugs.
* Each pull request should be associated with a GitHub issue.

Work on a new branch -- the branch will eventually be deleted, so the name 
of the branch is not very important; but aim for something short and descriptive.

### Create a pull request

Create a pull request using the GitHub user interface.

You can create the pull request at any time; you do not need to wait for the 
feature to be complete. Each time you push new commits, the GitHub actions 
will be re-run giving you feedback on the state of compilation/testing.

### Wait for approval

Once the feature is complete and the GitHub actions are all passing, request a review.
This can be done via the pull request interface in the right-hand panel.
Either choose an appropriate reviewer or ask in Slack for who would be an appropriate reviewer.

### Merge pull request

Once the pull request is approved, merge it using the pull request interface. 
Do not choose the "squash commits" option as this eliminates all intermediate commit history.

{{< callout context="note" title="Note" icon="info-circle" >}}
After merging into `develop`, don't forget to delete the branch to keep the 
repository clean. This can be done from the pull request interface.
{{< /callout >}}


