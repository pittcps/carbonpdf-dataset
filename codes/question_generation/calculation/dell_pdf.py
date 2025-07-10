import fitz  # PyMuPDF
import os
import pandas as pd

def extract_text_from_pdf(pdf_path):
    """Extracts all text from a PDF file using PyMuPDF, preserving line breaks."""
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

input_csv = '../input/Dell_Carbon_Breakdown.csv'
df = pd.read_csv(input_csv)
pdf_filenames = df['Carbon Filename'].apply(lambda x: x.split('\\')[-1])
pdf_texts = process_pdfs('../../input/dell_carbon', set(pdf_filenames))
df['Text'] = pdf_filenames.apply(lambda x: pdf_texts.get(x.split('\\')[-1], ''))

# Define the columns to be appended
columns_to_append = [
    'Manufacturing Percentage', 'Chassis & Assembly Percentage', 'Hard Drive Percentage',
    'SSD Percentage', 'Power Supply Percentage', 'Battery Percentage',
    'Mainboard and Other Boards Percentage', 'Display Percentage', 'Packaging Percentage'
]
df['Text'] = df.apply(lambda row: append_percentages(row, columns_to_append), axis=1)

output_csv = '../output/dell_pdf.csv'
df.to_csv(output_csv, index=False)
