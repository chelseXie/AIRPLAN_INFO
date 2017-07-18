# coding='UTF-8'
from bottle import route, run
from bottle import get, post, request 
import dboperator
import datetime
import time
@route('/hello/:name')
def index(name = 'World'):
    return '<strong>Hello {}!'.format(name)
@route("/info")
def info():
    responseJson={"base":{"is_success":"1","error_msg":""}}
    airport = request.params.get('airport')
    flighttype = request.params.get('fight_type')
    timeStr = request.params.get('time')
    if timeStr is None or timeStr=="":
        timeStr= "240"
    if airport is None or airport=="":
        responseJson["base"]["is_success"]="0"
        responseJson["base"]["error_msg"]="机场参数不能为空"
        return responseJson
    if flighttype is None or flighttype=="" :
        responseJson["base"]["is_success"]="0"
        responseJson["base"]["error_msg"]="航班类型不能为空"
        return responseJson
    if timeStr is None:
        responseJson["base"]["is_success"]="0"
        responseJson["base"]["error_msg"]="时间参数不能为空"
        return responseJson
    if "0" == airport:
        airport="烟台蓬莱国际机场"
    if "1"==airport :
        airport="青岛流亭国际机场"
    now = datetime.datetime.now()  
    date = now+datetime.timedelta(minutes=int(timeStr))
    sendMinite = date.strftime('%H:%M')
    sendDate = time.strftime("%Y-%m-%d", time.localtime())
    sql=""
    condition=()
    #查询出港航班
    if "0" == flighttype:
        sql = """select flight_number fightNo,company company,start_plan depart_plan
                ,start_actual depart_actual,start_estimate depart_predict,'' lounge_room ,
                plan_port departure_gate,port_name destination,status fight_state
                from flight B,(select max(flight_number) flightNo,max(create_time) time from flight where send_date = %s GROUP BY flight_number ) A 
                where B.send_date = %s and B.create_time =A.time AND B.flight_number = A.flightNo  and B.flight_type='1'
                and B.air_port=%s and B.start_plan>%s order by start_plan asc"""
        condition=(sendDate,sendDate,airport,sendMinite)
    #查询进港航班
    if "1" == flighttype:
        sql = """  select flight_number fightNo,company company,port_name depart_address
                ,arrive_plan arrive_plan,arrive_actual arrive_actual,arrive_estimate arrive_predict ,
                air_port destination ,status fight_state
                 from flight B,(select max(flight_number) flightNo,max(create_time) time from flight where send_date=%s GROUP BY flight_number ) A 
                where B.send_date = %s and B.create_time =A.time AND B.flight_number = A.flightNo AND  B.flight_type='2'
                and B.air_port=%s and B.arrive_plan>%s order by arrive_plan asc"""
        condition=(sendDate,sendDate,airport,sendMinite)
    db = dboperator.Mysqldboperator("第一次初始化数据库连接")
    result = db.queryBysql(sql,condition)
    responseJson["list"]=result
    print("result-->"+str(responseJson))
    return responseJson

run(host="localhost",port=8080)
