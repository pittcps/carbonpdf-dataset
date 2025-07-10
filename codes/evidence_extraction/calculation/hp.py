import csv
import re
import json
import random

def find_matches(interest, text):
    patterns = {
        'ssd': r'Solid State Drive \(SSD\)\s*\d+(\.\d+)?%',
        'hdd': r'Hard Drive \(HDD\)\s*\d+(\.\d+)?%',
        'batteries': r'Batteries\s*\d+(\.\d+)?%',
        'chassis': r'Chassis\s*\d+(\.\d+)?%',
        'power supply unit': r'Power Supply Unit & External Cables\s*\d+(\.\d+)?%',
        'mainboard': r'Mainboard and other boards \s*\d+(\.\d+)?%',
        'display': r'Display\s*\d+(\.\d+)?%',
        'packaging': r'Packaging\s*\d+(\.\d+)?%',
        # 'odd': r'(Optical Disk Drive \(ODD\)|ODD)\s*(\d+(\.\d+)?%)',
        # 'external components': r'External components \(Keyboard & Mouse\)\s*\d+(\.\d+)?%'
    }

    interest = interest.strip()
    matches = []
    if interest.lower() == 'breakdown':
        for pattern in patterns.values():
            pattern_regex = re.compile(pattern)
            matches.extend(list(pattern_regex.finditer(text)))
    elif interest.lower() in patterns:
        pattern_interest = re.compile(patterns[interest.lower()])
        matches = list(pattern_interest.finditer(text))

    return matches

def process_text(row, questions_to_process):
    text = row['Text']
    question = row['Prompt']
    interests = row['Interests'].split(',')
    # print(interests)
    if interests[0] != 'breakdown' and questions_to_process[row['Commercial Name']] < 3:
        relevant_matches = [m for i in interests for m in find_matches(i, text)]
        if relevant_matches:
            num_to_remove = random.randint(1, 3)
            matches_to_remove = random.sample(relevant_matches, min(num_to_remove, len(relevant_matches)))

            for match in matches_to_remove:
                start, end = match.span()
                text = text[:start] + text[end:]  # Remove the matched text

            row['Text'] = text
            questions_to_process[row['Commercial Name']] += 1

    mapping = ['O'] * len(text)
    map_index = {}

    general_patterns = {
        'co2': r'\d{1,3}(,\d{3})*\s*kg\s*CO\s*2\s*(eq\.)?',
        'manufacturing': r'Manufacturing\s*\d+(\.\d+)?%',
        'production': r'Production\s*\d+(\.\d+)?%'
    }

    for pattern_key in general_patterns:
        pattern_regex = re.compile(general_patterns[pattern_key])
        for match in pattern_regex.finditer(text):
            start, end = match.span()
            mapping[start:end] = ['I'] * (end - start)
            index_string = f'[{start},{end-1}]'
            map_index[index_string] = text[start:end]

    match_count = 0
    for interest in interests:
        matches = find_matches(interest, text)
        for match in matches:
            start, end = match.span()
            mapping[start:end] = ['I'] * (end - start)
            index_string = f'[{start},{end-1}]'
            map_index[index_string] = text[start:end]
            match_count += 1

        # Remove manufacturing matches if the only interest is 'total'
        interest = interest.strip()
        if len(interests) == 1 and interest.lower() == 'total':
            pattern_regex = re.compile(general_patterns['manufacturing'] + '|' + general_patterns['production'])
            for match in pattern_regex.finditer(text):
                start, end = match.span()
                mapping[start:end] = ['O'] * (end - start)
                index_string = f'[{start},{end-1}]'
                if index_string in map_index:
                    del map_index[index_string]

    interests = [i.strip().lower() for i in interests]
    if 'breakdown' not in interests:
        if 'total' not in interests:
            if 'manufacturing' not in interests:
                if len(map_index) != len(interests) + 2:
                    print(len(map_index), len(interests), 'm1 error', row['Prompt'])
            elif 'manufacturing' in interests:
                if len(map_index) != len(interests) + 1:
                    print(len(map_index), len(interests),'m2 error', row['Prompt'])
        else:
            if len(interests) == 1 and interests[0].lower() == 'total':
                if len(map_index) != 1:
                    print(len(map_index), len(interests),'total error', row['Prompt'])
            else:
                if 'manufacturing' not in interests:
                    if len(map_index) != len(interests) + 1:
                        print(len(map_index), len(interests),'0m1 error', row['Prompt'])
                elif 'manufacturing' in interests:
                    if len(map_index) != len(interests):
                        print(len(map_index), len(interests),'0m2 error', row['Prompt'])
    map_index_str = json.dumps(map_index, ensure_ascii=False)

    interests = [i.strip().lower() for i in interests]

    return map_index_str

def main():
    input_file_path = '../output/hp_multiquestion_pdf.csv'
    output_file_path = '../output/hp_multiquestion_mapping.csv'

    questions_to_process = {}

    with open(input_file_path, mode='r', newline='', encoding='utf-8') as input_file:
        reader = csv.DictReader(input_file)
        fieldnames = reader.fieldnames + ['Mapping']

        with open(output_file_path, mode='w', newline='', encoding='utf-8') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=fieldnames, quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()

            for row in reader:
                product_name = row['Commercial Name']
                if product_name not in questions_to_process:
                    questions_to_process[product_name] = 0

                row['Mapping'] = process_text(row, questions_to_process)
                writer.writerow(row)

    print(f"Processed file saved as {output_file_path}")

if __name__ == "__main__":
    main()
