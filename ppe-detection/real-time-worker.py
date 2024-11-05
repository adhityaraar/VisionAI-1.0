import cv2
import argparse

from ultralytics import YOLO
import numpy as np
import supervision as sv

ZONE_POLYGON = np.array([
    [0, 0],
    [0.5, 0],
    [0.5, 1],
    [0, 1]
])

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument(
        "--webcam-resolution", 
        default=[1280, 720], 
        nargs=2, 
        type=int
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    frame_width, frame_height = args.webcam_resolution

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    # model = YOLO("yolov8l.pt")
    import os
    HOME = os.getcwd()
    model = YOLO(f"{HOME}/models/best.pt")

    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    zone_polygon = (ZONE_POLYGON * np.array(args.webcam_resolution)).astype(int)
    zone = sv.PolygonZone(polygon=zone_polygon, frame_resolution_wh=tuple(args.webcam_resolution))
    zone_annotator = sv.PolygonZoneAnnotator(
        zone=zone, 
        color=sv.Color.red(),
        thickness=2,
        text_thickness=4,
        text_scale=2
    )

    while True:
        ret, frame = cap.read()

        result = model(frame, agnostic_nms=True)[0]
        detections = sv.Detections.from_yolov8(result)
        labels = [
            f"{model.model.names[class_id]} {confidence:0.2f}"
            for _, confidence, class_id, _
            in detections
        ]
        frame = box_annotator.annotate(
            scene=frame, 
            detections=detections, 
            labels=labels
        )

        if labels == []:
            person_count = 0
            missing_safety = 0

        else:
            names = []
            scores = []
            for item in labels:
                split_item = item.rsplit(' ', 1)
                name = split_item[0]
                score = float(split_item[1])  # Convert score to float
                names.append(name)
                scores.append(score)

            # Creating a DataFrame
            import pandas as pd
            df = pd.DataFrame({'name': names, 'score': scores})

            ### if person available, if not person_count = 0
            person_count = df[(df['name'] == 'Person') & (df['score'] > 0.5)].shape[0]
            missing_safety = df[(~df['name'].str.contains('Person')) & (df['name'].str.startswith('NO')) & (df['score'] > 0.5)].shape[0]

        # zone.trigger(detections=detections)
        # frame = zone_annotator.annotate(scene=frame)  
        
        cv2.putText(frame, f"Person: {person_count:.0f}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f"Missing PPE: {missing_safety:.0f}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("PPE Detection: yolov8 model", frame)

        ## Split arrary into table
        # print(result.xyxy[0].cpu().numpy())

        if (cv2.waitKey(30) == 27):
            break


if __name__ == "__main__":
    main()

    ### split 'NO-Safety Vest 0.92' into 'NO-Safety Vest' and '0.92', also 'Person 0.86' into 'Person' and '0.86'
    ### if 'Person' in labels > 0.5, then count the number of 'Person' in labels

