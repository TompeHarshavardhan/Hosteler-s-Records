import face_recognition
import cv2
import numpy as np
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from datetime import datetime

db = pymysql.connect  (
    host="127.0.0.1",
    port=3306,
	user = "root",
	password = "root",
    database="hostel_db")
cursor = db.cursor()
video_capture = cv2.VideoCapture(0)

Harsh_image=face_recognition.load_image_file("Harsh.jpg")
Harsh_face_encoding = face_recognition.face_encodings(Harsh_image)[0]

Shreyash_image = face_recognition.load_image_file("Shreyash.jpg")
Shreyash_face_encoding = face_recognition.face_encodings(Shreyash_image)[0]

Suyash_image = face_recognition.load_image_file("Suyash.jpg")
Suyash_face_encoding = face_recognition.face_encodings(Suyash_image)[0]

Yash_image = face_recognition.load_image_file("Yash.jpg")
Yash_face_encoding = face_recognition.face_encodings(Yash_image)[0]
known_face_encodings = [
    Harsh_face_encoding,
    Shreyash_face_encoding,
    Suyash_face_encoding,
    Yash_face_encoding
    
]
known_face_names = [
    "Harsh",
    "Shreyash",
    "Suyash",
    "Yash"
]


face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
i=0
while True:
 
    ret, frame = video_capture.read()   
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)   
    rgb_small_frame = small_frame[:, :, ::-1]
  
    if process_this_frame:
        
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"           
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame
  
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)  
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        i = 0
        if(name == 'Harsh' or 'Shreyash' or 'Suyash' or 'Yash'):
          cursor.execute("SELECT * FROM `hostel_db`.`hosteler_io_rec` WHERE `name` = '%s' AND in_time = NULL "%(name))
          sql1 = cursor.fetchall()
          i = 1
          if(sql1 == name):  
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            a = (dt_string,name)
            sql4 = "UPDATE `hostel_db`.`hosteler_io_rec` SET `in_time`='%s' WHERE `in_time` = NULL AND `name` = '%s'"%(dt_string,name)
            cursor.execute(sql4)
          else:
            
            sql2 = "INSERT INTO `hostel_db`.`hosteler_io_rec` (name , roll_no , room_no ) SELECT name, roll_no, room_no FROM hostel_db.student_data WHERE `name` = '%s'" %(name)
            cursor.execute(sql2)
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            a = (dt_string,name)
            sql3 = "UPDATE `hostel_db`.`hosteler_io_rec` SET `out_time`='%s' WHERE `out_time` = NULL AND `name` = '%s'"%(dt_string,name)
            cursor.execute(sql3)  
          
        sql =" SELECT * FROM hostel_db.hosteler_io_rec;"
        cursor.execute(sql)
        db.commit()   
	    
             
    cv2.imshow('Video', frame)

  
    if (cv2.waitKey(1) & 0xFF == ord('q')) or i==1:
        break

video_capture.release()
cv2.destroyAllWindows()
cursor.close()
db.close()