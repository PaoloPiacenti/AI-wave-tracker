from ultralytics import YOLOv10
from params import *
import cv2

def inizialize_model(model):
    """
    Inizialize the YOLO v10 Model
    """
    model = YOLOv10(model)
    return model


def detect_wave_pockets_bbs(frame, model,show_bb=False):
    """
    Analyze a frame and return a list of bounding box detections (bbs)
    for objects in the current video frame.

    Return a list of tuples suitable for Deep SORT tracking, where each tuple
    contains:

    -   [left, top, w, h]: The coordinates and size of the bounding box
        (where left, top are the top-left corner, and w, h are the width and
        height of the bounding box).

    -   confidence: The confidence score of the detection (e.g., how certain
        the detector is that this is a valid object).

    -   detection_class: The class or category of the detected object
        (e.g., "person", "car", etc.).

    """
    # Object Detection with YOLO
    results = model(frame)

    detections = []  # To store detections for each frame

    # YOLO's output is an instance of Results, which contains the detections
    for result in results:
        boxes = result.boxes  # Extract the boxes object
        class_names_dict = result.names # Extract the dictonary class_id --> class_name

        # Extract the individual attributes: coordinates, confidence, and class ID
        if boxes is not None:
            xyxy = boxes.xyxy  # Bounding boxes in [x1 (left), y1 (top), x2 (right), y2 (bottom)] format
            confidences = boxes.conf  # Confidence scores
            class_ids = boxes.cls  # Class IDs for detected objects
            class_names = [class_names_dict[int(i)] for i in class_ids] # Class names for detected objects

            # Loop over the detected boxes and filter by confidence
            for i in range(len(xyxy)):
                x1, y1, x2, y2 = map(int, xyxy[i].tolist())  # Convert coordinates to list of integers
                conf = confidences[i].item()  # Confidence score
                class_id = int(class_ids[i].item())  # Class ID as an integer
                class_name = class_names[i] # Class name

                if conf > confidence_threshold:  # Filter out low confidence detections
                    detections.append([x1, y1, x2, y2, conf,class_name])  # [x1, y1, x2, y2, confidence,class_name]

                    if show_bb:

                        # Draw the bounding box on the frame
                        # Top-left is (x_left, y_top), bottom-right is (x_right, y_bottom)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                        # Draw the label (class name and confidence)
                        label = f"{class_name} ({conf:.2f})"
                        label_position = (x1, y1 - 10)  # Position the label above the box
                        cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Convert detections to [x1, y1, width, height, confidence] format
    detections = [[(x1, y1, (x2 - x1), (y2 - y1)), conf, class_name] for x1, y1, x2, y2, conf,class_name in detections]


    return detections, frame


if __name__ == '__main__':
    model = inizialize_model()
    print(type(model))
