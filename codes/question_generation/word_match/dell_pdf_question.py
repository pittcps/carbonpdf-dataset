import pandas as pd
import random
import csv
from itertools import permutations

def generate_prompts(row, num_prompts=10):
    """Generates multiple unique prompts for a single product based on its specifications and available carbon footprint data."""
    prompts = {}
    carbon_footprint_columns = {
        "Mainboard and Other Boards Percentage": "Mainboard and Other Boards",
        "Chassis & Assembly Percentage": "Chassis",
        "SSD Percentage": "SSD",
        "Power Supply Percentage": "Power Supply Unit",
        "Packaging Percentage": "Packaging",
        "Battery Percentage": "Battery",
        "Hard Drive Percentage": "HDD",
        "Display Percentage": "Display"
    }

    available_footprints = carbon_footprint_columns.copy()
    available_footprints["Manufacturing"] = "Manufacturing"
    # available_footprints["PCF"] = "Total"

    # full_description = f"{row['Commercial Name']}: "

   
    valid_footprints = {k: v for k, v in available_footprints.items() if pd.notna(row[k]) and row[k] != 0}

   
    perm = permutations(valid_footprints)
    perm_list = list(perm)
    num_permutations = len(perm_list)

    if not valid_footprints:
        print('No valid values found for: ', row['Commercial Name'])
        return list(prompts.items())

    while len(prompts) < min(num_prompts, num_permutations):
        question_aspects = random.sample(list(valid_footprints.values()), random.randint(1, min(4, len(valid_footprints))))

        if len(question_aspects) == 2:
            questions = " and ".join([aspect.lower() for aspect in question_aspects])
            prompt = f"What are the carbon footprint percentages of the {questions}"
        elif len(question_aspects) > 2:
            questions = ", ".join([aspect.lower() for aspect in question_aspects[:-2]])
            questions += f", {question_aspects[-2].lower()}, and {question_aspects[-1].lower()}"
            prompt = f"What are the carbon footprint percentages of the {questions}"
        else:
            questions = question_aspects[0].lower()
            prompt = f"What is the carbon footprint percentage of the {questions}"

        prompt += f" in the {row['Commercial Name']} {row['Category'].lower()}?"
        if prompt not in prompts:
            # question_aspects = [x.replace('Carbon Footprint', '') for x in question_aspects]
            prompts[prompt] = question_aspects



    return list(prompts.items())

def process_files(csv_input_path, csv_output_path):
    data = pd.read_csv(csv_input_path, encoding='utf-8')

    with open(csv_output_path, mode='w', newline='', encoding='utf-8') as outfile:
        fieldnames = ['Commercial Name', 'Prompt', 'Text', 'Interests', 'Question Type']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for _, row in data.iterrows():
            text = row['Text']

            relevant_prompts = generate_prompts(row)
            for prompt, interests in relevant_prompts:
                writer.writerow({'Commercial Name': row['Commercial Name'], 'Prompt': prompt, 'Text': text, 'Interests': ", ".join(interests), 'Question Type': 'as-is'})


csv_input_path = '../output/word_match/dell_pdf.csv'
csv_output_path = '../output/word_match/dell_multiquestion_pdf.csv'

process_files(csv_input_path, csv_output_path)
