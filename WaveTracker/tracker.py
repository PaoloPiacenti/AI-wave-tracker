"""
Keep the history (max 1h) of the detections.
Tracking the waves and calculate surf quality metrics.
"""

import cv2
from deep_sort_realtime.deepsort_tracker import DeepSort
from params import *


def initialize_tracker(max_age=35,n_init=3,nn_budget=None,max_iou_distance=0.7,embedder="mobilenet"):
    """
    Initializes the DeepSort tracker.
    Returns:
        tracker: An initialized DeepSort tracker object.
    """
    # Initialize Deep SORT tracker
    deep_sort = DeepSort(
        max_age=max_age,
        n_init=n_init,
        nn_budget=nn_budget,
        max_iou_distance=max_iou_distance,
        embedder=embedder
    )
    return deep_sort



def update_tracker_bbs(tracker, frame, bbs, show_bb=True):
    """
    Updates the tracker with bounding boxes and displays tracked objects on the frame.

    Tracker bbs example:
    [
        [(545, 927, 110, 89), 0.8788439631462097, 'pocket'],
        [(45, 951, 90, 88), 0.3620339632034302, 'pocket']
    ]


    Args:
        tracker: Deep SORT tracker object.
        frame: Current video frame.
        bbs: List of bounding boxes and detection info in the format [(left, top, width, height), confidence, detection_class].
        frame_width: Width of the video frame.
        frame_height: Height of the video frame.

    Returns:
        frame: Frame with drawn tracking boxes.
        tracks: List of track objects from Deep SORT.
    """

    # Pass the list of formatted detections to Deep SORT
    tracks = tracker.update_tracks(bbs, frame=frame)

    # Visualize the tracking results
    if show_bb:
        for track in tracks:
            if not track.is_confirmed():
                continue

            track_id = track.track_id
            #track_time = track.time_since_update

            ltrb = track.to_ltrb()

            # Extract bounding box coordinates
            left, top, right, bottom = map(int, ltrb)

            # Draw tracking box on the frame
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

            # Optionally, display the track ID on the frame
            track_id = track.track_id
            label = f"Wave: {track_id}"
            cv2.putText(frame, label, (left, bottom + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Return the updated frame and the tracks
    return frame, tracks
