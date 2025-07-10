import csv
import re

def remove_single_quote(value):
    if value.startswith("'"):
        return value[1:]
    return value

gt_list = []
with open('../output/acer_multiquestion_mapping.csv', 'r', newline='') as csvfile:
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

        gtl = []
        with open('../input/Acer_Carbon_Breakdown.csv', 'r', newline='') as csvfile2:
            reader2 = csv.DictReader(csvfile2)
            if interests[0] == 'breakdown':
                for row2 in reader2:
                    if row2['Commercial Name'] == row['Commercial Name']:
                        if row2['Solid State Drive (SSD) Carbon Footprint'] != '' and float(row2['Solid State Drive (SSD) Carbon Footprint']) != 0:
                            gtl.append({'ssd': row2['Solid State Drive (SSD) Carbon Footprint']})
                        if row2['Hard Drive (HDD) Carbon Footprint'] != '' and float(row2['Hard Drive (HDD) Carbon Footprint']) != 0:
                            gtl.append({'hdd': row2['Hard Drive (HDD) Carbon Footprint']})
                        if row2['Batteries Carbon Footprint'] != '' and float(row2['Batteries Carbon Footprint']) != 0:
                            gtl.append({'batteries': row2['Batteries Carbon Footprint']})
                        if row2['Chassis Carbon Footprint'] != '' and float(row2['Chassis Carbon Footprint']) != 0:
                            gtl.append({'chassis': row2['Chassis Carbon Footprint']})
                        if row2['Power Supply Unit & External Cables Carbon Footprint'] != '' and float(row2['Power Supply Unit & External Cables Carbon Footprint']) != 0:
                            gtl.append({'power': row2['Power Supply Unit & External Cables Carbon Footprint']})
                        if row2['Mainboard and other boards Carbon Footprint'] != '' and float(row2['Mainboard and other boards Carbon Footprint']) != 0:
                            gtl.append({'mainboard': row2['Mainboard and other boards Carbon Footprint']})
                        if row2['Display Carbon Footprint'] != '' and float(row2['Display Carbon Footprint']) != 0:
                            gtl.append({'display': row2['Display Carbon Footprint']})
                        if row2['Packaging Carbon Footprint'] != '' and float(row2['Packaging Carbon Footprint']) != 0:
                            gtl.append({'packaging': row2['Packaging Carbon Footprint']})

            #     pass
            # elif len(interests) > 1 and 'breakdown' in interests:
            #     print('No')
            else:
                for row2 in reader2:
                    if row2['Commercial Name'] == row['Commercial Name']:
                        for target in interests:
                            if target == 'ssd':
                                gtl.append(row2['Solid State Drive (SSD) Carbon Footprint'])
                            elif target == 'hdd':
                                gtl.append(row2['Hard Drive (HDD) Carbon Footprint'])
                            elif target == 'batteries':
                                gtl.append(row2['Batteries Carbon Footprint'])
                            elif target == 'chassis':
                                gtl.append(row2['Chassis Carbon Footprint'])
                            elif target == 'power':
                                gtl.append(row2['Power Supply Unit & External Cables Carbon Footprint'])
                            elif target == 'mainboard':
                                gtl.append(row2['Mainboard and other boards Carbon Footprint'])
                            elif target == 'display':
                                gtl.append(row2['Display Carbon Footprint'])
                            elif target == 'packaging':
                                gtl.append(row2['Packaging Carbon Footprint'])
                            elif target == 'odd':
                                gtl.append(row2['ODD2'])
                            elif target == 'external':
                                gtl.append(row2['External components (Keyboard & Mouse)2'])
                            elif target == 'manufacturing':
                                gtl.append(row2['Manufacturing'])
                            elif target == 'total':
                                gtl.append(row2['PCF'])
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
df = pd.read_csv("../output/acer_multiquestion_pal.csv")
df["Answer"] = gt_list
df.to_csv("../output/gt_acer_pal.csv", index=False)
