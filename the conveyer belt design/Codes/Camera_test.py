import cv2

cam = cv2.VideoCapture(1)

while True:

    ret, frame = cam.read()

    cv2.imshow("My Camera", frame)

    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()