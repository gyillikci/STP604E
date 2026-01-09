"""
Assignment 3 - Problem 4: Laminate Design Optimization
16-ply Zylon/Epoxy Laminate Design

Given:
- 16 plies, angles limited to (0°, ±30°, ±60°, 90°)
- Applied stresses: σx = 250 MPa, σy = 50 MPa, τxy = 150 MPa
- Strain limits: εx ≤ 0.006, εy ≤ 0.0006, γxy ≤ 0.02

Find:
a. All stacking sequences satisfying strain limits
b. Stacking sequence with minimum |αx|
c. Check individual ply failure
"""

import numpy as np
import matplotlib.pyplot as plt
from itertools import product
from collections import Counter

# =============================================================================
# MATERIAL PROPERTIES (Zylon/Epoxy)
# =============================================================================
E1 = 120.0e3    # MPa (120 GPa)
E2 = 6.5e3      # MPa (6.5 GPa)
G12 = 3.0e3     # MPa (3.0 GPa)
nu12 = 0.32
nu21 = nu12 * E2 / E1
t_ply = 1.0     # mm (assume unit thickness, will normalize)

# Thermal expansion coefficients
alpha1 = -0.8e-6    # 1/°C (fiber direction - negative for Zylon!)
alpha2 = 20.5e-6    # 1/°C (transverse direction)

# =============================================================================
# APPLIED STRESSES AND STRAIN LIMITS
# =============================================================================
sigma_x = 250   # MPa
sigma_y = 50    # MPa
tau_xy = 150    # MPa

# Strain limits (these are allowable strains)
eps_x_limit = 0.006     # 6000 με
eps_y_limit = 0.0006    # 600 με
gamma_xy_limit = 0.02   # 20000 με

print("=" * 70)
print("PROBLEM 4: LAMINATE DESIGN OPTIMIZATION")
print("=" * 70)
print(f"\nMaterial: Zylon/Epoxy")
print(f"E1 = {E1/1000:.1f} GPa, E2 = {E2/1000:.2f} GPa, G12 = {G12/1000:.1f} GPa, nu12 = {nu12}")
print(f"\nApplied Stresses:")
print(f"  σx = {sigma_x} MPa, σy = {sigma_y} MPa, τxy = {tau_xy} MPa")
print(f"\nStrain Limits:")
print(f"  |εx| ≤ {eps_x_limit} ({eps_x_limit*1e6:.0f} με)")
print(f"  |εy| ≤ {eps_y_limit} ({eps_y_limit*1e6:.0f} με)")
print(f"  |γxy| ≤ {gamma_xy_limit} ({gamma_xy_limit*1e6:.0f} με)")

# Available angles
available_angles = [0, 30, -30, 60, -60, 90]
n_plies = 16

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

def calculate_alpha_bar(theta_deg):
    """Calculate transformed thermal expansion coefficients"""
    theta = np.radians(theta_deg)
    c = np.cos(theta)
    s = np.sin(theta)
    
    alpha_x = alpha1 * c**2 + alpha2 * s**2
    alpha_y = alpha1 * s**2 + alpha2 * c**2
    alpha_xy = 2 * (alpha1 - alpha2) * c * s
    
    return np.array([alpha_x, alpha_y, alpha_xy])

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
# LAMINATE PROPERTY FUNCTIONS
# =============================================================================
def calculate_laminate_properties(ply_counts):
    """
    Calculate A-bar matrix and alpha-bar for given ply counts
    ply_counts: dict with angle: count pairs
    Returns: A_bar (normalized A matrix), alpha_laminate (effective CTE)
    """
    # For a symmetric, balanced laminate with given ply distribution
    # A_bar = sum(Qbar_k * v_k) where v_k is volume fraction of angle k
    
    total_plies = sum(ply_counts.values())
    
    A_bar = np.zeros((3, 3))
    for angle, count in ply_counts.items():
        if count > 0:
            v_k = count / total_plies  # volume fraction
            Qbar = calculate_Qbar(angle)
            A_bar += Qbar * v_k
    
    # Effective thermal expansion: α_bar = [A_bar]^-1 * sum(Qbar_k * α_k * v_k)
    sum_Qalpha = np.zeros(3)
    for angle, count in ply_counts.items():
        if count > 0:
            v_k = count / total_plies
            Qbar = calculate_Qbar(angle)
            alpha_k = calculate_alpha_bar(angle)
            sum_Qalpha += Qbar @ alpha_k * v_k
    
    a_bar = np.linalg.inv(A_bar)
    alpha_laminate = a_bar @ sum_Qalpha
    
    return A_bar, a_bar, alpha_laminate

def check_strain_limits(a_bar, sigma):
    """Check if strains are within limits"""
    eps = a_bar @ sigma
    
    eps_x_ok = abs(eps[0]) <= eps_x_limit
    eps_y_ok = abs(eps[1]) <= eps_y_limit
    gamma_xy_ok = abs(eps[2]) <= gamma_xy_limit
    
    return eps_x_ok and eps_y_ok and gamma_xy_ok, eps

# =============================================================================
# PART (a): FIND ALL VALID STACKING SEQUENCES
# =============================================================================
print("\n" + "=" * 70)
print("PART (a): FINDING ALL VALID STACKING SEQUENCES")
print("=" * 70)

# Applied stress vector
sigma = np.array([sigma_x, sigma_y, tau_xy])

# For a symmetric, balanced laminate:
# - Need equal +θ and -θ plies (balanced: A16 = A26 = 0)
# - Symmetric about midplane (B = 0)
# - 16 plies total, 8 in each half

# Possible ply groupings for balanced laminate:
# n0: number of 0° plies
# n30: number of ±30° pairs (so 2*n30 total)
# n60: number of ±60° pairs (so 2*n60 total)
# n90: number of 90° plies

# Constraint: n0 + 2*n30 + 2*n60 + n90 = 16

print("\nSearching for symmetric, balanced laminates...")
print("Constraint: n0 + 2×n30 + 2×n60 + n90 = 16")
print("(For balanced: equal +30 and -30 plies, equal +60 and -60 plies)")

valid_laminates = []

# Search through all combinations
for n0 in range(17):  # 0 to 16 plies at 0°
    for n30 in range(9):  # 0 to 8 pairs of ±30°
        for n60 in range(9):  # 0 to 8 pairs of ±60°
            n90 = 16 - n0 - 2*n30 - 2*n60
            
            if n90 < 0 or n90 > 16:
                continue
            
            # Create ply count dictionary
            ply_counts = {
                0: n0,
                30: n30,
                -30: n30,
                60: n60,
                -60: n60,
                90: n90
            }
            
            # Calculate laminate properties
            A_bar, a_bar, alpha_lam = calculate_laminate_properties(ply_counts)
            
            # Check strain limits
            valid, strains = check_strain_limits(a_bar, sigma)
            
            if valid:
                # Check that A16, A26 are approximately zero (balanced)
                if abs(A_bar[0, 2]) < 1 and abs(A_bar[1, 2]) < 1:
                    valid_laminates.append({
                        'n0': n0,
                        'n30': n30,
                        'n60': n60,
                        'n90': n90,
                        'ply_counts': ply_counts.copy(),
                        'A_bar': A_bar,
                        'a_bar': a_bar,
                        'strains': strains,
                        'alpha': alpha_lam,
                        'alpha_x': alpha_lam[0]
                    })

print(f"\nFound {len(valid_laminates)} valid laminate configurations")

# Display valid laminates
print("\n" + "-" * 100)
print(f"{'#':<4} {'n0':<4} {'n±30':<6} {'n±60':<6} {'n90':<4} {'εx (με)':<12} {'εy (με)':<12} {'γxy (με)':<12} {'αx (10⁻⁶/°C)':<14}")
print("-" * 100)

for i, lam in enumerate(valid_laminates):
    eps = lam['strains']
    ax = lam['alpha_x']
    print(f"{i+1:<4} {lam['n0']:<4} {2*lam['n30']:<6} {2*lam['n60']:<6} {lam['n90']:<4} "
          f"{eps[0]*1e6:<12.2f} {eps[1]*1e6:<12.2f} {eps[2]*1e6:<12.2f} {ax*1e6:<14.4f}")

# =============================================================================
# PART (b): FIND MINIMUM |αx| STACKING SEQUENCE
# =============================================================================
print("\n" + "=" * 70)
print("PART (b): MINIMUM |αx| STACKING SEQUENCE")
print("=" * 70)

# Sort by |alpha_x|
valid_laminates.sort(key=lambda x: abs(x['alpha_x']))

best = valid_laminates[0]

print(f"\nBest laminate (minimum |αx|):")
print(f"  n0 = {best['n0']}, n±30 = {2*best['n30']}, n±60 = {2*best['n60']}, n90 = {best['n90']}")

# Generate actual stacking sequence (symmetric, balanced)
def generate_stacking_sequence(n0, n30, n60, n90):
    """Generate a symmetric, balanced stacking sequence"""
    # For symmetric laminate, we define half and mirror it
    # For balanced, pair +θ with -θ
    half = []
    
    # Add 0° plies
    half.extend([0] * (n0 // 2))
    
    # Add ±30° pairs
    for _ in range(n30 // 2):
        half.extend([30, -30])
    
    # Add ±60° pairs  
    for _ in range(n60 // 2):
        half.extend([60, -60])
    
    # Add 90° plies
    half.extend([90] * (n90 // 2))
    
    # Handle odd numbers (place at center for symmetry)
    center = []
    if n0 % 2 == 1:
        center.append(0)
    if n90 % 2 == 1:
        center.append(90)
    if n30 % 2 == 1:
        # Need a pair at center
        center.extend([30, -30])
    if n60 % 2 == 1:
        center.extend([60, -60])
    
    # Full sequence: [half | center | reversed(half)]
    if center:
        full_seq = half + center + half[::-1]
    else:
        full_seq = half + half[::-1]
    
    return full_seq

stacking_seq = generate_stacking_sequence(best['n0'], 2*best['n30'], 2*best['n60'], best['n90'])

# Make sure we have exactly 16 plies
while len(stacking_seq) < 16:
    # Add more plies to match distribution
    stacking_seq = generate_stacking_sequence(best['n0'], 2*best['n30'], 2*best['n60'], best['n90'])
    break

# Create a proper 16-ply sequence manually based on the best configuration
def create_symmetric_balanced_sequence(n0, n30_pairs, n60_pairs, n90):
    """Create symmetric balanced sequence [...]_s notation"""
    half_n0 = n0 // 2
    half_n90 = n90 // 2
    
    # Build half laminate
    half = []
    
    # Distribute plies for good balance
    # Strategy: alternate angle plies for better properties
    for _ in range(n30_pairs // 2):
        half.append(30)
        half.append(-30)
    
    for _ in range(n60_pairs // 2):
        half.append(60)
        half.append(-60)
    
    half.extend([0] * half_n0)
    half.extend([90] * half_n90)
    
    # Add remaining plies if odd
    center = []
    if n0 % 2:
        center.append(0)
    if n90 % 2:
        center.append(90)
    if n30_pairs % 2:
        center.extend([30, -30])
    if n60_pairs % 2:
        center.extend([60, -60])
    
    full = half + center + half[::-1]
    return full[:16]  # Ensure exactly 16 plies

best_sequence = create_symmetric_balanced_sequence(best['n0'], 2*best['n30'], 2*best['n60'], best['n90'])

# Verify the sequence
actual_counts = Counter(best_sequence)
print(f"\nGenerated Stacking Sequence: {best_sequence}")
print(f"Ply count verification: {dict(actual_counts)}")

# Recalculate properties for the actual sequence
def calculate_properties_from_sequence(sequence):
    """Calculate properties from actual stacking sequence"""
    n = len(sequence)
    h = n * t_ply
    
    z = np.zeros(n + 1)
    z[0] = -h / 2
    for i in range(n):
        z[i+1] = z[i] + t_ply
    
    A = np.zeros((3, 3))
    for k in range(n):
        Qbar = calculate_Qbar(sequence[k])
        A += Qbar * (z[k+1] - z[k])
    
    A_bar = A / h
    a_bar = np.linalg.inv(A_bar)
    
    # Thermal expansion
    sum_Qalpha = np.zeros(3)
    for k in range(n):
        Qbar = calculate_Qbar(sequence[k])
        alpha_k = calculate_alpha_bar(sequence[k])
        sum_Qalpha += Qbar @ alpha_k * (z[k+1] - z[k])
    sum_Qalpha /= h
    
    alpha_lam = a_bar @ sum_Qalpha
    
    return A_bar, a_bar, alpha_lam, z

A_bar, a_bar, alpha_lam, z_coords = calculate_properties_from_sequence(best_sequence)
strains = a_bar @ sigma

print(f"\n" + "-" * 70)
print("BEST LAMINATE PROPERTIES")
print("-" * 70)

print(f"\nStacking Sequence: {best_sequence}")

# Express in standard notation
def express_laminate_notation(seq):
    """Convert sequence to standard laminate notation"""
    n = len(seq)
    half = seq[:n//2]
    # Check if symmetric
    is_sym = seq == seq[::-1] or seq[:n//2] == seq[n//2:][::-1]
    
    notation = "[" + "/".join(str(a) for a in half) + "]"
    if is_sym:
        notation += "s"
    return notation

# Better notation
notation_parts = []
i = 0
temp_seq = best_sequence[:8]  # Half for symmetric
while i < len(temp_seq):
    angle = temp_seq[i]
    count = 1
    while i + count < len(temp_seq) and temp_seq[i + count] == angle:
        count += 1
    if count > 1:
        notation_parts.append(f"{angle}_{count}")
    else:
        notation_parts.append(str(angle))
    i += count

print(f"Standard Notation: [{'/'.join(notation_parts)}]s")

print(f"\nMid-plane Strains under applied load:")
print(f"  εx  = {strains[0]:.6f} = {strains[0]*1e6:.2f} με  (limit: ±{eps_x_limit*1e6:.0f} με) {'✓' if abs(strains[0]) <= eps_x_limit else '✗'}")
print(f"  εy  = {strains[1]:.6f} = {strains[1]*1e6:.2f} με  (limit: ±{eps_y_limit*1e6:.0f} με) {'✓' if abs(strains[1]) <= eps_y_limit else '✗'}")
print(f"  γxy = {strains[2]:.6f} = {strains[2]*1e6:.2f} με  (limit: ±{gamma_xy_limit*1e6:.0f} με) {'✓' if abs(strains[2]) <= gamma_xy_limit else '✗'}")

print(f"\nCoefficients of Thermal Expansion:")
print(f"  αx  = {alpha_lam[0]*1e6:.6f} × 10⁻⁶ /°C")
print(f"  αy  = {alpha_lam[1]*1e6:.6f} × 10⁻⁶ /°C")
print(f"  αxy = {alpha_lam[2]*1e6:.6f} × 10⁻⁶ /°C")
print(f"\n  |αx| = {abs(alpha_lam[0])*1e6:.6f} × 10⁻⁶ /°C  ← MINIMUM among valid laminates")

# =============================================================================
# PLOT αx CONTOUR
# =============================================================================
print("\n" + "-" * 70)
print("GENERATING αx CONTOUR PLOT")
print("-" * 70)

# Create contour data using lamination parameters approach
# For visualization, we'll vary n0 and n90 (keeping n30+n60 to complete 16)

fig, ax = plt.subplots(figsize=(12, 10))

# Plot all valid points
n0_vals = [lam['n0'] for lam in valid_laminates]
n90_vals = [lam['n90'] for lam in valid_laminates]
alpha_x_vals = [lam['alpha_x']*1e6 for lam in valid_laminates]

scatter = ax.scatter(n0_vals, n90_vals, c=alpha_x_vals, cmap='coolwarm', 
                     s=100, edgecolors='black', linewidths=1)
plt.colorbar(scatter, label='αx (×10⁻⁶ /°C)')

# Mark the best one
best_idx = 0  # Already sorted, best is first
ax.scatter([best['n0']], [best['n90']], c='lime', s=300, marker='*', 
           edgecolors='black', linewidths=2, label=f'Minimum |αx| = {best["alpha_x"]*1e6:.4f}×10⁻⁶/°C', zorder=5)

# Add annotations for each point
for i, lam in enumerate(valid_laminates):
    ax.annotate(f'{lam["alpha_x"]*1e6:.3f}', 
                (lam['n0'], lam['n90']), 
                textcoords="offset points", 
                xytext=(0, 10), 
                ha='center', fontsize=8)

ax.set_xlabel('Number of 0° plies (n0)', fontsize=12)
ax.set_ylabel('Number of 90° plies (n90)', fontsize=12)
ax.set_title('αx Contour for Valid Laminate Configurations\n(16-ply symmetric, balanced laminates satisfying strain limits)', fontsize=12)
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)

# Set integer ticks
ax.set_xticks(range(0, 17, 2))
ax.set_yticks(range(0, 17, 2))

plt.tight_layout()
plt.savefig('c:/Users/z003n5uc/Desktop/STP604E/assignment_2/assignment_3/problem4_alpha_contour.png', dpi=300, bbox_inches='tight')
plt.show()

# =============================================================================
# PART (c): CHECK INDIVIDUAL PLY FAILURE
# =============================================================================
print("\n" + "=" * 70)
print("PART (c): INDIVIDUAL PLY FAILURE CHECK")
print("=" * 70)

print(f"\nPly strain limits (same as laminate limits):")
print(f"  |ε1| ≤ {eps_x_limit} ({eps_x_limit*1e6:.0f} με)")
print(f"  |ε2| ≤ {eps_y_limit} ({eps_y_limit*1e6:.0f} με)")
print(f"  |γ12| ≤ {gamma_xy_limit} ({gamma_xy_limit*1e6:.0f} με)")

# For thin plate under in-plane loading only, strain is constant through thickness
# (no curvature for symmetric laminate under in-plane load only)
global_strain = strains

print(f"\nGlobal strains (constant through thickness for symmetric laminate):")
print(f"  εx = {global_strain[0]*1e6:.2f} με")
print(f"  εy = {global_strain[1]*1e6:.2f} με")
print(f"  γxy = {global_strain[2]*1e6:.2f} με")

print("\n" + "-" * 90)
print(f"{'Ply':<5} {'θ':<6} {'ε1 (με)':<12} {'ε2 (με)':<12} {'γ12 (με)':<12} {'Status':<15}")
print("-" * 90)

any_failure = False
ply_results = []

unique_angles = sorted(set(best_sequence))

for k, theta in enumerate(best_sequence):
    # Transform global strain to local strain
    T_strain = calculate_T_strain(theta)
    local_strain = T_strain @ global_strain
    
    eps1 = local_strain[0]
    eps2 = local_strain[1]
    gamma12 = local_strain[2]
    
    # Check limits
    eps1_ok = abs(eps1) <= eps_x_limit
    eps2_ok = abs(eps2) <= eps_y_limit
    gamma12_ok = abs(gamma12) <= gamma_xy_limit
    
    if eps1_ok and eps2_ok and gamma12_ok:
        status = "Safe ✓"
    else:
        status = "FAIL ✗"
        any_failure = True
        if not eps1_ok:
            status += " (ε1)"
        if not eps2_ok:
            status += " (ε2)"
        if not gamma12_ok:
            status += " (γ12)"
    
    print(f"{k+1:<5} {theta:>4}°  {eps1*1e6:>10.2f}   {eps2*1e6:>10.2f}   {gamma12*1e6:>10.2f}   {status:<15}")
    
    ply_results.append({
        'ply': k+1,
        'theta': theta,
        'eps1': eps1,
        'eps2': eps2,
        'gamma12': gamma12,
        'status': status
    })

print("-" * 90)

# Summary by angle
print("\nSummary by Ply Orientation:")
print("-" * 70)
for theta in unique_angles:
    T_strain = calculate_T_strain(theta)
    local_strain = T_strain @ global_strain
    print(f"  {theta:>4}° ply: ε1 = {local_strain[0]*1e6:>8.2f} με, ε2 = {local_strain[1]*1e6:>8.2f} με, γ12 = {local_strain[2]*1e6:>8.2f} με")

# =============================================================================
# FINAL SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("FINAL SUMMARY")
print("=" * 70)

print(f"""
PART (a) - VALID STACKING SEQUENCES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Found {len(valid_laminates)} valid symmetric, balanced laminate configurations
that satisfy all strain limits.

PART (b) - MINIMUM |αx| STACKING SEQUENCE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Optimal Configuration:
  • Stacking Sequence: {best_sequence}
  • Ply distribution: {best['n0']} plies at 0°, {2*best['n30']} plies at ±30°, 
                      {2*best['n60']} plies at ±60°, {best['n90']} plies at 90°
  
Mid-plane Strains:
  • εx  = {strains[0]*1e6:>10.2f} με  (limit: ±6000 με)
  • εy  = {strains[1]*1e6:>10.2f} με  (limit: ±600 με)
  • γxy = {strains[2]*1e6:>10.2f} με  (limit: ±20000 με)

Coefficient of Thermal Expansion:
  • αx  = {alpha_lam[0]*1e6:.6f} × 10⁻⁶ /°C  ← MINIMUM |αx|
  • αy  = {alpha_lam[1]*1e6:.6f} × 10⁻⁶ /°C
  • αxy = {alpha_lam[2]*1e6:.6f} × 10⁻⁶ /°C

PART (c) - INDIVIDUAL PLY FAILURE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

if any_failure:
    failed_plies = [r for r in ply_results if 'FAIL' in r['status']]
    print(f"⚠️  FAILURE DETECTED in {len(failed_plies)} plies!")
    for r in failed_plies:
        print(f"   Ply {r['ply']} ({r['theta']}°): {r['status']}")
else:
    print("✓ NO FAILURE: All individual plies satisfy the strain limits.")

print(f"""
Note: For a symmetric laminate under pure in-plane loading, 
the strains are constant through thickness (κ = 0).
""")

print("\n✓ αx contour plot saved to 'problem4_alpha_contour.png'")

# =============================================================================
# ADDITIONAL ANALYSIS: Find laminates with NO ply failures
# =============================================================================
print("\n" + "=" * 70)
print("ADDITIONAL ANALYSIS: LAMINATES WITH NO PLY FAILURE")
print("=" * 70)

def check_ply_failure(ply_counts, global_strain):
    """Check if any ply fails under given global strain"""
    angles_to_check = []
    for angle, count in ply_counts.items():
        if count > 0:
            angles_to_check.append(angle)
    
    for theta in angles_to_check:
        T_strain = calculate_T_strain(theta)
        local_strain = T_strain @ global_strain
        
        eps1 = local_strain[0]
        eps2 = local_strain[1]
        gamma12 = local_strain[2]
        
        if abs(eps1) > eps_x_limit or abs(eps2) > eps_y_limit or abs(gamma12) > gamma_xy_limit:
            return False, theta, local_strain
    
    return True, None, None

# Check all valid laminates for ply-level failure
laminates_no_failure = []

for lam in valid_laminates:
    no_failure, fail_angle, fail_strain = check_ply_failure(lam['ply_counts'], lam['strains'])
    lam['ply_level_ok'] = no_failure
    if no_failure:
        laminates_no_failure.append(lam)

print(f"\nOut of {len(valid_laminates)} valid laminates, {len(laminates_no_failure)} have NO ply-level failure.")

if laminates_no_failure:
    # Sort by |alpha_x|
    laminates_no_failure.sort(key=lambda x: abs(x['alpha_x']))
    
    print("\n" + "-" * 100)
    print("LAMINATES WITH NO PLY FAILURE (sorted by |αx|):")
    print("-" * 100)
    print(f"{'#':<4} {'n0':<4} {'n±30':<6} {'n±60':<6} {'n90':<4} {'εx (με)':<12} {'εy (με)':<12} {'γxy (με)':<12} {'αx (10⁻⁶/°C)':<14}")
    print("-" * 100)
    
    for i, lam in enumerate(laminates_no_failure[:20]):
        eps = lam['strains']
        ax = lam['alpha_x']
        print(f"{i+1:<4} {lam['n0']:<4} {2*lam['n30']:<6} {2*lam['n60']:<6} {lam['n90']:<4} "
              f"{eps[0]*1e6:<12.2f} {eps[1]*1e6:<12.2f} {eps[2]*1e6:<12.2f} {ax*1e6:<14.4f}")
    
    # Best among those with no ply failure
    best_safe = laminates_no_failure[0]
    print(f"\n" + "=" * 70)
    print("BEST LAMINATE WITH NO PLY FAILURE (minimum |αx|)")
    print("=" * 70)
    
    print(f"\nPly distribution: {best_safe['n0']} plies at 0°, {2*best_safe['n30']} plies at ±30°, " 
          f"{2*best_safe['n60']} plies at ±60°, {best_safe['n90']} plies at 90°")
    
    eps = best_safe['strains']
    print(f"\nMid-plane Strains:")
    print(f"  εx  = {eps[0]*1e6:>10.2f} με  (limit: ±6000 με)")
    print(f"  εy  = {eps[1]*1e6:>10.2f} με  (limit: ±600 με)")
    print(f"  γxy = {eps[2]*1e6:>10.2f} με  (limit: ±20000 με)")
    
    print(f"\nCoefficient of Thermal Expansion:")
    print(f"  αx  = {best_safe['alpha_x']*1e6:.6f} × 10⁻⁶ /°C")
    
    # Verify ply strains
    print("\nPly-level strain verification:")
    for theta in sorted(set([0, 30, -30, 60, -60, 90])):
        if best_safe['ply_counts'].get(theta, 0) > 0 or best_safe['ply_counts'].get(-theta, 0) > 0:
            if best_safe['ply_counts'].get(theta, 0) > 0:
                T_strain = calculate_T_strain(theta)
                local_strain = T_strain @ best_safe['strains']
                status = "✓" if (abs(local_strain[0]) <= eps_x_limit and 
                                 abs(local_strain[1]) <= eps_y_limit and 
                                 abs(local_strain[2]) <= gamma_xy_limit) else "✗"
                print(f"  {theta:>4}° ply: ε1 = {local_strain[0]*1e6:>8.2f} με, "
                      f"ε2 = {local_strain[1]*1e6:>8.2f} με, γ12 = {local_strain[2]*1e6:>8.2f} με {status}")
else:
    print("\n⚠️  No laminates found that satisfy both laminate AND ply-level strain limits!")
    print("This means the ply strain limit εy = 0.0006 is too restrictive for off-axis plies.")

