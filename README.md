# STP 604E - Composite Materials Course

**Classical Laminated Plate Theory (CLPT) Analysis Tools**

A comprehensive Python toolkit for composite materials analysis including assignment solvers and interactive 3D visualization.

## 🎯 Features

### 1. **Complete Assignment Solutions**
- ✅ Problem 1: Quasi-Isotropic Laminate Analysis
- ✅ Problem 2: Micromechanics Analysis
- ✅ Problem 3: Zero Shear Strain Constraint
- ✅ Problem 4: Stiffness Matrix Comparison

### 2. **Interactive 3D Visualizer**
- 🏗️ **Laminate Structure Visualization**: 3D view of ply orientations
- 📊 **Stiffness Analysis**: Interactive heatmaps and rotation studies
- 🔄 **Quasi-Isotropic Study**: Real-time quasi-isotropy testing
- 🎛️ **Parametric Analysis**: Explore parameter effects interactively
- 📈 **Stress/Strain Distribution**: Through-thickness visualization

### 3. **Composite Materials Library**
- Micromechanics calculations (Rule of Mixtures, Halpin-Tsai)
- Lamina analysis (Q matrix, transformed properties)
- Laminate analysis (A, B, D matrices)
- Classical Laminated Plate Theory (CLPT)
- Stress/strain calculations

## 📦 Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## 🚀 Quick Start

### Run Assignment Solutions

```bash
# Interactive menu
python solve_assignments.py

# Or run specific problem
python solve_assignments.py 1   # Problem 1
python solve_assignments.py 2   # Problem 2
# etc.
```

### Launch 3D Visualizer

```bash
# Start the interactive web visualizer
python run_visualizer.py
```

The visualizer will open in your web browser with an interactive interface.

## 📚 Usage Examples

### Example 1: Create a Laminate

```python
from composite_lib import Laminate

# Define material properties
material = {
    'E1': 181.0,   # GPa
    'E2': 10.3,    # GPa
    'G12': 7.17,   # GPa
    'nu12': 0.28
}

# Create laminate
lam = Laminate(material, [0, 45, -45, 90], ply_thickness=0.125)

# Access stiffness matrices
print(lam.A)  # Extensional stiffness
print(lam.B)  # Coupling stiffness
print(lam.D)  # Bending stiffness
```

### Example 2: Micromechanics

```python
from composite_lib import Micromechanics

# Calculate lamina properties from fiber and matrix
micro = Micromechanics(
    E_f=220,    # Fiber modulus (GPa)
    nu_f=0.25,  # Fiber Poisson's ratio
    E_m=3.6,    # Matrix modulus (GPa)
    nu_m=0.40,  # Matrix Poisson's ratio
    V_f=0.60    # Fiber volume fraction
)

props = micro.get_engineering_constants()
print(f"E1 = {props['E1']:.2f} GPa")
print(f"E2 = {props['E2']:.2f} GPa")
```

### Example 3: Stress Analysis

```python
# Define loads
loads = {
    'Nx': 1000,   # N/m
    'Ny': 1000,   # N/m
    'Nxy': 0,     # N/m
    'Mx': 0,      # N
    'My': 50,     # N
    'Mxy': 0      # N
}

# Calculate strains and curvatures
strains, curvatures = lam.calculate_strains_curvatures(loads)

# Calculate ply stresses
for i in range(lam.n_plies):
    stress_global, stress_local = lam.calculate_ply_stresses(
        strains, curvatures, i, 'mid'
    )
    print(f"Ply {i+1}: σ1={stress_local[0]:.2f} MPa")
```

## 📁 Project Structure

```
STP604E/
├── composite_lib/          # Core analysis library
│   ├── __init__.py
│   ├── micromechanics.py   # Fiber/matrix to lamina
│   ├── lamina.py           # Single ply analysis
│   └── laminate.py         # CLPT implementation
│
├── assignments/            # Assignment solutions
│   ├── assignment1_problem1.py
│   ├── assignment1_problem2.py
│   ├── assignment1_problem3.py
│   └── assignment1_problem4.py
│
├── visualization/          # 3D visualization tools
│   └── composite_visualizer.py
│
├── solve_assignments.py    # Run assignment solutions
├── run_visualizer.py       # Launch 3D visualizer
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔬 Visualizer Features

### 1. Laminate Structure
- 3D visualization of ply stack
- Fiber orientation arrows
- Interactive rotation and zoom
- Ply-by-ply information

### 2. Stiffness Analysis
- Heatmap visualization of A, B, D matrices
- Real-time rotation effects
- Material property comparison

### 3. Quasi-Isotropic Study
- Test multiple laminate configurations
- Automatic quasi-isotropy detection
- Rotation invariance plots

### 4. Parametric Analysis
- Vary ply angles interactively
- Material property sensitivity
- Thickness effect studies

### 5. Stress/Strain Distribution
- Through-thickness stress plots
- Global and material coordinate systems
- Ply-by-ply analysis

## 📊 Assignment Solutions

### Problem 1: Quasi-Isotropic Analysis
- Analyzes [-45/0/45/90] and [0/30/60/90] laminates
- Plots A_ij vs rotation angle
- Determines quasi-isotropy automatically
- Generates publication-quality plots

### Problem 2: Micromechanics
- Calculates fiber volume fraction from geometry
- Applies Rule of Mixtures and Halpin-Tsai
- Determines laminate engineering constants
- Complete step-by-step solution

### Problem 3: Zero Shear Strain
- Finds optimal ply angles for constraint
- Parametric study over angle range
- Plots strains and curvatures
- Detailed discussion of results

### Problem 4: Stiffness Comparison
- Compares [-45/45] vs [-45/45/-45/45]
- Analyzes A, B, D matrix scaling
- Discusses thickness effects
- Comprehensive comparison tables

## 🛠️ Material Presets

The visualizer includes presets for common materials:
- **AS4/3501-6 Carbon/Epoxy**: High-performance aerospace
- **AS/3501 Graphite/Epoxy**: Classic graphite composite
- **Kevlar/Epoxy**: High-strength aramid fiber
- **E-Glass/Epoxy**: Cost-effective fiberglass
- **Custom**: Define your own material

## 📖 Theory Reference

Based on Classical Laminated Plate Theory (CLPT):

**Stiffness Matrices:**
- **[A]**: Extensional stiffness (relates N to ε°)
- **[B]**: Coupling stiffness (couples N and κ)
- **[D]**: Bending stiffness (relates M to κ)

**Key Equations:**
```
{N}   [A  B] {ε°}
{M} = [B  D] {κ }

A_ij = Σ Q̄_ij^(k) (z_k - z_{k-1})
B_ij = ½ Σ Q̄_ij^(k) (z_k² - z_{k-1}²)
D_ij = ⅓ Σ Q̄_ij^(k) (z_k³ - z_{k-1}³)
```

## 🎓 Course Information

**Course:** STP 604E - Defence Technologies
**Topic:** Classical Laminated Plate Theory (CLPT)
**Institution:** Istanbul Technical University
**Semester:** Fall 2025

### Topics Covered:
- Mechanics of laminated composite materials
- Classical lamination plate theory
- Failure criteria for composites
- Structural optimization
- Bending, buckling, and vibration analysis

## 📝 License

Educational use for STP 604E course.

## 👨‍💻 Author

Created for STP 604E Composite Materials Course

## 🤝 Contributing

This is a course project. For questions or suggestions, please contact the course instructor.

---

**Happy Learning! 🚀**
