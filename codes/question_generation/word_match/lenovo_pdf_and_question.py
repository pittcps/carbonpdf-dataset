import pandas as pd
import random
import csv

def generate_prompts(row):
    prompts = {}
    prompt = f"What is the carbon footprint of total in the {row['Commercial Name']}?"
    prompts[prompt] = "total "

    return prompts

def process_files(csv_input_path, csv_output_path):
    data = pd.read_csv(csv_input_path, encoding='utf-8')

    with open(csv_output_path, mode='w', newline='', encoding='utf-8') as outfile:
        fieldnames = ['Commercial Name', 'Prompt', 'Text', 'Interests', 'Question Type']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for _, row in data.iterrows():
            text = row['Text']
            prompts = generate_prompts(row)
            for prompt, interests in prompts.items():
                writer.writerow({'Commercial Name': row['Commercial Name'], 'Prompt': prompt, 'Text': text, 'Interests': interests, 'Question Type': 'as-is'})


csv_input_path = '../../out/lenovo_pdf.csv'
csv_output_path = '../output/lenovo_multiquestion_pdf.csv'

process_files(csv_input_path, csv_output_path)
