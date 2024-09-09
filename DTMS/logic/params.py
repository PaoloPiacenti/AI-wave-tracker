import os

################################################################################
#                            GENERAL SETTINGS                                  #
################################################################################


# List of the beaches covered
beaches = {
    "Carcavelos": "carcavelos",
    "Praia Grande":"praiagrande",
    "Ribeira D'Ilhas":"bcmafraribeira",
}

'''
DEPRECATED >> the mode now is selected at front-end

# Define what is shown on the website. Possible values:
# >> stream: just display the streaming from MeoBeach Cam
# >> detection: display the streaming with Bounding Boxes
# >> tracking: Bounding Boxes with unique ids and Surf Quality Metrics
mode = 'detection'
'''

# Set the model used for the detection:
# >> Roboflow: Yolo v10 through Roboflow API
# >> Cache: To use only cached results (for dev only)
# >> Local: Local Yolo v10
model_type = 'Local'

#Frame per second:
fps = 3

################################################################################
#                          DEEP SORT TRACKER                                   #
################################################################################

max_age = 30 # Tracks will be kept alive for up to max_age frames without a detection before being removed. Suggested:30
n_init = 3 # A track will only be confirmed after n_init consecutive detections. Suggested: 3
max_iou_distance = 0.5 # Detections will be matched to tracks if their bounding boxes have an IoU of at least. Suggested: 0.7


################################################################################
#                                  SQM API                                     #
################################################################################


snapshot_duration = 900  # Duration of each snapshot in seconds
wait_duration = 10      # Duration of wait time between snapshots


credentials = os.environ.get("GOOGLE_CREDENTIALS")


mapping_wind_stations = {
    "carcavelos": 6215360,
    "praiagrande": 1210750,
    "costacaparicacds": 1210773,
    "bcmafraribeira": 1210746,
    "praiaguinchosul": 1210750,
    "bccostasaojoao": 1210773,
    "costacaparicasaojoao": 1210773,
}
