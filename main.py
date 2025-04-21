import cv2
import numpy as np


# Opencv DNN
net = cv2.dnn.readNet("D:/project/dnn_model/yolov4-tiny.weights", "D:/project/dnn_model/yolov4-tiny.cfg")
model = cv2.dnn_DetectionModel(net) 
model.setInputParams(size=(320, 320), scale=1/255)

#Load class lists
classes = []
with open("D:/project/dnn_model/classes.txt", "r") as file_object:
    for class_name in file_object.readlines():
        class_name = class_name.strip()
        classes.append(class_name)

print("Objects list")
print(classes)

#Initialize camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1366)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)

def click_button(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        polygon =np.array([[(20,20), (260, 260), (260, 90), (20, 90)]])

        is_inside = cv2.pointPolygonTest(polygon, (x, y), False)
        if is_inside > 0:
            print("We're clicking inside th ebutton", x, y)

#Create window
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", click_button)

while True:
    #Get frame
    ret, frame = cap.read()


     #Object Detection
    (class_ids, scores, bboxes) = model.detect(frame)
    for class_id, score, bbox in zip(class_ids, scores, bboxes):
        (x, y, w, h) = bbox
        class_name = classes[class_id]

        cv2.putText(frame, str(class_name), (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 2, (200, 0, 50), 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (200, 0, 50), 3)


    #Create Button
    #cv2.rectangle(frame, (20, 20), (220, 70), (0, 0, 200), -1)
    polygon =np.array([[(20,20), (260, 260), (260, 90), (20, 90)]])
    cv2.fillPoly(frame, polygon, (0, 0, 200))
    cv2.putText(frame, "Person", (30, 60), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)


    cv2.imshow("Frame", frame)
    cv2.waitKey(1)
