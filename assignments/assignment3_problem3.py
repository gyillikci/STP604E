"""
Assignment 3 - Problem 3: Unsymmetric Laminate Analysis with Tsai-Hill
STP 604E - Advanced Design, Analysis and Optimization of Composite Structures

Analyze [30/45/-45/-30]T Kevlar/Epoxy laminate under combined loading:
Nx = Ny = 1000 N/m, My = Mxy = 50 N

a) Determine mid-plane strains and curvatures
b) Find global stresses and plot vs vertical location
c) Check Tsai-Hill failure criterion for each layer
"""

import numpy as np
import matplotlib.pyplot as plt
from math import cos, sin, radians

# Material Properties: Kevlar/Epoxy
E1 = 76e3     # MPa (76 GPa)
E2 = 5.50e3   # MPa (5.50 GPa)
G12 = 2.30e3  # MPa (2.30 GPa)
nu12 = 0.34
nu21 = nu12 * E2 / E1
t_ply = 1.25  # mm

# Strength Properties (MPa)
Xt = 1400     # Longitudinal tensile strength
Xc = 235      # Longitudinal compressive strength
Yt = 53       # Transverse tensile strength
Yc = 12       # Transverse compressive strength (Note: very low!)
S = 34        # In-plane shear strength

# Applied loads
Nx = 1000 / 1000  # N/m = 1 N/mm (convert to consistent units)
Ny = 1000 / 1000  # N/mm
Nxy = 0           # N/mm
Mx = 0            # N (Note: moments given in N, not N-mm/mm)
My = 50           # N
Mxy = 50          # N

print("=" * 70)
print("ASSIGNMENT 3 - PROBLEM 3: UNSYMMETRIC LAMINATE ANALYSIS")
print("=" * 70)
print("\nMaterial: Kevlar/Epoxy")
print(f"E1 = {E1/1000:.0f} GPa, E2 = {E2/1000:.2f} GPa, G12 = {G12/1000:.2f} GPa")
print(f"ν12 = {nu12}, t = {t_ply} mm")
print("\nStrength Properties:")
print(f"Xt = {Xt} MPa, Xc = {Xc} MPa")
print(f"Yt = {Yt} MPa, Yc = {Yc} MPa")
print(f"S = {S} MPa")

# Laminate stacking sequence: [30/45/-45/-30]T (non-symmetric!)
angles = [30, 45, -45, -30]
n_plies = len(angles)
h_total = n_plies * t_ply

print(f"\nLaminate: [30/45/-45/-30]T (Total laminate, not symmetric)")
print(f"Number of plies: {n_plies}")
print(f"Total thickness: {h_total} mm")
print(f"\nApplied Loads:")
print(f"Nx = {Nx*1000:.0f} N/m = {Nx:.3f} N/mm")
print(f"Ny = {Ny*1000:.0f} N/m = {Ny:.3f} N/mm")
print(f"Nxy = {Nxy} N/mm")
print(f"Mx = {Mx} N")
print(f"My = {My} N")
print(f"Mxy = {Mxy} N")


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


def stress_transformation(theta_deg):
    """Stress transformation matrix from global to local coordinates"""
    th = radians(theta_deg)
    m, n = cos(th), sin(th)

    T = np.array([
        [m**2, n**2, 2*m*n],
        [n**2, m**2, -2*m*n],
        [-m*n, m*n, m**2 - n**2]
    ])
    return T


# Calculate Q matrix
Q = Q_matrix()

print("\n" + "-" * 70)
print("Q-Matrix (Reduced Stiffness) [MPa]:")
print(np.array2string(Q, precision=1, suppress_small=True))

# Calculate ABD matrices
# z coordinates: bottom of laminate to top
z = []
z_current = -h_total / 2
for i in range(n_plies + 1):
    z.append(z_current)
    if i < n_plies:
        z_current += t_ply

z = np.array(z)

print(f"\nPly z-coordinates (mm): {z}")

A = np.zeros((3, 3))
B = np.zeros((3, 3))
D = np.zeros((3, 3))

Qbar_list = []

for i, theta in enumerate(angles):
    Qbar = Q_bar(Q, theta)
    Qbar_list.append(Qbar)

    z_bot = z[i]
    z_top = z[i + 1]

    A += Qbar * (z_top - z_bot)
    B += 0.5 * Qbar * (z_top**2 - z_bot**2)
    D += (1/3) * Qbar * (z_top**3 - z_bot**3)

print("\n" + "-" * 70)
print("A-Matrix (Extensional Stiffness) [N/mm]:")
print(np.array2string(A, precision=1, suppress_small=True))

print("\nB-Matrix (Coupling Stiffness) [N]:")
print(np.array2string(B, precision=2, suppress_small=True))
print("Note: B ≠ 0 because laminate is unsymmetric!")

print("\nD-Matrix (Bending Stiffness) [N-mm]:")
print(np.array2string(D, precision=1, suppress_small=True))

# Assemble ABD matrix
ABD = np.block([[A, B], [B, D]])

print("\n" + "-" * 70)
print("ABD Matrix:")
print(np.array2string(ABD, precision=2, suppress_small=True))

# Load vector [N, M]
NM = np.array([Nx, Ny, Nxy, Mx, My, Mxy])

print("\n" + "-" * 70)
print("Load Vector [Nx, Ny, Nxy, Mx, My, Mxy]:")
print(NM)

# Solve for mid-plane strains and curvatures
ABD_inv = np.linalg.inv(ABD)
eps_kappa = ABD_inv @ NM

eps0 = eps_kappa[:3]  # Mid-plane strains [eps_x0, eps_y0, gamma_xy0]
kappa = eps_kappa[3:]  # Curvatures [kappa_x, kappa_y, kappa_xy]

print("\n" + "=" * 70)
print("PART (a): MID-PLANE STRAINS AND CURVATURES")
print("=" * 70)

print("\nMid-plane strains:")
print(f"  ε_x⁰ = {eps0[0]:.6e}")
print(f"  ε_y⁰ = {eps0[1]:.6e}")
print(f"  γ_xy⁰ = {eps0[2]:.6e}")

print("\nCurvatures (1/mm):")
print(f"  κ_x = {kappa[0]:.6e}")
print(f"  κ_y = {kappa[1]:.6e}")
print(f"  κ_xy = {kappa[2]:.6e}")

# Calculate strains and stresses at top and bottom of each ply
print("\n" + "=" * 70)
print("PART (b): GLOBAL STRESSES VS VERTICAL LOCATION")
print("=" * 70)

ply_data = []

print("\n{:>4} {:>8} {:>10} {:>14} {:>14} {:>14}".format(
    "Ply", "Angle", "z (mm)", "σ_x (MPa)", "σ_y (MPa)", "τ_xy (MPa)"))
print("-" * 70)

for i, theta in enumerate(angles):
    z_bot = z[i]
    z_top = z[i + 1]
    z_mid = (z_bot + z_top) / 2

    # Strains at bottom, mid, and top of ply
    for z_loc, loc_name in [(z_bot, "bot"), (z_mid, "mid"), (z_top, "top")]:
        # Global strains: ε = ε⁰ + z*κ
        eps_global = eps0 + z_loc * kappa

        # Global stresses: σ = Q̄ * ε
        sigma_global = Qbar_list[i] @ eps_global

        ply_data.append({
            'ply': i + 1,
            'angle': theta,
            'z': z_loc,
            'location': loc_name,
            'eps_global': eps_global,
            'sigma_global': sigma_global
        })

        if loc_name in ["bot", "top"]:
            print(f"{i+1:>4} {theta:>8}° {z_loc:>10.4f} {sigma_global[0]:>14.4f} {sigma_global[1]:>14.4f} {sigma_global[2]:>14.4f}")

# Calculate local stresses and Tsai-Hill failure
print("\n" + "=" * 70)
print("PART (c): TSAI-HILL FAILURE ANALYSIS")
print("=" * 70)

print("\nLocal (Material) Stresses and Tsai-Hill Index:")
print("{:>4} {:>8} {:>10} {:>12} {:>12} {:>12} {:>12} {:>8}".format(
    "Ply", "Angle", "z (mm)", "σ_1 (MPa)", "σ_2 (MPa)", "τ_12 (MPa)", "Tsai-Hill", "Status"))
print("-" * 90)

failure_results = []

for data in ply_data:
    if data['location'] not in ['bot', 'top']:
        continue

    # Transform global stress to local (material) coordinates
    T = stress_transformation(data['angle'])
    sigma_local = T @ data['sigma_global']

    sigma1 = sigma_local[0]
    sigma2 = sigma_local[1]
    tau12 = sigma_local[2]

    # Tsai-Hill criterion
    # Use appropriate strength based on sign of stress
    X = Xt if sigma1 >= 0 else Xc
    Y = Yt if sigma2 >= 0 else Yc

    # Tsai-Hill: (σ1/X)² - (σ1*σ2/X²) + (σ2/Y)² + (τ12/S)² ≤ 1
    tsai_hill = (sigma1/X)**2 - (sigma1*sigma2)/X**2 + (sigma2/Y)**2 + (tau12/S)**2

    status = "FAIL" if tsai_hill >= 1 else "SAFE"

    failure_results.append({
        'ply': data['ply'],
        'angle': data['angle'],
        'z': data['z'],
        'location': data['location'],
        'sigma1': sigma1,
        'sigma2': sigma2,
        'tau12': tau12,
        'tsai_hill': tsai_hill,
        'status': status
    })

    print(f"{data['ply']:>4} {data['angle']:>8}° {data['z']:>10.4f} {sigma1:>12.4f} {sigma2:>12.4f} {tau12:>12.4f} {tsai_hill:>12.6f} {status:>8}")

# Summary
print("\n" + "-" * 70)
print("FAILURE SUMMARY:")
print("-" * 70)

failed_plies = [r for r in failure_results if r['status'] == "FAIL"]
if failed_plies:
    print(f"\n⚠ FAILURE DETECTED in {len(failed_plies)} location(s):")
    for f in failed_plies:
        print(f"  - Ply {f['ply']} ({f['angle']}°) at z = {f['z']:.3f} mm ({f['location']}), TH = {f['tsai_hill']:.4f}")
else:
    print("\n✓ NO FAILURE - All plies are safe under the applied loading")

max_th = max(r['tsai_hill'] for r in failure_results)
critical = [r for r in failure_results if r['tsai_hill'] == max_th][0]
print(f"\nCritical location: Ply {critical['ply']} ({critical['angle']}°) at z = {critical['z']:.3f} mm")
print(f"Maximum Tsai-Hill index: {max_th:.6f}")

if max_th < 1:
    safety_factor = 1 / np.sqrt(max_th)
    print(f"Safety Factor (load multiplier to failure): {safety_factor:.2f}")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Global stresses vs z
ax1 = axes[0, 0]
z_plot = [d['z'] for d in ply_data]
sigma_x = [d['sigma_global'][0] for d in ply_data]
sigma_y = [d['sigma_global'][1] for d in ply_data]
tau_xy = [d['sigma_global'][2] for d in ply_data]

ax1.plot(sigma_x, z_plot, 'b-o', label='σ_x', linewidth=2, markersize=4)
ax1.plot(sigma_y, z_plot, 'r-s', label='σ_y', linewidth=2, markersize=4)
ax1.plot(tau_xy, z_plot, 'g-^', label='τ_xy', linewidth=2, markersize=4)

# Add ply boundaries
for zi in z:
    ax1.axhline(y=zi, color='gray', linewidth=0.5, linestyle='--')

ax1.axvline(x=0, color='k', linewidth=0.5)
ax1.set_xlabel('Stress (MPa)', fontsize=12)
ax1.set_ylabel('z (mm)', fontsize=12)
ax1.set_title('Global Stresses vs. Vertical Location', fontsize=14)
ax1.legend()
ax1.grid(True, alpha=0.3)

# Add ply angle labels
for i, theta in enumerate(angles):
    z_mid = (z[i] + z[i+1]) / 2
    ax1.text(ax1.get_xlim()[1] * 0.95, z_mid, f'{theta}°', ha='right', va='center', fontsize=10)

# Plot 2: Local stresses vs z (at interfaces only)
ax2 = axes[0, 1]
z_local = [r['z'] for r in failure_results]
sigma1_plot = [r['sigma1'] for r in failure_results]
sigma2_plot = [r['sigma2'] for r in failure_results]
tau12_plot = [r['tau12'] for r in failure_results]

ax2.plot(sigma1_plot, z_local, 'b-o', label='σ_1', linewidth=2, markersize=6)
ax2.plot(sigma2_plot, z_local, 'r-s', label='σ_2', linewidth=2, markersize=6)
ax2.plot(tau12_plot, z_local, 'g-^', label='τ_12', linewidth=2, markersize=6)

for zi in z:
    ax2.axhline(y=zi, color='gray', linewidth=0.5, linestyle='--')

ax2.axvline(x=0, color='k', linewidth=0.5)
ax2.set_xlabel('Stress (MPa)', fontsize=12)
ax2.set_ylabel('z (mm)', fontsize=12)
ax2.set_title('Local (Material) Stresses vs. z', fontsize=14)
ax2.legend()
ax2.grid(True, alpha=0.3)

# Plot 3: Tsai-Hill index vs z
ax3 = axes[1, 0]
th_values = [r['tsai_hill'] for r in failure_results]

ax3.barh([f"Ply {r['ply']} ({r['location']})" for r in failure_results], th_values,
         color=['red' if v >= 1 else 'green' for v in th_values], alpha=0.7, edgecolor='black')
ax3.axvline(x=1, color='red', linewidth=2, linestyle='--', label='Failure threshold')
ax3.set_xlabel('Tsai-Hill Index', fontsize=12)
ax3.set_ylabel('Ply and Location', fontsize=12)
ax3.set_title('Tsai-Hill Failure Index by Ply', fontsize=14)
ax3.legend()
ax3.grid(True, alpha=0.3, axis='x')

# Plot 4: Laminate stacking visualization
ax4 = axes[1, 1]
colors_map = {30: '#1f77b4', 45: '#ff7f0e', -45: '#2ca02c', -30: '#d62728'}

for i, theta in enumerate(angles):
    rect = plt.Rectangle((0, z[i]), 4, t_ply,
                         facecolor=colors_map[theta], edgecolor='black', linewidth=1)
    ax4.add_patch(rect)
    ax4.text(4.3, (z[i] + z[i+1])/2, f'{theta}°', va='center', fontsize=11, fontweight='bold')
    ax4.text(-0.5, (z[i] + z[i+1])/2, f'Ply {i+1}', va='center', ha='right', fontsize=10)

ax4.set_xlim(-1, 5.5)
ax4.set_ylim(z[0] - 0.3, z[-1] + 0.3)
ax4.set_aspect('equal')
ax4.set_title('[30/45/-45/-30]T Laminate (Unsymmetric)', fontsize=14)
ax4.set_xlabel('Width (arbitrary)', fontsize=12)
ax4.set_ylabel('z (mm)', fontsize=12)
ax4.axhline(y=0, color='k', linewidth=1, linestyle='--', label='Mid-plane')

from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=colors_map[a], edgecolor='black', label=f'{a}°') for a in [30, 45, -45, -30]]
ax4.legend(handles=legend_elements, loc='upper right')

plt.tight_layout()
plt.savefig('/home/user/STP604E/assignment3_problem3_results.png', dpi=300, bbox_inches='tight')
print("\n" + "-" * 70)
print("Figure saved: assignment3_problem3_results.png")
print("=" * 70)

plt.close()
