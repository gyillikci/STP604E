# Assignment 2 - Problem 4: Mathematical Derivation

## Problem Statement

Derive the formula for the bending stiffness matrix **D** of a laminate composed of two sublaminates **M** and **N**:

$$D_{MN} = D_M + D_N + \frac{t_N^2}{4}A_M + \frac{t_M^2}{4}A_N - t_N B_M + t_M B_N$$

where:
- $D_{MN}$ = bending stiffness of combined laminate
- $D_M, D_N$ = bending stiffness matrices of sublaminates M and N
- $A_M, A_N$ = extensional stiffness matrices of sublaminates M and N
- $B_M, B_N$ = bending-extension coupling matrices of sublaminates M and N
- $t_M, t_N$ = total thicknesses of sublaminates M and N

---

## Theoretical Background

### Classical Lamination Theory (CLT)

The ABD matrices relate stress resultants to mid-plane strains and curvatures:

$$\begin{bmatrix} N \\ M \end{bmatrix} = \begin{bmatrix} A & B \\ B & D \end{bmatrix} \begin{bmatrix} \varepsilon^0 \\ \kappa \end{bmatrix}$$

where:
- $A_{ij} = \sum_{k=1}^{n} \bar{Q}_{ij}^{(k)} (z_{k} - z_{k-1})$ (extensional stiffness)
- $B_{ij} = \frac{1}{2} \sum_{k=1}^{n} \bar{Q}_{ij}^{(k)} (z_{k}^2 - z_{k-1}^2)$ (coupling stiffness)
- $D_{ij} = \frac{1}{3} \sum_{k=1}^{n} \bar{Q}_{ij}^{(k)} (z_{k}^3 - z_{k-1}^3)$ (bending stiffness)
- $z$ = through-thickness coordinate (measured from mid-plane)
- $\bar{Q}_{ij}^{(k)}$ = transformed reduced stiffness of ply $k$

---

## Derivation

### Step 1: Define Coordinate Systems

Consider two sublaminates **M** (bottom) and **N** (top) with their own local coordinate systems.

**Global coordinate system** (combined laminate MN):
- Origin at mid-plane of combined laminate
- $z$ ranges from $-h_{MN}/2$ to $+h_{MN}/2$
- Total thickness: $h_{MN} = t_M + t_N$

**Local coordinate system for sublaminate M**:
- Origin at mid-plane of M
- $z_M$ ranges from $-t_M/2$ to $+t_M/2$

**Local coordinate system for sublaminate N**:
- Origin at mid-plane of N
- $z_N$ ranges from $-t_N/2$ to $+t_N/2$

### Step 2: Coordinate Transformations

The relationship between global $z$ and local coordinates:

**For sublaminate M** (bottom):
$$z = z_M - d_M$$
where $d_M = \frac{t_N}{2}$ is the offset of M's mid-plane below the global mid-plane.

Thus:
$$z_M = z + \frac{t_N}{2}$$

**For sublaminate N** (top):
$$z = z_N + d_N$$
where $d_N = \frac{t_M}{2}$ is the offset of N's mid-plane above the global mid-plane.

Thus:
$$z_N = z - \frac{t_M}{2}$$

### Step 3: Express D_MN Using Definitions

The bending stiffness of the combined laminate is:

$$D_{MN} = \frac{1}{3} \sum_{\text{all plies}} \bar{Q}_{ij}^{(k)} (z_{k}^3 - z_{k-1}^3)$$

Split the sum into contributions from sublaminates M and N:

$$D_{MN} = \frac{1}{3} \sum_{\text{M plies}} \bar{Q}_{ij}^{(k)} (z_{k}^3 - z_{k-1}^3) + \frac{1}{3} \sum_{\text{N plies}} \bar{Q}_{ij}^{(k)} (z_{k}^3 - z_{k-1}^3)$$

$$D_{MN} = D_M^{\text{global}} + D_N^{\text{global}}$$

But we need to express this in terms of the **local** ABD matrices of M and N.

### Step 4: Transform D_M to Global Coordinates

In the **local** coordinate system of M:

$$D_M = \frac{1}{3} \sum_{\text{M plies}} \bar{Q}_{ij}^{(k)} (z_{M,k}^3 - z_{M,k-1}^3)$$

To transform to the **global** system, use $z = z_M - t_N/2$:

$$D_M^{\text{global}} = \frac{1}{3} \sum_{\text{M plies}} \bar{Q}_{ij}^{(k)} \left[(z_{M,k} - t_N/2)^3 - (z_{M,k-1} - t_N/2)^3\right]$$

Expand using $(a-b)^3 = a^3 - 3a^2b + 3ab^2 - b^3$:

$$(z_M - t_N/2)^3 = z_M^3 - 3z_M^2(t_N/2) + 3z_M(t_N/2)^2 - (t_N/2)^3$$

$$= z_M^3 - \frac{3t_N}{2}z_M^2 + \frac{3t_N^2}{4}z_M - \frac{t_N^3}{8}$$

Substituting into the sum:

$$D_M^{\text{global}} = \frac{1}{3} \sum \bar{Q}_{ij}^{(k)} \left[z_{M,k}^3 - z_{M,k-1}^3 - \frac{3t_N}{2}(z_{M,k}^2 - z_{M,k-1}^2) + \frac{3t_N^2}{4}(z_{M,k} - z_{M,k-1})\right]$$

Note the $-t_N^3/8$ terms cancel out in the difference.

Recognize the sums:
- $\frac{1}{3}\sum \bar{Q}_{ij}^{(k)} (z_{M,k}^3 - z_{M,k-1}^3) = D_M$
- $\frac{1}{2}\sum \bar{Q}_{ij}^{(k)} (z_{M,k}^2 - z_{M,k-1}^2) = B_M$
- $\sum \bar{Q}_{ij}^{(k)} (z_{M,k} - z_{M,k-1}) = A_M$

Therefore:

$$D_M^{\text{global}} = D_M - \frac{3t_N}{2} \cdot \frac{1}{3} \cdot \frac{1}{2} \sum \bar{Q}_{ij}^{(k)} (z_{M,k}^2 - z_{M,k-1}^2) \cdot 2 + \frac{3t_N^2}{4} \cdot \frac{1}{3} \sum \bar{Q}_{ij}^{(k)} (z_{M,k} - z_{M,k-1})$$

Simplifying:

$$D_M^{\text{global}} = D_M - t_N \cdot B_M + \frac{t_N^2}{4} A_M$$

### Step 5: Transform D_N to Global Coordinates

Similarly, for sublaminate N using $z = z_N + t_M/2$:

$$(z_N + t_M/2)^3 = z_N^3 + 3z_N^2(t_M/2) + 3z_N(t_M/2)^2 + (t_M/2)^3$$

$$= z_N^3 + \frac{3t_M}{2}z_N^2 + \frac{3t_M^2}{4}z_N + \frac{t_M^3}{8}$$

Following the same procedure:

$$D_N^{\text{global}} = \frac{1}{3} \sum \bar{Q}_{ij}^{(k)} \left[z_{N,k}^3 - z_{N,k-1}^3 + \frac{3t_M}{2}(z_{N,k}^2 - z_{N,k-1}^2) + \frac{3t_M^2}{4}(z_{N,k} - z_{N,k-1})\right]$$

Recognizing the sums:

$$D_N^{\text{global}} = D_N + t_M \cdot B_N + \frac{t_M^2}{4} A_N$$

### Step 6: Combine Results

The total bending stiffness of the combined laminate is:

$$D_{MN} = D_M^{\text{global}} + D_N^{\text{global}}$$

Substituting the expressions from Steps 4 and 5:

$$D_{MN} = \left(D_M - t_N B_M + \frac{t_N^2}{4} A_M\right) + \left(D_N + t_M B_N + \frac{t_M^2}{4} A_N\right)$$

Rearranging:

$$\boxed{D_{MN} = D_M + D_N + \frac{t_N^2}{4}A_M + \frac{t_M^2}{4}A_N - t_N B_M + t_M B_N}$$

**Q.E.D.**

---

## Physical Interpretation

The formula consists of several contributions:

1. **$D_M + D_N$**: Direct sum of bending stiffnesses of the two sublaminates in their local coordinate systems.

2. **$\frac{t_N^2}{4}A_M + \frac{t_M^2}{4}A_N$**: **Parallel axis theorem** contributions. When a sublaminate is moved away from the global neutral axis, its extensional stiffness contributes to the overall bending stiffness. The factor $t^2/4$ represents the square of the offset distance.

3. **$-t_N B_M + t_M B_N$**: **Coupling corrections**. The $B$ matrices represent asymmetry within each sublaminate. When transformed to the global coordinate system, these coupling terms must be adjusted by the offset distances. The signs reflect whether the sublaminate is above (+) or below (-) the global mid-plane.

### Special Cases

**Case 1: Symmetric sublaminates** ($B_M = B_N = 0$)
$$D_{MN} = D_M + D_N + \frac{t_N^2}{4}A_M + \frac{t_M^2}{4}A_N$$
Only the direct bending stiffnesses and parallel axis terms remain.

**Case 2: Equal thickness sublaminates** ($t_M = t_N = t/2$)
$$D_{MN} = D_M + D_N + \frac{t^2}{16}(A_M + A_N) + \frac{t}{2}(B_N - B_M)$$

**Case 3: Thin sublaminates** ($t_M, t_N \ll h_{MN}$)
The $t^2$ terms become negligible, and parallel axis effects dominate.

---

## Numerical Example

Consider two sublaminates:
- **Sublaminate M**: [0°/90°] with $t_M$ = 0.25 mm
- **Sublaminate N**: [45°/-45°] with $t_N$ = 0.25 mm

Using typical graphite/epoxy properties:
- E₁ = 138 GPa, E₂ = 8.96 GPa, G₁₂ = 7.10 GPa, ν₁₂ = 0.30
- Ply thickness = 0.125 mm

**Sublaminate M** (cross-ply):
```
A_M = [matrix values]
B_M = 0 (symmetric)
D_M = [matrix values]
```

**Sublaminate N** (angle-ply):
```
A_N = [matrix values]
B_N ≠ 0 (antisymmetric, but net coupling may be small)
D_N = [matrix values]
```

The combined laminate $D_{MN}$ would include:
1. Direct bending contributions from both sublaminates
2. Parallel axis terms: $(0.25)^2/4 \cdot A_M$ and $(0.25)^2/4 \cdot A_N$
3. Coupling corrections: $0.25 \cdot B_N$ (assuming $B_M = 0$)

This demonstrates how the formula enables **modular laminate design** - analyzing sublaminates independently and then combining them.

---

## Applications

This derivation is crucial for:

1. **Sandwich composites**: Face sheets (M and N) separated by a core
2. **Hybrid laminates**: Combining different material systems
3. **Repair patches**: Adding reinforcement to existing structures
4. **Computational efficiency**: Pre-computing sublaminate properties
5. **Sensitivity analysis**: Understanding how thickness changes affect bending stiffness

---

## Verification

The derived formula can be verified by:

1. **Direct calculation**: Compute $D_{MN}$ using standard CLT with all plies
2. **Modular calculation**: Compute $D_M$ and $D_N$ separately, then apply formula
3. **Confirm equality**: Both methods must give identical results

This verification is implemented in finite element codes and laminate analysis software.

---

## Conclusion

The derivation demonstrates how **coordinate transformations** and the **parallel axis theorem** enable modular analysis of composite laminates. The formula elegantly captures:
- Direct stiffness contributions ($D_M$, $D_N$)
- Geometric effects ($t^2$ terms)
- Asymmetry corrections ($B$ terms)

This result is a cornerstone of **building-block approaches** in composite structural analysis, allowing engineers to design and analyze complex laminates systematically.

---

## References

1. Jones, R.M., *Mechanics of Composite Materials*, 2nd ed., Taylor & Francis, 1999.
2. Hyer, M.W., *Stress Analysis of Fiber-Reinforced Composite Materials*, DEStech Publications, 2009.
3. Reddy, J.N., *Mechanics of Laminated Composite Plates and Shells: Theory and Analysis*, 2nd ed., CRC Press, 2004.

---

*Note: This derivation assumes linear elastic behavior, perfect bonding between sublaminates, and that Kirchhoff-Love plate theory assumptions hold (thin plates, small deformations).*
