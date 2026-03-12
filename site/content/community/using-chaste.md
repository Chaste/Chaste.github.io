---
title: "Guidelines for using Chaste in your research"
description: "Guidelines for Chaste users and PIs"
draft: false
images: []
toc: true
layout: "single"
---


Chaste is a large and mature codebase used in many areas of computational biology.
Because of its breadth and flexibility, there are often multiple ways to approach a modelling problem.

If you or your students, postdocs or collaborators are planning to use Chaste, we encourage you to get in touch and briefly describe your research aims.
The best ways to get in touch are either:

1. Through our public [discussions board](https://github.com/Chaste/Chaste/discussions)
2. Via email to one of [the team](https://chaste.github.io/team/)

We can often suggest relevant examples, modelling approaches, or existing components that may save you significant time.

If you plan to develop new features or extend existing functionality, early discussion is particularly valuable.
We can advise on design choices, testing expectations, and how best to structure your work so that it remains maintainable and can be merged smoothly into Chaste when it's ready.


## Guidelines for Principal Investigators

Sustaining Chaste requires a baseline of continual development effort, in addition to development aligned with scientific need, and both require support through research funding.

When applying for grants that depend on Chaste, we encourage Principal Investigators to cost appropriate Research Software Engineering (RSE) time.
This can support:

1. The baseline effort: maintaining compatibility with evolving platforms and dependencies
2. Implementing new functionality required by the research
3. Supporting and mentoring students and early-career researchers who are using and contributing to Chaste

The third categories is especially valuable, as widening the pool of researchers who can maintain Chaste is critical to its longevity.

At the Universities of Oxford, Nottingham, and Sheffield, internal RSE groups have established expertise in Chaste and can be costed directly into grant applications.
Researchers at other institutions are encouraged to contact us to discuss potential collaboration and inclusion of appropriate software effort.

We also strongly encourage PIs to engage with the Chaste core developers from the early stages of a project.
Early discussion of planned extensions or new functionality helps shape design decisions, align work with existing architecture, and avoid a large, difficult-to-merge code drop at the end of a grant.
Ongoing interaction throughout a project leads to smoother integration and more sustainable outcomes.

Embedding RSE support within grants strengthens individual projects, ensures continued availabity of Chaste, and helps ensure Chaste continues to evolve in line with research priorities.


## Guidelines for researchers

Chaste is designed to support rigorous, reproducible research.
Engaging early with the community can help you identify the most suitable modelling framework and avoid unnecessary duplication of effort.

We recommend developing new work within [user projects](/docs/user-guides/user-projects/) wherever possible.
This allows you to progress independently while keeping the core codebase stable.
When functionality matures, you can propose changes for inclusion in Chaste itself, and the more we know about the work you're doing, the easier this process will be.

Where possible, prefer adding new classes or methods rather than modifying existing ones.
This reduces the risk of unintended side effects and makes review and future maintenance simpler.

If you believe existing functionality needs to be changed, please get in touch first.
There may be an existing way, or potentially an easier or more maintainable way to achieve what you are aiming for.

When modifying core functionality, aim to work in small, manageable increments and open pull requests early for review.
Smaller changes are easier to discuss, test, and merge than large diverging branches, and this approach will help you avoid time-consuming integration issues later.

Keeping the community in the loop about what you're developing will significantly increase the likelihood that your developments can be reused and built upon by others.
