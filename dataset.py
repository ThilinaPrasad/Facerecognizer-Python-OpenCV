import cv2
import numpy as np
import sqlite3
import tkinter.messagebox
import os

#Data insert function to SQLite DB
def insertData(name,age,gender):
    conn=sqlite3.connect('FaceBase.db');
    cmd="INSERT INTO user(name,age,gender) VALUES ('"+str(name)+"','"+str(age)+"','"+str(gender)+"')"
    conn.execute(cmd);
    cmd="SELECT last_insert_rowid()"
    data = conn.execute(cmd)
    for row in data:
        user_id=int(row[0])
    conn.commit();
    conn.close();
    return user_id

#Take user inputs
user_name = input("Enter user name: ")
user_age = input("Enter user age: ")
user_gender = input("Enter user gender(M/F): ")
confirm = tkinter.messagebox.askquestion("Recognizer Info", "Are You ready to scan?\n\n(Press Q to exit in camera!)")
if(confirm=='yes'): 
    user_id = insertData(user_name,user_age,user_gender)
    faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
    cam = cv2.VideoCapture(0);          #Switch on the camera
    sampleNum=0;                        #Creare image saving sample no
    while(True):
        ret,img=cam.read();             #Read the camera input
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)   #convert the camera input to b&w in system level
        faces = faceDetect.detectMultiScale(gray,1.3,5);
        for(x,y,w,h) in faces:                      #Capture faces
            sampleNum+=1;
            cv2.imwrite("dataSet/User."+str(user_id)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w]);      
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.waitKey(100);
        cv2.imshow("User Register Monitor",img);    #Show the camera input in window
        cv2.waitKey(1);
        if(sampleNum>=20):                          #Take 20 imgs of detected face
            result = tkinter.messagebox.askquestion("Recognizer Info", "Scanned your face successfully!\n\nDo you want to train the system now?")
            if(result=='yes'):
                os.system('trainer.py')             #Train the system with newly captured images
            break;
        elif(cv2.waitKey(1)==ord('q')):             #Set quit key to the cameras
            break;
            
    cam.release()
    cv2.destroyAllWindows()

