from flask import Flask, render_template, Response, jsonify
import cv2
from ultralytics import YOLO
import atexit
import time
import subprocess

app = Flask(__name__)

HOME = "/home/adhityaraar/Documents"
model = YOLO(f"{HOME}/models/yolo8n-v1.pt", 'cuda')
class_names = model.names

cap = None

def is_camera_index_valid(index):
    cap = cv2.VideoCapture(index, cv2.CAP_V4L2)
    is_opened = cap.isOpened()
    cap.release()
    return is_opened

def get_video_capture():
    global cap
    if cap is None or not cap.isOpened():
        if cap is not None:
            cap.release()
        cap = next((cv2.VideoCapture(i) for i in range(10) if is_camera_index_valid(i)), None)
        if cap is not None:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    return cap

def gen_label(frame):
    result = model(frame, agnostic_nms=True)[0]
    labels = []

    for box in result.boxes.data:
        x1, y1, x2, y2, confidence, class_id = box
        label = f"{class_names[int(class_id)]} {confidence:.2f}"
        labels.append(label)
        color = (0, 0, 255) if label.startswith("NO") else (0, 255, 0)
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
        cv2.putText(frame, label, (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    person_count = sum('Person' in label and float(label.split()[-1]) > 0.5 for label in labels)
    no_ppe_count = sum(label.startswith('NO') and float(label.split()[-1]) > 0.5 for label in labels)

    label_stats = [("Person", person_count), ("Missing PPE", no_ppe_count)]
    
    for i, (label_text, label_count) in enumerate(label_stats):
        cv2.putText(frame, f"{label_text}: {label_count}", (20, 40 + i * 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
    return buffer.tobytes()

def gen_frames():
    global cap
    prev_time = time.time()

    while True:
        cap = get_video_capture()
        if cap is None:
            time.sleep(1)
            continue

        ret, frame = cap.read()
        if not ret:
            continue

        frame_bytes = gen_label(frame)
        current_time = time.time()
        elapsed_time = current_time - prev_time
        fps = 1.0 / elapsed_time if elapsed_time > 0 else 0
        prev_time = current_time
        print(f"FPS: {fps:.2f}")

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/shutdown', methods=['POST'])
def shutdown():
    try:
        subprocess.run(['bash', '/home/adhityaraar/Documents/shutdown.sh'])
        return jsonify({"message": "Shutting down. Please wait..."})
    except Exception as e:
        logging.exception("Failed to shut down")
        return jsonify({"error": str(e)})

def cleanup():
    global cap
    if cap is not None:
        cap.release()

if __name__ == '__main__':
    import warnings
    warnings.filterwarnings("ignore")
    atexit.register(cleanup)
    app.run(host='0.0.0.0', port=5000, debug=True)

