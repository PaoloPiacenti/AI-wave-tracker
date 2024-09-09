from ultralytics import YOLOv10
from params import *
import json

def inizialize_model(model_type = model_type):
    if model_type == 'Local':
        model_path = os.path.join('weights_model','weights_of_train_39','weights_best','best.pt')
        model = YOLOv10(model_path)
    return model


def detect_wave_pockets(frame, model, model_type=model_type):
    """
    Predict wave pockets on the current frame.
    Args:
        frame: The image frame as a numpy array.
    Returns:
        A list of predictions with bounding boxes and class names.
    """
    if model_type == 'Local':
        # Predict using local weights
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

def inizialize_cached_results(selected_video):
    frame_predictions = {}
    json_file = selected_video.replace('.mp4', '_3fps.json')  # Adjust this naming convention as needed
    json_path = os.path.join('surf_buddy','interface','cached_detections', json_file)
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            predictions_data = json.load(f)
            frame_offset = predictions_data.get('frame_offset')
            results = predictions_data.get('my-object-detection-co93y')
        # Create a mapping from frame_offset to prediction
        for pos, frame in enumerate(frame_offset):
            frame_predictions[frame] = results[pos]

        message = f"Loaded cached predictions from {json_file}"
        error = False

    else:
        message = f"Prediction JSON file not found for {selected_video}."
        error = True

    return error, frame_predictions, message
