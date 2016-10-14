from hand_pose import Hand_Pose
import RPi.GPIO as GPIO
import ClientSocket
from random import randint 
import time
from pyEMS.EMSCommand import ems_command
from pyEMS import openEMSstim
from threading import Thread

my_ems_board = openEMSstim.openEMSstim("/dev/tty0.usbserial",19200)
intensity1 = 0
intensity2 = 0
mode = 1

def cameraThreadFunc(handPose):
    print ('start camera')
    GPIO.output(3, GPIO.HIGH)
    handPose.startCamera()

def EMS(number, intensity1, intensity2):
    if number == 2:
        print ("scissor",)
        print (intensity2)
        my_ems_board.send(ems_command(1,intensity2,1000))
    elif number == 1:
        print ("rock",)
        print (intensity1)
        my_ems_board.send(ems_command(1,intensity1,1000))
        my_ems_board.send(ems_command(2,intensity1,1000))
    else:
        pass 

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(3, GPIO.OUT)
    GPIO.output(3, GPIO.LOW)
    hand_pose = Hand_Pose()
    cc = ClientSocket.ClientSocket('10.0.1.33', 4001)
    #cc.connect();
    GPIO.output(3, GPIO.HIGH)
    hand_pose.startCamera()
    #recvThread = Thread(target = cameraThreadFunc, args = (hand_pose,))
    #recvThread.start()
    
    try:
        while True:
            if cc.checkRecv():
                cmd = cc.recvCmd()
                params = cc.recvParam()
                print ("cmd = %s" % cmd)
                print ("params = %s" % params)
                
                if cmd == '1':
                    intensity1 = int(params[0])
                    intensity2 = int(params[1])
                    mode = int(params[2])
                elif cmd == '2':
                    if mode == 1:
                        rand_number = randint(1, 3)
                        EMS(rand_number, intensity1, intensity2)
                        time.sleep(0.5)
                        result = hand_pose.posPredict()
                        result = 1
                        if (rand_number == result):
                            cc.send('3')
                        elif ((rand_number - result == 1) or (rand_number - result == -2)):
                            cc.send('1')
                        else:
                            cc.send('2')
                    else:
                        predictResult = hand_pose.posPredict()
                        EMS(predictResult, intensity1, intensity2)
                        time.sleep(0.5)
                        realResult = hand_pose.posPredict()
                        if (predictResult == realResult):
                            cc.send('3')
                        elif ((predictResult - realResult == 1) or (predictResult - realResult == -2)):
                            cc.send('1')
                        else:
                            cc.send('2')                    
                elif cmd == '3':
                    intensity1 = int(params[0])
                    intensity2 = int(params[1])
                    mode = int(params[2])
                    ENS(mode, intensity1, intensity2)
                else:
                    print ("wrong cmd")
    finally:
        GPIO.output(3, GPIO.LOW)
