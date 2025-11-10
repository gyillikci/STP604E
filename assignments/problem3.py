import numpy as np
from math import cos, sin, radians
import matplotlib.pyplot as plt

# Material properties (Kevlar/Epoxy)
E1 = 76000  # MPa
E2 = 5500   # MPa
G12 = 2300  # MPa
nu12 = 0.34
nu21 = (E2/E1)*nu12
ply_thick = 1.25  # mm
num_plies = 8

# Calculate reduced stiffness matrix Q
Q = np.zeros((3,3))
Q[0,0] = E1/(1 - nu12*nu21)
Q[1,1] = E2/(1 - nu12*nu21)
Q[0,1] = Q[1,0] = nu12*E2/(1 - nu12*nu21)
Q[2,2] = G12

def Q_bar(Q, theta_deg):
    th = radians(theta_deg)
    m = cos(th)
    n = sin(th)
    Q11, Q22, Q12, Q66 = Q[0,0], Q[1,1], Q[0,1], Q[2,2]
    Q11b = Q11*m**4 + 2*(Q12+2*Q66)*m**2*n**2 + Q22*n**4
    Q12b = (Q11+Q22-4*Q66)*m**2*n**2 + Q12*(m**4 + n**4)
    Q22b = Q11*n**4 + 2*(Q12+2*Q66)*m**2*n**2 + Q22*m**4
    Q16b = (Q11 - Q12 - 2*Q66)*m**3*n - (Q22 - Q12 - 2*Q66)*m*n**3
    Q26b = (Q11 - Q12 - 2*Q66)*m*n**3 - (Q22 - Q12 - 2*Q66)*m**3*n
    Q66b = (Q11 + Q22 - 2*Q12 - 2*Q66)*m**2*n**2 + Q66*(m**2 - n**2)**2
    return np.array([[Q11b, Q12b, Q16b],
                     [Q12b, Q22b, Q26b],
                     [Q16b, Q26b, Q66b]])

# Loadings (N/m and N)
Nx, Ny, Nxy = 1000, 1000, 0
Mx, My, Mxy = 0, 50, 50
NM = np.array([Nx, Ny, Nxy, Mx, My, Mxy])

# Sweep theta from -90 to +90 degrees
thetas = np.linspace(-90, 90, 181)
mid_strains = []
mid_curvs = []

for th in thetas:
    # Stacking sequence symmetric: [30, th, th, -30]_s
    seq = [30, th, th, -30, -30, th, th, 30]
    z = np.linspace(-num_plies*ply_thick/2, num_plies*ply_thick/2, num_plies+1)

    A = np.zeros((3,3))
    B = np.zeros((3,3))
    D = np.zeros((3,3))

    for i, theta in enumerate(seq):
        Qb = Q_bar(Q, theta)
        dz = z[i+1] - z[i]
        dzz2 = z[i+1]**2 - z[i]**2
        dzz3 = z[i+1]**3 - z[i]**3
        A += Qb * dz
        B += Qb * dzz2 / 2
        D += Qb * dzz3 / 3

    ABD = np.block([[A, B], [B, D]])

    # Enforce constraint γ_xy⁰ = 0 by zeroing shear coupling row and column
    ABD_mod = ABD.copy()
    ABD_mod[2,:] = 0
    ABD_mod[:,2] = 0

    # Solve for mid-plane strains and curvatures
    eps_kappa = np.linalg.pinv(ABD_mod) @ NM

    mid_strains.append([eps_kappa[0], eps_kappa[1], 0])  # [ε_x, ε_y, γ_xy=0]
    mid_curvs.append([eps_kappa[3], eps_kappa[4]])       # [κ_x, κ_y]

# Convert to numpy arrays for plotting
mid_strains = np.array(mid_strains)
mid_curvs = np.array(mid_curvs)

# Print summary
print("\n" + "="*70)
print("PROBLEM 3: LAMINATE ANALYSIS WITH CONSTRAINT")
print("="*70)
print("Laminate: [30/theta/theta/-30]_s")
print("Constraint: gamma_xy0 = 0 (enforced)")
print("\nMaterial: Kevlar/Epoxy")
print(f"  E1 = {E1} MPa")
print(f"  E2 = {E2} MPa")
print(f"  G12 = {G12} MPa")
print(f"  nu12 = {nu12}")
print(f"\nLoads:")
print(f"  Nx = {Nx} N/m, Ny = {Ny} N/m, Nxy = {Nxy} N/m")
print(f"  Mx = {Mx} N, My = {My} N, Mxy = {Mxy} N")
print("\nAnalysis: Varying theta from -90 to +90 degrees")
print("="*70)

# Find some interesting values
idx_0 = np.argmin(np.abs(thetas - 0))
idx_30 = np.argmin(np.abs(thetas - 30))
idx_n30 = np.argmin(np.abs(thetas - (-30)))

print(f"\nResults at theta = 0 degrees:")
print(f"  epsilon_x = {mid_strains[idx_0,0]:.6e}")
print(f"  epsilon_y = {mid_strains[idx_0,1]:.6e}")
print(f"  kappa_x = {mid_curvs[idx_0,0]:.6e} /mm")
print(f"  kappa_y = {mid_curvs[idx_0,1]:.6e} /mm")

print(f"\nResults at theta = 30 degrees:")
print(f"  epsilon_x = {mid_strains[idx_30,0]:.6e}")
print(f"  epsilon_y = {mid_strains[idx_30,1]:.6e}")
print(f"  kappa_x = {mid_curvs[idx_30,0]:.6e} /mm")
print(f"  kappa_y = {mid_curvs[idx_30,1]:.6e} /mm")

print(f"\nResults at theta = -30 degrees:")
print(f"  epsilon_x = {mid_strains[idx_n30,0]:.6e}")
print(f"  epsilon_y = {mid_strains[idx_n30,1]:.6e}")
print(f"  kappa_x = {mid_curvs[idx_n30,0]:.6e} /mm")
print(f"  kappa_y = {mid_curvs[idx_n30,1]:.6e} /mm")
print("="*70)

# Plot results
plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
plt.plot(thetas, mid_strains[:,0], label='ε_x')
plt.plot(thetas, mid_strains[:,1], label='ε_y')
plt.title('Mid-plane Strains vs θ')
plt.xlabel('θ (degrees)')
plt.ylabel('Strain')
plt.legend()
plt.grid(True)

plt.subplot(1,2,2)
plt.plot(thetas, mid_curvs[:,0], label='κ_x')
plt.plot(thetas, mid_curvs[:,1], label='κ_y')
plt.title('Mid-plane Curvatures vs θ')
plt.xlabel('θ (degrees)')
plt.ylabel('Curvature (1/mm)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('problem3_results.png', dpi=300, bbox_inches='tight')
print("\nPlot saved to 'problem3_results.png'")
plt.close()
