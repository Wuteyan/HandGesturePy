from hand_pose import Hand_Pose
import RPi.GPIO as GPIO
import ClientSocket
from random import randint 
import time
from pyEMS.EMSCommand import ems_command
from pyEMS import openEMSstim


my_ems_board = openEMSstim.openEMSstim("/dev/tty0.usbserial",19200)
intensity1=0
intensity2=0

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(3, GPIO.OUT)
    GPIO.output(3, GPIO.LOW)
    hand_pose = Hand_Pose()
    cc = ClientSocket.ClientSocket('10.0.1.21', 4001)
    cc.connect();
    try:
        while True:
            if cc.checkRecv():
                cmd = cc.recvCmd()

                if cmd == '1':
                    GPIO.output(3, GPIO.HIGH)
                    hand_pose.startCamera()
                elif cmd == '2':
                    # GPIO.output(3, GPIO.HIGH)
                    rand_number = randint(1, 3)
                    ENS(random_number)
                    # my_ems_board.send(ems_command(1,i2,1000))
                    time.sleep(0.5)
                    result = hand_pose.getPredictedResult()
                    cc.send('p:' + str(rand_number) + 'r' + str(result))
                    # hand_pose.startCamera()
                elif cmd == '3':
                    predicted_result = hand_pose.getPredictedResult()
                    ENS(predicted_result, intensity1, intensity2)
                    # my_ems_board.send(ems_command(1,i2,1000))
                    time.sleep(0.5)
                    result = hand_pose.getPredictedResult()
                    cc.send('p:' + str(predicted_result) + 'r' + str(result))
                elif cmd == '4':
                    intensity1 = int(cc.recvAll())%1000
                elif cmd == '5':
                    intensity2 = int(cc.recvAll())%1000
                elif cmd == '6':
                    ENS(3, intensity1, intensity2)
                elif cmd == '7':
                    ENS(2, intensity1, intensity2)
                else:
                    print ("wrong cmd")
    finally:
        GPIO.output(3, GPIO.LOW)


def EMS(number, intensity1, intensity2):

    if number == 3:
        print ("scissor",)
        print (intensity2)
        my_ems_board.send(ems_command(1,intensity2,1000))
    elif number ==2:
        print ("rock",)
        print (intensity1)
        my_ems_board.send(ems_command(1,intensity1,1000))
        my_ems_board.send(ems_command(2,intensity1,1000))
    else:
        pass 
