import cv2
import os

cap=cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            cv2.rectangle(frame, (175, 100), (475,400), (255,0,0), 2)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        

def capture_img():
    _, frame = cap.read()
    x1,y1 = 175, 100
    x2,y2 = 475, 400
    frame = frame[y1:y2, x1:x2]
    cv2.imwrite('static/Saved_Images/img.jpg', frame)

