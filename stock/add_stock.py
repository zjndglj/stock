# coding=utf-8

import requests
import re
import json
import csv
from time import sleep


def add_stock():
    stockcode_pre_0 = "0"
    stockcode_pre_1 = "1"
    company_list_url = "http://quote.eastmoney.com/zixuan/api/zxg/addstock"
    data = {
        "groupid": "445414800",
        "stockcode": ""
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Cookie": "qgqp_b_id=f3890fbd3176439a8cf0bec18cc8dcdd; em_hq_fls=js; intellpositionL=1522.39px; ct=dY0xxV51vgddPYszmsKwMQ0nowWR-MbRtN4Hgh375NVdz_ebNe1NSKYDxQzH2jipr7B6ILNQ8hgRbF5t4nsqPOv5xdS17QtoaEfsL0Dz_z3gm5lx3QRDDONWGvCVqMBPqk8Z8W4Y5Xeqc4wWlPtQj1Sa3fKsrSvrU417YehVtfI; ut=FobyicMgeV5ghfUPKWOH56yX_VkX7Ao3Yr_d0v3TxJt9g-LgKdEav4eKglnKB40GhksRpjwPrXVEzLJjtGvP2TBCMaR6NFgNiBhL_LAoMT0O3Q1Orq83EGmjAwT-Tv8yi3KwAlr4J7MTbU_fbpQ7R3p3El1iJ2UcebHoi1sHKmGm6tyHInvDhil4DbjNbk9AA3rchfApElUrH1PN8wL7hF7LjryV7mmnBKgonbOr1Md0XARCzRFxomOVPO0wJ8R0YUAJ3n7ShJieuY7rbLzxlbBUFrNBsbjo; pi=4018335786074910%3bn4018335786074910%3b%e8%82%a1%e5%8f%8bhAENKq%3bAkMckL3%2bkcd0LJrn6Hg8AqkIzVf18KX%2bG9SAy9jQK2nyQGToJ5pUIGtDad5okI%2b2LDL%2f4%2b0DbyGdwsDNRqV7Cu2cazGsSOeKsQ8XlUsZ%2bmg4EH68LjX%2f5gZo4k16%2fTjAt8s4R3bTpNAosU0hcx76P8xRYg%2f8uvbyv2OGZlYSU%2fkBneM02ZI4q7N8%2bKjieA%2bAfgNYgS%2b1%3bpPOSGx8yyxcCTlQp%2fn%2fkuKl%2bO7O79Ql%2fhENCokWNav%2bfUdJMdoZcjXLQyVwVJwRREo6mFo0IadfMRo00PYPGJFl6RmhCHMWDIgOii9P3QFQkxrx%2f%2f88NuODjLRNAMsYKRlyAubFwApNIYRMpfHi8zM%2fRWAwAFg%3d%3d; uidal=4018335786074910%e8%82%a1%e5%8f%8bhAENKq; sid=141686415; vtpst=|; em-quote-version=topspeed; emhq_picfq=1; emshistory=%5B%22%E8%82%A1%E7%A5%A8%E5%88%97%E8%A1%A8%22%2C%22002959%22%2C%22300829%22%2C%22002214%22%2C%22300866%22%2C%22300868%22%2C%22688556%22%5D; intellpositionT=1055px; st_si=72235599404522; waptgshowtime=2020829; isoutside=0; HAList=a-sz-002768-%u56FD%u6069%u80A1%u4EFD%2Ca-sh-688398-%u8D5B%u7279%u65B0%u6750%2Ca-sh-688202-%u7F8E%u8FEA%u897F%2Ca-sz-002975-%u535A%u6770%u80A1%u4EFD%2Ca-sh-688278-%u7279%u5B9D%u751F%u7269%2Ca-sh-688111-%u91D1%u5C71%u529E%u516C%2Ca-sh-688166-%u535A%u745E%u533B%u836F%2Ca-sh-603489-%u516B%u65B9%u80A1%u4EFD%2Ca-sh-688299-%u957F%u9633%u79D1%u6280%2Ca-sh-688399-%u7855%u4E16%u751F%u7269%2Ca-sz-300021-%u5927%u79B9%u8282%u6C34%2Ca-sh-600262-%u5317%u65B9%u80A1%u4EFD%2Ca-sz-002254-%u6CF0%u548C%u65B0%u6750; st_pvi=85391273294842; st_sp=2020-08-06%2021%3A21%3A26; st_inirUrl=https%3A%2F%2Fwww.eastmoney.com%2F; st_sn=13; st_psi=20200829163707436-113200301712-0502880677; st_asi=20200829163707436-113200301712-0502880677-Web_so_zq-2",
        "Host": "quote.eastmoney.com",
        "Origin": "http://quote.eastmoney.com",
        "Referer": "http://quote.eastmoney.com/zixuan/?from=home"
    }

    with open('add_stock_list.txt', 'r') as f:
        while True:
            stock_code = f.readline()
            if stock_code[0] == '6':
                data["stockcode"] = stockcode_pre_1 + "." + stock_code
            else:
                data["stockcode"] = stockcode_pre_0 + "." + stock_code
            respons = requests.post(company_list_url, data=data, headers=headers, timeout=10)
            print(stock_code, respons.status_code)
            sleep(0.5)


if __name__ == '__main__':
    add_stock()
