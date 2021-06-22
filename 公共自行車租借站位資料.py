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


# In[3]:


city=['NewTaipei','Taoyuan','Taichung','Tainan','Kaohsiung','Keelung','Hsinchu','HsinchuCounty','MiaoliCounty','ChanghuaCounty'
,'NantouCounty','YunlinCounty','ChiayiCounty','Chiayi','PingtungCounty','YilanCounty','HualienCounty','TaitungCounty'
,'KinmenCounty','PenghuCounty','LienchiangCounty','Taipei']
Bike_information=pd.DataFrame(columns = ['站點唯一識別代碼','站點代碼','業管單位代碼',"站點中文名稱","站點英文名稱"
                                         ,'位置緯度(WGS84)','位置經度(WGS84)',"地理空間編碼","站牌中文地址","站牌英文地址"
                                         ,"可容納之自行車總數","資料版本編號",'資料更新日期時間'])
for j in city:
    print(j)
    a = Auth(app_id, app_key)
    r=requests.get("https://ptx.transportdata.tw/MOTC/v2/Bike/Station/"+str(j)+"?$format=xml", headers= a.get_auth_header())
    r.close()
    soup = BeautifulSoup(r.text, "html.parser")
    #for i in soup.find_all('bikestation'): #每次跑一個站的資料
    #print(soup.prettify())
    #print(j)
    #for j in i.find_all("stops"):
    stationuid = [stationuid.text for stationuid in soup.find_all('stationuid')]
    stationid = [stationid.text for stationid in soup.find_all('stationid')]
    authorityid = [authorityid.text for authorityid in soup.find_all('authorityid')]
    StopName_zh_tw = [i.zh_tw.text for i in soup.find_all('stationname')]
    StopName_En = [en.text for en in soup.find_all('stationname')]
    PositionLat = [positionlat.text for positionlat in soup.find_all('positionlat')]
    PositionLon = [positionlon.text for positionlon in soup.find_all('positionlon')]
    GeoHash = [geohash.text for geohash in soup.find_all('geohash')]
    try:
        stationaddress_zh_tw = [i.zh_tw.text for i in soup.find_all('stationaddress')]
    except AttributeError:
        stationaddress_zh_tw=[]
    try:  
        stationaddress_En = [i.en.text for i in soup.find_all('stationaddress')]
    except AttributeError:
        stationaddress_En=[]
    bikescapacity = [bikescapacity.text for bikescapacity in soup.find_all('bikescapacity')]
    srcupdatetime = [srcupdatetime.text for srcupdatetime in soup.find_all('srcupdatetime')]
    UpdateTime = [updatetime.text for updatetime in soup.find_all('updatetime')]
    #VersionID = [versionid.text for versionid in i.find_all('versionid')]
    #print(authorityid)
    Bike={'站點唯一識別代碼':stationuid,'站點代碼':stationid,'業管單位代碼':authorityid
        ,"站點中文名稱":StopName_zh_tw,"站點英文名稱":StopName_En,'位置緯度(WGS84)':PositionLat
        ,'位置經度(WGS84)':PositionLon,"地理空間編碼":GeoHash,"站牌中文地址":stationaddress_zh_tw
        ,"站牌英文地址":stationaddress_En,"可容納之自行車總數":bikescapacity
        ,"資料版本編號":srcupdatetime,'資料更新日期時間':UpdateTime}
    
    Bike = pd.DataFrame.from_dict(Bike, orient='index')
    Bike=Bike.transpose()#把欄位顛倒過來
    Bike_information=Bike_information.append(Bike)
    #print(stationaddress_En)
    #break
    time.sleep(5)


# In[4]:


Bike_information.to_csv(r'C:\Users\公共自行車租借站位資料.csv', index=False,encoding="utf_8_sig" )


# In[ ]:




