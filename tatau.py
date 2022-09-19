## Bagian Library
import cv2  #Library Open CV untuk pengolahatn citra
from cvzone.HandTrackingModule import HandDetector ##Library cvzone untuk module tracking
from cvzone.ClassificationModule import Classifier ## lirary klasifikasi
import numpy as np #library numpy untuk pengolahan matematis komputasi
import math        #Library math untuk matematika dasar
from gtts import gTTS #Library get Text To Speech untuk membaca kata
import os           #memasukkan envoirentmen os


#### untuk parsing arduino ####
import serial   #Library komunikasi serial
import time     #Library waktu


arduino = serial.Serial(port='COM8', baudrate=115200, timeout=.1) #mengkoneksikan arduino dari device Manager
#### arduino ####

### Bagian memanggil kamera dan data yang sudah di train
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("Data P7/keras_model.h5", "Data P7/labels.txt") #Direktory data bagian vision
count=0
offset = 20
imgSize = 300
folder = "Data/C"
counter = 0

# labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "U", "Y", "Stop", ""]
labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "R", "S", "T", "U", "V", "W", "Y", "ZRun",""]
labelPrev = labels[0]
tekseja = labels[24]

#Proses dari menghidupkan kamera dan mengolah data
while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)

    
    data = arduino.readline().decode('ascii') #membaca nilai dari board arduino
    mylist=data.split(',')

    # 
    try:
        if(mylist[1]== True):
            pass
        a=int(mylist[0])
        b=int(mylist[1])
        c=int(mylist[2])
        d=int(mylist[3])
        e=int(mylist[4])
    except:
        continue

   

    # print(type(a))
    # print(a,'\t',b,'\t',c,'\t',d,'\t',e)

    try:
        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']

            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

            imgCropShape = imgCrop.shape

            aspectRatio = h / w

            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)
                # print(prediction, index)

                mytext = labels[index]

            ### Bagian treshold antar text dengan nilai yang lahir dari sensor flex

                if(mytext == labels[0] or mytext == labels[4] or mytext == labels[13] or mytext == labels[14] 
                or mytext == labels[18] or mytext == labels[23] or mytext == labels[21] ):
                    if a > 200 and a < 300 and b > 300 and c > 300 and d > 300 and e < 900  : 
                        #huruf A
                        mytext = labels[0]
                    elif a > 300 and b < 300 and c < 300  and e < 300  : 
                        #huruf B
                        mytext = labels[1]
                    elif a > 300 and b > 300 and c > 300 and d > 300 and e > 300  : 
                        #huruf E
                        mytext = labels[4]                    
                    elif a < 220 and b > 300 and c > 300 and d < 300 and e < 300 : 
                        #huruf N
                        mytext = labels[14]
                    elif a < 360 and b > 300 and c > 300 and d > 320 and e > 390 and a > 340: 
                        #huruf S
                        mytext = labels[18]
                    elif a > 200 and b > 300 and d < 300 and e > 300 and c > 300 :
                        #huruf y
                        mytext = labels[18]
                    elif a < 300 and b < 300 and d < 300 and e < 300 and c > 300 :
                        #huruf w
                        mytext = labels[21]
    


                if (mytext == labels[23]):
                    if (len(tekseja) != 0):
                        # language = 'id'
                        # myobj = gTTS(text=tekseja, lang=language, slow=True)
                        # myobj.save("welcome.mp3")
                        # os.system("mpg321 welcome.mp3")
                        tekseja = labels[24]

                else:
                    if (mytext != labelPrev):
                        count+=1
                        if(count>15):
                            tekseja = tekseja + mytext
                            labelPrev = mytext
                        # tekseja.append(mytext)
                        # tekseja = tekseja + mytext

                        print(tekseja)

                        
                    else:
                        count=0

            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=True)

            
            

            cv2.rectangle(imgOutput, (x - offset, y - offset - 50),
                          (x - offset + 90, y - offset - 50 + 50), (255, 0, 255), cv2.FILLED)
            cv2.putText(imgOutput, labels[index], (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
            cv2.rectangle(imgOutput, (x - offset, y - offset),
                          (x + w + offset, y + h + offset), (255, 0, 255), 4)

            cv2.imshow("ImageCrop", imgCrop)
            cv2.imshow("ImageWhite", imgWhite)
    except:
        continue

    font = cv2.FONT_HERSHEY_COMPLEX #font yang digunakant
    cv2.putText(imgOutput,tekseja,(50,50),font,2,(0,215,255),1) #huruf yang muncul di layar

    cv2.imshow("Image", imgOutput)
    cv2.waitKey(10)