import fitz
from docx import Document
import json
import os
from html2docx import html2docx

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    html_content = ""
    for page in doc:
        html_content += page.get_text("html")  # preserves layout, fonts, styles
    doc.close()
    return html_content

def save_text_to_word_format(extracted_html, output_file):
    docx_stream = html2docx(extracted_html, 'yaeh')  # returns BytesIO
    with open(output_file, "wb") as f:
        f.write(docx_stream.getvalue())  # extract raw bytes