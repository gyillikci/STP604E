"""
Assignment 3 - Problem 2: Stacking Sequence Identification from Experiments
STP 604E - Advanced Design, Analysis and Optimization of Composite Structures

Determine the laminate stacking sequence from uniaxial tensile and three-point bending test results.
- Under uniaxial tensile load: no bending or shear observed
- Under bending load: only pure bending
- Elongation: 0.0897 mm at 2500 N
- Three-point bending slope: 0.0808 mm/N
- Plate: 150 mm × 30 mm × 2 mm
- Possible plies: 0°, ±45°, 90°
"""

import numpy as np
from math import cos, sin, radians
from itertools import combinations_with_replacement, permutations

# Material Properties
E1 = 181e3    # MPa (181 GPa)
E2 = 10.3e3   # MPa (10.3 GPa)
G12 = 7.17e3  # MPa (7.17 GPa)
nu12 = 0.28
nu21 = nu12 * E2 / E1
t_ply = 0.25  # mm

# Specimen dimensions
L = 150  # mm (length)
W = 30   # mm (width)
H = 2.0  # mm (thickness)

# Experimental results
delta_tension = 0.0897  # mm elongation
P_tension = 2500  # N load
slope_bending = 0.0808  # mm/N (displacement per unit load)

# Number of plies
n_plies = int(H / t_ply)  # 2/0.25 = 8 plies

print("=" * 70)
print("ASSIGNMENT 3 - PROBLEM 2: STACKING SEQUENCE IDENTIFICATION")
print("=" * 70)
print("\nMaterial Properties:")
print(f"E1 = {E1/1000:.0f} GPa, E2 = {E2/1000:.1f} GPa, G12 = {G12/1000:.2f} GPa")
print(f"ν12 = {nu12}, t_ply = {t_ply} mm")
print(f"\nSpecimen: {L} mm × {W} mm × {H} mm")
print(f"Number of plies: {n_plies}")
print("\nExperimental Observations:")
print("- Uniaxial tension: No bending, no shear coupling")
print("- Bending test: Pure bending (no twist)")
print(f"- Elongation at {P_tension} N: {delta_tension} mm")
print(f"- Bending slope: {slope_bending} mm/N")


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


def calculate_ABD(angles):
    """Calculate A, B, D matrices for a given stacking sequence"""
    Q = Q_matrix()
    n = len(angles)
    h_total = n * t_ply
    z = np.linspace(-h_total/2, h_total/2, n + 1)

    A = np.zeros((3, 3))
    B = np.zeros((3, 3))
    D = np.zeros((3, 3))

    for i, theta in enumerate(angles):
        Qbar = Q_bar(Q, theta)
        dz = z[i+1] - z[i]
        z_mid = (z[i+1] + z[i]) / 2
        A += Qbar * dz
        B += Qbar * dz * z_mid
        D += Qbar * (dz * z_mid**2 + dz**3 / 12)

    return A, B, D


def check_constraints(A, B, D):
    """
    Check experimental constraints:
    1. B = 0 (no bending-extension coupling) - symmetric laminate
    2. A16 = A26 = 0 (no shear-extension coupling) - balanced laminate
    3. D16 = D26 = 0 (no bend-twist coupling)
    """
    tol = 1e-6

    # Check B matrix is zero (symmetric)
    B_zero = np.allclose(B, 0, atol=tol * np.max(np.abs(A)))

    # Check A16, A26 are zero (balanced)
    A_balanced = abs(A[0, 2]) < tol * A[0, 0] and abs(A[1, 2]) < tol * A[0, 0]

    # Check D16, D26 are zero (no bend-twist)
    D_no_twist = abs(D[0, 2]) < tol * D[0, 0] and abs(D[1, 2]) < tol * D[0, 0]

    return B_zero, A_balanced, D_no_twist


def calculate_elongation(A, P, L, W):
    """
    Calculate elongation under uniaxial tensile load.
    delta = (N_x * L) / (A11_eff * W) where N_x = P / W
    For balanced laminate: eps_x = a11 * N_x where a = A^-1
    """
    A_inv = np.linalg.inv(A)
    a11 = A_inv[0, 0]

    # N_x = P / W (force per unit width)
    N_x = P / W

    # Strain: eps_x = a11 * N_x
    eps_x = a11 * N_x

    # Elongation: delta = eps_x * L
    delta = eps_x * L

    return delta


def calculate_bending_slope(D, L, W):
    """
    Calculate deflection per unit load for three-point bending.
    For simply supported beam with center load:
    delta/P = L³ / (48 * E * I) = L³ / (48 * D11_eff * W)

    Using effective bending stiffness from D matrix.
    """
    # For three-point bending of a composite beam
    # Deflection at center: delta = P * L³ / (48 * D11 * W)
    # Slope = delta/P = L³ / (48 * D11 * W)

    D11 = D[0, 0]
    slope = L**3 / (48 * D11 * W)

    return slope


# Analyze experimental constraints
print("\n" + "=" * 70)
print("ANALYSIS OF EXPERIMENTAL CONSTRAINTS")
print("=" * 70)

print("\nConstraint 1: No bending under uniaxial tension")
print("  → Laminate must be SYMMETRIC (B = 0)")

print("\nConstraint 2: No shear coupling under uniaxial tension")
print("  → Laminate must be BALANCED (A16 = A26 = 0)")
print("  → Equal number of +θ and -θ plies")

print("\nConstraint 3: Pure bending (no twist) under bending load")
print("  → D16 = D26 = 0")
print("  → Requires special symmetric arrangement of angle plies")

# Expected elongation and bending behavior
print("\n" + "-" * 70)
print("TARGET VALUES FROM EXPERIMENTS:")
print("-" * 70)
print(f"Target elongation at {P_tension} N: {delta_tension} mm")
print(f"Target bending slope: {slope_bending} mm/N")

# For a symmetric and balanced laminate with 8 plies, possible sequences
# using only 0°, ±45°, 90° are limited
# Symmetric: [θ1/θ2/θ3/θ4]s
# Balanced: equal +45 and -45 plies

# Possible half-laminate combinations (4 plies for symmetric)
possible_angles = [0, 45, -45, 90]

print("\n" + "=" * 70)
print("SEARCHING FOR MATCHING STACKING SEQUENCE")
print("=" * 70)

# Generate all symmetric laminates with balance constraint
# For symmetric [θ1/θ2/θ3/θ4]s, we need equal +45 and -45 in total laminate

matching_sequences = []

# Generate combinations for half-laminate (4 plies)
from itertools import product

all_half_sequences = list(product(possible_angles, repeat=4))

for half_seq in all_half_sequences:
    # Create full symmetric laminate
    full_seq = list(half_seq) + list(half_seq)[::-1]

    # Check balance (equal +45 and -45)
    count_plus45 = full_seq.count(45)
    count_minus45 = full_seq.count(-45)

    if count_plus45 != count_minus45:
        continue

    # Calculate ABD matrices
    A, B, D = calculate_ABD(full_seq)

    # Check constraints
    B_zero, A_balanced, D_no_twist = check_constraints(A, B, D)

    if not (B_zero and A_balanced and D_no_twist):
        continue

    # Calculate predicted elongation and bending slope
    pred_elongation = calculate_elongation(A, P_tension, L, W)
    pred_slope = calculate_bending_slope(D, L, W)

    # Check if matches experimental values (within tolerance)
    elong_error = abs(pred_elongation - delta_tension) / delta_tension * 100
    slope_error = abs(pred_slope - slope_bending) / slope_bending * 100

    if elong_error < 5 and slope_error < 5:  # Within 5% tolerance
        matching_sequences.append({
            'sequence': full_seq,
            'half_seq': half_seq,
            'elongation': pred_elongation,
            'slope': pred_slope,
            'elong_error': elong_error,
            'slope_error': slope_error,
            'A': A,
            'D': D
        })

# Sort by combined error
matching_sequences.sort(key=lambda x: x['elong_error'] + x['slope_error'])

print(f"\nFound {len(matching_sequences)} matching sequences:")
print("-" * 70)

for i, match in enumerate(matching_sequences[:5]):  # Show top 5
    half = match['half_seq']
    seq_str = f"[{half[0]}/{half[1]}/{half[2]}/{half[3]}]s"
    print(f"\n{i+1}. {seq_str}")
    print(f"   Full sequence: {match['sequence']}")
    print(f"   Predicted elongation: {match['elongation']:.4f} mm (error: {match['elong_error']:.2f}%)")
    print(f"   Predicted bending slope: {match['slope']:.4f} mm/N (error: {match['slope_error']:.2f}%)")

if matching_sequences:
    best_match = matching_sequences[0]
    print("\n" + "=" * 70)
    print("IDENTIFIED STACKING SEQUENCE")
    print("=" * 70)

    half = best_match['half_seq']
    seq_str = f"[{half[0]}/{half[1]}/{half[2]}/{half[3]}]s"

    print(f"\nBest match: {seq_str}")
    print(f"Full sequence: {best_match['sequence']}")

    print("\n" + "-" * 70)
    print("VERIFICATION:")
    print("-" * 70)
    print(f"\nElongation at {P_tension} N:")
    print(f"  Experimental: {delta_tension} mm")
    print(f"  Calculated:   {best_match['elongation']:.4f} mm")
    print(f"  Error:        {best_match['elong_error']:.2f}%")

    print(f"\nBending slope (deflection/force):")
    print(f"  Experimental: {slope_bending} mm/N")
    print(f"  Calculated:   {best_match['slope']:.4f} mm/N")
    print(f"  Error:        {best_match['slope_error']:.2f}%")

    print("\n" + "-" * 70)
    print("STIFFNESS MATRICES:")
    print("-" * 70)

    print("\nA-Matrix (Extensional Stiffness) [N/mm]:")
    print(np.array2string(best_match['A'], precision=1, suppress_small=True))

    print("\nD-Matrix (Bending Stiffness) [N-mm]:")
    print(np.array2string(best_match['D'], precision=1, suppress_small=True))

    # Calculate effective properties
    A = best_match['A']
    A_inv = np.linalg.inv(A)
    h = H

    Ex_eff = 1 / (h * A_inv[0, 0])
    Ey_eff = 1 / (h * A_inv[1, 1])

    print("\n" + "-" * 70)
    print("EFFECTIVE LAMINATE PROPERTIES:")
    print("-" * 70)
    print(f"Effective Ex = {Ex_eff/1000:.2f} GPa")
    print(f"Effective Ey = {Ey_eff/1000:.2f} GPa")

else:
    print("\nNo exact match found. Showing closest candidates...")
    # Show sequences with larger tolerance
    all_candidates = []
    for half_seq in all_half_sequences:
        full_seq = list(half_seq) + list(half_seq)[::-1]
        count_plus45 = full_seq.count(45)
        count_minus45 = full_seq.count(-45)
        if count_plus45 != count_minus45:
            continue
        A, B, D = calculate_ABD(full_seq)
        B_zero, A_balanced, D_no_twist = check_constraints(A, B, D)
        if not (B_zero and A_balanced):
            continue
        pred_elongation = calculate_elongation(A, P_tension, L, W)
        pred_slope = calculate_bending_slope(D, L, W)
        elong_error = abs(pred_elongation - delta_tension) / delta_tension * 100
        slope_error = abs(pred_slope - slope_bending) / slope_bending * 100
        all_candidates.append({
            'half_seq': half_seq,
            'full_seq': full_seq,
            'elongation': pred_elongation,
            'slope': pred_slope,
            'elong_error': elong_error,
            'slope_error': slope_error
        })

    all_candidates.sort(key=lambda x: x['elong_error'] + x['slope_error'])
    for i, cand in enumerate(all_candidates[:10]):
        half = cand['half_seq']
        print(f"\n{i+1}. [{half[0]}/{half[1]}/{half[2]}/{half[3]}]s")
        print(f"   Elong: {cand['elongation']:.4f} mm ({cand['elong_error']:.1f}%)")
        print(f"   Slope: {cand['slope']:.4f} mm/N ({cand['slope_error']:.1f}%)")

# Create visualization
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Show the identified laminate
ax1 = axes[0]
if matching_sequences:
    best_seq = matching_sequences[0]['sequence']
else:
    best_seq = all_candidates[0]['full_seq'] if all_candidates else [0, 45, -45, 90, 90, -45, 45, 0]

colors_map = {0: '#1f77b4', 45: '#ff7f0e', -45: '#2ca02c', 90: '#d62728'}
h_total = len(best_seq) * t_ply

for i, theta in enumerate(best_seq):
    rect = plt.Rectangle((0, i * t_ply - h_total/2), 4, t_ply,
                         facecolor=colors_map[theta], edgecolor='black', linewidth=0.5)
    ax1.add_patch(rect)
    ax1.text(4.3, (i + 0.5) * t_ply - h_total/2, f'{theta}°', va='center', fontsize=10)

ax1.set_xlim(-0.5, 5.5)
ax1.set_ylim(-h_total/2 - 0.2, h_total/2 + 0.2)
ax1.set_aspect('equal')
half = best_seq[:4]
ax1.set_title(f'Identified Laminate: [{half[0]}/{half[1]}/{half[2]}/{half[3]}]s', fontsize=14)
ax1.set_xlabel('Width (arbitrary)', fontsize=12)
ax1.set_ylabel('z (mm)', fontsize=12)
ax1.axhline(y=0, color='k', linewidth=1, linestyle='--')

from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=colors_map[a], edgecolor='black', label=f'{a}°') for a in [0, 45, -45, 90]]
ax1.legend(handles=legend_elements, loc='upper right')

# Plot 2: Show comparison of experimental vs predicted
ax2 = axes[1]
categories = ['Elongation\n(mm)', 'Bending Slope\n(mm/N)']
exp_values = [delta_tension, slope_bending]

if matching_sequences:
    pred_values = [matching_sequences[0]['elongation'], matching_sequences[0]['slope']]
elif all_candidates:
    pred_values = [all_candidates[0]['elongation'], all_candidates[0]['slope']]
else:
    pred_values = [0, 0]

x = np.arange(len(categories))
width = 0.35

bars1 = ax2.bar(x - width/2, exp_values, width, label='Experimental', color='steelblue', edgecolor='black')
bars2 = ax2.bar(x + width/2, pred_values, width, label='Predicted', color='coral', edgecolor='black')

ax2.set_ylabel('Value', fontsize=12)
ax2.set_title('Experimental vs Predicted Values', fontsize=14)
ax2.set_xticks(x)
ax2.set_xticklabels(categories)
ax2.legend()
ax2.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bar, val in zip(bars1, exp_values):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.002,
             f'{val:.4f}', ha='center', va='bottom', fontsize=10)
for bar, val in zip(bars2, pred_values):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.002,
             f'{val:.4f}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig('/home/user/STP604E/assignment3_problem2_results.png', dpi=300, bbox_inches='tight')
print("\n" + "-" * 70)
print("Figure saved: assignment3_problem2_results.png")
print("=" * 70)

plt.close()
