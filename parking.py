import cv2
import numpy as np
import pickle
import pandas as pd
from ultralytics import YOLO
import cvzone
with open ("saved","rb") as f:
        data = pickle.load(f)
        shapes,area_names = data["shapes"],data["area_names"]


my_file = open("C:\\Users\\MISHO TECHNOLOGY\\Downloads\\Parking\\future parking\\yolov8-advance-parkingspace-detection-main\\coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

model=YOLO('yolov8s.pt')


cap=cv2.VideoCapture("easy.mp4")




count=0

while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
   
    count += 1
    if count % 3 != 0:
       continue

    frame=cv2.resize(frame,(1020,500))
    frame_copy = frame.copy()
    results=model.predict(frame)
 #   print(results)
    a=results[0].boxes.data
    px=pd.DataFrame(a).astype("float")
#    print(px)
    list1 = []
    for index,row in px.iterrows():
#        print(row)
 
        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])
        d=int(row[5])
        
        c=class_list[d]
        cx=int(x1+x2)//2
        cy=int(y1+y2)//2
        if "car" in c :
            list1.append([cx,cy])
        counter1 = [] 
        list2 = []
    for i,shape in enumerate(shapes):
        list2.append(i)
        cv2.polylines(frame,[shape],True,(0,255,0),2)
        cvzone.putTextRect(frame,f'{area_names[i]}',tuple(shape[0]),1,1) 
        for i1 in list1:
            cx1 = i1[0]
            cy1 = i1[1]
            result = cv2.pointPolygonTest(shape,((cx1,cy1)),False)
            if result >0:
                # cv2.circle(frame,(cx,cy),5,(0,0,255),-1)
                cv2.polylines(frame,[shape],True,(0,0,255),2)
                counter1.append(cx1)

    car_count = len(counter1)  
    free_space = len(list2) - car_count
    cvzone.putTextRect(frame,f'free_space = {free_space}',(20,30),2,2,(255,255,255)) 
    cvzone.putTextRect(frame,f'car_count = {car_count}',(20,80),2,2,(255,255,255))     
    cv2.imshow('FRAME', frame)
   

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # Press 'Esc' to exit
        break
   

cap.release()
cv2.destroyAllWindows()

