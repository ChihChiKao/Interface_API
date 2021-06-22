#!/usr/bin/env python
# coding: utf-8

# In[7]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime  
import time


# In[2]:


str_time = str(input('請輸入開始日期(西元年月日(共8碼))：'))
end_time = str(input('請輸入結束日期(西元年月日(共8碼))：'))


# In[3]:



#start='2016-06-01'  
#end='2017-01-01'  

datestart=datetime.datetime.strptime(str_time,'%Y%m%d')  
dateend=datetime.datetime.strptime(end_time,'%Y%m%d')
#計算中間日期
time_day=[]
while datestart<dateend:  
    datestart+=datetime.timedelta(days=1)  
    #print(datestart.strftime('%Y%m%d'))
    time_day.append(datestart.strftime('%Y%m%d'))
time_day.insert(0,str_time)
#轉民國
all_time=[]
for i in time_day:
    #print(int(i)-19110000)
    all_time.append(int(i)-19110000)
    #print(type(i))


# In[6]:


skip=0 #每次從第0比開始抓
company_information=pd.DataFrame(columns = ["統一編號","公司狀況","公司名稱","資本總額(登記資本額)","實收資本額",
                                          "代表人姓名","公司登記地址","登記機關名稱","核准設立日期","最後核准變更日期","公司撤銷日期",
                                          "停復業狀況","停復業狀況描述","停業核准日期","停業/延展期間(起)","停業/延展期間(迄)"])#建立空的datafram
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
for j in all_time:#跑全部日期
    print(j) 
    for skip in range(500000):#從第0筆開始抓
        r=requests.get("http://data.gcis.nat.gov.tw/od/data/api/4347A009-6489-4F19-AC79-78F366BE7976?$format=xml&$filter=Change_Of_Approval_Data eq "+str(j)+"&$skip="+str(skip)+"&$top=1", headers=headers)
        r.close()
        soup = BeautifulSoup(r.text, "html.parser")
        #if soup.find_all("row")
        # 提取span标签的内容
        #if soup("div row") == False:
            #print("空值!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            #continue  
        #else:
        if len(soup.find_all("row")) ==0:
            #print(False)
            break
        #列出全部統一編號
        for Number in soup.find_all('business_accounting_no'):
            all_data= pd.DataFrame(columns = ["統一編號","公司狀況","公司名稱","資本總額(登記資本額)","實收資本額",
                                          "代表人姓名","公司登記地址","登記機關名稱","核准設立日期","最後核准變更日期","公司撤銷日期",
                                          "停復業狀況","停復業狀況描述","停業核准日期","停業/延展期間(起)","停業/延展期間(迄)"])#建立空的datafram
            a=[]#序號(應用三)
            b=[]#營業項目代碼(應用三)
            c=[]#營業項目(應用三)
            d=[]#公司名稱(應用三)
            #soup.find_all('business_accounting_no')
            #print(Number)
            print(Number.text)
            #串接到應用一的資料
            one=requests.get("http://data.gcis.nat.gov.tw/od/data/api/5F64D864-61CB-4D0D-8AD9-492047CC1EA6?$format=xml&$filter=Business_Accounting_NO eq "+Number.text+"&$skip=0&$top=1")
            #print(r)
            #公司登記基本資料-應用一
            soup1 = BeautifulSoup(one.text, "html.parser")
            #公司登記基本資料-應用一(欄位)
            company_status_desc=soup1.find('company_status_desc').text #公司狀況
            company_name=soup1.find('company_name').text #公司名稱
            capital_stock_amount=soup1.find('capital_stock_amount').text #資本總額
            paid_in_capital_amount=soup1.find('paid_in_capital_amount').text #實收資本額
            responsible_name=soup1.find('responsible_name').text #代表人姓名
            company_location=soup1.find('company_location').text #公司登記地址
            register_organization_desc=soup1.find('register_organization_desc').text #登記機關名稱
            company_setup_date=soup1.find('company_setup_date').text #核准設立日期
            change_of_approval_data=soup1.find('change_of_approval_data').text #最後核准變更日期
            revoke_app_date=soup1.find('revoke_app_date').text #公司撤銷日期
            case_status=soup1.find('case_status').text #停復業狀況
            case_status_desc=soup1.find('case_status_desc').text #停復業狀況描述
            sus_app_date=soup1.find('sus_app_date').text #停業核准日期
            sus_beg_date=soup1.find('sus_beg_date').text #停業/延展期間(起)
            sus_end_date=soup1.find('sus_end_date').text #停業/延展期間(迄)
            #print("success")
            #串接到應用二的資料
            #two=requests.get("http://data.gcis.nat.gov.tw/od/data/api/F05D1060-7D57-4763-BDCE-0DAF5975AFE0?$format=xml&$filter=Business_Accounting_NO eq "+Number.text+"&$skip=0&$top=1")
            #公司登記基本資料-應用二
            #soup2 = BeautifulSoup(two.text, "html.parser")
            #公司登記基本資料-應用二(欄位)
            #company_status=soup2.find('company_status').text #公司狀況代碼
            #company_status_desc=soup2.find('company_status_desc').text #公司狀態說明
            all_data=all_data.append({'統一編號':Number.text , '公司狀況':company_status_desc , '公司名稱':company_name
                                      , '資本總額(登記資本額)':capital_stock_amount
                                      ,'實收資本額':paid_in_capital_amount , '代表人姓名':responsible_name,'公司登記地址':company_location 
                                      ,'登記機關名稱':register_organization_desc , '核准設立日期':company_setup_date,
                                      '最後核准變更日期':change_of_approval_data , '公司撤銷日期':revoke_app_date,
                                      '停復業狀況':case_status , '停復業狀況描述':case_status_desc,'停業核准日期':sus_app_date , 
                                      '停業/延展期間(起)':sus_beg_date , '停業/延展期間(迄)':sus_end_date 
                                      },ignore_index=True)
            company_information=company_information.append(all_data,ignore_index=True)
            #print(all_data)

            #print(skip)
    #finally:
    time.sleep(5)

company_information.to_csv(r'C:\Users\公司登記名冊.csv', index=False,encoding="utf_8_sig" )
#print("查詢完畢")


# In[5]:





# In[ ]:




