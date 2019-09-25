from PIL import Image
import os, glob
import numpy as np
import random, math
#회전해서 학습하기
#분류대상 카테고리
root_dir="/home/iot/images/"
categories=["aoaMINA","exidJEONGHWA","GAIN","girlsdayMINA"]
nb_classes=len(categories)
image_size=50

#이미지 데이터 읽어들이기
X=[] #이미지 데이터
Y=[]#레이블 데이터
def add_sample(cat, fname, is_train):
	img=Image.open(fname)
	img=img.convert("RGB") #색상모드 변경하기
	img=img.resize((image_size,image_size))#이미지 크기 변경
	data=np.asarray(img)
	X.append(data)
	Y.append(cat)
	if not is_train: return
        #각도를 조금 변경한 파일 추가하기
        #회전하기
	for ang in range(-20, 20, 5):
		img2=img.rotate(ang)
		data=np.asarray(img2)
		X.append(data)
		Y.append(cat)
                #img2.save("people-"+str(ang)+".PNG")로 회전한 사진 저장가능
                #반전하기 
		img2=img2.transpose(Image.FLIP_LEFT_RIGHT)
		data=np.asarray(img2)
		X.append(data)
		Y.append(cat)

def make_sample(files,is_train):
	global X,Y
	X=[];Y=[]
	for cat, fname in files:
	    add_sample(cat, fname, is_train)
	return np.array(X),np.array(Y)

#각 폴더안에 있는 파일 수집하기
allfiles=[]
for idx, cat in enumerate(categories):
	image_dir=root_dir+"/"+cat
	files=glob.glob(image_dir+"/*.jpg")
	for f in files:
	    allfiles.append((idx,f))#파일의 인덱스와내용 저장

#섞은 뒤에 학습 전용 데이터와 테스트 전용 데이터 구분하기
random.shuffle(allfiles)
th=math.floor(len(allfiles)*0.6)
train=allfiles[0:th]
test = allfiles[th:]
X_train,Y_train = make_sample(train,True)
X_test,Y_test=make_sample(test,False)
xy= (X_train,X_test,Y_train,Y_test)
np.save("./people2.npy",xy)
print("ok,",len(Y_train))
