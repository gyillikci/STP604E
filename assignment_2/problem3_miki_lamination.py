"""
Assignment 2 - Problem 3: 16-Layer Balanced Symmetric Laminate Design
Using Miki's Lamination Parameters Approach
Maximize Ey subject to Ex≥70 GPa, Gxy≥15 GPa, νxy<0.4
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import time

class LaminationParameterDesign:
    """
    Design using lamination parameters
    """
    
    def __init__(self, E1, E2, G12, nu12):
        self.E1 = E1 * 1e3  # Convert GPa to MPa
        self.E2 = E2 * 1e3
        self.G12 = G12 * 1e3
        self.nu12 = nu12
        self.nu21 = nu12 * E2 / E1
        
        # Calculate invariants
        self.calculate_invariants()
    
    def calculate_invariants(self):
        """Calculate laminate invariants U1-U5"""
        E1, E2, nu12, nu21, G12 = self.E1, self.E2, self.nu12, self.nu21, self.G12
        
        # Reduced stiffness matrix components
        Q11 = E1 / (1 - nu12 * nu21)
        Q22 = E2 / (1 - nu12 * nu21)
        Q12 = nu12 * E2 / (1 - nu12 * nu21)
        Q66 = G12
        
        # Tsai-Pagano invariants
        self.U1 = (3*Q11 + 3*Q22 + 2*Q12 + 4*Q66) / 8
        self.U2 = (Q11 - Q22) / 2
        self.U3 = (Q11 + Q22 - 2*Q12 - 4*Q66) / 8
        self.U4 = (Q11 + Q22 + 6*Q12 - 4*Q66) / 8
        self.U5 = (Q11 + Q22 - 2*Q12 + 4*Q66) / 8
    
    def laminate_properties_from_V(self, V1, V2, V3, V4):
        """
        Calculate laminate properties from in-plane lamination parameters
        For symmetric balanced laminates
        """
        U1, U2, U3, U4, U5 = self.U1, self.U2, self.U3, self.U4, self.U5
        
        # A matrix components (per unit thickness)
        A11 = U1 + U2*V1 + U3*V3
        A22 = U1 - U2*V1 + U3*V3
        A12 = U4 - U3*V3
        A66 = U5 - U3*V3
        A16 = 0.5 * U2 * V2 + U3 * V4  # Should be 0 for balanced
        A26 = 0.5 * U2 * V2 - U3 * V4  # Should be 0 for balanced
        
        # For balanced laminates, A16 = A26 = 0
        # This requires V2 = V4 = 0
        
        # Compliance matrix (assuming A16=A26=0)
        det = A11*A22 - A12**2
        if det <= 0:
            return None
        
        a11 = A22 / det
        a22 = A11 / det
        a12 = -A12 / det
        a66 = 1 / A66
        
        # Engineering constants
        Ex = 1 / a11 / 1000  # Convert to GPa
        Ey = 1 / a22 / 1000
        Gxy = 1 / a66 / 1000
        nu_xy = -a12 / a11
        
        return {
            'Ex': Ex,
            'Ey': Ey,
            'Gxy': Gxy,
            'nu_xy': nu_xy,
            'V1': V1,
            'V2': V2,
            'V3': V3,
            'V4': V4
        }
    
    def check_V_feasibility(self, V1, V2, V3, V4):
        """
        Check if lamination parameters are in feasible region
        For balanced laminates: V2 = V4 = 0
        """
        # Basic bounds
        if not (-1 <= V1 <= 1 and -1 <= V3 <= 1):
            return False
        
        # Feasibility constraints for balanced laminates
        # |V3| ≤ 1 - 2|V1|
        if abs(V3) > 1 - 2*abs(V1):
            return False
        
        return True

def objective_function_continuous(x, designer):
    """
    Objective: maximize Ey (minimize -Ey)
    For continuous angle case
    x = [V1, V3]  (V2=V4=0 for balanced)
    """
    V1, V3 = x
    V2, V4 = 0, 0  # Balanced constraint
    
    # Check feasibility
    if not designer.check_V_feasibility(V1, V2, V3, V4):
        return 1e10
    
    props = designer.laminate_properties_from_V(V1, V2, V3, V4)
    
    if props is None:
        return 1e10
    
    # Objective: maximize Ey (minimize -Ey)
    objective = -props['Ey']
    
    # Constraints with penalties
    penalty = 0
    
    # Ex ≥ 70 GPa
    if props['Ex'] < 70:
        penalty += 1000 * (70 - props['Ex'])
    
    # Gxy ≥ 15 GPa
    if props['Gxy'] < 15:
        penalty += 1000 * (15 - props['Gxy'])
    
    # νxy < 0.4
    if props['nu_xy'] >= 0.4:
        penalty += 1000 * (props['nu_xy'] - 0.4 + 0.01)
    
    return objective + penalty

def pso_continuous_angles(designer, maxite=200, nnn=100):
    """
    PSO for continuous angle optimization
    Optimize lamination parameters V1, V3
    """
    n_vars = 2  # V1, V3
    
    # PSO parameters
    wmax, wmin = 0.9, 0.4
    c1, c2 = 2.0, 2.0
    
    # Bounds
    LB = np.array([-1.0, -1.0])
    UB = np.array([1.0, 1.0])
    
    print("="*70)
    print("  CASE (a): CONTINUOUS FIBER ORIENTATIONS")
    print("="*70)
    print(f"\nOptimizing lamination parameters V1, V3 (V2=V4=0 for balanced)")
    print(f"Objective: Maximize Ey")
    print(f"Constraints: Ex≥70 GPa, Gxy≥15 GPa, νxy<0.4")
    print(f"\nPSO: Population={nnn}, Iterations={maxite}")
    print("-"*70)
    
    np.random.seed(42)
    
    # Initialization
    x0 = np.zeros((nnn, n_vars))
    for i in range(nnn):
        for j in range(n_vars):
            x0[i, j] = LB[j] + np.random.rand() * (UB[j] - LB[j])
    
    x = x0.copy()
    v = 0.1 * x0
    
    f0 = np.array([objective_function_continuous(x0[i, :], designer) for i in range(nnn)])
    
    fmin0 = np.min(f0)
    index0 = np.argmin(f0)
    
    pbest = x0.copy()
    gbest = x0[index0, :].copy()
    
    ffmin = []
    
    # PSO loop
    ite = 0
    tolerance = 1
    
    while ite < maxite and tolerance > 1e-12:
        w = wmax - (wmax - wmin) * ite / maxite
        
        for i in range(nnn):
            for j in range(n_vars):
                v[i, j] = 0.73 * (w * v[i, j] + 
                                 c1 * np.random.rand() * (pbest[i, j] - x[i, j]) +
                                 c2 * np.random.rand() * (gbest[j] - x[i, j]))
                x[i, j] = x[i, j] + v[i, j]
                
                if x[i, j] < LB[j]:
                    x[i, j] = LB[j]
                elif x[i, j] > UB[j]:
                    x[i, j] = UB[j]
        
        f = np.array([objective_function_continuous(x[i, :], designer) for i in range(nnn)])
        
        for i in range(nnn):
            if f[i] < f0[i]:
                pbest[i, :] = x[i, :]
                f0[i] = f[i]
        
        fmin = np.min(f0)
        index = np.argmin(f0)
        ffmin.append(fmin)
        
        if fmin < fmin0:
            gbest = pbest[index, :].copy()
            fmin0 = fmin
        
        if ite > 50:
            tolerance = abs(ffmin[ite - 50] - fmin0)
        
        if ite % 50 == 0:
            V1, V3 = gbest
            props = designer.laminate_properties_from_V(V1, 0, V3, 0)
            if props:
                print(f"Iter {ite}: Ey={props['Ey']:.2f} GPa, Ex={props['Ex']:.2f}, Gxy={props['Gxy']:.2f}, νxy={props['nu_xy']:.3f}")
        
        ite += 1
    
    return {
        'best_fitness': fmin0,
        'best_solution': gbest,
        'convergence': ffmin
    }

def lamination_params_to_angles_2angle(V1, V3):
    """
    Convert lamination parameters to 2-angle solution
    For 16-layer balanced symmetric: [±θ1/±θ2]2s
    """
    # For 2-angle balanced symmetric design
    # V1 = 0.5*(cos(2θ1) + cos(2θ2))
    # V3 = 0.5*(cos(4θ1) + cos(4θ2))
    
    # Solve system of equations
    # cos(2θ1) + cos(2θ2) = 2*V1
    # cos(4θ1) + cos(4θ2) = 2*V3
    
    # Using cos(4θ) = 2*cos²(2θ) - 1
    # Let c1 = cos(2θ1), c2 = cos(2θ2)
    # c1 + c2 = 2*V1
    # 2*c1² - 1 + 2*c2² - 1 = 2*V3
    # c1² + c2² = V3 + 1
    
    # From c1 + c2 = 2*V1: c2 = 2*V1 - c1
    # Substitute: c1² + (2*V1 - c1)² = V3 + 1
    # 2*c1² - 4*V1*c1 + 4*V1² = V3 + 1
    # c1 = V1 ± sqrt(V1² - 0.5*(4*V1² - V3 - 1))
    # c1 = V1 ± sqrt(0.5*(V3 + 1 - 2*V1²))
    
    discriminant = 0.5 * (V3 + 1 - 2*V1**2)
    if discriminant < 0:
        return None
    
    c1 = V1 + np.sqrt(discriminant)
    c2 = 2*V1 - c1
    
    # Check if valid
    if abs(c1) > 1 or abs(c2) > 1:
        # Try other solution
        c1 = V1 - np.sqrt(discriminant)
        c2 = 2*V1 - c1
        if abs(c1) > 1 or abs(c2) > 1:
            return None
    
    theta1 = np.degrees(np.arccos(c1) / 2)
    theta2 = np.degrees(np.arccos(c2) / 2)
    
    return theta1, theta2

def lamination_params_to_angles_3angle(V1, V3, equal_proportions=True):
    """
    Convert lamination parameters to 3-angle solution
    For 16-layer: multiple combinations possible
    """
    # For 3-angle balanced symmetric with equal proportions
    # Each angle appears with weight 1/3
    # V1 = (cos(2θ1) + cos(2θ2) + cos(2θ3))/3
    # V3 = (cos(4θ1) + cos(4θ2) + cos(4θ3))/3
    
    # This is underdetermined - try common solutions
    # Option 1: Use genetic algorithm or search
    # Option 2: Assume one angle is 0 or 90
    # Option 3: Use symmetric distribution
    
    # Simple approach: assume θ3 = 90°, solve for θ1, θ2
    theta3 = 90
    # cos(2*90) = -1, cos(4*90) = 1
    # V1 = (cos(2θ1) + cos(2θ2) - 1)/3
    # V3 = (cos(4θ1) + cos(4θ2) + 1)/3
    
    V1_adj = 3*V1 + 1
    V3_adj = 3*V3 - 1
    
    # Now solve 2-angle problem
    discriminant = 0.5 * (V3_adj + 1 - 2*V1_adj**2)
    if discriminant < 0:
        return None
    
    c1 = V1_adj + np.sqrt(discriminant)
    c2 = 2*V1_adj - c1
    
    if abs(c1) > 1 or abs(c2) > 1:
        c1 = V1_adj - np.sqrt(discriminant)
        c2 = 2*V1_adj - c1
        if abs(c1) > 1 or abs(c2) > 1:
            return None
    
    theta1 = np.degrees(np.arccos(c1) / 2)
    theta2 = np.degrees(np.arccos(c2) / 2)
    
    return theta1, theta2, theta3

def optimize_discrete_angles(designer, available_angles, case_name):
    """
    Optimize with discrete angles
    """
    print("\n" + "="*70)
    print(f"  CASE {case_name}")
    print("="*70)
    print(f"Available angles: {available_angles}")
    
    best_Ey = -np.inf
    best_config = None
    best_props = None
    
    # For 16-layer balanced symmetric
    # Try different combinations
    from itertools import combinations_with_replacement
    
    # Generate all possible configurations
    # For balanced symmetric: need even number of each non-90/0 angle
    
    configs_tested = 0
    valid_configs = 0
    
    print("\nSearching through angle combinations...")
    
    # Strategy: enumerate different ply distributions
    # Total 16 plies, symmetric (8 unique), balanced
    
    max_configs = 10000
    
    for n_angles in range(1, min(len(available_angles), 5) + 1):
        for angle_combo in combinations_with_replacement(available_angles, n_angles):
            if configs_tested >= max_configs:
                break
            
            # Try different distributions
            for distribution in generate_distributions(n_angles, 8):
                if configs_tested >= max_configs:
                    break
                
                # Build angle sequence
                angles = []
                for angle, count in zip(angle_combo, distribution):
                    angles.extend([angle] * count)
                
                if len(angles) != 8:
                    continue
                
                # Make symmetric
                full_angles = angles + angles[::-1]
                
                # Calculate lamination parameters
                V_params = calculate_V_from_angles(full_angles)
                props = designer.laminate_properties_from_V(*V_params)
                
                if props is None:
                    continue
                
                configs_tested += 1
                
                # Check constraints
                if (props['Ex'] >= 70 and props['Gxy'] >= 15 and 
                    props['nu_xy'] < 0.4):
                    valid_configs += 1
                    
                    if props['Ey'] > best_Ey:
                        best_Ey = props['Ey']
                        best_config = full_angles
                        best_props = props
                        print(f"  New best: Ey={best_Ey:.2f} GPa, angles={angle_combo}, dist={distribution}")
            
            if configs_tested >= max_configs:
                break
        
        if configs_tested >= max_configs:
            break
    
    print(f"\nConfigurations tested: {configs_tested}")
    print(f"Valid configurations: {valid_configs}")
    
    return best_config, best_props

def generate_distributions(n_angles, total_plies):
    """Generate all distributions of total_plies across n_angles"""
    if n_angles == 1:
        yield [total_plies]
        return
    
    for i in range(total_plies + 1):
        for rest in generate_distributions(n_angles - 1, total_plies - i):
            yield [i] + rest

def calculate_V_from_angles(angles):
    """Calculate lamination parameters from angle list"""
    n = len(angles)
    V1 = sum(np.cos(2 * np.radians(theta)) for theta in angles) / n
    V2 = sum(np.sin(2 * np.radians(theta)) for theta in angles) / n
    V3 = sum(np.cos(4 * np.radians(theta)) for theta in angles) / n
    V4 = sum(np.sin(4 * np.radians(theta)) for theta in angles) / n
    return V1, V2, V3, V4

def plot_feasible_region_and_solution(designer, results_continuous):
    """Plot feasible region in V1-V3 space with optimal solution"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left plot: Feasible region
    V1_range = np.linspace(-1, 1, 100)
    V3_range = np.linspace(-1, 1, 100)
    V1_grid, V3_grid = np.meshgrid(V1_range, V3_range)
    
    feasible = np.zeros_like(V1_grid)
    Ey_grid = np.zeros_like(V1_grid)
    
    for i in range(len(V1_range)):
        for j in range(len(V3_range)):
            V1, V3 = V1_grid[j, i], V3_grid[j, i]
            if designer.check_V_feasibility(V1, 0, V3, 0):
                props = designer.laminate_properties_from_V(V1, 0, V3, 0)
                if props and props['Ex'] >= 70 and props['Gxy'] >= 15 and props['nu_xy'] < 0.4:
                    feasible[j, i] = 1
                    Ey_grid[j, i] = props['Ey']
    
    # Plot feasible region
    contour = ax1.contourf(V1_grid, V3_grid, Ey_grid, levels=20, cmap='viridis', alpha=0.7)
    ax1.contour(V1_grid, V3_grid, feasible, levels=[0.5], colors='red', linewidths=2)
    
    # Plot optimal solution
    V1_opt, V3_opt = results_continuous['best_solution']
    ax1.plot(V1_opt, V3_opt, 'r*', markersize=20, label='Optimal')
    
    ax1.set_xlabel('V₁', fontsize=12)
    ax1.set_ylabel('V₃', fontsize=12)
    ax1.set_title('Feasible Region (Ey contours)', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    plt.colorbar(contour, ax=ax1, label='Ey (GPa)')
    
    # Right plot: Convergence
    # Convert -Ey back to Ey for plotting
    Ey_convergence = [-val for val in results_continuous['convergence']]
    ax2.plot(Ey_convergence, linewidth=2, color='steelblue')
    ax2.set_xlabel('Iteration', fontsize=12)
    ax2.set_ylabel('Ey (GPa)', fontsize=12)
    ax2.set_title('PSO Convergence', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('problem3_continuous_results.png', dpi=300, bbox_inches='tight')
    print("\n✓ Plot saved: problem3_continuous_results.png")
    plt.close()

def plot_comparison(results_dict):
    """Compare all three cases"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Extract data
    cases = []
    Ey_vals = []
    Ex_vals = []
    Gxy_vals = []
    nu_vals = []
    
    for case_name, (config, props) in results_dict.items():
        if props:
            cases.append(case_name)
            Ey_vals.append(props['Ey'])
            Ex_vals.append(props['Ex'])
            Gxy_vals.append(props['Gxy'])
            nu_vals.append(props['nu_xy'])
    
    # Bar chart of properties
    x = np.arange(len(cases))
    width = 0.2
    
    ax1.bar(x - 1.5*width, Ex_vals, width, label='Ex', alpha=0.8)
    ax1.bar(x - 0.5*width, Ey_vals, width, label='Ey', alpha=0.8)
    ax1.bar(x + 0.5*width, Gxy_vals, width, label='Gxy', alpha=0.8)
    ax1.bar(x + 1.5*width, [v*100 for v in nu_vals], width, label='νxy×100', alpha=0.8)
    
    ax1.set_ylabel('Value', fontsize=12)
    ax1.set_title('Property Comparison', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(cases, rotation=15, ha='right')
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add requirement lines
    ax1.axhline(y=70, color='r', linestyle='--', alpha=0.5, label='Ex req')
    ax1.axhline(y=15, color='g', linestyle='--', alpha=0.5, label='Gxy req')
    
    # Objective comparison
    ax2.bar(cases, Ey_vals, color='steelblue', alpha=0.8, edgecolor='black')
    ax2.set_ylabel('Ey (GPa)', fontsize=12)
    ax2.set_title('Objective: Maximize Ey', fontsize=14, fontweight='bold')
    ax2.set_xticklabels(cases, rotation=15, ha='right')
    ax2.grid(True, alpha=0.3, axis='y')
    
    for i, v in enumerate(Ey_vals):
        ax2.text(i, v + 1, f'{v:.1f}', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('problem3_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Plot saved: problem3_comparison.png")
    plt.close()

if __name__ == "__main__":
    start_time = time.time()
    
    # Material properties (same as Problem 1)
    designer = LaminationParameterDesign(
        E1=138,     # GPa
        E2=8.96,    # GPa
        G12=7.10,   # GPa
        nu12=0.30
    )
    
    print("\n" + "="*70)
    print("  PROBLEM 3: 16-LAYER BALANCED SYMMETRIC LAMINATE")
    print("  Using Miki's Lamination Parameters")
    print("="*70)
    print(f"\nMaterial: Graphite/Epoxy")
    print(f"  E₁ = 138 GPa, E₂ = 8.96 GPa, G₁₂ = 7.10 GPa, ν₁₂ = 0.30")
    print(f"\nObjective: Maximize Ey")
    print(f"Constraints: Ex ≥ 70 GPa, Gxy ≥ 15 GPa, νxy < 0.4")
    print(f"Configuration: 16-layer balanced symmetric")
    
    results_dict = {}
    
    # CASE (a): Continuous angles
    print("\n\n")
    results_cont = pso_continuous_angles(designer, maxite=200, nnn=100)
    V1_opt, V3_opt = results_cont['best_solution']
    props_cont = designer.laminate_properties_from_V(V1_opt, 0, V3_opt, 0)
    
    print(f"\n{'='*70}")
    print("CASE (a) - CONTINUOUS ANGLES RESULTS:")
    print(f"{'='*70}")
    print(f"Optimal Lamination Parameters:")
    print(f"  V₁ = {V1_opt:.4f}")
    print(f"  V₃ = {V3_opt:.4f}")
    print(f"  (V₂ = V₄ = 0 for balanced)")
    print(f"\nLaminate Properties:")
    print(f"  Ey  = {props_cont['Ey']:.2f} GPa  (OBJECTIVE)")
    print(f"  Ex  = {props_cont['Ex']:.2f} GPa  (req: ≥70) {'✓' if props_cont['Ex']>=70 else '✗'}")
    print(f"  Gxy = {props_cont['Gxy']:.2f} GPa  (req: ≥15) {'✓' if props_cont['Gxy']>=15 else '✗'}")
    print(f"  νxy = {props_cont['nu_xy']:.3f}  (req: <0.4) {'✓' if props_cont['nu_xy']<0.4 else '✗'}")
    
    # Convert to angles
    angles_2 = lamination_params_to_angles_2angle(V1_opt, V3_opt)
    if angles_2:
        print(f"\n2-Angle Solution: [±{angles_2[0]:.1f}/±{angles_2[1]:.1f}]₂ₛ")
    
    angles_3 = lamination_params_to_angles_3angle(V1_opt, V3_opt)
    if angles_3:
        print(f"3-Angle Solution: [±{angles_3[0]:.1f}/±{angles_3[1]:.1f}/±{angles_3[2]:.1f}]ₛ (with 90°)")
    
    results_dict['Continuous\n(2-angle)'] = (angles_2, props_cont)
    
    plot_feasible_region_and_solution(designer, results_cont)
    
    # CASE (b): Discrete angles - 0, ±45, 90
    print("\n\n")
    config_b, props_b = optimize_discrete_angles(
        designer, [0, 45, -45, 90], "(b): 0°, ±45°, 90°"
    )
    
    if props_b:
        print(f"\n{'='*70}")
        print("CASE (b) RESULTS:")
        print(f"{'='*70}")
        print(f"Optimal layup: {config_b}")
        print(f"\nLaminate Properties:")
        print(f"  Ey  = {props_b['Ey']:.2f} GPa  (OBJECTIVE)")
        print(f"  Ex  = {props_b['Ex']:.2f} GPa  (req: ≥70) {'✓' if props_b['Ex']>=70 else '✗'}")
        print(f"  Gxy = {props_b['Gxy']:.2f} GPa  (req: ≥15) {'✓' if props_b['Gxy']>=15 else '✗'}")
        print(f"  νxy = {props_b['nu_xy']:.3f}  (req: <0.4) {'✓' if props_b['nu_xy']<0.4 else '✗'}")
        results_dict['Discrete\n(0,±45,90)'] = (config_b, props_b)
    
    # CASE (c): Discrete angles - 0, ±30, ±60, 90
    print("\n\n")
    config_c, props_c = optimize_discrete_angles(
        designer, [0, 30, -30, 60, -60, 90], "(c): 0°, ±30°, ±60°, 90°"
    )
    
    if props_c:
        print(f"\n{'='*70}")
        print("CASE (c) RESULTS:")
        print(f"{'='*70}")
        print(f"Optimal layup: {config_c}")
        print(f"\nLaminate Properties:")
        print(f"  Ey  = {props_c['Ey']:.2f} GPa  (OBJECTIVE)")
        print(f"  Ex  = {props_c['Ex']:.2f} GPa  (req: ≥70) {'✓' if props_c['Ex']>=70 else '✗'}")
        print(f"  Gxy = {props_c['Gxy']:.2f} GPa  (req: ≥15) {'✓' if props_c['Gxy']>=15 else '✗'}")
        print(f"  νxy = {props_c['nu_xy']:.3f}  (req: <0.4) {'✓' if props_c['nu_xy']<0.4 else '✗'}")
        results_dict['Discrete\n(0,±30,±60,90)'] = (config_c, props_c)
    
    # Comparison plot
    if len(results_dict) > 1:
        print("\n")
        plot_comparison(results_dict)
    
    elapsed_time = time.time() - start_time
    print(f"\n{'='*70}")
    print(f"⏱ Total execution time: {elapsed_time:.2f} seconds")
    print(f"{'='*70}")
