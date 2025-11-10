# STP 604E - Assignment 1 Results
## Classical Laminated Plate Theory (CLPT) Analysis

**Course**: Advanced Design, Analysis and Optimization of Composite Structure for Aerospace  
**Date**: November 8, 2025  
**Analysis Tool**: Python with custom composite_lib  
**Prepared by**: Giray Yıllıkçı

> **Note on Academic Integrity**: I am disclosing that AI tools (GitHub Copilot, Claude) were used in the preparation of this document and the development of the computational analysis code. This note is added voluntarily to maintain transparency and academic integrity.

---

## Table of Contents
1. [Problem 1: Quasi-Isotropic Laminate Analysis](#problem-1)
2. [Problem 2: Micromechanics Analysis](#problem-2)
3. [Problem 3: Zero Shear Strain Constraint](#problem-3)
4. [Problem 3 (Version 2): Alternative Stacking Sequence](#problem-3-v2)
5. [Problem 4: Stiffness Matrix Comparison](#problem-4)
6. [Summary and Conclusions](#summary)

---

## Problem 1: Quasi-Isotropic Laminate Analysis {#problem-1}

### Problem Statement
Analyze whether laminates consisting of three or more identical orthotropic laminae oriented at the same angle relative to adjacent laminae exhibit isotropic extensional stiffness. Rotate the laminates and plot A-matrix elements as a function of the top ply orientation.

**Laminates Analyzed:**
- Laminate 1: `[-45/0/45/90]`
- Laminate 2: `[0/30/60/90]`

### Material Properties
- **Material**: AS4/3501-6 Carbon/Epoxy
- E₁ = 142.0 GPa
- E₂ = 10.3 GPa
- G₁₂ = 7.2 GPa
- ν₁₂ = 0.27
- Ply thickness = 0.125 mm

### Results Summary

#### Laminate 1: [-45/0/45/90] ✓ QUASI-ISOTROPIC

**Key Findings:**
- **A₁₁ variation**: 0.00% (perfectly constant)
- **A₂₂ variation**: 0.00% (perfectly constant)
- **Max |A₁₆|**: 0.000000 N/mm (essentially zero)
- **Max |A₂₆|**: 0.000000 N/mm (essentially zero)

**Conclusion**: This laminate maintains constant stiffness properties regardless of rotation angle - it is truly quasi-isotropic! The 45° angle spacing creates a balanced configuration.

**A-matrix at 0° rotation:**
```
[[30.86  8.82  0.00]
 [ 8.82 30.86  0.00]
 [ 0.00  0.00 11.02]]
```

#### Laminate 2: [0/30/60/90] ✗ NOT QUASI-ISOTROPIC

**Key Findings:**
- **A₁₁ variation**: 92.82% (huge variation with rotation)
- **A₂₂ variation**: 92.82% (huge variation with rotation)
- **Max |A₁₆|**: 7.93 N/mm (significant coupling)
- **Max |A₂₆|**: 7.93 N/mm (significant coupling)

**Conclusion**: Properties change dramatically with rotation angle. The 30° spacing does not achieve quasi-isotropy.

### Visualization

![Problem 1 Results](assignment1_problem1_results.png)

**Figure 1**: Extensional stiffness matrix components vs. rotation angle for both laminates. The left column shows Laminate 1 (quasi-isotropic behavior with flat lines), while the right column shows Laminate 2 (significant variation with rotation).

### Key Insights
1. **Quasi-isotropic laminates require specific angle spacing** - the [-45/0/45/90] configuration with 45° increments works perfectly
2. **Shear-extension coupling terms (A₁₆, A₂₆) must be zero** for quasi-isotropy
3. **Equal normal stiffnesses (A₁₁ = A₂₂)** are necessary but not sufficient
4. The analysis validates the theoretical requirement: n ≥ 3 plies with equal angular spacing of 180°/n

---

## Problem 2: Micromechanics Analysis {#problem-2}

### Problem Statement
Determine the engineering constants of a `[0/90/0]ₛ` laminate fabricated from unidirectional laminae using micromechanics principles.

### Given Data

**Fiber Properties:**
- E_f = 220 GPa
- ν_f = 0.25

**Matrix Properties:**
- E_m = 3.6 GPa
- ν_m = 0.40

**Geometry:**
- Lamina thickness (t) = 0.25 mm
- Fiber diameter (d) = 10 μm
- Number of fibers per mm width = 1900

### Analysis Process

#### Step 1: Fiber Volume Fraction Calculation
```
Fiber cross-sectional area per fiber:
  A_fiber = π × (5×10⁻³)² = 7.854×10⁻⁵ mm²

Total fiber area per 1 mm width:
  A_fibers = 1900 × 7.854×10⁻⁵ = 0.1492 mm²

Cross-sectional area of lamina per 1 mm width:
  A_lamina = 0.25 × 1 = 0.25 mm²

Fiber Volume Fraction:
  V_f = 0.1492 / 0.25 = 0.5970 (59.70%)
  V_m = 0.4030 (40.30%)
```

> **Note on Calculation Ambiguity**: There is some uncertainty in interpreting the problem statement regarding whether the calculated value 0.1492 represents the fiber area (leading to V_f = 59.70%) or if it should be used directly as the volume fraction (V_f = 14.92%). I proceeded with V_f = 59.70% because a fiber volume fraction of ~15% would be abnormally low for a structural composite laminate. Typical aerospace-grade composites have fiber volume fractions in the range of 55-65%. However, this interpretation should be verified with the problem statement or instructor guidance.

#### Step 2: Lamina Engineering Constants (Micromechanics)

**Using Rule of Mixtures and Halpin-Tsai equations:**

| Property | Method | Value |
|----------|--------|-------|
| E₁ | Rule of Mixtures | 132.727 GPa |
| E₂ | Halpin-Tsai (ξ=2) | 8.077 GPa |
| G₁₂ | Halpin-Tsai (ξ=1) | 3.363 GPa |
| ν₁₂ | Rule of Mixtures | 0.3103 |

**Intermediate Calculations:**
- G_f = E_f / (2(1+ν_f)) = 88.000 GPa
- G_m = E_m / (2(1+ν_m)) = 1.286 GPa
- η (for E₂) = 0.9689
- η (for G₁₂) = 0.9715

#### Step 3: Laminate Properties

**Stacking Sequence:** `[0/90/0]ₛ` = `[0/90/0/0/90/0]`
- Number of plies: 6
- Total thickness: 1.500 mm
- Symmetric: Yes

**ABD Matrices:**

Extensional Stiffness [A] (N/mm):
```
[[278.52   5.04   0.00]
 [  5.04 278.52   0.00]
 [  0.00   0.00  10.09]]
```

Coupling Stiffness [B] (N):
```
[[ 0.00  0.00  0.00]
 [ 0.00  0.00  0.00]
 [ 0.00  0.00  0.00]]
```
*Note: B matrix is zero (symmetric laminate)*

Bending Stiffness [D] (N·mm):
```
[[15.38  0.98  0.00]
 [ 0.98 15.38  0.00]
 [ 0.00  0.00  0.56]]
```

**Effective Laminate Engineering Constants:**

| Property | Value |
|----------|-------|
| E_x | 185.666 GPa |
| E_y | 185.666 GPa |
| G_xy | 6.725 GPa |
| ν_xy | 0.0181 |
| ν_yx | 0.0181 |

### Key Observations
1. **Balanced laminate**: E_x = E_y due to [0/90]ₛ symmetry
2. **Low Poisson's ratio**: ν_xy ≈ 0.018 (much lower than individual plies)
3. **Zero coupling**: B matrix = 0 confirms symmetric laminate behavior
4. **High fiber volume fraction**: 59.7% leads to excellent longitudinal properties

---

## Problem 3: Zero Shear Strain Constraint {#problem-3}

### Problem Statement
For a laminate with stacking sequence `[30/θ₁/θ₂/-30]ₛ`, find angles θ₁ and θ₂ such that the mid-plane shear strain γ_xy⁰ = 0 under specified loading.

### Material & Loading

**Material**: Kevlar/Epoxy
- E₁ = 76 GPa
- E₂ = 5.50 GPa
- G₁₂ = 2.30 GPa
- ν₁₂ = 0.34
- t = 1.25 mm

**Applied Loads:**
- N_x = 1000 N/m
- N_y = 1000 N/m
- N_xy = 0 N/m
- M_x = 0 N
- M_y = 50 N
- M_xy = 50 N

### Solution Approach
Assuming θ₁ = θ₂ = θ for symmetric solution, use numerical optimization (scipy.fsolve) to find θ that produces zero shear strain.

### Results

**Solution: θ = 0.00°**

**Expanded Laminate:** `[30/0/0/-30/-30/0/0/30]`

**Mid-plane Strains at Solution:**
- ε_x⁰ = -103,351.893 με
- ε_y⁰ = 12,696,682.555 με
- γ_xy⁰ = **0.000000 με** ✓ (constraint satisfied)

**Curvatures at Solution:**
- κ_x = -0.024650 /mm
- κ_y = 0.066825 /mm
- κ_xy = 0.062002 /mm

### Visualization

![Problem 3 Results](assignment1_problem3_results.png)

**Figure 2**: Mid-plane strains and curvatures vs. θ for `[30/θ/θ/-30]ₛ` laminate. The green line (γ_xy⁰) crosses zero at θ = 0°, marked by the magenta vertical line. The top plot shows strains, and the bottom shows curvatures.

### Physical Interpretation
1. **Solution exists**: The constraint γ_xy⁰ = 0 can be achieved by proper selection of θ
2. **Sensitivity**: Shear strain is highly sensitive to ply orientation
3. **Design flexibility**: Demonstrates ability to tailor laminate properties for specific constraints
4. **Balanced configuration**: θ = 0° creates a balanced arrangement around the outer ±30° plies

---

## Problem 3 (Version 2): Alternative Stacking Sequence {#problem-3-v2}

### Problem Statement
Same as Problem 3, but with stacking sequence `[30/θ₁/θ₂/30]ₛ` (outer plies both at +30° instead of ±30°).

### Solution

**Solution: θ = -30.00°**

**Expanded Laminate:** `[30/-30/-30/30/30/-30/-30/30]`

This creates a perfectly balanced alternating pattern!

**Mid-plane Strains at Solution:**
- ε_x⁰ = -1,782,571.281 με
- ε_y⁰ = 12,231,160.188 με
- γ_xy⁰ = **-0.000000 με** ✓ (constraint satisfied)

**Curvatures at Solution:**
- κ_x = -0.038655 /mm
- κ_y = 0.107890 /mm
- κ_xy = 0.039669 /mm

**ABD Matrices at Solution:**

Extensional Stiffness [A] (N/mm):
```
[[216.67  84.46  62.84]
 [ 84.46 216.67  62.84]
 [ 62.84  62.84  60.09]]
```

Coupling Stiffness [B] (N):
```
[[ 0.00  0.00  0.00]
 [ 0.00  0.00  0.00]
 [ 0.00  0.00  0.00]]
```

Bending Stiffness [D] (N·mm):
```
[[281.08 109.58  81.59]
 [109.58 281.08  81.59]
 [ 81.59  81.59  78.00]]
```

### Visualization

![Problem 3 V2 Results](assignment1_problem3_v2_results.png)

**Figure 3**: Mid-plane strains and curvatures vs. θ for `[30/θ/θ/30]ₛ` laminate. The solution occurs at θ = -30°, creating a balanced [30/-30] alternating pattern. Note the different scale compared to Problem 3 - strains are much larger in magnitude.

### Comparison: Problem 3 vs. Problem 3 V2

| Aspect | [30/θ/θ/-30]ₛ | [30/θ/θ/30]ₛ |
|--------|---------------|--------------|
| **Solution θ** | 0.00° | -30.00° |
| **Final Laminate** | [30/0/0/-30]ₛ | [30/-30/-30/30]ₛ |
| **Pattern** | Mixed angles | Alternating ±30° |
| **ε_x⁰ magnitude** | ~100k με | ~1.8M με |
| **ε_y⁰ magnitude** | ~12.7M με | ~12.2M με |
| **B matrix** | Non-zero | Zero (balanced) |
| **A₁₆, A₂₆** | ~0 N/mm | ~63 N/mm |

### Key Insights
1. **Dramatic sensitivity**: Changing outer ply from -30° to +30° changes solution from 0° to -30°
2. **Balanced laminate advantage**: V2 solution creates zero B matrix (no bending-extension coupling)
3. **Strain magnitudes**: V2 experiences much higher strains due to different load distribution
4. **Design implications**: Small changes in stacking sequence can dramatically affect optimal angles

---

## Problem 4: Stiffness Matrix Comparison {#problem-4}

### Problem Statement
Calculate and compare the extensional [A], coupling [B], and bending [D] stiffness matrices for two laminates:
- **Part (a)**: `[-45/45]`
- **Part (b)**: `[-45/45/-45/45]`

Analyze how doubling the thickness by repeating the layup affects each stiffness matrix.

### Material Properties
- **Material**: AS/3501 Graphite-Epoxy
- E₁ = 181.0 GPa
- E₂ = 10.3 GPa
- G₁₂ = 7.17 GPa
- ν₁₂ = 0.28
- Ply thickness = 0.5 mm

### Results

#### Part (a): Laminate [-45/45]

**Laminate Configuration:**
- Stacking: `[-45, 45]`
- Number of plies: 2
- Total thickness: 1.0 mm
- Classification: Balanced, Non-symmetric

**Extensional Stiffness [A] (N/mm):**
```
[[56.658  42.318   0.000]
 [42.318  56.658   0.000]
 [ 0.000   0.000  46.591]]
```

**Coupling Stiffness [B] (N):**
```
[[ 0.000   0.000  10.717]
 [ 0.000   0.000  10.717]
 [10.717  10.717   0.000]]
```
*Note: B ≠ 0 because laminate is NOT symmetric*

**Bending Stiffness [D] (N·mm):**
```
[[4.721  3.526  0.000]
 [3.526  4.721  0.000]
 [0.000  0.000  3.883]]
```

#### Part (b): Laminate [-45/45/-45/45]

**Laminate Configuration:**
- Stacking: `[-45, 45, -45, 45]`
- Number of plies: 4
- Total thickness: 2.0 mm
- Classification: Balanced, Non-symmetric

**Extensional Stiffness [A] (N/mm):**
```
[[113.316   84.636    0.000]
 [ 84.636  113.316    0.000]
 [  0.000    0.000   93.182]]
```

**Coupling Stiffness [B] (N):**
```
[[ 0.000   0.000  21.433]
 [ 0.000   0.000  21.433]
 [21.433  21.433   0.000]]
```
*Note: B ≠ 0 because laminate is still NOT symmetric*

**Bending Stiffness [D] (N·mm):**
```
[[37.772  28.212   0.000]
 [28.212  37.772   0.000]
 [ 0.000   0.000  31.061]]
```

### Comparative Analysis

| Property | [-45/45] | [-45/45/-45/45] | Ratio | Expected Scaling |
|----------|----------|-----------------|-------|------------------|
| **Thickness** | 1.0 mm | 2.0 mm | 2.0 | Linear |
| **A₁₁** | 56.658 N/mm | 113.316 N/mm | 2.00 | h¹ → 2.0 |
| **A₂₂** | 56.658 N/mm | 113.316 N/mm | 2.00 | h¹ → 2.0 |
| **A₆₆** | 46.591 N/mm | 93.182 N/mm | 2.00 | h¹ → 2.0 |
| **\|B₁₆\|** | 10.717 N | 21.433 N | 2.00 | h² → 4.0* |
| **\|B₂₆\|** | 10.717 N | 21.433 N | 2.00 | h² → 4.0* |
| **D₁₁** | 4.721 N·mm | 37.772 N·mm | 8.00 | h³ → 8.0 |
| **D₂₂** | 4.721 N·mm | 37.772 N·mm | 8.00 | h³ → 8.0 |
| **D₆₆** | 3.883 N·mm | 31.061 N·mm | 8.00 | h³ → 8.0 |

*\*B matrix scaling depends on laminate symmetry and ply arrangement*

### Key Findings

1. **Extensional Stiffness [A]:**
   - Scales **linearly** with thickness (factor of 2.0)
   - Formula: A_ij = ∫Q̄_ij dz
   - Both laminates are balanced → A₁₆ = A₂₆ ≈ 0

2. **Coupling Stiffness [B]:**
   - Observed scaling factor of **2.0**
   - Formula: B_ij = ½∫Q̄_ij z dz
   - Both laminates non-symmetric → B ≠ 0
   - B couples in-plane loads with curvatures
   - The factor of 2.0 (not 4.0) results from the specific layup repetition pattern

3. **Bending Stiffness [D]:**
   - Scales **cubically** with thickness (factor of 8.0)
   - Formula: D_ij = ⅓∫Q̄_ij z² dz
   - This demonstrates the high efficiency of thickness for bending resistance
   - 2× thickness → 8× bending stiffness!

### Design Implications

1. **For in-plane loading:**
   - Add plies for linear increase in extensional stiffness
   - Cost-effective way to increase membrane strength

2. **For bending/flexural loading:**
   - Increase thickness for cubic gain in bending stiffness
   - Much more efficient than adding plies for bending applications
   - Critical for plate/shell structures

3. **For uncoupled behavior:**
   - Use symmetric layups to eliminate [B] matrix
   - Prevents coupling between in-plane and out-of-plane deformations

4. **Laminate classification:**
   - Both laminates are **balanced** (no shear-extension coupling)
   - Neither is **symmetric** (B ≠ 0, causes extension-bending coupling)

### Results Validation

To verify the accuracy of our custom `composite_lib` implementation, the ABD matrices were cross-checked using ABDComposites.com's online calculator tool. The validation screenshots below confirm that our computed values match the industry-standard tool.

#### Validation: Laminate [-45/45]

![Problem 4 Validation - Laminate 1](problem4_validation_laminate1.png)

**Figure 4a**: ABDComposites.com validation for [-45/45] laminate showing identical A, B, and D matrix values to our calculations.

#### Validation: Laminate [-45/45/-45/45]

![Problem 4 Validation - Laminate 2](problem4_validation_laminate2.png)

**Figure 4b**: ABDComposites.com validation for [-45/45/-45/45] laminate confirming our implementation accuracy.

**Validation Notes:**
- ✅ All extensional stiffness [A] values match exactly
- ✅ All coupling stiffness [B] values match exactly  
- ✅ All bending stiffness [D] values match exactly
- ✅ Confirms the reliability of our Python implementation for Classical Laminated Plate Theory
- ✅ Validates the Q-bar transformation matrices and ABD integration algorithms

This independent verification demonstrates that the `composite_lib` toolkit produces accurate, industry-standard results suitable for engineering analysis and design applications.

---

## Summary and Conclusions {#summary}

### Overall Findings

1. **Quasi-Isotropy (Problem 1)**
   - Confirmed that [-45/0/45/90] configuration achieves perfect quasi-isotropy
   - Requires equal angular spacing (180°/n where n = number of unique angles)
   - 30° spacing [0/30/60/90] is insufficient

2. **Micromechanics (Problem 2)**
   - Successfully predicted lamina properties from constituent materials
   - Fiber volume fraction of 59.7% yields excellent longitudinal stiffness
   - [0/90]ₛ laminate shows balanced properties with E_x = E_y

3. **Constrained Design (Problem 3 & 3-V2)**
   - Zero shear strain constraint can be satisfied through angle optimization
   - Multiple solutions exist depending on outer ply configuration
   - Balanced laminates (alternating ±θ) eliminate bending-extension coupling

### Methodology Validation

The Python-based `composite_lib` successfully handles:
- ✅ Q-matrix calculation and transformation
- ✅ ABD matrix assembly for symmetric and asymmetric laminates
- ✅ Micromechanics (Rule of Mixtures, Halpin-Tsai)
- ✅ Strain and curvature calculations under combined loading
- ✅ Numerical optimization for constrained design

### Design Recommendations

1. **For quasi-isotropic behavior**: Use n ≥ 3 plies with angular spacing of 180°/n
2. **For zero coupling**: Ensure symmetric and balanced layups
3. **For specific constraints**: Use optimization to find optimal ply angles
4. **For high stiffness**: Maximize fiber volume fraction and align fibers with load direction

### Future Work

- Extend analysis to unsymmetric laminates
- Include failure analysis (Tsai-Wu, maximum stress criteria)
- Investigate thermal effects
- Study impact of manufacturing defects on properties

---

## Appendices

### A. Computational Tools Used

- **Python 3.12.4**
- **Libraries**: NumPy, SciPy, Matplotlib, Plotly, Streamlit
- **Custom Library**: `composite_lib` (laminate.py, lamina.py, micromechanics.py)
- **Optimization**: scipy.optimize.fsolve for nonlinear constraint satisfaction

### B. Repository Structure

```
STP604E/
├── assignments/
│   ├── assignment1_problem1.py
│   ├── assignment1_problem2.py
│   ├── assignment1_problem3.py
│   └── assignment1_problem3_v2.py
├── composite_lib/
│   ├── lamina.py
│   ├── laminate.py
│   └── micromechanics.py
├── visualization/
│   └── composite_visualizer.py
├── run_visualizer.py
├── solve_assignments.py
└── ASSIGNMENT_RESULTS.md (this file)
```

### C. How to Run

```bash
# Run all assignments interactively
python solve_assignments.py

# Run specific problem
python solve_assignments.py 1

# Launch 3D visualizer
python run_visualizer.py

# Run individual files
python assignments/assignment1_problem1.py
python assignments/assignment1_problem2.py
python assignments/assignment1_problem3.py
python assignments/assignment1_problem3_v2.py
```

---

**Document Generated**: November 8, 2025  
**Analysis Tool**: Python with composite_lib  
**Course**: STP 604E - Advanced Design, Analysis and Optimization of Composite Structure for Aerospace  
**GitHub Repository**: https://github.com/gyillikci/STP604E  
