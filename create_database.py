import pymysql

mydb = pymysql.connect(

    host="127.0.0.1",
    port=3306,
	user = "root",
	password = "root"
)

mycursor = mydb.cursor()


mycursor.execute("CREATE DATABASE hostel_db")