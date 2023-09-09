import cv2 
import sqlite3
import numpy as np

faceDetect = cv2.CascadeClassifier(r'C:\\Users\\Pramod B.S\\Desktop\\face_Recog_sqlite\\haarcascade_frontalface_default.xml')

# capture frames from a camera
cap = cv2.VideoCapture(0)

def insertOrUpdate(Id,Name):
    conn=sqlite3.connect("FaceDB.db")
    cmd="SELECT * FROM People WHERE ID="+str(Id)
    #return row with id matching given id
    cursor=conn.execute(cmd)
    recordExists=0
#enter name in double quotation marks

    for row in cursor:
        recordExists=1
    if(recordExists==1):
        cmd="UPDATE People SET Name="+str(Name)+" WHERE ID="+str(Id)
    else:
        cmd="INSERT INTO People(ID,Name) Values("+str(Id)+","+str(Name)+")"
    conn.execute(cmd)
    conn.commit()
    conn.close()

id=raw_input('enter user id : ')
name=raw_input('enter name : ')

insertOrUpdate(id,name)

counterID=0

# loop runs if capturing has been initialized.
while 1: 
 
    # reads frames from a camera
    ret, img = cap.read() 
 
    # convert to gray scale of each frames
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
    # Detects faces of different sizes in the input image
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)
 
    for (x,y,w,h) in faces:
        counterID=counterID+1
        cv2.imwrite("dataset/User."+str(id)+"."+str(counterID)+".jpg",gray[y:y+h,x:x+w])
        # To draw a rectangle in a face 
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.waitKey(100) 

    cv2.imshow('img',img)
    cv2.waitKey(1)

    if(counterID>30):
        break;
 
# Close the window
cap.release()
 
# De-allocate any associated memory usage
cv2.destroyAllWindows()