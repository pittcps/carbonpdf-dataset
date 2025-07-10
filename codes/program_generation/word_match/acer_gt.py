import csv
import re

gt_list = []
with open('../output/word_match/acer_multiquestion_mapping.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        gtl = []
        str = row['Interests']
        interests = str.split(',')
        interests = [i.strip().lower() for i in interests]
        i_temp = []
        for i in interests:
            i2 = i.split()
            i_temp.append(i2[0])
        interests = i_temp

        with open('../input/Acer_Carbon_Breakdown.csv', 'r', newline='') as csvfile2:
            reader2 = csv.DictReader(csvfile2)
            for row2 in reader2:
                if row2['Commercial Name'] == row['Commercial Name']:
                    for target in interests:
                        if target == 'ssd':
                            gtl.append(row2['SSD Percentage'])
                        elif target == 'hdd':
                            gtl.append(row2['Hard Drive Percentage'])
                        elif target == 'battery':
                            gtl.append(row2['Battery Percentage'])
                        elif target == 'chassis':
                            gtl.append(row2['Chassis & Assembly Percentage'])
                        elif target == 'power':
                            gtl.append(row2['Power Supply Percentage'])
                        elif target == 'mainboard':
                            gtl.append(row2['Mainboard and Other Boards Percentage'])
                        elif target == 'display':
                            gtl.append(row2['Display Percentage'])
                        elif target == 'packaging':
                            gtl.append(row2['Packaging Percentage'])
                        elif target == 'manufacturing':
                            gtl.append(row2['Manufacturing Percentage'])
                    break
        # print(interests)
        # print(gtl)
        gt_list.append(gtl)

# with open('../../out/gt_hp_pal.csv', 'w', newline='') as csvfile:
# # with open('../output/mapping_compute.csv', 'w', newline='') as csvfile:
#     fieldnames = ['Answer']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#
#     writer.writeheader()
#
#     for answer in gt_list:
#         if answer:
#             writer.writerow({'Answer': answer})

import pandas as pd
df = pd.read_csv("../output/word_match/acer_multiquestion_pal.csv")
df["Answer"] = gt_list
df.to_csv("../output/word_match/gt_acer_pal.csv", index=False)
