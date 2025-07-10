import csv
import re
import ast

results_list = []
with open('../output/gt_acer_pal.csv', 'r', newline='') as csvfile:
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
                # print("Answer is", answer)
            # else:
            #     print("No 'answer' variable found in the generated program.")
            results_list.append(result)
        except Exception as e:
            print("Error:", e)

        gt_list = ast.literal_eval(row['Answer'])

        # print(gt_list)
        if len(result) != len(gt_list):
            print('Different lengths error!')
            print(row['Prompt'])
            print(gt_list)
            print(result)
        if interests[0] != 'breakdown':
            gt_list = [float(gt) for gt in gt_list]
            for gt, r in zip(gt_list, result):
                if abs(gt - r) > 1:
                    print('Not equal!')
                    print(row['Prompt'])
                    print(row['Program'])
                    print(gt_list)
                    print(result)
                    print(interests)
                    break
        else: # breakdown
            float_gt_list = []
            for d in gt_list:
                key, value = next(iter(d.items()))
                float_gt_list.append({key:float(value)})

            for d in float_gt_list:
                gt_name, gt_value = next(iter(d.items()))
                found = False
                for d2 in result:
                    r_name, r_value = next(iter(d.items()))
                    if r_name == gt_name and abs(r_value - gt_value) < 0.1:
                        found = True
                if not found:
                    print('Not found')
            # print(gt_list)
            # print(float_gt_list)
            # # print(row['Program'])
            # print(result)
            # print(row['Prompt'])
            # print(type(gt_list[0]))

import pandas as pd
df = pd.read_csv("../output/gt_acer_pal.csv")
# print(len(results_list))
df["Answer_exec"] = results_list
df.to_csv("../output/gt_exec_acer_pal.csv", index=False)
