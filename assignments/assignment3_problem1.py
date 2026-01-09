"""
Assignment 3 - Problem 1: Strength Envelope using Maximum Strain Criterion
STP 604E - Advanced Design, Analysis and Optimization of Composite Structures

A Graphite/Epoxy laminate with [0/±45₂/90]s stacking sequence is loaded only by biaxial loads.
Draw the strength envelope in the σ̄x-σ̄y plane using maximum strain criterion.
Determine max pure tensile Nx and pure compressive Ny.
"""

import numpy as np
import matplotlib.pyplot as plt
from math import cos, sin, radians

# Material Properties: Graphite/Epoxy
E1 = 138e3    # MPa (138 GPa)
E2 = 8.69e3   # MPa (8.69 GPa)
G12 = 7.10e3  # MPa (7.10 GPa)
nu12 = 0.3
nu21 = nu12 * E2 / E1
t_ply = 0.125  # mm

# Strength Properties (MPa)
Xt = 2280     # Longitudinal tensile strength
Xc = 1725     # Longitudinal compressive strength
Yt = 57       # Transverse tensile strength
Yc = 228      # Transverse compressive strength
S = 76        # In-plane shear strength

# Calculate ultimate strains
eps1_t = Xt / E1      # Longitudinal tensile strain limit
eps1_c = Xc / E1      # Longitudinal compressive strain limit
eps2_t = Yt / E2      # Transverse tensile strain limit
eps2_c = Yc / E2      # Transverse compressive strain limit
gamma12_ult = S / G12 # Shear strain limit

print("=" * 70)
print("ASSIGNMENT 3 - PROBLEM 1: STRENGTH ENVELOPE")
print("=" * 70)
print("\nMaterial: Graphite/Epoxy")
print(f"E1 = {E1/1000:.0f} GPa, E2 = {E2/1000:.2f} GPa, G12 = {G12/1000:.2f} GPa")
print(f"ν12 = {nu12}, t = {t_ply} mm")
print("\nStrength Properties:")
print(f"Xt = {Xt} MPa, Xc = {Xc} MPa")
print(f"Yt = {Yt} MPa, Yc = {Yc} MPa")
print(f"S = {S} MPa")
print("\nUltimate Strains:")
print(f"ε1t = {eps1_t:.6f}, ε1c = {eps1_c:.6f}")
print(f"ε2t = {eps2_t:.6f}, ε2c = {eps2_c:.6f}")
print(f"γ12_ult = {gamma12_ult:.6f}")

# Laminate stacking sequence: [0/±45₂/90]s
# This means: [0/45/45/-45/-45/90]s = [0/45/45/-45/-45/90/90/-45/-45/45/45/0]
angles = [0, 45, 45, -45, -45, 90, 90, -45, -45, 45, 45, 0]
n_plies = len(angles)
h_total = n_plies * t_ply

print(f"\nLaminate: [0/±45₂/90]s")
print(f"Full sequence: {angles}")
print(f"Number of plies: {n_plies}")
print(f"Total thickness: {h_total} mm")


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


def transformation_matrix(theta_deg):
    """Strain transformation matrix from global to local coordinates"""
    th = radians(theta_deg)
    m, n = cos(th), sin(th)

    # Transformation matrix for strains (note: uses 2*m*n for shear)
    T_eps = np.array([
        [m**2, n**2, m*n],
        [n**2, m**2, -m*n],
        [-2*m*n, 2*m*n, m**2 - n**2]
    ])
    return T_eps


# Calculate Q matrix
Q = Q_matrix()

# Calculate A matrix (symmetric laminate, B = 0)
z = np.linspace(-h_total/2, h_total/2, n_plies + 1)

A = np.zeros((3, 3))
Qbar_list = []

for i, theta in enumerate(angles):
    Qbar = Q_bar(Q, theta)
    Qbar_list.append(Qbar)
    dz = z[i+1] - z[i]
    A += Qbar * dz

print("\n" + "-" * 70)
print("A-Matrix (Extensional Stiffness) [N/mm]:")
print(np.array2string(A, precision=1, suppress_small=True))

# A-inverse for calculating strains from loads
A_inv = np.linalg.inv(A)

print("\nA-inverse [mm/N]:")
print(np.array2string(A_inv, precision=10, suppress_small=True))


def check_max_strain_failure(eps_global, angles, Qbar_list):
    """
    Check maximum strain criterion for all plies.
    Returns the maximum failure index and the critical ply info.
    """
    max_fi = 0
    critical_info = None

    for i, theta in enumerate(angles):
        # Transform global strains to local (material) coordinates
        T_eps = transformation_matrix(theta)
        eps_local = T_eps @ eps_global

        eps1 = eps_local[0]
        eps2 = eps_local[1]
        gamma12 = eps_local[2]

        # Calculate failure indices for each strain component
        if eps1 >= 0:
            fi1 = eps1 / eps1_t
        else:
            fi1 = -eps1 / eps1_c

        if eps2 >= 0:
            fi2 = eps2 / eps2_t
        else:
            fi2 = -eps2 / eps2_c

        fi12 = abs(gamma12) / gamma12_ult

        # Maximum strain criterion: max of all components
        fi_ply = max(fi1, fi2, fi12)

        if fi_ply > max_fi:
            max_fi = fi_ply
            # Determine failure mode
            if fi_ply == fi1:
                mode = "Fiber tension" if eps1 >= 0 else "Fiber compression"
            elif fi_ply == fi2:
                mode = "Matrix tension" if eps2 >= 0 else "Matrix compression"
            else:
                mode = "Shear"
            critical_info = {
                'ply': i + 1,
                'angle': theta,
                'fi': fi_ply,
                'mode': mode,
                'eps_local': eps_local
            }

    return max_fi, critical_info


def find_failure_load_ratio(sigma_x_ratio, sigma_y_ratio):
    """
    Find the load multiplier at which failure occurs.
    sigma_x = k * sigma_x_ratio, sigma_y = k * sigma_y_ratio
    Returns k at failure.
    """
    # For in-plane loading only (no moments)
    # N = sigma * h (for average stress)
    # epsilon = A_inv @ N = A_inv @ (sigma * h)

    # Unit stress vector direction
    sigma_unit = np.array([sigma_x_ratio, sigma_y_ratio, 0])

    # Mid-plane strains for unit stress
    eps_unit = A_inv @ (sigma_unit * h_total)

    # Binary search for failure load
    k_low, k_high = 0, 10000

    for _ in range(100):
        k = (k_low + k_high) / 2
        eps_global = k * eps_unit
        fi, _ = check_max_strain_failure(eps_global, angles, Qbar_list)

        if fi < 1:
            k_low = k
        else:
            k_high = k

    return k, check_max_strain_failure(k * eps_unit, angles, Qbar_list)


# Generate strength envelope
print("\n" + "=" * 70)
print("GENERATING STRENGTH ENVELOPE")
print("=" * 70)

n_points = 360
theta_angles = np.linspace(0, 2*np.pi, n_points)

envelope_sigma_x = []
envelope_sigma_y = []

for theta in theta_angles:
    ratio_x = np.cos(theta)
    ratio_y = np.sin(theta)

    if abs(ratio_x) < 1e-10 and abs(ratio_y) < 1e-10:
        continue

    k, (fi, info) = find_failure_load_ratio(ratio_x, ratio_y)

    envelope_sigma_x.append(k * ratio_x)
    envelope_sigma_y.append(k * ratio_y)

envelope_sigma_x = np.array(envelope_sigma_x)
envelope_sigma_y = np.array(envelope_sigma_y)

# Find maximum pure tensile Nx (sigma_y = 0, sigma_x > 0)
print("\n" + "-" * 70)
print("(a) Maximum Pure Tensile Load (Nx):")
print("-" * 70)

k_tension, (fi_t, info_t) = find_failure_load_ratio(1, 0)
sigma_x_max_tension = k_tension
Nx_max_tension = sigma_x_max_tension * h_total

print(f"Maximum σ̄x (tensile) = {sigma_x_max_tension:.2f} MPa")
print(f"Maximum Nx = σ̄x × h = {sigma_x_max_tension:.2f} × {h_total} = {Nx_max_tension:.2f} N/mm")
print(f"Critical ply: Ply {info_t['ply']} ({info_t['angle']}°)")
print(f"Failure mode: {info_t['mode']}")
print(f"Local strains at failure: ε1={info_t['eps_local'][0]:.6f}, ε2={info_t['eps_local'][1]:.6f}, γ12={info_t['eps_local'][2]:.6f}")

# Find maximum pure compressive Ny (sigma_x = 0, sigma_y < 0)
print("\n" + "-" * 70)
print("(b) Maximum Pure Compressive Load (Ny):")
print("-" * 70)

k_compression, (fi_c, info_c) = find_failure_load_ratio(0, -1)
sigma_y_max_compression = -k_compression  # Negative for compression
Ny_max_compression = sigma_y_max_compression * h_total

print(f"Maximum σ̄y (compressive) = {sigma_y_max_compression:.2f} MPa")
print(f"Maximum Ny = σ̄y × h = {sigma_y_max_compression:.2f} × {h_total} = {Ny_max_compression:.2f} N/mm")
print(f"Critical ply: Ply {info_c['ply']} ({info_c['angle']}°)")
print(f"Failure mode: {info_c['mode']}")
print(f"Local strains at failure: ε1={info_c['eps_local'][0]:.6f}, ε2={info_c['eps_local'][1]:.6f}, γ12={info_c['eps_local'][2]:.6f}")

# Also find max tensile Ny and compressive Nx for completeness
k_ty, (_, info_ty) = find_failure_load_ratio(0, 1)
k_cx, (_, info_cx) = find_failure_load_ratio(-1, 0)

print("\n" + "-" * 70)
print("Additional Results (for completeness):")
print("-" * 70)
print(f"Max σ̄y (tensile) = {k_ty:.2f} MPa, Ny = {k_ty * h_total:.2f} N/mm")
print(f"Max σ̄x (compressive) = {-k_cx:.2f} MPa, Nx = {-k_cx * h_total:.2f} N/mm")

# Create visualization
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Strength envelope
ax1 = axes[0]
ax1.plot(envelope_sigma_x, envelope_sigma_y, 'b-', linewidth=2, label='Failure Envelope')
ax1.fill(envelope_sigma_x, envelope_sigma_y, alpha=0.2, color='blue')

# Mark key points
ax1.scatter([sigma_x_max_tension], [0], color='red', s=150, zorder=5, marker='o', label=f'Max Nx (tension): {sigma_x_max_tension:.0f} MPa')
ax1.scatter([0], [sigma_y_max_compression], color='green', s=150, zorder=5, marker='s', label=f'Max Ny (compression): {sigma_y_max_compression:.0f} MPa')
ax1.scatter([0], [k_ty], color='orange', s=100, zorder=5, marker='^', label=f'Max Ny (tension): {k_ty:.0f} MPa')
ax1.scatter([-k_cx], [0], color='purple', s=100, zorder=5, marker='d', label=f'Max Nx (compression): {-k_cx:.0f} MPa')

ax1.axhline(y=0, color='k', linewidth=0.5)
ax1.axvline(x=0, color='k', linewidth=0.5)
ax1.set_xlabel('σ̄x (MPa)', fontsize=12)
ax1.set_ylabel('σ̄y (MPa)', fontsize=12)
ax1.set_title('Strength Envelope - Maximum Strain Criterion\n[0/±45₂/90]s Graphite/Epoxy', fontsize=14)
ax1.legend(loc='upper left', fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.set_aspect('equal')

# Plot 2: Laminate stacking visualization
ax2 = axes[1]
unique_angles = sorted(set(angles))
colors_map = {0: '#1f77b4', 45: '#ff7f0e', -45: '#2ca02c', 90: '#d62728'}

for i, theta in enumerate(angles):
    rect = plt.Rectangle((0, i * t_ply - h_total/2), 4, t_ply,
                         facecolor=colors_map[theta], edgecolor='black', linewidth=0.5)
    ax2.add_patch(rect)
    ax2.text(4.2, (i + 0.5) * t_ply - h_total/2, f'{theta}°', va='center', fontsize=9)

ax2.set_xlim(-0.5, 5.5)
ax2.set_ylim(-h_total/2 - 0.1, h_total/2 + 0.1)
ax2.set_aspect('equal')
ax2.set_title('[0/±45₂/90]s Laminate Stack', fontsize=14)
ax2.set_xlabel('Width (arbitrary)', fontsize=12)
ax2.set_ylabel('z (mm)', fontsize=12)
ax2.axhline(y=0, color='k', linewidth=1, linestyle='--', label='Mid-plane')

from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=colors_map[a], edgecolor='black', label=f'{a}°') for a in [0, 45, -45, 90]]
ax2.legend(handles=legend_elements, loc='upper right')

plt.tight_layout()
plt.savefig('/home/user/STP604E/assignment3_problem1_results.png', dpi=300, bbox_inches='tight')
print("\n" + "-" * 70)
print("Figure saved: assignment3_problem1_results.png")
print("=" * 70)

plt.close()
