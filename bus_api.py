#!/usr/bin/env python
# coding: utf-8

# In[2]:


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


# In[3]:


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


# In[22]:


city=['NewTaipei','Taoyuan','Taichung','Tainan','Kaohsiung','Keelung','Hsinchu','HsinchuCounty','MiaoliCounty','ChanghuaCounty'
,'NantouCounty','YunlinCounty','ChiayiCounty','Chiayi','PingtungCounty','YilanCounty','HualienCounty','TaitungCounty'
,'KinmenCounty','PenghuCounty','LienchiangCounty','Taipei']
Bus_information=pd.DataFrame(columns = ["站牌唯一識別代碼","站牌代碼(為原資料內碼)","業管機關代碼","站牌中文名稱","站牌英文名稱"
                                        ,"站牌緯度(WGS84)","站牌經度(WGS84)","地理空間編碼","站牌地址","方位角","站牌所屬的站位ID"
                                        ,"站牌權管所屬縣市","站牌權管所屬縣市之代碼","站牌位置縣市之代碼","資料更新日期時間"
                                        ,"資料版本編號"])#建立空的datafram
for city in city:
    print(city)
    a = Auth(app_id, app_key)
    r=requests.get("https://ptx.transportdata.tw/MOTC/v2/Bus/Stop/City/"+str(city)+"?$format=xml", headers= a.get_auth_header())
    r.close()
    #if len(soup.find_all("busstop")) ==0:
        #print(False)
        #break
    soup = BeautifulSoup(r.text, "html.parser")
    #StopUID=soup.find("stopuid").text
    StopUID = [stopuid.text for stopuid in soup.find_all('stopuid')]
    #StopID=soup.find("stopid").text
    StopID = [stopid.text for stopid in soup.find_all('stopid')]
    #AuthorityID=soup.find("authorityid").text
    AuthorityID = [authorityid.text for authorityid in soup.find_all('authorityid')]
    #StopName=soup.find("zh_tw").text
    StopName = [zh_tw.text for zh_tw in soup.find_all('zh_tw')]
    #En=soup.find("en").text
    En = [en.text for en in soup.find_all('en')]
    #PositionLat=soup.find("positionlat").text
    PositionLat = [positionlat.text for positionlat in soup.find_all('positionlat')]
    #PositionLon=soup.find("positionlon").text
    PositionLon = [positionlon.text for positionlon in soup.find_all('positionlon')]
    #GeoHash=soup.find("geohash").text
    GeoHash = [geohash.text for geohash in soup.find_all('geohash')]
    #stopaddress=soup.find("stopaddress").text
    Stopaddress = [stopaddress.text for stopaddress in soup.find_all('stopaddress')]
    #Bearing=soup.find("bearing").text
    Bearing = [bearing.text for bearing in soup.find_all('bearing')]
    #StationID=soup.find("stationid").text
    StationID = [stationid.text for stationid in soup.find_all('stationid')]
    #City=soup.find("city").text
    City = [city.text for city in soup.find_all('city')]
    #CityCode=soup.find("citycode").text
    CityCode = [citycode.text for citycode in soup.find_all('citycode')]
    #LocationCityCode=soup.find("locationcitycode").text
    LocationCityCode = [locationcitycode.text for locationcitycode in soup.find_all('locationcitycode')]
    #UpdateTime=soup.find("updatetime").text
    UpdateTime = [updatetime.text for updatetime in soup.find_all('updatetime')]
    #VersionID=soup.find("versionid").text
    VersionID = [versionid.text for versionid in soup.find_all('versionid')]
    Bus={'站牌唯一識別代碼':StopUID,'站牌代碼(為原資料內碼)':StopID,'業管機關代碼':AuthorityID
                    ,"站牌中文名稱":StopName ,"站牌英文名稱":En,"站牌緯度(WGS84)":PositionLat,"站牌經度(WGS84)":PositionLon
                    ,"地理空間編碼":GeoHash,"站牌地址":Stopaddress,"方位角":Bearing,"站牌所屬的站位ID":StationID
                    ,"站牌權管所屬縣市":City,"站牌權管所屬縣市之代碼":CityCode,"站牌位置縣市之代碼":LocationCityCode
                    ,"資料更新日期時間":UpdateTime,"資料版本編號":VersionID
                    }
    #print(Bus_information)
    df = pd.DataFrame.from_dict(Bus, orient='index')
    df=df.transpose()#把欄位顛倒過來
    Bus_information=pd.concat([Bus_information,df])
    #df.to_csv(r'C:\Users\bus_'+city+'.csv', index=False,encoding="utf_8_sig" )
Bus_information.to_csv(r'C:\Users\bus.csv', index=False,encoding="utf_8_sig" )


# In[ ]:




