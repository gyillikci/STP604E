"""
PSO Example 5.21
Particle Swarm Optimization for constrained optimization problem
Converted from MATLAB to Python

Problem: Minimize -(64.88 + 11.05*no - 4.326*nf - 6.724*nn)
Subject to:
    6.724*no + 4.326*nf - 11.05*nn - 44.88 <= 0
    1.05 + 1.082*no - 2.163*nf + 1.082*nn <= 0
    8 - no - 2*nf - nn <= 0
    no + 2*nf + nn - 8 <= 0
    0 <= no <= 8
    0 <= nf <= 4
    0 <= nn <= 8
"""

import numpy as np
import matplotlib.pyplot as plt
import time

def objective_function(x):
    """
    Calculate objective function with penalty for constraint violations
    
    Parameters:
    x: array [no, nf, nn]
    
    Returns:
    f: penalized fitness value
    """
    no, nf, nn = x[0], x[1], x[2]
    
    # Objective function (negative because we're minimizing)
    of = -(64.88 + 11.05*no - 4.326*nf - 6.724*nn)
    
    # Constraints (c <= 0 for feasible solutions)
    c0 = np.array([
        6.724*no + 4.326*nf - 11.05*nn - 44.88,
        1.05 + 1.082*no - 2.163*nf + 1.082*nn,
        8 - no - 2*nf - nn,
        no + 2*nf + nn - 8
    ])
    
    # Penalty for constraint violations
    c = np.where(c0 > 0, 1, 0)
    penalty = 1000000
    f = of + penalty * np.sum(c)
    
    return f

def pso_optimization(maxite=20, maxrun=5, nnn=100, mmm=3):
    """
    Particle Swarm Optimization Algorithm
    
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
    LB = np.array([0.0, 0.0, 0.0])
    UB = np.array([8.0, 4.0, 8.0])
    
    # Storage for results
    best_fitness_all_runs = []
    best_solution_all_runs = []
    convergence_all_runs = []
    
    np.random.seed(42)  # For reproducibility
    
    print("="*70)
    print("  PSO EXAMPLE 5.21 - OPTIMIZATION")
    print("="*70)
    print(f"\nPopulation size: {nnn}")
    print(f"Max iterations: {maxite}")
    print(f"Number of runs: {maxrun}")
    print(f"Variables: {mmm}")
    print(f"Bounds: no=[{LB[0]},{UB[0]}], nf=[{LB[1]},{UB[1]}], nn=[{LB[2]},{UB[2]}]")
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
        
        print(f"  Best fitness: {fmin0:.6f}")
        print(f"  Best solution: no={gbest[0]:.2f}, nf={gbest[1]:.2f}, nn={gbest[2]:.2f}")
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
    """Plot convergence curves for all runs"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Convergence curves for all runs
    for i, conv in enumerate(results['convergence']):
        ax1.semilogy(conv, label=f'Run {i+1}', alpha=0.7)
    ax1.set_xlabel('Iteration', fontsize=12)
    ax1.set_ylabel('Best Fitness (log scale)', fontsize=12)
    ax1.set_title('PSO Convergence - All Runs', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='best', fontsize=8)
    
    # Plot 2: Best fitness across runs
    ax2.bar(range(1, len(results['all_fitness'])+1), results['all_fitness'], 
            color='steelblue', alpha=0.7, edgecolor='black')
    ax2.set_xlabel('Run Number', fontsize=12)
    ax2.set_ylabel('Best Fitness', fontsize=12)
    ax2.set_title('Best Fitness per Run', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Highlight best run
    best_run = results['best_run']
    ax2.bar(best_run+1, results['all_fitness'][best_run], 
            color='red', alpha=0.7, edgecolor='black', label='Best Run')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('pso_example521_results.png', dpi=300, bbox_inches='tight')
    print("\n✓ Plot saved: pso_example521_results.png")
    plt.show()

def print_summary(results):
    """Print detailed summary of results"""
    print("\n" + "="*70)
    print("  OPTIMIZATION RESULTS SUMMARY")
    print("="*70)
    
    best_sol = results['best_solution']
    
    # Calculate actual objective value (not penalized)
    actual_obj = -(64.88 + 11.05*best_sol[0] - 4.326*best_sol[1] - 6.724*best_sol[2])
    
    print(f"\n✓ OPTIMAL SOLUTION (from Run {results['best_run']+1}):")
    print(f"  no = {best_sol[0]:.4f}")
    print(f"  nf = {best_sol[1]:.4f}")
    print(f"  nn = {best_sol[2]:.4f}")
    print(f"\n✓ OBJECTIVE FUNCTION VALUE:")
    print(f"  f = {actual_obj:.6f}")
    
    # Check constraints
    print(f"\n✓ CONSTRAINT SATISFACTION:")
    c1 = 6.724*best_sol[0] + 4.326*best_sol[1] - 11.05*best_sol[2] - 44.88
    c2 = 1.05 + 1.082*best_sol[0] - 2.163*best_sol[1] + 1.082*best_sol[2]
    c3 = 8 - best_sol[0] - 2*best_sol[1] - best_sol[2]
    c4 = best_sol[0] + 2*best_sol[1] + best_sol[2] - 8
    
    print(f"  Constraint 1: {c1:.6f} {'✓ (satisfied)' if c1 <= 0 else '✗ (violated)'}")
    print(f"  Constraint 2: {c2:.6f} {'✓ (satisfied)' if c2 <= 0 else '✗ (violated)'}")
    print(f"  Constraint 3: {c3:.6f} {'✓ (satisfied)' if c3 <= 0 else '✗ (violated)'}")
    print(f"  Constraint 4: {c4:.6f} {'✓ (satisfied)' if c4 <= 0 else '✗ (violated)'}")
    
    print(f"\n✓ STATISTICS ACROSS ALL RUNS:")
    print(f"  Best fitness:  {np.min(results['all_fitness']):.6f}")
    print(f"  Worst fitness: {np.max(results['all_fitness']):.6f}")
    print(f"  Mean fitness:  {np.mean(results['all_fitness']):.6f}")
    print(f"  Std dev:       {np.std(results['all_fitness']):.6f}")
    print("="*70)

if __name__ == "__main__":
    start_time = time.time()
    
    # Run PSO optimization
    results = pso_optimization(maxite=20, maxrun=5, nnn=100, mmm=3)
    
    # Print summary
    print_summary(results)
    
    # Plot results
    plot_results(results)
    
    elapsed_time = time.time() - start_time
    print(f"\n⏱ Total execution time: {elapsed_time:.2f} seconds")
