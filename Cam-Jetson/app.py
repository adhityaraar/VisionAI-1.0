from flask import Flask, render_template, Response
import cv2
import pandas as pd
from ultralytics import YOLO

app = Flask(__name__)

HOME = "/home/adhityaraar/Documents"
model = YOLO(f"{HOME}/models/yolo5-v1.pt", 'cuda')

class_names = model.names

def gen_frames():
    try:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) #1280
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) #720
        cap.set(cv2.CAP_PROP_FPS, 10)

        while True:
            ret, frame = cap.read()
            result = model(frame, agnostic_nms=True)[0]
            labels = []
            for box in result.boxes.data:
                x1, y1, x2, y2, confidence, class_id = box
                label = f"{class_names[int(class_id)]} {confidence:.2f}"
                labels.append(label)

                color = (0, 255, 0)  # Green
                if label.startswith("NO"):
                    color = (0, 0, 255)  # Red

                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                cv2.putText(frame, label, (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            person_count = sum('Person' in label and float(label.split()[-1]) > 0.5 for label in labels)
            missing_safety = sum(label.startswith('NO') and float(label.split()[-1]) > 0.5 for label in labels)

            cv2.putText(frame, f"Person: {person_count}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, f"Missing PPE: {missing_safety}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
            ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except Exception as e:
        print(f"An error occurred: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')

