# STP604E Assignment 2 - Complete Solution Summary

**Course**: STP604E - Mechanics of Composite Materials  
**Term**: Fall 2025  
**Date**: December 16, 2025

---

## Executive Summary

This assignment explores advanced optimization techniques for composite laminate design using **Particle Swarm Optimization (PSO)** and **Miki's Lamination Parameters**. Four problems demonstrate different design objectives and constraints:

| Problem | Objective | Method | Result |
|---------|-----------|--------|--------|
| **1** | Minimize thermal expansion αₓ | PSO (continuous angles) | θ₁=8°, θ₂=61°, \|αₓ\|=0.428×10⁻⁶/°C |
| **2** | Minimize thickness | PSO (discrete angles) | 5 plies (0.625 mm) |
| **3** | Maximize Ey | Lamination parameters | Ey = 58.59 GPa |
| **4** | Derive D_MN formula | Analytical derivation | Complete proof |

---

## Problem 1: Thermal Expansion Optimization

### Problem Statement
Design a balanced symmetric laminate **[±θ₁/±30°/±θ₂]ₛ** to minimize longitudinal thermal expansion coefficient |αₓ| with constraint θ₂ > 60°.

**Material**: Graphite/Epoxy
- E₁ = 138 GPa, E₂ = 8.96 GPa, G₁₂ = 7.10 GPa, ν₁₂ = 0.30
- α₁ = -0.3×10⁻⁶/°C, α₂ = 28.1×10⁻⁶/°C
- t = 0.125 mm/ply

### Solution
**PSO Optimization Results:**
- **Optimal angles**: θ₁ = 8° (or -8°), θ₂ = 61°
- **Stacking sequence**: [8/-8/30/-30/61/-61/-61/61/-30/30/-8/8]
- **Thermal expansion**: αₓ = 0.4284×10⁻⁶/°C (99.98% reduction)
- **Consistency**: 100% success rate across 10 independent runs

**Elastic Properties:**
- Ex = 71.6 GPa
- Ey = 35.3 GPa
- Gxy = 21.8 GPa
- νxy = 0.4448

**Key Innovation**: Custom `ThermalLaminate` class implementing Classical Lamination Theory with thermal effects.

### Files
- `problem1_thermal_cte.py` (485 lines)
- `problem1_convergence.png` - PSO convergence curves
- `problem1_cte_variation.png` - 3D surface plots of CTE vs angles

---

## Problem 2: Minimum Thickness Laminate

### Problem Statement
Design laminate with **minimum number of plies** using discrete angles (0°, ±15°, ±30°, ±45°, ±60°, ±75°, 90°) subject to:
- 0.2 ≤ νxy ≤ 0.7
- Gxy ≥ 5 GPa
- Ex ≥ 22 GPa
- Ey ≥ 18 GPa

**Material**: Different from Problem 1
- E₁ = 38.6 GPa, E₂ = 8.27 GPa, G₁₂ = 4.14 GPa, ν₁₂ = 0.28
- t = 0.125 mm/ply

### Solution
**Optimal Design: 5 plies (0.625 mm)**
- **Ply distribution**: 2×0°, 1×30°, 2×(-75°)
- **Properties**:
  - Ex = 23.10 GPa ✓
  - Ey = 18.34 GPa ✓
  - Gxy = 5.45 GPa ✓
  - νxy = 0.235 ✓

**Parameter Study Results:**
- **Population size**: 50-100 recommended (balance exploration vs. cost)
- **Iterations**: 100-200 optimal (diminishing returns after)
- Smaller populations (20) give inconsistent results
- Larger populations (200) can find infeasible solutions with low penalties

**Computational Performance**: 78 seconds (including full parameter study)

### Files
- `problem2_minimum_thickness.py` (700+ lines)
- `problem2_results.png` - Convergence, ply distribution, property comparison
- `problem2_parameter_study.png` - Population & iteration effects
- `PROBLEM2_RESULTS.md` - Comprehensive analysis

---

## Problem 3: Miki's Lamination Parameters

### Problem Statement
Design **16-layer balanced symmetric laminate** to **maximize Ey** subject to:
- Ex ≥ 70 GPa
- Gxy ≥ 15 GPa
- νxy < 0.4

**Three Cases:**
- **(a)** Continuous fiber orientations (2-angle and 3-angle)
- **(b)** Discrete: 0°, ±45°, 90°
- **(c)** Discrete: 0°, ±30°, ±60°, 90°

**Material**: Same as Problem 1 (Graphite/Epoxy)

### Solution Summary

| Case | Configuration | **Ey (GPa)** | Ex (GPa) | Gxy (GPa) | νxy |
|------|---------------|--------------|----------|-----------|-----|
| **(a)** Continuous 2-angle | [±10.3°/±69.5°]₂ₛ | **58.59** | 70.00 | 15.00 | 0.176 |
| **(b)** 0°,±45°,90° | [0₄/45₃/90]ₛ | **36.84** | 82.95 | 17.79 | 0.344 |
| **(c)** 0°,±30°,±60°,90° | [0₄/60₃/90]ₛ | **52.25** | 75.92 | 15.12 | 0.200 |

### Key Findings

🏆 **Best Performance**: Continuous angles achieve Ey = 58.59 GPa (59% higher than standard 0/±45/90)

**Lamination Parameters** (Case a):
- V₁ = 0.0903
- V₃ = 0.4457
- V₂ = V₄ = 0 (balanced constraint)

**Design Space Comparison:**
- Case (a): Infinite design space → optimal solution
- Case (b): Only 28 feasible configurations (0.4% of 6,769 tested)
- Case (c): 730 feasible configurations (7.3% of 10,000 tested)

**Performance vs. Manufacturability Trade-off:**
- Continuous angles: 100% performance, requires AFP (Automated Fiber Placement)
- Case (c): 89% performance, standard tape-laying equipment
- Case (b): 63% performance, industry-standard angles

**Computational Performance**: 2.73 seconds total

### Files
- `problem3_miki_lamination.py` (550+ lines)
- `problem3_continuous_results.png` - Feasible region in V₁-V₃ space
- `problem3_comparison.png` - Bar charts comparing all three cases
- `PROBLEM3_RESULTS.md` - Detailed analysis with theory

---

## Problem 4: Mathematical Derivation

### Problem Statement
Derive the formula for bending stiffness of a laminate composed of two sublaminates M and N:

$$D_{MN} = D_M + D_N + \frac{t_N^2}{4}A_M + \frac{t_M^2}{4}A_N - t_N B_M + t_M B_N$$

### Solution Approach

**Step-by-step derivation:**
1. Define coordinate systems (global and local for M and N)
2. Establish coordinate transformations
3. Express D_MN using CLT definitions
4. Transform D_M to global coordinates using binomial expansion
5. Transform D_N to global coordinates
6. Combine results

**Key Mathematical Tool**: Binomial expansion of $(z \pm d)^3$ combined with parallel axis theorem

**Physical Interpretation:**
- **$D_M + D_N$**: Direct bending stiffnesses
- **$\frac{t^2}{4}A$ terms**: Parallel axis theorem (extensional → bending)
- **$tB$ terms**: Coupling corrections due to coordinate shift

### Files
- `PROBLEM4_DERIVATION.md` - Complete mathematical proof with examples

---

## Methodology Summary

### Particle Swarm Optimization (PSO)

**Algorithm Parameters Used:**
- Inertia weight: w = 0.9 → 0.4 (linear decay)
- Acceleration coefficients: c₁ = c₂ = 2.0
- Constriction factor: χ = 0.73
- Population sizes: 50-200 (problem-dependent)
- Iterations: 100-300 (problem-dependent)

**Constraint Handling**: Penalty method with coefficients 10,000-10¹⁰

**Performance Characteristics:**
- Fast convergence (typically 50-100 iterations)
- Good global search capability
- Multiple runs recommended for consistency

### Lamination Parameters Approach

**Advantages:**
- Reduces design space dimensionality (n plies → 4 parameters)
- Separates material from geometry
- Enables direct property calculation
- Feasibility constraints well-defined

**Implementation:**
- Tsai-Pagano invariants U₁-U₅
- Feasible region: |V₃| ≤ 1 - 2|V₁|
- Balanced constraint: V₂ = V₄ = 0

---

## Computational Summary

| Problem | Runtime | Key Metric |
|---------|---------|------------|
| Problem 1 | 23.1 sec | 10 PSO runs × 100 iterations |
| Problem 2 | 78.1 sec | 5 main + 16 parameter study runs |
| Problem 3 | 2.7 sec | 1 PSO run + 2 enumerations |
| **Total** | **103.9 sec** | Highly efficient |

**Environment:**
- Python 3.12.4
- NumPy 1.x
- Matplotlib 3.x
- Custom composite mechanics implementations

---

## Key Insights and Lessons Learned

### 1. **Problem Formulation Matters**
- Problem 1: Continuous angles → PSO excels
- Problem 2: Discrete plies → PSO with rounding
- Problem 3: Lamination parameters → reduced dimensionality

### 2. **Constraint Activity Indicates Optimality**
- Problem 1: Constraint θ₂ > 60° active at 61°
- Problem 3: Both Ex and Gxy at exact minimums (70 and 15 GPa)
- Active constraints = Pareto-optimal design

### 3. **Manufacturing Constraints Are Expensive**
- Restricting to 0°/±45°/90° costs 37% performance (Problem 3b)
- Adding ±30°/±60° recovers to 89% performance (Problem 3c)
- Value of manufacturing flexibility quantified

### 4. **PSO Tuning Guidelines**
- Population: 50-100 for 2-5 variables
- Iterations: 100-200 sufficient for most problems
- Multiple runs essential (5-10) due to stochastic nature
- Penalty coefficients: 10,000 for property constraints

### 5. **Thermal Design Challenges**
- Achieving |αx| ≈ 0 is possible but requires specific angles
- CTE is highly sensitive to ply angles
- Balanced/symmetric helps but doesn't eliminate thermal expansion

---

## Academic Integrity Note

⚠️ **Important**: These solutions are provided for educational purposes. Students must:
1. Understand the underlying theory and derivations
2. Be able to reproduce results independently
3. Explain physical meaning of solutions
4. Not submit these solutions as their own work

The value lies in **understanding the methodology**, not copying the code.

---

## Code Structure

```
assignment_2/
├── problem1_thermal_cte.py          # Problem 1: Thermal optimization
├── problem1_convergence.png          # Results visualization
├── problem1_cte_variation.png        # 3D CTE surfaces
│
├── problem2_minimum_thickness.py     # Problem 2: Minimum thickness
├── problem2_results.png              # Main results
├── problem2_parameter_study.png      # PSO parameter effects
├── PROBLEM2_RESULTS.md               # Detailed analysis
│
├── problem3_miki_lamination.py       # Problem 3: Lamination parameters
├── problem3_continuous_results.png   # Feasible region & convergence
├── problem3_comparison.png           # Case comparison
├── PROBLEM3_RESULTS.md               # Theory & analysis
│
├── PROBLEM4_DERIVATION.md            # Problem 4: Mathematical proof
│
└── ASSIGNMENT2_COMPLETE_SUMMARY.md   # This file
```

---

## Extension Ideas

### For Further Study:

1. **Problem 1**: Study effect of different fixed angle (currently 30°)
2. **Problem 2**: Multi-objective: minimize thickness AND maximize Ey
3. **Problem 3**: Include manufacturing constraints (max ply drops, angle restrictions)
4. **Problem 4**: Extend to sandwich structures with core
5. **General**: Compare PSO with Genetic Algorithms, Simulated Annealing

### Research Directions:

- **Robustness**: Account for manufacturing tolerances
- **Damage**: Include progressive failure analysis
- **Dynamics**: Add frequency constraints
- **Cost**: Multi-objective with manufacturing cost
- **Uncertainty**: Probabilistic design optimization

---

## References

### Theory
1. Jones, R.M., *Mechanics of Composite Materials*, 2nd ed., 1999
2. Hyer, M.W., *Stress Analysis of Fiber-Reinforced Composite Materials*, 2009
3. Tsai, S.W., *Composites Design*, 4th ed., 1988

### Optimization
4. Kennedy, J., Eberhart, R., "Particle Swarm Optimization," IEEE, 1995
5. Miki, M., "Design of Laminated Fibrous Composite Plates," JSME, 1982
6. Fukunaga, H., Vanderplaats, G.N., "Strength Optimization," AIAA, 1991

### Software
7. Python NumPy Documentation: https://numpy.org/doc/
8. Matplotlib Documentation: https://matplotlib.org/

---

## Conclusion

This assignment demonstrates the power of **computational optimization** in composite materials design. Key takeaways:

✅ PSO is highly effective for continuous and discrete laminate optimization  
✅ Lamination parameters elegantly reduce design space complexity  
✅ Manufacturing constraints significantly impact achievable performance  
✅ Multiple optimization runs essential for confidence in stochastic algorithms  
✅ Active constraints at optimum indicate true optimal designs  

The combination of **Classical Lamination Theory** and **modern optimization algorithms** enables engineers to design composite structures that were impractical to analyze by hand, pushing the boundaries of performance while satisfying complex constraints.

---

**Total LOC**: ~1,900 lines of Python code  
**Total Documentation**: ~5,000 lines of Markdown  
**Plots Generated**: 7 publication-quality figures  
**Execution Time**: < 2 minutes total

*All code is reproducible and well-documented for educational use.*

---

## Contact & Attribution

**Course**: STP604E - Mechanics of Composite Materials  
**Institution**: Istanbul Technical University  
**Term**: Fall 2025  

*Solutions implemented using Python 3.12.4, NumPy, and Matplotlib.*  
*Repository: [Link to be added if shared]*

---

**End of Assignment 2 Summary**
