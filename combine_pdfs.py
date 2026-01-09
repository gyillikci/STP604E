"""
Combine all Assignment 2 problem PDFs into a single document
"""

from pypdf import PdfReader, PdfWriter
from pathlib import Path
import os

def combine_pdfs():
    print("="*60)
    print("Combining Assignment 2 PDFs")
    print("="*60)
    
    # List of PDFs to combine (in order)
    pdf_files = [
        "assignment_2/PROBLEM1_ANALYSIS.pdf",
        "assignment_2/PROBLEM2_ANALYSIS.pdf",
        "assignment_2/PROBLEM3_ANALYSIS.pdf",
        "assignment_2/PROBLEM4_ANALYSIS.pdf",
    ]
    
    # Output file
    output_file = "assignment_2/ASSIGNMENT2_COMPLETE_SOLUTIONS.pdf"
    
    # Create PDF writer
    writer = PdfWriter()
    
    total_pages = 0
    
    for pdf_path in pdf_files:
        if not os.path.exists(pdf_path):
            print(f"✗ File not found: {pdf_path}")
            continue
        
        print(f"Adding: {pdf_path}")
        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)
        
        for page in reader.pages:
            writer.add_page(page)
        
        total_pages += num_pages
        print(f"  → {num_pages} pages added")
    
    # Write combined PDF
    with open(output_file, 'wb') as f:
        writer.write(f)
    
    file_size = os.path.getsize(output_file) / 1024
    
    print()
    print("="*60)
    print(f"✓ Combined PDF created: {output_file}")
    print(f"  Total pages: {total_pages}")
    print(f"  File size: {file_size:.1f} KB")
    print("="*60)
    
    # Open the combined PDF
    os.startfile(os.path.abspath(output_file))
    print("✓ Opening combined PDF...")

if __name__ == "__main__":
    combine_pdfs()
