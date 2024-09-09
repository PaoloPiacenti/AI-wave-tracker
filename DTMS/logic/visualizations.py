import cv2

def draw_predictions(frame, predictions):
    """
    Draw bounding boxes on the frame based on predictions.
    Args:
        frame: The original image frame as a numpy array.
        predictions: The prediction results from YOLO v10 model.
    Returns:
        Annotated image frame and a list of detections in the format expected by Deep SORT.
    """
    detections = []
    for obj in predictions['predictions']:
        # YOLO predictions are center x, y, and width/height; convert to corner coordinates
        x0 = int(obj['x'] - obj['width'] / 2)
        y0 = int(obj['y'] - obj['height'] / 2)
        width = int(obj['width'])
        height = int(obj['height'])
        confidence_score = obj['confidence']


        # Deep SORT expects the detection format: [x0, y0, width, height, confidence]
        detections.append(([x0, y0, width, height], confidence_score))

        # Draw rectangle
        x1 = x0 + width
        y1 = y0 + height
        class_name = obj['class']
        cv2.rectangle(frame, (x0, y0), (x1, y1), (0, 255, 0), 2)
        # Draw label
        cv2.putText(frame, f"{class_name} ({confidence_score:.2f})", (x0, y0 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame, detections
