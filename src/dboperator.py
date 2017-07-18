# coding='UTF-8'
import pymysql
class Mysqldboperator():
     config = {
#          'host':'127.0.0.1',
          'host':'192.168.1.103',
          'port':3306,
          'user':'root',
          'password':'123456',
          'db':'airplaninfo',
          'charset':'utf8mb4',
          'cursorclass':pymysql.cursors.DictCursor
          }
     def __init__(self,message):
         print(message)
     def insert(self,sql,data):
         try:
             connect = pymysql.Connect(**self.config)
             cursor = connect.cursor()  
             cursor.execute(sql % data)  
             connect.commit()
             cursor.close()  
             print('成功插入', cursor.rowcount, '条数据')
         finally:
             connect.close()
     def  insertBatch(self,sql,list):
         try:
             connect = pymysql.Connect(**self.config)
             cursor = connect.cursor()  
             cursor.executemany(sql ,list)  
             connect.commit()  
             cursor.close()
             print('成功插入', cursor.rowcount, '条数据')   
         finally:
             connect.close()
     def queryBysql(self,sql,condition):
         try:
             connect = pymysql.Connect(**self.config)
             with  connect.cursor() as cursor:
                 cursor.execute(sql, condition)
                 result = cursor.fetchall()
                 print("成功查询出"+str(len(result))+"条数据")
                 print(result)
             # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
                 cursor.close()
                 return result
                
         finally:
             connect.close()
     def deleteBySql(self,sql,condition):
         try:
             connect = pymysql.Connect(**self.config)
             with  connect.cursor() as cursor:
                 print(sql % condition)
                 result = cursor.execute(sql , condition)
                 print("删除"+str(result)+"条数据")
                 result1 = connect.commit()
                 # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
                 cursor.close()
                 return result
                
         finally:
             connect.close()
          
#test insert
#insertOperator = Mysqldboperator("第一次初始化对象");
# sql = "insert flight (flight_number,company) values(%s,%s) "
# data = ("111","111")
# list = [("123","123"),("123","123")]
# list.append(data)
# insertOperator.insert(sql, data)
# insertOperator.insertBatch(sql, list)
#sql = "select * from flight where send_date=%s"
#insertOperator.queryBysql(sql,("2017-07-14"))
#insertOperator.queryBysql(sql,("2017-07-14"))
             
            