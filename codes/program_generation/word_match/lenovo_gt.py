import csv
import pandas as pd

gt_list = []

# Open both CSV files simultaneously using zip
with open('../output/lenovo_multiquestion_mapping.csv', 'r', newline='') as csvfile, \
        open('../input/lenovo_pcf.csv', 'r', newline='') as csvfile2:
    reader = csv.DictReader(csvfile)
    reader2 = csv.DictReader(csvfile2)

    for row, row2 in zip(reader, reader2):
        interests_str = row['Interests']
        interests = [i.strip().lower().split()[0] for i in interests_str.split(',')]

        gtl = []
        if row2['Commercial Name'] == row['Commercial Name']:
            gtl.append(row2['PCF'])

        gt_list.append(gtl)

# Read the third CSV
df = pd.read_csv("../output/lenovo_multiquestion_pal.csv")

# Assign the new column to DataFrame
df["Answer"] = gt_list

# Save the DataFrame to CSV
df.to_csv("../output/gt_lenovo_pal.csv", index=False)
