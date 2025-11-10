"""
Convert ASSIGNMENT_RESULTS.md to PDF via HTML intermediate
Uses markdown2 to convert MD -> HTML, then browser print or alternative PDF generator
"""

import markdown2
import os

def convert_markdown_to_html():
    """Convert markdown to HTML with embedded images and styling"""
    
    input_file = "ASSIGNMENT_RESULTS.md"
    html_output = "ASSIGNMENT_RESULTS.html"
    
    print(f"Converting {input_file} to HTML...")
    
    # Read the markdown file
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML with extras
    html_body = markdown2.markdown(
        md_content,
        extras=[
            'fenced-code-blocks',
            'tables',
            'break-on-newline',
            'header-ids',
            'toc'
        ]
    )
    
    # Create full HTML document with styling
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>STP 604E - Assignment 1 Results</title>
    <style>
        @media print {{
            @page {{
                size: A4;
                margin: 2cm;
            }}
            body {{
                font-size: 10pt;
            }}
            h1 {{
                page-break-before: always;
            }}
            h1:first-of-type {{
                page-break-before: avoid;
            }}
            table, img, pre {{
                page-break-inside: avoid;
            }}
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #ffffff;
            color: #333;
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 40px;
        }}
        
        h2 {{
            color: #34495e;
            border-bottom: 2px solid #95a5a6;
            padding-bottom: 8px;
            margin-top: 30px;
        }}
        
        h3 {{
            color: #555;
            margin-top: 25px;
        }}
        
        h4 {{
            color: #666;
            margin-top: 20px;
        }}
        
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.9em;
        }}
        
        pre {{
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            overflow-x: auto;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.85em;
            line-height: 1.4;
        }}
        
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        th {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
            padding: 12px;
            text-align: left;
            border: 1px solid #2980b9;
        }}
        
        td {{
            padding: 10px;
            border: 1px solid #ddd;
        }}
        
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        tr:hover {{
            background-color: #f0f0f0;
        }}
        
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px auto;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        hr {{
            border: none;
            border-top: 2px solid #3498db;
            margin: 40px 0;
        }}
        
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        ul, ol {{
            margin: 15px 0;
            padding-left: 30px;
        }}
        
        li {{
            margin: 8px 0;
        }}
        
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 20px;
            margin: 20px 0;
            color: #666;
            font-style: italic;
        }}
        
        .toc {{
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 20px;
            margin: 30px 0;
        }}
        
        .toc h2 {{
            margin-top: 0;
            border: none;
        }}
    </style>
</head>
<body>
{html_body}

<footer style="margin-top: 60px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #777; font-size: 0.9em;">
    <p>Generated on November 10, 2025 | STP 604E - Composite Materials</p>
</footer>
</body>
</html>
"""
    
    # Write HTML file
    with open(html_output, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"✓ Successfully created {html_output}")
    print(f"  File size: {os.path.getsize(html_output) / 1024:.1f} KB")
    
    print("\n" + "="*70)
    print("TO CREATE PDF:")
    print("="*70)
    print("\nOption 1: Browser (Recommended)")
    print("  1. Open ASSIGNMENT_RESULTS.html in your browser")
    print("  2. Press Ctrl+P (Print)")
    print("  3. Select 'Save as PDF' or 'Microsoft Print to PDF'")
    print("  4. Save as ASSIGNMENT_RESULTS.pdf")
    
    print("\nOption 2: VS Code")
    print("  1. Install 'Markdown PDF' extension")
    print("  2. Right-click ASSIGNMENT_RESULTS.md")
    print("  3. Select 'Markdown PDF: Export (pdf)'")
    
    print("\nOption 3: Command Line (requires wkhtmltopdf)")
    print("  pip install pdfkit")
    print("  Download wkhtmltopdf from https://wkhtmltopdf.org/downloads.html")
    
    # Try to open the HTML file in default browser
    try:
        import webbrowser
        webbrowser.open(os.path.abspath(html_output))
        print(f"\n✓ Opening {html_output} in your default browser...")
    except:
        print(f"\n→ Please manually open: {os.path.abspath(html_output)}")

if __name__ == "__main__":
    convert_markdown_to_html()
