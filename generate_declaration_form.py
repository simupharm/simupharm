import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def create_declaration_form():
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(11)
    font.color.rgb = RGBColor(0x11, 0x11, 0x11)
    style.paragraph_format.line_spacing = 1.2
    style.paragraph_format.space_after = Pt(4)

    # Title
    p = doc.add_paragraph()
    r = p.add_run('AUTHOR DECLARATION & INTEGRITY CERTIFICATION FORM')
    r.font.bold = True
    r.font.size = Pt(15)
    r.font.color.rgb = RGBColor(0x00, 0x4b, 0x87)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(12)

    # Manuscript Details Table
    table = doc.add_table(rows=4, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    for row in table.rows:
        row.cells[0].width = Inches(1.8)
        row.cells[1].width = Inches(4.7)

    headers = [
        ('Manuscript Title:', 'SimuPharm: An Open-Source Multi-Instrument Analytical and Spectroscopic Simulation Suite for Pharmaceutical Research and Education'),
        ('Corresponding Author:', 'SimuPharm Development Team (info@simupharm.io)'),
        ('Software Repository:', 'https://github.com/simupharm/simupharm (Release v1.0.0)'),
        ('Target Journal(s):', 'Elsevier SoftwareX / ACS JCIM / JOSS / Computers & Chemical Engineering / J. Chrom A')
    ]

    for idx, (h, val) in enumerate(headers):
        c0 = table.rows[idx].cells[0]
        c1 = table.rows[idx].cells[1]
        c0.text = h
        c0.paragraphs[0].runs[0].font.bold = True
        c0.paragraphs[0].runs[0].font.size = Pt(10)
        c1.text = val
        c1.paragraphs[0].runs[0].font.size = Pt(10)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    def add_sec(title, text):
        h = doc.add_heading(level=2)
        hr = h.add_run(title)
        hr.font.bold = True
        hr.font.size = Pt(11.5)
        hr.font.color.rgb = RGBColor(0x00, 0x4b, 0x87)
        h.paragraph_format.space_before = Pt(8)
        h.paragraph_format.space_after = Pt(2)
        p = doc.add_paragraph(text)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(6)

    add_sec(
        '1. Statement of Authorship and Originality',
        'The authors hereby certify that this manuscript represents original research software and computational methodology. All authors listed have contributed significantly to the conception, software development, mathematical modeling, and manuscript preparation. The material presented has not been published previously and is not under consideration for publication elsewhere.'
    )

    add_sec(
        '2. Generative AI and AI-Assisted Technologies Disclosure Statement',
        'In strict compliance with Elsevier, ACS, and COPE (Committee on Publication Ethics) Guidelines on Generative AI:\n\n'
        '"During the preparation of this work, the authors used AI-assisted language models and coding assistants to support code modularization, automated test script authoring, and English grammatical language editing. Following the use of these tools, the authors thoroughly reviewed, verified, and edited all technical content, mathematical derivations, and code outputs. The authors take full intellectual responsibility and legal accountability for the accuracy, scientific integrity, and contents of the publication. The AI tools do not meet authorship criteria and are not listed as co-authors."'
    )

    add_sec(
        '3. Data, Code, and Software Reproducibility',
        'The authors confirm that the complete, reproducible source code for the SimuPharm package is publicly archived under an OSI-approved open-source license (MIT License) at: https://github.com/simupharm/simupharm (tagged version v1.0.0). All test suites (100% pytest pass rate), numerical benchmarks, and case study generation scripts are open and executable without proprietary dependencies.'
    )

    add_sec(
        '4. Research Ethics and Human/Animal Subjects Exemption',
        'The authors confirm that this work is strictly a computational modeling, simulation, and research software investigation. No human participants, student subjects, clinical trials, or vertebrate animal experiments were conducted. Consequently, Institutional Review Board (IRB) or animal ethics committee approvals were not required.'
    )

    add_sec(
        '5. Conflict of Interest Declaration',
        'The authors declare that they have no known competing financial interests, patents, consulting fees, or personal relationships that could have appeared to influence the work reported in this paper.'
    )

    # Signature block
    sig_h = doc.add_heading(level=2)
    sr = sig_h.add_run('6. Certification & Author Signature')
    sr.font.bold = True
    sr.font.size = Pt(11.5)
    sr.font.color.rgb = RGBColor(0x00, 0x4b, 0x87)

    sp = doc.add_paragraph(
        'I, the corresponding author, confirm the veracity of all statements made above on behalf of all co-authors.\n\n'
        'Signature: ____________________________________\n'
        'Printed Name: ________________________________\n'
        'Affiliation: SimuPharm Open Source Project\n'
        'Date: November 5, 2026'
    )
    sp.paragraph_format.space_before = Pt(4)

    out_root = 'simupharm_author_declaration_form.docx'
    out_brain = 'C:/Users/dsant/.gemini/antigravity/brain/55a75768-f2c0-4fa0-b387-5baedff096a9/simupharm_author_declaration_form.docx'

    doc.save(out_root)
    doc.save(out_brain)
    print(f'Generated {out_root} and {out_brain} successfully!')

if __name__ == '__main__':
    create_declaration_form()
