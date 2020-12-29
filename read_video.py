import cv2

cap = cv2.VideoCapture(1)
while True:
    ret , frame = cap.read()
    if not ret:
        break
    cv2.imshow("frame" , frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
