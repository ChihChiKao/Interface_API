#!/usr/bin/env python
# coding: utf-8

# In[22]:


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


# In[23]:


app_id = '****'
app_key = '****'
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


# In[25]:


a = Auth(app_id, app_key)
r=requests.get("https://ptx.transportdata.tw/MOTC/v2/Bus/StopOfRoute/InterCity?$format=xml", headers= a.get_auth_header())
r.close()
soup = BeautifulSoup(r.text, "html.parser")
data_all=pd.DataFrame(columns = ["路線唯一識別代碼","地區既用中之路線代碼","路線中文名稱","路線英文名稱","營運業者代碼"
                                 ,"營運業者中文名稱","營運業者英文名稱","營運業者簡碼","營運業者編號","附屬路線唯一識別代碼"
                                 ,'附屬路線代碼',"附屬路線中文名稱",'附屬路線英文名稱',"去返程","資料更新日期時間","資料版本編號"
                                 ,"經此站牌唯一識別代碼","經此站牌代碼","經此站牌中文名稱","經此站牌英文名稱"
                                 ,"經此站牌上下車站別","路線經過站牌之順序","經此站牌位置緯度","經此站牌位置經度","經此站牌地理空間編碼"
                                 ,"經此站牌所屬的站位ID","站牌所屬的組站位ID","經此站牌位置縣市之代碼"])
for i in soup.find_all('busstopofroute'): #每次跑一個站的資料
    #print(i.prettify())
    #print(j)
    #for j in i.find_all("stops"):
    routeuid = [routeuid.text for routeuid in i.find_all('routeuid')]
    routeid = [routeid.text for routeid in i.find_all('routeid')]
    route_zh_tw = [i.zh_tw.text for i in i.find_all('routename')]
    route_en = [i.en.text for en in i.find_all('routename')]
    operatorid = [operatorid.text for operatorid in i.find_all('operatorid')]
    operatorid_zh_tw = [ i.zh_tw.text for i in i.find_all('operatorname')]
    try:
        operatorid_en = [ i.en.text for i in i.find_all('operatorname')]
    except AttributeError:
        operatorid_en=[]
    operatorcode = [operatorcode.text for operatorcode in i.find_all('operatorcode')]
    operatorno = [operatorno.text for operatorno in i.find_all('operatorno')]
    subrouteuid = [subrouteuid.text for subrouteuid in i.find_all('subrouteuid')]
    subrouteid = [subrouteid.text for subrouteid in i.find_all('subrouteid')]
    subroutename_zh_tw = [i.zh_tw.text for zh_tw in i.find_all('subroutename')]
    subroutename_en = [i.en.text for en in i.find_all('subroutename')]
    direction = [direction.text for direction in i.find_all('direction')]
    #city = [city.text for city in i.find_all('city')]
    #citycode = [i.citycode.text for citycode in i.find_all('citycode')]
    updateTime = [i.updatetime.text for updatetime in i.find_all('updatetime')]
    versionID = [versionid.text for versionid in i.find_all('versionid')]
    print(routeuid)

    busstop_of_route={"路線唯一識別代碼":routeuid,"地區既用中之路線代碼":routeid,"路線中文名稱":route_zh_tw,"路線英文名稱":route_en
        ,"營運業者代碼":operatorid,"營運業者中文名稱":operatorid_zh_tw,"營運業者英文名稱":operatorid_en
        ,"營運業者簡碼":operatorcode,"營運業者編號":operatorno,"附屬路線唯一識別代碼":subrouteuid,'附屬路線代碼':subrouteid,
         '附屬路線中文名稱':subroutename_zh_tw,'附屬路線英文名稱':subroutename_en,"去返程":direction,"資料更新日期時間":updateTime
        ,"資料版本編號":versionID}
    #print(Bus_information)
    busstop_of_route = pd.DataFrame.from_dict(busstop_of_route, orient='index')
    busstop_of_route=busstop_of_route.transpose()#把欄位顛倒過來
    #print(busstop_of_route)
    #合併經過公車
    
    routeuid = [routeuid.text for routeuid in i.find_all('routeuid')]
    stopuid = [i.stopuid.text for i in i.find_all('stop')]
    stopid = [i.stopid.text for i in i.find_all('stop')]
    stopname_zh_tw=[i.zh_tw.text for i in i.find_all('stopname')]
    stopname_en=[i.en.text for i in i.find_all('stopname')]
    stopboarding = [i.text for i in i.find_all('stopboarding')]
    stopsequence = [i.text for i in i.find_all('stopsequence')]
    positionlat = [i.text for i in i.find_all('positionlat')]
    positionlon=[i.text for i in i.find_all('positionlon')]
    geohash = [i.text for i in i.find_all('geohash')]
    stationid=[i.text for i in i.find_all('stationid')]
    stationgroupid=[i.text for i in i.find_all('stationgroupid')]
    locationcitycode=[i.text for i in i.find_all('locationcitycode')]
    route_connection={'路線唯一識別代碼':routeuid,"經此站牌唯一識別代碼":stopuid,"經此站牌代碼":stopid,
                      "經此站牌中文名稱":stopname_zh_tw,"經此站牌英文名稱":stopname_en,"經此站牌上下車站別":stopboarding,
                      "路線經過站牌之順序":stopsequence,"經此站牌位置緯度":positionlat,"經此站牌位置經度":positionlon,
                      "經此站牌地理空間編碼":geohash,"經此站牌所屬的站位ID":stationid,"站牌所屬的組站位ID":stationgroupid,
                      "經此站牌位置縣市之代碼":locationcitycode}
    df = pd.DataFrame.from_dict(route_connection, orient='index')
    df=df.transpose()#把欄位顛倒過來
    df=df.fillna(method='pad')#用前一個值彌補後一個值
    _all=pd.merge(busstop_of_route, df,on="路線唯一識別代碼")#完整資料
    
    #Route_information=pd.concat([Route_information, _all])
    data_all=data_all.append(_all)
    time.sleep(0.5)


# In[20]:


data_all.to_csv(r'C:\Users\公路客運之路線與站牌資料.csv', index=False,encoding="utf_8_sig" )


# In[ ]:




