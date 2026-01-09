"""
PSO Mishra's Bird Function
Particle Swarm Optimization for finding minimum of Mishra's Bird Function
Converted from MATLAB to Python

Mishra's Bird Function is a complex optimization test function
f(x,y) = sin(y)*exp((1-cos(x))^2) + cos(x)*exp((1-sin(y))^2) + (x-y)^2
Subject to: (x+5)^2 + (y+5)^2 <= 25 (circular constraint)
Domain: -10 <= x <= 0, -6.5 <= y <= 0
Global minimum: f(-3.1302468, -1.5821422) ≈ -106.7645367
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

def objective_function(x):
    """
    Mishra's Bird Function with circular constraint
    
    Parameters:
    x: array [x1, x2]
    
    Returns:
    f: penalized fitness value
    """
    x1, x2 = x[0], x[1]
    
    # Mishra's Bird Function
    of = (np.sin(x2) * np.exp((1 - np.cos(x1))**2) + 
          np.cos(x1) * np.exp((1 - np.sin(x2))**2) + 
          (x1 - x2)**2)
    
    # Circular constraint: (x+5)^2 + (y+5)^2 <= 25
    c0 = np.array([
        (x1 + 5)**2 + (x2 + 5)**2 - 25
    ])
    
    # Penalty for constraint violations
    c = np.where(c0 > 0, 1, 0)
    penalty = 1000000
    f = of + penalty * np.sum(c)
    
    return f

def pso_optimization(maxite=100, maxrun=10, nnn=10, mmm=2):
    """
    Particle Swarm Optimization Algorithm for Mishra's Bird Function
    
    Parameters:
    maxite: maximum iterations
    maxrun: maximum runs
    nnn: population size
    mmm: number of variables
    """
    # PSO parameters
    wmax = 0.9
    wmin = 0.4
    c1 = 2.0
    c2 = 2.0
    
    # Bounds
    LB = np.array([-10.0, -6.5])
    UB = np.array([0.0, 0.0])
    
    # Storage for results
    best_fitness_all_runs = []
    best_solution_all_runs = []
    convergence_all_runs = []
    
    np.random.seed(42)  # For reproducibility
    
    print("="*70)
    print("  PSO MISHRA'S BIRD FUNCTION OPTIMIZATION")
    print("="*70)
    print(f"\nPopulation size: {nnn}")
    print(f"Max iterations: {maxite}")
    print(f"Number of runs: {maxrun}")
    print(f"Variables: {mmm} (continuous)")
    print(f"Domain: x ∈ [{LB[0]}, {UB[0]}], y ∈ [{LB[1]}, {UB[1]}]")
    print(f"Constraint: (x+5)² + (y+5)² ≤ 25")
    print(f"Known global minimum: f(-3.1302, -1.5821) ≈ -106.7645")
    print("\n" + "-"*70)
    
    for run in range(maxrun):
        print(f"\nRun {run+1}/{maxrun}")
        
        # Initialization
        x0 = np.zeros((nnn, mmm))
        for i in range(nnn):
            for j in range(mmm):
                x0[i, j] = LB[j] + np.random.rand() * (UB[j] - LB[j])
        
        x = x0.copy()
        v = 0.1 * x0
        
        # Evaluate initial population
        f0 = np.array([objective_function(x0[i, :]) for i in range(nnn)])
        
        fmin0 = np.min(f0)
        index0 = np.argmin(f0)
        
        pbest = x0.copy()
        gbest = x0[index0, :].copy()
        
        # Storage for convergence
        ffmin = []
        
        # PSO main loop
        ite = 0
        tolerance = 1
        
        while ite < maxite and tolerance > 1e-12:
            # Update inertia weight
            w = wmax - (wmax - wmin) * ite / maxite
            
            # Update velocity
            for i in range(nnn):
                for j in range(mmm):
                    v[i, j] = 0.73 * (w * v[i, j] + 
                                     c1 * np.random.rand() * (pbest[i, j] - x[i, j]) +
                                     c2 * np.random.rand() * (gbest[j] - x[i, j]))
            
            # Update position (continuous, no rounding)
            for i in range(nnn):
                for j in range(mmm):
                    x[i, j] = x[i, j] + v[i, j]
            
            # Handle boundary violations
            for i in range(nnn):
                for j in range(mmm):
                    if x[i, j] < LB[j]:
                        x[i, j] = LB[j]
                    elif x[i, j] > UB[j]:
                        x[i, j] = UB[j]
            
            # Evaluate fitness
            f = np.array([objective_function(x[i, :]) for i in range(nnn)])
            
            # Update pbest
            for i in range(nnn):
                if f[i] < f0[i]:
                    pbest[i, :] = x[i, :]
                    f0[i] = f[i]
            
            # Find best particle
            fmin = np.min(f0)
            index = np.argmin(f0)
            ffmin.append(fmin)
            
            # Update gbest
            if fmin < fmin0:
                gbest = pbest[index, :].copy()
                fmin0 = fmin
            
            # Calculate tolerance
            if ite > 100:
                tolerance = abs(ffmin[ite - 100] - fmin0)
            
            ite += 1
        
        # Store results
        best_fitness_all_runs.append(fmin0)
        best_solution_all_runs.append(gbest.copy())
        convergence_all_runs.append(ffmin)
        
        print(f"  Best fitness: {fmin0:.6f}")
        print(f"  Best solution: x={gbest[0]:.6f}, y={gbest[1]:.6f}")
        print(f"  Iterations: {ite}")
    
    # Find overall best
    best_run = np.argmin(best_fitness_all_runs)
    best_fitness = best_fitness_all_runs[best_run]
    best_solution = best_solution_all_runs[best_run]
    
    return {
        'best_fitness': best_fitness,
        'best_solution': best_solution,
        'best_run': best_run,
        'all_fitness': best_fitness_all_runs,
        'all_solutions': best_solution_all_runs,
        'convergence': convergence_all_runs
    }

def plot_results(results):
    """Plot convergence curves and 3D surface"""
    fig = plt.figure(figsize=(16, 5))
    
    # Plot 1: Convergence curves
    ax1 = plt.subplot(1, 3, 1)
    for i, conv in enumerate(results['convergence']):
        ax1.plot(conv, label=f'Run {i+1}', alpha=0.7)
    ax1.set_xlabel('Iteration', fontsize=12)
    ax1.set_ylabel('Best Fitness', fontsize=12)
    ax1.set_title("PSO Convergence - All Runs", fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='best', fontsize=8)
    ax1.axhline(y=-106.7645, color='red', linestyle='--', linewidth=2, 
                label='Known Global Min', alpha=0.5)
    
    # Plot 2: 3D Surface with constraint region
    ax2 = plt.subplot(1, 3, 2, projection='3d')
    
    # Create mesh grid
    x1 = np.linspace(-10, 0, 100)
    x2 = np.linspace(-6.5, 0, 100)
    X1, X2 = np.meshgrid(x1, x2)
    
    # Calculate Z values
    Z = np.zeros_like(X1)
    for i in range(X1.shape[0]):
        for j in range(X1.shape[1]):
            # Apply constraint mask
            if (X1[i,j] + 5)**2 + (X2[i,j] + 5)**2 <= 25:
                Z[i,j] = (np.sin(X2[i,j]) * np.exp((1 - np.cos(X1[i,j]))**2) + 
                         np.cos(X1[i,j]) * np.exp((1 - np.sin(X2[i,j]))**2) + 
                         (X1[i,j] - X2[i,j])**2)
            else:
                Z[i,j] = np.nan
    
    surf = ax2.plot_surface(X1, X2, Z, cmap='viridis', alpha=0.7, edgecolor='none')
    
    # Plot best solution
    best_sol = results['best_solution']
    ax2.scatter([best_sol[0]], [best_sol[1]], [results['best_fitness']], 
               color='red', s=100, marker='*', edgecolors='black', linewidths=2,
               label='PSO Solution')
    
    ax2.set_xlabel('x', fontsize=10)
    ax2.set_ylabel('y', fontsize=10)
    ax2.set_zlabel('f(x,y)', fontsize=10)
    ax2.set_title("Mishra's Bird Function\n3D Surface", fontsize=14, fontweight='bold')
    ax2.view_init(elev=20, azim=45)
    
    # Plot 3: Contour plot with constraint circle
    ax3 = plt.subplot(1, 3, 3)
    
    # Contour plot
    contour = ax3.contour(X1, X2, Z, levels=20, cmap='viridis', alpha=0.6)
    ax3.clabel(contour, inline=True, fontsize=8)
    
    # Draw constraint circle
    theta = np.linspace(0, 2*np.pi, 100)
    circle_x = -5 + 5*np.cos(theta)
    circle_y = -5 + 5*np.sin(theta)
    ax3.plot(circle_x, circle_y, 'r--', linewidth=2, label='Constraint Boundary')
    
    # Plot all solutions
    for i, sol in enumerate(results['all_solutions']):
        ax3.plot(sol[0], sol[1], 'o', markersize=8, alpha=0.6, 
                label=f'Run {i+1}' if i < 5 else '')
    
    # Highlight best solution
    best_sol = results['best_solution']
    ax3.plot(best_sol[0], best_sol[1], '*', markersize=15, color='red', 
            markeredgecolor='black', markeredgewidth=2, label='Best Solution')
    
    # Plot known global minimum
    ax3.plot(-3.1302468, -1.5821422, 'X', markersize=12, color='lime',
            markeredgecolor='black', markeredgewidth=2, label='Known Global Min')
    
    ax3.set_xlabel('x', fontsize=12)
    ax3.set_ylabel('y', fontsize=12)
    ax3.set_title("Contour Plot with Solutions", fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.legend(loc='best', fontsize=8)
    ax3.set_xlim(-10, 0)
    ax3.set_ylim(-6.5, 0)
    
    plt.tight_layout()
    plt.savefig('pso_mishrasbird_results.png', dpi=300, bbox_inches='tight')
    print("\n✓ Plot saved: pso_mishrasbird_results.png")
    plt.show()

def print_summary(results):
    """Print detailed summary of results"""
    print("\n" + "="*70)
    print("  OPTIMIZATION RESULTS SUMMARY")
    print("="*70)
    
    best_sol = results['best_solution']
    
    print(f"\n✓ OPTIMAL SOLUTION (from Run {results['best_run']+1}):")
    print(f"  x = {best_sol[0]:.8f}")
    print(f"  y = {best_sol[1]:.8f}")
    print(f"\n✓ OBJECTIVE FUNCTION VALUE:")
    print(f"  f(x,y) = {results['best_fitness']:.8f}")
    
    # Check constraint
    constraint_val = (best_sol[0] + 5)**2 + (best_sol[1] + 5)**2 - 25
    print(f"\n✓ CONSTRAINT SATISFACTION:")
    print(f"  (x+5)² + (y+5)² - 25 = {constraint_val:.6f} {'✓ (satisfied)' if constraint_val <= 0 else '✗ (violated)'}")
    
    # Compare with known global minimum
    known_min_x = -3.1302468
    known_min_y = -1.5821422
    known_min_f = -106.7645367
    
    error_x = abs(best_sol[0] - known_min_x)
    error_y = abs(best_sol[1] - known_min_y)
    error_f = abs(results['best_fitness'] - known_min_f)
    
    print(f"\n✓ COMPARISON WITH KNOWN GLOBAL MINIMUM:")
    print(f"  Known: x* = {known_min_x:.8f}, y* = {known_min_y:.8f}, f* = {known_min_f:.8f}")
    print(f"  Error in x: {error_x:.8f}")
    print(f"  Error in y: {error_y:.8f}")
    print(f"  Error in f: {error_f:.8f}")
    print(f"  Relative error: {(error_f/abs(known_min_f)*100):.4f}%")
    
    print(f"\n✓ STATISTICS ACROSS ALL RUNS:")
    print(f"  Best fitness:  {np.min(results['all_fitness']):.8f}")
    print(f"  Worst fitness: {np.max(results['all_fitness']):.8f}")
    print(f"  Mean fitness:  {np.mean(results['all_fitness']):.8f}")
    print(f"  Std dev:       {np.std(results['all_fitness']):.8f}")
    print("="*70)

if __name__ == "__main__":
    start_time = time.time()
    
    # Run PSO optimization
    results = pso_optimization(maxite=100, maxrun=10, nnn=10, mmm=2)
    
    # Print summary
    print_summary(results)
    
    # Plot results
    plot_results(results)
    
    elapsed_time = time.time() - start_time
    print(f"\n⏱ Total execution time: {elapsed_time:.2f} seconds")
