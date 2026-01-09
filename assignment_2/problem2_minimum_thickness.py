"""
Assignment 2 - Problem 2: Minimum Thickness Laminate Design
Design laminate with minimum thickness using discrete angles
Constraints on Poisson's ratio, shear modulus, and elastic moduli
"""

import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations_with_replacement
import time

class LaminateDesigner:
    """
    Laminate design with specific angle options
    """
    
    def __init__(self, E1, E2, G12, nu12, t):
        self.E1 = E1 * 1000  # Convert GPa to MPa
        self.E2 = E2 * 1000
        self.G12 = G12 * 1000
        self.nu12 = nu12
        self.nu21 = nu12 * E2 / E1
        self.t = t
        
        # Available angles
        self.available_angles = [0, 15, -15, 30, -30, 45, -45, 60, -60, 75, -75, 90]
    
    def get_Q_matrix(self):
        """Calculate reduced stiffness matrix Q (in MPa)"""
        E1, E2, nu12, nu21 = self.E1, self.E2, self.nu12, self.nu21
        
        Q11 = E1 / (1 - nu12 * nu21)
        Q22 = E2 / (1 - nu12 * nu21)
        Q12 = nu12 * E2 / (1 - nu12 * nu21)
        Q66 = self.G12
        
        return np.array([
            [Q11, Q12, 0],
            [Q12, Q22, 0],
            [0, 0, Q66]
        ])
    
    def get_Qbar(self, theta_deg):
        """Calculate transformed stiffness matrix Q̄"""
        theta = np.radians(theta_deg)
        c = np.cos(theta)
        s = np.sin(theta)
        
        Q = self.get_Q_matrix()
        
        # Transformation matrix
        T = np.array([
            [c**2, s**2, 2*s*c],
            [s**2, c**2, -2*s*c],
            [-s*c, s*c, c**2 - s**2]
        ])
        
        T_inv = np.linalg.inv(T)
        Qbar = np.dot(np.dot(T_inv, Q), T_inv.T)
        
        return Qbar
    
    def analyze_laminate(self, angles):
        """
        Analyze laminate properties
        
        Parameters:
        angles: list of ply angles
        
        Returns:
        dict with elastic properties
        """
        if len(angles) == 0:
            return None
        
        n_plies = len(angles)
        t = self.t
        h = n_plies * t
        
        # Calculate A matrix
        A = np.zeros((3, 3))
        for angle in angles:
            Qbar = self.get_Qbar(angle)
            A += Qbar * t
        
        # Calculate compliance matrix
        try:
            A_inv = np.linalg.inv(A)
        except:
            return None
        
        # Laminate elastic constants
        Ex = 1 / (h * A_inv[0, 0])  # MPa
        Ey = 1 / (h * A_inv[1, 1])  # MPa
        Gxy = 1 / (h * A_inv[2, 2])  # MPa
        nu_xy = -A_inv[0, 1] / A_inv[0, 0]
        nu_yx = -A_inv[1, 0] / A_inv[1, 1]
        
        return {
            'Ex': Ex / 1000,      # Convert to GPa
            'Ey': Ey / 1000,      # Convert to GPa
            'Gxy': Gxy / 1000,    # Convert to GPa
            'nu_xy': nu_xy,
            'nu_yx': nu_yx,
            'n_plies': n_plies,
            'thickness': h
        }

def check_constraints(props):
    """
    Check if design satisfies all constraints
    
    Constraints:
    - 0.2 ≤ ν_xy ≤ 0.7
    - G_xy ≥ 5 GPa
    - E_x ≥ 22 GPa
    - E_y ≥ 18 GPa
    """
    if props is None:
        return False
    
    c1 = 0.2 <= props['nu_xy'] <= 0.7
    c2 = props['Gxy'] >= 5.0
    c3 = props['Ex'] >= 22.0
    c4 = props['Ey'] >= 18.0
    
    return c1 and c2 and c3 and c4

def objective_function(x, designer):
    """
    Objective: minimize number of plies (thickness)
    With penalty for constraint violations
    """
    # x represents number of plies at each angle
    # x = [n0, n15, n_15, n30, n_30, n45, n_45, n60, n_60, n75, n_75, n90]
    
    ply_counts = [int(np.round(val)) for val in x]
    
    # Build angle list
    angles = []
    for i, angle in enumerate(designer.available_angles):
        angles.extend([angle] * ply_counts[i])
    
    if len(angles) == 0:
        return 1e10
    
    # Analyze laminate
    props = designer.analyze_laminate(angles)
    
    if props is None:
        return 1e10
    
    # Objective: minimize plies
    objective = props['n_plies']
    
    # Calculate constraint violations
    penalty = 0
    
    # Poisson's ratio constraint
    if props['nu_xy'] < 0.2:
        penalty += 10000 * (0.2 - props['nu_xy'])
    elif props['nu_xy'] > 0.7:
        penalty += 10000 * (props['nu_xy'] - 0.7)
    
    # Shear modulus constraint
    if props['Gxy'] < 5.0:
        penalty += 10000 * (5.0 - props['Gxy'])
    
    # Longitudinal modulus constraint
    if props['Ex'] < 22.0:
        penalty += 10000 * (22.0 - props['Ex'])
    
    # Transverse modulus constraint
    if props['Ey'] < 18.0:
        penalty += 10000 * (18.0 - props['Ey'])
    
    return objective + penalty

def pso_optimization(designer, maxite=100, nnn=50, maxrun=5):
    """
    PSO for laminate design
    """
    n_vars = len(designer.available_angles)
    
    # PSO parameters
    wmax = 0.9
    wmin = 0.4
    c1 = 2.0
    c2 = 2.0
    
    # Bounds (0 to 20 plies per angle)
    LB = np.zeros(n_vars)
    UB = 20 * np.ones(n_vars)
    
    best_fitness_all_runs = []
    best_solution_all_runs = []
    convergence_all_runs = []
    
    np.random.seed(42)
    
    print("="*70)
    print("  PROBLEM 2: MINIMUM THICKNESS LAMINATE DESIGN")
    print("="*70)
    print(f"\nAvailable angles: {designer.available_angles}")
    print(f"Objective: Minimize number of plies")
    print(f"\nConstraints:")
    print(f"  - 0.2 ≤ ν_xy ≤ 0.7")
    print(f"  - G_xy ≥ 5 GPa")
    print(f"  - E_x ≥ 22 GPa")
    print(f"  - E_y ≥ 18 GPa")
    print(f"\nPSO Parameters:")
    print(f"  Population: {nnn}, Iterations: {maxite}, Runs: {maxrun}")
    print("\n" + "-"*70)
    
    for run in range(maxrun):
        print(f"\nRun {run+1}/{maxrun}")
        
        # Initialization
        x0 = np.zeros((nnn, n_vars))
        for i in range(nnn):
            for j in range(n_vars):
                x0[i, j] = np.round(LB[j] + np.random.rand() * (UB[j] - LB[j]))
        
        x = x0.copy()
        v = 0.1 * x0
        
        f0 = np.array([objective_function(x0[i, :], designer) for i in range(nnn)])
        
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
                    x[i, j] = np.round(x[i, j] + v[i, j])
                    
                    if x[i, j] < LB[j]:
                        x[i, j] = LB[j]
                    elif x[i, j] > UB[j]:
                        x[i, j] = UB[j]
            
            f = np.array([objective_function(x[i, :], designer) for i in range(nnn)])
            
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
            
            ite += 1
        
        best_fitness_all_runs.append(fmin0)
        best_solution_all_runs.append(gbest.copy())
        convergence_all_runs.append(ffmin)
        
        # Build and check solution
        ply_counts = [int(np.round(val)) for val in gbest]
        angles = []
        for i, angle in enumerate(designer.available_angles):
            angles.extend([angle] * ply_counts[i])
        props = designer.analyze_laminate(angles)
        
        print(f"  Best plies: {len(angles)}, Fitness: {fmin0:.2f}")
        if props and check_constraints(props):
            print(f"  ✓ All constraints satisfied")
        else:
            print(f"  ✗ Constraints violated")
    
    best_run = np.argmin(best_fitness_all_runs)
    
    return {
        'best_fitness': best_fitness_all_runs[best_run],
        'best_solution': best_solution_all_runs[best_run],
        'best_run': best_run,
        'all_fitness': best_fitness_all_runs,
        'all_solutions': best_solution_all_runs,
        'convergence': convergence_all_runs
    }

def study_parameter_effects(designer):
    """
    Study effects of population size and max iterations
    """
    print("\n" + "="*70)
    print("  PARAMETER SENSITIVITY STUDY")
    print("="*70)
    
    # Test different population sizes
    pop_sizes = [20, 50, 100, 200]
    max_iter = 100
    
    pop_results = {}
    
    print("\n1. Population Size Effect (fixed iterations = 100)")
    print("-"*70)
    
    for pop in pop_sizes:
        print(f"\nTesting population size: {pop}")
        result = pso_optimization(designer, maxite=max_iter, nnn=pop, maxrun=3)
        pop_results[pop] = result
    
    # Test different iteration counts
    iter_counts = [50, 100, 200, 300]
    pop_size = 50
    
    iter_results = {}
    
    print("\n\n2. Iteration Count Effect (fixed population = 50)")
    print("-"*70)
    
    for iters in iter_counts:
        print(f"\nTesting iterations: {iters}")
        result = pso_optimization(designer, maxite=iters, nnn=pop_size, maxrun=3)
        iter_results[iters] = result
    
    return pop_results, iter_results

def plot_results(results, designer):
    """Plot optimization results"""
    fig = plt.figure(figsize=(16, 5))
    
    # Plot 1: Convergence
    ax1 = plt.subplot(1, 3, 1)
    for i, conv in enumerate(results['convergence']):
        ax1.semilogy(conv, label=f'Run {i+1}', alpha=0.7)
    ax1.set_xlabel('Iteration', fontsize=12)
    ax1.set_ylabel('Fitness (Number of Plies)', fontsize=12)
    ax1.set_title('PSO Convergence', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Plot 2: Ply distribution
    ax2 = plt.subplot(1, 3, 2)
    ply_counts = [int(np.round(val)) for val in results['best_solution']]
    
    x_pos = np.arange(len(designer.available_angles))
    bars = ax2.bar(x_pos, ply_counts, color='steelblue', alpha=0.7, edgecolor='black')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels([f"{a}°" for a in designer.available_angles], rotation=45)
    ax2.set_xlabel('Ply Angle', fontsize=12)
    ax2.set_ylabel('Number of Plies', fontsize=12)
    ax2.set_title('Optimal Ply Distribution', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add values on bars
    for bar, count in zip(bars, ply_counts):
        if count > 0:
            ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                    f'{count}', ha='center', va='bottom', fontsize=9)
    
    # Plot 3: Properties comparison
    ax3 = plt.subplot(1, 3, 3)
    
    angles = []
    for i, angle in enumerate(designer.available_angles):
        angles.extend([angle] * ply_counts[i])
    props = designer.analyze_laminate(angles)
    
    requirements = ['ν_xy', 'G_xy\n(GPa)', 'E_x\n(GPa)', 'E_y\n(GPa)']
    achieved = [props['nu_xy'], props['Gxy'], props['Ex'], props['Ey']]
    constraints_min = [0.2, 5, 22, 18]
    constraints_max = [0.7, None, None, None]
    
    x_pos = np.arange(len(requirements))
    bars = ax3.bar(x_pos, achieved, color='lightgreen', alpha=0.7, edgecolor='black', label='Achieved')
    
    for i, (ach, cmin) in enumerate(zip(achieved, constraints_min)):
        ax3.plot([i-0.4, i+0.4], [cmin, cmin], 'r--', linewidth=2)
        if constraints_max[i]:
            ax3.plot([i-0.4, i+0.4], [constraints_max[i], constraints_max[i]], 'r--', linewidth=2)
    
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(requirements)
    ax3.set_ylabel('Value', fontsize=12)
    ax3.set_title('Properties vs Requirements', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.legend()
    
    plt.tight_layout()
    plt.savefig('problem2_results.png', dpi=300, bbox_inches='tight')
    print("\n✓ Plot saved: problem2_results.png")
    plt.close()

def plot_parameter_study(pop_results, iter_results):
    """Plot parameter sensitivity study"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Population size effect
    pop_sizes = sorted(pop_results.keys())
    best_plies = [np.min(pop_results[p]['all_fitness']) for p in pop_sizes]
    mean_plies = [np.mean(pop_results[p]['all_fitness']) for p in pop_sizes]
    
    ax1.plot(pop_sizes, best_plies, 'o-', linewidth=2, markersize=8, label='Best')
    ax1.plot(pop_sizes, mean_plies, 's-', linewidth=2, markersize=8, label='Mean')
    ax1.set_xlabel('Population Size', fontsize=12)
    ax1.set_ylabel('Number of Plies', fontsize=12)
    ax1.set_title('Effect of Population Size', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Iteration count effect
    iter_counts = sorted(iter_results.keys())
    best_plies = [np.min(iter_results[i]['all_fitness']) for i in iter_counts]
    mean_plies = [np.mean(iter_results[i]['all_fitness']) for i in iter_counts]
    
    ax2.plot(iter_counts, best_plies, 'o-', linewidth=2, markersize=8, label='Best')
    ax2.plot(iter_counts, mean_plies, 's-', linewidth=2, markersize=8, label='Mean')
    ax2.set_xlabel('Maximum Iterations', fontsize=12)
    ax2.set_ylabel('Number of Plies', fontsize=12)
    ax2.set_title('Effect of Iteration Count', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('problem2_parameter_study.png', dpi=300, bbox_inches='tight')
    print("✓ Plot saved: problem2_parameter_study.png")
    plt.close()

def print_results(results, designer):
    """Print detailed results"""
    ply_counts = [int(np.round(val)) for val in results['best_solution']]
    
    angles = []
    for i, angle in enumerate(designer.available_angles):
        angles.extend([angle] * ply_counts[i])
    
    props = designer.analyze_laminate(angles)
    
    print("\n" + "="*70)
    print("  PROBLEM 2 RESULTS")
    print("="*70)
    
    print(f"\n✓ OPTIMAL DESIGN:")
    print(f"  Total plies: {len(angles)}")
    print(f"  Total thickness: {props['thickness']:.4f} mm")
    
    print(f"\n✓ PLY DISTRIBUTION:")
    for angle, count in zip(designer.available_angles, ply_counts):
        if count > 0:
            print(f"  {angle:4}°: {count:2} plies")
    
    print(f"\n✓ LAMINATE PROPERTIES:")
    print(f"  E_x   = {props['Ex']:.2f} GPa  (req: ≥ 22 GPa) {'✓' if props['Ex'] >= 22 else '✗'}")
    print(f"  E_y   = {props['Ey']:.2f} GPa  (req: ≥ 18 GPa) {'✓' if props['Ey'] >= 18 else '✗'}")
    print(f"  G_xy  = {props['Gxy']:.2f} GPa  (req: ≥ 5 GPa) {'✓' if props['Gxy'] >= 5 else '✗'}")
    print(f"  ν_xy  = {props['nu_xy']:.3f}  (req: 0.2-0.7) {'✓' if 0.2 <= props['nu_xy'] <= 0.7 else '✗'}")
    
    print(f"\n✓ CONSTRAINT CHECK: {'ALL SATISFIED' if check_constraints(props) else 'VIOLATED'}")
    
    print("="*70)

if __name__ == "__main__":
    start_time = time.time()
    
    # Material properties
    designer = LaminateDesigner(
        E1=38.6,    # GPa
        E2=8.27,    # GPa
        G12=4.14,   # GPa
        nu12=0.28,
        t=0.125     # mm
    )
    
    # Main optimization
    print("\nMAIN OPTIMIZATION RUN")
    results = pso_optimization(designer, maxite=100, nnn=50, maxrun=5)
    print_results(results, designer)
    plot_results(results, designer)
    
    # Parameter sensitivity study
    print("\n\nPARAMETER SENSITIVITY STUDY")
    pop_results, iter_results = study_parameter_effects(designer)
    plot_parameter_study(pop_results, iter_results)
    
    elapsed_time = time.time() - start_time
    print(f"\n⏱ Total execution time: {elapsed_time:.2f} seconds")
