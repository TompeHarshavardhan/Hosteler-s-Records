import pymysql

mydb = pymysql.connect(

    host="127.0.0.1",
    port=3306,
	user = "root",
	password = "root",
	database = "hostel_db"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE student_data ( name VARCHAR(255),  roll_no VARCHAR(255), room_no VARCHAR(255))")
mycursor.execute("CREATE TABLE hosteler_io_rec( name VARCHAR(255),  roll_no VARCHAR(255), room_no VARCHAR(255) , out_time VARCHAR(255), in_time VARCHAR(255))")

sqlFormula = "INSERT INTO student_data (name , roll_no, room_no) VALUES (%s, %s, %s)"
students = [("Harsh", "CH21BTECH11033", "K1016"),
			("Shreyash", "CH21BTECH11028", "K906"),
			("Yash","CH21BTECH11036","K1007"),
			("Suyash","CH21BTECH11031","K1015"),]
		
mycursor.executemany(sqlFormula, students)
mycursor.execute("SELECT * FROM hostel_db.hosteler_io_rec")
mydb.commit()
myresult = mycursor.fetchall()
for x in myresult:
	print(x)