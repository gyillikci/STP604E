"""
Assignment 1 - Problem 1: Quasi-Isotropic Laminate Analysis

Problem Statement:
If a laminate consists of three or more identical orthotropic laminae that are
oriented at the same angle relative to adjacent laminae, the extensional stiffness
matrix will be isotropic. Rotate the given laminates and plot the elements of the
extensional stiffness matrix A_ij as a function of the top ply orientation.

Laminates: [-45/0/45/90] and [0/30/60/90]
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from composite_lib import Laminate


def solve_problem1():
    """
    Solve Assignment 1 - Problem 1
    Analyze quasi-isotropic behavior of laminates
    """
    print("\n" + "="*70)
    print("ASSIGNMENT 1 - PROBLEM 1: QUASI-ISOTROPIC LAMINATE ANALYSIS")
    print("="*70)

    # Material properties (using typical carbon/epoxy - AS4/3501-6)
    material = {
        'E1': 142.0,   # GPa
        'E2': 10.3,    # GPa
        'G12': 7.2,    # GPa
        'nu12': 0.27
    }

    ply_thickness = 0.125  # mm

    # Define laminates
    laminate1_base = [-45, 0, 45, 90]
    laminate2_base = [0, 30, 60, 90]

    # Rotation angles to test
    rotation_angles = np.linspace(0, 360, 73)  # Every 5 degrees

    # Storage for results
    results1 = {f'A{i}{j}': [] for i in [1,2,6] for j in [1,2,6]}
    results2 = {f'A{i}{j}': [] for i in [1,2,6] for j in [1,2,6]}

    print("\nMaterial Properties:")
    print(f"  E1  = {material['E1']:.1f} GPa")
    print(f"  E2  = {material['E2']:.1f} GPa")
    print(f"  G12 = {material['G12']:.1f} GPa")
    print(f"  ν12 = {material['nu12']:.3f}")
    print(f"  Ply thickness = {ply_thickness} mm")

    print("\n" + "-"*70)
    print("LAMINATE 1: [-45/0/45/90]")
    print("-"*70)

    for rotation in rotation_angles:
        # Rotate laminate 1
        rotated_seq1 = [(angle + rotation) % 360 for angle in laminate1_base]
        # Adjust angles to -180 to 180 range
        rotated_seq1 = [angle if angle <= 180 else angle - 360 for angle in rotated_seq1]

        lam1 = Laminate(material, rotated_seq1, ply_thickness)

        # Store A matrix components
        results1['A11'].append(lam1.A[0, 0])
        results1['A22'].append(lam1.A[1, 1])
        results1['A12'].append(lam1.A[0, 1])
        results1['A66'].append(lam1.A[2, 2])
        results1['A16'].append(lam1.A[0, 2])
        results1['A26'].append(lam1.A[1, 2])

    print(f"\nRotating from 0° to 360°...")
    print(f"At 0° rotation: {laminate1_base}")
    print(f"\nA matrix at 0°:")
    lam1_0 = Laminate(material, laminate1_base, ply_thickness)
    print(lam1_0.A)

    # Check for quasi-isotropy (A11 ≈ A22, A16 ≈ 0, A26 ≈ 0)
    A11_range = max(results1['A11']) - min(results1['A11'])
    A22_range = max(results1['A22']) - min(results1['A22'])
    A16_max = max(np.abs(results1['A16']))
    A26_max = max(np.abs(results1['A26']))

    print(f"\nVariation Analysis:")
    print(f"  A11 range: {A11_range:.3f} N/mm ({A11_range/np.mean(results1['A11'])*100:.2f}%)")
    print(f"  A22 range: {A22_range:.3f} N/mm ({A22_range/np.mean(results1['A22'])*100:.2f}%)")
    print(f"  Max |A16|: {A16_max:.6f} N/mm")
    print(f"  Max |A26|: {A26_max:.6f} N/mm")

    is_quasi_iso_1 = (A11_range < 0.01 * np.mean(results1['A11']) and
                      A16_max < 0.01 and A26_max < 0.01)

    print(f"\n*** Laminate 1 is {'QUASI-ISOTROPIC' if is_quasi_iso_1 else 'NOT quasi-isotropic'} ***")

    print("\n" + "-"*70)
    print("LAMINATE 2: [0/30/60/90]")
    print("-"*70)

    for rotation in rotation_angles:
        # Rotate laminate 2
        rotated_seq2 = [(angle + rotation) % 360 for angle in laminate2_base]
        rotated_seq2 = [angle if angle <= 180 else angle - 360 for angle in rotated_seq2]

        lam2 = Laminate(material, rotated_seq2, ply_thickness)

        # Store A matrix components
        results2['A11'].append(lam2.A[0, 0])
        results2['A22'].append(lam2.A[1, 1])
        results2['A12'].append(lam2.A[0, 1])
        results2['A66'].append(lam2.A[2, 2])
        results2['A16'].append(lam2.A[0, 2])
        results2['A26'].append(lam2.A[1, 2])

    print(f"\nRotating from 0° to 360°...")
    print(f"At 0° rotation: {laminate2_base}")
    print(f"\nA matrix at 0°:")
    lam2_0 = Laminate(material, laminate2_base, ply_thickness)
    print(lam2_0.A)

    A11_range = max(results2['A11']) - min(results2['A11'])
    A22_range = max(results2['A22']) - min(results2['A22'])
    A16_max = max(np.abs(results2['A16']))
    A26_max = max(np.abs(results2['A26']))

    print(f"\nVariation Analysis:")
    print(f"  A11 range: {A11_range:.3f} N/mm ({A11_range/np.mean(results2['A11'])*100:.2f}%)")
    print(f"  A22 range: {A22_range:.3f} N/mm ({A22_range/np.mean(results2['A22'])*100:.2f}%)")
    print(f"  Max |A16|: {A16_max:.6f} N/mm")
    print(f"  Max |A26|: {A26_max:.6f} N/mm")

    is_quasi_iso_2 = (A11_range < 0.01 * np.mean(results2['A11']) and
                      A16_max < 0.01 and A26_max < 0.01)

    print(f"\n*** Laminate 2 is {'QUASI-ISOTROPIC' if is_quasi_iso_2 else 'NOT quasi-isotropic'} ***")

    # Create plots
    create_plots(rotation_angles, results1, results2,
                 is_quasi_iso_1, is_quasi_iso_2)

    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Laminate 1 [-45/0/45/90]:  {'✓ QUASI-ISOTROPIC' if is_quasi_iso_1 else '✗ NOT quasi-isotropic'}")
    print(f"Laminate 2 [0/30/60/90]:   {'✓ QUASI-ISOTROPIC' if is_quasi_iso_2 else '✗ NOT quasi-isotropic'}")
    print("\nPlots saved to 'assignment1_problem1_results.png'")
    print("="*70 + "\n")

    return results1, results2, rotation_angles


def create_plots(rotation_angles, results1, results2, is_quasi_iso_1, is_quasi_iso_2):
    """Create publication-quality plots"""

    fig, axes = plt.subplots(3, 2, figsize=(14, 12))
    fig.suptitle('Assignment 1 - Problem 1: Extensional Stiffness vs. Rotation Angle',
                 fontsize=14, fontweight='bold')

    # Laminate 1 plots
    # A11 and A22
    axes[0, 0].plot(rotation_angles, results1['A11'], 'b-', linewidth=2, label='A₁₁')
    axes[0, 0].plot(rotation_angles, results1['A22'], 'r--', linewidth=2, label='A₂₂')
    axes[0, 0].set_ylabel('Stiffness [N/mm]', fontsize=10)
    axes[0, 0].set_title('Laminate 1: [-45/0/45/90] - Normal Stiffness', fontsize=11, fontweight='bold')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # A12 and A66
    axes[1, 0].plot(rotation_angles, results1['A12'], 'g-', linewidth=2, label='A₁₂')
    axes[1, 0].plot(rotation_angles, results1['A66'], 'm--', linewidth=2, label='A₆₆')
    axes[1, 0].set_ylabel('Stiffness [N/mm]', fontsize=10)
    axes[1, 0].set_title('Laminate 1: [-45/0/45/90] - Coupling & Shear Stiffness', fontsize=11)
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # A16 and A26
    axes[2, 0].plot(rotation_angles, results1['A16'], 'c-', linewidth=2, label='A₁₆')
    axes[2, 0].plot(rotation_angles, results1['A26'], 'y--', linewidth=2, label='A₂₆')
    axes[2, 0].set_xlabel('Top Ply Rotation [degrees]', fontsize=10)
    axes[2, 0].set_ylabel('Stiffness [N/mm]', fontsize=10)
    axes[2, 0].set_title('Laminate 1: [-45/0/45/90] - Shear Coupling', fontsize=11)
    axes[2, 0].legend()
    axes[2, 0].grid(True, alpha=0.3)
    axes[2, 0].axhline(y=0, color='k', linestyle='-', linewidth=0.5)

    # Add text annotation
    status1 = "QUASI-ISOTROPIC ✓" if is_quasi_iso_1 else "NOT Quasi-Isotropic ✗"
    axes[2, 0].text(0.5, 0.95, status1, transform=axes[2, 0].transAxes,
                    fontsize=10, fontweight='bold',
                    verticalalignment='top', horizontalalignment='center',
                    bbox=dict(boxstyle='round', facecolor='lightgreen' if is_quasi_iso_1 else 'lightyellow', alpha=0.7))

    # Laminate 2 plots
    # A11 and A22
    axes[0, 1].plot(rotation_angles, results2['A11'], 'b-', linewidth=2, label='A₁₁')
    axes[0, 1].plot(rotation_angles, results2['A22'], 'r--', linewidth=2, label='A₂₂')
    axes[0, 1].set_ylabel('Stiffness [N/mm]', fontsize=10)
    axes[0, 1].set_title('Laminate 2: [0/30/60/90] - Normal Stiffness', fontsize=11, fontweight='bold')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # A12 and A66
    axes[1, 1].plot(rotation_angles, results2['A12'], 'g-', linewidth=2, label='A₁₂')
    axes[1, 1].plot(rotation_angles, results2['A66'], 'm--', linewidth=2, label='A₆₆')
    axes[1, 1].set_ylabel('Stiffness [N/mm]', fontsize=10)
    axes[1, 1].set_title('Laminate 2: [0/30/60/90] - Coupling & Shear Stiffness', fontsize=11)
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    # A16 and A26
    axes[2, 1].plot(rotation_angles, results2['A16'], 'c-', linewidth=2, label='A₁₆')
    axes[2, 1].plot(rotation_angles, results2['A26'], 'y--', linewidth=2, label='A₂₆')
    axes[2, 1].set_xlabel('Top Ply Rotation [degrees]', fontsize=10)
    axes[2, 1].set_ylabel('Stiffness [N/mm]', fontsize=10)
    axes[2, 1].set_title('Laminate 2: [0/30/60/90] - Shear Coupling', fontsize=11)
    axes[2, 1].legend()
    axes[2, 1].grid(True, alpha=0.3)
    axes[2, 1].axhline(y=0, color='k', linestyle='-', linewidth=0.5)

    # Add text annotation
    status2 = "QUASI-ISOTROPIC ✓" if is_quasi_iso_2 else "NOT Quasi-Isotropic ✗"
    axes[2, 1].text(0.5, 0.95, status2, transform=axes[2, 1].transAxes,
                    fontsize=10, fontweight='bold',
                    verticalalignment='top', horizontalalignment='center',
                    bbox=dict(boxstyle='round', facecolor='lightgreen' if is_quasi_iso_2 else 'lightyellow', alpha=0.7))

    plt.tight_layout()
    plt.savefig('assignment1_problem1_results.png', dpi=300, bbox_inches='tight')
    print("\n✓ Plots saved to 'assignment1_problem1_results.png'")


if __name__ == "__main__":
    solve_problem1()
