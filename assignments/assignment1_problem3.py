"""
Assignment 1 - Problem 3: Laminate Analysis with Constraint

Problem Statement:
Consider a laminate with stacking sequence [30/θ₁/θ₂/-30]_s subjected to:
  N_x = N_y = 1000 N/m
  M_y = M_xy = 50 N

Material: Kevlar/Epoxy
  E₁ = 76 GPa, E₂ = 5.50 GPa, G₁₂ = 2.30 GPa, ν₁₂ = 0.34, t = 1.25 mm

Constraint: No shear strain (γ_xy⁰ = 0)

Determine and plot mid-plane strains and curvatures as a function of θ.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from scipy.optimize import fsolve
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from composite_lib import Laminate


def solve_problem3():
    """
    Solve Assignment 1 - Problem 3
    Find θ₁ and θ₂ such that γ_xy = 0
    """
    print("\n" + "="*70)
    print("ASSIGNMENT 1 - PROBLEM 3: LAMINATE WITH ZERO SHEAR STRAIN")
    print("="*70)

    # Material properties - Kevlar/Epoxy
    material = {
        'E1': 76.0,    # GPa
        'E2': 5.50,    # GPa
        'G12': 2.30,   # GPa
        'nu12': 0.34
    }

    t = 1.25  # mm - ply thickness

    # Applied loads
    Nx = 1000   # N/m
    Ny = 1000   # N/m
    Nxy = 0     # N/m
    Mx = 0      # N
    My = 50     # N
    Mxy = 50    # N

    loads = np.array([Nx, Ny, Nxy, Mx, My, Mxy])

    print("\nMaterial Properties (Kevlar/Epoxy):")
    print(f"  E₁  = {material['E1']} GPa")
    print(f"  E₂  = {material['E2']} GPa")
    print(f"  G₁₂ = {material['G12']} GPa")
    print(f"  ν₁₂ = {material['nu12']}")
    print(f"  t   = {t} mm")

    print("\nApplied Loads:")
    print(f"  N_x  = {Nx} N/m")
    print(f"  N_y  = {Ny} N/m")
    print(f"  N_xy = {Nxy} N/m")
    print(f"  M_x  = {Mx} N")
    print(f"  M_y  = {My} N")
    print(f"  M_xy = {Mxy} N")

    print("\nStacking Sequence: [30/θ₁/θ₂/-30]_s")
    print("Constraint: γ_xy⁰ = 0 (zero mid-plane shear strain)")

    # Approach: Assume θ₁ = θ₂ = θ for simplicity and symmetry
    # Then find θ such that γ_xy = 0

    print("\n" + "-"*70)
    print("STEP 1: Find θ such that γ_xy⁰ = 0")
    print("-"*70)
    print("\nAssuming θ₁ = θ₂ = θ for symmetric solution")

    def shear_strain_constraint(theta):
        """Calculate shear strain for given theta"""
        stacking = [30, theta, theta, -30, -30, theta, theta, 30]
        lam = Laminate(material, stacking, t)
        strains, _ = lam.calculate_strains_curvatures(loads)
        return strains[2]  # γ_xy

    # Find theta that gives zero shear strain
    theta_initial_guess = 0
    theta_solution = fsolve(shear_strain_constraint, theta_initial_guess)[0]

    print(f"\nSolution: θ = {theta_solution:.2f}°")

    # Verify solution
    stacking_solution = [30, theta_solution, theta_solution, -30,
                        -30, theta_solution, theta_solution, 30]
    lam_solution = Laminate(material, stacking_solution, t)
    strains_sol, curvatures_sol = lam_solution.calculate_strains_curvatures(loads)

    print(f"\nVerification with θ = {theta_solution:.2f}°:")
    print(f"  ε_x⁰  = {strains_sol[0]*1e6:.3f} με")
    print(f"  ε_y⁰  = {strains_sol[1]*1e6:.3f} με")
    print(f"  γ_xy⁰ = {strains_sol[2]*1e6:.6f} με  ← Should be ≈ 0")
    print(f"\n  κ_x   = {curvatures_sol[0]:.6f} mm⁻¹")
    print(f"  κ_y   = {curvatures_sol[1]:.6f} mm⁻¹")
    print(f"  κ_xy  = {curvatures_sol[2]:.6f} mm⁻¹")

    # Step 2: Plot strains and curvatures vs θ
    print("\n" + "-"*70)
    print("STEP 2: Parametric Study - Vary θ from -90° to 90°")
    print("-"*70)

    theta_range = np.linspace(-90, 90, 181)

    strains_x = []
    strains_y = []
    strains_xy = []
    curv_x = []
    curv_y = []
    curv_xy = []

    for theta in theta_range:
        stacking = [30, theta, theta, -30, -30, theta, theta, 30]
        lam = Laminate(material, stacking, t)
        strains, curvatures = lam.calculate_strains_curvatures(loads)

        strains_x.append(strains[0] * 1e6)  # Convert to microstrain
        strains_y.append(strains[1] * 1e6)
        strains_xy.append(strains[2] * 1e6)
        curv_x.append(curvatures[0])
        curv_y.append(curvatures[1])
        curv_xy.append(curvatures[2])

    # Create plots
    create_plots(theta_range, theta_solution,
                strains_x, strains_y, strains_xy,
                curv_x, curv_y, curv_xy,
                strains_sol, curvatures_sol)

    # Discussion
    print("\n" + "-"*70)
    print("DISCUSSION")
    print("-"*70)
    print(f"""
The analysis shows that for the laminate [30/θ/θ/-30]_s:

1. Zero Shear Strain Condition:
   - The angle θ ≈ {theta_solution:.2f}° produces zero mid-plane shear strain
   - This is due to the balanced arrangement of plies around this angle

2. Strain Behavior:
   - ε_x⁰ and ε_y⁰ vary with θ but remain relatively stable
   - γ_xy⁰ varies significantly, crossing zero at θ = {theta_solution:.2f}°
   - The shear strain is highly sensitive to ply orientation

3. Curvature Behavior:
   - All curvatures show variation with θ
   - The coupling between bending moments and curvatures depends on
     the laminate stacking sequence
   - Even with symmetric layup, [B] ≠ 0 for non-symmetric angles

4. Physical Interpretation:
   - The constraint γ_xy⁰ = 0 can be achieved by proper selection of θ
   - This demonstrates the design flexibility of composite laminates
   - Such constraints are important in applications requiring specific
     deformation patterns
    """)

    print("="*70 + "\n")

    return {
        'theta_solution': theta_solution,
        'strains': strains_sol,
        'curvatures': curvatures_sol,
        'theta_range': theta_range,
        'results': {
            'strains_x': strains_x,
            'strains_y': strains_y,
            'strains_xy': strains_xy,
            'curv_x': curv_x,
            'curv_y': curv_y,
            'curv_xy': curv_xy
        }
    }


def create_plots(theta_range, theta_sol, sx, sy, sxy, kx, ky, kxy,
                strains_sol, curvatures_sol):
    """Create publication-quality plots"""

    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    fig.suptitle('Assignment 1 - Problem 3: Mid-Plane Strains and Curvatures vs. θ',
                 fontsize=14, fontweight='bold')

    # Strains plot
    axes[0].plot(theta_range, sx, 'b-', linewidth=2, label='ε_x⁰')
    axes[0].plot(theta_range, sy, 'r-', linewidth=2, label='ε_y⁰')
    axes[0].plot(theta_range, sxy, 'g-', linewidth=2, label='γ_xy⁰')
    axes[0].axhline(y=0, color='k', linestyle='--', linewidth=0.8, alpha=0.5)
    axes[0].axvline(x=theta_sol, color='m', linestyle=':', linewidth=2,
                   label=f'θ = {theta_sol:.2f}° (γ_xy⁰=0)')

    # Mark the solution point
    idx_sol = np.argmin(np.abs(theta_range - theta_sol))
    axes[0].plot(theta_sol, sxy[idx_sol], 'mo', markersize=10,
                label=f'Solution: γ_xy⁰≈0')

    axes[0].set_xlabel('θ [degrees]', fontsize=11)
    axes[0].set_ylabel('Mid-Plane Strains [με]', fontsize=11)
    axes[0].set_title('Mid-Plane Strains for [30/θ/θ/-30]_s', fontsize=12, fontweight='bold')
    axes[0].legend(loc='best', fontsize=9)
    axes[0].grid(True, alpha=0.3)
    axes[0].set_xlim([-90, 90])

    # Curvatures plot
    axes[1].plot(theta_range, kx, 'b-', linewidth=2, label='κ_x')
    axes[1].plot(theta_range, ky, 'r-', linewidth=2, label='κ_y')
    axes[1].plot(theta_range, kxy, 'g-', linewidth=2, label='κ_xy')
    axes[1].axhline(y=0, color='k', linestyle='--', linewidth=0.8, alpha=0.5)
    axes[1].axvline(x=theta_sol, color='m', linestyle=':', linewidth=2,
                   label=f'θ = {theta_sol:.2f}° (γ_xy⁰=0)')

    axes[1].set_xlabel('θ [degrees]', fontsize=11)
    axes[1].set_ylabel('Curvatures [mm⁻¹]', fontsize=11)
    axes[1].set_title('Curvatures for [30/θ/θ/-30]_s', fontsize=12, fontweight='bold')
    axes[1].legend(loc='best', fontsize=9)
    axes[1].grid(True, alpha=0.3)
    axes[1].set_xlim([-90, 90])

    plt.tight_layout()
    plt.savefig('assignment1_problem3_results.png', dpi=300, bbox_inches='tight')
    print("\n✓ Plots saved to 'assignment1_problem3_results.png'")


if __name__ == "__main__":
    solve_problem3()
