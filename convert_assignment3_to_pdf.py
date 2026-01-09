"""
Convert ASSIGNMENT3_RESULTS.md to PDF via HTML intermediate
"""

import markdown2
import os
import base64
from datetime import datetime

def get_image_base64(image_path):
    """Convert image to base64 for embedding in HTML"""
    try:
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    except:
        return None

def convert_markdown_to_html():
    """Convert markdown to HTML with embedded images and styling"""

    input_file = "ASSIGNMENT3_RESULTS.md"
    html_output = "ASSIGNMENT3_RESULTS.html"

    print(f"Converting {input_file} to HTML...")

    # Read the markdown file
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Embed images as base64
    image_files = [
        'assignment3_problem1_results.png',
        'assignment3_problem2_results.png',
        'assignment3_problem3_results.png'
    ]

    for img_file in image_files:
        if os.path.exists(img_file):
            b64 = get_image_base64(img_file)
            if b64:
                md_content = md_content.replace(
                    f'![Problem 1 Results]({img_file})',
                    f'<img src="data:image/png;base64,{b64}" alt="Problem 1 Results" style="max-width:100%;">'
                )
                md_content = md_content.replace(
                    f'![Problem 2 Results]({img_file})',
                    f'<img src="data:image/png;base64,{b64}" alt="Problem 2 Results" style="max-width:100%;">'
                )
                md_content = md_content.replace(
                    f'![Problem 3 Results]({img_file})',
                    f'<img src="data:image/png;base64,{b64}" alt="Problem 3 Results" style="max-width:100%;">'
                )

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
    <title>STP 604E - Assignment 3 Results</title>
    <style>
        @media print {{
            @page {{
                size: A4;
                margin: 1.5cm;
            }}
            body {{
                font-size: 10pt;
            }}
            h2 {{
                page-break-before: always;
            }}
            h2:first-of-type {{
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
            font-size: 1.8em;
        }}

        h2 {{
            color: #34495e;
            border-bottom: 2px solid #95a5a6;
            padding-bottom: 8px;
            margin-top: 30px;
            font-size: 1.4em;
        }}

        h3 {{
            color: #555;
            margin-top: 25px;
            font-size: 1.2em;
        }}

        h4 {{
            color: #666;
            margin-top: 20px;
            font-size: 1.1em;
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
            font-size: 0.9em;
        }}

        th {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
            padding: 10px;
            text-align: left;
            border: 1px solid #2980b9;
        }}

        td {{
            padding: 8px;
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

        .formula {{
            font-family: 'Times New Roman', serif;
            font-style: italic;
        }}
    </style>
</head>
<body>
{html_body}

<footer style="margin-top: 60px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #777; font-size: 0.9em;">
    <p>Generated on {datetime.now().strftime('%B %d, %Y')} | STP 604E - Composite Materials Analysis</p>
</footer>
</body>
</html>
"""

    # Write HTML file
    with open(html_output, 'w', encoding='utf-8') as f:
        f.write(html_template)

    print(f"Successfully created {html_output}")
    print(f"File size: {os.path.getsize(html_output) / 1024:.1f} KB")

    return html_output

def convert_html_to_pdf(html_file):
    """Try to convert HTML to PDF using available tools"""

    pdf_output = "STP604E_Fall2025_Assignment3.pdf"

    # Try weasyprint first
    try:
        from weasyprint import HTML
        print(f"Converting {html_file} to PDF using WeasyPrint...")
        HTML(html_file).write_pdf(pdf_output)
        print(f"Successfully created {pdf_output}")
        return True
    except ImportError:
        pass
    except Exception as e:
        print(f"WeasyPrint error: {e}")

    # Try pdfkit/wkhtmltopdf
    try:
        import pdfkit
        print(f"Converting {html_file} to PDF using pdfkit...")
        pdfkit.from_file(html_file, pdf_output)
        print(f"Successfully created {pdf_output}")
        return True
    except ImportError:
        pass
    except Exception as e:
        print(f"pdfkit error: {e}")

    print("\nTo create PDF manually:")
    print("1. Open ASSIGNMENT3_RESULTS.html in a browser")
    print("2. Press Ctrl+P and select 'Save as PDF'")
    print(f"3. Save as {pdf_output}")

    return False

if __name__ == "__main__":
    html_file = convert_markdown_to_html()
    convert_html_to_pdf(html_file)
