"""
Assignment 3 - Problem 4: 16-ply Laminate Design with Strain Constraints and Thermal Optimization
STP 604E - Advanced Design, Analysis and Optimization of Composite Structures

Design a 16-ply Zylon/Epoxy laminate with fiber angles limited to (0°,±30°,±60°,90°)
Subject to: σx = 250 MPa, σy = 50 MPa, τxy = 150 MPa
Strain limits: εx = 0.006, εy = 0.0006, γxy = 0.02

a) Find all stacking sequences satisfying strain limits
b) Find sequence with minimum |αx| (CTE)
c) Check ply strain limits
"""

import numpy as np
import matplotlib.pyplot as plt
from math import cos, sin, radians
from itertools import combinations_with_replacement, permutations

# Material Properties: Zylon/Epoxy
E1 = 120.0e3  # MPa (120 GPa)
E2 = 6.5e3    # MPa (6.5 GPa)
G12 = 3.0e3   # MPa (3.0 GPa)
nu12 = 0.32
nu21 = nu12 * E2 / E1
t_ply = 0.125  # mm (assumed standard ply thickness)

# Thermal expansion coefficients
alpha1 = -0.8e-6   # 1/°C (fiber direction)
alpha2 = 20.5e-6   # 1/°C (transverse direction)

# Applied stresses
sigma_x = 250  # MPa
sigma_y = 50   # MPa
tau_xy = 150   # MPa

# Strain limits (allowable)
eps_x_limit = 0.006
eps_y_limit = 0.0006
gamma_xy_limit = 0.02

# Available ply angles
available_angles = [0, 30, -30, 60, -60, 90]

# Number of plies
n_plies = 16

print("=" * 70)
print("ASSIGNMENT 3 - PROBLEM 4: 16-PLY LAMINATE DESIGN")
print("=" * 70)
print("\nMaterial: Zylon/Epoxy")
print(f"E1 = {E1/1000:.1f} GPa, E2 = {E2/1000:.1f} GPa, G12 = {G12/1000:.1f} GPa")
print(f"ν12 = {nu12}")
print(f"\nThermal Expansion Coefficients:")
print(f"α1 = {alpha1:.2e} /°C, α2 = {alpha2:.2e} /°C")
print(f"\nApplied Stresses:")
print(f"σx = {sigma_x} MPa, σy = {sigma_y} MPa, τxy = {tau_xy} MPa")
print(f"\nStrain Limits:")
print(f"εx_limit = {eps_x_limit}, εy_limit = {eps_y_limit}, γxy_limit = {gamma_xy_limit}")
print(f"\nAvailable angles: {available_angles}")
print(f"Number of plies: {n_plies}")


def Q_matrix():
    """Calculate reduced stiffness matrix Q"""
    Q = np.zeros((3, 3))
    denom = 1 - nu12 * nu21
    Q[0, 0] = E1 / denom
    Q[1, 1] = E2 / denom
    Q[0, 1] = Q[1, 0] = nu12 * E2 / denom
    Q[2, 2] = G12
    return Q


def Q_bar(Q, theta_deg):
    """Calculate transformed stiffness matrix Q-bar"""
    th = radians(theta_deg)
    m, n = cos(th), sin(th)

    Q11, Q22, Q12, Q66 = Q[0, 0], Q[1, 1], Q[0, 1], Q[2, 2]

    Qbar = np.zeros((3, 3))
    Qbar[0, 0] = Q11*m**4 + 2*(Q12 + 2*Q66)*m**2*n**2 + Q22*n**4
    Qbar[0, 1] = Qbar[1, 0] = (Q11 + Q22 - 4*Q66)*m**2*n**2 + Q12*(m**4 + n**4)
    Qbar[1, 1] = Q11*n**4 + 2*(Q12 + 2*Q66)*m**2*n**2 + Q22*m**4
    Qbar[0, 2] = Qbar[2, 0] = (Q11 - Q12 - 2*Q66)*m**3*n - (Q22 - Q12 - 2*Q66)*m*n**3
    Qbar[1, 2] = Qbar[2, 1] = (Q11 - Q12 - 2*Q66)*m*n**3 - (Q22 - Q12 - 2*Q66)*m**3*n
    Qbar[2, 2] = (Q11 + Q22 - 2*Q12 - 2*Q66)*m**2*n**2 + Q66*(m**4 + n**4 - 2*m**2*n**2)

    return Qbar


def transformed_alpha(theta_deg):
    """Calculate transformed thermal expansion coefficients"""
    th = radians(theta_deg)
    m, n = cos(th), sin(th)

    alpha_x = alpha1 * m**2 + alpha2 * n**2
    alpha_y = alpha1 * n**2 + alpha2 * m**2
    alpha_xy = 2 * (alpha1 - alpha2) * m * n

    return np.array([alpha_x, alpha_y, alpha_xy])


def transformation_matrix_strain(theta_deg):
    """Strain transformation matrix from global to local"""
    th = radians(theta_deg)
    m, n = cos(th), sin(th)

    T = np.array([
        [m**2, n**2, m*n],
        [n**2, m**2, -m*n],
        [-2*m*n, 2*m*n, m**2 - n**2]
    ])
    return T


def calculate_A_and_alpha(angle_counts):
    """
    Calculate A matrix and effective CTE for a laminate.
    angle_counts: dict with angle -> count
    """
    Q = Q_matrix()
    h = sum(angle_counts.values()) * t_ply

    A = np.zeros((3, 3))
    alpha_N = np.zeros(3)  # Thermal force contribution

    for angle, count in angle_counts.items():
        if count == 0:
            continue
        Qbar = Q_bar(Q, angle)
        alpha_bar = transformed_alpha(angle)
        thickness = count * t_ply

        A += Qbar * thickness
        alpha_N += Qbar @ alpha_bar * thickness

    # Effective CTE: α_eff = A^-1 @ alpha_N
    A_inv = np.linalg.inv(A)
    alpha_eff = A_inv @ alpha_N

    return A, alpha_eff, A_inv


def check_strain_limits(A_inv, h):
    """
    Check if laminate strains are within limits under applied stress.
    Strain = A_inv @ (stress * h)
    """
    stress = np.array([sigma_x, sigma_y, tau_xy])
    # N = stress * h (force per unit width)
    N = stress * h

    # Strain = A_inv @ N
    eps = A_inv @ N

    # Check limits
    eps_x_ok = abs(eps[0]) <= eps_x_limit
    eps_y_ok = abs(eps[1]) <= eps_y_limit
    gamma_xy_ok = abs(eps[2]) <= gamma_xy_limit

    return eps, eps_x_ok and eps_y_ok and gamma_xy_ok, (eps_x_ok, eps_y_ok, gamma_xy_ok)


# Generate all possible angle combinations for 16 plies
# Using lamination parameters approach for efficiency
# For symmetric balanced laminate: n0, n90, n_pm30, n_pm60

print("\n" + "=" * 70)
print("PART (a): FINDING VALID STACKING SEQUENCES")
print("=" * 70)

valid_sequences = []
Q = Q_matrix()

# For a 16-ply laminate with angles 0, ±30, ±60, 90
# We search over possible counts: n0, n90, n30 (pairs of +30/-30), n60 (pairs of +60/-60)
# Total: n0 + n90 + 2*n30 + 2*n60 = 16

print("\nSearching for valid combinations...")
print("(Considering symmetric balanced laminates for practical design)")

for n0 in range(0, 17, 2):  # Even numbers for symmetry
    for n90 in range(0, 17 - n0, 2):
        for n30_pairs in range(0, (17 - n0 - n90) // 2 + 1):
            n60_pairs = (16 - n0 - n90 - 2*n30_pairs) // 2
            if n60_pairs < 0 or n0 + n90 + 2*n30_pairs + 2*n60_pairs != 16:
                continue

            # Create angle counts
            angle_counts = {
                0: n0,
                90: n90,
                30: n30_pairs,
                -30: n30_pairs,
                60: n60_pairs,
                -60: n60_pairs
            }

            total_plies = sum(angle_counts.values())
            if total_plies != 16:
                continue

            h = total_plies * t_ply

            try:
                A, alpha_eff, A_inv = calculate_A_and_alpha(angle_counts)
                eps, valid, (ok_x, ok_y, ok_xy) = check_strain_limits(A_inv, h)

                if valid:
                    valid_sequences.append({
                        'angle_counts': angle_counts.copy(),
                        'n0': n0, 'n90': n90, 'n30_pairs': n30_pairs, 'n60_pairs': n60_pairs,
                        'A': A,
                        'A_inv': A_inv,
                        'alpha_eff': alpha_eff,
                        'strains': eps,
                        'alpha_x': alpha_eff[0]
                    })
            except:
                continue

print(f"\nFound {len(valid_sequences)} valid sequences satisfying strain limits.")

# Display valid sequences
print("\n" + "-" * 70)
print("VALID STACKING SEQUENCES:")
print("-" * 70)
print(f"{'#':>3} {'n0':>4} {'n90':>4} {'n±30':>5} {'n±60':>5} {'εx':>12} {'εy':>12} {'γxy':>12} {'αx (1/°C)':>14}")
print("-" * 70)

for i, seq in enumerate(valid_sequences[:20]):  # Show first 20
    print(f"{i+1:>3} {seq['n0']:>4} {seq['n90']:>4} {seq['n30_pairs']*2:>5} {seq['n60_pairs']*2:>5} "
          f"{seq['strains'][0]:>12.6f} {seq['strains'][1]:>12.6f} {seq['strains'][2]:>12.6f} "
          f"{seq['alpha_x']:>14.2e}")

if len(valid_sequences) > 20:
    print(f"... and {len(valid_sequences) - 20} more sequences")

# Part (b): Find minimum |αx|
print("\n" + "=" * 70)
print("PART (b): MINIMUM THERMAL EXPANSION COEFFICIENT")
print("=" * 70)

# Sort by |αx|
valid_sequences.sort(key=lambda x: abs(x['alpha_x']))

best_seq = valid_sequences[0]

print(f"\nOptimal sequence for minimum |αx|:")
print(f"  n0 = {best_seq['n0']}, n90 = {best_seq['n90']}")
print(f"  n±30 = {best_seq['n30_pairs']*2}, n±60 = {best_seq['n60_pairs']*2}")

# Construct actual stacking sequence
# For symmetric laminate: [half]s
half_seq = []
for _ in range(best_seq['n0'] // 2):
    half_seq.append(0)
for _ in range(best_seq['n30_pairs']):
    half_seq.append(30)
    half_seq.append(-30)
for _ in range(best_seq['n60_pairs']):
    half_seq.append(60)
    half_seq.append(-60)
for _ in range(best_seq['n90'] // 2):
    half_seq.append(90)

# Ensure half sequence has 8 plies
while len(half_seq) < 8:
    if best_seq['n0'] > 0:
        half_seq.append(0)
    elif best_seq['n90'] > 0:
        half_seq.append(90)

half_seq = half_seq[:8]  # Take first 8
full_seq = half_seq + half_seq[::-1]

print(f"\nExample stacking sequence: [{'/'.join(map(str, half_seq))}]s")
print(f"Full sequence: {full_seq}")

print(f"\nMid-plane strains under applied loading:")
print(f"  εx = {best_seq['strains'][0]:.6f} (limit: {eps_x_limit})")
print(f"  εy = {best_seq['strains'][1]:.6f} (limit: {eps_y_limit})")
print(f"  γxy = {best_seq['strains'][2]:.6f} (limit: {gamma_xy_limit})")

print(f"\nCoefficient of thermal expansion:")
print(f"  αx = {best_seq['alpha_x']:.4e} /°C")
print(f"  αy = {best_seq['alpha_eff'][1]:.4e} /°C")
print(f"  αxy = {best_seq['alpha_eff'][2]:.4e} /°C")

print(f"\n|αx| = {abs(best_seq['alpha_x']):.4e} /°C (minimized)")

# Part (c): Check ply strain limits
print("\n" + "=" * 70)
print("PART (c): PLY STRAIN FAILURE CHECK")
print("=" * 70)

eps_global = best_seq['strains']

print("\nAssuming ply strain limits are the same as laminate strain limits:")
print(f"  ε1_limit = {eps_x_limit}")
print(f"  ε2_limit = {eps_y_limit}")
print(f"  γ12_limit = {gamma_xy_limit}")

print("\n{:>6} {:>12} {:>12} {:>12} {:>10}".format(
    "Angle", "ε1", "ε2", "γ12", "Status"))
print("-" * 60)

ply_failure = []
unique_angles = set()
for angle in full_seq:
    if angle in unique_angles:
        continue
    unique_angles.add(angle)

    # Transform global strain to local
    T = transformation_matrix_strain(angle)
    eps_local = T @ eps_global

    # Check limits
    ok1 = abs(eps_local[0]) <= eps_x_limit
    ok2 = abs(eps_local[1]) <= eps_y_limit
    ok12 = abs(eps_local[2]) <= gamma_xy_limit

    status = "SAFE" if (ok1 and ok2 and ok12) else "FAIL"

    ply_failure.append({
        'angle': angle,
        'eps1': eps_local[0],
        'eps2': eps_local[1],
        'gamma12': eps_local[2],
        'status': status,
        'ok1': ok1, 'ok2': ok2, 'ok12': ok12
    })

    fail_comp = []
    if not ok1: fail_comp.append("ε1")
    if not ok2: fail_comp.append("ε2")
    if not ok12: fail_comp.append("γ12")

    print(f"{angle:>6}° {eps_local[0]:>12.6f} {eps_local[1]:>12.6f} {eps_local[2]:>12.6f} {status:>10}")
    if fail_comp:
        print(f"       → Exceeds limits: {', '.join(fail_comp)}")

# Summary
print("\n" + "-" * 70)
print("FAILURE SUMMARY:")
print("-" * 70)

failed_plies = [p for p in ply_failure if p['status'] == "FAIL"]
if failed_plies:
    print(f"\n⚠ FAILURE in {len(failed_plies)} ply orientation(s):")
    for f in failed_plies:
        print(f"  - {f['angle']}° ply: ε1={f['eps1']:.6f}, ε2={f['eps2']:.6f}, γ12={f['gamma12']:.6f}")
else:
    print("\n✓ All plies are within strain limits")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Valid sequences - αx distribution
ax1 = axes[0, 0]
alpha_x_values = [abs(s['alpha_x']) * 1e6 for s in valid_sequences]
ax1.hist(alpha_x_values, bins=20, color='steelblue', edgecolor='black', alpha=0.7)
ax1.axvline(x=abs(best_seq['alpha_x']) * 1e6, color='red', linewidth=2, linestyle='--',
           label=f'Minimum |αx| = {abs(best_seq["alpha_x"])*1e6:.2f}')
ax1.set_xlabel('|αx| (×10⁻⁶ /°C)', fontsize=12)
ax1.set_ylabel('Number of Valid Sequences', fontsize=12)
ax1.set_title('Distribution of |αx| for Valid Sequences', fontsize=14)
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Strain comparison
ax2 = axes[0, 1]
categories = ['εx', 'εy', 'γxy']
actual_strains = [abs(best_seq['strains'][i]) for i in range(3)]
limit_strains = [eps_x_limit, eps_y_limit, gamma_xy_limit]

x = np.arange(len(categories))
width = 0.35

bars1 = ax2.bar(x - width/2, actual_strains, width, label='Actual', color='coral', edgecolor='black')
bars2 = ax2.bar(x + width/2, limit_strains, width, label='Limit', color='steelblue', edgecolor='black')

ax2.set_ylabel('Strain', fontsize=12)
ax2.set_title('Laminate Strains vs. Limits', fontsize=14)
ax2.set_xticks(x)
ax2.set_xticklabels(categories)
ax2.legend()
ax2.grid(True, alpha=0.3, axis='y')

# Plot 3: Ply strains
ax3 = axes[1, 0]
angles_plot = [p['angle'] for p in ply_failure]
eps1_plot = [p['eps1'] for p in ply_failure]
eps2_plot = [p['eps2'] for p in ply_failure]
gamma12_plot = [p['gamma12'] for p in ply_failure]

x = np.arange(len(angles_plot))
width = 0.25

ax3.bar(x - width, eps1_plot, width, label='ε1', color='blue', alpha=0.7)
ax3.bar(x, eps2_plot, width, label='ε2', color='red', alpha=0.7)
ax3.bar(x + width, gamma12_plot, width, label='γ12', color='green', alpha=0.7)

ax3.axhline(y=eps_x_limit, color='blue', linestyle='--', linewidth=1, alpha=0.5)
ax3.axhline(y=eps_y_limit, color='red', linestyle='--', linewidth=1, alpha=0.5)
ax3.axhline(y=-eps_x_limit, color='blue', linestyle='--', linewidth=1, alpha=0.5)
ax3.axhline(y=-eps_y_limit, color='red', linestyle='--', linewidth=1, alpha=0.5)

ax3.set_xlabel('Ply Angle', fontsize=12)
ax3.set_ylabel('Strain', fontsize=12)
ax3.set_title('Local Ply Strains', fontsize=14)
ax3.set_xticks(x)
ax3.set_xticklabels([f'{a}°' for a in angles_plot])
ax3.legend()
ax3.grid(True, alpha=0.3)

# Plot 4: Optimal laminate visualization
ax4 = axes[1, 1]
h_total = 16 * t_ply
colors_map = {0: '#1f77b4', 30: '#ff7f0e', -30: '#2ca02c', 60: '#d62728', -60: '#9467bd', 90: '#8c564b'}

z_positions = np.linspace(-h_total/2, h_total/2, 17)

for i, theta in enumerate(full_seq):
    rect = plt.Rectangle((0, z_positions[i]), 4, t_ply,
                         facecolor=colors_map[theta], edgecolor='black', linewidth=0.3)
    ax4.add_patch(rect)

ax4.set_xlim(-0.5, 5.5)
ax4.set_ylim(-h_total/2 - 0.1, h_total/2 + 0.1)
ax4.set_aspect('equal')
seq_str = f"[{'/'.join(map(str, half_seq))}]s"
ax4.set_title(f'Optimal Laminate: {seq_str}\n|αx| = {abs(best_seq["alpha_x"])*1e6:.2f}×10⁻⁶/°C', fontsize=12)
ax4.set_xlabel('Width (arbitrary)', fontsize=12)
ax4.set_ylabel('z (mm)', fontsize=12)
ax4.axhline(y=0, color='k', linewidth=1, linestyle='--')

from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=colors_map[a], edgecolor='black', label=f'{a}°')
                  for a in sorted(colors_map.keys())]
ax4.legend(handles=legend_elements, loc='upper right', fontsize=8)

plt.tight_layout()
plt.savefig('/home/user/STP604E/assignment3_problem4_results.png', dpi=300, bbox_inches='tight')
print("\n" + "-" * 70)
print("Figure saved: assignment3_problem4_results.png")
print("=" * 70)

plt.close()

# Final summary
print("\n" + "=" * 70)
print("FINAL SUMMARY")
print("=" * 70)
print(f"\nOptimal 16-ply Zylon/Epoxy laminate:")
print(f"  Stacking sequence: {seq_str}")
print(f"  Full sequence: {full_seq}")
print(f"\nPly distribution:")
print(f"  0° plies: {best_seq['n0']}")
print(f"  90° plies: {best_seq['n90']}")
print(f"  ±30° plies: {best_seq['n30_pairs']*2}")
print(f"  ±60° plies: {best_seq['n60_pairs']*2}")
print(f"\nMid-plane strains: εx={best_seq['strains'][0]:.6f}, εy={best_seq['strains'][1]:.6f}, γxy={best_seq['strains'][2]:.6f}")
print(f"Thermal expansion: αx={best_seq['alpha_x']:.4e} /°C")
print("=" * 70)
