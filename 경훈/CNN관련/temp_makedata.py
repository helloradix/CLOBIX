from sklearn import model_selection
from sklearn.model_selection import train_test_split
from PIL import Image
import os, glob
import numpy as np

#분류대상 카테고리
root_dir="/home/iot/images/"
categories=["aoaMINA","exidJEONGHWA","GAIN","girlsdayMINA"]
nb_classes=len(categories)
image_size=50

#폴더마다의 이미지 데이터 읽어 들이기
X=[]#이미지 데이터
Y=[]#레이블 데이터
for idx,cat in enumerate(categories):
    image_dir=root_dir+"/"+cat
    files =glob.glob(image_dir+"/*.jpg")
    print("---",cat,"처리 중")
    for i, f in enumerate(files):
        img=Image.open(f)
        img=img.convert("RGB")#색상모드변경
        img=img.resize((image_size,image_size))#이미지 크기 변경
        data = np.asarray(img)
        X.append(data)
        Y.append(idx)
X=np.array(X)
Y=np.array(Y)

#학습전용데이터와 텍스트 전용데이터 분류하기
X_train,X_test,Y_train,Y_test=\
train_test_split(X,Y)
xy=(X_train,X_test,Y_train,Y_test)
np.save("./people.npy",xy)
print("ok",len(Y))
