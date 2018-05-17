import cv2,os
import numpy as np
from PIL import Image
import pickle
import sqlite3
import time
import tkinter.messagebox

recognizer=cv2.face.LBPHFaceRecognizer_create();        #initialize the OpenCV inbuilt recognizer in application
recognizer.read('trainerData/trainedData.yml')          #read the previously trained data in the application
faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
path="dataSet"                                          #Set path of the images

#Get user data from SQLite db
def getProfile(id):
    conn=sqlite3.connect("FaceBase.db");
    cmd = "SELECT * FROM user WHERE id="+str(id)
    data=conn.execute(cmd)
    profile=None
    for row in data:
        profile=row
    conn.close()
    return profile
    
cam = cv2.VideoCapture(0);                              #Switch on the camera
fontface = cv2.FONT_HERSHEY_COMPLEX                     #Initialize the openCV font for the detected face
fontscale = 0.5
fontcolor = (0, 255, 0)
timer = []

while(True):
    ret,img=cam.read();                                 #Read camera input
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)           #Convert camera input into gray scale in application level
    faces = faceDetect.detectMultiScale(gray,1.3,5);    #Detect the faces in camera input
    detected=False
    for(x,y,w,h) in faces:
        id, conf = recognizer.predict(gray[y:y+h,x:x+w])    #Recognize the face on past trained data
        print(conf)
        if(conf>70):                                        #Recogize actual face on the confidence level of the face detection
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            profile=getProfile(id);
            if(profile!=None):                              #Set User data to the live camera input
                this_time= int(round(time.time() * 1000))
                timer.append(this_time)
                #print(timer)
                cv2.putText(img,"Name: "+str(profile[1]), (x,y+h+30), fontface, fontscale, fontcolor)
                cv2.putText(img,"Age: "+str(profile[2]), (x,y+h+50), fontface, fontscale, fontcolor)
                cv2.putText(img,"Gender: "+str(profile[3]), (x,y+h+70), fontface, fontscale, fontcolor)
                #print(timer[-1]-timer[0])
                if(timer[-1]-timer[0] >=3000):
                    detected = True
            else:
                cv2.putText(img,str("Unknown"), (x,y+h+30), fontface, fontscale, fontcolor)
        else:
            timer = []
    if(detected):
        confirm = tkinter.messagebox.askquestion("Recognized", "System recognized you successfully!")
        if(confirm=="yes"):
            break
    cv2.imshow("Detection Monitor",img);
    if(cv2.waitKey(1)==ord('q')):                           #Set quit key Q
        break;
cam.release()
cv2.destroyAllWindows()
