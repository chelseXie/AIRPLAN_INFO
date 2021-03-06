# coding='UTF-8'
from bs4 import BeautifulSoup 
import re
import urllib.request
import sys
import io
import dboperator
import time
import json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码（这个比较重要一点，可以有效解决编码异常）
#青岛航班url
url = "http://www.qdairport.com/control/FindHbcx?catalogId=head_hbxx0101"
body_value = {"serviceName":"domesticDeparture","flightStarttime":"2017-07-13 17:00:00",
              "flightEndtime":"","flightNumber":"","airCity":"","airCompany":"",
              "startDate":"2017-07-13","startTime":"00:00","endTime":""}
header = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
          "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
          "Cache-Control":"max-age=0",
          "Connection":"keep-alive",
          "Content-Type":"application/x-www-form-urlencoded",
          "Host":"www.qdairport.com",
          "Origin":"http://www.qdairport.com",
          "Referer":"http://www.qdairport.com/control/FindHbcx?flightNumber=&serviceName=&catalogId=head_hbxx0101",
          "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.108 Safari/537.36"
          }
request_body_send = "domesticDeparture"
request_body_send_international="internationalDeparture"
request_body_arrive = "domesticArrival"
request_body_arrive_international="internationalArrival"
sendDate = time.strftime("%Y-%m-%d", time.localtime())
flightStarttime = sendDate+" 00:00:00"
body_value["startDate"]=sendDate
body_value["flightStarttime"]=flightStarttime
airportName = "青岛流亭国际机场"

#获取烟台蓬莱机场出港航班信息
yantaiUrl = "http://119.180.28.88:7777/FligthManage/FlightInfo/FlightInfoHandler.ashx"
yantaiAirPort = "烟台蓬莱国际机场"
#烟台航班请求参数    

#获取青岛出发航班信息
def getQingDaoStartInfo(body_value,header,international):
#请求出发信息
    if international:
        body_value["serviceName"]=request_body_send_international
    else:
        body_value["serviceName"]==request_body_send
    postdata =urllib.parse.urlencode(body_value).encode('utf-8')
    req = urllib.request.Request(url,postdata,header)
    data= urllib.request.urlopen(req)
    html = data.read().decode()
    soup = BeautifulSoup(html)
    plans = []
    nowTime =time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for x in soup.find_all("table"):
        for tr in x.find("tbody").find_all("tr"):
            tds = tr.find_all("td")
            length = len(tds)
            if 9!=length:
              continue
            else :
              planData={}
              planData["start_plan"] = re.sub("\s",'',tds[0].get_text())
              planData["flight_number"] = re.sub("\s",'',tds[1].get_text())
              planData["company"] =re.sub("\s",'', tds[2].get_text())
              planData["start_actual"] = re.sub("\s",'',tds[4].get_text())
              planData["port_name"] = re.sub("\s",'',tds[5].get_text(","))
              planData["arrive_estimate"] = re.sub("\s",'',tds[6].get_text())
              planData["status"] = re.sub("\s",'',tds[7].get_text())
              if(planData["port_name"]is not None and len(planData["port_name"])>0 and planData["port_name"][len(planData["port_name"])-1]==","):
                 planData["port_name"]=planData["port_name"][0:len(planData["port_name"])-1]
              plans.append((sendDate,planData["start_plan"], planData["flight_number"], planData["company"], 
                            planData["start_actual"], planData["port_name"],planData["arrive_estimate"],
                            planData["status"],"1",airportName,nowTime,nowTime))
    print(plans)          
    return plans
#获取青岛到达航班信息
def getQingDaoArriveInfo(body_value,header,international):
    if international:
        body_value["serviceName"]=request_body_arrive
    else :
        body_value["serviceName"]=request_body_arrive_international
    postdata =urllib.parse.urlencode(body_value).encode('utf-8')
    req = urllib.request.Request(url,postdata,header)
    data= urllib.request.urlopen(req)
    html = data.read().decode()
    soup = BeautifulSoup(html)
    plans = []
    nowTime =time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for x in soup.find_all("table"):
        for tr in x.find("tbody").find_all("tr"):
            tds = tr.find_all("td")
            length = len(tds)
            if 8!=length:
              continue
            else :
              planData={}
              planData["arrive_plan"] = re.sub("\s",'',tds[0].get_text())
              planData["flight_number"] = re.sub("\s",'',tds[1].get_text())
              planData["company"] =re.sub("\s",'', tds[2].get_text())
              planData["port_name"] = re.sub("\s",'',tds[3].get_text(","))
              planData["status"] = re.sub("\s",'',tds[6].get_text())
              if "到达"==planData["status"]:
                  planData["arrive_estimate"]=""
                  planData["arrive_actual"] = re.sub("\s",'',tds[4].get_text())
              else :
                  planData["arrive_estimate"] = re.sub("\s",'',tds[4].get_text())
                  planData["arrive_actual"]=""
              planData["plan_port"] = re.sub("\s",'',tds[5].get_text())
              if(planData["port_name"]is not None and len(planData["port_name"])>0 and planData["port_name"][len(planData["port_name"])-1]==","):
                 planData["port_name"]=planData["port_name"][0:len(planData["port_name"])-1]
              plans.append((sendDate,planData["arrive_plan"], planData["flight_number"], planData["company"], 
                            planData["port_name"], planData["arrive_estimate"],planData["arrive_actual"],planData["plan_port"],
                            planData["status"],"2",airportName,nowTime,nowTime))
    print(plans)          
    return plans
#获取烟台机场出港航班
def getYanTaiStartInfo(yantaiUrl):
    yantaiUrl +=  "?flio=D"
    data = urllib.request.urlopen(yantaiUrl)
    html = data.read().decode()
    plans = json.loads(html)
    nowTime =time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    plansData=[]
    for dict in plans["rows"]:
        port_name = dict["HX"].replace("-",",")
        if port_name is not None and len(port_name)>3 and port_name[0:3]=="烟台,":
            port_name=port_name.replace("烟台,","")
        plan = (dict["HBH"],dict["AIRCOMPANY"],dict["HX"],sendDate,dict["JX"],dict["JHQFSJ"],"" if "1900-01-01" in dict["YJQFSJ"] else dict["YJQFSJ"],
                dict["SJQFSJ"],"","","",dict["HBZT"],dict["HBYCZT"],dict["HBYCYY"],
                dict["GXHB"],"1",port_name,dict["DJK"],yantaiAirPort,nowTime,nowTime)
        plansData.append(plan)
    print(plansData)    
    return plansData
#获取烟台机场进港航班
def getYanTaiArriveInfo(yantaiUrl):
    yantaiUrl +=  "?flio=A"
    data = urllib.request.urlopen(yantaiUrl)
    html = data.read().decode()
    plans = json.loads(html)
    nowTime =time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    plansData=[]
    for dict in plans["rows"]:
        port_name = dict["HX"].replace("-",",")
        print(port_name)
        print(port_name[len(port_name)-3:len(port_name)])
        if port_name is not None and len(port_name)>3 and port_name[len(port_name)-3:len(port_name)]==",烟台":
            port_name=port_name.replace(",烟台","")
        plan = (dict["HBH"],dict["AIRCOMPANY"],dict["HX"],sendDate,dict["JX"],dict["SJQFSJ"],dict["JHDDSJ"],
                dict["YJDDSJ"], dict["SJDDSJ"],dict["HBZT"],dict["HBYCZT"],dict["HBYCYY"],
                dict["GXHB"],"2",port_name,yantaiAirPort,nowTime,nowTime)
        plansData.append(plan)
    print(plansData)    
    return plansData
db = dboperator.Mysqldboperator("第一次初始化数据库连接")
#插入青岛机场出发信息
insertSQL = """insert flight (send_date,start_plan,flight_number,company,start_actual,port_name,arrive_estimate,status,flight_type,air_port,create_time,modify_time) 
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
#db.insertBatch(insertSQL,getQingDaoStartInfo(body_value,header,False))
#插入青岛国际航线信息
#db.insertBatch(insertSQL,getQingDaoStartInfo(body_value,header,True))
#插入青岛机场到达信息
insertSQL = """insert flight (send_date,arrive_plan,flight_number,company,port_name,arrive_estimate,arrive_actual,plan_port,status,flight_type,air_port,create_time,modify_time) 
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
#db.insertBatch(insertSQL,getQingDaoArriveInfo(body_value,header,False))
#插入青岛国际航线信息
#db.insertBatch(insertSQL,getQingDaoArriveInfo(body_value,header,True))
#插入烟台出港航班数据
insertSQL = """insert flight (flight_number,company,line,send_date,plane_type,start_plan,start_estimate,start_actual,arrive_plan,arrive_estimate,arrive_actual,status,
            exception,exception_reason,flight_number_share,flight_type,port_name,plan_port,air_port,create_time,modify_time) 
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
db.insertBatch(insertSQL,getYanTaiStartInfo(yantaiUrl))
#插入烟台进港信息
insertSQL = """insert flight (flight_number,company,line,send_date,plane_type,start_actual,arrive_plan,arrive_estimate,arrive_actual,status,
            exception,exception_reason,flight_number_share,flight_type,port_name,air_port,create_time,modify_time) values
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
db.insertBatch(insertSQL,getYanTaiArriveInfo(yantaiUrl))

#删除旧数据
deleteSQL = "delete from flight where send_date < %s"
db.deleteBySql(deleteSQL,(sendDate))


    
 





