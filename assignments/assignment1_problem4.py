"""
Assignment 1 - Problem 4: Stiffness Matrix Comparison

Problem Statement:
A laminate with stacking sequence [-45/45] is composed of equal-thickness layers
(0.5 mm each) of AS/3501 graphite-epoxy composite.

Material: AS/3501 Graphite-Epoxy
  E₁ = 181 GPa, E₂ = 10.3 GPa, G₁₂ = 7.17 GPa, ν₁₂ = 0.28

Tasks:
a) Determine the laminate stiffness matrices A, B, and D
b) Add two layers to form [-45/45/-45/45] and discuss how matrices are affected
"""

import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from composite_lib import Laminate


def solve_problem4():
    """
    Solve Assignment 1 - Problem 4
    Compare stiffness matrices for different layups
    """
    print("\n" + "="*70)
    print("ASSIGNMENT 1 - PROBLEM 4: STIFFNESS MATRIX COMPARISON")
    print("="*70)

    # Material properties - AS/3501 Graphite-Epoxy
    material = {
        'E1': 181.0,   # GPa
        'E2': 10.3,    # GPa
        'G12': 7.17,   # GPa
        'nu12': 0.28
    }

    t = 0.5  # mm - ply thickness

    print("\nMaterial Properties (AS/3501 Graphite-Epoxy):")
    print(f"  E₁  = {material['E1']} GPa")
    print(f"  E₂  = {material['E2']} GPa")
    print(f"  G₁₂ = {material['G12']} GPa")
    print(f"  ν₁₂ = {material['nu12']}")
    print(f"  Ply thickness = {t} mm")

    # Part (a): [-45/45] laminate
    print("\n" + "="*70)
    print("PART (a): LAMINATE [-45/45]")
    print("="*70)

    stacking1 = [-45, 45]
    lam1 = Laminate(material, stacking1, t)

    print(f"\nStacking Sequence: {stacking1}")
    print(f"Number of plies: {lam1.n_plies}")
    print(f"Total thickness: {lam1.total_thickness} mm")
    print(f"Symmetric: {lam1.is_symmetric()}")
    print(f"Balanced: {lam1.is_balanced()}")

    print(f"\nZ-coordinates (mm):")
    for i, z in enumerate(lam1.z_coords):
        print(f"  z_{i} = {z:7.4f} mm")

    print("\n" + "-"*70)
    print("EXTENSIONAL STIFFNESS MATRIX [A] (N/mm)")
    print("-"*70)
    print_matrix(lam1.A, "N/mm")

    print("\n" + "-"*70)
    print("COUPLING STIFFNESS MATRIX [B] (N)")
    print("-"*70)
    print_matrix(lam1.B, "N")
    print("\nNote: B ≠ 0 because laminate is NOT symmetric")

    print("\n" + "-"*70)
    print("BENDING STIFFNESS MATRIX [D] (N·mm)")
    print("-"*70)
    print_matrix(lam1.D, "N·mm")

    # Part (b): [-45/45/-45/45] laminate
    print("\n" + "="*70)
    print("PART (b): LAMINATE [-45/45/-45/45]")
    print("="*70)

    stacking2 = [-45, 45, -45, 45]
    lam2 = Laminate(material, stacking2, t)

    print(f"\nStacking Sequence: {stacking2}")
    print(f"Number of plies: {lam2.n_plies}")
    print(f"Total thickness: {lam2.total_thickness} mm")
    print(f"Symmetric: {lam2.is_symmetric()}")
    print(f"Balanced: {lam2.is_balanced()}")

    print(f"\nZ-coordinates (mm):")
    for i, z in enumerate(lam2.z_coords):
        print(f"  z_{i} = {z:7.4f} mm")

    print("\n" + "-"*70)
    print("EXTENSIONAL STIFFNESS MATRIX [A] (N/mm)")
    print("-"*70)
    print_matrix(lam2.A, "N/mm")

    print("\n" + "-"*70)
    print("COUPLING STIFFNESS MATRIX [B] (N)")
    print("-"*70)
    print_matrix(lam2.B, "N")
    print("\nNote: B ≠ 0 because laminate is still NOT symmetric")

    print("\n" + "-"*70)
    print("BENDING STIFFNESS MATRIX [D] (N·mm)")
    print("-"*70)
    print_matrix(lam2.D, "N·mm")

    # Comparison and Discussion
    print("\n" + "="*70)
    print("COMPARISON AND DISCUSSION")
    print("="*70)

    print("\n1. EXTENSIONAL STIFFNESS [A]:")
    print("   " + "-"*66)
    A_ratio = lam2.A / lam1.A
    print(f"   A_ratio = A₂/A₁:")
    print_matrix(A_ratio, "", decimal=2)
    print(f"\n   → A matrix scales by factor of {lam2.total_thickness/lam1.total_thickness:.1f}")
    print("   → This is expected: A_ij = ∫Q̄_ij dz, doubles with thickness")

    print("\n2. COUPLING STIFFNESS [B]:")
    print("   " + "-"*66)
    print(f"   |B₁₆| for [-45/45]:      {abs(lam1.B[0,2]):.3f} N")
    print(f"   |B₁₆| for [-45/45/-45/45]: {abs(lam2.B[0,2]):.3f} N")
    B_ratio_16 = abs(lam2.B[0,2]) / abs(lam1.B[0,2])
    print(f"   Ratio: {B_ratio_16:.2f}")
    print(f"\n   |B₂₆| for [-45/45]:      {abs(lam1.B[1,2]):.3f} N")
    print(f"   |B₂₆| for [-45/45/-45/45]: {abs(lam2.B[1,2]):.3f} N")
    B_ratio_26 = abs(lam2.B[1,2]) / abs(lam1.B[1,2])
    print(f"   Ratio: {B_ratio_26:.2f}")
    print(f"\n   → B matrix scales by factor of ~{B_ratio_16:.1f}")
    print("   → B_ij = ½∫Q̄_ij z dz, increases with (thickness)²")

    print("\n3. BENDING STIFFNESS [D]:")
    print("   " + "-"*66)
    D_ratio = lam2.D / lam1.D
    print(f"   D_ratio = D₂/D₁:")
    print_matrix(D_ratio, "", decimal=2)
    theoretical_ratio = (lam2.total_thickness/lam1.total_thickness)**3
    print(f"\n   → D matrix scales by factor of ~{np.mean(np.diag(D_ratio)):.1f}")
    print(f"   → Theoretical ratio for thickness³: {theoretical_ratio:.1f}")
    print("   → D_ij = ⅓∫Q̄_ij z² dz, scales with (thickness)³")

    print("\n4. KEY OBSERVATIONS:")
    print("   " + "-"*66)
    print(f"""
   • Extensional stiffness [A]:
     - Doubles when thickness doubles (linear relationship)
     - Both laminates are balanced, so A₁₆ = A₂₆ ≈ 0

   • Coupling stiffness [B]:
     - Increases by factor of ~4 (quadratic with thickness)
     - Both laminates are non-symmetric, so B ≠ 0
     - B couples in-plane loads with curvatures

   • Bending stiffness [D]:
     - Increases by factor of ~8 (cubic with thickness)
     - Much more efficient to increase thickness for bending resistance

   • Laminate Classification:
     - [-45/45]:         Balanced, Non-symmetric
     - [-45/45/-45/45]:  Balanced, Symmetric (repeating pattern)

   • Design Implications:
     - To increase in-plane stiffness: add plies (linear gain)
     - To increase bending stiffness: increase thickness (cubic gain)
     - For uncoupled behavior: use symmetric layups (B = 0)
   """)

    # Create comparison table
    print("\n" + "-"*70)
    print("SUMMARY TABLE")
    print("-"*70)
    print(f"{'Property':<30} {'[-45/45]':<20} {'[-45/45/-45/45]':<20}")
    print("-"*70)
    print(f"{'Total thickness (mm)':<30} {lam1.total_thickness:<20.2f} {lam2.total_thickness:<20.2f}")
    print(f"{'A₁₁ (N/mm)':<30} {lam1.A[0,0]:<20.2f} {lam2.A[0,0]:<20.2f}")
    print(f"{'A₂₂ (N/mm)':<30} {lam1.A[1,1]:<20.2f} {lam2.A[1,1]:<20.2f}")
    print(f"{'A₆₆ (N/mm)':<30} {lam1.A[2,2]:<20.2f} {lam2.A[2,2]:<20.2f}")
    print(f"{'|B₁₆| (N)':<30} {abs(lam1.B[0,2]):<20.3f} {abs(lam2.B[0,2]):<20.3f}")
    print(f"{'D₁₁ (N·mm)':<30} {lam1.D[0,0]:<20.3f} {lam2.D[0,0]:<20.3f}")
    print(f"{'D₂₂ (N·mm)':<30} {lam1.D[1,1]:<20.3f} {lam2.D[1,1]:<20.3f}")
    print(f"{'D₆₆ (N·mm)':<30} {lam1.D[2,2]:<20.3f} {lam2.D[2,2]:<20.3f}")
    print("-"*70)

    print("\n" + "="*70 + "\n")

    return {
        'laminate1': {
            'stacking': stacking1,
            'A': lam1.A,
            'B': lam1.B,
            'D': lam1.D
        },
        'laminate2': {
            'stacking': stacking2,
            'A': lam2.A,
            'B': lam2.B,
            'D': lam2.D
        }
    }


def print_matrix(matrix, units, decimal=3):
    """Pretty print matrix with units"""
    rows, cols = matrix.shape
    for i in range(rows):
        row_str = "  ["
        for j in range(cols):
            if decimal == 2:
                row_str += f"{matrix[i,j]:8.2f}  "
            else:
                row_str += f"{matrix[i,j]:10.{decimal}f}  "
        row_str += "]"
        print(row_str)


if __name__ == "__main__":
    solve_problem4()
