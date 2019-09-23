import cv2
import numpy as np
from os import listdir
import os.path
import sys

model = cv2.face.LBPHFaceRecognizer_create()
model.read("model.yaml")
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def face_detector(img, size = 0.5):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)
    if faces is():
        return img,[]
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,255),2)
        roi = img[y:y+h, x:x+w]
        roi = cv2.resize(roi, (200,200))
    return img,roi   
	

def recognizeFace(imageFileName):
	personNames ={}
	counter = 0

	for person in listdir("croppedimages/"):
		personNames[counter] = person
		counter+=1
	
	try:
		image,face = face_detector(cv2.imread(imageFileName))
		face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
		label, result = model.predict(face)
		
		if result < 500:
			confidence = int(100*(1-result/300))
			display_string = str(confidence)+'% Confidence it is user'
			print(display_string)
			print("recognized as {0}, {1} confidence".format(personNames[label], confidence))
		else:
			print("can't recognize face")
	except:
		print("face not found")
		
if __name__ == '__main__':
	recognizeFace(sys.argv[1])