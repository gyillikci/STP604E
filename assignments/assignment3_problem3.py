"""
Assignment 3 - Problem 3: Laminate Strength Optimization
STP 604E - Advanced Design, Analysis and Optimization of Composite Structures

Design a symmetric laminate to maximize strength under biaxial loading
using Particle Swarm Optimization (PSO) to find optimal ply angles.
"""

import numpy as np
import matplotlib.pyplot as plt
from math import cos, sin, radians
import sys
sys.path.insert(0, '/home/user/STP604E')

np.random.seed(42)

# Material Properties: IM7/8552 Carbon/Epoxy
E1 = 165000  # MPa
E2 = 8400    # MPa
G12 = 5600   # MPa
nu12 = 0.34
nu21 = nu12 * E2 / E1
t_ply = 0.125  # mm

# Strength Properties (MPa)
Xt = 2724    # Longitudinal tensile strength
Xc = 1690    # Longitudinal compressive strength
Yt = 111     # Transverse tensile strength
Yc = 199     # Transverse compressive strength
S = 130      # In-plane shear strength

# Target loading: biaxial tension with shear
Nx_target = 500   # N/mm
Ny_target = 300   # N/mm
Nxy_target = 100  # N/mm

print("=" * 70)
print("ASSIGNMENT 3 - PROBLEM 3: LAMINATE STRENGTH OPTIMIZATION")
print("=" * 70)
print("\nMaterial: IM7/8552 Carbon/Epoxy")
print(f"E1 = {E1} MPa, E2 = {E2} MPa, G12 = {G12} MPa")
print(f"nu12 = {nu12}, t_ply = {t_ply} mm")
print("\nStrength Properties:")
print(f"Xt = {Xt} MPa, Xc = {Xc} MPa")
print(f"Yt = {Yt} MPa, Yc = {Yc} MPa")
print(f"S = {S} MPa")
print(f"\nTarget Loading:")
print(f"Nx = {Nx_target} N/mm, Ny = {Ny_target} N/mm, Nxy = {Nxy_target} N/mm")


def Q_matrix():
    """Calculate reduced stiffness matrix Q"""
    nu21_calc = nu12 * E2 / E1
    Q = np.zeros((3, 3))
    Q[0, 0] = E1 / (1 - nu12 * nu21_calc)
    Q[1, 1] = E2 / (1 - nu12 * nu21_calc)
    Q[0, 1] = Q[1, 0] = nu12 * E2 / (1 - nu12 * nu21_calc)
    Q[2, 2] = G12
    return Q


def Q_bar(Q, theta_deg):
    """Calculate transformed stiffness matrix"""
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
    """Stress transformation matrix"""
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
    return F1*sigma1 + F2*sigma2 + F11*sigma1**2 + F22*sigma2**2 + F66*tau12**2 + 2*F12*sigma1*sigma2


def evaluate_laminate(angles, loads):
    """
    Evaluate laminate strength under given loads.
    Returns maximum Tsai-Wu failure index across all plies.
    """
    Q = Q_matrix()

    # Create symmetric laminate: [angles]_s
    full_angles = list(angles) + list(angles)[::-1]
    n_plies = len(full_angles)
    h_total = n_plies * t_ply
    z = np.linspace(-h_total/2, h_total/2, n_plies + 1)

    # Calculate A matrix
    A = np.zeros((3, 3))
    Qbar_list = []
    for i, theta in enumerate(full_angles):
        Qbar = Q_bar(Q, theta)
        Qbar_list.append(Qbar)
        dz = z[i+1] - z[i]
        A += Qbar * dz

    # Mid-plane strains
    try:
        A_inv = np.linalg.inv(A)
    except:
        return 1e10  # Singular matrix

    N = np.array(loads)
    epsilon_0 = A_inv @ N

    # Calculate max failure index
    max_fi = 0
    for i, theta in enumerate(full_angles):
        sigma_global = Qbar_list[i] @ epsilon_0
        T = transformation_matrix(theta)
        sigma_local = T @ sigma_global
        fi = tsai_wu_fi(sigma_local[0], sigma_local[1], sigma_local[2])
        max_fi = max(max_fi, fi)

    return max_fi


def pso_optimize(n_plies_half, n_particles=30, n_iterations=100, loads=None):
    """
    Particle Swarm Optimization to minimize failure index.
    Optimizes ply angles for a symmetric laminate.
    """
    if loads is None:
        loads = [Nx_target, Ny_target, Nxy_target]

    # Initialize particles (angles between -90 and 90)
    positions = np.random.uniform(-90, 90, (n_particles, n_plies_half))
    velocities = np.random.uniform(-10, 10, (n_particles, n_plies_half))

    # PSO parameters
    w = 0.7      # Inertia weight
    c1 = 1.5     # Cognitive parameter
    c2 = 1.5     # Social parameter

    # Initialize best positions
    personal_best_pos = positions.copy()
    personal_best_val = np.array([evaluate_laminate(p, loads) for p in positions])

    global_best_idx = np.argmin(personal_best_val)
    global_best_pos = personal_best_pos[global_best_idx].copy()
    global_best_val = personal_best_val[global_best_idx]

    history = [global_best_val]

    for iteration in range(n_iterations):
        for i in range(n_particles):
            # Update velocity
            r1, r2 = np.random.random(n_plies_half), np.random.random(n_plies_half)
            velocities[i] = (w * velocities[i] +
                           c1 * r1 * (personal_best_pos[i] - positions[i]) +
                           c2 * r2 * (global_best_pos - positions[i]))

            # Clamp velocity
            velocities[i] = np.clip(velocities[i], -30, 30)

            # Update position
            positions[i] += velocities[i]
            positions[i] = np.clip(positions[i], -90, 90)

            # Evaluate
            fi = evaluate_laminate(positions[i], loads)

            # Update personal best
            if fi < personal_best_val[i]:
                personal_best_val[i] = fi
                personal_best_pos[i] = positions[i].copy()

                # Update global best
                if fi < global_best_val:
                    global_best_val = fi
                    global_best_pos = positions[i].copy()

        history.append(global_best_val)

        # Adaptive inertia weight
        w = 0.9 - 0.5 * (iteration / n_iterations)

    return global_best_pos, global_best_val, history


# Run optimization for different laminate configurations
print("\n" + "=" * 70)
print("OPTIMIZATION RESULTS")
print("=" * 70)

configs = [
    (2, "4-ply symmetric [θ₁/θ₂]s"),
    (4, "8-ply symmetric [θ₁/θ₂/θ₃/θ₄]s"),
    (6, "12-ply symmetric [θ₁/θ₂/θ₃/θ₄/θ₅/θ₆]s"),
]

results = {}
loads = [Nx_target, Ny_target, Nxy_target]

for n_plies_half, description in configs:
    print(f"\n{description}:")
    print("-" * 50)

    best_angles, best_fi, history = pso_optimize(n_plies_half, n_particles=40, n_iterations=150, loads=loads)

    # Round angles to nearest 5 degrees (practical manufacturing)
    rounded_angles = np.round(best_angles / 5) * 5

    # Re-evaluate with rounded angles
    fi_rounded = evaluate_laminate(rounded_angles, loads)

    safety_factor = 1 / np.sqrt(best_fi) if best_fi > 0 else float('inf')
    sf_rounded = 1 / np.sqrt(fi_rounded) if fi_rounded > 0 else float('inf')

    results[description] = {
        'angles': best_angles,
        'rounded_angles': rounded_angles,
        'fi': best_fi,
        'fi_rounded': fi_rounded,
        'sf': safety_factor,
        'sf_rounded': sf_rounded,
        'history': history
    }

    print(f"  Optimal angles: [{', '.join([f'{a:.1f}°' for a in best_angles])}]s")
    print(f"  Rounded angles: [{', '.join([f'{int(a)}°' for a in rounded_angles])}]s")
    print(f"  Tsai-Wu FI (optimal): {best_fi:.6f}")
    print(f"  Tsai-Wu FI (rounded): {fi_rounded:.6f}")
    print(f"  Safety Factor (optimal): {safety_factor:.2f}")
    print(f"  Safety Factor (rounded): {sf_rounded:.2f}")

# Compare with standard laminates
print("\n" + "=" * 70)
print("COMPARISON WITH STANDARD LAMINATES")
print("=" * 70)

standard_laminates = {
    "Cross-ply [0/90]s": [0, 90],
    "Angle-ply [±45]s": [45, -45],
    "Quasi-isotropic [0/±45/90]s": [0, 45, -45, 90],
    "Balanced [0/±60]s": [0, 60, -60],
}

print(f"\n{'Laminate':<35} {'Tsai-Wu FI':>12} {'Safety Factor':>14}")
print("-" * 65)

for name, angles in standard_laminates.items():
    fi = evaluate_laminate(angles, loads)
    sf = 1 / np.sqrt(fi) if fi > 0 else float('inf')
    print(f"{name:<35} {fi:>12.6f} {sf:>14.2f}")

# Add optimized results
for desc, res in results.items():
    short_name = f"Optimized {desc.split()[0]}"
    print(f"{short_name:<35} {res['fi']:>12.6f} {res['sf']:>14.2f}")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Convergence history
ax1 = axes[0, 0]
colors = ['blue', 'red', 'green']
for (desc, res), color in zip(results.items(), colors):
    label = desc.split()[0]
    ax1.plot(res['history'], label=label, linewidth=2, color=color)
ax1.set_xlabel('Iteration', fontsize=12)
ax1.set_ylabel('Best Tsai-Wu Failure Index', fontsize=12)
ax1.set_title('PSO Convergence History', fontsize=14)
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_yscale('log')

# Plot 2: Safety factor comparison
ax2 = axes[0, 1]
all_laminates = {}
for name, angles in standard_laminates.items():
    fi = evaluate_laminate(angles, loads)
    sf = 1 / np.sqrt(fi) if fi > 0 else float('inf')
    all_laminates[name.replace('[', '\n[')] = sf

for desc, res in results.items():
    short = f"Optimized\n{desc.split()[0]}"
    all_laminates[short] = res['sf']

names = list(all_laminates.keys())
sfs = list(all_laminates.values())
bar_colors = ['gray'] * len(standard_laminates) + colors[:len(results)]
bars = ax2.bar(range(len(names)), sfs, color=bar_colors, alpha=0.8, edgecolor='black')
ax2.set_xticks(range(len(names)))
ax2.set_xticklabels(names, fontsize=9)
ax2.set_ylabel('Safety Factor', fontsize=12)
ax2.set_title('Safety Factor Comparison', fontsize=14)
ax2.grid(True, alpha=0.3, axis='y')
ax2.axhline(y=1, color='r', linestyle='--', linewidth=2, label='Failure threshold')

# Plot 3: Optimized laminate visualization (8-ply)
ax3 = axes[1, 0]
best_8ply = results['8-ply symmetric [θ₁/θ₂/θ₃/θ₄]s']
angles_8 = list(best_8ply['rounded_angles']) + list(best_8ply['rounded_angles'])[::-1]
n_plies_vis = len(angles_8)
h_total_vis = n_plies_vis * t_ply

cmap = plt.cm.coolwarm
for i, theta in enumerate(angles_8):
    color = cmap((theta + 90) / 180)
    rect = plt.Rectangle((0, i * t_ply - h_total_vis/2), 4, t_ply,
                         facecolor=color, edgecolor='black', linewidth=0.5)
    ax3.add_patch(rect)
    ax3.text(4.2, (i + 0.5) * t_ply - h_total_vis/2, f'{int(theta)}°', va='center', fontsize=10)

ax3.set_xlim(-0.5, 5)
ax3.set_ylim(-h_total_vis/2 - 0.1, h_total_vis/2 + 0.1)
ax3.set_aspect('equal')
ax3.set_title(f'Optimized 8-ply Laminate\nSF = {best_8ply["sf_rounded"]:.2f}', fontsize=14)
ax3.set_xlabel('Width (arbitrary)', fontsize=12)
ax3.set_ylabel('z (mm)', fontsize=12)
ax3.axhline(y=0, color='k', linewidth=1, linestyle='--')

# Add colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(-90, 90))
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax3, orientation='vertical', label='Ply Angle (°)')

# Plot 4: Failure index surface for 2-angle laminate
ax4 = axes[1, 1]
theta1_range = np.linspace(-90, 90, 50)
theta2_range = np.linspace(-90, 90, 50)
FI_surface = np.zeros((len(theta1_range), len(theta2_range)))

for i, t1 in enumerate(theta1_range):
    for j, t2 in enumerate(theta2_range):
        FI_surface[i, j] = evaluate_laminate([t1, t2], loads)

# Clip for visualization
FI_surface = np.clip(FI_surface, 0, 2)

T1, T2 = np.meshgrid(theta1_range, theta2_range)
contour = ax4.contourf(T1, T2, FI_surface.T, levels=20, cmap='RdYlGn_r')
ax4.contour(T1, T2, FI_surface.T, levels=[1.0], colors='black', linewidths=2)
cbar2 = plt.colorbar(contour, ax=ax4, label='Tsai-Wu FI')

# Mark optimum
opt_4ply = results['4-ply symmetric [θ₁/θ₂]s']
ax4.scatter(opt_4ply['angles'][0], opt_4ply['angles'][1], color='blue', s=200, marker='*',
           edgecolor='white', linewidth=2, zorder=5, label='PSO Optimum')
ax4.set_xlabel('θ₁ (degrees)', fontsize=12)
ax4.set_ylabel('θ₂ (degrees)', fontsize=12)
ax4.set_title('Failure Index Surface for [θ₁/θ₂]s\n(Black line = FI=1)', fontsize=14)
ax4.legend(loc='upper right')

plt.tight_layout()
plt.savefig('/home/user/STP604E/assignment3_problem3_results.png', dpi=300, bbox_inches='tight')
print("\n" + "-" * 70)
print("Figure saved: assignment3_problem3_results.png")
print("=" * 70)

# Final Summary
print("\n" + "=" * 70)
print("SUMMARY: RECOMMENDED LAMINATE DESIGN")
print("=" * 70)
best_config = max(results.items(), key=lambda x: x[1]['sf_rounded'])
print(f"\nBest performing laminate: {best_config[0]}")
print(f"Recommended stacking sequence: [{', '.join([f'{int(a)}°' for a in best_config[1]['rounded_angles']])}]s")
print(f"Safety Factor: {best_config[1]['sf_rounded']:.2f}")
print(f"\nThis design provides {best_config[1]['sf_rounded']:.1f}x safety margin under the specified loading:")
print(f"  Nx = {Nx_target} N/mm, Ny = {Ny_target} N/mm, Nxy = {Nxy_target} N/mm")
print("=" * 70)

plt.close()
