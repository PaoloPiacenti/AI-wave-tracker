import cv2
from deep_sort_realtime.deepsort_tracker import DeepSort

from DemoSite.params import *

tracker = DeepSort(max_age=max_age, n_init=n_init, max_iou_distance=max_iou_distance)

def initialize_tracker():
    """
    Initializes the DeepSort tracker.
    """
    return tracker

def update_tracker(tracker, frame, detections):
    """
    Update the tracker with new detections and return the updated frame.
    Args:
        tracker: The DeepSort tracker object.
        frame: The current image frame (as a numpy array).
        detections: List of detections in the format [x0, y0, width, height, confidence].
    Returns:
        updated_frame: The frame with tracking information drawn on it.
        tracks: A list of track objects from DeepSort.
    """
    tracks = tracker.update_tracks(detections, frame=frame)

    # Draw tracking information on the frame
    for track in tracks:
        if not track.is_confirmed():
            continue
        track_id = track.track_id
        ltrb = track.to_ltrb()
        x0, y0, x1, y1 = map(int, ltrb)
        track_time = track.time_since_update

        # Draw tracking box
        cv2.rectangle(frame, (x0, y0), (x1, y1), (255, 0, 0), 2)
        # Draw tracking ID and duration
        cv2.putText(frame, f"ID: {track_id} Time: {track_time}", (x0, y1 + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    return frame, tracks
