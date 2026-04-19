# An Empirical Logarithmic Relation Between Gravitational and Electromagnetic Coupling Constants

Code and notebooks for the paper:

> **An Empirical Logarithmic Relation Between Gravitational and Electromagnetic Coupling Constants**
>
> Liang Wang, 2026

## Core Result

An empirical relation connecting the Planck-proton mass hierarchy to the electromagnetic coupling:

```
π · ln(m_P / m_p) = 138.27 ≈ 1/α_em = 137.04   (0.9% in log, factor 2.19 in G)
```

Equivalently:

```
G ≈ (ℏc/m_p²) · exp(-2/πα_em)
```

This captures 35 of 36 orders of magnitude in the gauge hierarchy with no free parameters,
but the predicted G is off by a factor of 2.19 from the measured value.

## Statistical Analysis

- Proton-specific p-value: 0.029 (1/35 low-complexity constants hit within 1%)
- Family p-value (5 SM masses): ~0.5 (proton not uniquely singled out)
- m_tau (-0.6%) and m_pi×3 (+0.5%) give comparable or better agreement
- The relation favors a mass scale near ~1 GeV, not the proton specifically

## Notebooks

| # | Notebook | Description |
|---|----------|-------------|
| 1 | `01_137_connection.ipynb` | Core numerical relation and comparison |
| 2 | `02_spectral_action.ipynb` | Riemann zero spectral action analysis |
| 3 | `03_G_constraints.ipynb` | G(t) time evolution and constraint checks |
| 4 | `04_statistical_analysis.py` | Look-elsewhere and sensitivity analysis |

## Quick Start

```bash
cd notebooks
jupyter lab
```

All notebooks run on CPU with standard Python packages (`numpy`, `matplotlib`, `scipy`).

## Citation

```bibtex
@misc{Wang2026PLB,
  author    = {Wang, Liang},
  title     = {An Empirical Logarithmic Relation Between Gravitational
               and Electromagnetic Coupling Constants},
  year      = {2026},
  note      = {v1.0},
  doi       = {10.5281/zenodo.19649205},
  publisher = {Zenodo}
}
```

## Related Work

- [DSC Framework](https://doi.org/10.5281/zenodo.19429778) — Discrete Symplectic Cosmology theory
- [Fine-Structure Constant & Hubble Tension](https://doi.org/10.5281/zenodo.19218674) — Empirical evidence for 1/ln²(t) scaling
- [DSC-CMB Simulation](https://github.com/maris205/riemann_engine) — CMB simulation code
