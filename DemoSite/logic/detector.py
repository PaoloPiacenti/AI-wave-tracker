from ultralytics import YOLOv10
from DemoSite.params import *


def initialize_model():
    model = YOLOv10(MODEL_PATH)
    return model


def detect_wave_pockets(frame, model):
    """
    Predict wave pockets on the current frame.
    Args:
        frame: The image frame as a numpy array.
    Returns:
        A list of predictions with bounding boxes and class names.
    """

    result = model(frame)

    lst= []
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

    return prediction
