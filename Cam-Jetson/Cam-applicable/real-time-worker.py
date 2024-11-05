import time
import cv2
from ultralytics import YOLO

HOME = "/home/adhityaraar/Documents"
model = YOLO(f"{HOME}/models/yolo8n-v1.pt", 'cuda')

class_names = model.names

def main():
    try:
        cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 552) #1280
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 552) #720
        #cap.set(cv2.CAP_PROP_FPS, 10)

        if not cap.isOpened():
            print("Could not open webcam")
            exit()

        prev_time = 0

        while True:
            start_time = time.time()
            
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            pre_inference_time = time.time()
            result = model(frame, agnostic_nms=True)[0]
            post_inference_time = time.time()
            
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

            # Calculating FPS
            current_time = time.time()
            fps = 1 / (current_time - prev_time)
            prev_time = current_time

            cv2.imshow('Video Feed', frame)

            end_time = time.time()
            frame_time = end_time - start_time
            inference_time = post_inference_time - pre_inference_time

            print(f"Frame time: {frame_time:.2f} s, Inference time: {inference_time:.2f} s, FPS: {fps:.2f}")

            # Break the loop on pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

