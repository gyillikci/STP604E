# Problem 1: Strength Envelope Analysis

## Graphite/Epoxy Laminate [0/±45₂/90]s under Biaxial Loading

### Given Data

**Material Properties (Graphite/Epoxy):**
| Property | Value |
|----------|-------|
| E₁ | 138 GPa |
| E₂ | 8.69 GPa |
| G₁₂ | 7.10 GPa |
| ν₁₂ | 0.3 |
| t (ply) | 0.125 mm |

**Strength Values:**
| Property | Value |
|----------|-------|
| Xₜ (Longitudinal Tensile) | 2280 MPa |
| Xc (Longitudinal Compressive) | 1725 MPa |
| Yₜ (Transverse Tensile) | 57 MPa |
| Yc (Transverse Compressive) | 228 MPa |
| S (Shear) | 76 MPa |

---

## Laminate Configuration

**Stacking Sequence:** [0/±45₂/90]s

**Full layup:** [0°, 45°, 45°, -45°, -45°, 90°, 90°, -45°, -45°, 45°, 45°, 0°]

**Total thickness:** h = 12 × 0.125 = **1.5 mm**

---

## Maximum Strain Criterion

The allowable strains are calculated from the strength values:

| Strain Limit | Formula | Value |
|--------------|---------|-------|
| ε₁ᵗ (fiber tensile) | Xₜ/E₁ | 16,522 με |
| ε₁ᶜ (fiber compressive) | Xc/E₁ | 12,500 με |
| ε₂ᵗ (matrix tensile) | Yₜ/E₂ | 6,559 με |
| ε₂ᶜ (matrix compressive) | Yc/E₂ | 26,237 με |
| γ₁₂ᵐᵃˣ (shear) | S/G₁₂ | 10,704 με |

---

## Ā Matrix (Extensional Stiffness normalized by thickness)

$$\bar{A} = \frac{[A]}{h} = \begin{bmatrix} 54782.65 & 21602.25 & 0 \\ 21602.25 & 54782.65 & 0 \\ 0 & 0 & 26080.39 \end{bmatrix} \text{ MPa}$$

This is a **balanced laminate** (A₁₆ = A₂₆ = 0) and **quasi-isotropic-like** (Ā₁₁ = Ā₂₂).

---

## Results

### (a) Maximum Pure Tensile Load (Nₓ)

| Parameter | Value |
|-----------|-------|
| **Maximum σ̄ₓ** | **303.46 MPa** |
| **Maximum Nₓ** | **455.19 N/mm** |
| **Failure Type** | **Matrix Tensile failure (ε₂ > ε₂ᵗ) in 90° ply** |

**Explanation:** Under pure tensile Nₓ loading, the 90° ply experiences the highest transverse tensile strain. The fibers in the 90° ply are perpendicular to the loading direction, so they carry load primarily through the matrix (transverse direction). The matrix tensile strength is the limiting factor.

**Strains at Failure:**
- Global: εₓ = 6559 με, εᵧ = -2586 με
- In 90° ply: ε₂ = 6559 με = ε₂ᵗ (failure)

---

### (b) Maximum Pure Compressive Load (Nᵧ)

| Parameter | Value |
|-----------|-------|
| **Maximum σ̄ᵧ** | **-355.17 MPa** |
| **Maximum Nᵧ** | **-532.76 N/mm** |
| **Failure Type** | **Shear failure (|γ₁₂| > γ₁₂ᵐᵃˣ) in ±45° plies** |

**Explanation:** Under pure compressive Nᵧ loading, the ±45° plies experience high shear strains due to the off-axis loading. The shear strain in these plies reaches the allowable limit first, causing in-plane shear failure.

**Strains at Failure:**
- Global: εₓ = 3027 με, εᵧ = -7677 με  
- In ±45° plies: γ₁₂ = ±10,704 με = γ₁₂ᵐᵃˣ (failure)

---

## Strength Envelope

![Strength Envelope](strength_envelope.png)

The strength envelope shows the safe operating region (shaded) in the σ̄ₓ - σ̄ᵧ stress space. Key observations:

1. **Symmetric envelope:** Due to balanced laminate (Ā₁₁ = Ā₂₂), the envelope is symmetric about the 45° line
2. **Tensile limits (σ̄ₓ, σ̄ᵧ > 0):** Governed by matrix tensile failure in 90° and 0° plies respectively
3. **Compressive limits:** Governed by shear failure in ±45° plies
4. **The laminate is stronger in compression than tension** along principal axes

---

## Summary Table

| Load Case | Maximum Stress | Maximum Load | Failure Mode |
|-----------|---------------|--------------|--------------|
| Nₓ (tensile) | σ̄ₓ = 303.5 MPa | **455.2 N/mm** | Matrix tensile in 90° ply |
| Nₓ (compressive) | σ̄ₓ = -355.2 MPa | -532.8 N/mm | Shear in ±45° plies |
| Nᵧ (tensile) | σ̄ᵧ = 303.5 MPa | 455.2 N/mm | Matrix tensile in 0° ply |
| Nᵧ (compressive) | σ̄ᵧ = -355.2 MPa | **-532.8 N/mm** | Shear in ±45° plies |
