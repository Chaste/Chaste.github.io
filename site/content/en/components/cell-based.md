---
title : "Cell-based Chaste"
description: "a multiscale computational framework for modelling cell populations"
lead: "a multiscale computational framework for modelling cell populations"
date: 2020-10-06T08:47:36+00:00
lastmod: 2020-10-06T08:47:36+00:00
draft: false
images: []
toc: true
menu:
  docs:
    parent: "prologue"
---

## Introduction and aims
Mathematical and computational models of biological and physiological systems are rapidly increasing in complexity.
This is especially true of fields such as cancer modelling, where the amount of available biological data is increasing exponentially.
Modelling approaches therefore span the range from detailed models of molecular level processes, right through to biomechanical models at the tissue level.
The aim of cell-based Chaste is to develop a computational framework that bridges across these spatial and temporal scales within a single, generic modelling framework.

The initial focus of this work was the dynamic mechanisms underlying the onset of colorectal cancers.
This area was chosen due to the availability of particularly good experimental data, and since its biological understanding is sufficiently advanced to allow such a systems-level approach.
Colorectal cancers originate from the epithelium that covers the luminal surface of the intestinal tract.
This epithelium renews itself through a coordinated programme of cell proliferation, migration and differentiation, which begins in the of tiny crypts of Lieberkühn that descend from the epithelium into the underlying connective tissue.
A specialist crypt code component has been developed in Chaste to study intestinal crypts and the initiation of colorectal cancer.
This component includes code to define the intestinal crypt geometry, Wnt signalling pathway and intestinal cell-cycle models, and has been used to examine theoretically the concept and role of stem cells in crypt homeostasis and the role of mechanical effects in cell behaviour.
