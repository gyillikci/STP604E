"""
Assignment 3 - Problem 1: Strength Envelope Analysis
Graphite/Epoxy Laminate [0/±45₂/90]s under Biaxial Loading

Using Maximum Strain Failure Criterion to:
1. Draw strength envelope in σ̄x - σ̄y plane
2. Find maximum pure tensile load Nx
3. Find maximum pure compressive load Ny
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

# =============================================================================
# MATERIAL PROPERTIES (Graphite/Epoxy)
# =============================================================================
E1 = 138e3      # MPa (138 GPa)
E2 = 8.69e3     # MPa (8.69 GPa)
G12 = 7.10e3    # MPa (7.10 GPa)
nu12 = 0.3
nu21 = nu12 * E2 / E1
t_ply = 0.125   # mm

# Strength Values (MPa)
Xt = 2280       # Longitudinal tensile strength
Xc = 1725       # Longitudinal compressive strength
Yt = 57         # Transverse tensile strength
Yc = 228        # Transverse compressive strength
S = 76          # Shear strength

# =============================================================================
# STACKING SEQUENCE: [0/±45₂/90]s
# =============================================================================
# [0/±45₂/90]s means: 0, +45, +45, -45, -45, 90 | 90, -45, -45, +45, +45, 0
# Full sequence: [0, 45, 45, -45, -45, 90, 90, -45, -45, 45, 45, 0]
stacking_sequence = [0, 45, 45, -45, -45, 90, 90, -45, -45, 45, 45, 0]
n_plies = len(stacking_sequence)
h_total = n_plies * t_ply  # Total laminate thickness

print("=" * 70)
print("PROBLEM 1: STRENGTH ENVELOPE FOR [0/±45₂/90]s LAMINATE")
print("=" * 70)
print(f"\nStacking sequence: {stacking_sequence}")
print(f"Number of plies: {n_plies}")
print(f"Total thickness: {h_total} mm")

# =============================================================================
# CALCULATE ALLOWABLE STRAINS (Maximum Strain Criterion)
# =============================================================================
# Allowable strains in material coordinates
eps1_t = Xt / E1    # Tensile strain limit in fiber direction
eps1_c = Xc / E1    # Compressive strain limit in fiber direction
eps2_t = Yt / E2    # Tensile strain limit transverse
eps2_c = Yc / E2    # Compressive strain limit transverse
gamma12_max = S / G12  # Shear strain limit

print("\n" + "-" * 70)
print("ALLOWABLE STRAINS (Maximum Strain Criterion)")
print("-" * 70)
print(f"ε₁ᵗ (tensile)     = {eps1_t:.6f} ({eps1_t*1e6:.2f} με)")
print(f"ε₁ᶜ (compressive) = {eps1_c:.6f} ({eps1_c*1e6:.2f} με)")
print(f"ε₂ᵗ (tensile)     = {eps2_t:.6f} ({eps2_t*1e6:.2f} με)")
print(f"ε₂ᶜ (compressive) = {eps2_c:.6f} ({eps2_c*1e6:.2f} με)")
print(f"γ₁₂ᵐᵃˣ (shear)    = {gamma12_max:.6f} ({gamma12_max*1e6:.2f} με)")

# =============================================================================
# LAMINA STIFFNESS CALCULATIONS
# =============================================================================
def calculate_Q():
    """Calculate reduced stiffness matrix Q in material coordinates"""
    denom = 1 - nu12 * nu21
    Q11 = E1 / denom
    Q22 = E2 / denom
    Q12 = nu12 * E2 / denom
    Q66 = G12
    return np.array([[Q11, Q12, 0],
                     [Q12, Q22, 0],
                     [0, 0, Q66]])

def calculate_Qbar(theta_deg):
    """Calculate transformed stiffness matrix Q-bar"""
    Q = calculate_Q()
    theta = np.radians(theta_deg)
    c = np.cos(theta)
    s = np.sin(theta)
    
    Q11, Q22, Q12, Q66 = Q[0,0], Q[1,1], Q[0,1], Q[2,2]
    
    Qbar11 = Q11*c**4 + 2*(Q12 + 2*Q66)*c**2*s**2 + Q22*s**4
    Qbar22 = Q11*s**4 + 2*(Q12 + 2*Q66)*c**2*s**2 + Q22*c**4
    Qbar12 = (Q11 + Q22 - 4*Q66)*c**2*s**2 + Q12*(c**4 + s**4)
    Qbar16 = (Q11 - Q12 - 2*Q66)*c**3*s - (Q22 - Q12 - 2*Q66)*c*s**3
    Qbar26 = (Q11 - Q12 - 2*Q66)*c*s**3 - (Q22 - Q12 - 2*Q66)*c**3*s
    Qbar66 = (Q11 + Q22 - 2*Q12 - 2*Q66)*c**2*s**2 + Q66*(c**4 + s**4)
    
    return np.array([[Qbar11, Qbar12, Qbar16],
                     [Qbar12, Qbar22, Qbar26],
                     [Qbar16, Qbar26, Qbar66]])

def calculate_T_strain(theta_deg):
    """Strain transformation matrix (global to local)"""
    theta = np.radians(theta_deg)
    c = np.cos(theta)
    s = np.sin(theta)
    
    T = np.array([[c**2, s**2, c*s],
                  [s**2, c**2, -c*s],
                  [-2*c*s, 2*c*s, c**2 - s**2]])
    return T

# =============================================================================
# CALCULATE A MATRIX (Extensional Stiffness)
# =============================================================================
def calculate_z_coordinates():
    """Calculate z-coordinates of ply interfaces"""
    z = np.zeros(n_plies + 1)
    z[0] = -h_total / 2
    for i in range(n_plies):
        z[i+1] = z[i] + t_ply
    return z

z_coords = calculate_z_coordinates()

# Calculate A matrix
A = np.zeros((3, 3))
for k in range(n_plies):
    Qbar = calculate_Qbar(stacking_sequence[k])
    z_bot = z_coords[k]
    z_top = z_coords[k+1]
    A += Qbar * (z_top - z_bot)

print("\n" + "-" * 70)
print("A MATRIX (Extensional Stiffness) [N/mm]")
print("-" * 70)
for i in range(3):
    print(f"[{A[i,0]:12.2f}  {A[i,1]:12.2f}  {A[i,2]:12.2f}]")

# A-bar matrix (normalized by thickness)
A_bar = A / h_total

print("\n" + "-" * 70)
print("Ā MATRIX (A/h) [MPa]")
print("-" * 70)
for i in range(3):
    print(f"[{A_bar[i,0]:12.2f}  {A_bar[i,1]:12.2f}  {A_bar[i,2]:12.2f}]")

# Compliance matrix
a_bar = np.linalg.inv(A_bar)

print("\n" + "-" * 70)
print("ā MATRIX (Compliance, inverse of Ā) [1/MPa]")
print("-" * 70)
for i in range(3):
    print(f"[{a_bar[i,0]:12.3e}  {a_bar[i,1]:12.3e}  {a_bar[i,2]:12.3e}]")

# =============================================================================
# STRENGTH ENVELOPE CALCULATION
# =============================================================================
def get_local_strains(eps_x, eps_y, gamma_xy, theta_deg):
    """Transform global strains to local (material) strains"""
    global_strain = np.array([eps_x, eps_y, gamma_xy])
    T = calculate_T_strain(theta_deg)
    local_strain = T @ global_strain
    return local_strain  # [eps_1, eps_2, gamma_12]

def check_failure_max_strain(eps_1, eps_2, gamma_12):
    """
    Check failure using Maximum Strain Criterion
    Returns failure indices for each mode
    """
    # Fiber direction (mode 1)
    if eps_1 >= 0:
        FI_1 = eps_1 / eps1_t
    else:
        FI_1 = abs(eps_1) / eps1_c
    
    # Transverse direction (mode 2)
    if eps_2 >= 0:
        FI_2 = eps_2 / eps2_t
    else:
        FI_2 = abs(eps_2) / eps2_c
    
    # Shear (mode 3)
    FI_12 = abs(gamma_12) / gamma12_max
    
    return FI_1, FI_2, FI_12

def find_max_load_ratio(sigma_x, sigma_y):
    """
    Find maximum load ratio λ such that λ*(sigma_x, sigma_y) causes first ply failure
    Returns: (λ_max, critical_ply, failure_mode)
    """
    if sigma_x == 0 and sigma_y == 0:
        return float('inf'), None, None
    
    min_lambda = float('inf')
    critical_ply = None
    failure_mode = None
    
    # For each ply
    for k, theta in enumerate(stacking_sequence):
        # Global strains from unit stress
        eps_global = a_bar @ np.array([sigma_x, sigma_y, 0])
        eps_x, eps_y, gamma_xy = eps_global
        
        # Transform to local strains
        local_strain = get_local_strains(eps_x, eps_y, gamma_xy, theta)
        eps_1, eps_2, gamma_12 = local_strain
        
        # Check each failure mode
        # Mode 1: Fiber direction
        if eps_1 > 0:
            lam = eps1_t / eps_1 if eps_1 != 0 else float('inf')
            if lam > 0 and lam < min_lambda:
                min_lambda = lam
                critical_ply = k
                failure_mode = f"Fiber Tensile (ε₁ > ε₁ᵗ) in {theta}° ply"
        elif eps_1 < 0:
            lam = eps1_c / abs(eps_1)
            if lam > 0 and lam < min_lambda:
                min_lambda = lam
                critical_ply = k
                failure_mode = f"Fiber Compressive (|ε₁| > ε₁ᶜ) in {theta}° ply"
        
        # Mode 2: Transverse direction
        if eps_2 > 0:
            lam = eps2_t / eps_2 if eps_2 != 0 else float('inf')
            if lam > 0 and lam < min_lambda:
                min_lambda = lam
                critical_ply = k
                failure_mode = f"Matrix Tensile (ε₂ > ε₂ᵗ) in {theta}° ply"
        elif eps_2 < 0:
            lam = eps2_c / abs(eps_2)
            if lam > 0 and lam < min_lambda:
                min_lambda = lam
                critical_ply = k
                failure_mode = f"Matrix Compressive (|ε₂| > ε₂ᶜ) in {theta}° ply"
        
        # Mode 3: Shear
        if gamma_12 != 0:
            lam = gamma12_max / abs(gamma_12)
            if lam > 0 and lam < min_lambda:
                min_lambda = lam
                critical_ply = k
                failure_mode = f"Shear (|γ₁₂| > γ₁₂ᵐᵃˣ) in {theta}° ply"
    
    return min_lambda, critical_ply, failure_mode

# =============================================================================
# GENERATE STRENGTH ENVELOPE
# =============================================================================
print("\n" + "=" * 70)
print("GENERATING STRENGTH ENVELOPE")
print("=" * 70)

# Generate envelope points by scanning directions
n_angles = 360
angles = np.linspace(0, 2*np.pi, n_angles)
envelope_points = []

for angle in angles:
    # Unit stress direction
    sigma_x = np.cos(angle)
    sigma_y = np.sin(angle)
    
    # Find maximum allowable stress in this direction
    lam_max, ply, mode = find_max_load_ratio(sigma_x, sigma_y)
    
    if lam_max != float('inf'):
        envelope_points.append((lam_max * sigma_x, lam_max * sigma_y))

envelope_points = np.array(envelope_points)

# =============================================================================
# FIND SPECIFIC LOAD CASES
# =============================================================================
print("\n" + "-" * 70)
print("(a) MAXIMUM PURE TENSILE LOAD Nx (σ̄x > 0, σ̄y = 0)")
print("-" * 70)

# Pure Nx (tensile): σ̄x > 0, σ̄y = 0
lam_Nx_t, ply_Nx_t, mode_Nx_t = find_max_load_ratio(1, 0)
sigma_x_max_t = lam_Nx_t
Nx_max_t = sigma_x_max_t * h_total

print(f"Maximum σ̄x (tensile) = {sigma_x_max_t:.2f} MPa")
print(f"Maximum Nx (tensile) = σ̄x × h = {sigma_x_max_t:.2f} × {h_total} = {Nx_max_t:.2f} N/mm")
print(f"Failure mode: {mode_Nx_t}")

# Calculate strains at failure for verification
eps_global_Nx = a_bar @ np.array([sigma_x_max_t, 0, 0])
print(f"\nGlobal strains at failure:")
print(f"  εx = {eps_global_Nx[0]*1e6:.2f} με")
print(f"  εy = {eps_global_Nx[1]*1e6:.2f} με")
print(f"  γxy = {eps_global_Nx[2]*1e6:.2f} με")

# Check each ply
print("\nLocal strains in each ply:")
unique_plies = list(set(stacking_sequence))
for theta in sorted(unique_plies):
    local = get_local_strains(eps_global_Nx[0], eps_global_Nx[1], eps_global_Nx[2], theta)
    FI = check_failure_max_strain(local[0], local[1], local[2])
    print(f"  {theta:4}° ply: ε₁={local[0]*1e6:8.2f}με, ε₂={local[1]*1e6:8.2f}με, γ₁₂={local[2]*1e6:8.2f}με  FI=[{FI[0]:.3f}, {FI[1]:.3f}, {FI[2]:.3f}]")

print("\n" + "-" * 70)
print("(b) MAXIMUM PURE COMPRESSIVE LOAD Ny (σ̄x = 0, σ̄y < 0)")
print("-" * 70)

# Pure Ny (compressive): σ̄x = 0, σ̄y < 0
lam_Ny_c, ply_Ny_c, mode_Ny_c = find_max_load_ratio(0, -1)
sigma_y_max_c = -lam_Ny_c  # Negative for compression
Ny_max_c = sigma_y_max_c * h_total

print(f"Maximum σ̄y (compressive) = {sigma_y_max_c:.2f} MPa")
print(f"Maximum Ny (compressive) = σ̄y × h = {sigma_y_max_c:.2f} × {h_total} = {Ny_max_c:.2f} N/mm")
print(f"Failure mode: {mode_Ny_c}")

# Calculate strains at failure for verification
eps_global_Ny = a_bar @ np.array([0, sigma_y_max_c, 0])
print(f"\nGlobal strains at failure:")
print(f"  εx = {eps_global_Ny[0]*1e6:.2f} με")
print(f"  εy = {eps_global_Ny[1]*1e6:.2f} με")
print(f"  γxy = {eps_global_Ny[2]*1e6:.2f} με")

# Check each ply
print("\nLocal strains in each ply:")
for theta in sorted(unique_plies):
    local = get_local_strains(eps_global_Ny[0], eps_global_Ny[1], eps_global_Ny[2], theta)
    FI = check_failure_max_strain(local[0], local[1], local[2])
    print(f"  {theta:4}° ply: ε₁={local[0]*1e6:8.2f}με, ε₂={local[1]*1e6:8.2f}με, γ₁₂={local[2]*1e6:8.2f}με  FI=[{FI[0]:.3f}, {FI[1]:.3f}, {FI[2]:.3f}]")

# =============================================================================
# ADDITIONAL LOAD CASES FOR COMPLETENESS
# =============================================================================
print("\n" + "-" * 70)
print("ADDITIONAL LOAD CASES (for reference)")
print("-" * 70)

# Pure Nx (compressive)
lam_Nx_c, _, mode_Nx_c = find_max_load_ratio(-1, 0)
print(f"Nx (compressive): σ̄x = {-lam_Nx_c:.2f} MPa, Nx = {-lam_Nx_c * h_total:.2f} N/mm")
print(f"  Failure: {mode_Nx_c}")

# Pure Ny (tensile)
lam_Ny_t, _, mode_Ny_t = find_max_load_ratio(0, 1)
print(f"Ny (tensile): σ̄y = {lam_Ny_t:.2f} MPa, Ny = {lam_Ny_t * h_total:.2f} N/mm")
print(f"  Failure: {mode_Ny_t}")

# =============================================================================
# PLOT STRENGTH ENVELOPE
# =============================================================================
fig, ax = plt.subplots(1, 1, figsize=(12, 10))

# Plot the envelope
ax.fill(envelope_points[:,0], envelope_points[:,1], alpha=0.3, color='blue', label='Safe Region')
ax.plot(envelope_points[:,0], envelope_points[:,1], 'b-', linewidth=2, label='Failure Envelope')

# Mark key points
# (a) Maximum tensile Nx
ax.plot(sigma_x_max_t, 0, 'ro', markersize=12, markeredgecolor='black', markeredgewidth=2)
ax.annotate(f'(a) Max Nx (tensile)\nσ̄x = {sigma_x_max_t:.0f} MPa\nNx = {Nx_max_t:.1f} N/mm', 
            xy=(sigma_x_max_t, 0), xytext=(sigma_x_max_t + 50, 100),
            fontsize=10, ha='left',
            arrowprops=dict(arrowstyle='->', color='red'))

# (b) Maximum compressive Ny
ax.plot(0, sigma_y_max_c, 'gs', markersize=12, markeredgecolor='black', markeredgewidth=2)
ax.annotate(f'(b) Max Ny (compressive)\nσ̄y = {sigma_y_max_c:.0f} MPa\nNy = {Ny_max_c:.1f} N/mm', 
            xy=(0, sigma_y_max_c), xytext=(100, sigma_y_max_c),
            fontsize=10, ha='left',
            arrowprops=dict(arrowstyle='->', color='green'))

# Additional key points
ax.plot(-lam_Nx_c, 0, 'm^', markersize=10, label=f'Nx (comp): {-lam_Nx_c * h_total:.0f} N/mm')
ax.plot(0, lam_Ny_t, 'cv', markersize=10, label=f'Ny (tens): {lam_Ny_t * h_total:.0f} N/mm')

# Axes
ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
ax.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
ax.grid(True, linestyle='--', alpha=0.7)

# Labels
ax.set_xlabel('σ̄x (MPa)', fontsize=14)
ax.set_ylabel('σ̄y (MPa)', fontsize=14)
ax.set_title('Strength Envelope for [0/±45₂/90]s Graphite/Epoxy Laminate\n(Maximum Strain Criterion)', fontsize=14)

# Set equal aspect ratio
ax.set_aspect('equal', adjustable='box')
ax.legend(loc='upper right', fontsize=10)

plt.tight_layout()
plt.savefig('c:/Users/z003n5uc/Desktop/STP604E/assignment_2/assignment_3/strength_envelope.png', dpi=300, bbox_inches='tight')
plt.show()

# =============================================================================
# DETAILED FAILURE ANALYSIS
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY OF RESULTS")
print("=" * 70)
print(f"""
LAMINATE: [0/±45₂/90]s Graphite/Epoxy
Total thickness h = {h_total} mm ({n_plies} plies × {t_ply} mm)

MAXIMUM STRAIN CRITERION ALLOWABLES:
  ε₁ᵗ = {eps1_t*1e6:.2f} με (fiber tensile)
  ε₁ᶜ = {eps1_c*1e6:.2f} με (fiber compressive)
  ε₂ᵗ = {eps2_t*1e6:.2f} με (matrix tensile)
  ε₂ᶜ = {eps2_c*1e6:.2f} με (matrix compressive)
  γ₁₂ᵐᵃˣ = {gamma12_max*1e6:.2f} με (shear)

ANSWERS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
(a) MAXIMUM PURE TENSILE LOAD (Nx):
    σ̄x,max = {sigma_x_max_t:.2f} MPa
    Nx,max = {Nx_max_t:.2f} N/mm
    Failure Type: {mode_Nx_t}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
(b) MAXIMUM PURE COMPRESSIVE LOAD (Ny):
    σ̄y,max = {sigma_y_max_c:.2f} MPa
    Ny,max = {Ny_max_c:.2f} N/mm
    Failure Type: {mode_Ny_c}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("\n✓ Strength envelope plot saved to 'strength_envelope.png'")
