# Assignment 3: Composite Laminate Analysis

## Course: STP604E - Composite Materials

---

## Table of Contents
1. [Problem 1: Strength Envelope Analysis](#problem-1-strength-envelope-analysis)
2. [Problem 2: Stacking Sequence Determination](#problem-2-stacking-sequence-determination)
3. [Problem 3: Laminate Analysis under Combined Loading](#problem-3-laminate-analysis-under-combined-loading)
4. [Problem 4: Laminate Design Optimization](#problem-4-laminate-design-optimization)

---

## Problem 1: Strength Envelope Analysis

### Problem Statement
A Graphite/Epoxy laminate with [0/±45₂/90]s stacking sequence is loaded only by biaxial loads. Draw the strength envelope for the laminate in the σ̄x - σ̄y plane using the maximum strain criterion. Determine:
- (a) Maximum pure tensile load (Nx)
- (b) Maximum pure compressive load (Ny)

### Given Data

| Property | Value | Property | Value |
|----------|-------|----------|-------|
| E₁ | 138 GPa | Xt | 2280 MPa |
| E₂ | 8.69 GPa | Xc | 1725 MPa |
| G₁₂ | 7.10 GPa | Yt | 57 MPa |
| ν₁₂ | 0.3 | Yc | 228 MPa |
| t | 0.125 mm | S | 76 MPa |

### Solution Approach

1. **Laminate Configuration:**
   - Full layup: [0°, 45°, 45°, -45°, -45°, 90°, 90°, -45°, -45°, 45°, 45°, 0°]
   - Total thickness: h = 12 × 0.125 = 1.5 mm

2. **Maximum Strain Criterion Allowables:**
   | Strain Limit | Formula | Value |
   |--------------|---------|-------|
   | ε₁ᵗ (fiber tensile) | Xt/E₁ | 16,522 με |
   | ε₁ᶜ (fiber compressive) | Xc/E₁ | 12,500 με |
   | ε₂ᵗ (matrix tensile) | Yt/E₂ | 6,559 με |
   | ε₂ᶜ (matrix compressive) | Yc/E₂ | 26,237 με |
   | γ₁₂ᵐᵃˣ (shear) | S/G₁₂ | 10,704 με |

3. **Ā Matrix (Normalized Extensional Stiffness):**
   ```
   [54782.65  21602.25      0   ]
   [21602.25  54782.65      0   ] MPa
   [    0         0     26080.39]
   ```

### Results

#### (a) Maximum Pure Tensile Load (Nx)

| Parameter | Value |
|-----------|-------|
| **σ̄x,max** | **303.46 MPa** |
| **Nx,max** | **455.19 N/mm** |
| **Failure Type** | Matrix Tensile failure (ε₂ > ε₂ᵗ) in 90° ply |

**Explanation:** The 90° ply fails first because its fibers are perpendicular to the loading direction. The matrix carries the load in the transverse direction and reaches its tensile strain limit.

#### (b) Maximum Pure Compressive Load (Ny)

| Parameter | Value |
|-----------|-------|
| **σ̄y,max** | **-355.17 MPa** |
| **Ny,max** | **-532.76 N/mm** |
| **Failure Type** | Shear failure (|γ₁₂| > γ₁₂ᵐᵃˣ) in ±45° plies |

**Explanation:** The ±45° plies fail first in shear because the compressive y-direction load creates high shear strains in these off-axis plies.

### Strength Envelope

![Strength Envelope](strength_envelope.png)

The strength envelope shows the safe operating region in the σ̄x - σ̄y stress space. Key features:
- Symmetric about the 45° line (quasi-isotropic behavior)
- Tensile limits governed by matrix tensile failure
- Compressive limits governed by shear failure in ±45° plies

### Files
- `problem1_strength_envelope.py` - Analysis script
- `strength_envelope.png` - Strength envelope plot

---

## Problem 2: Stacking Sequence Determination

### Problem Statement
Determine the stacking sequence of a laminated composite plate from experimental test results:
- Uniaxial tensile test: No bending, no shear observed
- Three-point bending test: Only pure bending experienced
- Tensile elongation: 0.0897 mm at 2500 N load
- Bending slope: 0.0808 mm/N

Plate dimensions: 150 mm × 30 mm × 2 mm

### Given Data

| Property | Value |
|----------|-------|
| E₁ | 181 GPa |
| E₂ | 10.3 GPa |
| G₁₂ | 7.17 GPa |
| ν₁₂ | 0.28 |
| t (ply) | 0.25 mm |

### Solution Approach

1. **Interpret Experimental Observations:**
   - No bending under tension → **B = 0** → Symmetric laminate
   - No shear under tension → **A₁₆ = A₂₆ = 0** → Balanced laminate
   - Pure bending under moment → **D₁₆ = D₂₆ ≈ 0**

2. **Calculate Required Stiffnesses:**
   - From tensile test: Ex,eff = σx/εx = 69.68 GPa
   - From bending test: Ex,bend = 43.51 GPa

3. **Search for Matching Sequence:**
   - 8 plies total (2 mm / 0.25 mm)
   - Must be symmetric and balanced
   - Only 0°, ±45°, 90° plies allowed

### Results

| Parameter | Value |
|-----------|-------|
| **Stacking Sequence** | **[±45/0/90]s** |
| **Full Layup** | [45°/-45°/0°/90°/90°/0°/-45°/45°] |
| **Number of Plies** | 8 (2 each at 0°, 90°, +45°, -45°) |

### Verification

| Test | Experimental | Calculated | Error |
|------|--------------|------------|-------|
| Tensile elongation | 0.0897 mm | 0.0897 mm | **0.00%** |
| Bending slope | 0.0808 mm/N | 0.0814 mm/N | **0.78%** |

### Laminate Properties
- **Quasi-isotropic** in-plane behavior (A₁₁ = A₂₂)
- **No extension-bending coupling** (B = 0)
- **No extension-shear coupling** (A₁₆ = A₂₆ = 0)

### Files
- `problem2_stacking_sequence.py` - Analysis script

---

## Problem 3: Laminate Analysis under Combined Loading

### Problem Statement
Analyze a [30/45/-45/-30]T Kevlar/Epoxy laminate subjected to:
- Nx = Ny = 1000 N/m
- My = Mxy = 50 N

Determine:
- (a) Mid-plane strains and curvatures
- (b) Global stresses vs. vertical location (plot)
- (c) Failure analysis using Tsai-Hill criterion

### Given Data

| Property | Value | Property | Value |
|----------|-------|----------|-------|
| E₁ | 76 GPa | Xt | 1400 MPa |
| E₂ | 5.50 GPa | Xc | 235 MPa |
| G₁₂ | 2.30 GPa | Yt | 53 MPa |
| ν₁₂ | 0.34 | Yc | 12 MPa |
| t | 1.25 mm | S | 34 MPa |

### Solution Approach

1. **Calculate ABD Matrices** for the unsymmetric laminate
2. **Solve for strains/curvatures:** {ε°, κ} = [abd] × {N, M}
3. **Calculate stresses** at each ply interface
4. **Apply Tsai-Hill criterion** for failure check

### Results

#### (a) Mid-plane Strains and Curvatures

| **Mid-plane Strains** | **Value** |
|----------------------|-----------|
| ε°x | 666.66 με |
| ε°y | -11.48 με |
| γ°xy | 286.42 με |

| **Curvatures** | **Value** |
|----------------|-----------|
| κx | -0.2018 1/m |
| κy | 0.8060 1/m |
| κxy | 0.8453 1/m |

**Note:** Non-zero B matrix causes curvatures even with Mx = 0, and strains are affected by moments.

#### (b) Global Stresses vs. z

![Global Stresses](problem3_global_stresses.png)

| Ply | Location | z (mm) | σx (MPa) | σy (MPa) | τxy (MPa) |
|-----|----------|--------|----------|----------|-----------|
| 1 (30°) | Bot | -2.50 | -18.19 | -17.98 | -17.12 |
| 1 (30°) | Top | -1.25 | 9.40 | -2.96 | 1.21 |
| 2 (45°) | Bot | -1.25 | -11.38 | -20.30 | -16.88 |
| 2 (45°) | Top | 0.00 | 20.73 | 17.61 | 17.26 |
| 3 (-45°) | Bot | 0.00 | 10.55 | 7.43 | -6.03 |
| 3 (-45°) | Top | 1.25 | 5.10 | 7.78 | 1.26 |
| 4 (-30°) | Bot | 1.25 | 3.09 | 5.85 | 3.17 |
| 4 (-30°) | Top | 2.50 | -17.69 | 4.17 | 17.12 |

#### (c) Tsai-Hill Failure Analysis

| Ply | θ | Location | σ₁ (MPa) | σ₂ (MPa) | τ₁₂ (MPa) | FI | Status |
|-----|---|----------|----------|----------|-----------|------|--------|
| 1 | 30° | Bot | -32.96 | -3.21 | -8.47 | **0.1513** | Safe |
| 1 | 30° | Top | 7.36 | -0.92 | -4.75 | 0.0254 | Safe |
| 2 | 45° | Bot | -32.72 | 1.04 | -4.46 | 0.0376 | Safe |
| 2 | 45° | Top | 36.43 | 1.91 | -1.56 | 0.0040 | Safe |
| 3 | -45° | Bot | 15.02 | 2.96 | 1.56 | 0.0053 | Safe |
| 3 | -45° | Top | 5.18 | 7.70 | -1.34 | 0.0226 | Safe |
| 4 | -30° | Bot | 1.04 | 7.90 | 0.39 | 0.0224 | Safe |
| 4 | -30° | Top | -27.06 | 13.54 | -0.91 | 0.0858 | Safe |

### Conclusion
- **Maximum Failure Index:** FI = 0.1513 (Ply 1, 30°, bottom)
- **✓ NO FAILURE:** All plies are safe (FI < 1)
- **Safety Factor:** 2.57

### Files
- `problem3_laminate_analysis.py` - Analysis script
- `problem3_global_stresses.png` - Stress distribution plot

---

## Problem 4: Laminate Design Optimization

### Problem Statement
Design a 16-ply Zylon/Epoxy laminate with angles limited to (0°, ±30°, ±60°, 90°) subjected to:
- σx = 250 MPa, σy = 50 MPa, τxy = 150 MPa
- Strain limits: εx ≤ 0.006, εy ≤ 0.0006, γxy ≤ 0.02

Determine:
- (a) All possible stacking sequences satisfying strain limits
- (b) Stacking sequence with minimum |αx|
- (c) Check individual ply failure

### Given Data

| Property | Value |
|----------|-------|
| E₁ | 120.0 GPa |
| E₂ | 6.5 GPa |
| G₁₂ | 3.0 GPa |
| ν₁₂ | 0.32 |
| α₁ | -0.8 × 10⁻⁶ /°C |
| α₂ | 20.5 × 10⁻⁶ /°C |

### Results

#### (a) Valid Stacking Sequences

**Found 85 valid symmetric, balanced laminate configurations** satisfying laminate strain limits.

Top configurations by |αx|:

| # | n0 | n±30 | n±60 | n90 | εx (με) | εy (με) | γxy (με) | αx (10⁻⁶/°C) |
|---|-----|------|------|-----|---------|---------|----------|--------------|
| 1 | 2 | 10 | 0 | 4 | 4157.82 | -320.65 | 9368.89 | 0.0073 |
| 2 | 3 | 8 | 2 | 3 | 4157.82 | -320.65 | 9368.89 | 0.0073 |
| 3 | 4 | 6 | 4 | 2 | 4157.82 | -320.65 | 9368.89 | 0.0073 |
| 4 | 4 | 8 | 0 | 4 | 3687.23 | 100.44 | 11187.06 | -0.0632 |
| 5 | 5 | 6 | 2 | 3 | 3687.23 | 100.44 | 11187.06 | -0.0632 |

#### (b) Minimum |αx| Stacking Sequence

| Parameter | Value |
|-----------|-------|
| **Ply Distribution** | 6×0°, 2×(±30°), 8×(±60°), 0×90° |
| **Stacking Sequence** | [30/-30/60/-60/60/-60/60/-60]s |

**Mid-plane Strains:**

| Strain | Value | Limit | Status |
|--------|-------|-------|--------|
| εx | 4157.82 με | ±6000 με | ✓ |
| εy | -320.65 με | ±600 με | ✓ |
| γxy | 9368.89 με | ±20000 με | ✓ |

**Coefficients of Thermal Expansion:**

| CTE | Value |
|-----|-------|
| **αx** | **0.0073 × 10⁻⁶ /°C** ← MINIMUM |
| αy | 1.42 × 10⁻⁶ /°C |
| αxy | 0 /°C |

![Alpha Contour](problem4_alpha_contour.png)

#### (c) Individual Ply Failure Check

| Ply Angle | ε₁ (με) | ε₂ (με) | γ₁₂ (με) | Status |
|-----------|---------|---------|----------|--------|
| 0° | 4157.82 | -320.65 | 9368.89 | **Safe ✓** |
| 30° | 7095.05 | -3257.88 | 805.97 | **FAIL** (ε₁, ε₂) |
| -30° | -1018.65 | 4855.82 | 8562.92 | **FAIL** (ε₂) |
| 60° | 4855.82 | -1018.65 | -8562.92 | **FAIL** (ε₂) |
| -60° | -3257.88 | 7095.05 | -805.97 | **FAIL** (ε₂) |

### Conclusion
- **10 out of 16 plies FAIL** at the ply level
- Only **0° plies are safe**
- Off-axis plies fail due to excessive transverse strain (ε₂)
- The ply-level transverse strain limit of 600 με is too restrictive for off-axis plies

**Design Recommendation:** A redesign with different ply proportions or reduced loading would be needed for a safe design at the ply level.

### Files
- `problem4_laminate_design.py` - Analysis script
- `problem4_alpha_contour.png` - αx contour plot

---

## Summary of Python Scripts

| Problem | Script | Description |
|---------|--------|-------------|
| 1 | `problem1_strength_envelope.py` | Strength envelope using maximum strain criterion |
| 2 | `problem2_stacking_sequence.py` | Inverse problem - determine stacking from experiments |
| 3 | `problem3_laminate_analysis.py` | CLT analysis with Tsai-Hill failure criterion |
| 4 | `problem4_laminate_design.py` | Laminate design optimization for minimum CTE |

## How to Run

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run individual problems
python assignment_2/assignment_3/problem1_strength_envelope.py
python assignment_2/assignment_3/problem2_stacking_sequence.py
python assignment_2/assignment_3/problem3_laminate_analysis.py
python assignment_2/assignment_3/problem4_laminate_design.py
```

---

## References
- Classical Laminated Plate Theory (CLPT)
- Maximum Strain Failure Criterion
- Tsai-Hill Failure Criterion
- Thermal Expansion of Composite Laminates
