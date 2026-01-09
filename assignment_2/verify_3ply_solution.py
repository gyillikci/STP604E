"""
Verify the 3-ply solution found in parameter study
"""
import numpy as np
from problem2_minimum_thickness import LaminateDesigner

# Material properties
designer = LaminateDesigner(
    E1=38.6,    # GPa
    E2=8.27,    # GPa
    G12=4.14,   # GPa
    nu12=0.28,
    t=0.125     # mm
)

# Try various 3-ply combinations to find valid solutions
print("Searching for valid 3-ply solutions...")
print("="*70)

valid_solutions = []

# Try different combinations
test_combinations = [
    [0, 30, -75],
    [0, 45, -75],
    [0, 60, -75],
    [0, 75, -75],
    [0, -30, 75],
    [0, -45, 75],
    [0, -60, 75],
    [15, 30, -75],
    [15, 45, -75],
    [-15, 30, -75],
    [0, 0, 90],
    [0, 0, -75],
    [0, 0, 75],
]

for angles in test_combinations:
    props = designer.analyze_laminate(angles)
    if props:
        c1 = 0.2 <= props['nu_xy'] <= 0.7
        c2 = props['Gxy'] >= 5.0
        c3 = props['Ex'] >= 22.0
        c4 = props['Ey'] >= 18.0
        
        all_satisfied = c1 and c2 and c3 and c4
        
        if all_satisfied:
            valid_solutions.append((angles, props))
            print(f"\n✓ VALID: {angles}")
            print(f"  E_x={props['Ex']:.2f} GPa, E_y={props['Ey']:.2f} GPa")
            print(f"  G_xy={props['Gxy']:.2f} GPa, ν_xy={props['nu_xy']:.3f}")

print(f"\n{'='*70}")
print(f"Found {len(valid_solutions)} valid 3-ply solutions")
