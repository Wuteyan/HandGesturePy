import hand_pose
import RPi.GPIO as GPIO
import ClientSocket

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(3, GPIO.OUT)
    GPIO.output(3, GPIO.LOW)
    hand_pose = Hand_Pose()
    cc = client_socket('10.0.1.21', '4001')
    cc.connect();
    # cc = client_socket();
    try:
        while cc.check_recv():
            if cc.recv(1024)== 1:
                GPIO.output(3, GPIO.HIGH)
                hand_pose.startCamera()
            elif cc.recv(1024) == 2:
                # GPIO.output(3, GPIO.HIGH)
                # hand_pose.startCaeximera()
            elif cc.recv(1024) == 3:

    finally:
        GPIO.output(3, GPIO.LOW)

