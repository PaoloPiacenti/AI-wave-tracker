"""
Keep the history (max 1h) of the detections.
Tracking the waves and calculate surf quality metrics.
"""
import numpy as np
import cv2
from deep_sort_realtime.deepsort_tracker import DeepSort
from params import *

# Add a global dictionary to store tracking data
tracking_data = {}

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


def update_tracker_bbs_sqm(tracker, frame, bbs, current_frame_number, fps, show_bb=True):
    """
    Updates the tracker with bounding boxes and displays tracked objects on the frame.

    Args:
        tracker: Deep SORT tracker object.
        frame: Current video frame.
        bbs: List of bounding boxes and detection info in the format [(left, top, width, height), confidence, detection_class].
        current_frame_number: The index of the current frame.
        fps: Frames per second of the video.
        show_bb (bool): Whether to draw bounding boxes on the frame.

    Returns:
        frame: Frame with drawn tracking boxes.
        tracks: List of track objects from Deep SORT.
    """
    global tracking_data

    # Pass the list of formatted detections to Deep SORT
    tracks = tracker.update_tracks(bbs, frame=frame)

    # Visualize the tracking results and collect tracking data
    for track in tracks:
        if not track.is_confirmed():
            continue

        track_id = track.track_id
        ltrb = track.to_ltrb()
        left, top, right, bottom = map(int, ltrb)
        bbox_hight = bottom - top
        bbox_width = right - left
        current_time = current_frame_number / fps  # Calculate current time in seconds

        # Update tracking data
        if track_id not in tracking_data:
            # Initialize data for new track
            tracking_data[track_id] = {
                'wave_id': track_id,
                'start_time': current_time,
                'end_time': current_time,
                'num_detections': 1,
                'bbox_hight': [bbox_hight],
                'bbox_width': [bbox_width]
            }
        else:
            # Update existing track data
            tracking_data[track_id]['end_time'] = current_time
            tracking_data[track_id]['num_detections'] += 1
            tracking_data[track_id]['bbox_hight'].append(bbox_hight)
            tracking_data[track_id]['bbox_width'].append(bbox_width)

        if show_bb:
            # Draw tracking box on the frame
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

            # Display the track ID on the frame
            label = f"Wave: {track_id}"
            cv2.putText(frame, label, (left, bottom + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Return the updated frame and the tracks
    return frame, tracks
