"""
PSO Example 5.44
Particle Swarm Optimization for composite laminate optimization
Converted from MATLAB to Python

Problem: Minimize total ply count = 2*(n0+n90) + 4*(n30+n45+n60)
Subject to strain constraints for a composite laminate under loading
"""

import numpy as np
import matplotlib.pyplot as plt
import time

def objective_function(x):
    """
    Calculate objective function with penalty for constraint violations
    
    Parameters:
    x: array [n0, n30, n45, n60, n90] - ply counts
    
    Returns:
    f: penalized fitness value
    """
    n0, n30, n45, n60, n90 = x[0], x[1], x[2], x[3], x[4]
    
    # Loading conditions
    Nx = 10000  # N/mm
    Nxy = 3000  # N/mm
    epsx_lim = 0.004  # Strain limit
    gammaxy_lim = 0.006  # Shear strain limit
    
    # Stiffness matrix coefficients (from laminate theory)
    A11 = 0.186717*n0 + 0.230683*n30 + 0.127219*n45 + 0.230683*n60 + 0.0190754*n90
    A22 = 0.0190754*n0 + 0.0630414*n30 + 0.127219*n45 + 0.0630414*n60 + 0.186717*n90
    A12 = 0.00572262*n0 + 0.0703753*n30 + 0.0900187*n45 + 0.0703753*n60 + 0.00572262*n90
    A66 = 0.0093*n0 + 0.0775301*n30 + 0.0971735*n45 + 0.0775301*n60 + 0.0093*n90
    
    # Construct stiffness matrix
    A = np.array([
        [A11, A12, 0],
        [A12, A22, 0],
        [0, 0, A66]
    ]) * 1e6  # Convert to N/mm
    
    # Load vector
    N = np.array([Nx, 0, Nxy])
    
    # Calculate strains
    try:
        eps = np.linalg.solve(A, N)
    except:
        # If singular matrix, return high penalty
        return 1e10
    
    # Objective: minimize total ply count (with weighting for symmetry)
    of = 2*(n0 + n90) + 4*(n30 + n45 + n60)
    
    # Constraints
    c0 = np.array([
        eps[0] - epsx_lim,      # Normal strain constraint
        eps[2] - gammaxy_lim    # Shear strain constraint
    ])
    
    # Penalty for constraint violations or invalid values
    c = np.zeros(len(c0))
    for i in range(len(c0)):
        if c0[i] > 0 or np.isinf(c0[i]) or np.isnan(c0[i]):
            c[i] = 1
    
    penalty = 1000000
    f = of + penalty * np.sum(c)
    
    return f

def pso_optimization(maxite=100, maxrun=10, nnn=50, mmm=5):
    """
    Particle Swarm Optimization Algorithm for laminate design
    
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
    
    # Bounds (integer ply counts)
    LB = np.zeros(mmm)
    UB = np.array([50, 50, 50, 50, 50])  # Maximum plies for each orientation
    
    # Storage for results
    best_fitness_all_runs = []
    best_solution_all_runs = []
    convergence_all_runs = []
    
    np.random.seed(42)  # For reproducibility
    
    print("="*70)
    print("  PSO EXAMPLE 5.44 - COMPOSITE LAMINATE OPTIMIZATION")
    print("="*70)
    print(f"\nPopulation size: {nnn}")
    print(f"Max iterations: {maxite}")
    print(f"Number of runs: {maxrun}")
    print(f"Variables: {mmm} (n0, n30, n45, n60, n90)")
    print(f"Objective: Minimize total ply count")
    print("\n" + "-"*70)
    
    for run in range(maxrun):
        print(f"\nRun {run+1}/{maxrun}")
        
        # Initialization
        x0 = np.zeros((nnn, mmm))
        for i in range(nnn):
            for j in range(mmm):
                x0[i, j] = np.round(LB[j] + np.random.rand() * (UB[j] - LB[j]))
        
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
            
            # Update position
            for i in range(nnn):
                for j in range(mmm):
                    x[i, j] = np.round(x[i, j] + v[i, j])
            
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
        
        print(f"  Best fitness: {fmin0:.2f}")
        print(f"  Best solution: n0={int(gbest[0])}, n30={int(gbest[1])}, n45={int(gbest[2])}, n60={int(gbest[3])}, n90={int(gbest[4])}")
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
    """Plot convergence curves and ply distribution"""
    fig = plt.figure(figsize=(15, 5))
    
    # Plot 1: Convergence curves
    ax1 = plt.subplot(1, 3, 1)
    for i, conv in enumerate(results['convergence']):
        ax1.semilogy(conv, label=f'Run {i+1}', alpha=0.7)
    ax1.set_xlabel('Iteration', fontsize=12)
    ax1.set_ylabel('Best Fitness (log scale)', fontsize=12)
    ax1.set_title('PSO Convergence - All Runs', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='best', fontsize=8)
    
    # Plot 2: Best fitness across runs
    ax2 = plt.subplot(1, 3, 2)
    ax2.bar(range(1, len(results['all_fitness'])+1), results['all_fitness'], 
            color='steelblue', alpha=0.7, edgecolor='black')
    ax2.set_xlabel('Run Number', fontsize=12)
    ax2.set_ylabel('Best Fitness (Total Plies)', fontsize=12)
    ax2.set_title('Best Fitness per Run', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Highlight best run
    best_run = results['best_run']
    ax2.bar(best_run+1, results['all_fitness'][best_run], 
            color='red', alpha=0.7, edgecolor='black', label='Best Run')
    ax2.legend()
    
    # Plot 3: Optimal ply distribution
    ax3 = plt.subplot(1, 3, 3)
    best_sol = results['best_solution']
    orientations = ['0°', '30°', '45°', '60°', '90°']
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
    
    bars = ax3.bar(orientations, best_sol, color=colors, alpha=0.7, edgecolor='black')
    ax3.set_ylabel('Number of Plies', fontsize=12)
    ax3.set_title('Optimal Ply Distribution', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('pso_example544_results.png', dpi=300, bbox_inches='tight')
    print("\n✓ Plot saved: pso_example544_results.png")
    plt.show()

def print_summary(results):
    """Print detailed summary of results"""
    print("\n" + "="*70)
    print("  OPTIMIZATION RESULTS SUMMARY")
    print("="*70)
    
    best_sol = results['best_solution']
    
    print(f"\n✓ OPTIMAL PLY CONFIGURATION (from Run {results['best_run']+1}):")
    print(f"  n0°  = {int(best_sol[0])} plies")
    print(f"  n30° = {int(best_sol[1])} plies")
    print(f"  n45° = {int(best_sol[2])} plies")
    print(f"  n60° = {int(best_sol[3])} plies")
    print(f"  n90° = {int(best_sol[4])} plies")
    
    total_plies = 2*(best_sol[0] + best_sol[4]) + 4*(best_sol[1] + best_sol[2] + best_sol[3])
    print(f"\n✓ TOTAL PLY COUNT: {int(total_plies)}")
    
    # Calculate strains for verification
    n0, n30, n45, n60, n90 = best_sol
    A11 = 0.186717*n0 + 0.230683*n30 + 0.127219*n45 + 0.230683*n60 + 0.0190754*n90
    A22 = 0.0190754*n0 + 0.0630414*n30 + 0.127219*n45 + 0.0630414*n60 + 0.186717*n90
    A12 = 0.00572262*n0 + 0.0703753*n30 + 0.0900187*n45 + 0.0703753*n60 + 0.00572262*n90
    A66 = 0.0093*n0 + 0.0775301*n30 + 0.0971735*n45 + 0.0775301*n60 + 0.0093*n90
    
    A = np.array([[A11, A12, 0], [A12, A22, 0], [0, 0, A66]]) * 1e6
    N = np.array([10000, 0, 3000])
    eps = np.linalg.solve(A, N)
    
    print(f"\n✓ STRAIN ANALYSIS:")
    print(f"  εx    = {eps[0]:.6f} (limit: 0.004000) {'✓' if eps[0] <= 0.004 else '✗'}")
    print(f"  εy    = {eps[1]:.6f}")
    print(f"  γxy   = {eps[2]:.6f} (limit: 0.006000) {'✓' if eps[2] <= 0.006 else '✗'}")
    
    print(f"\n✓ STATISTICS ACROSS ALL RUNS:")
    print(f"  Best total plies:  {int(np.min(results['all_fitness']))}")
    print(f"  Worst total plies: {int(np.max(results['all_fitness']))}")
    print(f"  Mean total plies:  {np.mean(results['all_fitness']):.2f}")
    print(f"  Std dev:           {np.std(results['all_fitness']):.2f}")
    print("="*70)

if __name__ == "__main__":
    start_time = time.time()
    
    # Run PSO optimization
    results = pso_optimization(maxite=100, maxrun=10, nnn=50, mmm=5)
    
    # Print summary
    print_summary(results)
    
    # Plot results
    plot_results(results)
    
    elapsed_time = time.time() - start_time
    print(f"\n⏱ Total execution time: {elapsed_time:.2f} seconds")
