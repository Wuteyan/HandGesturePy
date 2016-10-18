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



import time
class  Hand_Pose():
	"""docstring for  Hand_Pose"""
	def __init__(self):
		super( Hand_Pose, self).__init__()
		self.model=st.trainSVM(3,40,'SICTrainData')
		self.move_text={'1':'Rock','2':'Scissor','3':'Paper','4':'Scissor','5':'Paper'}
		
		self.buffer = []
		self.resBuf = []
		#The main event loop
		# initialize the camera and grab a reference to the raw camera capture
		self.camera = PiCamera()
		self.camera.resolution = (640, 480)
		self.camera.framerate = 32
		
		
	def startCamera(self):
		#create and train SVM model each time coz bug in opencv 3.1.0 svm.load() https://github.com/Itseez/opencv/issues/4969
		rawCapture = PiRGBArray(self.camera, size=(640,480))
		# rawCapture = PiRGBArray(camera)
		self.resBuf[:] =[]
		# allow the camera to warmup
		time.sleep(0.1)

	# cam=int(raw_input("Enter Camera Index : "))
	# cap=cv2.VideoCapture(cam)
	# font = cv2.FONT_HERSHEY_SIMPLEX

		for frame in self.camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
			move=''
			t=time.time()
			img = frame.array
			# _,img=cap.read()
			gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
			ret,th1 = cv2.threshold(gray.copy(),75,255,cv2.THRESH_TOZERO)
			# cv2.imshow('thresh',th1)
			_,contours,hierarchy = cv2.findContours(th1.copy(),cv2.RETR_EXTERNAL, 2)
			cnt=ut.getMaxContour(contours,4000)
			if cnt!=None:
				gesture,res=ut.getGestureImg(cnt,img,th1,self.model)
				if len(self.resBuf) > 10:	
					self.resBuf.pop(0) 
					self.resBuf.append(res)
				else : self.resBuf.append(res)
				# print(res)
				# cv2.imshow('PredictedGesture',cv2.imread('SICTrainData/'+res+'_21.jpg'))
				# move='         '+move_text[res]
				
			fps=int(1/(time.time()-t))
			# cv2.putText(img,"FPS: "+str(fps)+move,(50,50),1,(255,255,255),2,cv2.LINE_AA)
			# cv2.imshow('Frame',img)
			rawCapture.truncate(0)
			k = 0xFF & cv2.waitKey(10)
			if k == 27:
				break
		

		cap.release()        
		# cv2.destroyAllWindows()

	def posPredict(self):
		# check resBuf and get the most possible gesture
		posRock = 0
		posScissors = 0
		posPapper = 0
		# SCOTT PRINT TEST
		# print (self.resBuf)
		for i in range(len(self.resBuf)):
			if self.resBuf[i] == "1":
				posRock = posRock + 1
			elif self.resBuf[i] == "2":
				posScissors = posScissors + 1
			elif self.resBuf[i] == "3":
				posPapper = posPapper + 1
		posFinal = max(posPapper, posScissors, posRock)
		# print (str(posRock))
		# print (str(posScissors))
		# print (str(posPapper))
		# clear resBuf
		self.resBuf[:] = []
		if posFinal == posRock:
			return 1
		elif posFinal == posScissors:
			return 2
		else:  return 3


	# def getbuffer(self):

