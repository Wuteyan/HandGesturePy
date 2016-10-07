from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640,480))
 
# allow the camera to warmup
time.sleep(0.1)
 
# grab an image from the camera
# camera.capture(rawCapture, format="bgr")
# image = rawCapture.array

 
# display the image on screen and wait for a keypress
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    cv2.imshow("Image", image)
    # cv2.waitKey(0)
    rawCapture.truncate(0)
    k = 0xFF & cv2.waitKey(10)
    if k == 27:
        break