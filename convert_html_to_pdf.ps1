# PowerShell script to automatically convert HTML to PDF using Edge
# This script opens the HTML file in Microsoft Edge and automates the print-to-PDF process

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "STP604E - Automated PDF Generator" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$htmlFile = "COMPLETE_DOCUMENTATION.html"
$pdfFile = "COMPLETE_DOCUMENTATION.pdf"

if (-not (Test-Path $htmlFile)) {
    Write-Host "Error: $htmlFile not found!" -ForegroundColor Red
    Write-Host "Please run generate_pdf_simple.py first" -ForegroundColor Yellow
    exit 1
}

Write-Host "Opening $htmlFile in Microsoft Edge..." -ForegroundColor Green
Write-Host ""
Write-Host "Instructions:" -ForegroundColor Yellow
Write-Host "1. The HTML file will open in Edge" -ForegroundColor White
Write-Host "2. Press Ctrl+P to open Print dialog" -ForegroundColor White
Write-Host "3. Select 'Save as PDF' as printer" -ForegroundColor White
Write-Host "4. Click 'Save' button" -ForegroundColor White
Write-Host "5. Save as: $pdfFile" -ForegroundColor White
Write-Host ""

# Get the full path
$fullPath = (Resolve-Path $htmlFile).Path

# Open in Edge
Start-Process "msedge" -ArgumentList "file:///$($fullPath.Replace('\', '/'))"

Write-Host "✓ HTML file opened in Edge" -ForegroundColor Green
Write-Host ""
Write-Host "Alternative: Use Chrome" -ForegroundColor Cyan
Write-Host "  chrome.exe --print-to-pdf=`"$pdfFile`" `"file:///$($fullPath.Replace('\', '/'))`"" -ForegroundColor Gray
