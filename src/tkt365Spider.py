# coding='UTF-8'
from bs4 import BeautifulSoup 
import re
import urllib.request
import sys
import io
import dboperator
import time
import json
import datetime
from xpinyin import Pinyin
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码（这个比较重要一点，可以有效解决编码异常）
#山东客运站id
stations=['370100006']
stations1=['120100001','120100002',
'120100003','120100004','370100001','370100002','370100003',
'370100004','370100005','370100006','370300001','370300002',
'370400001','370481001','370500001','370500002','370500003',
'370600001','370600002','370600003','370600004','370600005',
'370600006','370600014','370600015','370600016','370600017',
'370600018',
'370600019','370600020','370600021','370600022','370600023',
'370600024','370600026','370600028','370700001','370700002',
'370700003','370800001','370800002','370800003','370800004',
'370800005','370800006','370800007','370800008','370800009',
'370800010','370800011','370800012','370800013','370900001',
'370900002',
'370900003','370900004','370900005','370900006','370900007',
'370900008','370900009','370900010','370900011','370900012',
'370900013','370900015','370900016','370900017','370900018',
'371000001','371000002','371000003','371000004','371000005',
'371200001','371300001','371300002','371300003','371300004',
'371300005','371300006','371300007','371300008','371300009',
'371300010','371400001','371481001','371500001','371500002',
'371500003',
'371500004','371500005','371500006','371500007','371500008',
'371500009','371600001','371600002','371600003','371600004',
'371600005','371600006','371700010',
'371600007','371700001','371700002','371700003','371700004',
'371700005','371700006','371700007','371700008','371700009',
'371700011','371700012','371700013','411200001','411200002',
'411200003','411200004','411200005','411200006','610800001'];
#获取站点url
url = "http://www.365tkt.com/"
#获取班次url

header = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
          "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
          "Cache-Control":"max-age=0",
          "Connection":"keep-alive",
          "Content-Type":"application/x-www-form-urlencoded",
          "Host":"www.365tkt.com",
          "Origin":"http://www.365tkt.com",
          "Referer":"http://www.365tkt.com",
          "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.108 Safari/537.36"
          }

p = Pinyin()
nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
nowDate = time.strftime("%Y-%m-%d", time.localtime())
#获取客运站到达站信息
def getStationEndPorts(stationId):
    #请求出发信息
    portData=[]
    data = urllib.request.urlopen(url+"?c=service&a=GetPortsByID&format=json&id="+stationId)
    html = data.read().decode()
    if html is  None or not html.startswith("["):
        return None
    ports = json.loads(html)
    for dict in ports:
        try:
            port_name = dict["prtName"]
            print(port_name)
            pinyin = p.get_pinyin(port_name)
            if port_name is not None and len(port_name)>0 :
                 port = {"portName":port_name,"pinyin":pinyin,"pinyinPrefix":dict["prtCode"],"id":dict["prtID"]}
            portData.append(port)
        except Exception as e:
            print(dict["prtName"]+"出错！"+e)

    print(portData)    
    return portData

#获取一个站班次信息
def getStaitonPlanInfosPerDate(stationId, date,port):
    planInfos=[]
    try:
        if port["id"]=="8086" or port["portName"]=="肥城":
            print(port["portName"])
        requestUrl = url+"?c=service&a=GetLines&port="+port["id"]+"&date="+date+"&id="+stationId+"&portnm="+urllib.request.quote(port["portName"])+"&format=json"
        #requestUrl="http://www.365tkt.com/?c=service&a=GetLines&port=1070&date=2017-11-23&id=370100006&portnm=%E5%AE%9C%E5%85%B4&format=json"
        print(requestUrl)
        data = urllib.request.urlopen(requestUrl)
        html = data.read().decode()
        #print(html)
        if html is  None or len(html)<1:
            return None
        if html.startswith(u'\ufeff'):
            html = html.encode('utf8')[3:].decode('utf8')
        planInfoPerDate = json.loads(html,encoding='utf8');
        planInfos.extend(planInfoPerDate)
    except Exception as e:
        
        print(stationId+'站'+port["portName"]+'获取班次出错！'+date)
        print(e)
    return planInfos
#获取总班次
def getStationPlanInfos(stationId):
    date = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    ports = getStationEndPorts(stationId)
    if ports is None :
        return None
    for num in range(0,15):
        dateStr = date.strftime("%Y-%m-%d")
        date = date + oneday
        planInfos=[]
        returnpPort=[]
        for port in ports:
            planInfoPerDay = getStaitonPlanInfosPerDate(stationId,dateStr,port)
            if planInfoPerDay is not None and len(planInfoPerDay)>0:
                returnpPort.apend(port)
                planInfos.extend(planInfoPerDay)
        if len(planInfos)>0:
            print(planInfos)
        if len(returnpPort)>0:
            print(returnpPort)
#主函数
def _main(argv):
    print(argv)
    for station in stations:
        getStationPlanInfos(station)
_main("start..")