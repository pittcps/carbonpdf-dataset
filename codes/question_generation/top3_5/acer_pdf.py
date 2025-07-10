import fitz  # PyMuPDF
import os
import pandas as pd

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            page_text = page.get_text()
            text += page_text
        doc.close()
        return text
    except (fitz.FileDataError, fitz.EmptyFileError):
        return ""

def process_pdfs(directory, pdf_filenames):
    pdf_texts = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file in pdf_filenames:
                pdf_path = os.path.join(root, file)
                text = extract_text_from_pdf(pdf_path)
                if text:
                    text = text.replace('\n', ' ')
                    if len(text) > 131072:
                        text = text[:131070]
                    pdf_texts[file] = text
    return pdf_texts

def append_percentages(row, columns):
    text = row['Text']
    for column in columns:
        value = str(row[column]).replace('Percentage', '').strip()
        if value != '0.0':
            text += f" {column.split(' Percentage')[0]} {value}%"
    return text

input_csv = '../input/Acer_Carbon_Breakdown.csv'
df = pd.read_csv(input_csv)
pdf_filenames = df['Carbon Filename']
pdf_texts = process_pdfs('../../input/acer_carbon', set(pdf_filenames))
df['Text'] = pdf_filenames.apply(lambda x: pdf_texts.get(x, ''))

output_csv = '../output/dataset/acer_pdf.csv'
df.to_csv(output_csv, index=False)
