import os
import re
import time
from gradio_client import Client, handle_file
from docx import Document
from PyPDF2 import PdfReader, PdfWriter

client = Client("lightonai/LightOnOCR-1B-Demo")

def extract_single_page(pdf_path, page_num):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    writer.add_page(reader.pages[page_num])
    temp_path = f"temp_page_{page_num + 1}.pdf"
    with open(temp_path, "wb") as f:
        writer.write(f)
    return temp_path

def clean_markdown(text):
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # remove images
    text = re.sub(r'#+ ', '', text)              # remove headings
    text = re.sub(r'- ', '', text)               # remove list markers
    return text

def pdf_extraction_process(file_path, output_path="output.docx", max_retries=3, resume_from=0):
    reader = PdfReader(file_path)
    num_pages = len(reader.pages)
    print(f"Total pages: {num_pages}")

    doc = Document()
    failed_pages = []

    for page_num in range(resume_from, num_pages):
        print(f"Processing page {page_num + 1}/{num_pages}...")
        temp_pdf = None

        try:
            temp_pdf = extract_single_page(file_path, page_num)

            for attempt in range(max_retries):
                try:
                    result = client.predict(
                        file_input=handle_file(temp_pdf),
                        temperature=0.2,
                        page_num=1,
                        api_name="/process_input"
                    )
                    break
                except Exception as e:
                    print(f"Error on page {page_num + 1}, attempt {attempt + 1}: {e}")
                    time.sleep(2 ** attempt + 1)
            else:
                print(f"Skipping page {page_num + 1} after {max_retries} failed attempts.")
                failed_pages.append(page_num + 1)
                continue

            text_output = result["data"][0] if isinstance(result, dict) else result[0]
            raw_text = clean_markdown(text_output)

            doc.add_paragraph(raw_text)
            doc.add_page_break()
            doc.save(output_path)  # save after each page

        except Exception as e:
            print(f"Unexpected error on page {page_num + 1}: {e}")
            failed_pages.append(page_num + 1)

        finally:
            if temp_pdf and os.path.exists(temp_pdf):
                try:
                    os.remove(temp_pdf)
                except Exception as cleanup_error:
                    print(f"Failed to delete temp file {temp_pdf}: {cleanup_error}")

    print(f"Saved DOCX to {output_path}")
    if failed_pages:
        print("Failed pages:", failed_pages)