import temp_makedata2 as makedata
import sys,os
from PIL import Image
import numpy as np

#명령줄에서 파일 이름 지정하기
if len(sys.argv) <= 1:
    print("temp_datacheck.py (<파일이름>)")

image_size=50
categories=["aoaMINA","exidJEONGHWA","GAIN","girlsdayMINA"]
group_name=["AOA","EXID","BrownEyedGirls","GirlsDay"]

#입력이미지를 Numpy로 변환하기
X=[]
files=[]

for fname in sys.argv[1:]:
    img=Image.open(fname)
    img=img.convert("RGB")
    img=img.resize((image_size,image_size))
    in_data=np.asarray(img)
    X.append(in_data)
    files.append(fname)
X=np.array(X)

#CNN모델 구축하기
model=makedata.build_model(X.shape[1:])
model.load_weights("peoplemodel.hdf5") #temp_data2에서 저장했던 hdf5모델 불러옴

#데이터 예측하기
html=""
pre=model.predict(X)
for i, p in enumerate(pre):
    Y=p.argmax()
    print("+입력:",files[i])
    print("|이름:",categories[Y])
    print("|그룹명:",group_name[Y])
