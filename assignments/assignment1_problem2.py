"""
Assignment 1 - Problem 2: Micromechanics Analysis

Problem Statement:
A [0/90/0]_s laminate is fabricated from unidirectional laminae composed of
isotropic fibers and an isotropic matrix.

Given:
- E_f = 220 GPa, ν_f = 0.25 (fibers)
- E_m = 3.6 GPa, ν_m = 0.40 (matrix)
- t = 0.25 mm (lamina thickness)
- d = 10 μm (fiber diameter)
- n = 1900 fibers per 1 mm width

Determine the engineering constants of the laminate.
"""

import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from composite_lib import Micromechanics, Laminate


def solve_problem2():
    """
    Solve Assignment 1 - Problem 2
    Micromechanics to determine laminate engineering constants
    """
    print("\n" + "="*70)
    print("ASSIGNMENT 1 - PROBLEM 2: MICROMECHANICS ANALYSIS")
    print("="*70)

    # Given data
    E_f = 220.0      # GPa - Fiber modulus
    nu_f = 0.25      # Fiber Poisson's ratio
    E_m = 3.6        # GPa - Matrix modulus
    nu_m = 0.40      # Matrix Poisson's ratio
    t = 0.25         # mm - Lamina thickness
    d = 10e-3        # mm - Fiber diameter (10 μm)
    n_fibers = 1900  # Number of fibers per 1 mm width
    width = 1.0      # mm - Reference width

    print("\nGiven Data:")
    print("-" * 70)
    print("Fiber Properties:")
    print(f"  E_f = {E_f} GPa")
    print(f"  ν_f = {nu_f}")
    print("\nMatrix Properties:")
    print(f"  E_m = {E_m} GPa")
    print(f"  ν_m = {nu_m}")
    print("\nGeometry:")
    print(f"  Lamina thickness (t) = {t} mm")
    print(f"  Fiber diameter (d) = {d*1000} μm = {d} mm")
    print(f"  Number of fibers per {width} mm width = {n_fibers}")

    # Step 1: Calculate fiber volume fraction
    print("\n" + "-"*70)
    print("STEP 1: Calculate Fiber Volume Fraction")
    print("-"*70)

    V_f = Micromechanics.calculate_fiber_volume_fraction(
        n_fibers=n_fibers,
        d=d,
        width=width,
        t=t
    )

    print(f"\nFiber cross-sectional area per fiber:")
    A_fiber = np.pi * (d/2)**2
    print(f"  A_fiber = π × ({d/2})² = {A_fiber:.6e} mm²")

    print(f"\nTotal fiber area per {width} mm width:")
    A_fibers_total = n_fibers * A_fiber
    print(f"  A_fibers = {n_fibers} × {A_fiber:.6e} = {A_fibers_total:.6e} mm²")

    print(f"\nCross-sectional area of lamina per {width} mm width:")
    A_lamina = t * width
    print(f"  A_lamina = {t} × {width} = {A_lamina} mm²")

    print(f"\nFiber Volume Fraction:")
    print(f"  V_f = A_fibers / A_lamina = {A_fibers_total:.6e} / {A_lamina}")
    print(f"  V_f = {V_f:.4f} ({V_f*100:.2f}%)")

    V_m = 1 - V_f
    print(f"  V_m = {V_m:.4f} ({V_m*100:.2f}%)")

    # Step 2: Calculate lamina engineering constants
    print("\n" + "-"*70)
    print("STEP 2: Calculate Lamina Engineering Constants")
    print("-"*70)

    micro = Micromechanics(E_f, nu_f, E_m, nu_m, V_f)

    print("\nLongitudinal Modulus E₁ (Rule of Mixtures):")
    E1 = micro.longitudinal_modulus()
    print(f"  E₁ = E_f × V_f + E_m × V_m")
    print(f"  E₁ = {E_f} × {V_f:.4f} + {E_m} × {V_m:.4f}")
    print(f"  E₁ = {E1:.3f} GPa")

    print("\nTransverse Modulus E₂ (Halpin-Tsai, ξ=2):")
    E2 = micro.transverse_modulus_halpin_tsai(xi=2)
    print(f"  η = (E_f/E_m - 1)/(E_f/E_m + ξ)")
    eta_E = (E_f/E_m - 1)/(E_f/E_m + 2)
    print(f"  η = ({E_f}/{E_m} - 1)/({E_f}/{E_m} + 2) = {eta_E:.4f}")
    print(f"  E₂ = E_m × (1 + ξ×η×V_f)/(1 - η×V_f)")
    print(f"  E₂ = {E2:.3f} GPa")

    print("\nMajor Poisson's Ratio ν₁₂ (Rule of Mixtures):")
    nu12 = micro.major_poisson_ratio()
    print(f"  ν₁₂ = ν_f × V_f + ν_m × V_m")
    print(f"  ν₁₂ = {nu_f} × {V_f:.4f} + {nu_m} × {V_m:.4f}")
    print(f"  ν₁₂ = {nu12:.4f}")

    print("\nIn-Plane Shear Modulus G₁₂ (Halpin-Tsai, ξ=1):")
    G12 = micro.shear_modulus_halpin_tsai(xi=1)
    G_f = E_f / (2 * (1 + nu_f))
    G_m = E_m / (2 * (1 + nu_m))
    print(f"  G_f = E_f / (2(1+ν_f)) = {G_f:.3f} GPa")
    print(f"  G_m = E_m / (2(1+ν_m)) = {G_m:.3f} GPa")
    eta_G = (G_f/G_m - 1)/(G_f/G_m + 1)
    print(f"  η = (G_f/G_m - 1)/(G_f/G_m + ξ) = {eta_G:.4f}")
    print(f"  G₁₂ = {G12:.3f} GPa")

    # Step 3: Calculate laminate properties
    print("\n" + "-"*70)
    print("STEP 3: Calculate Laminate Engineering Constants")
    print("-"*70)

    # Create laminate [0/90/0]_s = [0/90/0/0/90/0]
    stacking_sequence = "0/90/0_s"
    print(f"\nStacking Sequence: {stacking_sequence}")
    print(f"Expanded: [0/90/0/0/90/0]")

    material_props = {
        'E1': E1,
        'E2': E2,
        'G12': G12,
        'nu12': nu12
    }

    laminate = Laminate(material_props, stacking_sequence, t)

    print(f"\nLaminate Configuration:")
    print(f"  Number of plies: {laminate.n_plies}")
    print(f"  Total thickness: {laminate.total_thickness:.3f} mm")
    print(f"  Symmetric: {laminate.is_symmetric()}")

    # Display ABD matrices
    print("\n" + "-"*70)
    print("EXTENSIONAL STIFFNESS MATRIX [A] (N/mm)")
    print("-"*70)
    print(laminate.A)

    print("\n" + "-"*70)
    print("COUPLING STIFFNESS MATRIX [B] (N)")
    print("-"*70)
    print(laminate.B)
    print("\nNote: B matrix is nearly zero (symmetric laminate)")

    print("\n" + "-"*70)
    print("BENDING STIFFNESS MATRIX [D] (N·mm)")
    print("-"*70)
    print(laminate.D)

    # Calculate effective laminate properties
    print("\n" + "-"*70)
    print("EFFECTIVE LAMINATE ENGINEERING CONSTANTS")
    print("-"*70)

    # For symmetric laminates, we can calculate effective properties
    h = laminate.total_thickness
    a_star = laminate.abd[:3, :3]  # Extract compliance matrix a*

    E_x = 1 / (h * a_star[0, 0])
    E_y = 1 / (h * a_star[1, 1])
    G_xy = 1 / (h * a_star[2, 2])
    nu_xy = -a_star[0, 1] / a_star[0, 0]
    nu_yx = -a_star[1, 0] / a_star[1, 1]

    print(f"\nEffective In-Plane Moduli:")
    print(f"  E_x  = {E_x:.3f} GPa")
    print(f"  E_y  = {E_y:.3f} GPa")
    print(f"  G_xy = {G_xy:.3f} GPa")
    print(f"  ν_xy = {nu_xy:.4f}")
    print(f"  ν_yx = {nu_yx:.4f}")

    # Summary
    print("\n" + "="*70)
    print("SUMMARY - ENGINEERING CONSTANTS")
    print("="*70)

    print("\nLamina Properties (single ply):")
    print(f"  V_f  = {V_f:.4f} ({V_f*100:.2f}%)")
    print(f"  E₁   = {E1:.3f} GPa")
    print(f"  E₂   = {E2:.3f} GPa")
    print(f"  G₁₂  = {G12:.3f} GPa")
    print(f"  ν₁₂  = {nu12:.4f}")

    print(f"\nLaminate Properties [0/90/0]_s:")
    print(f"  Total thickness = {h:.3f} mm")
    print(f"  E_x  = {E_x:.3f} GPa")
    print(f"  E_y  = {E_y:.3f} GPa")
    print(f"  G_xy = {G_xy:.3f} GPa")
    print(f"  ν_xy = {nu_xy:.4f}")

    print("\n" + "="*70 + "\n")

    return {
        'V_f': V_f,
        'lamina': material_props,
        'laminate': {
            'E_x': E_x,
            'E_y': E_y,
            'G_xy': G_xy,
            'nu_xy': nu_xy,
            'A': laminate.A,
            'B': laminate.B,
            'D': laminate.D
        }
    }


if __name__ == "__main__":
    solve_problem2()
