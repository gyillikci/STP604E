"""
Final PDF Generator using pdfkit (wkhtmltopdf) for Windows
This is the most reliable method for Windows PDF generation
"""

import os
import sys
import subprocess
from pathlib import Path

def check_wkhtmltopdf():
    """Check if wkhtmltopdf is installed"""
    try:
        result = subprocess.run(['wkhtmltopdf', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ wkhtmltopdf is installed")
            return True
    except FileNotFoundError:
        pass
    
    print("✗ wkhtmltopdf is not installed")
    return False

def install_pdfkit():
    """Install pdfkit library"""
    try:
        import pdfkit
        print("✓ pdfkit already installed")
        return True
    except ImportError:
        print("Installing pdfkit...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pdfkit'])
        print("✓ pdfkit installed")
        return True

def convert_html_to_pdf_with_pdfkit():
    """Convert HTML to PDF using pdfkit"""
    import pdfkit
    
    html_file = "COMPLETE_DOCUMENTATION.html"
    pdf_file = "COMPLETE_DOCUMENTATION.pdf"
    
    if not os.path.exists(html_file):
        print(f"✗ Error: {html_file} not found!")
        print("Please run generate_pdf_simple.py first")
        return False
    
    print(f"Converting {html_file} to PDF...")
    
    # PDF options for better output
    options = {
        'page-size': 'A4',
        'margin-top': '20mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '20mm',
        'encoding': 'UTF-8',
        'enable-local-file-access': None,
        'print-media-type': None,
        'no-outline': None
    }
    
    try:
        pdfkit.from_file(html_file, pdf_file, options=options)
        
        file_size = os.path.getsize(pdf_file) / (1024 * 1024)
        print(f"✓ PDF created successfully: {pdf_file}")
        print(f"  File size: {file_size:.2f} MB")
        return True
    except Exception as e:
        print(f"✗ Error creating PDF: {e}")
        return False

def print_instructions():
    """Print installation and usage instructions"""
    print("\n" + "="*70)
    print("TO GENERATE PDF - CHOOSE ONE METHOD:")
    print("="*70)
    
    print("\n" + "Option 1: Browser Print (EASIEST - Recommended)".upper())
    print("-" * 70)
    print("1. The HTML file is now open in your browser")
    print("2. Press Ctrl+P (or Cmd+P on Mac)")
    print("3. Select 'Save as PDF' or 'Microsoft Print to PDF'")
    print("4. Configure settings:")
    print("   - Paper size: A4")
    print("   - Margins: Default (or 20mm)")
    print("   - Enable 'Background graphics'")
    print("5. Save as: COMPLETE_DOCUMENTATION.pdf")
    print()
    print("✓ This method produces the best quality PDF with all formatting!")
    
    print("\n" + "Option 2: Install wkhtmltopdf (Automated)".upper())
    print("-" * 70)
    print("1. Download wkhtmltopdf from:")
    print("   https://wkhtmltopdf.org/downloads.html")
    print("2. Install wkhtmltopdf (add to PATH during installation)")
    print("3. Run this script again:")
    print("   python create_final_pdf.py")
    
    print("\n" + "Option 3: Microsoft Word (Alternative)".upper())
    print("-" * 70)
    print("1. Open COMPLETE_DOCUMENTATION.html in Microsoft Word")
    print("2. File -> Save As -> PDF")
    
    print("\n" + "Option 4: Python automation with selenium (Advanced)".upper())
    print("-" * 70)
    print("Requires Chrome/Edge and chromedriver")
    print()

def main():
    """Main function"""
    print("="*70)
    print("STP604E - Final PDF Generator")
    print("="*70)
    print()
    
    # Check if HTML file exists
    html_file = "COMPLETE_DOCUMENTATION.html"
    if not os.path.exists(html_file):
        print(f"✗ {html_file} not found!")
        print("\nGenerating HTML file first...")
        subprocess.run([sys.executable, 'generate_pdf_simple.py'])
        print()
    
    # Try wkhtmltopdf method
    has_wkhtmltopdf = check_wkhtmltopdf()
    
    if has_wkhtmltopdf:
        install_pdfkit()
        success = convert_html_to_pdf_with_pdfkit()
        
        if success:
            print("\n" + "="*70)
            print("✓ PDF GENERATED SUCCESSFULLY!")
            print("="*70)
            print(f"\nOutput file: {os.path.abspath('COMPLETE_DOCUMENTATION.pdf')}")
            
            # Try to open the PDF
            try:
                os.startfile('COMPLETE_DOCUMENTATION.pdf')
                print("\n✓ Opening PDF...")
            except:
                pass
            return
    
    # If wkhtmltopdf not available, open HTML and show instructions
    print_instructions()
    
    # Open HTML in browser
    try:
        import webbrowser
        webbrowser.open(os.path.abspath(html_file))
        print(f"\n✓ Opened {html_file} in your browser")
        print("  Follow the instructions above to save as PDF")
    except Exception as e:
        print(f"\n✗ Could not open browser: {e}")
        print(f"  Please manually open: {os.path.abspath(html_file)}")

if __name__ == "__main__":
    main()
