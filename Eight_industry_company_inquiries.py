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
import numpy as np


# %%
key_name = str(input('請輸入關鍵字：'))


# %%
Company_Status = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
                  '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33']
Company_Status_Desc = ['核准設立', '核准設立，但已命令解散', '重整', '解散', '撤銷', '破產', '合併解散', '撤回認許', '廢止', '廢止認許', '解散已清算完結', '撤銷已清算完結', '廢止已清算完結', '撤回認許已清算完結', '撤銷認許已清算完結', '廢止認許已清算完結',
                       '撤銷認許', '分割解散', '終止破產', '中止破產', '塗銷破產', '破產程序終結(終止)', '破產程序終結(終止)清算中', '破產已清算完結', '接管', '撤銷無需清算', '撤銷許可', '廢止許可', '撤銷許可已清算完結', '廢止許可已清算完結', '清理', '撤銷公司設立', '清理完結']
Company_status_code = {'狀態代碼': Company_Status, '狀態': Company_Status_Desc}
Company_status_code = pd.DataFrame.from_dict(
    Company_status_code, orient='index')
Company_status_code = Company_status_code.transpose()  # 把欄位顛倒過來
# Company_status_code["狀態代碼"]


# %%
skip = 0
all_data = pd.DataFrame(columns=["公司統一編號", "公司名稱", "代表人姓名", "公司登記地址", "公司狀況代碼", "公司狀況描述",
                                 "資本總額(元)", "實收資本額(元)", "登記機關代碼", "登記機關名稱", "核准設立日期", "最後核准變更日期"])  # 建立空的datafram
for code in Company_status_code["狀態代碼"]:
    print(code)
    for skip in range(500000):  # 從第0筆開始抓
        # print(skip)
        r = requests.get("https://data.gcis.nat.gov.tw/od/data/api/8813AADD-D020-4C55-A703-FC15B49F4262?$format=xml&$filter=Company_Name like " +
                         key_name + " and Company_Status eq "+code+"&$skip="+str(skip) + "&$top=1")
        soup = BeautifulSoup(r.text, "html.parser")
        # print(soup.prettify)
        if len(soup.find_all("row")) == 0:
            # print(False)
            break
        business_accounting_no = soup.find(
            'business_accounting_no').text  # 公司統一編號
        print(business_accounting_no)
        company_name = soup.find('company_name').text  # 公司名稱
        responsible_name = soup.find('responsible_name').text  # 代表人姓名
        company_location = soup.find('company_location').text  # 公司登記地址
        company_status = soup.find('company_status').text  # 公司狀況代碼
        company_status_desc = soup.find('company_status_desc').text  # 公司狀況描述
        capital_stock_amount = soup.find(
            'capital_stock_amount').text  # 資本總額(元)
        paid_in_capital_amount = soup.find(
            'paid_in_capital_amount').text  # 實收資本額(元)
        register_organization = soup.find(
            'register_organization').text  # 登記機關代碼
        register_organization_desc = soup.find(
            'register_organization_desc').text  # 登記機關名稱
        company_setup_date = soup.find('company_setup_date').text  # 核准設立日期
        change_of_approval_data = soup.find(
            'change_of_approval_data').text  # 最後核准變更日期
        all_data = all_data.append({'公司統一編號': business_accounting_no, '公司名稱': company_name, '代表人姓名': responsible_name,
                                    '公司登記地址': company_location, '公司狀況代碼': company_status, '公司狀況描述': company_status_desc,
                                    '資本總額(元)': capital_stock_amount, '實收資本額(元)': paid_in_capital_amount, '登記機關代碼': register_organization,
                                    '登記機關名稱': register_organization_desc, '核准設立日期': company_setup_date,
                                    '最後核准變更日期': change_of_approval_data}, ignore_index=True)
    # break
all_data.to_csv(r'C:\Users\八大行業公司查詢.csv', index=False, encoding="utf_8_sig")


# %%
