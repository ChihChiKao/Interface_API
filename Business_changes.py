# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import io
import sys
import requests
from bs4 import BeautifulSoup
import os
import urllib.request
import pandas as pd
import re
import shutil
import numpy as np
import datetime  


# %%
str_time = str(input('請輸入開始日期(西元年月日(共8碼))：'))
end_time = str(input('請輸入結束日期(西元年月日(共8碼))：'))


# %%
datestart=datetime.datetime.strptime(str_time,'%Y%m%d')  
dateend=datetime.datetime.strptime(end_time,'%Y%m%d')
#計算中間日期
time=[]
while datestart<dateend:  
    datestart+=datetime.timedelta(days=1)  
    #print(datestart.strftime('%Y%m%d'))
    time.append(datestart.strftime('%Y%m%d'))
time.insert(0,str_time)
#轉民國
all_time=[]
for i in time:
    #print(int(i)-19110000)
    all_time.append(int(i)-19110000)
    #print(type(i))


# %%
AGENCYCODE=["376410000A","379100000G","383100000G","376570000A","376580000A","376590000A","376610000A","376600000A","376430000A","376440000A","376420000A","376450000A","376470000A","376480000A","376490000A","376500000A","376530000A","376560000A","376550000A","376540000A","371010000A","371030000A"]
AGENCYNAME=["新北市政府經濟發展局","臺北市商業處","高雄市政府","基隆市政府","新竹市政府","臺中市政府","臺南市政府","嘉義市政府","桃園市政府","新竹縣政府","宜蘭縣政府",
"苗栗縣政府","彰化縣政府","南投縣政府","雲林縣政府","嘉義縣政府","屏東縣政府","澎湖縣政府",'花蓮縣政府','臺東縣政府','福建省金門縣政府','福建省連江縣政府']
#Commercial_application=pd.DataFrame(columns = ["AGENCYCODE","AGENCYNAME"])#建立空的datafram
Commercial_application={'機關代碼':AGENCYCODE ,'登記機關':AGENCYNAME}
Commercial_application = pd.DataFrame.from_dict(Commercial_application, orient='index')
Commercial_application=Commercial_application.transpose()#把欄位顛倒過來
#Commercial_application


# %%
skip=0 #每次從第0比開始抓
all_data= pd.DataFrame(columns = ["登記機關","商業統一編號","商業名稱","現況"])#建立空的datafram
for j in all_time:#跑全部日期
    print(j) 
    for skip in range(500000):#從第0筆開始抓
        r=requests.get("http://data.gcis.nat.gov.tw/od/data/api/9B84E7EF-7DEE-4426-A53D-059113F6B1E3?$format=xml&$filter=Business_Last_Change_Date eq "+str(j)+"&$skip="+str(skip)+"&$top=1")
        soup = BeautifulSoup(r.text, "html.parser")
        if len(soup.find_all("row")) ==0:
            #print(False)
            break
        #print(soup.prettify())
        president_no=soup.find('president_no').text #商業統一編號
        agency_desc=soup.find('agency_desc').text #登記機關
        business_name=soup.find('business_name').text #商業名稱
        business_current_status_desc=soup.find('business_current_status_desc').text #現況
        #print(skip)
        #print(president_no)
        #for Number in soup.find_all('president_no'):
            #all_data= pd.DataFrame(columns = ["登記機關","商業統一編號","商業名稱","現況"])#建立空的datafram
        #print(president_no)
        all_data=all_data.append({'登記機關':agency_desc ,'商業統一編號':president_no , '商業名稱':business_name,'現況':business_current_status_desc},                                           ignore_index=True)
        #company_information=company_information.append(all_data,ignore_index=True)
    df3 = pd.merge(all_data, Commercial_application)
    df3 = df3[df3["現況"]=="核准設立"]
    #break


# %%
data= pd.DataFrame(columns = ["商業統一編號","商業名稱","商業狀況代碼","商業狀況","資本額","負責人","企業組織類型","業務組織類型描述",
                              "機構","機構名稱","地址","業務設置批准日期","業務更改批准日期","關係人姓名","關係人職責","關係人職責名稱","關係人資本"])#建立空的datafram

for index,row in df3[["商業統一編號","機關代碼"]].iterrows():
    #print(row["商業統一編號"])
    r2=requests.get("https://data.gcis.nat.gov.tw/od/data/api/7E6AFA72-AD6A-46D3-8681-ED77951D912D?$format=xml&$filter=President_No eq "+row["商業統一編號"]+" and Agency eq "+row["機關代碼"])
    soup2 = BeautifulSoup(r2.text, "html.parser")
    #print(soup2.prettify())
    president_no=soup2.find('president_no').text #商業統一編號
    business_name=soup2.find('business_name').text #商業名稱
    business_current_status=soup2.find('business_current_status').text #商業狀況代碼
    business_current_status_desc=soup2.find('business_current_status_desc').text #商業狀況
    business_register_funds=soup2.find('business_register_funds').text #資本額
    responsible_name=soup2.find('responsible_name').text #負責人
    business_organization_type=soup2.find('business_organization_type').text #企業組織類型
    business_organization_type_desc=soup2.find('business_organization_type_desc').text #業務組織類型描述
    agency=soup2.find('agency').text #機構
    agency_desc=soup2.find('agency_desc').text #機構名稱
    business_address=soup2.find('business_address').text #地址
    business_setup_approve_date=soup2.find('business_setup_approve_date').text #業務設置批准日期
    business_last_change_date=soup2.find('business_last_change_date').text #業務更改批准日期
    print(president_no)
    business_director=soup2.select('business_director')[0].text
    business_director=str(business_director)[2:-2]
    wordlist = business_director.split(',')
    Business_Duty=wordlist[0].replace('Business_Duty=', '') #業務職責
    Business_Duty_Desc=wordlist[1].replace('Business_Duty_Desc=', '')#關係人職責名稱
    Name=wordlist[2].replace('Name=', '')#關係人姓名
    Funds=wordlist[3].replace('Funds=', '')#關係人資本

    data=data.append({"商業統一編號":president_no,"商業名稱":business_name,"商業狀況代碼":business_current_status,"商業狀況":business_current_status_desc
                      ,"資本額":business_register_funds,"負責人":responsible_name,"企業組織類型":business_organization_type
                      ,"業務組織類型描述":business_organization_type_desc,"機構":agency,"機構名稱":agency_desc,"地址":business_address
                      ,"業務設置批准日期":business_setup_approve_date,"業務更改批准日期":business_last_change_date,"關係人姓名":Name
                      ,"關係人職責":Business_Duty,"關係人職責名稱":Business_Duty_Desc,"關係人資本":Funds},ignore_index=True)
data.to_csv(r'C:\Users\商業異動查詢.csv', index=False,encoding="utf_8_sig" )
    #break

# %% [markdown]
# ----------------------------------------------------------------------------------------------------------------

# %%



