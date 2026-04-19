#!/usr/bin/env python3
"""
Look-elsewhere analysis for the 137 connection.
Following the reviewer's prescription: fixed grammar, fixed catalog, exhaustive enumeration.
"""
import numpy as np
from itertools import product as iterproduct
import matplotlib.pyplot as plt

plt.rcParams.update({'figure.dpi': 120, 'font.size': 11, 'font.family': 'serif'})

# ============================================================
# 1. Atomic catalog of dimensionless quantities
# ============================================================
# Masses in GeV
m_e = 0.000511; m_mu = 0.1057; m_tau = 1.777
m_p = 0.9383; m_n = 0.9396; m_pi = 0.1396; m_pi0 = 0.1350
Lambda_QCD = 0.220; m_W = 80.38; m_Z = 91.19; m_H = 125.1
v_higgs = 246.2  # Higgs VEV
m_P = 1.221e19  # Planck mass in GeV

# Couplings at various scales
alpha_em_0 = 1/137.036      # Thomson limit
alpha_em_me = 1/135.9       # at m_e
alpha_em_mmu = 1/133.5      # at m_mu  
alpha_em_mp = 1/133.5       # at m_p (approx)
alpha_em_MZ = 1/127.95      # at M_Z
alpha_s_MZ = 0.1179         # strong coupling at M_Z
sin2_thetaW = 0.2312        # weak mixing angle

# Build catalog
masses = {
    'm_e': m_e, 'm_mu': m_mu, 'm_tau': m_tau,
    'm_p': m_p, 'm_n': m_n, 'm_pi': m_pi, 'm_pi0': m_pi0,
    'Lambda_QCD': Lambda_QCD, 'm_W': m_W, 'm_Z': m_Z,
    'm_H': m_H, 'v_Higgs': v_higgs,
}

couplings = {
    'alpha_em(0)': alpha_em_0,
    'alpha_em(m_e)': alpha_em_me,
    'alpha_em(m_mu)': alpha_em_mmu,
    'alpha_em(M_Z)': alpha_em_MZ,
    'alpha_s(M_Z)': alpha_s_MZ,
    'sin2_thetaW': sin2_thetaW,
}

# Derived: ln(m_P/m_i) for each mass
log_ratios = {}
for name, m in masses.items():
    log_ratios[f'ln(m_P/{name})'] = np.log(m_P / m)

# ============================================================
# 2. Search grammar: u(q_i) ≈ C · v(q_j)
# ============================================================
# Transforms: x, ln(x), ln(1/x), 1/x
def transforms(x, name):
    results = {}
    if x > 0:
        results[f'{name}'] = x
        results[f'ln({name})'] = np.log(x)
        results[f'ln(1/{name})'] = np.log(1/x)
        results[f'1/{name}'] = 1/x
    return results

# Nice constants (low complexity)
nice_constants = {
    '1': 1, '2': 2, 'pi': np.pi, 'pi/2': np.pi/2,
    '2pi': 2*np.pi, 'sqrt(2)': np.sqrt(2), 'sqrt(pi)': np.sqrt(np.pi),
    'e': np.e, 'e/pi': np.e/np.pi, 'pi/e': np.pi/np.e,
    '1/2': 0.5, '3': 3, '4': 4,
}

# ============================================================
# 3. Exhaustive enumeration
# ============================================================
print("=" * 60)
print("Look-Elsewhere Analysis")
print("=" * 60)

# Build all LHS quantities (from log_ratios and couplings)
all_quantities = {}
for name, val in log_ratios.items():
    all_quantities.update(transforms(val, name))
for name, val in couplings.items():
    all_quantities.update(transforms(val, name))

# Build all RHS quantities (same catalog)
# We look for: u(q_i) ≈ C · v(q_j) where C is a nice constant

results = []
for (lhs_name, lhs_val), (rhs_name, rhs_val) in iterproduct(
    all_quantities.items(), all_quantities.items()
):
    if lhs_name == rhs_name:
        continue
    if abs(rhs_val) < 1e-10 or abs(lhs_val) < 1e-10:
        continue
    
    ratio = lhs_val / rhs_val
    if abs(ratio) < 0.01 or abs(ratio) > 100:
        continue
    
    for c_name, c_val in nice_constants.items():
        if abs(c_val) < 1e-10:
            continue
        rel_error = abs(ratio / c_val - 1)
        if rel_error < 0.02:  # within 2%
            results.append({
                'lhs': lhs_name, 'rhs': rhs_name,
                'C': c_name, 'C_val': c_val,
                'ratio': ratio, 'error': rel_error,
                'lhs_val': lhs_val, 'rhs_val': rhs_val,
            })

# Sort by error
results.sort(key=lambda x: x['error'])

# Count total search space
n_lhs = len(all_quantities)
n_rhs = len(all_quantities)
n_C = len(nice_constants)
n_total = n_lhs * n_rhs * n_C
print(f"\nSearch space: {n_lhs} LHS × {n_rhs} RHS × {n_C} constants = {n_total:,} trials")

# Count hits at various thresholds
for threshold in [0.005, 0.01, 0.02]:
    n_hits = sum(1 for r in results if r['error'] < threshold)
    print(f"  Hits within {threshold*100:.1f}%: {n_hits} ({n_hits/n_total*100:.2f}%)")

# ============================================================
# 4. Find our relation and its rank
# ============================================================
print("\n" + "=" * 60)
print("Top 20 relations (within 2%)")
print("=" * 60)

seen = set()
rank = 0
our_rank = None
for r in results:
    key = (r['lhs'], r['rhs'], r['C'])
    if key in seen:
        continue
    seen.add(key)
    rank += 1
    
    is_ours = ('ln(1/alpha_em' in r['lhs'] or '1/alpha_em' in r['lhs']) and \
              ('ln(m_P/m_p)' in r['rhs'] or 'ln(m_P/m_p)' in r['lhs'])
    marker = " <<<< OUR RELATION" if is_ours else ""
    
    if rank <= 20 or is_ours:
        print(f"  #{rank:3d} | {r['lhs']:30s} ≈ {r['C']:6s} × {r['rhs']:30s} | err={r['error']*100:.3f}%{marker}")
    
    if is_ours and our_rank is None:
        our_rank = rank

print(f"\nOur relation rank: #{our_rank} out of {len(seen)} unique relations within 2%")

# ============================================================
# 5. Monte Carlo: surrogate data
# ============================================================
print("\n" + "=" * 60)
print("Monte Carlo: Surrogate Data")
print("=" * 60)

n_mc = 10000
n_hits_mc = []
rng = np.random.default_rng(42)

# Null: randomize mass ratios and couplings
for trial in range(n_mc):
    # Random masses (log-uniform in 0.1 MeV to 10^19 GeV)
    rand_masses = 10**rng.uniform(-4, 19, len(masses))
    rand_couplings = 10**rng.uniform(-3, 0, len(couplings))
    rand_m_P = 10**rng.uniform(17, 21)
    
    # Build random catalog
    rand_quantities = {}
    for i, (name, _) in enumerate(masses.items()):
        lr = np.log(rand_m_P / rand_masses[i])
        rand_quantities.update(transforms(lr, f'ln(m_P/{name})'))
    for i, (name, _) in enumerate(couplings.items()):
        rand_quantities.update(transforms(rand_couplings[i], name))
    
    # Count hits
    hits = 0
    for (lhs_name, lhs_val), (rhs_name, rhs_val) in iterproduct(
        rand_quantities.items(), rand_quantities.items()
    ):
        if lhs_name == rhs_name: continue
        if abs(rhs_val) < 1e-10 or abs(lhs_val) < 1e-10: continue
        ratio = lhs_val / rhs_val
        if abs(ratio) < 0.01 or abs(ratio) > 100: continue
        for c_val in nice_constants.values():
            if abs(ratio / c_val - 1) < 0.009:  # within 0.9%
                hits += 1
                break
    n_hits_mc.append(hits)

n_hits_real = sum(1 for r in results if r['error'] < 0.009)
mean_mc = np.mean(n_hits_mc)
std_mc = np.std(n_hits_mc)
p_value = np.mean([h >= n_hits_real for h in n_hits_mc])

print(f"Real data: {n_hits_real} relations within 0.9%")
print(f"Monte Carlo ({n_mc} trials): {mean_mc:.1f} ± {std_mc:.1f}")
print(f"p-value (fraction of MC ≥ real): {p_value:.4f}")
print(f"Sigma: {(n_hits_real - mean_mc) / (std_mc + 1e-10):.1f}")

# ============================================================
# 6. RG / Mass sensitivity table
# ============================================================
print("\n" + "=" * 60)
print("Sensitivity to Mass Scale and Coupling")
print("=" * 60)

import warnings; warnings.filterwarnings('ignore')
hbar_c = 0.197327  # GeV·fm -> use natural units

G_obs = 6.67430e-11
hbar = 1.054571817e-34
c = 2.99792458e8
m_p_kg = 1.67262192e-27

print(f"\n{'Mass scale':<15} {'m [GeV]':>10} {'alpha_G':>12} {'(pi/2)ln(1/aG)':>16} {'1/alpha_em':>12} {'Discrepancy':>12}")
print("-" * 80)

for name, m_gev in [('m_e', m_e), ('m_mu', m_mu), ('m_pi', m_pi),
                     ('m_p', m_p), ('m_n', m_n), ('Lambda_QCD', Lambda_QCD),
                     ('m_tau', m_tau)]:
    m_kg = m_gev * 1.783e-27  # GeV to kg
    aG = G_obs * m_kg**2 / (hbar * c)
    lhs = np.pi/2 * np.log(1/aG)
    for alpha_name, alpha_val in [('alpha_em(0)', alpha_em_0)]:
        rhs = 1/alpha_val
        disc = (lhs - rhs) / rhs * 100
        print(f"{name:<15} {m_gev:10.4f} {aG:12.4e} {lhs:16.2f} {rhs:12.3f} {disc:+11.1f}%")

print(f"\n{'Coupling scale':<15} {'1/alpha':>10} {'(pi/2)ln(1/aG)':>16} {'Discrepancy':>12}")
print("-" * 55)
aG_proton = G_obs * m_p_kg**2 / (hbar * c)
lhs_proton = np.pi/2 * np.log(1/aG_proton)
for name, alpha_val in couplings.items():
    rhs = 1/alpha_val
    disc = (lhs_proton - rhs) / rhs * 100
    print(f"{name:<15} {rhs:10.3f} {lhs_proton:16.2f} {disc:+11.1f}%")

# ============================================================
# 7. Figure
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# (a) Histogram of MC hits
ax = axes[0]
ax.hist(n_hits_mc, bins=30, color='steelblue', alpha=0.7, density=True)
ax.axvline(n_hits_real, color='crimson', lw=2, ls='--', label=f'Real data: {n_hits_real}')
ax.axvline(mean_mc, color='gray', lw=1, ls=':', label=f'MC mean: {mean_mc:.1f}')
ax.set_xlabel('Number of 0.9%-level hits')
ax.set_ylabel('Density')
ax.set_title(f'(a) Look-elsewhere: p = {p_value:.3f}')
ax.legend(fontsize=9)

# (b) Mass sensitivity
ax = axes[1]
mass_names = ['m_e', 'm_mu', 'm_pi', 'm_p', 'm_n', 'Λ_QCD', 'm_tau']
mass_vals = [m_e, m_mu, m_pi, m_p, m_n, Lambda_QCD, m_tau]
discs = []
for m_gev in mass_vals:
    m_kg = m_gev * 1.783e-27
    aG = G_obs * m_kg**2 / (hbar * c)
    lhs = np.pi/2 * np.log(1/aG)
    discs.append((lhs - 137.036) / 137.036 * 100)

colors = ['gray']*3 + ['crimson'] + ['gray']*3
ax.barh(mass_names, discs, color=colors, alpha=0.7)
ax.axvline(0, color='green', ls='--', lw=1)
ax.set_xlabel('Discrepancy from 1/α_em (%)')
ax.set_title('(b) Mass scale sensitivity')

# (c) Coupling sensitivity
ax = axes[2]
coup_names = list(couplings.keys())
coup_discs = []
for alpha_val in couplings.values():
    rhs = 1/alpha_val
    coup_discs.append((lhs_proton - rhs) / rhs * 100)

ax.barh(coup_names, coup_discs, color='steelblue', alpha=0.7)
ax.axvline(0, color='green', ls='--', lw=1)
ax.set_xlabel('Discrepancy (%)')
ax.set_title('(c) Coupling scale sensitivity')

plt.tight_layout()
plt.savefig('fig4_statistical_analysis.png', dpi=150, bbox_inches='tight')
print("\nSaved: fig4_statistical_analysis.png")
plt.show()
