"""
Assignment 2 - Problem 1: Thermal Expansion Optimization
Optimize laminate stacking sequence [±θ₁/±30°/±θ₂]ₛ to minimize |αₓ|
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import time

class ThermalLaminate:
    """
    Laminate analysis including thermal expansion properties
    Based on Classical Laminated Plate Theory (CLPT)
    """
    
    def __init__(self, E1, E2, G12, nu12, alpha1, alpha2, t):
        """
        Initialize material properties
        
        Parameters:
        E1, E2: Moduli in fiber and transverse directions (GPa)
        G12: Shear modulus (GPa)
        nu12: Poisson's ratio
        alpha1, alpha2: CTEs in fiber and transverse directions (1/°C)
        t: Ply thickness (mm)
        """
        self.E1 = E1
        self.E2 = E2
        self.G12 = G12
        self.nu12 = nu12
        self.nu21 = nu12 * E2 / E1
        self.alpha1 = alpha1
        self.alpha2 = alpha2
        self.t = t
        
    def get_Q_matrix(self):
        """Calculate reduced stiffness matrix Q"""
        E1, E2, nu12, nu21 = self.E1, self.E2, self.nu12, self.nu21
        
        Q11 = E1 / (1 - nu12 * nu21)
        Q22 = E2 / (1 - nu12 * nu21)
        Q12 = nu12 * E2 / (1 - nu12 * nu21)
        Q66 = self.G12
        
        Q = np.array([
            [Q11, Q12, 0],
            [Q12, Q22, 0],
            [0, 0, Q66]
        ])
        
        return Q
    
    def get_T_matrix(self, theta_deg):
        """Calculate transformation matrix T for angle theta"""
        theta = np.radians(theta_deg)
        c = np.cos(theta)
        s = np.sin(theta)
        
        T = np.array([
            [c**2, s**2, 2*s*c],
            [s**2, c**2, -2*s*c],
            [-s*c, s*c, c**2 - s**2]
        ])
        
        return T
    
    def get_Qbar(self, theta_deg):
        """Calculate transformed stiffness matrix Q̄"""
        Q = self.get_Q_matrix()
        T = self.get_T_matrix(theta_deg)
        T_inv = np.linalg.inv(T)
        
        Qbar = np.dot(np.dot(T_inv, Q), T_inv.T)
        
        return Qbar
    
    def get_alpha_bar(self, theta_deg):
        """Calculate transformed thermal expansion coefficients"""
        theta = np.radians(theta_deg)
        c = np.cos(theta)
        s = np.sin(theta)
        
        alpha1, alpha2 = self.alpha1, self.alpha2
        
        alpha_x = alpha1 * c**2 + alpha2 * s**2
        alpha_y = alpha1 * s**2 + alpha2 * c**2
        alpha_xy = 2 * (alpha1 - alpha2) * s * c
        
        return np.array([alpha_x, alpha_y, alpha_xy])
    
    def analyze_laminate(self, angles):
        """
        Analyze laminate with given ply angles
        
        Parameters:
        angles: list of ply angles from bottom to top
        
        Returns:
        dict with A, B, D matrices and thermal properties
        """
        n_plies = len(angles)
        t = self.t
        
        # Initialize matrices
        A = np.zeros((3, 3))
        B = np.zeros((3, 3))
        D = np.zeros((3, 3))
        
        # Calculate z-coordinates (measured from laminate midplane)
        h = n_plies * t
        z = np.linspace(-h/2, h/2, n_plies + 1)
        
        # Build ABD matrices
        for k in range(n_plies):
            Qbar_k = self.get_Qbar(angles[k])
            z_k = z[k]
            z_k1 = z[k + 1]
            
            A += Qbar_k * (z_k1 - z_k)
            B += 0.5 * Qbar_k * (z_k1**2 - z_k**2)
            D += (1/3) * Qbar_k * (z_k1**3 - z_k**3)
        
        # Calculate thermal force and moment resultants
        N_T = np.zeros(3)
        M_T = np.zeros(3)
        
        for k in range(n_plies):
            Qbar_k = self.get_Qbar(angles[k])
            alpha_k = self.get_alpha_bar(angles[k])
            z_k = z[k]
            z_k1 = z[k + 1]
            
            N_T += np.dot(Qbar_k, alpha_k) * (z_k1 - z_k)
            M_T += 0.5 * np.dot(Qbar_k, alpha_k) * (z_k1**2 - z_k**2)
        
        # Calculate ABD matrix
        ABD = np.block([
            [A, B],
            [B, D]
        ])
        
        # Calculate laminate thermal expansion coefficients
        # For symmetric laminates: B = 0, so α̅ = A⁻¹ · N_T
        try:
            A_inv = np.linalg.inv(A)
            alpha_laminate = np.dot(A_inv, N_T)
        except:
            alpha_laminate = np.array([np.inf, np.inf, np.inf])
        
        # Calculate elastic constants from A matrix
        A_inv = np.linalg.inv(A) if np.linalg.det(A) != 0 else np.zeros((3,3))
        
        Ex = 1 / (h * A_inv[0, 0]) if A_inv[0, 0] != 0 else 0
        Ey = 1 / (h * A_inv[1, 1]) if A_inv[1, 1] != 0 else 0
        Gxy = 1 / (h * A_inv[2, 2]) if A_inv[2, 2] != 0 else 0
        nu_xy = -A_inv[0, 1] / A_inv[0, 0] if A_inv[0, 0] != 0 else 0
        nu_yx = -A_inv[1, 0] / A_inv[1, 1] if A_inv[1, 1] != 0 else 0
        
        return {
            'A': A,
            'B': B,
            'D': D,
            'alpha': alpha_laminate,
            'Ex': Ex / 1000,  # Convert to GPa
            'Ey': Ey / 1000,
            'Gxy': Gxy / 1000,
            'nu_xy': nu_xy,
            'nu_yx': nu_yx,
            'h': h
        }

def create_stacking_sequence(theta1, theta2):
    """
    Create stacking sequence [±θ₁/±30°/±θ₂]ₛ
    Returns full laminate from bottom to top
    """
    # One quarter of laminate (before symmetry)
    quarter = [theta1, -theta1, 30, -30, theta2, -theta2]
    
    # Symmetric laminate
    full_laminate = quarter + quarter[::-1]
    
    return full_laminate

def objective_function(x, laminate):
    """
    Objective function for PSO: minimize |αₓ|
    """
    theta1 = int(np.round(x[0]))
    theta2 = int(np.round(x[1]))
    
    # Constraint: theta2 > 60
    if theta2 <= 60:
        return 1e10  # Large penalty
    
    angles = create_stacking_sequence(theta1, theta2)
    
    try:
        result = laminate.analyze_laminate(angles)
        alpha_x = result['alpha'][0]
        
        # Minimize absolute value
        return abs(alpha_x)
    except:
        return 1e10

def pso_optimization(laminate, maxite=100, maxrun=10, nnn=50):
    """
    PSO to find optimal θ₁ and θ₂
    """
    # PSO parameters
    wmax = 0.9
    wmin = 0.4
    c1 = 2.0
    c2 = 2.0
    
    # Bounds
    LB = np.array([-90, 61])  # θ₁: [-90, 90], θ₂: > 60
    UB = np.array([90, 90])
    
    best_fitness_all_runs = []
    best_solution_all_runs = []
    convergence_all_runs = []
    
    np.random.seed(42)
    
    print("="*70)
    print("  PROBLEM 1: THERMAL EXPANSION OPTIMIZATION")
    print("="*70)
    print(f"\nLaminate: [±θ₁/±30°/±θ₂]ₛ")
    print(f"Objective: Minimize |αₓ|")
    print(f"Constraint: θ₂ > 60°")
    print(f"\nPSO Parameters:")
    print(f"  Population size: {nnn}")
    print(f"  Max iterations: {maxite}")
    print(f"  Number of runs: {maxrun}")
    print("\n" + "-"*70)
    
    for run in range(maxrun):
        print(f"\nRun {run+1}/{maxrun}")
        
        # Initialization
        x0 = np.zeros((nnn, 2))
        for i in range(nnn):
            x0[i, 0] = np.round(LB[0] + np.random.rand() * (UB[0] - LB[0]))
            x0[i, 1] = np.round(LB[1] + np.random.rand() * (UB[1] - LB[1]))
        
        x = x0.copy()
        v = 0.1 * x0
        
        # Evaluate initial population
        f0 = np.array([objective_function(x0[i, :], laminate) for i in range(nnn)])
        
        fmin0 = np.min(f0)
        index0 = np.argmin(f0)
        
        pbest = x0.copy()
        gbest = x0[index0, :].copy()
        
        ffmin = []
        
        # PSO main loop
        ite = 0
        tolerance = 1
        
        while ite < maxite and tolerance > 1e-12:
            w = wmax - (wmax - wmin) * ite / maxite
            
            # Update velocity and position
            for i in range(nnn):
                for j in range(2):
                    v[i, j] = 0.73 * (w * v[i, j] + 
                                     c1 * np.random.rand() * (pbest[i, j] - x[i, j]) +
                                     c2 * np.random.rand() * (gbest[j] - x[i, j]))
                    x[i, j] = np.round(x[i, j] + v[i, j])
                    
                    if x[i, j] < LB[j]:
                        x[i, j] = LB[j]
                    elif x[i, j] > UB[j]:
                        x[i, j] = UB[j]
            
            # Evaluate fitness
            f = np.array([objective_function(x[i, :], laminate) for i in range(nnn)])
            
            # Update pbest
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
            
            if ite > 100:
                tolerance = abs(ffmin[ite - 100] - fmin0)
            
            ite += 1
        
        best_fitness_all_runs.append(fmin0)
        best_solution_all_runs.append(gbest.copy())
        convergence_all_runs.append(ffmin)
        
        print(f"  Best |αₓ|: {fmin0:.6e} 1/°C")
        print(f"  θ₁ = {int(gbest[0])}°, θ₂ = {int(gbest[1])}°")
    
    best_run = np.argmin(best_fitness_all_runs)
    
    return {
        'best_fitness': best_fitness_all_runs[best_run],
        'best_solution': best_solution_all_runs[best_run],
        'best_run': best_run,
        'all_fitness': best_fitness_all_runs,
        'all_solutions': best_solution_all_runs,
        'convergence': convergence_all_runs
    }

def plot_cte_variation(laminate, theta1_opt, theta2_opt):
    """
    Plot αₓ, αᵧ, αₓᵧ as functions of θ₁ and θ₂
    """
    theta1_range = np.arange(-90, 91, 5)
    theta2_range = np.arange(61, 91, 2)
    
    THETA1, THETA2 = np.meshgrid(theta1_range, theta2_range)
    
    ALPHA_X = np.zeros_like(THETA1, dtype=float)
    ALPHA_Y = np.zeros_like(THETA1, dtype=float)
    ALPHA_XY = np.zeros_like(THETA1, dtype=float)
    
    for i in range(THETA1.shape[0]):
        for j in range(THETA1.shape[1]):
            angles = create_stacking_sequence(THETA1[i, j], THETA2[i, j])
            result = laminate.analyze_laminate(angles)
            ALPHA_X[i, j] = result['alpha'][0] * 1e6  # Convert to 1e-6/°C
            ALPHA_Y[i, j] = result['alpha'][1] * 1e6
            ALPHA_XY[i, j] = result['alpha'][2] * 1e6
    
    fig = plt.figure(figsize=(18, 5))
    
    # Plot 1: αₓ
    ax1 = fig.add_subplot(131, projection='3d')
    surf1 = ax1.plot_surface(THETA1, THETA2, ALPHA_X, cmap='coolwarm', alpha=0.8)
    ax1.scatter([theta1_opt], [theta2_opt], 
                [laminate.analyze_laminate(create_stacking_sequence(theta1_opt, theta2_opt))['alpha'][0]*1e6],
                color='red', s=100, marker='*', edgecolors='black', linewidths=2)
    ax1.set_xlabel('θ₁ (°)', fontsize=10)
    ax1.set_ylabel('θ₂ (°)', fontsize=10)
    ax1.set_zlabel('αₓ (×10⁻⁶/°C)', fontsize=10)
    ax1.set_title('Longitudinal CTE', fontsize=12, fontweight='bold')
    plt.colorbar(surf1, ax=ax1, shrink=0.5)
    
    # Plot 2: αᵧ
    ax2 = fig.add_subplot(132, projection='3d')
    surf2 = ax2.plot_surface(THETA1, THETA2, ALPHA_Y, cmap='viridis', alpha=0.8)
    ax2.scatter([theta1_opt], [theta2_opt],
                [laminate.analyze_laminate(create_stacking_sequence(theta1_opt, theta2_opt))['alpha'][1]*1e6],
                color='red', s=100, marker='*', edgecolors='black', linewidths=2)
    ax2.set_xlabel('θ₁ (°)', fontsize=10)
    ax2.set_ylabel('θ₂ (°)', fontsize=10)
    ax2.set_zlabel('αᵧ (×10⁻⁶/°C)', fontsize=10)
    ax2.set_title('Transverse CTE', fontsize=12, fontweight='bold')
    plt.colorbar(surf2, ax=ax2, shrink=0.5)
    
    # Plot 3: αₓᵧ
    ax3 = fig.add_subplot(133, projection='3d')
    surf3 = ax3.plot_surface(THETA1, THETA2, ALPHA_XY, cmap='plasma', alpha=0.8)
    ax3.scatter([theta1_opt], [theta2_opt],
                [laminate.analyze_laminate(create_stacking_sequence(theta1_opt, theta2_opt))['alpha'][2]*1e6],
                color='red', s=100, marker='*', edgecolors='black', linewidths=2)
    ax3.set_xlabel('θ₁ (°)', fontsize=10)
    ax3.set_ylabel('θ₂ (°)', fontsize=10)
    ax3.set_zlabel('αₓᵧ (×10⁻⁶/°C)', fontsize=10)
    ax3.set_title('Shear CTE', fontsize=12, fontweight='bold')
    plt.colorbar(surf3, ax=ax3, shrink=0.5)
    
    plt.tight_layout()
    plt.savefig('problem1_cte_variation.png', dpi=300, bbox_inches='tight')
    print("\n✓ Plot saved: problem1_cte_variation.png")
    plt.close()

def plot_convergence(results):
    """Plot PSO convergence"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Convergence curves
    for i, conv in enumerate(results['convergence']):
        ax1.semilogy(conv, label=f'Run {i+1}', alpha=0.7)
    ax1.set_xlabel('Iteration', fontsize=12)
    ax1.set_ylabel('|αₓ| (1/°C, log scale)', fontsize=12)
    ax1.set_title('PSO Convergence', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='best', fontsize=8)
    
    # Best solutions scatter
    theta1_vals = [int(sol[0]) for sol in results['all_solutions']]
    theta2_vals = [int(sol[1]) for sol in results['all_solutions']]
    
    scatter = ax2.scatter(theta1_vals, theta2_vals, c=results['all_fitness'],
                         s=200, cmap='coolwarm', alpha=0.7, edgecolors='black', linewidths=2)
    ax2.scatter(int(results['best_solution'][0]), int(results['best_solution'][1]),
               s=300, marker='*', color='lime', edgecolors='black', linewidths=2,
               label='Best Solution', zorder=5)
    ax2.set_xlabel('θ₁ (°)', fontsize=12)
    ax2.set_ylabel('θ₂ (°)', fontsize=12)
    ax2.set_title('Solution Space', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    plt.colorbar(scatter, ax=ax2, label='|αₓ| (1/°C)')
    
    plt.tight_layout()
    plt.savefig('problem1_convergence.png', dpi=300, bbox_inches='tight')
    print("✓ Plot saved: problem1_convergence.png")
    plt.close()

def print_results(laminate, results):
    """Print comprehensive results"""
    theta1 = int(results['best_solution'][0])
    theta2 = int(results['best_solution'][1])
    
    angles = create_stacking_sequence(theta1, theta2)
    result = laminate.analyze_laminate(angles)
    
    print("\n" + "="*70)
    print("  PROBLEM 1 RESULTS")
    print("="*70)
    
    print(f"\n✓ OPTIMAL STACKING SEQUENCE:")
    print(f"  θ₁ = {theta1}°")
    print(f"  θ₂ = {theta2}°")
    print(f"  Full sequence: [±{theta1}/±30/±{theta2}]ₛ")
    print(f"  Detailed: {angles}")
    
    print(f"\n✓ THERMAL EXPANSION COEFFICIENTS:")
    print(f"  αₓ  = {result['alpha'][0]:.6e} 1/°C  ({result['alpha'][0]*1e6:.4f} ×10⁻⁶/°C)")
    print(f"  αᵧ  = {result['alpha'][1]:.6e} 1/°C  ({result['alpha'][1]*1e6:.4f} ×10⁻⁶/°C)")
    print(f"  αₓᵧ = {result['alpha'][2]:.6e} 1/°C  ({result['alpha'][2]*1e6:.4f} ×10⁻⁶/°C)")
    
    print(f"\n✓ ELASTIC CONSTANTS:")
    print(f"  Eₓ    = {result['Ex']:.4f} GPa")
    print(f"  Eᵧ    = {result['Ey']:.4f} GPa")
    print(f"  Gₓᵧ   = {result['Gxy']:.4f} GPa")
    print(f"  νₓᵧ   = {result['nu_xy']:.4f}")
    print(f"  νᵧₓ   = {result['nu_yx']:.4f}")
    print(f"  Total thickness = {result['h']:.4f} mm")
    
    print(f"\n✓ OPTIMIZATION STATISTICS:")
    print(f"  Best |αₓ|: {results['best_fitness']:.6e} 1/°C")
    print(f"  Mean |αₓ|: {np.mean(results['all_fitness']):.6e} 1/°C")
    print(f"  Std dev:   {np.std(results['all_fitness']):.6e} 1/°C")
    print(f"  Best run:  {results['best_run'] + 1}")
    
    print("="*70)

if __name__ == "__main__":
    start_time = time.time()
    
    # Material properties
    laminate = ThermalLaminate(
        E1=138,      # GPa
        E2=8.96,     # GPa
        G12=7.10,    # GPa
        nu12=0.3,
        alpha1=-0.3e-6,   # 1/°C
        alpha2=28.1e-6,   # 1/°C
        t=0.125      # mm
    )
    
    # Run PSO optimization
    results = pso_optimization(laminate, maxite=100, maxrun=10, nnn=50)
    
    # Print results
    print_results(laminate, results)
    
    # Generate plots
    theta1_opt = int(results['best_solution'][0])
    theta2_opt = int(results['best_solution'][1])
    
    plot_convergence(results)
    plot_cte_variation(laminate, theta1_opt, theta2_opt)
    
    elapsed_time = time.time() - start_time
    print(f"\n⏱ Total execution time: {elapsed_time:.2f} seconds")
