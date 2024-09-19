################################################################################
#                            YOLO V10 - Detector                               #
################################################################################

"""
Params to fine tune the YOLO V10 Model to detect 'Wave Pockets' in each
video frame.
"""

fps = 25 # Number of prediction per second. In relation to the FPS of the video, it determine the percentage of frame that will be predicted.
confidence_threshold = 0.35 # Detection of Wave Pockets with a confidence lower then the threshold are discarted.


################################################################################
#                            DEEP SORT - Tracker                               #
################################################################################

"""
Params to configure the Deep SORT Model track 'Waves' in a video starting
from the 'Waves Pockets' detections in each frame.
"""

max_age = 5 # Tracks will be kept alive for up to max_age frames without a detection before being removed. Suggested:30
n_init = 5 # A track will only be confirmed after n_init consecutive detections. Suggested: 3
max_iou_distance = 0.4 # Detections will be matched to tracks if their bounding boxes have an IoU of at least. Suggested: 0.7


################################################################################
#                         ENVIRONMENTAL VARIABLES                              #
################################################################################

import os

MODEL_PATH = os.environ.get("MODEL_PATH")
