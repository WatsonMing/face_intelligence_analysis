#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
"""
MariaDB [face]> show tables;
+---------------------+
| Tables_in_face      |
+---------------------+
| EmployeeInformation |
| SignIn              |
+---------------------+
MariaDB [face]> desc SignIn;
+----------+----------+------+-----+---------+-------+
| Field    | Type     | Null | Key | Default | Extra |
+----------+----------+------+-----+---------+-------+
| no       | char(30) | NO   | PRI | NULL    |       |
| userId   | char(20) | NO   | MUL | NULL    |       |
| signTime | datetime | NO   |     | NULL    |       |
| type     | char(2)  | NO   |     | NULL    |       |
+----------+----------+------+-----+---------+-------+
MariaDB [face]> desc EmployeeInformation;
+------------+----------+------+-----+---------+-------+
| Field      | Type     | Null | Key | Default | Extra |
+------------+----------+------+-----+---------+-------+
| userName   | char(20) | NO   |     | NULL    |       |
| userId     | char(20) | NO   | PRI | NULL    |       |
| age        | int(11)  | YES  |     | NULL    |       |
| sex        | char(1)  | YES  |     | NULL    |       |
| department | char(5)  | YES  |     | NULL    |       |
+------------+----------+------+-----+---------+-------+

SignIn.userId -> EmployeeInformation.userId
"""
class mydb:
    def __init__(self):
        db = MySQLdb.connect("localhost", "root", "raspberry", "face", charset='utf8' )
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
    def InsertDb(userName,userId,age,sex,department):
        sql="insert into EmployeeInformation(userName,userId,age,sex,department) values('{thisName}',\
        '{thisId}',{thisAge},'{thisSex}','{thisDepartment}');".format{thisName=userName,thisId=userId,
        thisAge=age,thisSex=sex,thisDepartment=department
        }
        # 创建数据表SQL语句
        self.cursor.execute(sql)
        self.db.close()
    def SelectDb(userName,userId):
        if userId！='': 
            sql="select signTime,type from SignIn where userId='{thisId}' ".format{thisId=userId}
        else: 
            sql="select signTime,type from SignIn where userId=(select userId from EmployeeInformation where userName='{thisName}')' ".format{thisName=userName}
        # 创建数据表SQL语句
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        self.db.close()
        while result!=None:
            sTArray = []
            TypeArray = []
            for row in results:
                sTArray.append(row[0])
                TypeArray.append(row[1])
        return sTArray,TypeArray
