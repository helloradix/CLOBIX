import cv2
from os import listdir
from threading import Thread, Lock

import sys, gc
from socket import *

class FaceRecognizer(object):
    def __init__(self):
        self.modelSetting() # 트레이닝 시켜놓은 Model들을 읽어 드린다
        self.face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.lock = Lock()
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind(('', 60000))
        self.sock.listen(4)


    def HandleClientRequest(self):
        # C++ 에서 연결이 들어오면 스래드를 생성시켜 판정 결과 값을 송신한다.
        while True:
            self.clnt_sock, addr = self.sock.accept()
            th = Thread(target=self.recognize, args=(self.clnt_sock,))
            th.daemon = True
            th.start()

    def modelSetting(self):
        self.dataSetLists = [] # 학습된 데이터들의 종류를 담을 변수 (ex. person의 mina, choa, hyejung 등)
        self.models = [] # 학습된 모델들을 담을 변수
        for type in listdir("DataSet"):
            tmp_model = cv2.face.LBPHFaceRecognizer_create()
            # TrainedModels폴더에 존재하는 model 파일들을 읽어들여 models 리스트에 담는다
            tmp_model.read(("TrainedModels/" + type + "_model.yaml"))
            self.models.append(tmp_model)
            elementCounter = 0
            dataSet = {}
            # DataSet 폴더에 있는 폴더 리스트(person, expression등)를 읽어드리고 안에 있는 데이터 리스트를 읽어
            # dataSet 딕셔니리에 채운다
            for element in listdir(("DataSet/" + type)):
                dataSet[elementCounter] = element
                elementCounter += 1

            # 채워진 datsSet 딕셔너리를 dataSetLists에 담는다
            self.dataSetLists.append(dataSet)

    def recognize(self, sock):
        imageFilePath = sock.recv(100) # C++로부터 이미지 파일의 경로를 전달 받는다
        try:
            image, face = self.face_detector(cv2.imread(imageFilePath))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            dataToSend = ""
            self.lock.acquire()
            # 읽어드린 학습 모델 개수만큼 반복하며 얼굴에 대한 predict 결과를 누적
            for i in range(0, len(self.models), 1):
                label, result = self.models[i].predict(face)
                if result < 500:
                    confidence = int(100 * (1 - result / 300))
                    dataToSend += "{0}|{1}|".format(self.dataSetLists[i][label], confidence)
            self.lock.release()
            self.clnt_sock.send(dataToSend) # 누적된 결과 값을 송신
            gc.collect()
        except:
            self.clnt_sock.send("/error|")

    def face_detector(self, img, size=0.5):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_classifier.detectMultiScale(gray, 1.3, 5)
        if faces is ():
            return img, []
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
            roi = img[y:y + h, x:x + w]
            roi = cv2.resize(roi, (200, 200))
        return img, roi


if __name__ == '__main__':
    obj = FaceRecognizer()
    obj.HandleClientRequest()

    sys.exit()