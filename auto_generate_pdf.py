"""
Auto-generate PDF using Chrome/Edge headless mode
This script automates the browser print-to-PDF process
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def find_chrome_or_edge():
    """Find Chrome or Edge executable on Windows"""
    
    # Common Chrome locations
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
    ]
    
    # Common Edge locations
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    
    # Check Chrome first
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✓ Found Google Chrome: {path}")
            return path, "Chrome"
    
    # Check Edge
    for path in edge_paths:
        if os.path.exists(path):
            print(f"✓ Found Microsoft Edge: {path}")
            return path, "Edge"
    
    return None, None

def generate_pdf_with_browser(browser_path, browser_name):
    """Generate PDF using browser headless mode"""
    
    html_file = Path("COMPLETE_DOCUMENTATION.html").absolute()
    pdf_file = Path("COMPLETE_DOCUMENTATION.pdf").absolute()
    
    if not html_file.exists():
        print(f"✗ Error: {html_file} not found!")
        return False
    
    print(f"\nGenerating PDF using {browser_name} (headless mode)...")
    print(f"Input:  {html_file}")
    print(f"Output: {pdf_file}")
    print()
    
    # Chrome/Edge command line arguments for PDF generation
    cmd = [
        browser_path,
        '--headless',
        '--disable-gpu',
        '--no-sandbox',
        '--print-to-pdf=' + str(pdf_file),
        '--print-to-pdf-no-header',
        '--no-pdf-header-footer',
        str(html_file)
    ]
    
    try:
        print("Processing...")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Wait a moment for file to be written
        time.sleep(1)
        
        if pdf_file.exists():
            file_size = pdf_file.stat().st_size / (1024 * 1024)
            print(f"\n✓ PDF generated successfully!")
            print(f"  File: {pdf_file}")
            print(f"  Size: {file_size:.2f} MB")
            return True
        else:
            print(f"\n✗ PDF file was not created")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("\n✗ Browser process timed out")
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False

def main():
    """Main function"""
    print("="*70)
    print("STP604E - Automated PDF Generator (Chrome/Edge)")
    print("="*70)
    print()
    
    # Check if HTML exists
    if not os.path.exists("COMPLETE_DOCUMENTATION.html"):
        print("HTML file not found. Generating...")
        subprocess.run([sys.executable, 'generate_pdf_simple.py'])
        print()
    
    # Find browser
    browser_path, browser_name = find_chrome_or_edge()
    
    if not browser_path:
        print("✗ Neither Chrome nor Edge found!")
        print("\nPlease install Google Chrome or Microsoft Edge")
        print("Or use the manual method:")
        print("  1. Open COMPLETE_DOCUMENTATION.html in any browser")
        print("  2. Press Ctrl+P")
        print("  3. Save as PDF")
        return
    
    # Generate PDF
    success = generate_pdf_with_browser(browser_path, browser_name)
    
    if success:
        print("\n" + "="*70)
        print("✓ SUCCESS!")
        print("="*70)
        
        # Try to open the PDF
        pdf_path = Path("COMPLETE_DOCUMENTATION.pdf").absolute()
        try:
            os.startfile(str(pdf_path))
            print(f"\n✓ Opening PDF: {pdf_path}")
        except:
            print(f"\nPDF location: {pdf_path}")
    else:
        print("\n" + "="*70)
        print("Manual Method (Always Works):")
        print("="*70)
        print("1. Open COMPLETE_DOCUMENTATION.html in browser")
        print("2. Press Ctrl+P (Print)")
        print("3. Select 'Save as PDF'")
        print("4. Save as: COMPLETE_DOCUMENTATION.pdf")

if __name__ == "__main__":
    main()
