# C.elegans-Odour-Landscape
Python simulation of C. elegans chemotaxis based on Yoshida et al. (2012).


# C. elegans Odour Landscape Simulation

A Python simulation exploring how *Caenorhabditis elegans* navigates chemical gradients using klinokinesis and klinotaxis.

## Overview

This project implements a simplified computational model based on the behavioural framework described by Yoshida et al. (2012), *Odour concentration-dependent olfactory preference change in C. elegans*.

The simulation models the movement of a worm through a two-dimensional odour landscape and compares different navigation strategies.

The model includes:

* Random movement
* Klinokinesis (pirouette-based navigation)
* Klinotaxis (weathervane navigation)
* A combined klinokinesis + klinotaxis strategy

The aim is to investigate how different behavioural mechanisms influence the ability of *C. elegans* to navigate towards or away from an odour source.

## Model

The simulated worm moves with a constant speed of approximately 0.22 mm/s and is updated every 0.5 seconds.

The model includes correlated random curvature:

$$
\phi_i = 0.933\phi_{i-1} + \xi_i
$$

where the random component is sampled from a Gaussian distribution.

### Klinotaxis

The weathervane mechanism is represented by:
$$
\psi_i = \phi_i + \alpha\sin(\theta)
$$
where:

- $\phi_i$ is the random curvature
- $\alpha$ is the weathervane index
- $\theta$ is the bearing of the odour source relative to the worm's direction
Klinokinesis

The probability of a pirouette is dependent on the worm's direction relative to the odour source:
$$
P_{\mathrm{pirouette}}
=
P_{\mathrm{basal}}
-
I_{\mathrm{pirouette}}\cos(\theta)
$$
A pirouette causes the worm to make a large reorientation before continuing its movement.

## Simulation

The simulation creates an odour concentration field using an exponential decay from an odour source.

Multiple worms are simulated under four conditions:

1. Random walk
2. Klinokinesis
3. Klinotaxis
4. Klinokinesis + klinotaxis

Their trajectories are plotted over the odour landscape to allow comparison of the different navigation strategies.

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/c-elegans-odour-landscape.git
```

Change into the project directory:

```bash
cd c-elegans-odour-landscape
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Running the simulation

Run:

```bash
python OdourLandscape.py
```

The program will simulate the four navigation strategies and generate trajectory plots for comparison.

## Project status

This is a simplified reconstruction of the behavioural model described by Yoshida et al. (2012). Some behavioural parameters are approximated because the original paper presents several parameters graphically rather than as a complete numerical dataset.

The model is intended as a starting point for investigating how different chemotaxis strategies perform in different odour landscapes.

## Reference

Yoshida, K. et al. (2012). *Odour concentration-dependent olfactory preference change in C. elegans*. Nature Communications, 3, 739.

DOI: 10.1038/ncomms1750

## Future development

Possible extensions include:

* Implementing the exact experimentally measured parameter distributions
* Introducing noisy or turbulent odour landscapes
* Comparing smooth and patchy chemical gradients
* Measuring the time required to locate the odour source
* Measuring the proportion of worms reaching the source
* Comparing navigation efficiency between klinokinesis and klinotaxis
* Investigating concentration-dependent switching between attraction and avoidance
