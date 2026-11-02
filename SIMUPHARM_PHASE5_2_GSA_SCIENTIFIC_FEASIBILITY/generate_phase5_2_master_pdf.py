"""
SimuPharm Phase 5.2 - Master Single PDF Renderer
Reads report_template.html, injects base64 encoded figures, and compiles via Playwright.
"""

import os
import sys
import base64
import shutil
from playwright.sync_api import sync_playwright

BASE_DIR = 'SIMUPHARM_PHASE5_2_GSA_SCIENTIFIC_FEASIBILITY'
ARTIFACT_DIR = r'C:\Users\dsant\.gemini\antigravity\brain\55a75768-f2c0-4fa0-b387-5baedff096a9'
FINAL_PDF_NAME = 'SIMUPHARM_PHASE5_2_GSA_SCIENTIFIC_FEASIBILITY_AND_KILL_SPRINT.pdf'

def get_base64_image(rel_path):
    p = os.path.join(BASE_DIR, rel_path)
    if not os.path.exists(p):
        print(f"Warning: Image missing: {p}")
        return ""
    with open(p, 'rb') as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode('utf-8')

def build_pdf():
    print("Reading HTML template...")
    template_path = os.path.join(BASE_DIR, 'report_template.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()

    print("Encoding images into data URIs...")
    replacements = {
        '__IMG_VANDEEMTER__': get_base64_image('02_ENGINE_AUDIT/van_deemter_audit.png'),
        '__IMG_PRESSURE__': get_base64_image('02_ENGINE_AUDIT/hydraulic_pressure_audit.png'),
        '__IMG_RANGE__': get_base64_image('03_PARAMETER_SPACE/range_sensitivity_comparison.png'),
        '__IMG_SOBOL_BAR__': get_base64_image('07_INTERACTION_ANALYSIS/sobol_S1_ST_barchart.png'),
        '__IMG_CONV__': get_base64_image('05_CONVERGENCE/convergence_plot_ST.png'),
        '__IMG_OFAT__': get_base64_image('06_OFAT_COMPARISON/ofat_response_curves.png'),
        '__IMG_RSM__': get_base64_image('07_INTERACTION_ANALYSIS/rsm_actual_vs_predicted.png'),
        '__IMG_CONTOUR__': get_base64_image('08_FAILURE_BOUNDARY/failure_boundary_contour.png')
    }

    for placeholder, data_uri in replacements.items():
        html = html.replace(placeholder, data_uri)

    target_html = os.path.join(BASE_DIR, 'compiled_report.html')
    with open(target_html, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Compiled standalone HTML written ({os.path.getsize(target_html) / 1024:.1f} KB)")

    target_root_pdf = FINAL_PDF_NAME
    target_report_pdf = os.path.join(BASE_DIR, '14_FINAL_REPORT', FINAL_PDF_NAME)
    target_artifact_pdf = os.path.join(ARTIFACT_DIR, FINAL_PDF_NAME)

    print(f"Rendering PDF to {target_root_pdf} via Playwright Chromium...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('file:///' + os.path.abspath(target_html).replace('\\', '/'))
        page.wait_for_load_state('networkidle')
        page.pdf(
            path=target_root_pdf,
            format='A4',
            print_background=True,
            margin={'top': '18mm', 'bottom': '18mm', 'left': '14mm', 'right': '14mm'},
            display_header_footer=False
        )
        browser.close()

    print("Copying PDF to internal report folder and artifact directory...")
    shutil.copyfile(target_root_pdf, target_report_pdf)
    shutil.copyfile(target_root_pdf, target_artifact_pdf)

    size_mb = os.path.getsize(target_root_pdf) / (1024 * 1024)
    print(f"Generated Master PDF: {target_root_pdf} ({size_mb:.2f} MB)")
    print(f"Mirrored to: {target_report_pdf}")
    print(f"Mirrored to Artifacts: {target_artifact_pdf}")

if __name__ == '__main__':
    build_pdf()
