"""
Master Assembly & Playwright PDF Compiler for SimuPharm Phase 5 Report
Outputs: SIMUPHARM_PHASE5_PUBLICATION_DISCOVERY_REPORT.pdf
"""
import os
import shutil
from playwright.sync_api import sync_playwright

from part1_sections_1_to_8 import get_part1_html
from part2_sections_9_to_16 import get_part2_html
from part3_sections_17_to_24 import get_part3_html
from part4_sections_25_to_36 import get_part4_html

CSS_STYLING = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

@page {
    size: letter;
    margin: 18mm 16mm 20mm 16mm;
}

* {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #0f172a;
    background-color: #ffffff;
    font-size: 8.5pt;
    line-height: 1.45;
    margin: 0;
    padding: 0;
}

.page {
    page-break-after: always;
    position: relative;
    padding-bottom: 5px;
}

.page:last-child {
    page-break-after: avoid;
}

/* COVER PAGE */
.cover-page {
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 90vh;
    padding: 40px 20px;
}

.cover-badge {
    align-self: flex-start;
    background-color: #0f172a;
    color: #f8fafc;
    font-size: 8.5pt;
    font-weight: 700;
    letter-spacing: 1.5px;
    padding: 5px 12px;
    border-radius: 4px;
    margin-bottom: 25px;
}

.cover-title {
    font-size: 34pt;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #1e3a8a;
    margin: 0 0 8px 0;
    line-height: 1.05;
}

.cover-subtitle {
    font-size: 15pt;
    font-weight: 600;
    color: #0369a1;
    margin: 0 0 20px 0;
    line-height: 1.25;
}

.cover-divider {
    height: 3px;
    width: 90px;
    background: linear-gradient(90deg, #1e3a8a, #0284c7);
    margin-bottom: 25px;
}

.cover-desc {
    font-size: 10pt;
    line-height: 1.5;
    color: #334155;
    max-width: 650px;
    margin-bottom: 35px;
}

.cover-meta-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 16px 20px;
    margin-bottom: 40px;
}

.meta-item {
    display: flex;
    flex-direction: column;
}

.meta-label {
    font-size: 7pt;
    font-weight: 700;
    letter-spacing: 0.8px;
    color: #64748b;
    margin-bottom: 3px;
}

.meta-val {
    font-size: 8.5pt;
    font-weight: 600;
    color: #1e293b;
}

.cover-footer {
    display: flex;
    justify-content: space-between;
    border-top: 1px solid #e2e8f0;
    padding-top: 15px;
    font-size: 8pt;
    color: #64748b;
    font-weight: 500;
}

/* SECTION HEADINGS */
.section-title {
    font-size: 14pt;
    font-weight: 800;
    color: #1e3a8a;
    border-bottom: 1.5px solid #0284c7;
    padding-bottom: 5px;
    margin-top: 0;
    margin-bottom: 12px;
    letter-spacing: -0.2px;
    text-transform: uppercase;
}

.subsection-title {
    font-size: 10.5pt;
    font-weight: 700;
    color: #0f172a;
    margin-top: 14px;
    margin-bottom: 6px;
}

.body-text {
    font-size: 8.5pt;
    line-height: 1.45;
    color: #334155;
    margin-top: 0;
    margin-bottom: 8px;
}

/* TOC STYLING */
.toc-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-top: 10px;
}

.toc-group-title {
    font-size: 8pt;
    font-weight: 800;
    letter-spacing: 0.6px;
    color: #1e3a8a;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 3px;
    margin-top: 10px;
    margin-bottom: 6px;
    text-transform: uppercase;
}

.toc-entry {
    display: flex;
    align-items: baseline;
    font-size: 7.8pt;
    margin-bottom: 4px;
    color: #1e293b;
}

.toc-num {
    font-weight: 700;
    width: 20px;
    color: #0284c7;
}

.toc-text {
    font-weight: 500;
}

.toc-dots {
    flex-grow: 1;
    border-bottom: 1px dotted #94a3b8;
    margin: 0 6px;
}

.toc-p {
    font-weight: 700;
    color: #64748b;
    font-size: 7.5pt;
}

/* TABLES */
.data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 7.5pt;
    line-height: 1.35;
    margin: 10px 0;
    page-break-inside: avoid;
}

.data-table th {
    background-color: #1e3a8a;
    color: #ffffff;
    font-weight: 700;
    text-align: left;
    padding: 5px 6px;
    border: 1px solid #1e3a8a;
}

.data-table td {
    padding: 4.5px 6px;
    border: 1px solid #cbd5e1;
    vertical-align: top;
    color: #1e293b;
}

.data-table tbody tr:nth-child(even) {
    background-color: #f8fafc;
}

/* CALLOUTS & BOXES */
.callout {
    border-radius: 5px;
    padding: 9px 13px;
    margin: 10px 0;
    font-size: 8.2pt;
    line-height: 1.45;
    page-break-inside: avoid;
}

.callout-discovery {
    background-color: #eff6ff;
    border-left: 4px solid #2563eb;
    color: #1e40af;
}

.callout-note {
    background-color: #f8fafc;
    border-left: 4px solid #64748b;
    color: #334155;
}

.callout-warning {
    background-color: #fffbeb;
    border-left: 4px solid #d97706;
    color: #92400e;
}

.callout-success {
    background-color: #f0fdf4;
    border-left: 4px solid #16a34a;
    color: #166534;
}

.quote-box {
    background-color: #f1f5f9;
    border-left: 3px solid #0f172a;
    padding: 10px 15px;
    font-style: italic;
    color: #0f172a;
    font-size: 9.5pt;
    margin: 10px 0;
    font-weight: 500;
}

.rule-box {
    background-color: #f8fafc;
    border: 1.5px solid #0284c7;
    border-radius: 5px;
    padding: 10px 14px;
    font-size: 8.2pt;
    margin: 10px 0;
    color: #0c4a6e;
    line-height: 1.45;
}

.redteam-box {
    background-color: #fef2f2;
    border: 1.5px solid #ef4444;
    border-radius: 5px;
    padding: 10px 14px;
    font-size: 8pt;
    color: #991b1b;
    margin: 8px 0;
    line-height: 1.4;
}

/* BADGES */
.badge {
    display: inline-block;
    padding: 1.5px 6px;
    border-radius: 3px;
    font-size: 6.8pt;
    font-weight: 700;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}

.badge-green { background-color: #dcfce7; color: #15803d; border: 1px solid #86efac; }
.badge-yellow { background-color: #fef3c7; color: #b45309; border: 1px solid #fde68a; }
.badge-red { background-color: #fee2e2; color: #b91c1c; border: 1px solid #fca5a5; }

.badge-observed { background-color: #e2e8f0; color: #334155; }
.badge-lit { background-color: #e0e7ff; color: #3730a3; }
.badge-data { background-color: #d1fae5; color: #065f46; }
.badge-pub { background-color: #ccfbf1; color: #115e59; }
.badge-inf { background-color: #fef3c7; color: #92400e; }
.badge-hyp { background-color: #f3e8ff; color: #6b21a8; }
.badge-future { background-color: #e0f2fe; color: #075985; }

/* CODE & FORMULAS */
.code-span {
    font-family: 'JetBrains Mono', Consolas, monospace;
    background-color: #f1f5f9;
    color: #0f172a;
    padding: 1px 4px;
    border-radius: 3px;
    font-size: 7.5pt;
}

.equation-block {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 3px solid #0284c7;
    border-radius: 4px;
    padding: 7px 12px;
    margin: 8px 0;
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 8pt;
    color: #1e293b;
    page-break-inside: avoid;
}

/* CARDS & GRIDS */
.grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin: 8px 0;
}

.grid-3 {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 8px;
    margin: 8px 0;
}

.card {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 9px 12px;
    page-break-inside: avoid;
}

.card-title {
    font-size: 8.5pt;
    font-weight: 700;
    color: #1e3a8a;
    margin-bottom: 4px;
}

.card-text {
    font-size: 7.8pt;
    color: #334155;
    line-height: 1.35;
    margin: 0;
}

/* LISTS */
.bullet-list, .numbered-list {
    margin: 4px 0 8px 18px;
    padding: 0;
    font-size: 8.2pt;
    line-height: 1.45;
    color: #334155;
}

.bullet-list li, .numbered-list li {
    margin-bottom: 5px;
}

/* FLOW DIAGRAM */
.flow-diagram {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 12px 0;
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 12px 10px;
    page-break-inside: avoid;
}

.flow-step {
    flex: 1;
    background-color: #ffffff;
    border: 1px solid #94a3b8;
    border-radius: 4px;
    padding: 8px 10px;
    margin: 0 4px;
    min-height: 80px;
}

.step-title {
    font-size: 7.5pt;
    font-weight: 700;
    color: #1e3a8a;
    margin-bottom: 3px;
    text-transform: uppercase;
}

.step-desc {
    font-size: 7pt;
    color: #475569;
    line-height: 1.25;
}

.flow-arrow {
    font-size: 14pt;
    font-weight: 800;
    color: #0284c7;
    padding: 0 4px;
}

/* TIMELINE CARDS */
.timeline-container {
    margin: 10px 0;
}

.timeline-card {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #1e3a8a;
    border-radius: 4px;
    padding: 8px 12px;
    margin-bottom: 8px;
    page-break-inside: avoid;
}

.timeline-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 4px;
}

.timeline-phase {
    font-size: 8.5pt;
    font-weight: 700;
    color: #1e3a8a;
}

.timeline-duration {
    font-size: 7.5pt;
    font-weight: 700;
    color: #0284c7;
    background-color: #e0f2fe;
    padding: 1px 6px;
    border-radius: 3px;
}

.timeline-text {
    font-size: 7.8pt;
    color: #334155;
    line-height: 1.35;
    margin: 0;
}
"""

def generate_master_pdf():
    print("--- Assembling HTML from Parts 1, 2, 3, and 4 ---")
    part1 = get_part1_html()
    part2 = get_part2_html()
    part3 = get_part3_html()
    part4 = get_part4_html()

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SIMUPHARM.IO - Phase 5 Master Research Discovery Report</title>
    <style>
        {CSS_STYLING}
    </style>
</head>
<body>
    {part1}
    {part2}
    {part3}
    {part4}
</body>
</html>
"""

    html_path = "PHASE5_REPORT_COMPLETE.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Complete HTML saved to {html_path} ({len(full_html):,} bytes)")

    output_pdf_path = "SIMUPHARM_PHASE5_PUBLICATION_DISCOVERY_REPORT.pdf"
    artifact_dir = r"C:\Users\dsant\.gemini\antigravity\brain\55a75768-f2c0-4fa0-b387-5baedff096a9"
    artifact_pdf_path = os.path.join(artifact_dir, "SIMUPHARM_PHASE5_PUBLICATION_DISCOVERY_REPORT.pdf")

    print("--- Launching Playwright Chromium for High-Density PDF Rendering ---")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Load local HTML file
        abs_html_url = "file:///" + os.path.abspath(html_path).replace("\\\\", "/")
        page.goto(abs_html_url, wait_until="networkidle")
        
        # Render PDF with running headers and footers
        header_template = '''
        <div style="font-family: 'Inter', sans-serif; font-size: 6.5pt; width: 100%; display: flex; justify-content: space-between; padding: 0 16mm; color: #64748b; border-bottom: 0.5px solid #cbd5e1; padding-bottom: 2px;">
            <span>SIMUPHARM.IO — PHASE 5 RESEARCH DISCOVERY & INNOVATION SPRINT</span>
            <span>CONFIDENTIAL SCIENTIFIC STRATEGY</span>
        </div>
        '''
        
        footer_template = '''
        <div style="font-family: 'Inter', sans-serif; font-size: 6.5pt; width: 100%; display: flex; justify-content: space-between; padding: 0 16mm; color: #64748b; border-top: 0.5px solid #cbd5e1; padding-top: 2px;">
            <span>Master Scientific Assessment & Publication Roadmap</span>
            <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
        </div>
        '''

        pdf_bytes = page.pdf(
            path=output_pdf_path,
            format="Letter",
            print_background=True,
            display_header_footer=True,
            header_template=header_template,
            footer_template=footer_template,
            margin={
                "top": "16mm",
                "bottom": "18mm",
                "left": "14mm",
                "right": "14mm"
            }
        )
        browser.close()

    print(f"PDF successfully compiled at: {output_pdf_path}")
    print(f"File size: {os.path.getsize(output_pdf_path):,} bytes")

    # Copy to Artifact directory
    if os.path.exists(artifact_dir):
        shutil.copy2(output_pdf_path, artifact_pdf_path)
        print(f"Artifact successfully mirrored to: {artifact_pdf_path}")

    # Inspect rendered PDF page count via pypdf or PyPDF2 if available
    try:
        import pypdf
        reader = pypdf.PdfReader(output_pdf_path)
        print(f"Total Pages Generated: {len(reader.pages)}")
    except Exception:
        try:
            from pypdf import PdfReader
            reader = PdfReader(output_pdf_path)
            print(f"Total Pages Generated: {len(reader.pages)}")
        except Exception as e:
            print("pypdf not available for page count check:", e)

if __name__ == "__main__":
    generate_master_pdf()
