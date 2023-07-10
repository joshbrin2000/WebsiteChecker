import mysql.connector
from datetime import datetime

mydb = None
mycursor = None

def databaseInit():
    global mydb, mycursor
    if (not mydb):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password"
        )

    if (not mycursor):
        mycursor = mydb.cursor()
    
    mycursor.execute("CREATE DATABASE IF NOT EXISTS urlDatabase")
    mydb.database = "urlDatabase"

def tableInit():
    global mydb, mycursor
    if (mycursor):
        mycursor.execute("CREATE TABLE IF NOT EXISTS urlEntries (id INT AUTO_INCREMENT PRIMARY KEY, url VARCHAR(255), result_resp VARCHAR(255), time_created DATETIME)")

def insertTable(u, rr):
    global mydb, mycursor
    if (mycursor and mydb.is_connected()):
        now = datetime.now()
        date_time = now.strftime('%Y-%m-%d %H:%M:%S')
        #insertTable("test.com", "test", date_time)
        mycursor.execute("INSERT INTO urlEntries (url, result_resp, time_created) VALUES (%s, %s, %s)", (u, rr, date_time))
        mydb.commit()
    
def selectNTable(n):
    global mydb, mycursor
    if (mycursor):
        mycursor.execute(f"SELECT * FROM urlentries ORDER BY id DESC LIMIT {n}")
        myresult = mycursor.fetchall()
        return myresult
    
def clearTable():
    global mydb, mycursor
    if (mycursor):
        mycursor.execute("TRUNCATE TABLE urlEntries")
        mycursor.execute("ALTER TABLE urlEntries AUTO_INCREMENT=1")
    
def closeSQL():
    global mydb, mycursor
    if (mycursor):
        mycursor.close()
    if (mydb.is_connected()):
        mydb.close()