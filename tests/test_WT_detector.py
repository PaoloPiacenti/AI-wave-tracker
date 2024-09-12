import pytest
from WaveTracker import detector as dt
#from DTMS_p import params as p

def test_model_init():
    model = dt.inizialize_model()
    #assert p.MODEL_PATH is not None, "MODEL_PATH is not set. Please provide a valid model path."
    assert type(model) == "<class 'ultralytics.models.yolov10.model.YOLOv10'>", 'Model ot intialized correctly. Provide a valid YOLO v10.'
