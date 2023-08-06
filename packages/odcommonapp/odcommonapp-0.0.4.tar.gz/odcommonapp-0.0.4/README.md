# object_detection_common_application
This repo will help to predict the object with in image using various framework like TF2 ,Detectron and Yolo5 and also user can choose the model they need to experiment

How to use?
Fork or clone the repo.
1.Create the separate conda or virtual envoriment.
2.pip install -r requirements.txt
3. Run 
python clientApp.py

Note:
=====
If already model copied into respective framework model folder it won't download. Otherwise first time detection the model will download.


TF2 Models Prediction:
======================

1.EfficientDet D1 640x640:

![image](https://user-images.githubusercontent.com/46878296/164759399-06afea00-a1e3-4b29-9704-7e83aff58361.png)



Terminal Output:
No_of_objects_detected_by_mode: 3

Time Taken to execute the model 86.15892791748047

2.SSD MobileNet v2 320x320:

![image](https://user-images.githubusercontent.com/46878296/164757670-ec0364b8-4fe7-4506-a6ca-87fd154aa94c.png)

Terminal Output:
No_of_objects_detected_by_mode: 8

Time Taken to execute the model 27.62358021736145

3.SSD MobileNet V2 FPNLite 320x320:

![image](https://user-images.githubusercontent.com/46878296/164757303-3199f50c-e6a1-42b6-b9bd-b22a33c48c81.png)

Terminal Output:

No_of_objects_detected_by_mode: 5

Time Taken to execute the model 27.080549240112305

4.Faster R-CNN ResNet50 V1 640x640:

![image](https://user-images.githubusercontent.com/46878296/164757107-2878826d-c2b9-4150-b755-d98740796b82.png)

Terminal Output:
No_of_objects_detected_by_mode: 8

Time Taken to execute the model 78.90951347351074

5.Faster R-CNN ResNet101 V1 640x640:

![image](https://user-images.githubusercontent.com/46878296/164756209-6f7d3d2e-862a-4086-8154-55f3052d2dbb.png)

Terminal Output:

No_of_objects_detected_by_mode: 9

Time Taken to execute the model 189.88386058807373

Detectron2 Models Prediction:
============================
The model will download and  stored into your local PC following path:   

**C:\Users\<username>\.torch\iopath_cache\detectron2\COCO-Detection**

1.R50-FPN:(faster_rcnn_R_50_FPN_1x)


![image](https://user-images.githubusercontent.com/46878296/164746614-c3355f00-0b76-44ba-b1db-48a101f04e83.png)

Terminal Output:
The no.of object detected by model are: 10

['bowl 99%', 'chair 98%', 'refrigerator 95%', 'sink 93%', 'oven 81%', 'bottle 66%', 'dining table 61%', 'vase 61%', 'cup 58%', 'bowl 57%']

Time Taken to execute the model 25.72547149658203


2.R50-C4:(faster_rcnn_R_50_C4_1x)

![image](https://user-images.githubusercontent.com/46878296/165212575-dc2fa121-19d3-4b71-b9f8-503df9514b95.png)


Terminal Output:

The no.of object detected by model are: 8
['bowl 99%', 'bowl 98%', 'bowl 96%', 'bowl 95%', 'carrot 95%', 'carrot 93%', 'carrot 77%', 'dining table 72%']
Time Taken to execute the model 27.740586757659912




3.R101-FPN (faster_rcnn_R_101_C4_3x)
![image](https://user-images.githubusercontent.com/46878296/165213051-65b4fbcf-fd0f-4a08-a96e-9bc8539a4b01.png)

Terminal Output:
The no.of object detected by model are: 8
['bowl 99%', 'dining table 96%', 'broccoli 95%', 'cake 94%', 'broccoli 84%', 'broccoli 80%', 'broccoli 76%', 'sandwich 75%']
Time Taken to execute the model 46.38965344429016

4.R101-FPN (faster_rcnn_R_101_FPN_3x)
![image](https://user-images.githubusercontent.com/46878296/165213290-eac9afd7-198f-4adf-8f60-f90c0be5e624.png)

Terminal Output:
The no.of object detected by model are: 20
['clock 100%', 'clock 100%', 'car 99%', 'person 99%', 'person 98%', 'person 98%', 'person 96%', 'person 96%', 'person 94%', 'car 90%', 'fire hydrant 77%', 'handbag 75%', 'person 75%', 'person 74%', 'person 60%', 'stop sign 59%', 'traffic light 59%', 'person 59%', 'person 57%', 'oven 56%']
Time Taken to execute the model 31.190783977508545

YOLO5
=====

1.YOLOv5s

![image](https://user-images.githubusercontent.com/46878296/165214021-693f04c9-f7c7-4331-93d9-d2471728bc5e.png)

Terminal O/P:
1 bowl, 1 sandwich, 1 dining table
Time Taken to execute the model 4.314246654510498

2.YOLOv5m
![image](https://user-images.githubusercontent.com/46878296/165214364-9c276db9-f653-43c3-8c57-11cad07d847b.png)

Terminal O/P:

14 persons, 1
baseball bat, 1 baseball glove, Done. (0.441s)


3.YOLOv5l

![image](https://user-images.githubusercontent.com/46878296/165214519-7e7abdec-62b3-4534-a2cd-1ca0e522cc67.png)

3 bowls, 1 apple, 2 chairs, 1 dining table, 1 microwave, 1 oven, 1 sink, 1 refrigerator, Done. (1.559s)
Terminal O/P:

4.YOLOv5x
![image](https://user-images.githubusercontent.com/46878296/165214858-4a00d09d-4084-496a-a410-5dc14c9d4801.png)


Terminal O/P:
8 persons, 2 cars, 2 clocks, Done. (2.369s)

5.YOLOv5s6
![image](https://user-images.githubusercontent.com/46878296/165215364-d60991a6-509d-43e9-8a0d-b268e818e0f4.png)

Terminal O/P:
12 persons, 9
chairs, 1 dining table, 1 tv, 1 clock, Done. (1.738s)

