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

pdf_directory = 'lenovo/'
csv_directory = 'out/'
csv_file_path = os.path.join(csv_directory, 'lenovo.csv')

os.makedirs(csv_directory, exist_ok=True)

all_maps = []
for file_name in os.listdir(pdf_directory):
    if file_name.lower().endswith('.pdf'):
        pdf_path = os.path.join(pdf_directory, file_name)
        text = extract_text_from_pdf(pdf_path)

        maps = {'Filename': file_name}
        maps['Commercial Name'] = extract_value_after_key(text, 'Commercial Name', 1)
        maps['Model Number'] = extract_value_after_key(text, 'Model Number', 1)
        maps['Issue Date'] = extract_value_after_key(text, 'Issue Date', 1)

        str = extract_value_after_key(text, '(a) Product Carbon Footprint Value:', 1)
        # print(file_name, str)
        maps['PCF'] = extract_number_from_string(str)
        maps['Product Weight'] = extract_nearest_number_after_key(text, 'Product Weight', 4)
        maps['Screen Size'] = extract_nearest_number_after_key(text, 'Screen Size', 3)
        maps['Product Lifetime'] = extract_nearest_number_after_key(text, 'Product Lifetime', 4)
        maps['Assembly Location'] = extract_value_after_key(text, 'Assembly Location', 2)
        maps['Use Location'] = extract_value_after_key(text, 'Use Location', 2)

        maps['To country of use: by air'] = extract_nearest_number_after_key(text, 'To country of use: by air', 4)
        maps['To country of use: by ship'] = extract_nearest_number_after_key(text, 'To country of use: by ship', 4)
        maps['To country of use: by rail'] = extract_nearest_number_after_key(text, 'To country of use: by rail', 4)
        maps['To country of use: by truck'] = extract_nearest_number_after_key(text, 'To country of use: by truck', 4)
        maps['In country of use: by air'] = extract_nearest_number_after_key(text, 'In country of use: by air', 4)
        maps['In country of use: by ship'] = extract_nearest_number_after_key(text, 'In country of use: by ship', 4)
        maps['In country of use: by rail'] = extract_nearest_number_after_key(text, 'In country of use: by rail', 4)
        maps['In country of use: by truck'] = extract_nearest_number_after_key(text, 'In country of use: by truck', 4)

        maps['Fraction Recycled (remainder to landfill)'] = extract_nearest_number_after_key(text, 'Fraction Recycled (remainder to landfill)', 3)
        maps['Fraction Shredded Recycling (remainder to manual)'] = extract_nearest_number_after_key(text, 'Fraction Shredded Recycling (remainder to manual)', 3)

        assembly_location = extract_value_after_key(text, 'Assembly Location', 2)
        if assembly_location and assembly_location.startswith('Below is a breakout'):
            continue

        if any(value is not None for key, value in maps.items() if key != 'Filename'):
            all_maps.append(maps)

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=all_maps[0].keys())
    writer.writeheader()
    for data_map in all_maps:
        writer.writerow(data_map)
