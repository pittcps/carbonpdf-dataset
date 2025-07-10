import csv
import re

gt_list = []
with open('../output/max_min/hp_multiquestion_mapping.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        str = row['Interests']
        interests = str.split(',')
        interests = [i.strip().lower() for i in interests]

        gtl = {}
        with open('../input/HP_Carbon_Breakdown.csv', 'r', newline='') as csvfile2:
            reader2 = csv.DictReader(csvfile2)
            for row2 in reader2:
                if row2['Commercial Name'] == row['Commercial Name']:
                    if row2['SSD Percentage'] != '' and float(row2['SSD Percentage']) != 0:
                        gtl['ssd'] = float(row2['SSD Percentage'])
                    if row2['Hard Drive Percentage'] != '' and float(row2['Hard Drive Percentage']) != 0:
                        gtl['hdd'] = float(row2['Hard Drive Percentage'])
                    if row2['Battery Percentage'] != '' and float(row2['Battery Percentage']) != 0:
                        gtl['battery'] = float(row2['Battery Percentage'])
                    if row2['Chassis & Assembly Percentage'] != '' and float(row2['Chassis & Assembly Percentage']) != 0:
                        gtl['chassis'] = float(row2['Chassis & Assembly Percentage'])
                    if row2['Power Supply Percentage'] != '' and float(row2['Power Supply Percentage']) != 0:
                        gtl['power'] = float(row2['Power Supply Percentage'])
                    if row2['Mainboard and Other Boards Percentage'] != '' and float(row2['Mainboard and Other Boards Percentage']) != 0:
                        gtl['mainboard'] = float(row2['Mainboard and Other Boards Percentage'])
                    if row2['Display Percentage'] != '' and float(row2['Display Percentage']) != 0:
                        gtl['display'] = float(row2['Display Percentage'])
                    if row2['Packaging Percentage'] != '' and float(row2['Packaging Percentage']) != 0:
                        gtl['packaging'] = float(row2['Packaging Percentage'])
                    break
            max_pair=max(gtl.items(), key=lambda item: item[1])
            min_pair=min(gtl.items(), key=lambda item: item[1])
            # print(max_pair, min_pair)
            dict_list = []
            if len(interests) == 1 and interests[0] == 'max':
                dict_list.append({max_pair[0]: max_pair[1]})
            elif len(interests) == 1 and interests[0] == 'min':
                dict_list.append({min_pair[0]: min_pair[1]})
            else:
                dict_list.append({max_pair[0]: max_pair[1]})
                dict_list.append({min_pair[0]: min_pair[1]})

        gt_list.append(dict_list)

import pandas as pd
df = pd.read_csv("../output/max_min/hp_multiquestion_pal.csv")
df["Answer"] = gt_list
df.to_csv("../output/max_min/gt_hp_pal.csv", index=False)
