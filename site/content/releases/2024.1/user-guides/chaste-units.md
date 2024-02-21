---
title: "Chaste Units"
description: "Chaste Units"
draft: false
images: []
toc: true
layout: "single"
version: "2024.1"
---

This page provides information on the units used within Chaste.

## Cardiac Units

Note: $F$=Farad, $S$=Siemen=Amp/Volt, $A$=Ampere

| Quantity                                     | Units     | Notes                                                     |
|----------------------------------------------|-----------|-----------------------------------------------------------|
| Length                                       | $cm$      | hence surface-area-to-volume ratio is $cm^{-1}$ etc.      |
| Time                                         | $ms$      |                                                           |
| Voltage or intra- or extracellular potential | $mV$      |                                                           |
| Capacitance per unit surface area            | $\mu F \thickspace cm^{-2}$ | $C_m$ which we refer to as the capacitance, is actually a capacitance per unit area. The SI unit of capicitance is the Farad ( = Coulombs/Volts) ($C=Q/V$) |
| Conductivities                               | $mS \thickspace cm^{-1}$ |                                                        |
| (Stimulus) currents per unit volume          | $\mu A \thickspace cm^{-3}$ | Applies to (intracellular) **stimulus currents given to cells in mono/bidomain problems** (ie a stimulus current as a RHS source term in the bidomain equations. Note we don't allow RHS extracellular stimuli) |
| Currents per unit area | $\mu A \thickspace cm^{-2}$              | Applies to **all ionic currents** (single-cell/mono/bidomain equations), **intracellular stimuli in single-cell problems** or applied as Neumann boundary conditions, and **extracellular stimuli through electrodes** (which are also Neumann boundary conditions) |

## Cell-based

| Quantity | Units         | Notes                                                            |
|----------|---------------|------------------------------------------------------------------|
| Length   | dimensionless | Nondimensionalised by typical cell diameter (approx $10^{-5}$ m) |
| Time     | hours         |                                                                  |

## Mechanics
Material laws parameters, pressures, and active stresses (in cardiac
electro-mechanics) are in kPa. For mechanics simulations the user is free to
choose the units for all other quantities, but should do so consistently. For
example, if gravity is applied, then `[* gravitational acceleration](density)`
should be equal `kPa/[length]` (here `[]` denotes "units of"), since the
governing equations state that divergence of stress summed with density times
gravitational acceleration is zero.
