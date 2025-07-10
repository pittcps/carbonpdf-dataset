import csv
import re
import os
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    extracted_text = [page.get_text() for page in doc.pages()]
    doc.close()

    return extracted_text

# Function to extract specific information from the PDF text
def extract_info(pdf_text_pages):
    full_text = ''.join(pdf_text_pages)
    if len(pdf_text_pages) >= 2:
        second_page_text = pdf_text_pages[1]
        estimated_footprint_match = re.search(r"(\d+\.\d+|\d+) kgCO2e", second_page_text)
        estimated_footprint = estimated_footprint_match.group(1).strip() if estimated_footprint_match else "N/A"
    else:
        estimated_footprint = "N/A"

    product_weight_match = re.search(r"Product Weight \n(\d+\.\d+) kg", full_text, re.IGNORECASE)
    product_weight = product_weight_match.group(1).strip() if product_weight_match else "N/A"

    screen_size_match = re.search(r"Screen Size \n(.*?)\n", full_text, re.IGNORECASE)
    screen_size = screen_size_match.group(1).strip() if screen_size_match else "N/A"

    assembly_location_match = re.search(r"Assembly \nLocation \n(.*?)\n", full_text, re.IGNORECASE)
    assembly_location = assembly_location_match.group(1).strip() if assembly_location_match else "N/A"

    product_lifetime_match = re.search(r"Product Lifetime \n(\d+) years", full_text, re.IGNORECASE)
    product_lifetime = product_lifetime_match.group(1).strip() if product_lifetime_match else "N/A"

    use_location_match = re.search(r"Use Location \n(.*?)\n", full_text, re.IGNORECASE)
    use_location = use_location_match.group(1).strip() if use_location_match else "N/A"

    energy_demand_match = re.search(r"Energy Demand \n\(Yearly TEC\) \n(\d+\.\d+) kWh", full_text, re.IGNORECASE)
    energy_demand = energy_demand_match.group(1).strip() if energy_demand_match else "N/A"

    return {
        "Estimated Carbon Footprint": estimated_footprint,
        "Product Weight": product_weight,
        "Screen Size": screen_size,
        "Assembly Location": assembly_location,
        "Product Lifetime": product_lifetime,
        "Use Location": use_location,
        "Energy Demand (Yearly TEC)": energy_demand
    }

def process_pdf_files(directory, csv_file_path):
    # List of files to exclude
    exclude_files = [
        'dell-modern-slavery-statement.pdf', 
        'lca-docking-station-family.pdf', 
        'List-of-Dell-Technologies-Entities-for-Privacy-Statement.pdf', 
        'pcf-faqs-external-info-only.pdf', 
        'pcf-lca-whitepaper.pdf'
    ]

    fieldnames = ['Filename', 'Estimated Carbon Footprint', 'Product Weight', 'Screen Size', 'Assembly Location', 'Product Lifetime', 'Use Location', 'Energy Demand (Yearly TEC)']
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for filename in os.listdir(directory):
            if filename.endswith('.pdf') and filename not in exclude_files:
                pdf_path = os.path.join(directory, filename)
                pdf_text_pages = extract_text_from_pdf(pdf_path)
                extracted_info = extract_info(pdf_text_pages)

                if extracted_info:
                    writer.writerow({'Filename': filename, **extracted_info})

pdf_file_path = 'dell/clientperipherals'
csv_file_path = 'out/dell/dell_clientperipherals.csv'

process_pdf_files(pdf_file_path, csv_file_path)
