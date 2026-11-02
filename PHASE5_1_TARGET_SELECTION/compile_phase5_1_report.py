"""
Master Compiler for SimuPharm Phase 5.1 Report:
Outputs: SIMUPHARM_PHASE5_1_PUBLICATION_TARGET_SELECTION_REPORT.pdf
"""
import os
import shutil
from playwright.sync_api import sync_playwright

from part1_prelims_and_inventory import get_part1_html
from part2_candidate_directions import get_part2_html
from part3_evidence_and_methodology import get_part3_html
from part4_rankings_roadmap_decision import get_part4_html
from part5_appendices_and_decision_card import get_part5_html

CSS_STYLING = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

@page {
    size: letter;
    margin: 16mm 15mm 18mm 15mm;
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
    font-size: 8.2pt;
    line-height: 1.42;
    margin: 0;
    padding: 0;
}

.page {
    page-break-after: always;
    position: relative;
    padding-bottom: 4px;
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
    padding: 35px 20px;
}

.cover-badge {
    align-self: flex-start;
    background-color: #0f172a;
    color: #f8fafc;
    font-size: 8pt;
    font-weight: 700;
    letter-spacing: 1.5px;
    padding: 4px 12px;
    border-radius: 4px;
    margin-bottom: 22px;
}

.cover-title {
    font-size: 32pt;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #1e3a8a;
    margin: 0 0 6px 0;
    line-height: 1.05;
}

.cover-subtitle {
    font-size: 14pt;
    font-weight: 600;
    color: #0369a1;
    margin: 0 0 18px 0;
    line-height: 1.25;
}

.cover-divider {
    height: 3px;
    width: 80px;
    background: linear-gradient(90deg, #1e3a8a, #0284c7);
    margin-bottom: 22px;
}

.cover-desc {
    font-size: 9.5pt;
    line-height: 1.5;
    color: #334155;
    max-width: 650px;
    margin-bottom: 30px;
}

.cover-meta-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 14px 18px;
    margin-bottom: 35px;
}

.meta-item {
    display: flex;
    flex-direction: column;
}

.meta-label {
    font-size: 6.8pt;
    font-weight: 700;
    letter-spacing: 0.8px;
    color: #64748b;
    margin-bottom: 2px;
}

.meta-val {
    font-size: 8.2pt;
    font-weight: 600;
    color: #1e293b;
}

.cover-footer {
    display: flex;
    justify-content: space-between;
    border-top: 1px solid #e2e8f0;
    padding-top: 12px;
    font-size: 7.8pt;
    color: #64748b;
    font-weight: 500;
}

/* SECTION HEADINGS */
.section-title {
    font-size: 13.5pt;
    font-weight: 800;
    color: #1e3a8a;
    border-bottom: 1.5px solid #0284c7;
    padding-bottom: 4px;
    margin-top: 0;
    margin-bottom: 10px;
    letter-spacing: -0.2px;
    text-transform: uppercase;
}

.subsection-title {
    font-size: 10pt;
    font-weight: 700;
    color: #0f172a;
    margin-top: 12px;
    margin-bottom: 5px;
}

.body-text {
    font-size: 8.2pt;
    line-height: 1.42;
    color: #334155;
    margin-top: 0;
    margin-bottom: 7px;
}

/* TOC STYLING */
.toc-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-top: 8px;
}

.toc-group-title {
    font-size: 7.5pt;
    font-weight: 800;
    letter-spacing: 0.6px;
    color: #1e3a8a;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 2px;
    margin-top: 8px;
    margin-bottom: 5px;
    text-transform: uppercase;
}

.toc-entry {
    display: flex;
    align-items: baseline;
    font-size: 7.5pt;
    margin-bottom: 3.5px;
    color: #1e293b;
}

.toc-num {
    font-weight: 700;
    width: 22px;
    color: #0284c7;
}

.toc-text {
    font-weight: 500;
}

.toc-dots {
    flex-grow: 1;
    border-bottom: 1px dotted #94a3b8;
    margin: 0 5px;
}

.toc-p {
    font-weight: 700;
    color: #64748b;
    font-size: 7.2pt;
}

/* TABLES */
.data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 7.2pt;
    line-height: 1.32;
    margin: 8px 0;
    page-break-inside: avoid;
}

.data-table th {
    background-color: #1e3a8a;
    color: #ffffff;
    font-weight: 700;
    text-align: left;
    padding: 4.5px 5.5px;
    border: 1px solid #1e3a8a;
}

.data-table td {
    padding: 4px 5.5px;
    border: 1px solid #cbd5e1;
    vertical-align: top;
    color: #1e293b;
}

.data-table tbody tr:nth-child(even) {
    background-color: #f8fafc;
}

/* CALLOUTS & BOXES */
.callout {
    border-radius: 4px;
    padding: 8px 12px;
    margin: 8px 0;
    font-size: 8pt;
    line-height: 1.4;
    page-break-inside: avoid;
}

.callout-discovery {
    background-color: #eff6ff;
    border-left: 3.5px solid #2563eb;
    color: #1e40af;
}

.callout-note {
    background-color: #f8fafc;
    border-left: 3.5px solid #64748b;
    color: #334155;
}

.callout-warning {
    background-color: #fffbeb;
    border-left: 3.5px solid #d97706;
    color: #92400e;
}

.callout-success {
    background-color: #f0fdf4;
    border-left: 3.5px solid #16a34a;
    color: #166534;
}

.rule-box {
    background-color: #f8fafc;
    border: 1.5px solid #0284c7;
    border-radius: 4px;
    padding: 8px 12px;
    font-size: 7.8pt;
    margin: 8px 0;
    color: #0c4a6e;
    line-height: 1.4;
}

.redteam-box {
    background-color: #fef2f2;
    border: 1.5px solid #ef4444;
    border-radius: 4px;
    padding: 8px 12px;
    font-size: 7.8pt;
    color: #991b1b;
    margin: 7px 0;
    line-height: 1.38;
}

/* BADGES */
.badge {
    display: inline-block;
    padding: 1px 5px;
    border-radius: 3px;
    font-size: 6.5pt;
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
    font-size: 7.2pt;
}

.equation-block {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 3px solid #0284c7;
    border-radius: 4px;
    padding: 6px 10px;
    margin: 7px 0;
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 7.8pt;
    color: #1e293b;
    page-break-inside: avoid;
}

/* CARDS & GRIDS */
.grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 9px;
    margin: 7px 0;
}

.grid-3 {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 7px;
    margin: 7px 0;
}

.card {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 8px 10px;
    page-break-inside: avoid;
}

.card-title {
    font-size: 8.2pt;
    font-weight: 700;
    color: #1e3a8a;
    margin-bottom: 3px;
}

.card-text {
    font-size: 7.5pt;
    color: #334155;
    line-height: 1.32;
    margin: 0;
}

/* LISTS */
.bullet-list, .numbered-list {
    margin: 3px 0 7px 16px;
    padding: 0;
    font-size: 7.9pt;
    line-height: 1.4;
    color: #334155;
}

.bullet-list li, .numbered-list li {
    margin-bottom: 4px;
}

/* FLOW DIAGRAM */
.flow-diagram {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 9px 0;
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 9px 8px;
    page-break-inside: avoid;
}

.flow-step {
    flex: 1;
    background-color: #ffffff;
    border: 1px solid #94a3b8;
    border-radius: 4px;
    padding: 6px 8px;
    margin: 0 3px;
    min-height: 65px;
}

.step-title {
    font-size: 7.2pt;
    font-weight: 700;
    color: #1e3a8a;
    margin-bottom: 2px;
    text-transform: uppercase;
}

.step-desc {
    font-size: 6.8pt;
    color: #475569;
    line-height: 1.22;
}

.flow-arrow {
    font-size: 13pt;
    font-weight: 800;
    color: #0284c7;
    padding: 0 3px;
}

/* TIMELINE CARDS */
.timeline-container {
    margin: 8px 0;
}

.timeline-card {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-left: 3.5px solid #1e3a8a;
    border-radius: 4px;
    padding: 7px 10px;
    margin-bottom: 6px;
    page-break-inside: avoid;
}

.timeline-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 3px;
}

.timeline-phase {
    font-size: 8pt;
    font-weight: 700;
    color: #1e3a8a;
}

.timeline-duration {
    font-size: 7pt;
    font-weight: 700;
    color: #0284c7;
    background-color: #e0f2fe;
    padding: 1px 5px;
    border-radius: 3px;
}

.timeline-text {
    font-size: 7.5pt;
    color: #334155;
    line-height: 1.32;
    margin: 0;
}
"""

def generate_phase5_1_pdf():
    print("--- Assembling HTML for Phase 5.1 from Parts 1 to 5 ---")
    p1 = get_part1_html()
    p2 = get_part2_html()
    p3 = get_part3_html()
    p4 = get_part4_html()
    p5 = get_part5_html()

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SIMUPHARM.IO - Phase 5.1 Publication Target Selection Report</title>
    <style>
        {CSS_STYLING}
    </style>
</head>
<body>
    {p1}
    {p2}
    {p3}
    {p4}
    {p5}
</body>
</html>
"""

    html_file = "PHASE5_1_REPORT_COMPLETE.html"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Complete HTML saved to {html_file} ({len(full_html):,} bytes)")

    out_pdf_local = "SIMUPHARM_PHASE5_1_PUBLICATION_TARGET_SELECTION_REPORT.pdf"
    out_pdf_root = os.path.join("..", out_pdf_local)
    artifact_dir = r"C:\Users\dsant\.gemini\antigravity\brain\55a75768-f2c0-4fa0-b387-5baedff096a9"
    out_pdf_artifact = os.path.join(artifact_dir, out_pdf_local)

    print("--- Launching Playwright Chromium for Master PDF Compilation ---")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        abs_html = "file:///" + os.path.abspath(html_file).replace("\\\\", "/")
        page.goto(abs_html, wait_until="networkidle")

        header_template = '''
        <div style="font-family: 'Inter', sans-serif; font-size: 6.2pt; width: 100%; display: flex; justify-content: space-between; padding: 0 15mm; color: #64748b; border-bottom: 0.5px solid #cbd5e1; padding-bottom: 2px;">
            <span>SIMUPHARM.IO — PHASE 5.1 PUBLICATION TARGET SELECTION & EVIDENCE SPRINT</span>
            <span>STRICT INTERNAL DECISION REPORT</span>
        </div>
        '''

        footer_template = '''
        <div style="font-family: 'Inter', sans-serif; font-size: 6.2pt; width: 100%; display: flex; justify-content: space-between; padding: 0 15mm; color: #64748b; border-top: 0.5px solid #cbd5e1; padding-top: 2px;">
            <span>SimuPharm Scientific Strategy Directive — Confidential</span>
            <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
        </div>
        '''

        page.pdf(
            path=out_pdf_local,
            format="Letter",
            print_background=True,
            display_header_footer=True,
            header_template=header_template,
            footer_template=footer_template,
            margin={
                "top": "15mm",
                "bottom": "17mm",
                "left": "13mm",
                "right": "13mm"
            }
        )
        browser.close()

    print(f"PDF generated locally at: {out_pdf_local} ({os.path.getsize(out_pdf_local):,} bytes)")

    # Copy to project root
    shutil.copy2(out_pdf_local, out_pdf_root)
    print(f"Copied to project root: {out_pdf_root}")

    # Copy to artifact directory
    if os.path.exists(artifact_dir):
        shutil.copy2(out_pdf_local, out_pdf_artifact)
        print(f"Copied to artifact directory: {out_pdf_artifact}")

    # Inspect page count
    try:
        import pypdf
        reader = pypdf.PdfReader(out_pdf_local)
        print(f"TOTAL PAGES IN REPORT: {len(reader.pages)}")
    except Exception as e:
        print("Page count check error:", e)

if __name__ == "__main__":
    generate_phase5_1_pdf()
