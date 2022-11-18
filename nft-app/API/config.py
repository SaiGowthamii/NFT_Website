#import pyodbc
import pandas as pd
import sqlalchemy
mySQL ={
'server' : 'localhost',
'database' : 'test',
'username' : 'root',
'password' : 'root',   
'driver' : '{MySQL ODBC 8.0 ANSI Driver}'
}

connection_string = (
    'DRIVER=MySQL ODBC 8.0 ANSI Driver;'
    'SERVER=localhost;'
    'DATABASE=test;'
    'UID=root;'
    'PWD=suhaas@142;'
    'charset=utf8mb4;'
)

def connect_to_mySQL():
    #conn =  pyodbc.connect('DRIVER='+mySQL['driver']+';SERVER='+mySQL['server']+';PORT=3306;DATABASE='+mySQL['database']+';uid='+mySQL['username']+';password='+ mySQL['password'])
    #conn = pyodbc.connect(connection_string)
    conn = sqlalchemy.create_engine("mysql+pymysql://root:root@localhost:3306/test")
    return conn