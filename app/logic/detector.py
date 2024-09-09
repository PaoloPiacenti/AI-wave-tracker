from ultralytics import YOLOv10
from app.params import *


def inizialize_model(model_type = model_type):
    model = YOLOv10('model/weights_best_&_last_pt/best.pt')
    return model


def detect_wave_pockets(frame, model, model_type=model_type):
    """
    Predict wave pockets on the current frame.
    Args:
        frame: The image frame as a numpy array.
    Returns:
        A list of predictions with bounding boxes and class names.
    """
    if model_type == 'Yolo v10':
        # Predict using Yolo v10 weights
        result = model(frame)

        lst= []
        # Create a json out of results
        for n in range(len(result[0].summary())):
            x,y,w,h = [float(i) for i in result[0].boxes.xywh[n]]
            conf = float(result[0].boxes.conf[n])
            class_id = list(result[0].names.keys())[0]
            class_name = result[0].names[0]
            lst.append({'x':x,
                         'y':y,
                         'width':w,
                         'height':h,
                         'confidence':conf,
                         'class':class_name,
                         'class_id':class_id})
        prediction = {'predictions':lst}

    else:
        prediction = 0

    return prediction
