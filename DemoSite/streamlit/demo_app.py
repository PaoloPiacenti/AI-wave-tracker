import os
import cv2
import time
import pandas as pd
import streamlit as st
import tempfile

from DemoSite.params import *

from DemoSite.logic.visualizations import draw_predictions
import DemoSite.logic.detector as dt
import DemoSite.logic.tracker as tr


################################################################################
#                           Variables  Inizialization                          #
################################################################################

st.session_state['video_dir'] = "surf_buddy/logic/videos"
video_dir = st.session_state['video_dir']
if not os.path.exists(video_dir):
    os.makedirs(video_dir)

if 'mode' not in st.session_state:
    st.session_state['mode'] = mode
st_mode = st.session_state['mode']

if 'model_type' not in st.session_state:
    st.session_state['model_type'] = model_type
st_model_type = st.session_state['model_type']

if 'fps' not in st.session_state:
    st.session_state['fps'] = fps
st_fps = st.session_state['fps']

if 'max_age' not in st.session_state:
    st.session_state['max_age'] = max_age
sort_max_age = st.session_state['max_age']

if 'n_init' not in st.session_state:
    st.session_state['n_init'] = n_init
sort_n_init = st.session_state['n_init']

if 'max_iou_distance' not in st.session_state:
    st.session_state['max_iou_distance'] = max_iou_distance
sort_max_iou_distance = st.session_state['max_iou_distance']

if 'snapshot_duration' not in st.session_state:
    st.session_state['snapshot_duration'] = 10
sqm_snapshot_duration = st.session_state['snapshot_duration']

if 'wait_duration' not in st.session_state:
    st.session_state['wait_duration'] = 10
sqm_wait_duration = st.session_state['wait_duration']

if 'beaches' not in st.session_state:
    st.session_state['beaches'] = beaches
beaches = st.session_state['beaches']

# Initialize model
if mode != "Streaming" and model_type != "Cache":
    model = dt.inizialize_model()

# Initialize tracker
if mode == 'Tracking':
    tracker = tr.initialize_tracker()

################################################################################
################################################################################
##                             Streamlit App                                  ##
################################################################################
################################################################################
# Imposta la larghezza della pagina per un layout più ampio
st.set_page_config(layout="wide")

st.title("Surf Buddy - AI Demo")

multi = '''The scope of this demo website is to showcase the functioning of the Wave Pocket Tracker on LiveStream Cam.
It is **not** the *Business Website*!!
'''
st.markdown(multi)

################################################################################
#                                 Select Source                                #
################################################################################

source_type = st.selectbox("Select Source", ["Video", "Livestream"])


if source_type == 'Video':

    video_file = st.file_uploader("Upload a video file", type=["mp4"])
    if video_file is not None:
        # If the user has uploaded a video file
        if video_file is not None:
            # Use a temporary file to handle the video without saving it permanently
            tfile = tempfile.NamedTemporaryFile(delete=False)  # Create a temporary file
            tfile.write(video_file.read())  # Write the video content into the temporary file
            video_source = tfile.name

    else:
        st.warning("Please upload a video file to proceed.")
        st.stop()

else:
    beach_choice = st.selectbox("Choose a Beach", list(beaches.keys()))
    selected_beach_url_part = beaches[beach_choice]
    video_source = f'https://video-auth1.iol.pt/beachcam/{selected_beach_url_part}/playlist.m3u8'

################################################################################
#                                 Visualization                                #
################################################################################

# OpenCV video capture object
cap = cv2.VideoCapture(video_source)

st.subheader(f"{source_type} - {st_mode}")
frame_placeholder = st.empty()


# Stream video frames in real-time
st.subheader("Surf Quality Metrics")

sqm_snapshot_explanation = f'In the following table are shown surfable waves statistics collected in time frames of {sqm_snapshot_duration} seconds'

st.markdown(sqm_snapshot_explanation)
tracking_info_placeholder = st.empty() if mode == 'Tracking' else None

################################################################################
#                               Setting Check                                  #
################################################################################

st.subheader("Current settings")
# Create a dictionary to hold the parameter names and their values
params = {
    "mode": st.session_state['mode'],
    "model_type": st.session_state['model_type'],
    "fps": st.session_state['fps'],
    "max_age": st.session_state['max_age'],
    "n_init": st.session_state['n_init'],
    "max_iou_distance": st.session_state['max_iou_distance'],
    "snapshot_duration": st.session_state['snapshot_duration'],
    "wait_duration": st.session_state['wait_duration']
}

# Convert the dictionary into a DataFrame for display
df = pd.DataFrame(list(params.items()), columns=['Parameter', 'Value'])

# Display the table in Streamlit
st.table(df)

################################################################################
#                       Video Processing Inizialization                        #
################################################################################

# Initialize timing variables
snapshot_start_time = time.time()
snapshot_mode = True  # Start in snapshot mode
current_frame_count = 0
snapshot_frame_count = 0
previous_average_wave_length = None
previous_max_wave_length = None
previous_num_waves = None

# Track data initialization
snapshot_data = []
current_snapshot_track_ids = set()
track_start_times = {}
track_end_times = {}

# Calculate the interval between frames to predict
original_fps = cap.get(cv2.CAP_PROP_FPS)
frame_interval = int(original_fps / fps)
frame_count = 0

# Snapshot and wait durations in terms of frames
snapshot_duration_frames = fps * sqm_snapshot_duration
wait_duration_frames = fps * sqm_wait_duration

################################################################################
#                             Video Processing Loop                            #
################################################################################

# While loop to continuously grab, process, and display frames
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        st.write("Failed to grab frame. Retrying...")
        continue

    current_time = time.time()
    current_frame_count += 1
    snapshot_frame_count += 1

    if st_mode != "Streaming":


        # Skip frames if not within the prediction interval
        if frame_count % frame_interval == 0:
            # Predict objects in the frame
            predictions = dt.detect_wave_pockets(frame, model)

        if mode == "Tracking":

            # Draw predictions on the frame
            frame, detections = draw_predictions(frame, predictions)

            # Perform tracking with Deep SORT
            frame, tracks = tr.update_tracker(tracker, frame, detections)

            # Update tracking data
            for track in tracks:
                track_id = track.track_id
                if track_id not in track_start_times:
                    track_start_times[track_id] = current_time  # Start tracking time for new object

                track_end_times[track_id] = current_time  # Update end time for all objects

                # Add current track ID to the snapshot set
                current_snapshot_track_ids.add(track_id)

            # Calculate durations for all tracked objects
            tracking_data = []
            total_tracking_duration = 0  # Reset total duration for this iteration
            max_tracking_duration = 0  # Initialize max duration

            for track_id in current_snapshot_track_ids:
                start_time = track_start_times[track_id]
                end_time = track_end_times.get(track_id, current_time)  # Use current time for active objects
                tracking_duration = end_time - start_time
                total_tracking_duration += tracking_duration  # Accumulate total duration

                # Update max tracking duration
                if tracking_duration > max_tracking_duration:
                    max_tracking_duration = tracking_duration

            # Calculate number of tracked objects (waves) in the current snapshot
            num_waves_in_snapshot = len(current_snapshot_track_ids)

            # Calculate average wave time in the current snapshot
            average_wave_time = total_tracking_duration / num_waves_in_snapshot if num_waves_in_snapshot > 0 else 0


            if snapshot_mode and snapshot_frame_count >= snapshot_duration_frames:
                # Prepare summary data for the DataFrame
                snapshot_data.append({
                    'Number of Waves': num_waves_in_snapshot,
                    'Average Wave Length (s)': round(average_wave_time, 2),
                    'Max Wave Length (s)': round(max_tracking_duration, 2)
                })
                snapshot_mode = False  # Switch to wait mode
                snapshot_frame_count = 0  # Reset frame counter for waiting period

                # Update previous values
                previous_average_wave_length = average_wave_time
                previous_max_wave_length = max_tracking_duration
                previous_num_waves = num_waves_in_snapshot

                # Clear the current snapshot tracking data
                current_snapshot_track_ids.clear()
                track_start_times.clear()
                track_end_times.clear()

            elif not snapshot_mode and snapshot_frame_count >= wait_duration_frames:
                snapshot_mode = True  # Switch back to snapshot mode
                snapshot_frame_count = 0  # Reset frame counter for new snapshot period

            # Convert the accumulated snapshot data to a DataFrame
            summary_df = pd.DataFrame(snapshot_data)

            # Display the summary DataFrame in Streamlit
            tracking_info_placeholder.dataframe(summary_df)
            print (tracking_info_placeholder)

        else:
            # Draw predictions on the frame
            frame = draw_predictions(frame, predictions)[0]

    # Convert the frame to RGB (OpenCV uses BGR by default)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Display the frame in the Streamlit app
    frame_placeholder.image(frame_rgb)

    frame_count += 1

# Release the capture object
cap.release()
