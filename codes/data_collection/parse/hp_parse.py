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

def extract_value_after_exact_key(text, key, n):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if line.strip() == key:
            return lines[i + n].strip() if i + n < len(lines) else None
    return None

def extract_number_after_exact_key(text, key, n):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if line.strip() == key:
            s = lines[i + n].strip() if i + n < len(lines) else None
            if s is None:
                return None
            s = s.replace(',', '')

            match = re.search(r'\d+(\.\d+)?', s)
            return match.group() if match else None
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

def extract_nearest_number_after_exact_key(text, key, n):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if line.strip() == key:
            for j in range(i + 1, min(i + n + 1, len(lines))):
                match = re.search(r'\d+(\.\d+)?', lines[j])
                if match:
                    return match.group()
    return None

def extract_nearest_percent_after_key(text, key, n):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if key in line:
            if n == 0:
                match = re.search(r'(\d+(\.\d+)?)%', lines[i])
                if match:
                    return float(match.group(1)) * 0.01
            else:
                for j in range(i + 1, min(i + n + 1, len(lines))):
                    # Find a number followed by '%', but only capture the number
                    match = re.search(r'(\d+(\.\d+)?)%', lines[j])
                    if match:
                        return float(match.group(1)) * 0.01
    return None

def extract_nearest_percent_after_exact_key(text, key, n):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if line.strip() == key:
            if n == 0:
                match = re.search(r'(\d+(\.\d+)?)%', lines[i])
                if match:
                    return float(match.group(1)) * 0.01
            else:
                for j in range(i + 1, min(i + n + 1, len(lines))):
                    match = re.search(r'(\d+(\.\d+)?)%', lines[j])
                    if match:
                        return float(match.group(1)) * 0.01
    return None

def extract_number_from_string(s):
    if s is None:
        return None

    s = s.replace(',', '')

    match = re.search(r'\d+(\.\d+)?', s)
    return match.group() if match else None




pdf_directory = 'hp/All'
csv_directory = 'out/'
csv_file_path = os.path.join(csv_directory, 'hp_All_new.csv')

os.makedirs(csv_directory, exist_ok=True)
all_maps = []
for file_name in os.listdir(pdf_directory):
    if file_name.lower().endswith('.pdf'):
        pdf_path = os.path.join(pdf_directory, file_name)
        text = extract_text_from_pdf(pdf_path)

        # print(text)
        maps = {'Filename': file_name}
        
        maps['Commercial Name'] = extract_value_after_key(text, 'Product Carbon Footprint Report', 1)

        pattern = r'\d{1,2}-[A-Za-z]{3}-\d{4}'
        str = extract_value_after_key(text, 'Product Carbon Footprint Report', 1)
        if str is not None and re.match(pattern, str):
            maps['Commercial Name'] = extract_value_after_key(text, 'Product Carbon Footprint Report', 2)
        
        if str == '':
            maps['Commercial Name'] = extract_value_after_key(text, 'Product Carbon Footprint Report', 2)

        if maps['Commercial Name'] == 'GHG Emissions':
            maps['Commercial Name'] = extract_value_after_key(text, 'HP’s Sustainability Website', 1)

        maps['Use location'] = extract_value_after_exact_key(text, 'Assumptions', 2)
        if maps['Use location'] == '':
            maps['Use location'] = extract_value_after_exact_key(text, 'Final manufacturing location', 3)



        maps['Final manufacturing location'] = extract_value_after_exact_key(text, 'Assumptions', 6)
        if maps['Final manufacturing location'] == 'Learn more at':
            maps['Final manufacturing location'] = extract_value_after_exact_key(text, 'Assumptions', 5)
        if maps['Final manufacturing location'] == '':
            maps['Final manufacturing location'] = extract_value_after_exact_key(text, 'Final manufacturing location', 7)

        maps['Lifetime'] = extract_number_after_exact_key(text, 'Assumptions', 1)
        maps['Use energy demand'] = extract_number_after_exact_key(text, 'Assumptions', 3)
        maps['Product weight'] = extract_number_after_exact_key(text, 'Assumptions', 4)
        maps['Screen size'] = extract_number_after_exact_key(text, 'Assumptions', 5)


        str = extract_value_after_key(text, 'omissions contained herein.', 1)
        # print(file_name, str)
        maps['PCF'] = extract_number_from_string(str)
        if maps['PCF'] == None:
            str = extract_value_after_key(text, 'additional warranty.', 1)
            # print(file_name, str)
            maps['PCF'] = extract_number_from_string(str)
        if maps['PCF'] == None:
            str = extract_value_after_key(text, 'Estimated impact', 1)
            # print(file_name, str)
            maps['PCF'] = extract_number_from_string(str)

        maps['Manufacturing'] = extract_nearest_percent_after_exact_key(text, 'Manufacturing', 1)
        if maps['Manufacturing'] is None:
            maps['Manufacturing'] = extract_nearest_percent_after_exact_key(text, 'Production', 1)

        maps['Distribution'] = extract_nearest_percent_after_exact_key(text, 'Distribution', 1)
        maps['Use'] = extract_nearest_percent_after_exact_key(text, 'Use', 1)
        if maps['Use'] is None:
            # print(file_name)
            maps['Use'] = extract_nearest_percent_after_key(text, 'Use', 0)

        maps['End of Life'] = extract_nearest_percent_after_exact_key(text, 'End of Life', 1)

        maps['Mainboard and other boards'] = extract_nearest_percent_after_exact_key(text, 'Mainboard and other boards', 1)
        maps['Chassis'] = extract_nearest_percent_after_exact_key(text, 'Chassis', 1)
        maps['Solid State Drive (SSD)'] = extract_nearest_percent_after_exact_key(text, 'Solid State Drive (SSD)', 1)
        maps['Power Supply Unit & External Cables'] = extract_nearest_percent_after_exact_key(text, 'Power Supply Unit & External Cables', 1)
        maps['Others*'] = extract_nearest_percent_after_exact_key(text, 'Others*', 1)
        maps['External components (Keyboard & Mouse)'] = extract_nearest_percent_after_exact_key(text, 'External components (Keyboard & Mouse)', 1)
        maps['Packaging'] = extract_nearest_percent_after_exact_key(text, 'Packaging', 1)
        maps['Batteries'] = extract_nearest_percent_after_exact_key(text, 'Batteries', 1)
        
        maps['ODD'] = extract_nearest_percent_after_exact_key(text, 'ODD', 1)
        if maps['ODD'] == None:
            maps['ODD'] = extract_nearest_percent_after_exact_key(text, 'Optical Disk Drive (ODD)', 1)
        maps['Hard Drive (HDD)'] = extract_nearest_percent_after_exact_key(text, 'Hard Drive (HDD)', 1)
        maps['Display'] = extract_nearest_percent_after_exact_key(text, 'Display', 1)

        if any(value is not None for key, value in maps.items() if key != 'Filename' and key != 'PCF') and maps['Use location'] != 'Lifetime of product':
            all_maps.append(maps)

# print(all_maps)
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=all_maps[0].keys())
    writer.writeheader()
    for data_map in all_maps:
        writer.writerow(data_map)
