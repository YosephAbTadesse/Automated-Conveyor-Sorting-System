import cv2
import numpy as np
import serial
import time

# Arduino connection
arduino = serial.Serial('COM4', 9600)
time.sleep(2)

# Camera
cam = cv2.VideoCapture(1)

last_trigger = 0
cooldown = 2

while True:

    ret, frame = cam.read()

    if not ret:
        break

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red color range
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Find colored area
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    current_time = time.time()

    for cnt in contours:

        area = cv2.contourArea(cnt)

        # Ignore tiny spots
        if area > 3000:

            x, y, w, h = cv2.boundingRect(cnt)

            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                "RED OBJECT",
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            if current_time - last_trigger > cooldown:

                print("RED DETECTED")

                arduino.write(b'A')

                last_trigger = current_time

    cv2.imshow("Color Sorter", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()