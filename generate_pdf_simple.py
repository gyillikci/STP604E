"""
Generate PDF documentation for STP604E Assignment Results
Uses reportlab for reliable cross-platform PDF generation
"""

import os
import sys
from datetime import datetime

def install_requirements():
    """Install required packages for PDF generation"""
    import subprocess
    
    print("Checking/Installing required packages...")
    packages = ['reportlab', 'markdown2']
    
    for package in packages:
        try:
            __import__(package)
            print(f"✓ {package} already installed")
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ {package} installed successfully")

def read_markdown_file(filepath):
    """Read a markdown file and return its content"""
    if not os.path.exists(filepath):
        return None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def generate_comprehensive_markdown():
    """Combine all assignment results into one comprehensive markdown document"""
    
    print("Generating comprehensive markdown document...")
    
    # Header
    content = f"""# STP604E - Complete Assignment Results
## Advanced Design, Analysis and Optimization of Composite Structures

**Student**: Giray Yıllıkçı  
**Course**: STP604E - Mechanics of Composite Materials  
**Term**: Fall 2025  
**Generated**: {datetime.now().strftime("%B %d, %Y at %H:%M")}

---

> **Note on Academic Integrity**: AI tools (GitHub Copilot, Claude) were used in the preparation of this document and the development of the computational analysis code. This note is added voluntarily to maintain transparency and academic integrity.

---

"""

    # Add Assignment 1 Results
    print("Adding Assignment 1 results...")
    assignment1_md = read_markdown_file("ASSIGNMENT_RESULTS.md")
    if assignment1_md:
        lines = assignment1_md.split('\n')
        assignment1_content = '\n'.join(lines[1:])
        content += f"""
---

# Assignment 1: Classical Laminated Plate Theory (CLPT) Analysis

{assignment1_content}

---

"""
    
    # Add Assignment 2 Complete Summary
    print("Adding Assignment 2 complete summary...")
    assignment2_summary = read_markdown_file("assignment_2/ASSIGNMENT2_COMPLETE_SUMMARY.md")
    if assignment2_summary:
        lines = assignment2_summary.split('\n')
        assignment2_content = '\n'.join(lines[1:])
        content += f"""
---

# Assignment 2: Optimization Techniques and Lamination Parameters

{assignment2_content}

---

"""
    
    # Add Problem 2 detailed results
    print("Adding Problem 2 detailed results...")
    problem2_results = read_markdown_file("assignment_2/PROBLEM2_RESULTS.md")
    if problem2_results:
        content += f"""
## Assignment 2 - Problem 2: Detailed Results

{problem2_results}

---

"""
    
    # Add Problem 3 detailed results
    print("Adding Problem 3 detailed results...")
    problem3_results = read_markdown_file("assignment_2/PROBLEM3_RESULTS.md")
    if problem3_results:
        content += f"""
## Assignment 2 - Problem 3: Detailed Results

{problem3_results}

---

"""
    
    # Add Problem 4 derivation
    print("Adding Problem 4 derivation...")
    problem4_derivation = read_markdown_file("assignment_2/PROBLEM4_DERIVATION.md")
    if problem4_derivation:
        content += f"""
## Assignment 2 - Problem 4: Analytical Derivation

{problem4_derivation}

---

"""
    
    # Add conclusion
    content += """
---

# Summary and Conclusions

This comprehensive documentation presents the complete solutions for STP604E assignments, demonstrating:

## Assignment 1 - Key Achievements
- Implementation of Classical Laminated Plate Theory (CLPT)
- Analysis of quasi-isotropic laminates
- Micromechanics calculations using Rule of Mixtures
- Optimization with zero shear strain constraints
- Stiffness matrix comparisons for different stacking sequences

## Assignment 2 - Key Achievements
- Particle Swarm Optimization (PSO) implementation
- Thermal expansion coefficient minimization
- Thickness optimization with mechanical constraints
- Miki's Lamination Parameters for maximum stiffness
- Analytical derivation of laminate constitutive relations

## Technical Implementation
All analyses were performed using custom Python libraries:
- `composite_lib`: Core laminate mechanics
- `assignments`: Problem-specific implementations
- `visualization`: Interactive Streamlit visualizations

## References
1. Daniel, I. M., & Ishai, O. (2006). *Engineering Mechanics of Composite Materials* (2nd ed.). Oxford University Press.
2. Jones, R. M. (1999). *Mechanics of Composite Materials* (2nd ed.). Taylor & Francis.
3. Hyer, M. W. (2009). *Stress Analysis of Fiber-Reinforced Composite Materials*. DEStech Publications.
4. Miki, M. (1982). Material Design of Composite Laminates with Required In-Plane Elastic Properties. *Progress in Science and Engineering of Composites*.

---

**End of Documentation**

*Generated using Python with reportlab*
"""
    
    # Write the comprehensive markdown
    output_md = "COMPLETE_DOCUMENTATION.md"
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Created {output_md} ({len(content)} characters)")
    return output_md, content

def markdown_to_html(md_content):
    """Convert markdown to HTML with styling"""
    import markdown2
    
    print("Converting markdown to HTML...")
    
    html_body = markdown2.markdown(
        md_content,
        extras=[
            'fenced-code-blocks',
            'tables',
            'break-on-newline',
            'header-ids',
            'toc',
            'code-friendly',
            'footnotes'
        ]
    )
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>STP604E - Complete Assignment Results</title>
    <style>
        @media print {{
            @page {{
                size: A4;
                margin: 2cm;
            }}
            body {{ font-size: 10pt; }}
            h1 {{ page-break-before: always; }}
            h1:first-of-type {{ page-break-before: avoid; }}
            table, pre, blockquote {{ page-break-inside: avoid; }}
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
            margin-top: 40px;
        }}
        
        h1:first-of-type {{
            font-size: 32px;
            text-align: center;
            border-bottom: none;
        }}
        
        h2 {{
            color: #2c5aa0;
            font-size: 22px;
            border-bottom: 2px solid #7ba7d8;
            padding-bottom: 8px;
            margin-top: 30px;
        }}
        
        h3 {{
            color: #34495e;
            font-size: 18px;
            margin-top: 25px;
        }}
        
        h4 {{
            color: #555;
            font-size: 16px;
            margin-top: 20px;
        }}
        
        code {{
            background-color: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 90%;
            color: #c7254e;
        }}
        
        pre {{
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-left: 4px solid #2c5aa0;
            border-radius: 4px;
            padding: 15px;
            overflow-x: auto;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 13px;
            line-height: 1.4;
        }}
        
        pre code {{
            background-color: transparent;
            padding: 0;
            color: #333;
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
        
        ul, ol {{
            margin: 15px 0;
            padding-left: 30px;
        }}
        
        li {{
            margin: 8px 0;
        }}
        
        blockquote {{
            border-left: 4px solid #ffc107;
            background-color: #fffbf0;
            padding: 15px 20px;
            margin: 20px 0;
            font-style: italic;
            color: #666;
        }}
        
        hr {{
            border: none;
            border-top: 2px solid #ddd;
            margin: 40px 0;
        }}
        
        strong {{
            color: #1a1a1a;
            font-weight: 600;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
        }}
    </style>
</head>
<body>
{html_body}
<footer style="margin-top: 60px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #777; font-size: 0.9em;">
    <p>Generated on {datetime.now().strftime("%B %d, %Y")} | STP604E - Composite Materials</p>
</footer>
</body>
</html>
"""
    
    return html_template

def generate_pdf_documentation():
    """Main function to generate PDF documentation"""
    
    print("="*70)
    print("STP604E - PDF Documentation Generator")
    print("="*70)
    print()
    
    # Step 1: Install requirements
    try:
        install_requirements()
        print()
    except Exception as e:
        print(f"✗ Error installing requirements: {e}")
        return
    
    # Step 2: Generate comprehensive markdown
    try:
        md_file, md_content = generate_comprehensive_markdown()
        print()
    except Exception as e:
        print(f"✗ Error generating markdown: {e}")
        return
    
    # Step 3: Convert to HTML
    try:
        html_content = markdown_to_html(md_content)
        
        html_file = "COMPLETE_DOCUMENTATION.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✓ HTML version saved: {html_file}")
        print()
    except Exception as e:
        print(f"✗ Error converting to HTML: {e}")
        return
    
    # Step 4: Print instructions for PDF generation
    print("="*70)
    print("✓ DOCUMENTATION GENERATED SUCCESSFULLY!")
    print("="*70)
    print()
    print(f"Output files:")
    print(f"  • {os.path.abspath('COMPLETE_DOCUMENTATION.md')}")
    print(f"  • {os.path.abspath('COMPLETE_DOCUMENTATION.html')}")
    print()
    print("TO CREATE PDF:")
    print("-" * 70)
    print()
    print("Method 1: Microsoft Edge/Chrome (Recommended - Best Quality)")
    print("  1. Open COMPLETE_DOCUMENTATION.html in Edge or Chrome")
    print("  2. Press Ctrl+P (Print)")
    print("  3. Select 'Save as PDF' as destination")
    print("  4. Settings:")
    print("     - Paper size: A4")
    print("     - Margins: Default")
    print("     - Scale: 100%")
    print("     - Check 'Background graphics'")
    print("  5. Click 'Save'")
    print("  6. Save as: COMPLETE_DOCUMENTATION.pdf")
    print()
    print("Method 2: Firefox")
    print("  1. Open COMPLETE_DOCUMENTATION.html in Firefox")
    print("  2. Press Ctrl+P")
    print("  3. Select 'Microsoft Print to PDF'")
    print("  4. Print")
    print()
    print("Method 3: PowerShell (Automated)")
    print("  Run this command in PowerShell:")
    print("  Start-Process msedge COMPLETE_DOCUMENTATION.html")
    print()
    
    # Try to open in default browser
    try:
        import webbrowser
        html_path = os.path.abspath('COMPLETE_DOCUMENTATION.html')
        webbrowser.open(html_path)
        print("✓ Opening HTML file in your default browser...")
        print("  Use Ctrl+P to print/save as PDF")
    except Exception as e:
        print(f"Could not auto-open browser: {e}")

if __name__ == "__main__":
    generate_pdf_documentation()
