# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import requests
from bs4 import BeautifulSoup
import os
import urllib.request
import pandas as pd
import re
import shutil
# import datetime from dateutil.parser
#import parse
import numpy as np


# %%
key_name = str(input('請輸入關鍵字：'))


# %%
Business_Current_Status = ['01', '02', '03',
                           '04', '05', '06', '07', '08', '09']
Business_Current_Status_Desc = [
    '核准設立', '停業', '歇業／撤銷', '申覆（辯）期', '遷他縣市', '列入廢止中', '廢止', '破產', '設立無效']
Business_status_code = {'狀態代碼': Business_Current_Status,
                        '狀態': Business_Current_Status_Desc}
Business_status_code = pd.DataFrame.from_dict(
    Business_status_code, orient='index')
Business_status_code = Business_status_code.transpose()  # 把欄位顛倒過來
# Business_status_code["狀態代碼"]


# %%
skip = 0
all_data = pd.DataFrame(columns=["商業統一編號", "商業名稱", "代表人姓名", "公司地址", "資本額",
                                 "商業狀態", "商業狀態描述", "登記機關", "登記機關名稱", "核准設立日期", "變更日期"])  # 建立空的datafram
for code in Business_status_code["狀態代碼"]:
    # print(code)
    for skip in range(500000):  # 從第0筆開始抓
        # print(skip)
        r = requests.get("https://data.gcis.nat.gov.tw/od/data/api/312E00AC-ABBF-487D-9376-A28E7C8AEF61?$format=xml&$filter=Business_Name like " +
                         key_name + " and Business_Current_Status eq "+code+"&$skip="+str(skip) + "&$top=1")
        soup = BeautifulSoup(r.text, "html.parser")
        # print(soup.prettify)
        if len(soup.find_all("row")) == 0:
            # print(False)
            break
        president_no = soup.find('president_no').text  # 商業統一編號
        print(president_no)
        business_name = soup.find('business_name').text  # 商業名稱
        responsible_name = soup.find('responsible_name').text  # 代表人姓名
        business_address = soup.find('business_address').text  # 公司地址
        business_register_funds = soup.find(
            'business_register_funds').text  # 資本額
        business_current_status = soup.find(
            'business_current_status').text  # 商業狀態
        business_current_status_desc = soup.find(
            'business_current_status_desc').text  # 商業狀態描述
        agency = soup.find('agency').text  # 登記機關
        agency_desc = soup.find('agency_desc').text  # 登記機關名稱
        business_setup_approve_date = soup.find(
            'business_setup_approve_date').text  # 核准設立日期
        business_last_change_date = soup.find(
            'business_last_change_date').text  # 變更日期
        all_data = all_data.append({'商業統一編號': president_no, '商業名稱': business_name, '代表人姓名': responsible_name, '公司地址': business_address,
                                    '資本額': business_register_funds, '商業狀態': business_current_status, '商業狀態描述': business_current_status_desc,
                                    '登記機關': agency, '登記機關名稱': agency_desc, '核准設立日期': business_setup_approve_date,
                                    '變更日期': business_last_change_date}, ignore_index=True)

    # break
all_data.to_csv(r'C:\Users\八大行業商業查詢.csv', index=False, encoding="utf_8_sig")
