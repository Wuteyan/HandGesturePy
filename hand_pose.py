"""
#Author : Arijit Mukherjee
#Date 	: June 2016
#B.P. Poddar Institute of Management and Technology
#Inteligent Human-Computer Interaction with depth prediction using normal webcam and IR leds
#Inspired by : http://research.microsoft.com/pubs/220845/depth4free_SIGGRAPH.pdf


Demo application to predict hand-pose from a set of test data 
"""

#Importing Opencv and Numpy
import cv2
import numpy as np

#Importing our dependencies
import util as ut
import svm_train as st 
from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO


import time


#create and train SVM model each time coz bug in opencv 3.1.0 svm.load() https://github.com/Itseez/opencv/issues/4969
model=st.trainSVM(3,40,'SICTrainData')
move_text={'1':'Rock','2':'Scissor','3':'Paper'}

#Camera and font initialization
# cam=int(raw_input("Enter Camera Index : "))
# cap=cv2.VideoCapture(cam)
# font = cv2.FONT_HERSHEY_SIMPLEX
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
GPIO.output(3, GPIO.HIGH)

#The main event loop
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640,480))

# rawCapture = PiRGBArray(camera)
 
# allow the camera to warmup
time.sleep(0.1)

# cam=int(raw_input("Enter Camera Index : "))
# cap=cv2.VideoCapture(cam)
# font = cv2.FONT_HERSHEY_SIMPLEX

for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
	move=''
	t=time.time()
	img = frame.array
	# _,img=cap.read()
	gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	ret,th1 = cv2.threshold(gray.copy(),75,255,cv2.THRESH_TOZERO)
	cv2.imshow('thresh',th1)
	_,contours,hierarchy = cv2.findContours(th1.copy(),cv2.RETR_EXTERNAL, 2)
	cnt=ut.getMaxContour(contours,4000)
	if cnt!=None:
		gesture,res=ut.getGestureImg(cnt,img,th1,model)
		print(res)
		cv2.imshow('PredictedGesture',cv2.imread('SICTrainData/'+res+'_21.jpg'))
		# move='         '+move_text[res]
		
	fps=int(1/(time.time()-t))
	# cv2.putText(img,"FPS: "+str(fps)+move,(50,50),1,(255,255,255),2,cv2.LINE_AA)
	cv2.imshow('Frame',img)
	rawCapture.truncate(0)
	k = 0xFF & cv2.waitKey(10)
	if k == 27:
		break
	

cap.release()        
cv2.destroyAllWindows()


