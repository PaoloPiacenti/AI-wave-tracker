import os

################################################################################
#                            GENERAL SETTINGS                                  #
################################################################################


# List of the beaches covered
beaches = {
    "Praia Grande":"praiagrande",
    "Ribeira D'Ilhas":"bcmafraribeira",
    "Caparica CDS":"costacaparicacds",
    "Caparica Norte":"bccostasaojoao",
    "Caparica Sao Joao":"costacaparicasaojoao",
    "Carcavelos": "carcavelos",
    "Guincho":"praiaguinchosul"
}

MODEL_PATH = os.environ.get("MODEL_PATH")
# Default mode:
# >> Streaming: just display the streaming from MeoBeach Cam
# >> Detection: display the streaming with Bounding Boxes
# >> Tracking: Bounding Boxes with unique ids and Surf Quality Metrics
mode = 'Tracking'

# Set the model used for the detection:
model_type = 'Yolo v10'

#Frame per second:
fps = 3


################################################################################
#                          DEEP SORT TRACKER                                   #
################################################################################

max_age = 15 # Tracks will be kept alive for up to max_age frames without a detection before being removed. Suggested:30
n_init = 5 # A track will only be confirmed after n_init consecutive detections. Suggested: 3
max_iou_distance = 0.4 # Detections will be matched to tracks if their bounding boxes have an IoU of at least. Suggested: 0.7
