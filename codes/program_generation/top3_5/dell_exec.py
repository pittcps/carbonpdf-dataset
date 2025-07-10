import csv
import re
import ast

results_list = []
with open('../output/top5/gt_dell_pal.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        str = row['Interests']
        interests = str.split(',')
        interests = [i.strip().lower() for i in interests]
        i_temp = []
        for i in interests:
            i2 = i.split()
            i_temp.append(i2[0])
        interests = i_temp

        program = row['Program']
        pattern = r'```(?:python)?(.*?)```'
        matches = re.findall(pattern, program, re.DOTALL)
        first_match = matches[0] if matches else "" # -1

        result = []
        try:
            if 'answer' in locals():
                del answer
            exec(first_match)
            if 'answer' in locals():
                result = answer
                results_list.append(result)
                # print("Answer is", answer)
            else:
                print("No 'answer' variable found in the generated program.")
        except Exception as e:
            print("Error:", e)

        gt_list = ast.literal_eval(row['Answer'])

        # print(gt_list)
        if len(result) != len(gt_list):
            print('Different lengths error!')
            print(row['Prompt'])
            print(gt_list)
            print(result)
        float_gt_list = []
        for d in gt_list:
            key, value = next(iter(d.items()))
            float_gt_list.append({key:float(value)})

        for d in float_gt_list:
            gt_name, gt_value = next(iter(d.items()))
            found = False
            for d2 in result:
                r_name, r_value = next(iter(d.items()))
                if r_name == gt_name and abs(r_value - gt_value) < 0.01:
                    found = True
            if not found:
                print('Not found')

import pandas as pd
df = pd.read_csv("../output/top5/gt_dell_pal.csv")
# print(len(results_list))
df["Answer_exec"] = results_list
df.to_csv("../output/top5/gt_exec_dell_pal.csv", index=False)
