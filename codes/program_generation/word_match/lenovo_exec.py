import csv
import re
import ast

results_list = []
with open('../output/gt_lenovo_pal.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
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
        gt_list = [float(gt) for gt in gt_list]
        for gt, r in zip(gt_list, result):
            if abs(gt - r) > 0.1:
                print('Not equal!')
                print(row['Prompt'])
                print(row['Program'])
                print(gt_list)
                print(result)
                break

import pandas as pd
df = pd.read_csv("../output/gt_lenovo_pal.csv")
# print(len(results_list))
df["Answer_exec"] = results_list
df.to_csv("../output/gt_exec_lenovo_pal.csv", index=False)
