from fpdf import FPDF
from os import path


def pdf_convert(entries, to_pdf_attr):
    # Creating path to pdf file
    full_path = to_pdf_attr
    new_pdf = 'rss.pdf'
    complete_pdf = path.join(full_path, new_pdf)

    # Creating fpdf object
    pdf = FPDF('P', 'mm', 'Letter')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Looping through entries end filling pdf
    pdf.set_font('helvetica', '', 16)
    for i, e in enumerate(entries):
        title = e.title.text[:20]
        link = e.link.get('href')
        date = e.updated.text
        summary = e.summary.text

        pdf.cell(0, 10, txt=f"Title: " + title, ln=1)
        pdf.cell(0, 10, txt=f"Link: " + link, ln=1)
        pdf.cell(0, 10, txt=f"Date: " + date, ln=1)
        pdf.multi_cell(0, 10, txt=f"Summary: " + summary, align="L")
    pdf.output(complete_pdf)
