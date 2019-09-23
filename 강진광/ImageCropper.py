import cv2
from os import listdir
from os.path
import sys

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

def faceCropWriter():
    path = 'testimage/'
    for person in listdir(path):
		personDirPath = path+person+"/"
		writeImage(person, personDirPath)

def writeImage(person, personDirPath):
	imageList = listdir(personDirPath)
	pathToWrite = "croppedimages/"+person+"/"
	imageCounter = 0
	for imageFileName in imageList:
		print(personDirPath+imageFileName)
		try:
			image, face = face_detector(cv2.imread(personDirPath+imageFileName))
			writeFileName = "{0}{1}_{2}.jpg".format(pathToWrite, person, imageCounter)
			while True:
				if os.path.exist(writeFileName):
					imageCounter+=1
					writeFileName = "{0}{1}_{2}.jpg".format(pathToWrite, person, imageCounter)
				else:
					break
					
			cv2.imwrite(writeFileName, face)
			imageCounter += 1
		except:
			print("face not found")
			
if __name__ == '__main__':
	faceCropWriter()