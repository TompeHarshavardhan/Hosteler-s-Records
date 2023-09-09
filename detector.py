import cv2 
import numpy as np
import sqlite3

faceDetect = cv2.CascadeClassifier(r'C:\\Users\\Pramod B.S\\Desktop\\face_Recog_sqlite\\haarcascade_frontalface_default.xml')

# capture frames from a camera
cap = cv2.VideoCapture(0)
 
rec=cv2.createLBPHFaceRecognizer()
rec.load('recognizer\\trainingData.yml')

id=0
font=cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_COMPLEX_SMALL,5,1,0,4)

def getProfile(id):
    conn=sqlite3.connect("FaceDB.db")
    cmd="SELECT * FROM People WHERE ID="+str(id)
    cursor=conn.execute(cmd)
    profile=None

    for row in cursor:
        profile=row
    conn.close()
    return profile

# loop runs if capturing has been initialized.
while 1: 
 
    # reads frames from a camera
    ret, img = cap.read() 
 
    # convert to gray scale of each frames
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
    # Detects faces of different sizes in the input image
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)
 
    for (x,y,w,h) in faces:
        # To draw a rectangle in a face 
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2) 
        id,conf=rec.predict(gray[y:y+h,x:x+w])
        profile=getProfile(id)

        if(profile!=None):
            cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[0]),(x,y+50),font,255);
            cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[1]),(x,y+100),font,255);
            cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[2]),(x,y+150),font,255);
            cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[3]),(x,y+200),font,255);

    cv2.imshow('img',img)
 
    # Wait for Esc key to stop
    if(cv2.waitKey(1) == ord('q')):
        break;
 
# Close the window
cap.release()
 
# De-allocate any associated memory usage
cv2.destroyAllWindows()