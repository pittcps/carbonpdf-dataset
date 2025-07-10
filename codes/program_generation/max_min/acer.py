import csv
import re

def extract_percent(text):
    """Extracts the numeric percentage value from the operand."""
    match = re.search(r'(\d+(\.\d+)?)%', text)
    if match:
        return round(float(match.group(1)), 6)
    return 0

def extract_string(text):
    """Extracts the component name from the operand."""
    match = re.search(r'(.+?)\s*\d+(\.\d+)?%', text)
    if match:
        return match.group(1).strip()
    return ""

prompts = []
with open('../output/max_min/acer_multiquestion_mapping.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        str = row['Interests']
        interests = str.split(',')

        mappings = row['Mapping'].split('\", \"')

        components = {}
        for operand in mappings:
            if '%' in operand:
                str = operand.split(',')
                str2 = str[-1].split('"')
                str3 = str2[0].lower().strip()
                str4 = str3.split()
                cp_name = str4[0]
                if cp_name == 'solid':
                    cp_name = 'ssd'
                if cp_name == 'hard':
                    cp_name = 'hdd'
                # if cp_name == 'battery':
                #     cp_name = 'batteries'
                component_percent = extract_percent(operand)
                components[cp_name] = component_percent
        print(components)
        prompt = f"```"

        if len(interests) == 1 and interests[0] == 'max':
            prompt += "\nbreakdown_dict={"
            for name, percent in components.items():
                prompt += f'"{name}":{percent},'
            prompt = prompt[:-1]
            prompt += "}"
            prompt += f'\nmax_pair=max(breakdown_dict.items(), key=lambda item: item[1])'
            prompt += "\nanswer=["
            prompt += f'{{max_pair[0]: max_pair[1]}}'
            prompt += "]"
        elif len(interests) == 1 and interests[0] == 'min':
            prompt += "\nbreakdown_dict={"
            for name, percent in components.items():
                prompt += f'"{name}":{percent},'
            prompt = prompt[:-1]
            prompt += "}"
            prompt += f'\nmin_pair=min(breakdown_dict.items(), key=lambda item: item[1])'
            prompt += "\nanswer=["
            prompt += f'{{min_pair[0]: min_pair[1]}}'
            prompt += "]"
        else:
            prompt += "\nbreakdown_dict={"
            for name, percent in components.items():
                prompt += f'"{name}":{percent},'
            prompt = prompt[:-1]
            prompt += "}"
            prompt += f'\nmax_pair=max(breakdown_dict.items(), key=lambda item: item[1])'
            prompt += f'\nmin_pair=min(breakdown_dict.items(), key=lambda item: item[1])'
            prompt += "\nanswer=["
            prompt += f'{{max_pair[0]: max_pair[1]}},'
            prompt += f'{{min_pair[0]: min_pair[1]}}'
            prompt += "]"

        prompt += "\n```"
        prompts.append(prompt)

import pandas as pd
df = pd.read_csv("../output/max_min/acer_multiquestion_mapping.csv")
df["Program"] = prompts
df.to_csv("../output/max_min/acer_multiquestion_pal.csv", index=False)
