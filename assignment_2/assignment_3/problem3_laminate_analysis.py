"""
Assignment 3 - Problem 3: Laminate Analysis under Combined Loading
[30/45/-45/-30]_T Kevlar/Epoxy Laminate

Given:
- Nx = Ny = 1000 N/m, Nxy = 0
- Mx = 0, My = Mxy = 50 N (Note: units should be N·m/m = N)
- Material: Kevlar/Epoxy

Find:
a. Mid-plane strains and curvatures
b. Global stresses vs. vertical location (plot)
c. Failure analysis using Tsai-Hill criterion
"""

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# MATERIAL PROPERTIES (Kevlar/Epoxy)
# =============================================================================
E1 = 76e9       # Pa (76 GPa)
E2 = 5.50e9     # Pa (5.50 GPa)
G12 = 2.30e9    # Pa (2.30 GPa)
nu12 = 0.34
nu21 = nu12 * E2 / E1
t_ply = 1.25e-3  # m (1.25 mm)

# Strength Values (Pa)
Xt = 1400e6     # Longitudinal tensile strength
Xc = 235e6      # Longitudinal compressive strength
Yt = 53e6       # Transverse tensile strength
Yc = 12e6       # Transverse compressive strength  
S = 34e6        # Shear strength

# =============================================================================
# STACKING SEQUENCE: [30/45/-45/-30]_T (Total - unsymmetric)
# =============================================================================
stacking_sequence = [30, 45, -45, -30]  # Bottom to top
n_plies = len(stacking_sequence)
h_total = n_plies * t_ply  # Total laminate thickness

print("=" * 70)
print("PROBLEM 3: LAMINATE ANALYSIS [30/45/-45/-30]_T")
print("=" * 70)
print(f"\nStacking sequence: {stacking_sequence} (bottom to top)")
print(f"Number of plies: {n_plies}")
print(f"Ply thickness: {t_ply*1000:.2f} mm")
print(f"Total thickness: {h_total*1000:.2f} mm")

# =============================================================================
# APPLIED LOADS
# =============================================================================
# Force resultants (N/m)
Nx = 1000       # N/m
Ny = 1000       # N/m
Nxy = 0         # N/m

# Moment resultants (N·m/m = N)
Mx = 0          # N
My = 50         # N
Mxy = 50        # N

# Load vectors
N_vec = np.array([Nx, Ny, Nxy])
M_vec = np.array([Mx, My, Mxy])
load_vec = np.concatenate([N_vec, M_vec])

print("\n" + "-" * 70)
print("APPLIED LOADS")
print("-" * 70)
print(f"Nx = {Nx} N/m,  Ny = {Ny} N/m,  Nxy = {Nxy} N/m")
print(f"Mx = {Mx} N,    My = {My} N,    Mxy = {Mxy} N")

# =============================================================================
# LAMINA STIFFNESS FUNCTIONS
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

def calculate_T_stress(theta_deg):
    """Stress transformation matrix (global to local)"""
    theta = np.radians(theta_deg)
    c = np.cos(theta)
    s = np.sin(theta)
    
    T = np.array([[c**2, s**2, 2*c*s],
                  [s**2, c**2, -2*c*s],
                  [-c*s, c*s, c**2 - s**2]])
    return T

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
# CALCULATE Z-COORDINATES
# =============================================================================
def calculate_z_coordinates():
    """Calculate z-coordinates of ply interfaces (bottom to top)"""
    z = np.zeros(n_plies + 1)
    z[0] = -h_total / 2  # Bottom of laminate
    for i in range(n_plies):
        z[i+1] = z[i] + t_ply
    return z

z_coords = calculate_z_coordinates()

print("\n" + "-" * 70)
print("PLY Z-COORDINATES (from midplane)")
print("-" * 70)
print(f"{'Ply':<6} {'Angle':<8} {'z_bot (mm)':<12} {'z_top (mm)':<12} {'z_mid (mm)':<12}")
print("-" * 70)
for k in range(n_plies):
    z_bot = z_coords[k] * 1000
    z_top = z_coords[k+1] * 1000
    z_mid = (z_coords[k] + z_coords[k+1]) / 2 * 1000
    print(f"{k+1:<6} {stacking_sequence[k]:>4}°    {z_bot:>10.4f}   {z_top:>10.4f}   {z_mid:>10.4f}")

# =============================================================================
# CALCULATE ABD MATRICES
# =============================================================================
A = np.zeros((3, 3))
B = np.zeros((3, 3))
D = np.zeros((3, 3))

for k in range(n_plies):
    Qbar = calculate_Qbar(stacking_sequence[k])
    z_bot = z_coords[k]
    z_top = z_coords[k+1]
    
    A += Qbar * (z_top - z_bot)
    B += 0.5 * Qbar * (z_top**2 - z_bot**2)
    D += (1/3) * Qbar * (z_top**3 - z_bot**3)

print("\n" + "-" * 70)
print("A MATRIX (Extensional Stiffness) [N/m]")
print("-" * 70)
for i in range(3):
    print(f"[{A[i,0]:15.4e}  {A[i,1]:15.4e}  {A[i,2]:15.4e}]")

print("\n" + "-" * 70)
print("B MATRIX (Coupling Stiffness) [N]")
print("-" * 70)
for i in range(3):
    print(f"[{B[i,0]:15.4e}  {B[i,1]:15.4e}  {B[i,2]:15.4e}]")

print("\n" + "-" * 70)
print("D MATRIX (Bending Stiffness) [N·m]")
print("-" * 70)
for i in range(3):
    print(f"[{D[i,0]:15.4e}  {D[i,1]:15.4e}  {D[i,2]:15.4e}]")

# Assemble 6x6 ABD matrix
ABD = np.zeros((6, 6))
ABD[0:3, 0:3] = A
ABD[0:3, 3:6] = B
ABD[3:6, 0:3] = B
ABD[3:6, 3:6] = D

# Calculate compliance matrix (inverse of ABD)
abd = np.linalg.inv(ABD)

# =============================================================================
# PART (a): MID-PLANE STRAINS AND CURVATURES
# =============================================================================
print("\n" + "=" * 70)
print("PART (a): MID-PLANE STRAINS AND CURVATURES")
print("=" * 70)

# Solve for strains and curvatures: [ε°, κ] = [abd] × [N, M]
strain_curvature = abd @ load_vec

eps0_x = strain_curvature[0]
eps0_y = strain_curvature[1]
gamma0_xy = strain_curvature[2]
kappa_x = strain_curvature[3]
kappa_y = strain_curvature[4]
kappa_xy = strain_curvature[5]

print("\nMid-plane Strains:")
print(f"  ε°x  = {eps0_x:15.6e} = {eps0_x*1e6:10.2f} με")
print(f"  ε°y  = {eps0_y:15.6e} = {eps0_y*1e6:10.2f} με")
print(f"  γ°xy = {gamma0_xy:15.6e} = {gamma0_xy*1e6:10.2f} με")

print("\nCurvatures:")
print(f"  κx  = {kappa_x:15.6e} 1/m = {kappa_x:10.6f} 1/m")
print(f"  κy  = {kappa_y:15.6e} 1/m = {kappa_y:10.6f} 1/m")
print(f"  κxy = {kappa_xy:15.6e} 1/m = {kappa_xy:10.6f} 1/m")

eps0 = np.array([eps0_x, eps0_y, gamma0_xy])
kappa = np.array([kappa_x, kappa_y, kappa_xy])

# =============================================================================
# PART (b): GLOBAL STRESSES VS. VERTICAL LOCATION
# =============================================================================
print("\n" + "=" * 70)
print("PART (b): GLOBAL STRESSES VS. VERTICAL LOCATION")
print("=" * 70)

# Calculate stresses at top and bottom of each ply
z_plot = []
sigma_x_plot = []
sigma_y_plot = []
tau_xy_plot = []

# Also store for failure analysis
ply_stresses_global = []
ply_stresses_local = []

print("\n" + "-" * 70)
print("GLOBAL STRESSES AT PLY INTERFACES")
print("-" * 70)
print(f"{'Ply':<5} {'Loc':<6} {'z (mm)':<10} {'σx (MPa)':<12} {'σy (MPa)':<12} {'τxy (MPa)':<12}")
print("-" * 70)

for k in range(n_plies):
    theta = stacking_sequence[k]
    Qbar = calculate_Qbar(theta)
    
    # Bottom of ply
    z_bot = z_coords[k]
    eps_bot = eps0 + z_bot * kappa
    sigma_bot = Qbar @ eps_bot
    
    # Top of ply
    z_top = z_coords[k+1]
    eps_top = eps0 + z_top * kappa
    sigma_top = Qbar @ eps_top
    
    # Store for plotting (global stresses in Pa, convert to MPa for display)
    z_plot.extend([z_bot*1000, z_top*1000])
    sigma_x_plot.extend([sigma_bot[0]/1e6, sigma_top[0]/1e6])
    sigma_y_plot.extend([sigma_bot[1]/1e6, sigma_top[1]/1e6])
    tau_xy_plot.extend([sigma_bot[2]/1e6, sigma_top[2]/1e6])
    
    print(f"{k+1:<5} {'Bot':<6} {z_bot*1000:>8.4f}   {sigma_bot[0]/1e6:>10.4f}   {sigma_bot[1]/1e6:>10.4f}   {sigma_bot[2]/1e6:>10.4f}")
    print(f"{'':<5} {'Top':<6} {z_top*1000:>8.4f}   {sigma_top[0]/1e6:>10.4f}   {sigma_top[1]/1e6:>10.4f}   {sigma_top[2]/1e6:>10.4f}")
    
    # Store for failure analysis (average stress in ply)
    sigma_avg = (sigma_bot + sigma_top) / 2
    ply_stresses_global.append({
        'ply': k+1,
        'theta': theta,
        'sigma_bot': sigma_bot,
        'sigma_top': sigma_top,
        'sigma_avg': sigma_avg
    })

# Create plot
fig, axes = plt.subplots(1, 3, figsize=(14, 8))

# Plot σx
ax1 = axes[0]
ax1.plot(sigma_x_plot, z_plot, 'b-o', linewidth=2, markersize=4)
ax1.axvline(x=0, color='k', linestyle='--', linewidth=0.5)
ax1.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
for z in z_coords * 1000:
    ax1.axhline(y=z, color='gray', linestyle=':', linewidth=0.5)
ax1.set_xlabel('σx (MPa)', fontsize=12)
ax1.set_ylabel('z (mm)', fontsize=12)
ax1.set_title('σx vs. z', fontsize=14)
ax1.grid(True, alpha=0.3)

# Plot σy
ax2 = axes[1]
ax2.plot(sigma_y_plot, z_plot, 'r-s', linewidth=2, markersize=4)
ax2.axvline(x=0, color='k', linestyle='--', linewidth=0.5)
ax2.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
for z in z_coords * 1000:
    ax2.axhline(y=z, color='gray', linestyle=':', linewidth=0.5)
ax2.set_xlabel('σy (MPa)', fontsize=12)
ax2.set_ylabel('z (mm)', fontsize=12)
ax2.set_title('σy vs. z', fontsize=14)
ax2.grid(True, alpha=0.3)

# Plot τxy
ax3 = axes[2]
ax3.plot(tau_xy_plot, z_plot, 'g-^', linewidth=2, markersize=4)
ax3.axvline(x=0, color='k', linestyle='--', linewidth=0.5)
ax3.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
for z in z_coords * 1000:
    ax3.axhline(y=z, color='gray', linestyle=':', linewidth=0.5)
ax3.set_xlabel('τxy (MPa)', fontsize=12)
ax3.set_ylabel('z (mm)', fontsize=12)
ax3.set_title('τxy vs. z', fontsize=14)
ax3.grid(True, alpha=0.3)

plt.suptitle('[30/45/-45/-30]T Laminate - Global Stresses vs. z\n(Nx=Ny=1000 N/m, My=Mxy=50 N)', fontsize=14)
plt.tight_layout()
plt.savefig('c:/Users/z003n5uc/Desktop/STP604E/assignment_2/assignment_3/problem3_global_stresses.png', dpi=300, bbox_inches='tight')
plt.show()

# =============================================================================
# PART (c): TSAI-HILL FAILURE CRITERION
# =============================================================================
print("\n" + "=" * 70)
print("PART (c): TSAI-HILL FAILURE CRITERION")
print("=" * 70)

def tsai_hill_criterion(sigma1, sigma2, tau12, Xt, Xc, Yt, Yc, S):
    """
    Calculate Tsai-Hill failure index
    Uses appropriate strength based on sign of stress
    
    Tsai-Hill: (σ1/X)² - (σ1×σ2/X²) + (σ2/Y)² + (τ12/S)² = 1 at failure
    
    Returns failure index (FI). FI ≥ 1 means failure.
    """
    # Select appropriate strength based on stress sign
    X = Xt if sigma1 >= 0 else Xc
    Y = Yt if sigma2 >= 0 else Yc
    
    # Tsai-Hill failure index
    FI = (sigma1/X)**2 - (sigma1*sigma2)/(X**2) + (sigma2/Y)**2 + (tau12/S)**2
    
    return FI, X, Y

print("\nLocal (Material) Stresses and Tsai-Hill Failure Analysis:")
print("-" * 90)
print(f"{'Ply':<5} {'θ':<6} {'Loc':<5} {'σ1 (MPa)':<12} {'σ2 (MPa)':<12} {'τ12 (MPa)':<12} {'FI':<10} {'Status':<10}")
print("-" * 90)

failure_detected = False
max_FI = 0
critical_ply = None

for k in range(n_plies):
    theta = stacking_sequence[k]
    Qbar = calculate_Qbar(theta)
    T_stress = calculate_T_stress(theta)
    
    # Bottom and top of ply
    for loc, z in [('Bot', z_coords[k]), ('Top', z_coords[k+1])]:
        # Global strain at this z
        eps_global = eps0 + z * kappa
        
        # Global stress
        sigma_global = Qbar @ eps_global
        
        # Transform to local (material) stress
        sigma_local = T_stress @ sigma_global
        sigma1 = sigma_local[0]
        sigma2 = sigma_local[1]
        tau12 = sigma_local[2]
        
        # Tsai-Hill failure index
        FI, X_used, Y_used = tsai_hill_criterion(sigma1, sigma2, tau12, Xt, Xc, Yt, Yc, S)
        
        status = "FAIL" if FI >= 1 else "Safe"
        if FI >= 1:
            failure_detected = True
        if FI > max_FI:
            max_FI = FI
            critical_ply = k + 1
            critical_loc = loc
            critical_theta = theta
        
        print(f"{k+1:<5} {theta:>4}°  {loc:<5} {sigma1/1e6:>10.4f}   {sigma2/1e6:>10.4f}   {tau12/1e6:>10.4f}   {FI:>8.4f}   {status:<10}")

print("-" * 90)

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY OF RESULTS")
print("=" * 70)

print(f"""
PART (a) - MID-PLANE STRAINS AND CURVATURES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Mid-plane Strains:
  ε°x  = {eps0_x*1e6:12.4f} με
  ε°y  = {eps0_y*1e6:12.4f} με  
  γ°xy = {gamma0_xy*1e6:12.4f} με

Curvatures:
  κx  = {kappa_x:12.6f} 1/m
  κy  = {kappa_y:12.6f} 1/m
  κxy = {kappa_xy:12.6f} 1/m

PART (b) - GLOBAL STRESSES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━
See plot saved to 'problem3_global_stresses.png'
Stresses vary linearly through each ply and show discontinuities
at ply interfaces due to different ply orientations.

PART (c) - TSAI-HILL FAILURE ANALYSIS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Maximum Failure Index: FI = {max_FI:.4f}
Critical Location: Ply {critical_ply} ({critical_theta}°) at {critical_loc}
""")

if failure_detected:
    print("⚠️  FAILURE DETECTED: One or more plies have exceeded the Tsai-Hill criterion!")
else:
    if max_FI < 1:
        print(f"✓ NO FAILURE: All plies are safe. Maximum FI = {max_FI:.4f} < 1")
        print(f"  Safety Factor = {1/np.sqrt(max_FI):.2f} (based on Tsai-Hill)")
    
print(f"""
Notes:
- Tsai-Hill criterion uses appropriate strength (tensile/compressive) 
  based on the sign of the stress component.
- Failure Index (FI) ≥ 1 indicates failure.
- The laminate is unsymmetric [30/45/-45/-30]T, so B ≠ 0 
  (coupling between extension and bending).
""")

print("\n✓ Stress plot saved to 'problem3_global_stresses.png'")
