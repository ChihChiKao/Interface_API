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


# In[7]:


a = Auth(app_id, app_key)
r=requests.get("https://ptx.transportdata.tw/MOTC/v2/Bus/Stop/InterCity?$format=xml", headers= a.get_auth_header())
r.close()

soup = BeautifulSoup(r.text, "html.parser")
#print(soup.prettify())
stopuid = [stopuid.text for stopuid in soup.find_all('stopuid')]

stopid = [stopid.text for stopid in soup.find_all('stopid')]

authorityid = [authorityid.text for authorityid in soup.find_all('authorityid')]

busstop_zh_tw = [zh_tw.text for zh_tw in soup.find_all('zh_tw')]

busstop_En = [en.text for en in soup.find_all('en')]

positionlat = [positionlat.text for positionlat in soup.find_all('positionlat')]

positionlon = [positionlon.text for positionlon in soup.find_all('positionlon')]

geohash = [geohash.text for geohash in soup.find_all('geohash')]

stopaddress = [stopaddress.text for stopaddress in soup.find_all('stopaddress')]

bearing = [bearing.text for bearing in soup.find_all('bearing')]

stationid = [stationid.text for stationid in soup.find_all('stationid')]

stationgroupid = [stationgroupid.text for stationgroupid in soup.find_all('stationgroupid')]

locationcitycode = [locationcitycode.text for locationcitycode in soup.find_all('locationcitycode')]

updatetime = [updatetime.text for updatetime in soup.find_all('updatetime')]

versionid = [versionid.text for versionid in soup.find_all('versionid')]

Busstop={'????????????????????????':stopuid,'??????????????????????????????':stopid,'??????????????????':authorityid
    ,"??????????????????":busstop_zh_tw ,"??????????????????":busstop_En,"????????????(WGS84)":positionlat,"????????????(WGS84)":positionlon
    ,"??????????????????":geohash,"????????????":stopaddress,"?????????":bearing,"?????????????????????ID":stationid
    ,"????????????????????????ID":stationgroupid,"???????????????????????????":locationcitycode
    ,"????????????????????????":updatetime,"??????????????????":versionid}
#print(Bus_information)
df = pd.DataFrame.from_dict(Busstop, orient='index')
df=df.transpose()#?????????????????????

#Bus_information=pd.concat([Bus_information,df])
#df.to_csv(r'C:\Users\bus_'+city+'.csv', index=False,encoding="utf_8_sig" )
#Bus_information.to_csv(r'C:\Users\bus.csv', index=False,encoding="utf_8_sig" )


# In[9]:


df.to_csv(r'C:\Users\???????????????????????????.csv', index=False,encoding="utf_8_sig" )


# In[ ]:




