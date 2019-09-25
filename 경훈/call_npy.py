from keras.utils import np_utils
import numpy as np
import cv2

X_train, X_test, Y_train, Y_test = np.load("./people.npy",allow_pickle=True)

X_test=X_test.astype("float")/256#정규화

# test갯수 = len(Y_test)
#Y_test의 중복제거를 하면 사람 이름명단이 나올 것!
#사람별로, 4칸짜리 배열을 만들어서 , 계산해야할것이다.
#Y_test의 종류 : set(Y_test)~~ set을 하면 순서는 깨진다. 단지 배열을 만들기위함..
#테스트시에는 Y_test를 써야함.


#########인물마다 평가를 기록할 리스트 작성 일단 모두 0으로 초기화
#[사람이름, a,b,c,d] 
#data_line[n][1]:a:사람이름에 해당하는 사진을 넣었을 때, 모델이 해당 인물을 모의
#data_line[n][2]:b:사람이름에 해당하는 사진을 넣었을 때, 모델이 다른 인물을 모의 
#data_line[n][3]:c:사람이름에 해당하지 않는 사진을 넣었을 때, 모델이 이 인물을 모의
#data_line[n][4]:d:사람이름에 해당하지 않는 사진을 넣었을 때, 사람이름에 해당하지 해당 사진을 모의
categories=list(set(Y_test))

data_list=[]#임시기록[이름, a,b,c,d]
send_list=[]#DB에 직접 갈 아이[이름,Accuracy , F1 Score] 
for cat in categories:
    data_line=[]
    data_line.append(cat)
    data_line.append(0)
    data_line.append(0)
    data_line.append(0)
    data_line.append(0)
    data_list.append(data_line)

for cat in categories:
    send_line=[]
    send_line.append(cat)
    send_line.append(0)
    send_line.append(0)
    send_list.append(send_line)

#모델 불러오기
model=cv2.face.LBPHFaceRecognizer_create()
model.read("/home/iot/KH/mina.yml")
#model.read("/home/iot/AIServer/TrainedModel/1_person-2_model.yaml")
#X_test갯수만큼 모의 
for idx,img in enumerate(X_test):
    #X_test값 모의  시도하기 
    machine_think_result=model.predict(img)
    #machin_think_result[0]은 label, result[1]은 신뢰도일것, 우린 label만필요하다.
    #결과~
    #Y_test값과 비교
    #for 문을 이용해 모든 data_list의 행에 접근 값조정해줌,
    for idx_line,line in enumerate(data_list): 
        if(line[0]==Y_test[idx] and line[0]==machine_think_result):line[1]+=1
        elif(line[0]==Y_test[idx] and line[0]!=machine_think_result):line[2]+=1
        elif(line[0]!=Y_test[idx] and line[0]==machine_think_result):line[3]+=1
        else :line[4]+=1

#test출력
print(data_list)

def makeAccuracy(line):
    return line[1]/(line[1]+line[2]+line[3]+line[4])
def makeF1Score(line):
    if(line[1]+line[3]==0):precision=0
    else: precision=line[1]/(line[1]+line[3])
    recall= line[1]/(line[1]+line[2])
    
    if precision+recall==0 : return 0                       
    return (2*precision*recall)/(precision+recall)


#send_list에 data_list를 이용 필요값대입.
for idx,line in enumerate(data_list):
    send_list[idx][0]=line[0]
    send_list[idx][1]=makeAccuracy(line)
    send_list[idx][2]=makeF1Score(line)

print(send_list)#확인겸,
