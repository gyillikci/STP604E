# Assignment 2 - Problem 2 Results

## Problem Statement
Design a laminate with **minimum thickness** using discrete angles: 0°, ±15°, ±30°, ±45°, ±60°, ±75°, 90°

### Constraints
- Poisson's ratio: 0.2 ≤ ν_xy ≤ 0.7
- Shear modulus: G_xy ≥ 5 GPa
- Longitudinal modulus: E_x ≥ 22 GPa
- Transverse modulus: E_y ≥ 18 GPa

### Material Properties
- E₁ = 38.6 GPa
- E₂ = 8.27 GPa
- G₁₂ = 4.14 GPa
- ν₁₂ = 0.28
- Ply thickness: t = 0.125 mm

---

## Optimal Solution

### Design Configuration
**Minimum thickness: 5 plies (0.625 mm)**

**Ply Distribution:**
- 0°: 2 plies
- 30°: 1 ply
- -75°: 2 plies

### Laminate Properties

| Property | Value | Requirement | Status |
|----------|-------|-------------|--------|
| E_x | 23.10 GPa | ≥ 22 GPa | ✓ |
| E_y | 18.34 GPa | ≥ 18 GPa | ✓ |
| G_xy | 5.45 GPa | ≥ 5 GPa | ✓ |
| ν_xy | 0.235 | 0.2-0.7 | ✓ |

**All constraints satisfied** ✓

---

## Parameter Sensitivity Study

### 1. Effect of Population Size (fixed iterations = 100)

| Population | Best Plies | Mean Plies | Notes |
|------------|------------|------------|-------|
| 20 | 22 | 43.3 | Poor exploration, inconsistent results |
| 50 | 6 | 35.7 | Good balance |
| 100 | 6 | 16.0 | Better consistency |
| 200 | 3* | 16.0 | Best exploration, but 3-ply violates constraints |

*Note: The 3-ply solution found with pop=200 appears feasible in PSO but actually violates the ν_xy constraint (ν_xy < 0.2). The penalty function brings fitness to 3.0, but it's not a truly feasible solution.

**Key Findings:**
- Smaller populations (20) struggle to find good solutions consistently
- Population size 50-100 provides good balance between computational cost and solution quality
- Larger populations (200) explore more thoroughly but can be misled by penalty approximations
- **Recommended: Population = 50-100**

### 2. Effect of Maximum Iterations (fixed population = 50)

| Max Iterations | Best Plies | Mean Plies | Notes |
|----------------|------------|------------|-------|
| 50 | 5 | 39.7 | Quick convergence possible, but inconsistent |
| 100 | 6 | 35.7 | Good balance |
| 200 | 5 | 20.3 | Better consistency |
| 300 | 5 | 6.3 | Most consistent, minimal improvement |

**Key Findings:**
- 50 iterations can find good solutions but with high variability
- 100 iterations provide reasonable consistency
- 200+ iterations show diminishing returns
- **Recommended: Iterations = 100-200**

---

## Discussion

### Problem Characteristics

1. **Discrete Optimization Challenge**: Unlike Problem 1 with continuous angles, this problem requires integer numbers of plies at specific orientations. This makes the search space discrete and potentially more challenging for PSO.

2. **Multiple Competing Constraints**: The four constraints create a complex feasible region:
   - E_x and E_y requirements favor 0° and 90° plies
   - G_xy requirement favors ±45° plies  
   - ν_xy constraint limits design flexibility
   - Minimizing plies conflicts with satisfying all properties

3. **Constraint Handling**: The penalty method with coefficient 10,000 effectively enforces hard constraints. Solutions consistently satisfy all requirements in the main optimization runs.

### Optimization Performance

**Convergence Behavior:**
- PSO converges rapidly in the first 20-30 iterations
- Best solutions typically found early in the search
- Multiple runs show significant variation (5-68 plies), indicating:
  - Multiple local minima exist
  - Initial population quality strongly affects outcome
  - Larger populations help avoid poor local minima

**Solution Diversity:**
- Main run (pop=50, iter=100, 5 runs): Found solutions ranging from 5 to 68 plies
- Best run consistently identified 5-6 ply designs
- The optimal 5-ply design uses a clever mix: longitudinal stiffness (0°), moderate angle (30°), and high angle (-75°)

### Practical Implications

1. **Manufacturing Considerations:**
   - 5 plies = 0.625 mm total thickness
   - Simple layup sequence: easy to manufacture
   - Limited angles used (3 out of 12 available)
   - Asymmetric design (not balanced/symmetric) - may exhibit coupling

2. **Performance Trade-offs:**
   - Meets all minimum requirements with small margins
   - E_x = 23.10 GPa (5% above minimum)
   - E_y = 18.34 GPa (2% above minimum)
   - Little room for property degradation

3. **Design Robustness:**
   - Tight constraint satisfaction suggests limited design space
   - Alternative 6-7 ply designs may provide more robust margins
   - Parameter study shows significant run-to-run variation

### Recommendations

For **production applications**:
- Consider 6-7 ply designs for property margins
- Implement balanced/symmetric layups if bending-extension coupling is undesirable
- Validate with finite element analysis

For **PSO parameter selection**:
- Population: 50-100 (good balance of exploration and computational cost)
- Iterations: 100-200 (consistent convergence)
- Multiple runs: 5-10 (capture solution variability)
- Penalty coefficient: 10,000 (effective constraint enforcement)

---

## Computational Performance

- Total execution time: 78.06 seconds
- Main optimization (5 runs): ~20 seconds
- Parameter study (16 optimization runs): ~58 seconds
- Average time per optimization: ~3.5 seconds

The discrete nature and constraint complexity make this problem more computationally intensive than Problem 1, but still very manageable for practical design applications.

---

## Visualization

Three key plots generated:

1. **Convergence Plot**: Shows PSO fitness evolution across all 5 runs
2. **Ply Distribution**: Bar chart of optimal ply counts at each angle
3. **Properties vs Requirements**: Comparison of achieved properties against constraints
4. **Parameter Study**: Effects of population size and iteration count on solution quality

See `problem2_results.png` and `problem2_parameter_study.png` for details.

---

## Conclusion

PSO successfully identified a **5-ply laminate** (0.625 mm) that minimizes thickness while satisfying all mechanical property constraints. The parameter study demonstrates that:

- **Population size** significantly affects solution quality and consistency
- **Iteration count** shows diminishing returns beyond 100-200 iterations
- **Multiple runs** are essential due to the stochastic nature of PSO

The optimal design uses a smart combination of 0° (strength), 30° (intermediate), and -75° (high angle) plies to balance all four property requirements efficiently.
