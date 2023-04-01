import mysql.connector

mydb = mysql.connector.connect(
  host="mysql",
  user="root",
  password="test1234",
)


print(mydb)

cursorObject = mydb.cursor()
 
# creating database
# cursorObject.execute("drop database stud")
# cursorObject.execute("CREATE DATABASE stud")
# cursorObject.execute("commit")

# cursorObject.execute("use stud")
cursorObject.execute("select 1 as col;")
cursorObject.fetchall()
