import fitz  # PyMuPDF
import pandas as pd
import os
import csv

def extract_text_from_pdf(pdf_path):
    """Extracts all text from a PDF file using PyMuPDF, removing line breaks."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text").replace('\n', ' ')
    doc.close()
    return text.strip()

def find_pdf_files(root_dir, filename):
    """Searches for a PDF file in a directory and its subdirectories."""
    for dirpath, _, files in os.walk(root_dir):
        for file in files:
            if file == filename:
                return os.path.join(dirpath, file)
    return None

def process_files(csv_input_path, root_dir, csv_output_path):
    data = pd.read_csv(csv_input_path, encoding='utf-8')

    with open(csv_output_path, mode='w', newline='', encoding='utf-8') as outfile:
        fieldnames = list(data.columns) + ['Text']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for _, row in data.iterrows():
            pdf_filename = row['Carbon Filename']
            pdf_path = find_pdf_files(root_dir, pdf_filename)
            text = extract_text_from_pdf(pdf_path) if pdf_path else "PDF file not found"
            row['Text'] = text
            writer.writerow(row.to_dict())

csv_input_path = '../input/HP_Carbon_Breakdown.csv'
root_dir = '../../input/hp_carbon'
csv_output_path = '../output/hp_pdf.csv'

process_files(csv_input_path, root_dir, csv_output_path)
