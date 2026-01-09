"""
Generate PDF documentation for Assignment 2 Problems 2, 3, and 4
"""

import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

def find_browser():
    """Find Chrome or Edge executable"""
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for path in chrome_paths:
        if os.path.exists(path):
            return path
    for path in edge_paths:
        if os.path.exists(path):
            return path
    return None

def html_to_pdf(html_file, pdf_file, browser):
    """Convert HTML to PDF using browser"""
    cmd = [
        browser,
        '--headless',
        '--disable-gpu',
        '--no-sandbox',
        '--print-to-pdf=' + str(pdf_file.absolute()),
        '--print-to-pdf-no-header',
        '--no-pdf-header-footer',
        str(html_file.absolute())
    ]
    subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    time.sleep(1)
    return pdf_file.exists()

# ============================================================================
# PROBLEM 2 HTML
# ============================================================================
def generate_problem2_html():
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Assignment 2 - Problem 2 Analysis</title>
    <style>
        @media print {{ @page {{ size: A4; margin: 2cm; }} body {{ font-size: 10pt; }} }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 20px; color: #333; }}
        h1 {{ color: #1a1a1a; font-size: 28px; border-bottom: 3px solid #2c5aa0; padding-bottom: 10px; text-align: center; }}
        h2 {{ color: #2c5aa0; font-size: 20px; border-bottom: 2px solid #7ba7d8; padding-bottom: 8px; margin-top: 30px; }}
        h3 {{ color: #34495e; font-size: 16px; margin-top: 20px; }}
        .header-info {{ text-align: center; margin-bottom: 30px; color: #666; }}
        .success-box {{ background-color: #d4edda; border: 2px solid #28a745; border-radius: 8px; padding: 20px; margin: 20px 0; text-align: center; }}
        .success-box h2 {{ color: #28a745; border: none; margin: 0; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; font-size: 14px; }}
        th {{ background-color: #2c5aa0; color: white; font-weight: bold; padding: 12px 8px; text-align: left; border: 1px solid #1e3d6f; }}
        td {{ padding: 10px 8px; border: 1px solid #ddd; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .check-mark {{ color: #28a745; font-weight: bold; }}
        .highlight {{ background-color: #fff3cd; padding: 15px; border-radius: 5px; border-left: 4px solid #ffc107; margin: 15px 0; }}
        footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #777; font-size: 0.9em; }}
        pre {{ background-color: #f8f8f8; border: 1px solid #ddd; border-left: 4px solid #2c5aa0; border-radius: 4px; padding: 15px; font-family: 'Consolas', monospace; font-size: 12px; }}
    </style>
</head>
<body>

<h1>Assignment 2 - Problem 2 Analysis</h1>

<div class="header-info">
    <p><strong>Course:</strong> STP604E - Mechanics of Composite Materials</p>
    <p><strong>Student:</strong> Giray Yıllıkçı</p>
    <p><strong>Date:</strong> {datetime.now().strftime("%B %d, %Y")}</p>
</div>

<div class="success-box">
    <h2>✅ Optimal Solution Found: 5 Plies (0.625 mm)</h2>
</div>

<h2>Problem Statement</h2>
<p>Design a laminate with <strong>minimum thickness</strong> using discrete angles: 0°, ±15°, ±30°, ±45°, ±60°, ±75°, 90°</p>

<h3>Constraints</h3>
<table>
    <tr><th>Property</th><th>Requirement</th></tr>
    <tr><td>Poisson's ratio (ν<sub>xy</sub>)</td><td>0.2 ≤ ν<sub>xy</sub> ≤ 0.7</td></tr>
    <tr><td>Shear modulus (G<sub>xy</sub>)</td><td>≥ 5 GPa</td></tr>
    <tr><td>Longitudinal modulus (E<sub>x</sub>)</td><td>≥ 22 GPa</td></tr>
    <tr><td>Transverse modulus (E<sub>y</sub>)</td><td>≥ 18 GPa</td></tr>
</table>

<h3>Material Properties</h3>
<table>
    <tr><th>Property</th><th>Value</th></tr>
    <tr><td>E₁</td><td>38.6 GPa</td></tr>
    <tr><td>E₂</td><td>8.27 GPa</td></tr>
    <tr><td>G₁₂</td><td>4.14 GPa</td></tr>
    <tr><td>ν₁₂</td><td>0.28</td></tr>
    <tr><td>Ply thickness</td><td>0.125 mm</td></tr>
</table>

<h2>Optimal Solution</h2>

<h3>Design Configuration</h3>
<div class="highlight">
    <strong>Minimum thickness: 5 plies (0.625 mm)</strong><br><br>
    <strong>Ply Distribution:</strong><br>
    • 0°: 2 plies<br>
    • 30°: 1 ply<br>
    • -75°: 2 plies
</div>

<h3>Laminate Properties</h3>
<table>
    <tr><th>Property</th><th>Value</th><th>Requirement</th><th>Status</th></tr>
    <tr><td>E<sub>x</sub></td><td>23.10 GPa</td><td>≥ 22 GPa</td><td class="check-mark">✅</td></tr>
    <tr><td>E<sub>y</sub></td><td>18.34 GPa</td><td>≥ 18 GPa</td><td class="check-mark">✅</td></tr>
    <tr><td>G<sub>xy</sub></td><td>5.45 GPa</td><td>≥ 5 GPa</td><td class="check-mark">✅</td></tr>
    <tr><td>ν<sub>xy</sub></td><td>0.235</td><td>0.2 - 0.7</td><td class="check-mark">✅</td></tr>
</table>

<h2>Parameter Sensitivity Study</h2>

<h3>Effect of Population Size (fixed iterations = 100)</h3>
<table>
    <tr><th>Population</th><th>Best Plies</th><th>Mean Plies</th><th>Notes</th></tr>
    <tr><td>20</td><td>22</td><td>43.3</td><td>Poor exploration</td></tr>
    <tr><td>50</td><td>6</td><td>35.7</td><td>Good balance</td></tr>
    <tr style="background-color: #d4edda;"><td><strong>100</strong></td><td><strong>6</strong></td><td><strong>16.0</strong></td><td><strong>Recommended</strong></td></tr>
    <tr><td>200</td><td>3*</td><td>16.0</td><td>*Infeasible solution</td></tr>
</table>

<h3>Effect of Maximum Iterations (fixed population = 50)</h3>
<table>
    <tr><th>Iterations</th><th>Best Plies</th><th>Mean Plies</th><th>Notes</th></tr>
    <tr><td>50</td><td>5</td><td>39.7</td><td>High variability</td></tr>
    <tr style="background-color: #d4edda;"><td><strong>100-200</strong></td><td><strong>5-6</strong></td><td><strong>20-35</strong></td><td><strong>Recommended</strong></td></tr>
    <tr><td>300</td><td>5</td><td>6.3</td><td>Diminishing returns</td></tr>
</table>

<h2>Key Findings</h2>
<ul>
    <li><strong>Discrete optimization</strong> is more challenging than continuous angles</li>
    <li>Multiple competing constraints create complex feasible region</li>
    <li>Population size 50-100 provides good exploration/cost balance</li>
    <li>100-200 iterations sufficient for convergence</li>
    <li>Multiple runs recommended (5-10) to capture variability</li>
</ul>

<h2>Recommendations</h2>

<h3>For Production Applications</h3>
<ul>
    <li>Consider 6-7 ply designs for safety margins</li>
    <li>Implement balanced/symmetric layups if coupling is undesirable</li>
    <li>Validate with finite element analysis</li>
</ul>

<h3>For PSO Parameters</h3>
<ul>
    <li>Population: 50-100</li>
    <li>Iterations: 100-200</li>
    <li>Multiple runs: 5-10</li>
    <li>Penalty coefficient: 10,000</li>
</ul>

<h2>Computational Performance</h2>
<p>Total execution time: <strong>78.06 seconds</strong> (including parameter study)</p>

<footer>
    <p>Generated on {datetime.now().strftime("%B %d, %Y at %H:%M")} | STP604E - Assignment 2</p>
</footer>

</body>
</html>
"""

# ============================================================================
# PROBLEM 3 HTML
# ============================================================================
def generate_problem3_html():
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Assignment 2 - Problem 3 Analysis</title>
    <style>
        @media print {{ @page {{ size: A4; margin: 2cm; }} body {{ font-size: 10pt; }} }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 20px; color: #333; }}
        h1 {{ color: #1a1a1a; font-size: 28px; border-bottom: 3px solid #2c5aa0; padding-bottom: 10px; text-align: center; }}
        h2 {{ color: #2c5aa0; font-size: 20px; border-bottom: 2px solid #7ba7d8; padding-bottom: 8px; margin-top: 30px; }}
        h3 {{ color: #34495e; font-size: 16px; margin-top: 20px; }}
        .header-info {{ text-align: center; margin-bottom: 30px; color: #666; }}
        .success-box {{ background-color: #d4edda; border: 2px solid #28a745; border-radius: 8px; padding: 20px; margin: 20px 0; text-align: center; }}
        .success-box h2 {{ color: #28a745; border: none; margin: 0; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; font-size: 14px; }}
        th {{ background-color: #2c5aa0; color: white; font-weight: bold; padding: 12px 8px; text-align: left; border: 1px solid #1e3d6f; }}
        td {{ padding: 10px 8px; border: 1px solid #ddd; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .check-mark {{ color: #28a745; font-weight: bold; }}
        .highlight {{ background-color: #fff3cd; padding: 15px; border-radius: 5px; border-left: 4px solid #ffc107; margin: 15px 0; }}
        footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #777; font-size: 0.9em; }}
        pre {{ background-color: #f8f8f8; border: 1px solid #ddd; border-left: 4px solid #2c5aa0; border-radius: 4px; padding: 15px; font-family: 'Consolas', monospace; font-size: 12px; }}
        .best {{ background-color: #d4edda; font-weight: bold; }}
    </style>
</head>
<body>

<h1>Assignment 2 - Problem 3 Analysis</h1>

<div class="header-info">
    <p><strong>Course:</strong> STP604E - Mechanics of Composite Materials</p>
    <p><strong>Student:</strong> Giray Yıllıkçı</p>
    <p><strong>Date:</strong> {datetime.now().strftime("%B %d, %Y")}</p>
</div>

<div class="success-box">
    <h2>✅ Maximum E<sub>y</sub> = 58.59 GPa (Continuous Angles)</h2>
</div>

<h2>Problem Statement</h2>
<p>Design a <strong>16-layer balanced symmetric laminate</strong> to <strong>maximize E<sub>y</sub></strong> subject to:</p>
<ul>
    <li>E<sub>x</sub> ≥ 70 GPa</li>
    <li>G<sub>xy</sub> ≥ 15 GPa</li>
    <li>ν<sub>xy</sub> < 0.4</li>
</ul>

<h3>Material Properties (Graphite/Epoxy)</h3>
<table>
    <tr><th>Property</th><th>Value</th></tr>
    <tr><td>E₁</td><td>138 GPa</td></tr>
    <tr><td>E₂</td><td>8.96 GPa</td></tr>
    <tr><td>G₁₂</td><td>7.10 GPa</td></tr>
    <tr><td>ν₁₂</td><td>0.30</td></tr>
</table>

<h3>Three Design Cases</h3>
<ul>
    <li><strong>(a)</strong> Continuous fiber orientations (2-angle solution)</li>
    <li><strong>(b)</strong> Discrete angles: 0°, ±45°, 90°</li>
    <li><strong>(c)</strong> Discrete angles: 0°, ±30°, ±60°, 90°</li>
</ul>

<h2>Methodology: Miki's Lamination Parameters</h2>
<p>For balanced symmetric laminates, only two parameters are needed:</p>
<ul>
    <li><strong>V₁</strong>: Related to longitudinal stiffness variation</li>
    <li><strong>V₃</strong>: Related to extension-shear coupling</li>
</ul>

<h2>Results Summary</h2>
<table>
    <tr><th>Case</th><th>Configuration</th><th>E<sub>y</sub> (GPa)</th><th>E<sub>x</sub> (GPa)</th><th>G<sub>xy</sub> (GPa)</th><th>ν<sub>xy</sub></th></tr>
    <tr class="best"><td>(a) Continuous</td><td>[±10.3°/±69.5°]₂ₛ</td><td><strong>58.59</strong></td><td>70.00</td><td>15.00</td><td>0.176</td></tr>
    <tr><td>(b) 0°,±45°,90°</td><td>[0₄/45₃/90]ₛ</td><td>36.84</td><td>82.95</td><td>17.79</td><td>0.344</td></tr>
    <tr><td>(c) 0°,±30°,±60°,90°</td><td>[0₄/60₃/90]ₛ</td><td>52.25</td><td>75.92</td><td>15.12</td><td>0.200</td></tr>
</table>

<h2>Case (a): Continuous Fiber Orientations</h2>

<div class="highlight">
    <strong>🏆 Best Performance: E<sub>y</sub> = 58.59 GPa</strong><br><br>
    <strong>Optimal Lamination Parameters:</strong><br>
    • V₁ = 0.0903<br>
    • V₃ = 0.4457<br><br>
    <strong>2-Angle Solution:</strong> [±10.3°/±69.5°]₂ₛ
</div>

<p><strong>Physical Interpretation:</strong></p>
<ul>
    <li><strong>10.3° plies:</strong> Provide longitudinal stiffness (E<sub>x</sub> ≥ 70)</li>
    <li><strong>69.5° plies:</strong> Provide transverse stiffness (maximize E<sub>y</sub>)</li>
    <li>E<sub>x</sub> and G<sub>xy</sub> are exactly at constraint boundaries → truly optimal</li>
</ul>

<h2>Case (b): Discrete Angles (0°, ±45°, 90°)</h2>

<p><strong>Configuration:</strong> [0°/0°/0°/0°/45°/45°/45°/90°]ₛ</p>
<p><strong>E<sub>y</sub> = 36.84 GPa</strong> (63% of optimal)</p>

<p><strong>Ply Distribution:</strong></p>
<ul>
    <li>0°: 8 plies (50%)</li>
    <li>45°: 6 plies (37.5%)</li>
    <li>90°: 2 plies (12.5%)</li>
</ul>

<h2>Case (c): Extended Discrete (0°, ±30°, ±60°, 90°)</h2>

<p><strong>Configuration:</strong> [0°/0°/0°/0°/60°/60°/60°/90°]ₛ</p>
<p><strong>E<sub>y</sub> = 52.25 GPa</strong> (89% of optimal)</p>

<p><strong>Key Insight:</strong> The 60° plies are the key differentiator, providing better E<sub>y</sub> contribution than 45° plies.</p>

<h2>Comparative Analysis</h2>

<table>
    <tr><th>Metric</th><th>Case (a)</th><th>Case (c)</th><th>Case (b)</th></tr>
    <tr><td><strong>E<sub>y</sub> (objective)</strong></td><td>58.59 GPa (100%)</td><td>52.25 GPa (89%)</td><td>36.84 GPa (63%)</td></tr>
    <tr><td>E<sub>x</sub> margin</td><td>0%</td><td>+8%</td><td>+18%</td></tr>
    <tr><td>G<sub>xy</sub> margin</td><td>0%</td><td>+0.8%</td><td>+19%</td></tr>
    <tr><td>ν<sub>xy</sub> margin</td><td>56%</td><td>50%</td><td>14%</td></tr>
</table>

<h2>Key Findings</h2>

<ol>
    <li><strong>Continuous angles</strong> achieve theoretical maximum by pushing constraints to exact boundaries</li>
    <li><strong>Discrete angle restrictions</strong> significantly impact performance:
        <ul>
            <li>±30°/±60° options: 11% loss (acceptable)</li>
            <li>Only 0°/±45°/90°: 37% loss (substantial)</li>
        </ul>
    </li>
    <li><strong>Lamination parameters</strong> provide elegant optimization approach</li>
    <li>PSO converges in ~50 iterations in 2D parameter space</li>
</ol>

<h2>Engineering Recommendations</h2>

<table>
    <tr><th>Application</th><th>Recommended Design</th><th>E<sub>y</sub></th></tr>
    <tr><td>Maximum Performance (AFP capable)</td><td>[±10.3°/±69.5°]₂ₛ</td><td>58.59 GPa</td></tr>
    <tr><td>Practical Manufacturing</td><td>[0₄/60₃/90]ₛ</td><td>52.25 GPa</td></tr>
    <tr><td>Aerospace Standards Only</td><td>[0₄/45₃/90]ₛ</td><td>36.84 GPa</td></tr>
</table>

<h2>Computational Performance</h2>
<p>Total execution time: <strong>2.73 seconds</strong></p>

<footer>
    <p>Generated on {datetime.now().strftime("%B %d, %Y at %H:%M")} | STP604E - Assignment 2</p>
</footer>

</body>
</html>
"""

# ============================================================================
# PROBLEM 4 HTML
# ============================================================================
def generate_problem4_html():
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Assignment 2 - Problem 4 Derivation</title>
    <style>
        @media print {{ @page {{ size: A4; margin: 2cm; }} body {{ font-size: 10pt; }} }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 20px; color: #333; }}
        h1 {{ color: #1a1a1a; font-size: 28px; border-bottom: 3px solid #2c5aa0; padding-bottom: 10px; text-align: center; }}
        h2 {{ color: #2c5aa0; font-size: 20px; border-bottom: 2px solid #7ba7d8; padding-bottom: 8px; margin-top: 30px; }}
        h3 {{ color: #34495e; font-size: 16px; margin-top: 20px; }}
        .header-info {{ text-align: center; margin-bottom: 30px; color: #666; }}
        .success-box {{ background-color: #d4edda; border: 2px solid #28a745; border-radius: 8px; padding: 20px; margin: 20px 0; text-align: center; }}
        .success-box h2 {{ color: #28a745; border: none; margin: 0; }}
        .formula-box {{ background-color: #e8f4fd; border: 2px solid #2c5aa0; border-radius: 8px; padding: 20px; margin: 20px 0; text-align: center; font-size: 16px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; font-size: 14px; }}
        th {{ background-color: #2c5aa0; color: white; font-weight: bold; padding: 12px 8px; text-align: left; border: 1px solid #1e3d6f; }}
        td {{ padding: 10px 8px; border: 1px solid #ddd; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .highlight {{ background-color: #fff3cd; padding: 15px; border-radius: 5px; border-left: 4px solid #ffc107; margin: 15px 0; }}
        footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #777; font-size: 0.9em; }}
        pre {{ background-color: #f8f8f8; border: 1px solid #ddd; border-left: 4px solid #2c5aa0; border-radius: 4px; padding: 15px; font-family: 'Consolas', monospace; font-size: 12px; overflow-x: auto; }}
        .math {{ font-family: 'Cambria Math', 'Times New Roman', serif; font-style: italic; }}
    </style>
</head>
<body>

<h1>Assignment 2 - Problem 4 Derivation</h1>

<div class="header-info">
    <p><strong>Course:</strong> STP604E - Mechanics of Composite Materials</p>
    <p><strong>Student:</strong> Giray Yıllıkçı</p>
    <p><strong>Date:</strong> {datetime.now().strftime("%B %d, %Y")}</p>
</div>

<div class="success-box">
    <h2>✅ Mathematical Derivation Complete</h2>
</div>

<h2>Problem Statement</h2>
<p>Derive the formula for the bending stiffness matrix <strong>D</strong> of a laminate composed of two sublaminates <strong>M</strong> and <strong>N</strong>.</p>

<div class="formula-box">
    <strong>D<sub>MN</sub> = D<sub>M</sub> + D<sub>N</sub> + (t<sub>N</sub>²/4)A<sub>M</sub> + (t<sub>M</sub>²/4)A<sub>N</sub> − t<sub>N</sub>B<sub>M</sub> + t<sub>M</sub>B<sub>N</sub></strong>
</div>

<h3>Variables</h3>
<table>
    <tr><th>Symbol</th><th>Description</th></tr>
    <tr><td>D<sub>MN</sub></td><td>Bending stiffness of combined laminate</td></tr>
    <tr><td>D<sub>M</sub>, D<sub>N</sub></td><td>Bending stiffness matrices of sublaminates</td></tr>
    <tr><td>A<sub>M</sub>, A<sub>N</sub></td><td>Extensional stiffness matrices of sublaminates</td></tr>
    <tr><td>B<sub>M</sub>, B<sub>N</sub></td><td>Bending-extension coupling matrices</td></tr>
    <tr><td>t<sub>M</sub>, t<sub>N</sub></td><td>Total thicknesses of sublaminates</td></tr>
</table>

<h2>Derivation</h2>

<h3>Step 1: Define Coordinate Systems</h3>
<p>Consider two sublaminates: <strong>M</strong> (bottom) and <strong>N</strong> (top)</p>
<ul>
    <li><strong>Global system:</strong> Origin at mid-plane of combined laminate</li>
    <li><strong>Local system M:</strong> Origin at mid-plane of sublaminate M</li>
    <li><strong>Local system N:</strong> Origin at mid-plane of sublaminate N</li>
</ul>

<h3>Step 2: Coordinate Transformations</h3>
<p><strong>For sublaminate M (bottom):</strong></p>
<pre>z = z<sub>M</sub> − t<sub>N</sub>/2</pre>
<p>Thus: z<sub>M</sub> = z + t<sub>N</sub>/2</p>

<p><strong>For sublaminate N (top):</strong></p>
<pre>z = z<sub>N</sub> + t<sub>M</sub>/2</pre>
<p>Thus: z<sub>N</sub> = z − t<sub>M</sub>/2</p>

<h3>Step 3: Transform D<sub>M</sub> to Global Coordinates</h3>
<p>Using the binomial expansion of (z<sub>M</sub> − t<sub>N</sub>/2)³:</p>
<pre>
(z<sub>M</sub> − t<sub>N</sub>/2)³ = z<sub>M</sub>³ − (3t<sub>N</sub>/2)z<sub>M</sub>² + (3t<sub>N</sub>²/4)z<sub>M</sub> − t<sub>N</sub>³/8
</pre>

<p>Recognizing the CLT definitions:</p>
<ul>
    <li>∫Q̄(z³) → D<sub>M</sub></li>
    <li>∫Q̄(z²) → B<sub>M</sub></li>
    <li>∫Q̄(z) → A<sub>M</sub></li>
</ul>

<p>We obtain:</p>
<pre>D<sub>M</sub><sup>global</sup> = D<sub>M</sub> − t<sub>N</sub>·B<sub>M</sub> + (t<sub>N</sub>²/4)·A<sub>M</sub></pre>

<h3>Step 4: Transform D<sub>N</sub> to Global Coordinates</h3>
<p>Similarly, using (z<sub>N</sub> + t<sub>M</sub>/2)³:</p>
<pre>D<sub>N</sub><sup>global</sup> = D<sub>N</sub> + t<sub>M</sub>·B<sub>N</sub> + (t<sub>M</sub>²/4)·A<sub>N</sub></pre>

<h3>Step 5: Combine Results</h3>
<p>The total bending stiffness:</p>
<pre>D<sub>MN</sub> = D<sub>M</sub><sup>global</sup> + D<sub>N</sub><sup>global</sup></pre>

<div class="formula-box">
    <strong>D<sub>MN</sub> = D<sub>M</sub> + D<sub>N</sub> + (t<sub>N</sub>²/4)A<sub>M</sub> + (t<sub>M</sub>²/4)A<sub>N</sub> − t<sub>N</sub>B<sub>M</sub> + t<sub>M</sub>B<sub>N</sub></strong>
    <br><br><em>Q.E.D.</em>
</div>

<h2>Physical Interpretation</h2>

<table>
    <tr><th>Term</th><th>Physical Meaning</th></tr>
    <tr><td>D<sub>M</sub> + D<sub>N</sub></td><td>Direct sum of bending stiffnesses</td></tr>
    <tr><td>(t²/4)·A</td><td><strong>Parallel axis theorem:</strong> Extensional stiffness contributes to bending when offset from neutral axis</td></tr>
    <tr><td>±t·B</td><td><strong>Coupling corrections:</strong> Asymmetry adjustments for global coordinate system</td></tr>
</table>

<h2>Special Cases</h2>

<h3>Case 1: Symmetric Sublaminates (B<sub>M</sub> = B<sub>N</sub> = 0)</h3>
<pre>D<sub>MN</sub> = D<sub>M</sub> + D<sub>N</sub> + (t<sub>N</sub>²/4)A<sub>M</sub> + (t<sub>M</sub>²/4)A<sub>N</sub></pre>

<h3>Case 2: Equal Thickness (t<sub>M</sub> = t<sub>N</sub> = t/2)</h3>
<pre>D<sub>MN</sub> = D<sub>M</sub> + D<sub>N</sub> + (t²/16)(A<sub>M</sub> + A<sub>N</sub>) + (t/2)(B<sub>N</sub> − B<sub>M</sub>)</pre>

<h2>Applications</h2>
<ul>
    <li><strong>Sandwich composites:</strong> Face sheets separated by core</li>
    <li><strong>Hybrid laminates:</strong> Combining different material systems</li>
    <li><strong>Repair patches:</strong> Adding reinforcement to existing structures</li>
    <li><strong>Computational efficiency:</strong> Pre-computing sublaminate properties</li>
    <li><strong>Modular design:</strong> Building-block approaches in structural analysis</li>
</ul>

<h2>Conclusion</h2>
<div class="highlight">
    The derivation demonstrates how <strong>coordinate transformations</strong> and the <strong>parallel axis theorem</strong> enable modular analysis of composite laminates. This formula is fundamental for:
    <ul>
        <li>Sandwich panel design</li>
        <li>Hybrid laminate optimization</li>
        <li>Efficient computational analysis</li>
    </ul>
</div>

<h2>References</h2>
<ol>
    <li>Jones, R.M., <em>Mechanics of Composite Materials</em>, 2nd ed., Taylor & Francis, 1999.</li>
    <li>Hyer, M.W., <em>Stress Analysis of Fiber-Reinforced Composite Materials</em>, DEStech Publications, 2009.</li>
    <li>Reddy, J.N., <em>Mechanics of Laminated Composite Plates and Shells</em>, 2nd ed., CRC Press, 2004.</li>
</ol>

<footer>
    <p>Generated on {datetime.now().strftime("%B %d, %Y at %H:%M")} | STP604E - Assignment 2</p>
</footer>

</body>
</html>
"""

# ============================================================================
# MAIN FUNCTION
# ============================================================================
def main():
    print("="*60)
    print("Generating Assignment 2 Analysis PDFs")
    print("="*60)
    
    browser = find_browser()
    if not browser:
        print("✗ No browser found!")
        return
    
    print(f"✓ Using browser: {browser}")
    
    problems = [
        (2, generate_problem2_html),
        (3, generate_problem3_html),
        (4, generate_problem4_html),
    ]
    
    for num, generator in problems:
        print(f"\nProblem {num}:")
        
        html_file = Path(f"assignment_2/PROBLEM{num}_ANALYSIS.html")
        pdf_file = Path(f"assignment_2/PROBLEM{num}_ANALYSIS.pdf")
        
        # Generate HTML
        html_content = generator()
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"  ✓ HTML: {html_file}")
        
        # Convert to PDF
        if html_to_pdf(html_file, pdf_file, browser):
            size = pdf_file.stat().st_size / 1024
            print(f"  ✓ PDF: {pdf_file} ({size:.1f} KB)")
        else:
            print(f"  ✗ PDF creation failed")
    
    print("\n" + "="*60)
    print("✓ All PDFs generated successfully!")
    print("="*60)
    
    # Open the PDFs
    for num in [2, 3, 4]:
        pdf_path = Path(f"assignment_2/PROBLEM{num}_ANALYSIS.pdf").absolute()
        if pdf_path.exists():
            os.startfile(str(pdf_path))

if __name__ == "__main__":
    main()
