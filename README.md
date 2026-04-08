# Dynamic Location Theory (DLT)

**A frequency-based framework for spatial position, temporal re-localization, and informational retrieval**

**Christopher Woodyard**<br>
Vers3Dynamics &middot; R.A.I.N. Lab<br>
Washington, D.C., USA

[![PDF](https://img.shields.io/badge/PDF-Read%20Paper-blue?style=flat-square&logo=adobeacrobatreader)](137.pdf)
[![Repository](https://img.shields.io/badge/GitHub-Repository-black?style=flat-square&logo=github)](https://github.com/topherchris420/research)

---

## Research posture

This repository presents **Dynamic Location Theory** as a research framework worth investigating. The core claim is that **location is a property of the object**, expressed through resonance between matter and a background scalar field rather than through external spacetime labels alone.

The work is presented as a serious, falsifiable proposal with direct paths into the paper, citation, equations, and repository source.

## Abstract

The paper unifies spatial localization and temporal re-localization under a single-resonance model in which the spatiotemporal position of a physical system is encoded in the dominant resonance frequency of its coupled matter-scalar-field state.

The framework supplies concrete predictions for:

- atomic-clock interferometry
- matter-wave interferometry
- gravitational-wave detection

## Quick links

- [Read the paper](137.pdf)
- [Research website source](https://github.com/topherchris420/research)
- [R.A.I.N. Lab repository](https://github.com/topherchris420/james_library)

## Citation

```bibtex
@misc{woodyard2026dlt,
  author    = {Christopher Woodyard},
  title     = {Dynamic Localization Across Space and Time: A Frequency-Based Framework},
  year      = {2026},
  doi       = {10.5281/zenodo.18263032},
  publisher = {Vers3Dynamics, R.A.I.N. Lab},
  url       = {https://vers3dynamics.com}
}
```

## Website license

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.


## DLT simulation prototype (Python)

A runnable prototype is included in `dlt_simulation.py` and models spatial position and temporal re-localization from resonance coupling.

### Quick start

```bash
python dlt_simulation.py --num-objects 300 --steps 1500 --coupling 1.2 --animate
```

### Parameter controls

- `--num-objects`: number of simulated objects
- `--omega-min`, `--omega-max`: resonance frequency range
- `--coupling`: interaction strength κ
- `--noise`: phase perturbation amplitude
- `--speed`: simulation drift speed
- `--log-trajectories --save-log out.npz`: optional logging
