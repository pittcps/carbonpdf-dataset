import pandas as pd
import random
import csv

def generate_prompts(row):
    prompts = {}

    prompt = f"What are the top 3 components with the highest carbon footprint percentages in the manufacturing breakdown of the {row['Commercial Name']} {row['Category'].lower()}?"
    prompts[prompt] = 3
    prompt = f"What are the top 5 components with the highest carbon footprint percentages in the manufacturing breakdown of the {row['Commercial Name']} {row['Category'].lower()}?"
    prompts[prompt] = 5

    return list(prompts.items())

def process_files(csv_input_path, csv_output_path):
    data = pd.read_csv(csv_input_path, encoding='utf-8')

    with open(csv_output_path, mode='w', newline='', encoding='utf-8') as outfile:
        fieldnames = ['Commercial Name', 'Prompt', 'Text', 'Interests','Question Type']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for _, row in data.iterrows():
            text = row['Text']
            prompts = generate_prompts(row)
            for prompt, interest in prompts:
                writer.writerow({'Commercial Name': row['Commercial Name'], 'Prompt': prompt, 'Text': text, 'Interests': interest,'Question Type': 'derive'})


csv_input_path = '../output/top5/dell_pdf.csv'
csv_output_path = '../output/top5/dell_multiquestion_pdf.csv'

process_files(csv_input_path, csv_output_path)
