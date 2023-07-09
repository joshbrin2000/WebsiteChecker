import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password"
    )

mycursor = mydb.cursor()

def databaseInit():
    mycursor.execute("CREATE DATABASE IF NOT EXISTS urlDatabase")
    mydb.database = "urlDatabase"

def tableInit():
    mycursor.execute("CREATE TABLE IF NOT EXISTS urlEntries (id INT AUTO_INCREMENT PRIMARY KEY, url VARCHAR(255), result_resp VARCHAR(255), time_created DATETIME)")

def insertTable(u, rr):
    now = datetime.now()
    date_time = now.strftime('%Y-%m-%d %H:%M:%S')
    #insertTable("test.com", "test", date_time)
    mycursor.execute("INSERT INTO urlEntries (url, result_resp, time_created) VALUES (%s, %s, %s)", (u, rr, date_time))
    mydb.commit()
    
def selectNTable(n):
    mycursor.execute(f"SELECT * FROM urlentries ORDER BY id DESC LIMIT {n}")
    myresult = mycursor.fetchall()
    return myresult
    
def clearTable():
    mycursor.execute("TRUNCATE TABLE urlEntries")
    mycursor.execute("ALTER TABLE urlEntries AUTO_INCREMENT=1")