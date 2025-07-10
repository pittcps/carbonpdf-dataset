import csv
import re

gt_list = []
with open('../output/top5/dell_multiquestion_mapping.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        interest = row['Interests']

        gtl = {}
        with open('../input/Dell_Carbon_Breakdown.csv', 'r', newline='') as csvfile2:
            reader2 = csv.DictReader(csvfile2)
            for row2 in reader2:
                if row2['Commercial Name'] == row['Commercial Name']:
                    if float(row2['SSD Percentage']) != 0:
                        gtl['ssd'] = float(row2['SSD Percentage'])
                    if float(row2['Hard Drive Percentage']) != 0:
                        gtl['hdd'] = float(row2['Hard Drive Percentage'])
                    if float(row2['Battery Percentage']) != 0:
                        gtl['battery'] = float(row2['Battery Percentage'])
                    if float(row2['Chassis & Assembly Percentage']) != 0:
                        gtl['chassis'] = float(row2['Chassis & Assembly Percentage'])
                    if float(row2['Power Supply Percentage']) != 0:
                        gtl['power'] = float(row2['Power Supply Percentage'])
                    if float(row2['Mainboard and Other Boards Percentage']) != 0:
                        gtl['mainboard'] = float(row2['Mainboard and Other Boards Percentage'])
                    if float(row2['Display Percentage']) != 0:
                        gtl['display'] = float(row2['Display Percentage'])
                    if float(row2['Packaging Percentage']) != 0:
                        gtl['packaging'] = float(row2['Packaging Percentage'])
                    break
            dict_list = []
            if interest == '3':
                dict_list = [{k: v} for k, v in sorted(gtl.items(), key=lambda item: item[1], reverse=True)[:3]]
            elif interest == '5':
                dict_list = [{k: v} for k, v in sorted(gtl.items(), key=lambda item: item[1], reverse=True)[:5]]

        gt_list.append(dict_list)

import pandas as pd
df = pd.read_csv("../output/top5/dell_multiquestion_pal.csv")
df["Answer"] = gt_list
df.to_csv("../output/top5/gt_dell_pal.csv", index=False)
