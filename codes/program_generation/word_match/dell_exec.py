import csv
import re
import ast

results_list = []
with open('../output/word_match/gt_dell_pal.csv', 'r', newline='') as csvfile:
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
        gt_list = [float(gt) for gt in gt_list]
        for gt, r in zip(gt_list, result):
            if abs(gt - r) > 0.01:
                print('Not equal!')
                print(row['Prompt'])
                print(row['Program'])
                print(gt_list)
                print(result)
                print(interests)
                break

import pandas as pd
df = pd.read_csv("../output/word_match/gt_dell_pal.csv")
# print(len(results_list))
df["Answer_exec"] = results_list
df.to_csv("../output/word_match/gt_exec_dell_pal.csv", index=False)
