import serial
import time

arduino = serial.Serial(
    'COM4',
    9600
)

time.sleep(2)

arduino.write(b'A')

print("Signal sent")