# Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `numpy` - Numerical computing
- `scipy` - Scientific computing
- `matplotlib` - Plotting
- `plotly` - Interactive 3D visualization
- `streamlit` - Web-based visualizer

### Step 2: Run Assignment Solutions

```bash
python solve_assignments.py
```

You'll see an interactive menu:

```
Select an option:
  1 - Problem 1: Quasi-Isotropic Laminate Analysis
  2 - Problem 2: Micromechanics Analysis
  3 - Problem 3: Zero Shear Strain Constraint
  4 - Problem 4: Stiffness Matrix Comparison
  5 - Run ALL problems
  0 - Exit
```

**Each problem will:**
- Show step-by-step calculations
- Display results in the terminal
- Generate plots (saved as PNG files)
- Provide detailed explanations

### Step 3: Launch the 3D Visualizer

```bash
python run_visualizer.py
```

This opens an interactive web interface where you can:
- **Visualize** laminate structures in 3D
- **Explore** parameter effects in real-time
- **Analyze** stiffness matrices
- **Plot** stress/strain distributions
- **Test** quasi-isotropic laminates

## 📊 Quick Examples

### Example 1: Solve a Specific Problem

```bash
python solve_assignments.py 1
```

This runs Problem 1 directly without the menu.

### Example 2: Use the Library in Python

```python
from composite_lib import Laminate

# Define material (AS/3501 Graphite-Epoxy)
material = {
    'E1': 181.0,
    'E2': 10.3,
    'G12': 7.17,
    'nu12': 0.28
}

# Create a quasi-isotropic laminate
lam = Laminate(material, [0, 45, -45, 90], ply_thickness=0.125)

# Print properties
lam.print_properties()

# Access stiffness matrices
print("A matrix:", lam.A)
print("B matrix:", lam.B)
print("D matrix:", lam.D)
```

### Example 3: Micromechanics Calculation

```python
from composite_lib import Micromechanics

# Calculate properties from fiber and matrix
micro = Micromechanics(
    E_f=220.0,   # Fiber modulus (GPa)
    nu_f=0.25,   # Fiber Poisson's ratio
    E_m=3.6,     # Matrix modulus (GPa)
    nu_m=0.40,   # Matrix Poisson's ratio
    V_f=0.60     # Fiber volume fraction
)

# Get lamina properties
props = micro.get_engineering_constants()
micro.print_properties()
```

## 🎯 Visualizer Guide

### Visualization Modes:

1. **Laminate Structure**
   - 3D view of ply stack
   - Fiber orientations
   - Z-coordinate table

2. **Stiffness Analysis**
   - Matrix heatmaps
   - Rotation effects
   - Real-time updates

3. **Quasi-Isotropic Study**
   - Test standard configurations
   - Automatic isotropy detection
   - Rotation plots

4. **Parametric Analysis**
   - Vary ply angles
   - Material properties
   - Thickness effects

5. **Stress/Strain Distribution**
   - Through-thickness plots
   - Ply-by-ply stresses
   - Global & local coordinates

### Controls:

- **Sidebar:** Material properties and configuration
- **Main Panel:** Visualization and results
- **Interactive Plots:** Zoom, pan, rotate with mouse
- **Real-time Updates:** Changes reflect immediately

## 📝 Assignment Solutions

### Problem 1: Quasi-Isotropic
- **Output:** Terminal results + `assignment1_problem1_results.png`
- **Shows:** A_ij vs rotation, isotropy determination

### Problem 2: Micromechanics
- **Output:** Terminal results with step-by-step calculations
- **Shows:** V_f calculation, lamina properties, laminate constants

### Problem 3: Zero Shear Strain
- **Output:** Terminal results + `assignment1_problem3_results.png`
- **Shows:** Optimal θ, strain/curvature plots, discussion

### Problem 4: Stiffness Comparison
- **Output:** Terminal results with comparison tables
- **Shows:** A, B, D matrices for both laminates, scaling analysis

## 💡 Tips

1. **For quick testing:** Run individual problems (1-4)
2. **For exploration:** Use the visualizer
3. **For custom analysis:** Import the library in your own scripts
4. **For learning:** Read the printed step-by-step solutions

## 🔧 Troubleshooting

**Import Error?**
```bash
pip install -r requirements.txt
```

**Visualizer won't start?**
```bash
# Check streamlit installation
streamlit --version

# Reinstall if needed
pip install streamlit --upgrade
```

**Plots not showing?**
- Plots are saved as PNG files in the current directory
- Look for `assignment1_problem*_results.png`

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the code in `composite_lib/` to understand CLPT implementation
- Try modifying material properties in the visualizer
- Create custom laminates and analyze them

**Happy analyzing! 🎓**
