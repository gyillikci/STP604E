"""
Assignment 3 - Problem 1: Failure Criteria Analysis
STP 604E - Advanced Design, Analysis and Optimization of Composite Structures

Compare different failure criteria for a unidirectional lamina under combined loading.
Analyze Tsai-Wu, Tsai-Hill, Maximum Stress, and Maximum Strain criteria.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '/home/user/STP604E')

# Material Properties: T300/5208 Carbon/Epoxy
E1 = 181000  # MPa
E2 = 10300   # MPa
G12 = 7170   # MPa
nu12 = 0.28
nu21 = nu12 * E2 / E1

# Strength Properties (MPa)
Xt = 1500    # Longitudinal tensile strength
Xc = 1500    # Longitudinal compressive strength
Yt = 40      # Transverse tensile strength
Yc = 246     # Transverse compressive strength
S = 68       # In-plane shear strength

# Ultimate strains
eps1_t = Xt / E1   # Longitudinal tensile strain
eps1_c = Xc / E1   # Longitudinal compressive strain
eps2_t = Yt / E2   # Transverse tensile strain
eps2_c = Yc / E2   # Transverse compressive strain
gamma12_ult = S / G12  # Shear strain

print("=" * 70)
print("ASSIGNMENT 3 - PROBLEM 1: FAILURE CRITERIA COMPARISON")
print("=" * 70)
print("\nMaterial: T300/5208 Carbon/Epoxy")
print(f"E1 = {E1} MPa, E2 = {E2} MPa, G12 = {G12} MPa")
print(f"nu12 = {nu12}")
print("\nStrength Properties:")
print(f"Xt = {Xt} MPa, Xc = {Xc} MPa")
print(f"Yt = {Yt} MPa, Yc = {Yc} MPa")
print(f"S = {S} MPa")


def max_stress_criterion(sigma1, sigma2, tau12):
    """Maximum Stress Failure Criterion"""
    # Check each stress component independently
    f1 = sigma1 / Xt if sigma1 >= 0 else -sigma1 / Xc
    f2 = sigma2 / Yt if sigma2 >= 0 else -sigma2 / Yc
    f12 = abs(tau12) / S
    return max(f1, f2, f12)


def max_strain_criterion(sigma1, sigma2, tau12):
    """Maximum Strain Failure Criterion"""
    # Calculate strains
    eps1 = sigma1 / E1 - nu12 * sigma2 / E1
    eps2 = sigma2 / E2 - nu21 * sigma1 / E2
    gamma12 = tau12 / G12

    # Check each strain component
    f1 = eps1 / eps1_t if eps1 >= 0 else -eps1 / eps1_c
    f2 = eps2 / eps2_t if eps2 >= 0 else -eps2 / eps2_c
    f12 = abs(gamma12) / gamma12_ult
    return max(f1, f2, f12)


def tsai_hill_criterion(sigma1, sigma2, tau12):
    """Tsai-Hill Failure Criterion"""
    X = Xt if sigma1 >= 0 else Xc
    Y = Yt if sigma2 >= 0 else Yc

    FI = (sigma1/X)**2 - (sigma1*sigma2)/X**2 + (sigma2/Y)**2 + (tau12/S)**2
    return np.sqrt(FI) if FI > 0 else 0


def tsai_wu_criterion(sigma1, sigma2, tau12):
    """Tsai-Wu Failure Criterion"""
    # Tsai-Wu coefficients
    F1 = 1/Xt - 1/Xc
    F2 = 1/Yt - 1/Yc
    F11 = 1/(Xt * Xc)
    F22 = 1/(Yt * Yc)
    F66 = 1/S**2
    F12 = -0.5 * np.sqrt(F11 * F22)  # Interaction term (commonly used approximation)

    FI = (F1*sigma1 + F2*sigma2 +
          F11*sigma1**2 + F22*sigma2**2 + F66*tau12**2 +
          2*F12*sigma1*sigma2)
    return FI


# Generate failure envelopes in sigma1-sigma2 space (tau12 = 0)
n_points = 500
theta = np.linspace(0, 2*np.pi, n_points)

# Scale factors for plotting
sigma1_range = np.linspace(-1600, 1600, n_points)
sigma2_range = np.linspace(-300, 100, n_points)

# Find failure envelope points for each criterion
def find_envelope_point(criterion_func, angle, tau12=0):
    """Find the failure point along a given direction"""
    # Direction in stress space
    cos_a = np.cos(angle)
    sin_a = np.sin(angle)

    # Binary search for failure point
    r_low, r_high = 0, 3000
    for _ in range(50):
        r = (r_low + r_high) / 2
        sigma1 = r * cos_a
        sigma2 = r * sin_a * 0.2  # Scale sigma2 for visualization

        fi = criterion_func(sigma1, sigma2, tau12)
        if criterion_func == tsai_wu_criterion:
            if fi < 1:
                r_low = r
            else:
                r_high = r
        else:
            if fi < 1:
                r_low = r
            else:
                r_high = r

    return r * cos_a, r * sin_a * 0.2

# Generate envelope points
envelopes = {
    'Maximum Stress': [],
    'Maximum Strain': [],
    'Tsai-Hill': [],
    'Tsai-Wu': []
}

criteria = {
    'Maximum Stress': max_stress_criterion,
    'Maximum Strain': max_strain_criterion,
    'Tsai-Hill': tsai_hill_criterion,
    'Tsai-Wu': tsai_wu_criterion
}

for name, func in criteria.items():
    for angle in theta:
        s1, s2 = find_envelope_point(func, angle)
        envelopes[name].append((s1, s2))
    envelopes[name] = np.array(envelopes[name])

# Create figure with failure envelopes
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Sigma1-Sigma2 failure envelope (tau12 = 0)
ax1 = axes[0]
colors = {'Maximum Stress': 'blue', 'Maximum Strain': 'green',
          'Tsai-Hill': 'red', 'Tsai-Wu': 'purple'}

for name, envelope in envelopes.items():
    ax1.plot(envelope[:, 0], envelope[:, 1], label=name, color=colors[name], linewidth=2)

ax1.axhline(y=0, color='k', linewidth=0.5)
ax1.axvline(x=0, color='k', linewidth=0.5)
ax1.set_xlabel('σ₁ (MPa)', fontsize=12)
ax1.set_ylabel('σ₂ (MPa)', fontsize=12)
ax1.set_title('Failure Envelopes (τ₁₂ = 0)', fontsize=14)
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3)
ax1.set_xlim(-1700, 1700)
ax1.set_ylim(-300, 100)

# Plot 2: Sigma2-Tau12 failure envelope (sigma1 = 0)
ax2 = axes[1]
sigma2_vals = np.linspace(-250, 50, 100)
tau12_vals = np.linspace(-100, 100, 100)

for name, func in criteria.items():
    envelope_s2 = []
    envelope_tau = []

    for s2 in sigma2_vals:
        # Find max tau12 for this sigma2
        for tau in np.linspace(0, 100, 200):
            fi = func(0, s2, tau)
            target = 1
            if fi >= target:
                envelope_s2.append(s2)
                envelope_tau.append(tau)
                envelope_s2.append(s2)
                envelope_tau.append(-tau)
                break

    if envelope_s2:
        # Sort for proper plotting
        points = sorted(zip(envelope_s2, envelope_tau))
        s2_plot = [p[0] for p in points]
        tau_plot = [p[1] for p in points]
        ax2.scatter(s2_plot, tau_plot, label=name, color=colors[name], s=5, alpha=0.7)

ax2.axhline(y=0, color='k', linewidth=0.5)
ax2.axvline(x=0, color='k', linewidth=0.5)
ax2.set_xlabel('σ₂ (MPa)', fontsize=12)
ax2.set_ylabel('τ₁₂ (MPa)', fontsize=12)
ax2.set_title('Failure Envelopes (σ₁ = 0)', fontsize=14)
ax2.legend(loc='upper right')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/home/user/STP604E/assignment3_problem1_results.png', dpi=300, bbox_inches='tight')
print("\nFigure saved: assignment3_problem1_results.png")

# Test case analysis
print("\n" + "=" * 70)
print("TEST CASE ANALYSIS")
print("=" * 70)

test_cases = [
    (500, 20, 30, "Combined loading - moderate"),
    (1000, 0, 0, "Pure longitudinal tension"),
    (0, 30, 0, "Pure transverse tension"),
    (0, 0, 50, "Pure shear"),
    (-800, -100, 40, "Combined compression with shear"),
]

print("\n{:<40} {:>12} {:>12} {:>12} {:>12}".format(
    "Loading Case", "Max Stress", "Max Strain", "Tsai-Hill", "Tsai-Wu"))
print("-" * 90)

results_data = []
for sigma1, sigma2, tau12, desc in test_cases:
    ms = max_stress_criterion(sigma1, sigma2, tau12)
    mst = max_strain_criterion(sigma1, sigma2, tau12)
    th = tsai_hill_criterion(sigma1, sigma2, tau12)
    tw = tsai_wu_criterion(sigma1, sigma2, tau12)

    print(f"σ₁={sigma1:>5}, σ₂={sigma2:>4}, τ₁₂={tau12:>3} MPa   {ms:>12.4f} {mst:>12.4f} {th:>12.4f} {tw:>12.4f}")
    results_data.append({
        'case': desc,
        'sigma1': sigma1,
        'sigma2': sigma2,
        'tau12': tau12,
        'max_stress': ms,
        'max_strain': mst,
        'tsai_hill': th,
        'tsai_wu': tw
    })

print("\nNote: Failure Index (FI) >= 1 indicates failure")
print("=" * 70)

# Safety factor analysis
print("\n" + "=" * 70)
print("SAFETY FACTOR ANALYSIS")
print("=" * 70)
print("\nSafety Factor = 1 / Failure Index")
print("\n{:<40} {:>12} {:>12} {:>12} {:>12}".format(
    "Loading Case", "Max Stress", "Max Strain", "Tsai-Hill", "Tsai-Wu"))
print("-" * 90)

for data in results_data:
    sf_ms = 1/data['max_stress'] if data['max_stress'] > 0 else float('inf')
    sf_mst = 1/data['max_strain'] if data['max_strain'] > 0 else float('inf')
    sf_th = 1/data['tsai_hill'] if data['tsai_hill'] > 0 else float('inf')
    sf_tw = 1/data['tsai_wu'] if data['tsai_wu'] > 0 else float('inf')

    print(f"{data['case']:<40} {sf_ms:>12.2f} {sf_mst:>12.2f} {sf_th:>12.2f} {sf_tw:>12.2f}")

print("\nNote: Safety Factor > 1 means the lamina is safe under the given loading")
print("=" * 70)

plt.close()
