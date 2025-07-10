import csv
import re
import json

def process_text(row):
    text = row['Text']
    question = row['Prompt']

    mapping = ['O'] * len(text)
    map_index = {}

    general_patterns = {
        'co2': r'Product Carbon Footprint Value:\s*\d+(\.\d+)?\s*(kg)? of CO2e',
    }

    for pattern_key in general_patterns:
        pattern_regex = re.compile(general_patterns[pattern_key])
        matches = list(pattern_regex.finditer(text))
        if matches:
            last_match = matches[-1]
            start, end = last_match.span()
            mapping[start:end] = ['I'] * (end - start)
            index_string = f'[{start},{end-1}]'
            map_index[index_string] = text[start:end]
        else:
            return None  # Return None when "nan" condition is met

    map_index_str = json.dumps(map_index, ensure_ascii=False)
    return map_index_str

def main():
    input_file_path = '../output/lenovo_multiquestion_pdf.csv'
    output_file_path = '../output/lenovo_multiquestion_mapping.csv'

    with open(input_file_path, mode='r', newline='', encoding='utf-8') as input_file:
        reader = csv.DictReader(input_file)
        fieldnames = reader.fieldnames + ['Mapping']

        with open(output_file_path, mode='w', newline='', encoding='utf-8') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=fieldnames, quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()

            for i, row in enumerate(reader, start=1):  # Start counting from 1
                mapping = process_text(row)
                if mapping is None:
                    print(f"Row number {i}: nan")
                else:
                    row['Mapping'] = mapping
                    writer.writerow(row)

    print(f"Processed file saved as {output_file_path}")

if __name__ == "__main__":
    main()
