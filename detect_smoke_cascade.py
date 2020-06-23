import cv2


def detect_smoke_cascade(frame):
    smoke_cascade = cv2.CascadeClassifier("hand_cascade.xml")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    smoke = smoke_cascade.detectMultiScale(gray,
    scaleFactor=1.05,
    minNeighbors=5)
    cv2.imshow("d", frame)
    cv2.waitKey(1)
    for x,y,w,h in smoke:
        img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.imshow("d", img)
        cv2.waitKey(1)
        area = w*h
        if area > 10000:
            img= cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),3)
            return True
        else:
            return False



