#import pyodbc
import pandas as pd
import sqlalchemy


###### Change the values according to your database configuration
mySQL ={
'server' : 'localhost',
'database' : 'test',
'username' : 'root',
'password' : 'suhaas%40142',
}

def connect_to_mySQL():
    #conn =  pyodbc.connect('DRIVER='+mySQL['driver']+';SERVER='+mySQL['server']+';PORT=3306;DATABASE='+mySQL['database']+';uid='+mySQL['username']+';password='+ mySQL['password'])
    #conn = sqlalchemy.create_engine("mysql+pymysql://root:suhaas%40142@localhost:3306/test")
    conn = sqlalchemy.create_engine('mysql+pymysql://'+mySQL['username']+':'+mySQL['password']+'@'+mySQL['server']+':3306/'+mySQL['database'])
    return conn