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
with open('../output/word_match/dell_multiquestion_mapping.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        prompt = ''
        str = row['Interests']
        interests = str.split(',')
        interests = [i.strip().lower() for i in interests]
        i_temp = []
        for i in interests:
            i2 = i.split()
            i_temp.append(i2[0])
        interests = i_temp
        # print('interests:', interests)
        mappings = row['Mapping'].split('\", \"')
        # print('mappings:', mappings)

        components = {}
        # found = False
        for operand in mappings:
            if '%' in operand:
                str = operand.split('\": \"')
                str2 = str[1].split()
                cp_name = str2[0].lower().strip()
                if cp_name == 'solid':
                    cp_name = 'ssd'
                if cp_name == 'hard':
                    cp_name = 'hdd'
                # if cp_name == 'battery':
                #     cp_name = 'batteries'
                component_percent = extract_percent(operand)
                # component_percent = round(component_percent, 7)
                components[cp_name] = component_percent

        prompt = f"```"

        for interest in interests:
            for name, percent in components.items():
                if interest in name:
                    prompt += f"\n{name}_percent={percent}"

        prompt += "\nanswer=["
        for interest in interests:
            for name, percent in components.items():
                if interest in name:
                    prompt += f"{name}_percent,"
        prompt = prompt[:-1]
        prompt += "]"
        prompt += "\n```"

        prompts.append(prompt)

import pandas as pd
df = pd.read_csv("../output/word_match/dell_multiquestion_mapping.csv")
df["Program"] = prompts
df.to_csv("../output/word_match/dell_multiquestion_pal.csv", index=False)
