import hand_pose
import RPi.GPIO as GPIO
import ClientSocket
from random import randint 
import time

my_ems_board = openEMSstim.openEMSstim("/dev/tty0.usbserial",19200)
intensity1=0
intensity2=0

def callback(data):
    if data== '1':
        GPIO.output(3, GPIO.HIGH)
        hand_pose.startCamera()
    elif data == '2':
        # GPIO.output(3, GPIO.HIGH)
        rand_number = randint(1, 3)
        ENS(random_number)
        # my_ems_board.send(ems_command(1,i2,1000))
        time.sleep(0.5)
        result = hand_pose.getPredictedResult()
        cc.send('p:' + str(rand_number) + 'r' + str(result))
        # hand_pose.startCamera()
    elif data == '3':
        predicted_result = hand_pose.getPredictedResult()
        ENS(predicted_result, intensity1, intensity2)
        # my_ems_board.send(ems_command(1,i2,1000))
        time.sleep(0.5)
        result = hand_pose.getPredictedResult()
        cc.send('p:' + str(predicted_result) + 'r' + str(result))
    elif data[0] == '4':
        intensity1 = int(data)%1000
    elif data[0] == '5':
        intensity2 = int(data)%1000
    elif data[0] == '6':
        ENS(3, intensity1, intensity2)
    elif cc.recv(1024)[0] == '7':
        ENS(2, intensity1, intensity2)

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(3, GPIO.OUT)
    GPIO.output(3, GPIO.LOW)
    hand_pose = Hand_Pose()
    cc = ClientSocket.ClientSocket('10.0.1.21', '4001')
    cc.connect();
    cc.recv(callback)
    # cc = client_socket();
    try:
        while True:
            pass
    finally:
        GPIO.output(3, GPIO.LOW)


def EMS(number, intensity1, intensity2):

    if number == 3:
        print "scissor",
        print intensity2
        my_ems_board.send(ems_command(1,intensity2,1000))
    elif number ==2:
        print "rock",
        print intensity1
        my_ems_board.send(ems_command(1,intensity1,1000))
        my_ems_board.send(ems_command(2,intensity1,1000))
    else:
        pass 