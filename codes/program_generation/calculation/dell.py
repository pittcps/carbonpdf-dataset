import csv
import re

def extract_carbon(text):
    """Extracts numeric carbon footprint value from the operand, handling commas and arbitrary spaces."""
    match = re.search(r'(\d{1,3}(,\d{3})*)\s*kg\s*CO\s*2\s*e\s*(\+/-|mean\s+of\s+\d{1,3}(,\d{3})*\s*kg\s*of\s*CO\s*2\s*e)?', text)
    if not match:
        # Try matching "mean of xxx kg of CO2e"
        match = re.search(r'mean\s+of\s+(\d{1,3}(,\d{3})*)\s*kg\s*of\s*CO\s*2\s*e', text)

    if match:
        # return round(float(match.group(1).replace(',', '')), 6)
        return round(float(match.group(1).replace(',', '')), 6)
    return 0

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
with open('../output/dell_multiquestion_mapping.csv', 'r', newline='') as csvfile:
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
            if 'kg' in operand:
                total_carbon = extract_carbon(operand)
            elif '%' in operand:
                str = operand.split('\": \"')
                str2 = str[1].split()
                cp_name = str2[0].lower().strip()
                if cp_name == 'solid':
                    cp_name = 'ssd'
                if cp_name == 'hard':
                    cp_name = 'hdd'
                if cp_name == 'battery':
                    cp_name = 'batteries' # interests
                component_percent = extract_percent(operand) / 100
                component_percent = round(component_percent, 7)
                components[cp_name] = component_percent

        prompt = f"```\ntotal_carbon={total_carbon}"

        if len(interests) == 1 and 'total' in interests: # only total
                prompt += "\nanswer=[total_carbon]"
        elif 'breakdown' in interests:
            for name, percent in components.items():
                prompt += f"\n{name}_percent={percent}"
                prompt += f"\n{name}_carbon=total_carbon*{name}_percent"
            prompt += "\nanswer=["
            for name, percent in components.items():
                prompt += f'{{"{name}":{name}_carbon}},' # name,carbon pair; Then for breakdown ground truth, it also needs name, carbon pairs
            prompt = prompt[:-1]
            prompt += "]"
            # print(prompt)
        else:
            # print('----')
            for interest in interests:
                for name, percent in components.items():
                    # if name == 'batteries':
                    #     print(interest)
                    if interest in name:
                        prompt += f"\n{name}_percent={percent}"
                        prompt += f"\n{name}_carbon=total_carbon*{name}_percent"

            prompt += "\nanswer=["
            for interest in interests:
                if interest == 'total':
                    prompt += 'total_carbon,'
                else:
                    # found = False
                    for name, percent in components.items():
                        if interest in name:
                            prompt += f"{name}_carbon,"
                        #     found = True
                        # if len(interests) == 1 and 'manufacturing' in interests:
                        #     found = True
                    # if not found:
                    #     print(row['Prompt'])
            prompt = prompt[:-1]
            prompt += "]"
        prompt += "\n```"
        # print(interests)
        # print(prompt)
        # if 'batteries' in interests:
        #     print(prompt)
        prompts.append(prompt)

import pandas as pd
df = pd.read_csv("../output/dell_multiquestion_mapping.csv")
df["Program"] = prompts
# print('Hi', prompts)
df.to_csv("../output/dell_multiquestion_pal.csv", index=False)
