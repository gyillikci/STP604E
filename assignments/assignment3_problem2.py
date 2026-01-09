"""
Assignment 3 - Problem 2: First Ply Failure (FPF) Analysis
STP 604E - Advanced Design, Analysis and Optimization of Composite Structures

Determine the First Ply Failure load for a [0/45/-45/90]s laminate under uniaxial loading.
Compare FPF predictions using different failure criteria.
"""

import numpy as np
import matplotlib.pyplot as plt
from math import cos, sin, radians
import sys
sys.path.insert(0, '/home/user/STP604E')

# Material Properties: AS4/3501-6 Carbon/Epoxy
E1 = 142000  # MPa
E2 = 10300   # MPa
G12 = 7200   # MPa
nu12 = 0.27
nu21 = nu12 * E2 / E1
t_ply = 0.125  # mm (ply thickness)

# Strength Properties (MPa)
Xt = 2280    # Longitudinal tensile strength
Xc = 1440    # Longitudinal compressive strength
Yt = 57      # Transverse tensile strength
Yc = 228     # Transverse compressive strength
S = 71       # In-plane shear strength

print("=" * 70)
print("ASSIGNMENT 3 - PROBLEM 2: FIRST PLY FAILURE ANALYSIS")
print("=" * 70)
print("\nMaterial: AS4/3501-6 Carbon/Epoxy")
print(f"E1 = {E1} MPa, E2 = {E2} MPa, G12 = {G12} MPa")
print(f"nu12 = {nu12}, t_ply = {t_ply} mm")
print("\nStrength Properties:")
print(f"Xt = {Xt} MPa, Xc = {Xc} MPa")
print(f"Yt = {Yt} MPa, Yc = {Yc} MPa")
print(f"S = {S} MPa")

# Laminate configuration: [0/45/-45/90]s
angles = [0, 45, -45, 90, 90, -45, 45, 0]
n_plies = len(angles)
h_total = n_plies * t_ply  # Total laminate thickness

print(f"\nLaminate: [0/45/-45/90]s")
print(f"Number of plies: {n_plies}")
print(f"Total thickness: {h_total} mm")


def Q_matrix(E1, E2, G12, nu12):
    """Calculate reduced stiffness matrix Q"""
    nu21 = nu12 * E2 / E1
    Q = np.zeros((3, 3))
    Q[0, 0] = E1 / (1 - nu12 * nu21)
    Q[1, 1] = E2 / (1 - nu12 * nu21)
    Q[0, 1] = Q[1, 0] = nu12 * E2 / (1 - nu12 * nu21)
    Q[2, 2] = G12
    return Q


def Q_bar(Q, theta_deg):
    """Calculate transformed stiffness matrix Q-bar"""
    th = radians(theta_deg)
    m, n = cos(th), sin(th)

    Q11, Q22, Q12, Q66 = Q[0, 0], Q[1, 1], Q[0, 1], Q[2, 2]

    Qbar = np.zeros((3, 3))
    Qbar[0, 0] = Q11*m**4 + 2*(Q12+2*Q66)*m**2*n**2 + Q22*n**4
    Qbar[0, 1] = Qbar[1, 0] = (Q11+Q22-4*Q66)*m**2*n**2 + Q12*(m**4 + n**4)
    Qbar[1, 1] = Q11*n**4 + 2*(Q12+2*Q66)*m**2*n**2 + Q22*m**4
    Qbar[0, 2] = Qbar[2, 0] = (Q11 - Q12 - 2*Q66)*m**3*n - (Q22 - Q12 - 2*Q66)*m*n**3
    Qbar[1, 2] = Qbar[2, 1] = (Q11 - Q12 - 2*Q66)*m*n**3 - (Q22 - Q12 - 2*Q66)*m**3*n
    Qbar[2, 2] = (Q11 + Q22 - 2*Q12 - 2*Q66)*m**2*n**2 + Q66*(m**4 + n**4 - 2*m**2*n**2)

    return Qbar


def transformation_matrix(theta_deg):
    """Stress transformation matrix from global to local coordinates"""
    th = radians(theta_deg)
    m, n = cos(th), sin(th)

    T = np.array([
        [m**2, n**2, 2*m*n],
        [n**2, m**2, -2*m*n],
        [-m*n, m*n, m**2 - n**2]
    ])
    return T


def tsai_wu_fi(sigma1, sigma2, tau12):
    """Calculate Tsai-Wu failure index"""
    F1 = 1/Xt - 1/Xc
    F2 = 1/Yt - 1/Yc
    F11 = 1/(Xt * Xc)
    F22 = 1/(Yt * Yc)
    F66 = 1/S**2
    F12 = -0.5 * np.sqrt(F11 * F22)

    FI = (F1*sigma1 + F2*sigma2 +
          F11*sigma1**2 + F22*sigma2**2 + F66*tau12**2 +
          2*F12*sigma1*sigma2)
    return FI


def tsai_hill_fi(sigma1, sigma2, tau12):
    """Calculate Tsai-Hill failure index"""
    X = Xt if sigma1 >= 0 else Xc
    Y = Yt if sigma2 >= 0 else Yc
    FI = (sigma1/X)**2 - (sigma1*sigma2)/X**2 + (sigma2/Y)**2 + (tau12/S)**2
    return FI


def max_stress_fi(sigma1, sigma2, tau12):
    """Calculate Maximum Stress failure index"""
    f1 = sigma1/Xt if sigma1 >= 0 else -sigma1/Xc
    f2 = sigma2/Yt if sigma2 >= 0 else -sigma2/Yc
    f12 = abs(tau12)/S
    return max(f1, f2, f12)


# Calculate Q matrix
Q = Q_matrix(E1, E2, G12, nu12)

# Calculate ABD matrices
z = np.linspace(-h_total/2, h_total/2, n_plies + 1)

A = np.zeros((3, 3))
B = np.zeros((3, 3))
D = np.zeros((3, 3))

Qbar_list = []
for i, theta in enumerate(angles):
    Qbar = Q_bar(Q, theta)
    Qbar_list.append(Qbar)
    dz = z[i+1] - z[i]
    z_mid = (z[i+1] + z[i]) / 2
    A += Qbar * dz
    B += Qbar * dz * z_mid
    D += Qbar * (dz * z_mid**2 + dz**3 / 12)

print("\n" + "-" * 70)
print("A-Matrix (Extensional Stiffness) [N/mm]:")
print(np.array2string(A, precision=1, suppress_small=True))
print("\nB-Matrix (Coupling Stiffness) [N]:")
print(np.array2string(B, precision=1, suppress_small=True))
print("\nD-Matrix (Bending Stiffness) [N-mm]:")
print(np.array2string(D, precision=1, suppress_small=True))

# Apply unit load Nx = 1 N/mm (uniaxial tension)
# For symmetric laminate, B = 0, so we only need A-inverse
A_inv = np.linalg.inv(A)

# Mid-plane strains for unit load
epsilon_0 = A_inv @ np.array([1, 0, 0])  # [eps_x, eps_y, gamma_xy] for Nx = 1 N/mm

print("\n" + "-" * 70)
print("Mid-plane strains for Nx = 1 N/mm:")
print(f"  ε_x⁰ = {epsilon_0[0]:.6e}")
print(f"  ε_y⁰ = {epsilon_0[1]:.6e}")
print(f"  γ_xy⁰ = {epsilon_0[2]:.6e}")

# Calculate ply stresses in material coordinates for unit load
print("\n" + "-" * 70)
print("PLY-BY-PLY STRESS ANALYSIS (for Nx = 1 N/mm)")
print("-" * 70)
print(f"{'Ply':>4} {'Angle':>8} {'σ₁':>12} {'σ₂':>12} {'τ₁₂':>12} {'Tsai-Wu':>10} {'Tsai-Hill':>10} {'Max Stress':>10}")
print(f"{'':>4} {'(deg)':>8} {'(MPa)':>12} {'(MPa)':>12} {'(MPa)':>12} {'FI':>10} {'FI':>10} {'FI':>10}")
print("-" * 90)

ply_stresses = []
ply_fi = {'Tsai-Wu': [], 'Tsai-Hill': [], 'Max Stress': []}

for i, theta in enumerate(angles):
    # Global stresses (for unit load, stress = Q_bar * strain)
    Qbar = Qbar_list[i]
    sigma_global = Qbar @ epsilon_0

    # Transform to material coordinates
    T = transformation_matrix(theta)
    sigma_local = T @ sigma_global
    sigma1, sigma2, tau12 = sigma_local

    # Calculate failure indices
    fi_tw = tsai_wu_fi(sigma1, sigma2, tau12)
    fi_th = tsai_hill_fi(sigma1, sigma2, tau12)
    fi_ms = max_stress_fi(sigma1, sigma2, tau12)

    ply_stresses.append((sigma1, sigma2, tau12))
    ply_fi['Tsai-Wu'].append(fi_tw)
    ply_fi['Tsai-Hill'].append(fi_th)
    ply_fi['Max Stress'].append(fi_ms)

    print(f"{i+1:>4} {theta:>8} {sigma1:>12.4f} {sigma2:>12.4f} {tau12:>12.4f} {fi_tw:>10.6f} {fi_th:>10.6f} {fi_ms:>10.6f}")

# Find First Ply Failure load
print("\n" + "=" * 70)
print("FIRST PLY FAILURE (FPF) RESULTS")
print("=" * 70)

fpf_results = {}
for criterion, fi_list in ply_fi.items():
    max_fi = max(fi_list)
    critical_ply = fi_list.index(max_fi) + 1
    critical_angle = angles[critical_ply - 1]

    # FPF load = 1 / sqrt(max_fi) for quadratic criteria, 1/max_fi for linear
    if criterion in ['Tsai-Wu', 'Tsai-Hill']:
        fpf_load = 1 / np.sqrt(max_fi) if max_fi > 0 else float('inf')
    else:
        fpf_load = 1 / max_fi if max_fi > 0 else float('inf')

    fpf_results[criterion] = {
        'load': fpf_load,
        'critical_ply': critical_ply,
        'critical_angle': critical_angle,
        'max_fi': max_fi
    }

    print(f"\n{criterion}:")
    print(f"  Critical Ply: {critical_ply} ({critical_angle}° ply)")
    print(f"  Failure Index at unit load: {max_fi:.6f}")
    print(f"  First Ply Failure Load: Nx = {fpf_load:.2f} N/mm")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Failure indices by ply
ax1 = axes[0, 0]
x = np.arange(1, n_plies + 1)
width = 0.25
ax1.bar(x - width, ply_fi['Tsai-Wu'], width, label='Tsai-Wu', color='purple', alpha=0.8)
ax1.bar(x, ply_fi['Tsai-Hill'], width, label='Tsai-Hill', color='red', alpha=0.8)
ax1.bar(x + width, ply_fi['Max Stress'], width, label='Max Stress', color='blue', alpha=0.8)
ax1.set_xlabel('Ply Number', fontsize=12)
ax1.set_ylabel('Failure Index (for Nx = 1 N/mm)', fontsize=12)
ax1.set_title('Failure Index by Ply (Unit Load)', fontsize=14)
ax1.set_xticks(x)
ax1.set_xticklabels([f'{i}\n({angles[i-1]}°)' for i in x])
ax1.legend()
ax1.grid(True, alpha=0.3, axis='y')

# Plot 2: FPF loads comparison
ax2 = axes[0, 1]
criteria_names = list(fpf_results.keys())
fpf_loads = [fpf_results[c]['load'] for c in criteria_names]
colors = ['purple', 'red', 'blue']
bars = ax2.bar(criteria_names, fpf_loads, color=colors, alpha=0.8, edgecolor='black')
ax2.set_ylabel('First Ply Failure Load Nx (N/mm)', fontsize=12)
ax2.set_title('FPF Load Comparison by Criterion', fontsize=14)
ax2.grid(True, alpha=0.3, axis='y')
for bar, load in zip(bars, fpf_loads):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
             f'{load:.1f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

# Plot 3: Ply stresses distribution
ax3 = axes[1, 0]
sigma1_vals = [s[0] for s in ply_stresses]
sigma2_vals = [s[1] for s in ply_stresses]
tau12_vals = [s[2] for s in ply_stresses]

ax3.plot(x, sigma1_vals, 'o-', label='σ₁', linewidth=2, markersize=8)
ax3.plot(x, sigma2_vals, 's-', label='σ₂', linewidth=2, markersize=8)
ax3.plot(x, tau12_vals, '^-', label='τ₁₂', linewidth=2, markersize=8)
ax3.set_xlabel('Ply Number', fontsize=12)
ax3.set_ylabel('Stress (MPa) for Nx = 1 N/mm', fontsize=12)
ax3.set_title('Ply Stresses in Material Coordinates', fontsize=14)
ax3.set_xticks(x)
ax3.set_xticklabels([f'{i}\n({angles[i-1]}°)' for i in x])
ax3.legend()
ax3.grid(True, alpha=0.3)
ax3.axhline(y=0, color='k', linewidth=0.5)

# Plot 4: Laminate stacking sequence visualization
ax4 = axes[1, 1]
colors_ply = {0: '#1f77b4', 45: '#ff7f0e', -45: '#2ca02c', 90: '#d62728'}
for i, theta in enumerate(angles):
    rect = plt.Rectangle((0, i * t_ply - h_total/2), 4, t_ply,
                         facecolor=colors_ply[theta], edgecolor='black', linewidth=1)
    ax4.add_patch(rect)
    ax4.text(4.2, (i + 0.5) * t_ply - h_total/2, f'{theta}°', va='center', fontsize=11)
    ax4.text(-0.5, (i + 0.5) * t_ply - h_total/2, f'Ply {i+1}', va='center', ha='right', fontsize=10)

ax4.set_xlim(-1, 5)
ax4.set_ylim(-h_total/2 - 0.1, h_total/2 + 0.1)
ax4.set_aspect('equal')
ax4.set_title('[0/45/-45/90]s Laminate Stack', fontsize=14)
ax4.set_xlabel('Width (arbitrary units)', fontsize=12)
ax4.set_ylabel('z (mm)', fontsize=12)
ax4.axhline(y=0, color='k', linewidth=0.5, linestyle='--', label='Mid-plane')

# Add legend for ply angles
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=colors_ply[a], edgecolor='black', label=f'{a}°') for a in [0, 45, -45, 90]]
ax4.legend(handles=legend_elements, loc='upper right')

plt.tight_layout()
plt.savefig('/home/user/STP604E/assignment3_problem2_results.png', dpi=300, bbox_inches='tight')
print("\n" + "-" * 70)
print("Figure saved: assignment3_problem2_results.png")
print("=" * 70)

plt.close()
