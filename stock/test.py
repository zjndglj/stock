import re
import json


fo1 = open("finance_analysis_1.txt", "r")
fo2 = open("finance_analysis_2.txt", "r")

# re_pattern = re.compile(r'\[(.*)\]', re.S)

while True:
    dict1 = {}
    dict2 = {}
    data1 = fo1.readline()
    print(data1.split()[-1])
    json_data1 = json.loads(data1.split()[-1])
    for row in json_data1:
        dict1[row.get("date")] = {"jbmgsy": row.get("jbmgsy"),
                                  "yyzsr": row.get("yyzsr")}
    dict_a1 = {"code": data1.split()[1], "name": data1.split()[2], "data": dict1.copy()}
    data2 = fo2.readline()
    print(data2.split()[-1])
    json_data2 = json.loads(data2.split()[-1])
    for row in json_data2:
        dict2[row.get("date")] = {"jbmgsy": row.get("jbmgsy"),
                                  "yyzsr": row.get("yyzsr")}
    dict_a2 = {"code": data2.split()[1], "name": data2.split()[2], "data": dict2.copy()}

    if dict_a1["code"] == dict_a2["code"]:
        data_merge = dict_a1.get("data").update(dict_a2.get("data"))
        print(dict_a1)
    # dict1.update(dict2)
    # print(dict1)
    break
