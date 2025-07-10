import pandas as pd
import random
import csv

def generate_prompts(row):
    prompts = {}

    prompt = f"What is the component with the highest carbon footprint percentage in the manufacturing breakdown of the {row['Commercial Name']} {row['Category'].lower()}?"
    prompts[prompt] = ['max']
    prompt = f"What is the component with the lowest carbon footprint percentage in the manufacturing breakdown of the {row['Commercial Name']} {row['Category'].lower()}?"
    prompts[prompt] = ['min']
    prompt = f"What are the components with the highest and lowest carbon footprint percentages in the manufacturing breakdown of the {row['Commercial Name']} {row['Category'].lower()}?"
    prompts[prompt] = ['max', 'min']

    return list(prompts.items())

def process_files(csv_input_path, csv_output_path):
    data = pd.read_csv(csv_input_path, encoding='utf-8')

    with open(csv_output_path, mode='w', newline='', encoding='utf-8') as outfile:
        fieldnames = ['Commercial Name', 'Prompt', 'Text', 'Interests', 'Question Type']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for _, row in data.iterrows():
            text = row['Text']
            prompts = generate_prompts(row)
            for prompt, interests in prompts:
                writer.writerow({'Commercial Name': row['Commercial Name'], 'Prompt': prompt, 'Text': text, 'Interests': ", ".join(interests),'Question Type': 'derive'})


csv_input_path = '../output/max_min/hp_pdf.csv'
csv_output_path = '../output/max_min/hp_multiquestion_pdf.csv'

process_files(csv_input_path, csv_output_path)
