# Assignment 3 - Results Summary

## Course: STP604E - Composite Materials
## Topic: Laminate Strength and Design Analysis

---

## Problem 1: Strength Envelope for [0/±45₂/90]s Graphite/Epoxy Laminate

### Material Properties
- E₁ = 138 GPa, E₂ = 8.69 GPa, G₁₂ = 7.10 GPa, ν₁₂ = 0.3
- Xt = 2280 MPa, Xc = 1725 MPa, Yt = 57 MPa, Yc = 228 MPa, S = 76 MPa
- Ply thickness = 0.125 mm

### Results

#### (a) Maximum Pure Tensile Load Nx
| Parameter | Value |
|-----------|-------|
| σ̄x,max | 303.46 MPa |
| **Nx,max** | **455.19 N/mm** |
| Failure Mode | Matrix tensile (ε₂ > ε₂ᵗ) |
| Critical Ply | 90° ply |

#### (b) Maximum Pure Compressive Load Ny
| Parameter | Value |
|-----------|-------|
| σ̄y,max | -355.17 MPa |
| **Ny,max** | **-532.76 N/mm** |
| Failure Mode | Shear failure (γ₁₂ > γ₁₂ᵐᵃˣ) |
| Critical Ply | ±45° plies |

### Strain Allowables (Maximum Strain Criterion)
| Limit | Value (με) |
|-------|------------|
| ε₁ᵗ (fiber tensile) | 16,522 |
| ε₁ᶜ (fiber compressive) | 12,500 |
| ε₂ᵗ (matrix tensile) | 6,559 |
| ε₂ᶜ (matrix compressive) | 26,237 |
| γ₁₂ᵐᵃˣ (shear) | 10,704 |

### Strength Envelope Plot

![Strength Envelope for [0/±45₂/90]s Laminate](strength_envelope.png)

*Figure 1: Biaxial strength envelope in the σ̄x - σ̄y plane using maximum strain criterion. The envelope shows the safe operating region bounded by different failure modes.*

---

## Problem 2: Stacking Sequence from Experimental Data

### Experimental Observations
1. Uniaxial tensile test: No bending, no shear → Symmetric & balanced laminate
2. Tensile elongation: 0.0897 mm at 2500 N load
3. Bending slope: 0.0808 mm/N
4. Plate dimensions: 150 mm × 30 mm × 2 mm (8 plies at 0.25 mm each)

### Material Properties
- E₁ = 181 GPa, E₂ = 10.3 GPa, G₁₂ = 7.17 GPa, ν₁₂ = 0.28

### Results

| Parameter | Value |
|-----------|-------|
| **Stacking Sequence** | **[±45/0/90]s** |
| Full Layup | [45°/-45°/0°/90°/90°/0°/-45°/45°] |
| Ply Distribution | 2×0°, 2×90°, 2×(+45°), 2×(-45°) |

### Verification
| Test | Experimental | Calculated | Error |
|------|--------------|------------|-------|
| Tensile elongation | 0.0897 mm | 0.0897 mm | **0.00%** |
| Bending slope | 0.0808 mm/N | 0.0814 mm/N | **0.78%** |

### Derived Stiffnesses
- Required Ex,eff (tensile) = 69.68 GPa
- Required Ex,bend (bending) = 43.51 GPa

### Stacking Sequence Visualization

![Stacking Sequence [±45/0/90]s and Experimental Verification](problem2_stacking_sequence.png)

*Figure 2: Left - Cross-sectional view of the [±45/0/90]s laminate showing ply orientations. Right - Comparison of experimental measurements vs. calculated values for the determined stacking sequence.*

---

## Problem 3: [30/45/-45/-30]T Kevlar/Epoxy under Combined Loading

### Loading Conditions
- Nx = Ny = 1000 N/m
- Mx = 0, My = Mxy = 50 N

### Material Properties
- E₁ = 76 GPa, E₂ = 5.50 GPa, G₁₂ = 2.30 GPa, ν₁₂ = 0.34
- Xt = 1400 MPa, Xc = 235 MPa, Yt = 53 MPa, Yc = 12 MPa, S = 34 MPa
- Ply thickness = 1.25 mm

### Results

#### (a) Mid-plane Strains and Curvatures

| Mid-plane Strains | Value |
|-------------------|-------|
| ε°x | 666.66 με |
| ε°y | -11.48 με |
| γ°xy | 286.42 με |

| Curvatures | Value |
|------------|-------|
| κx | -0.2018 1/m |
| κy | 0.8060 1/m |
| κxy | 0.8453 1/m |

#### (b) Global Stresses at Ply Interfaces

| Ply | θ | z (mm) | σx (MPa) | σy (MPa) | τxy (MPa) |
|-----|---|--------|----------|----------|-----------|
| 1 | 30° | -2.50 (bot) | -18.19 | -17.98 | -17.12 |
| 1 | 30° | -1.25 (top) | 9.40 | -2.96 | 1.21 |
| 2 | 45° | -1.25 (bot) | -11.38 | -20.30 | -16.88 |
| 2 | 45° | 0.00 (top) | 20.73 | 17.61 | 17.26 |
| 3 | -45° | 0.00 (bot) | 10.55 | 7.43 | -6.03 |
| 3 | -45° | 1.25 (top) | 5.10 | 7.78 | 1.26 |
| 4 | -30° | 1.25 (bot) | 3.09 | 5.85 | 3.17 |
| 4 | -30° | 2.50 (top) | -17.69 | 4.17 | 17.12 |

#### (c) Tsai-Hill Failure Analysis

| Ply | θ | Location | σ₁ (MPa) | σ₂ (MPa) | τ₁₂ (MPa) | FI | Status |
|-----|---|----------|----------|----------|-----------|------|--------|
| 1 | 30° | Bottom | -32.96 | -3.21 | -8.47 | **0.1513** | ✓ Safe |
| 1 | 30° | Top | 7.36 | -0.92 | -4.75 | 0.0254 | ✓ Safe |
| 2 | 45° | Bottom | -32.72 | 1.04 | -4.46 | 0.0376 | ✓ Safe |
| 2 | 45° | Top | 36.43 | 1.91 | -1.56 | 0.0040 | ✓ Safe |
| 3 | -45° | Bottom | 15.02 | 2.96 | 1.56 | 0.0053 | ✓ Safe |
| 3 | -45° | Top | 5.18 | 7.70 | -1.34 | 0.0226 | ✓ Safe |
| 4 | -30° | Bottom | 1.04 | 7.90 | 0.39 | 0.0224 | ✓ Safe |
| 4 | -30° | Top | -27.06 | 13.54 | -0.91 | 0.0858 | ✓ Safe |

### Global Stress Distribution Plot

![Global Stresses vs. Thickness for [30/45/-45/-30]T Laminate](problem3_global_stresses.png)

*Figure 3: Global stress components (σx, σy, τxy) through the laminate thickness. The discontinuities at ply interfaces are due to different ply orientations.*

### Conclusion
- **Maximum Failure Index:** 0.1513 (Ply 1, 30°, bottom surface)
- **Status: ✓ NO FAILURE** - All plies safe
- **Safety Factor:** 2.57

---

## Problem 4: 16-Ply Zylon/Epoxy Laminate Design Optimization

### Design Requirements
- 16 plies with angles limited to: 0°, ±30°, ±60°, 90°
- Symmetric and balanced laminate
- Loading: σx = 250 MPa, σy = 50 MPa, τxy = 150 MPa
- Strain limits: |εx| ≤ 6000 με, |εy| ≤ 600 με, |γxy| ≤ 20000 με

### Material Properties
- E₁ = 120 GPa, E₂ = 6.5 GPa, G₁₂ = 3.0 GPa, ν₁₂ = 0.32
- α₁ = -0.8 × 10⁻⁶ /°C, α₂ = 20.5 × 10⁻⁶ /°C

### Results

#### (a) Valid Stacking Sequences
**Found 85 symmetric, balanced configurations** satisfying laminate strain limits.

#### (b) Minimum |αx| Configuration

| Parameter | Value |
|-----------|-------|
| **Ply Distribution** | 6×0°, 2×(±30°), 8×(±60°), 0×90° |
| **Stacking Sequence** | [30/-30/60/-60/60/-60/60/-60]s |
| **αx** | **0.0073 × 10⁻⁶ /°C** |
| αy | 1.42 × 10⁻⁶ /°C |

#### Laminate Strains
| Strain | Value | Limit | Status |
|--------|-------|-------|--------|
| εx | 4157.82 με | ±6000 με | ✓ OK |
| εy | -320.65 με | ±600 με | ✓ OK |
| γxy | 9368.89 με | ±20000 με | ✓ OK |

### Coefficient of Thermal Expansion Contour

![αx Contour Plot for 16-Ply Laminate Design](problem4_alpha_contour.png)

*Figure 4: Contour plot showing αx (×10⁻⁶/°C) as a function of ply distribution. The optimal region with minimum |αx| is clearly visible.*

#### Top 5 Configurations by |αx|

| Rank | n₀ | n±₃₀ | n±₆₀ | n₉₀ | αx (10⁻⁶/°C) |
|------|-----|------|------|-----|--------------|
| 1 | 2 | 10 | 0 | 4 | 0.0073 |
| 2 | 3 | 8 | 2 | 3 | 0.0073 |
| 3 | 4 | 6 | 4 | 2 | 0.0073 |
| 4 | 4 | 8 | 0 | 4 | -0.0632 |
| 5 | 5 | 6 | 2 | 3 | -0.0632 |

#### (c) Individual Ply Failure Check

| Ply Angle | ε₁ (με) | ε₂ (με) | γ₁₂ (με) | Status |
|-----------|---------|---------|----------|--------|
| 0° | 4157.82 | -320.65 | 9368.89 | ✓ Safe |
| 30° | 7095.05 | -3257.88 | 805.97 | ✗ FAIL |
| -30° | -1018.65 | 4855.82 | 8562.92 | ✗ FAIL |
| 60° | 4855.82 | -1018.65 | -8562.92 | ✗ FAIL |
| -60° | -3257.88 | 7095.05 | -805.97 | ✗ FAIL |

### Conclusion
- **10 out of 16 plies FAIL** at the ply level
- Only **0° plies are safe**
- Off-axis plies fail due to excessive transverse strain (ε₂ > 600 με after transformation)
- **Design Note:** The ply-level εy limit of 600 με is too restrictive for off-axis plies under this loading

---

## Summary Table

| Problem | Key Result | Critical Finding |
|---------|------------|------------------|
| 1 | Nx,max = 455.19 N/mm | 90° ply fails first (matrix tensile) |
| 1 | Ny,max = -532.76 N/mm | ±45° plies fail first (shear) |
| 2 | [±45/0/90]s | Quasi-isotropic, 0.78% bending error |
| 3 | FI,max = 0.1513 | No failure, SF = 2.57 |
| 4 | αx,min = 0.0073×10⁻⁶/°C | 10/16 plies fail at ply level |

---

## Generated Files

| File | Description |
|------|-------------|
| `problem1_strength_envelope.py` | Strength envelope analysis |
| `problem2_stacking_sequence.py` | Inverse stacking sequence problem |
| `problem3_laminate_analysis.py` | CLT analysis with Tsai-Hill |
| `problem4_laminate_design.py` | Design optimization |
| `strength_envelope.png` | Problem 1 plot |
| `problem3_global_stresses.png` | Problem 3 stress distribution |
| `problem4_alpha_contour.png` | Problem 4 CTE contour |

---

*Generated: January 2026*
