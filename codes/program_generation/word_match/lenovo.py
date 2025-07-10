import csv
import re

def extract_carbon(text):
    """Extracts numeric carbon footprint value from the operand, handling commas and arbitrary spaces."""
    match = re.search(r'Product Carbon Footprint Value:\s*(\d+(\.\d+)?)\s*(kg)? of CO2e', text)
    if match:
        return round(float(match.group(1)), 6)
    return 0

prompts = []
with open('../output/lenovo_multiquestion_mapping.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # print('interests:', interests)
        mappings = row['Mapping']
        # print('mappings:', mappings)
        total_carbon = extract_carbon(mappings)

        prompt = f"```\ntotal_carbon={total_carbon}"
        prompt += "\nanswer=[total_carbon]"
        prompt += "\n```"

        prompts.append(prompt)

import pandas as pd
df = pd.read_csv("../output/lenovo_multiquestion_mapping.csv")
# print(len(prompts))
df["Program"] = prompts
df.to_csv("../output/lenovo_multiquestion_pal.csv", index=False)
