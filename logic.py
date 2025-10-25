import fitz
from docx import Document
import json
import os

def extract_text_from_pdf(pdf_path):
    pdf_file = fitz.open(pdf_path)
    full_text = ""
    for page in pdf_file:
        full_text += page.get_text() + '\n'
    pdf_file.close()
    return full_text

def save_text_to_word_format(extracted_content, output_file):
    doc = Document()
    for line in extracted_content.splitlines():
        doc.add_paragraph(line)
    doc.save(output_file)