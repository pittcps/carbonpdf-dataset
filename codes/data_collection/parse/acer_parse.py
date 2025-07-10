import os
import csv
import fitz
import re

def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

def extract_value_after_key(text, key, n):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if key in line:
            return lines[i + n].strip() if i + n < len(lines) else None
    return None

def extract_nearest_number_after_key(text, key, n):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if key in line:
            for j in range(i + 1, min(i + n + 1, len(lines))):
                match = re.search(r'\d+(\.\d+)?', lines[j])
                if match:
                    return match.group()
    return None

def extract_number_from_string(s):
    if s == None:
        return None
    match = re.search(r'\d+(\.\d+)?', s)
    return match.group() if match else None

pdf_directory = 'acer/'
csv_directory = 'out/'
csv_file_path = os.path.join(csv_directory, 'acer_laptops.csv')

os.makedirs(csv_directory, exist_ok=True)

all_maps = []
for file_name in os.listdir(pdf_directory):
    if file_name.lower().endswith('.pdf'):
        pdf_path = os.path.join(pdf_directory, file_name)
        text = extract_text_from_pdf(pdf_path)

        maps = {'Filename': file_name}
        maps['PCF'] = extract_value_after_key(text, 'Estimated carbon footprint', 1)
        maps['Product Weight'] = extract_nearest_number_after_key(text, 'Product Weight (excluded accessory and packaging)', 3)
        maps['Panel Size'] = extract_nearest_number_after_key(text, 'Panel Size', 3)
        maps['Energy Demand (Yearly TEC)'] = extract_nearest_number_after_key(text, 'Energy Demand (Yearly TEC)', 3)
        if maps['Energy Demand (Yearly TEC)'] == None:
            maps['Energy Demand (Yearly TEC)'] = extract_nearest_number_after_key(text, 'Total Energy Consumption (Yearly TEC)', 3)
        maps['Product Lifetime'] = extract_nearest_number_after_key(text, 'Product Lifetime', 3)

        if all(value is not None for key, value in maps.items() if key != 'Filename'):
            all_maps.append(maps)

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=all_maps[0].keys())
    writer.writeheader()
    for data_map in all_maps:
        writer.writerow(data_map)
