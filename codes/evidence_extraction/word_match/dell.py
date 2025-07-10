import csv
import re
import json

def find_matches(interest, text):
    patterns = {
        'ssd': r'SSD\s*\d+(\.\d+)?%',
        'hdd': r'Hard Drive \s*\d+(\.\d+)?%',
        'battery': r'Battery\s*\d+(\.\d+)?%',
        'chassis': r'Chassis & Assembly\s*\d+(\.\d+)?%',
        'power supply unit': r'Power Supply\s*\d+(\.\d+)?%',
        'mainboard and other boards': r'Mainboard and Other Boards \s*\d+(\.\d+)?%',
        'display': r'Display\s*\d+(\.\d+)?%',
        'packaging': r'Packaging\s*\d+(\.\d+)?%',
        'manufacturing': r'Manufacturing\s*\d+(\.\d+)?%'
    }

    interest = interest.strip()
    matches = []
    if interest.lower() in patterns:
        pattern_interest = re.compile(patterns[interest.lower()])
        matches = list(pattern_interest.finditer(text))
        if matches == []:
            print('None')
            print(text)
            print(interest)
        else:
            matches = [matches[-1]]
    return matches

def process_text(row):
    text = row['Text']
    question = row['Prompt']
    interests = row['Interests'].split(',')
    # print(interests)

    mapping = ['O'] * len(text)
    map_index = {}

    for interest in interests:
        matches = find_matches(interest, text)
        for match in matches:
            start, end = match.span()
            mapping[start:end] = ['I'] * (end - start)
            index_string = f'[{start},{end-1}]'
            map_index[index_string] = text[start:end]

    map_index_str = json.dumps(map_index, ensure_ascii=False)

    interests = [i.strip().lower() for i in interests]

    return map_index_str

def main():
    input_file_path = '../output/word_match/dell_multiquestion_pdf.csv'
    output_file_path = '../output/word_match/dell_multiquestion_mapping.csv'

    with open(input_file_path, mode='r', newline='', encoding='utf-8') as input_file:
        reader = csv.DictReader(input_file)
        fieldnames = reader.fieldnames + ['Mapping']

        with open(output_file_path, mode='w', newline='', encoding='utf-8') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=fieldnames, quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()

            for row in reader:
                row['Mapping'] = process_text(row)
                writer.writerow(row)

    print(f"Processed file saved as {output_file_path}")

if __name__ == "__main__":
    main()
