# coding=utf-8

import requests
import re
import json
import csv
from time import sleep


def get_company_list():
    company_list_url = "http://77.push2.eastmoney.com/api/qt/clist/get"
    param = {
        "cb": "jQuery112406691992199758061_1596720844105",
        "pn": "1",
        "pz": "1",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": "m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23",
        "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
        "_": "1596720844110"
    }

    respons = requests.get(company_list_url, params=param, timeout=10)
    re_pattern = re.compile(r'[(](.*)[)]', re.S)
    re_pattern_data = re.findall(re_pattern, respons.text)[0]
    json_data = json.loads(re_pattern_data)
    total_record = json_data.get('data').get('total')
    page = int(total_record / 1000 + 1)
    fo = open("company_list.txt", "w")
    param["pz"] = 1000

    for i in range(page):
        param["pn"] = i + 1
        respons = requests.get(company_list_url, params=param, timeout=10)
        re_pattern = re.compile(r'[(](.*)[)]', re.S)
        re_pattern_data = re.findall(re_pattern, respons.text)[0]
        json_data = json.loads(re_pattern_data)
        company_data = json_data.get('data').get('diff')
        for row_data in company_data:
            print(row_data.get("f12"), row_data.get("f14"))
            if row_data.get("f12")[0] == "6":
                fo.write("SH" + " " + row_data.get("f12") + " " + row_data.get("f14").strip().replace(" ", "") + "\n")
            else:
                fo.write("SZ" + " " + row_data.get("f12") + " " + row_data.get("f14").strip().replace(" ", "") + "\n")
        sleep(0.5)
    fo.close()


def get_finance_analysis():
    finance_analysis_url = "http://f10.eastmoney.com/NewFinanceAnalysis/MainTargetAjax"
    param = {
        "type": "0"  # 0：按照报告期  1：按年度 2：按单季度
    }

    fo = open("finance_analysis.txt", "w")
    with open("company_list.txt") as f:
        while True:
            company_code_data = f.readline()
            sleep(0.3)
            if company_code_data:
                print(company_code_data)
                try:
                    company_code_data_list = company_code_data.split(" ")
                    code = company_code_data_list[0] + company_code_data_list[1]
                    param["code"] = code
                    respons = requests.get(finance_analysis_url, params=param, timeout=20)
                    body_data = respons.text
                    fo.write(company_code_data.strip('\n') + " " + body_data + "\n")

                except Exception as e:
                    print("data: " + company_code_data)
                    print(e)
            else:
                break
    fo.close()


def merge_finance_data():
    # f_old = open("finance_analysis_old", "r")
    # f_current = open("finance_analysis_20200815.txt", "r")
    # f_new = open("finance_analysis_new.txt", "r")
    old_index = {}
    result_data_list = []
    i = 0
    with open("finance_analysis_20200829.txt", "r") as f_old:
        while True:
            finance_data_old = {}
            old_data = f_old.readline()
            if old_data:
                old_data_split = old_data.split()
                for finance_data_row in json.loads(old_data_split[-1]):
                    finance_data_old[finance_data_row.get("date")] = {"jbmgsy": finance_data_row.get("jbmgsy"),
                                                                      "yyzsr": finance_data_row.get("yyzsr")}
                finance_data_old_with_code = {"code": old_data_split[1], "name": old_data_split[2],
                                              "data": finance_data_old.copy()}
                result_data_list.append(finance_data_old_with_code.copy())
                old_index[old_data_split[1]] = i
                i += 1
            else:
                break

    with open("finance_analysis_20201031.txt", "r") as f_current:
        while True:
            finance_data_current = {}
            current_data = f_current.readline()
            if current_data:
                current_data_split = current_data.split()
                for finance_data_current_row in json.loads(current_data_split[-1]):
                    finance_data_current[finance_data_current_row.get("date")] = {
                        "jbmgsy": finance_data_current_row.get("jbmgsy"),
                        "yyzsr": finance_data_current_row.get("yyzsr")}
                finance_data_current_with_code = {"code": current_data_split[1], "name": current_data_split[2],
                                                  "data": finance_data_current.copy()}
                if old_index.get(current_data_split[1]):
                    result_data_list[old_index.get(current_data_split[1])]["data"].update(finance_data_current.copy())
                else:
                    result_data_list.append(finance_data_current_with_code)

            else:
                break

    with open("finance_analysis_new.txt", "w") as f_new:
        for row in result_data_list:
            f_new.write(str(row) + "\n")
    return result_data_list
    # print(old_index)
    # print(result_data_list[0:10])


def write_to_csv(data):
    out_datas = []
    date_list = ['2017-03-31', '2017-06-30', '2017-09-30', '2017-12-31',
                 '2018-03-31', '2018-06-30', '2018-09-30', '2018-12-31',
                 '2019-03-31', '2019-06-30', '2019-09-30', '2019-12-31',
                 '2020-03-31', '2020-06-30', '2020-09-30']

    for row in data:
        row_data = {}
        row_data['code'] = row.get("code")
        row_data['name'] = row.get("name")
        for (k1, v1) in row.get("data").items():
            if k1 not in date_list:
                continue
            for (k2, v2) in v1.items():
                if k2 == 'jbmgsy':
                    row_data[k1 + "-" + "mg"] = v2
                elif k2 == 'yyzsr':
                    if "万亿" in v2:
                        value = float(v2.strip("万亿")) * 1000000000000
                    else:
                        if "亿" in v2:
                            value = float(v2.strip("亿")) * 100000000
                        elif "万" in v2:
                            value = float(v2.strip("万")) * 10000
                        else:
                            value = v2
                    row_data[k1 + "-" + "ys"] = value
                else:
                    continue
        out_datas.append(row_data.copy())

    with open('test.csv', 'w', newline='', encoding='utf-8') as f:
        header = ['code', 'name',
                  '2017-03-31-mg', '2017-03-31-ys', '2017-06-30-mg', '2017-06-30-ys', '2017-09-30-mg', '2017-09-30-ys', '2017-12-31-mg', '2017-12-31-ys',
                  '2018-03-31-mg', '2018-03-31-ys', '2018-06-30-mg', '2018-06-30-ys', '2018-09-30-mg', '2018-09-30-ys', '2018-12-31-mg', '2018-12-31-ys',
                  '2019-03-31-mg', '2019-03-31-ys', '2019-06-30-mg', '2019-06-30-ys', '2019-09-30-mg', '2019-09-30-ys', '2019-12-31-mg', '2019-12-31-ys',
                  '2020-03-31-mg', '2020-03-31-ys', '2020-06-30-mg', '2020-06-30-ys', '2020-09-30-mg', '2020-09-30-ys']
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(out_datas)


if __name__ == '__main__':
    # get_company_list()
    # get_finance_analysis()
    # 将finance_analysis.txt名称修改为finance_analysis_2020xxxx.txt格式，并修改2个with open里面的文件名后执行
    merge_data_list = merge_finance_data()
    write_to_csv(merge_data_list)
