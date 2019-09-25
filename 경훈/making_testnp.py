from sklearn import model_selection
from sklearn.model_selection import train_test_split
from PIL import Image
import os, glob
from os import listdir
import numpy as np

import cv2

#분류대상 카테고리
root_dir="/home/iot/images/"
image_size=50

face_classifier=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#폴더마다의 이미지 데이터 읽어 들이기
X=[]#이미지 데이터
Y=[]#레이블 데이터
for person in listdir(root_dir):
    print("---",person,"처리 중")
    image_dir=root_dir+"/"+person+"/"
    files =glob.glob(image_dir+"/*.jpg")
    for i, f in enumerate(files):
        try:
            img=cv2.imread(f,cv2.IMREAD_GRAYSCALE)#파일을 그레이스케일로 읽음,
            faces=face_classifier.detectMultiScale(img,1.3,5)#얼굴을 찾아 분류
            if faces is():
                continue#찾은 얼굴이 없으면 돌아감 
            for(x,y,w,h) in faces:
                img=img[y:y+h,x:x+w]
                img=cv2.resize(img,(image_size,image_size))
        except:
            #혹시나 오류가 있었다면 넘어감
            continue
        data = np.asarray(img)
        X.append(data)
        Y.append(person)
X=np.array(X)
Y=np.array(Y)

#학습전용데이터와 텍스트 전용데이터 임의로 분류하기
X_train,X_test,Y_train,Y_test=train_test_split(X,Y)
xy=(X_train,X_test,Y_train,Y_test)
#print(xy)#xy로 원하는 데이터가 잘 들어갔는지 확인을 위해 한번 출력
np.save("./people.npy",xy)
print("ok",len(Y))
