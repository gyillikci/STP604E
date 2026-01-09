"""
Generate PDF documentation for Assignment 2 Problem 1 Verification
"""

import os
from datetime import datetime

def generate_verification_html():
    """Generate HTML content for the verification report"""
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Assignment 2 - Problem 1 Verification</title>
    <style>
        @media print {{
            @page {{
                size: A4;
                margin: 2cm;
            }}
            body {{ font-size: 10pt; }}
        }}
        
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        
        h1 {{
            color: #1a1a1a;
            font-size: 28px;
            border-bottom: 3px solid #2c5aa0;
            padding-bottom: 10px;
            text-align: center;
        }}
        
        h2 {{
            color: #2c5aa0;
            font-size: 20px;
            border-bottom: 2px solid #7ba7d8;
            padding-bottom: 8px;
            margin-top: 30px;
        }}
        
        h3 {{
            color: #34495e;
            font-size: 16px;
            margin-top: 20px;
        }}
        
        .header-info {{
            text-align: center;
            margin-bottom: 30px;
            color: #666;
        }}
        
        .success-box {{
            background-color: #d4edda;
            border: 2px solid #28a745;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            text-align: center;
        }}
        
        .success-box h2 {{
            color: #28a745;
            border: none;
            margin: 0;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            font-size: 14px;
        }}
        
        th {{
            background-color: #2c5aa0;
            color: white;
            font-weight: bold;
            padding: 12px 8px;
            text-align: left;
            border: 1px solid #1e3d6f;
        }}
        
        td {{
            padding: 10px 8px;
            border: 1px solid #ddd;
        }}
        
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        .check-mark {{
            color: #28a745;
            font-weight: bold;
        }}
        
        pre {{
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-left: 4px solid #2c5aa0;
            border-radius: 4px;
            padding: 15px;
            overflow-x: auto;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 12px;
            line-height: 1.4;
        }}
        
        code {{
            background-color: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 90%;
        }}
        
        .highlight {{
            background-color: #fff3cd;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #ffc107;
            margin: 15px 0;
        }}
        
        .formula {{
            font-family: 'Cambria Math', 'Times New Roman', serif;
            font-style: italic;
        }}
        
        footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #777;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>

<h1>Assignment 2 - Problem 1 Verification</h1>

<div class="header-info">
    <p><strong>Course:</strong> STP604E - Mechanics of Composite Materials</p>
    <p><strong>Student:</strong> Giray Yıllıkçı</p>
    <p><strong>Date:</strong> {datetime.now().strftime("%B %d, %Y")}</p>
</div>

<div class="success-box">
    <h2>✅ SOLUTION VERIFIED CORRECT</h2>
</div>

<h2>Problem Statement</h2>
<p>Design laminate <strong>[±θ₁/±30°/±θ₂]<sub>s</sub></strong> to minimize |α<sub>x</sub>| with constraint θ₂ &gt; 60°</p>

<h3>Material Properties (Graphite/Epoxy)</h3>
<table>
    <tr><th>Property</th><th>Value</th></tr>
    <tr><td>E₁</td><td>138.0 GPa</td></tr>
    <tr><td>E₂</td><td>8.96 GPa</td></tr>
    <tr><td>G₁₂</td><td>7.10 GPa</td></tr>
    <tr><td>ν₁₂</td><td>0.30</td></tr>
    <tr><td>α₁</td><td>-0.3 × 10⁻⁶/°C</td></tr>
    <tr><td>α₂</td><td>28.1 × 10⁻⁶/°C</td></tr>
    <tr><td>t (ply thickness)</td><td>0.125 mm</td></tr>
</table>

<h2>Claimed Solution</h2>
<table>
    <tr><th>Parameter</th><th>Value</th></tr>
    <tr><td><strong>θ₁</strong></td><td><strong>±8°</strong></td></tr>
    <tr><td><strong>θ₂</strong></td><td><strong>61°</strong></td></tr>
    <tr><td><strong>|α<sub>x</sub>|</strong></td><td><strong>0.4284 × 10⁻⁶/°C</strong></td></tr>
    <tr><td>Stacking Sequence</td><td>[8/-8/30/-30/61/-61/-61/61/-30/30/-8/8]</td></tr>
    <tr><td>Number of Plies</td><td>12</td></tr>
    <tr><td>Total Thickness</td><td>1.500 mm</td></tr>
</table>

<h2>Verification Results</h2>

<h3>Constraint and Optimality Checks</h3>
<table>
    <tr><th>Check</th><th>Result</th></tr>
    <tr><td>θ₁ matches global optimum</td><td class="check-mark">✅ True</td></tr>
    <tr><td>θ₂ matches global optimum</td><td class="check-mark">✅ True</td></tr>
    <tr><td>Constraint θ₂ &gt; 60° satisfied</td><td class="check-mark">✅ True (61° &gt; 60°)</td></tr>
    <tr><td>Balanced laminate (A₁₆ = A₂₆ = 0)</td><td class="check-mark">✅ True</td></tr>
</table>

<h3>A-Matrix (Extensional Stiffness) [GPa·mm]</h3>
<pre>
[A] = [ 119.0679    26.0774     0.0000 ]
      [  26.0774    58.6245     0.0000 ]
      [   0.0000     0.0000    32.6717 ]
</pre>
<p>Note: A₁₆ = A₂₆ = 0 confirms this is a <strong>balanced laminate</strong>.</p>

<h3>Thermal Expansion Coefficients</h3>
<table>
    <tr><th>Coefficient</th><th>Value</th></tr>
    <tr><td>α<sub>x</sub></td><td>0.4284 × 10⁻⁶/°C</td></tr>
    <tr><td>α<sub>y</sub></td><td>4.3446 × 10⁻⁶/°C</td></tr>
    <tr><td>α<sub>xy</sub></td><td>0.0000 × 10⁻⁶/°C</td></tr>
</table>

<h3>Elastic Properties</h3>
<table>
    <tr><th>Property</th><th>Value</th></tr>
    <tr><td>E<sub>x</sub></td><td>71.6 GPa</td></tr>
    <tr><td>E<sub>y</sub></td><td>35.3 GPa</td></tr>
    <tr><td>G<sub>xy</sub></td><td>21.8 GPa</td></tr>
    <tr><td>ν<sub>xy</sub></td><td>0.4448</td></tr>
</table>

<h2>Sensitivity Analysis (θ₁ = 8°)</h2>
<p>Scanning θ₂ values near the optimum confirms θ₂ = 61° is optimal:</p>
<table>
    <tr><th>θ₂</th><th>|α<sub>x</sub>| (× 10⁻⁶/°C)</th></tr>
    <tr style="background-color: #d4edda;"><td><strong>61°</strong></td><td><strong>0.428 ⭐</strong></td></tr>
    <tr><td>62°</td><td>0.493</td></tr>
    <tr><td>63°</td><td>0.555</td></tr>
    <tr><td>65°</td><td>0.671</td></tr>
    <tr><td>70°</td><td>0.911</td></tr>
    <tr><td>75°</td><td>1.089</td></tr>
    <tr><td>80°</td><td>1.210</td></tr>
    <tr><td>85°</td><td>1.280</td></tr>
    <tr><td>90°</td><td>1.303</td></tr>
</table>

<h2>Global Optimality Verification</h2>
<p>A complete scan of all θ₁ ∈ [-90°, 90°] and θ₂ ∈ [61°, 90°] confirmed:</p>
<div class="highlight">
    <strong>Global Optimum Found:</strong><br>
    θ₁ = ±8° (symmetric)<br>
    θ₂ = 61°<br>
    |α<sub>x</sub>| = 0.428369 × 10⁻⁶/°C
</div>

<h2>Physical Interpretation</h2>
<p>The fiber (α₁ = -0.3×10⁻⁶/°C) has <strong>negative thermal expansion</strong>, meaning it contracts when heated. The matrix (α₂ = 28.1×10⁻⁶/°C) has positive expansion.</p>

<p>By carefully balancing fiber angles:</p>
<ul>
    <li>Small θ₁ (8°) contributes near-fiber-direction behavior</li>
    <li>θ₂ = 61° (just above constraint boundary) balances the expansion</li>
    <li>The fixed ±30° plies provide intermediate contribution</li>
</ul>

<p>The result: <strong>α<sub>x</sub> ≈ 0.43×10⁻⁶/°C</strong> (nearly zero thermal expansion!)</p>

<h2>Comparison with Simple Laminates</h2>
<table>
    <tr><th>Laminate</th><th>α<sub>x</sub> (× 10⁻⁶/°C)</th></tr>
    <tr><td>[0°]₁₂</td><td>-0.30</td></tr>
    <tr><td>[90°]₁₂</td><td>28.10</td></tr>
    <tr style="background-color: #d4edda;"><td><strong>[±8/±30/±61]<sub>s</sub></strong></td><td><strong>0.43</strong></td></tr>
</table>

<div class="highlight">
    <strong>Improvement over [90°] laminate: 98.5% reduction in thermal expansion!</strong>
</div>

<h2>Conclusion</h2>
<div class="success-box">
    <p style="font-size: 18px; margin: 0;">The solution θ₁ = ±8°, θ₂ = 61° is <strong>mathematically and physically correct</strong>.</p>
    <p style="margin: 10px 0 0 0;">✅ Global optimum verified through exhaustive search</p>
    <p style="margin: 5px 0 0 0;">✅ All constraints satisfied</p>
    <p style="margin: 5px 0 0 0;">✅ Physical interpretation consistent</p>
</div>

<footer>
    <p>Generated on {datetime.now().strftime("%B %d, %Y at %H:%M")} | STP604E - Assignment 2 Verification</p>
</footer>

</body>
</html>
"""
    return html_content

def find_browser():
    """Find Chrome or Edge executable"""
    import os
    
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

def main():
    import subprocess
    import time
    from pathlib import Path
    
    print("="*60)
    print("Generating Problem 1 Verification PDF")
    print("="*60)
    
    # Generate HTML
    html_content = generate_verification_html()
    
    html_file = Path("assignment_2/PROBLEM1_VERIFICATION.html")
    pdf_file = Path("assignment_2/PROBLEM1_VERIFICATION.pdf")
    
    # Save HTML
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✓ HTML saved: {html_file}")
    
    # Convert to PDF using browser
    browser = find_browser()
    
    if browser:
        print(f"✓ Using browser: {browser}")
        print("  Converting to PDF...")
        
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
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        time.sleep(1)
        
        if pdf_file.exists():
            size = pdf_file.stat().st_size / 1024
            print(f"✓ PDF created: {pdf_file}")
            print(f"  Size: {size:.1f} KB")
            
            # Open the PDF
            os.startfile(str(pdf_file.absolute()))
            print("✓ Opening PDF...")
        else:
            print("✗ PDF creation failed")
    else:
        print("✗ No browser found for PDF generation")
        print("  Please open the HTML file and print to PDF")
    
    print("="*60)

if __name__ == "__main__":
    main()
