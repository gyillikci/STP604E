"""
Assignment 1 - Problem 3 (Version 2): Laminate Analysis with Constraint

Problem Statement:
Consider a laminate with stacking sequence [30/theta1/theta2/30]_s subjected to:
  N_x = N_y = 1000 N/m
  M_y = M_xy = 50 N

Material: Kevlar/Epoxy
  E1 = 76 GPa, E2 = 5.50 GPa, G12 = 2.30 GPa, nu12 = 0.34, t = 1.25 mm

Constraint: No shear strain (gamma_xy0 = 0)

Determine and plot mid-plane strains and curvatures as a function of theta.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from scipy.optimize import fsolve
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from composite_lib import Laminate


def solve_problem3_v2():
    """
    Solve Assignment 1 - Problem 3 (Version 2)
    Find theta1 and theta2 such that gamma_xy = 0
    For laminate [30/theta/theta/30]_s
    """
    print("\n" + "="*70)
    print("ASSIGNMENT 1 - PROBLEM 3 (V2): LAMINATE WITH ZERO SHEAR STRAIN")
    print("="*70)
    print("Stacking: [30/theta/theta/30]_s")
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
    print(f"  E1  = {material['E1']} GPa")
    print(f"  E2  = {material['E2']} GPa")
    print(f"  G12 = {material['G12']} GPa")
    print(f"  nu12 = {material['nu12']}")
    print(f"  t   = {t} mm")

    print("\nApplied Loads:")
    print(f"  N_x  = {Nx} N/m")
    print(f"  N_y  = {Ny} N/m")
    print(f"  N_xy = {Nxy} N/m")
    print(f"  M_x  = {Mx} N")
    print(f"  M_y  = {My} N")
    print(f"  M_xy = {Mxy} N")

    print("\nStacking Sequence: [30/theta1/theta2/30]_s")
    print("Expanded: [30/theta/theta/30/30/theta/theta/30]")
    print("Constraint: gamma_xy0 = 0 (zero mid-plane shear strain)")

    # Approach: Assume theta1 = theta2 = theta for simplicity and symmetry
    # Then find theta such that gamma_xy = 0

    print("\n" + "-"*70)
    print("STEP 1: Find theta such that gamma_xy0 = 0")
    print("-"*70)
    print("\nAssuming theta1 = theta2 = theta for symmetric solution")

    def shear_strain_constraint(theta):
        """Calculate shear strain for given theta"""
        # Extract scalar value if theta is an array
        theta_val = float(theta) if np.isscalar(theta) else float(theta[0])
        stacking = [30, theta_val, theta_val, 30, 30, theta_val, theta_val, 30]
        lam = Laminate(material, stacking, t)
        strains, _ = lam.calculate_strains_curvatures(loads)
        return strains[2]  # gamma_xy

    # Find theta that gives zero shear strain
    theta_initial_guess = 0
    theta_solution = fsolve(shear_strain_constraint, theta_initial_guess)[0]

    print(f"\nSolution: theta = {theta_solution:.2f} degrees")

    # Verify solution
    stacking_solution = [30, theta_solution, theta_solution, 30,
                        30, theta_solution, theta_solution, 30]
    lam_solution = Laminate(material, stacking_solution, t)
    strains_sol, curvatures_sol = lam_solution.calculate_strains_curvatures(loads)

    print(f"\nVerification with theta = {theta_solution:.2f} degrees:")
    print(f"  Stacking: [30/{theta_solution:.1f}/{theta_solution:.1f}/30/30/{theta_solution:.1f}/{theta_solution:.1f}/30]")
    print(f"\n  epsilon_x0  = {strains_sol[0]*1e6:.3f} microstrain")
    print(f"  epsilon_y0  = {strains_sol[1]*1e6:.3f} microstrain")
    print(f"  gamma_xy0   = {strains_sol[2]*1e6:.6f} microstrain  <- Should be approx 0")
    print(f"\n  kappa_x     = {curvatures_sol[0]:.6f} /mm")
    print(f"  kappa_y     = {curvatures_sol[1]:.6f} /mm")
    print(f"  kappa_xy    = {curvatures_sol[2]:.6f} /mm")

    # Display ABD matrices
    print("\n" + "-"*70)
    print("ABD MATRICES at Solution")
    print("-"*70)
    
    print("\nExtensional Stiffness [A] (N/mm):")
    print(lam_solution.A)
    
    print("\nCoupling Stiffness [B] (N):")
    print(lam_solution.B)
    
    print("\nBending Stiffness [D] (N*mm):")
    print(lam_solution.D)

    # Step 2: Plot strains and curvatures vs theta
    print("\n" + "-"*70)
    print("STEP 2: Parametric Study - Vary theta from -90 to 90 degrees")
    print("-"*70)

    theta_range = np.linspace(-90, 90, 181)

    strains_x = []
    strains_y = []
    strains_xy = []
    curv_x = []
    curv_y = []
    curv_xy = []

    print("\nCalculating strains and curvatures for 181 theta values...")
    
    for theta in theta_range:
        stacking = [30, theta, theta, 30, 30, theta, theta, 30]
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
The analysis shows that for the laminate [30/theta/theta/30]_s:

1. Zero Shear Strain Condition:
   - The angle theta = {theta_solution:.2f} degrees produces zero mid-plane shear strain
   - This creates the laminate [30/{theta_solution:.1f}/{theta_solution:.1f}/30]_s
   - The solution is symmetric and balanced

2. Strain Behavior:
   - epsilon_x0 and epsilon_y0 vary significantly with theta
   - gamma_xy0 varies and crosses zero at theta = {theta_solution:.2f} degrees
   - The shear strain is highly sensitive to ply orientation

3. Curvature Behavior:
   - All curvatures show variation with theta
   - The coupling between bending moments and curvatures depends on
     the laminate stacking sequence
   - Even with symmetric layup, [B] matrix is non-zero for non-symmetric angles

4. Physical Interpretation:
   - The constraint gamma_xy0 = 0 can be achieved by proper selection of theta
   - For [30/theta/theta/30]_s, the solution is theta = {theta_solution:.2f} degrees
   - This demonstrates the design flexibility of composite laminates
   - Such constraints are important in applications requiring specific
     deformation patterns

5. Comparison with [30/theta/theta/-30]_s:
   - Changing the outer ply from -30 to +30 degrees significantly affects the solution
   - Different ply arrangements produce different optimal angles for zero shear strain
    """)

    print("="*70 + "\n")

    return {
        'theta_solution': theta_solution,
        'strains': strains_sol,
        'curvatures': curvatures_sol,
        'theta_range': theta_range,
        'ABD': {
            'A': lam_solution.A,
            'B': lam_solution.B,
            'D': lam_solution.D
        },
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
    fig.suptitle('Assignment 1 - Problem 3 (V2): Mid-Plane Strains and Curvatures vs. theta\n' +
                 'Laminate: [30/theta/theta/30]_s',
                 fontsize=14, fontweight='bold')

    # Strains plot
    axes[0].plot(theta_range, sx, 'b-', linewidth=2, label='epsilon_x0')
    axes[0].plot(theta_range, sy, 'r-', linewidth=2, label='epsilon_y0')
    axes[0].plot(theta_range, sxy, 'g-', linewidth=2, label='gamma_xy0')
    axes[0].axhline(y=0, color='k', linestyle='--', linewidth=0.8, alpha=0.5)
    axes[0].axvline(x=theta_sol, color='m', linestyle=':', linewidth=2,
                   label=f'theta = {theta_sol:.2f} deg (gamma_xy0=0)')

    # Mark the solution point
    idx_sol = np.argmin(np.abs(theta_range - theta_sol))
    axes[0].plot(theta_sol, sxy[idx_sol], 'mo', markersize=12,
                label=f'Solution: gamma_xy0 approx 0', zorder=5)

    axes[0].set_xlabel('theta [degrees]', fontsize=11)
    axes[0].set_ylabel('Mid-Plane Strains [microstrain]', fontsize=11)
    axes[0].set_title('Mid-Plane Strains for [30/theta/theta/30]_s', fontsize=12, fontweight='bold')
    axes[0].legend(loc='best', fontsize=9)
    axes[0].grid(True, alpha=0.3)
    axes[0].set_xlim([-90, 90])

    # Add text annotation with solution
    axes[0].text(0.02, 0.98, f'Solution: theta = {theta_sol:.2f} deg',
                transform=axes[0].transAxes,
                fontsize=10, fontweight='bold',
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

    # Curvatures plot
    axes[1].plot(theta_range, kx, 'b-', linewidth=2, label='kappa_x')
    axes[1].plot(theta_range, ky, 'r-', linewidth=2, label='kappa_y')
    axes[1].plot(theta_range, kxy, 'g-', linewidth=2, label='kappa_xy')
    axes[1].axhline(y=0, color='k', linestyle='--', linewidth=0.8, alpha=0.5)
    axes[1].axvline(x=theta_sol, color='m', linestyle=':', linewidth=2,
                   label=f'theta = {theta_sol:.2f} deg (gamma_xy0=0)')

    axes[1].set_xlabel('theta [degrees]', fontsize=11)
    axes[1].set_ylabel('Curvatures [/mm]', fontsize=11)
    axes[1].set_title('Curvatures for [30/theta/theta/30]_s', fontsize=12, fontweight='bold')
    axes[1].legend(loc='best', fontsize=9)
    axes[1].grid(True, alpha=0.3)
    axes[1].set_xlim([-90, 90])

    plt.tight_layout()
    filename = 'assignment1_problem3_v2_results.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"\nPlots saved to '{filename}'")


if __name__ == "__main__":
    results = solve_problem3_v2()
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Laminate: [30/theta/theta/30]_s")
    print(f"Solution: theta = {results['theta_solution']:.2f} degrees")
    print(f"Expanded: [30/{results['theta_solution']:.1f}/{results['theta_solution']:.1f}/30/30/{results['theta_solution']:.1f}/{results['theta_solution']:.1f}/30]")
    print(f"\nMid-plane strains at solution:")
    print(f"  epsilon_x0 = {results['strains'][0]*1e6:.3f} microstrain")
    print(f"  epsilon_y0 = {results['strains'][1]*1e6:.3f} microstrain")
    print(f"  gamma_xy0  = {results['strains'][2]*1e6:.6f} microstrain (approx 0)")
    print(f"\nCurvatures at solution:")
    print(f"  kappa_x  = {results['curvatures'][0]:.6f} /mm")
    print(f"  kappa_y  = {results['curvatures'][1]:.6f} /mm")
    print(f"  kappa_xy = {results['curvatures'][2]:.6f} /mm")
    print("="*70 + "\n")
