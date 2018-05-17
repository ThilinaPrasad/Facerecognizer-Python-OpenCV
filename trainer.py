import os
import cv2
import numpy as np
from PIL import Image

recognizer=cv2.face.LBPHFaceRecognizer_create();    #Initialize the openCV face recognizer
samplePath = "dataSet"

#Get captured images in dataSet folder
def getImagesWithid(path):  
    imgPaths = [os.path.join(path,f) for f in os.listdir(path)] # get all the file in to list from dataSet Dir
    faces=[]
    ids=[]
    for imgPath in imgPaths:
        faceImg=Image.open(imgPath).convert('L');
        faceNp=np.array(faceImg,'uint8')
        user_id=int(os.path.split(imgPath)[-1].split('.')[1])
        faces.append(faceNp)
        ids.append(user_id)
        cv2.imshow('training',faceNp)
        cv2.waitKey(10)
    return np.array(ids),faces

ids, faces = getImagesWithid(samplePath);
recognizer.train(faces,ids)         #train the application with captured images
recognizer.save('trainerData/trainedData.yml')  #save the current specific data to the each face in .yml file
cv2.destroyAllWindows();
