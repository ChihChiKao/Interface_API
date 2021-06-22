#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime  
import time
from hashlib import sha1
import hmac
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import base64


# In[2]:


app_id = '2d16769d481b4ab69ec6ecb0ccd0672b'
app_key = 'dbr3zEbzwX8cj1Yv7ZxGzb4IpAc'
class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + self.app_id + '", ' +                         'algorithm="hmac-sha1", ' +                         'headers="x-date", ' +                         'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }


# In[4]:


city=['NewTaipei','Taoyuan','Taichung','Tainan','Kaohsiung','Keelung','Hsinchu','HsinchuCounty','MiaoliCounty','ChanghuaCounty'
,'NantouCounty','YunlinCounty','ChiayiCounty','Chiayi','PingtungCounty','YilanCounty','HualienCounty','TaitungCounty'
,'KinmenCounty','PenghuCounty','LienchiangCounty','Taipei']
Bike_allshape=pd.DataFrame(columns = ['路線名稱','業管機關名稱','路線所在縣市代碼',"路線所在縣市名稱"
                                   ,"路線所在鄉鎮名稱",'路線起點描述','路線迄點描述',"自行車道車行方向"
                                   ,"自行車道長度","自行車道完工日期時間","資料更新日期時間",'路線軌跡資料'])
for j in city:
    print(j)
    a = Auth(app_id, app_key)
    r=requests.get("https://ptx.transportdata.tw/MOTC/v2/Cycling/Shape/"+str(j)+"?$format=xml", headers= a.get_auth_header())
    r.close()
    soup = BeautifulSoup(r.text, "html.parser")
    #for i in soup.find_all('busstation'): #每次跑一個站的資料
    #print(soup.prettify())
        #print(j)
    #print(j)
    #for j in i.find_all("stops"):
    routename = [routename.text for routename in soup.find_all('routename')]
    authorityname = [authorityname.text for authorityname in soup.find_all('authorityname')]
    citycode = [citycode.text for citycode in soup.find_all('citycode')]
    city = [i.text for i in soup.find_all('city')]
    town = [town.text for town in soup.find_all('town')]
    roadsectionstart = [roadsectionstart.text for roadsectionstart in soup.find_all('roadsectionstart')]
    roadsectionend = [roadsectionend.text for roadsectionend in soup.find_all('roadsectionend')]
    Direction = [direction.text for direction in soup.find_all('direction')]
    
    cyclinglength = [cyclinglength.text for cyclinglength in soup.find_all('cyclinglength')]
    finishedtime = [i.text for i in soup.find_all('finishedtime')]
    updatetime = [i.text for i in soup.find_all('updatetime')]
    geometry = [geometry.text for geometry in soup.find_all('geometry')]
    #srcupdatetime = [srcupdatetime.text for srcupdatetime in soup.find_all('srcupdatetime')]
    #UpdateTime = [updatetime.text for updatetime in soup.find_all('updatetime')]
    #VersionID = [versionid.text for versionid in i.find_all('versionid')]

    Bike_shape={'路線名稱':routename,'業管機關名稱':authorityname,'路線所在縣市代碼':citycode
        ,"路線所在縣市名稱":city,"路線所在鄉鎮名稱":town,'路線起點描述':roadsectionstart
        ,'路線迄點描述':roadsectionend,"自行車道車行方向":Direction,"自行車道長度":cyclinglength
        ,"自行車道完工日期時間":finishedtime,"資料更新日期時間":updatetime,'路線軌跡資料':geometry}
    #print(Bus_information)
    Bike_shape = pd.DataFrame.from_dict(Bike_shape, orient='index')
    Bike_shape=Bike_shape.transpose()#把欄位顛倒過來
    Bike_allshape=Bike_allshape.append(Bike_shape)
    time.sleep(5)
    #print(Bike_shape)
    #break


# In[5]:


Bike_allshape.to_csv(r'C:\Users\指定縣市之自行車道路網圖資.txt', index=False,encoding="utf_8_sig" )


# In[ ]:




