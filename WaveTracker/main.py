import sys
import cv2

import detector as dt
import tracker as tr
import inout as io

from params import *


def WaveTracker():
    """
    Module's main function.
    It orchestrate all the logic for the WaveTracker.

    1. Upload the video
    2. Detect wave pockets
    3. Track waves
    4. Calculate Surf Quality Metrics
    5. Save the results in the output folder.

    """

    # Inizialize models
    model = dt.inizialize_model(MODEL_PATH)
    tracker = tr.initialize_tracker(max_age=max_age,n_init=n_init,max_iou_distance=max_iou_distance)

    # Upload video
    video_name = sys.argv[1]
    video_source = io.upload_video(video_name)
    cap = cv2.VideoCapture(video_source)

    if not cap.isOpened():
        print(f"Error: Unable to open video {video_name}")
        return

    # Calculate the interval between frames to predict
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(original_fps / fps)

    # Get frame size for output video
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (frame_width, frame_height)

    # Initialize the output folder and video writer
    output_folder = "WaveTracker/output"
    io.initialize_video_writer(output_folder,video_name,frame_size, original_fps)

    frame_count = 0

    # While loop to continuously grab, process, and display frames
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Predict only on the frames on the specified interval
        if frame_count % frame_interval == 0:
            bbs,frame = dt.detect_wave_pockets_bbs(frame,model,show_bb=True)


        # Update tracks only on not empty predictions
        if len(bbs) > 0:
            frame, tracks = tr.update_tracker_bbs(tracker, frame, bbs,show_bb=True)

        # Save the processed frame to the video
        print("Analyzing the video...")
        io.save_frame_with_bbs(frame)

        # Show the frame with bounding boxes in a window
        cv2.imshow('WaveTracker - Bounding Boxes', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1

    # Release video capture and writer resources
    cap.release()
    io.finalize_video_writer(output_folder)

    # If you're using OpenCV to visualize the video while processing, make sure to close windows
    cv2.destroyAllWindows()


if __name__ == '__main__':
    WaveTracker()
