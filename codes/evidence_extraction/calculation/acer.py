import csv
import re
import json
import random

valid_names = {
    'ssd': 'Solid State Drive(s)',
    'hdd': 'Hard Drive(s)',
    'batteries': 'Battery',
    'chassis': 'Chassis',
    'power supply unit': 'Power Supply Unit(s)',
    'mainboard': 'Mainboard (and other boards)',
    'display': 'Display',
    'packaging': 'Packaging',
    'use': 'Use',
    'transport': 'Transport',
    'end of life': 'End of Life',
    'op': 'Optical Drive(s)'
}

def find_matches(text):
    percent_pattern = re.compile(r'e % (.*?) General Information', re.DOTALL)
    name_start_pattern = re.compile(r'Product breakout', re.DOTALL)

    percent_match = percent_pattern.search(text)
    name_start_match = name_start_pattern.search(text)

    if (percent_match and name_start_match):
        percentages = percent_match.group(1).strip().split()

        # Start from "Product breakout" and find valid names
        name_start_index = name_start_match.end()
        names_text = text[name_start_index:]
        names = []
        used_names = set()
        words = names_text.split()
        i = 0
        while i < len(words):
            for j in range(i + 1, i + 10):
                candidate_name = " ".join(words[i:j])
                if candidate_name == 'Typical Energy Consumption (Yearly TEC)':
                    i = j - 1  # Skip this phrase and continue
                    break
                if (candidate_name in valid_names.values()) and (candidate_name not in used_names):
                    names.append(candidate_name)
                    used_names.add(candidate_name)
                    i = j - 1
                    break
            i += 1

        while percentages and percentages[-1] == "0.0%":
            percentages.pop()

        pairs = []
        name_start = 0
        percent_start = 0

        if len(percentages) != len(names):
            print('length error!')
            print(len(percentages), len(names))
            print(percentages)
            print(names)
            print(text)

        for i in range(min(len(percentages), len(names))):
            percent_value = percentages[i]
            name_value = names[i]

            percent_start = text.find(percent_value, percent_start)
            percent_end = percent_start + len(percent_value)

            name_start = text.find(name_value, name_start)
            name_end = name_start + len(name_value)

            pairs.append((percent_value, (percent_start, percent_end), name_value, (name_start, name_end)))

            percent_start = percent_end
            name_start = name_end

        return pairs

    alternative_pattern = re.compile(r'([a-zA-Z\s\(\)]+)\s(\d+\.\d+%)')
    matches = alternative_pattern.findall(text)

    pairs = []
    for name, percent in matches:
        name = name.strip()
        if name in valid_names.values():
            percent_start = text.index(percent)
            percent_end = percent_start + len(percent)
            name_start = text.index(name)
            name_end = name_start + len(name)
            pairs.append((percent, (percent_start, percent_end), name, (name_start, name_end)))

    return pairs

def process_text(row, questions_to_process):
    text = row['Text']
    interests = [interest.strip().lower() for interest in row['Interests'].split(',')]

    pairs = find_matches(text)

    if interests[0] != 'breakdown' and questions_to_process[row['Commercial Name']] < 3:
        relevant_matches = [(percent, name) for percent, _, name, _ in pairs if any(interest in name.lower() for interest in interests)]
        if relevant_matches:
            num_to_remove = random.randint(1, 3)
            matches_to_remove = random.sample(relevant_matches, min(num_to_remove, len(relevant_matches)))

            for percent, name in matches_to_remove:
                start_percent = text.find(percent)
                end_percent = start_percent + len(percent)
                start_name = text.find(name)
                end_name = start_name + len(name)

                text = text[:start_percent] + text[end_percent:]
                text = text[:start_name] + text[end_name:]

            row['Text'] = text
            questions_to_process[row['Commercial Name']] += 1

    mapping = ['O'] * len(text)
    map_index = {}

    general_patterns = {
        'co2': r'mean\s+of\s+\d{1,3}(,\d{3})*\s*kg\s*of\s*CO\s*2\s*(-)?e'
    }

    manu_patterns = {
        'manufacturing': r'Manufacturing\s*\d+(\.\d+)?%'
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

    for pattern_key in manu_patterns:
        if pattern_key in interests:
            pattern_regex = re.compile(manu_patterns[pattern_key])
            matches = list(pattern_regex.finditer(text))
            if matches:
                last_match = matches[-1]
                start, end = last_match.span()
                mapping[start:end] = ['I'] * (end - start)
                index_string = f'[{start},{end-1}]'
                map_index[index_string] = text[start:end]

    for percent_value, (percent_start, percent_end), name_value, (name_start, name_end) in pairs:
        if len(interests) == 1 and interests[0] == 'breakdown':
            if name_value != 'Use' and name_value != 'Transport' and name_value != 'End of Life' and name_value != 'Optical Drive(s)':
                mapping[percent_start:percent_end] = ['I'] * (percent_end - percent_start)
                mapping[name_start:name_end] = ['I'] * (name_end - name_start)
                combined_index_string = f'[{percent_start},{percent_end-1}], [{name_start},{name_end-1}]'
                map_index[combined_index_string] = f'{percent_value}, {name_value}'
        else:
            interest_key = [key for key, value in valid_names.items() if value == name_value][0]
            if interest_key in interests:
                mapping[percent_start:percent_end] = ['I'] * (percent_end - percent_start)
                mapping[name_start:name_end] = ['I'] * (name_end - name_start)
                combined_index_string = f'[{percent_start},{percent_end-1}], [{name_start},{name_end-1}]'
                map_index[combined_index_string] = f'{percent_value}, {name_value}'

    if 'breakdown' not in interests:
        if 'total' not in interests:
            if len(map_index) != len(interests) + 1:
                print(len(map_index), len(interests),'error1', row['Prompt'])
        else:
            if len(map_index) != len(interests):
                print(len(map_index), len(interests),'error2', row['Prompt'])

    map_index_str = json.dumps(map_index, ensure_ascii=False)

    return map_index_str

def main():
    input_file_path = '../output/acer_multiquestion_pdf.csv'
    output_file_path = '../output/acer_multiquestion_mapping.csv'

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
