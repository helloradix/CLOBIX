import cv2
import numpy as np
from os import listdir
import os.path
import sys


model = cv2.face.LBPHFaceRecognizer_create()
model.read("model.yaml")
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def trainFaces():
	path = 'croppedimages/'
	trainingData, labels = [], []
	labelCounter = 0 
	for person in listdir(path):
		personDirPath = path+person+"/"
		imageList = listdir(personDirPath)
		
		for imageFileName in imageList:
			image = cv2.imread(personDirPath+imageFileName, cv2.IMREAD_GRAYSCALE)
			trainingData.append(np.asarray(image, dtype = np.uint8))
			labels.append(labelCounter)
		
		labelCounter+=1 
		
	labels = np.asarray(labels, dtype=np.int32)
	model.train(np.asarray(trainingData), np.asarray(labels))
	model.write("model.yaml")
	print("training complete")
	
if __name__ == '__main__':
	trainFaces()