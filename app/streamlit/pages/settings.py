"""
In this page we controll all the AI Model Settings
"""

import streamlit as st
from app.logic import utils as ut
from app.params import *
import os

# Define a function for the settings page
def settings_page():
    st.title("Wave Pocket Tracker Settings")

    # Mode selection
    st.subheader("Select Demo Mode:")
    st.session_state['mode'] = st.selectbox("Select demo mode", ["Tracking", "Detection", "Streaming"])

    # Conditionally display Detection option only if mode is not "Streaming"
    if st.session_state['mode'] != "Streaming":

        # Model type selection
        st.subheader("Detection settings")
        st.session_state['fps'] = st.slider("Predictions per second", 1, 60, st.session_state.get('fps'))

        if st.session_state['mode'] == "Tracking":

            # Deep SORT tracker settings
            st.subheader("Deep SORT Tracker Settings")
            st.session_state['max_age'] = st.slider("Max Age", 1, 100, st.session_state.get('max_age', 15))
            st.session_state['n_init'] = st.slider("Number of Consecutive Detections (n_init)", 1, 10, st.session_state.get('n_init', 5))
            st.session_state['max_iou_distance'] = st.slider("Max IoU Distance", 0.0, 1.0, st.session_state.get('max_iou_distance', 0.7))

            # Surf Quality Metrics Snapshot
            st.subheader("Surf Quality Metrics Snapshots Settings")
            st.session_state['snapshot_duration'] = st.slider("Snapshot Duration [s]", 1, 100, st.session_state.get('snapshot_duration', 10)) # Duration of each snapshot in seconds
            st.session_state['wait_duration'] = st.slider("Wait Duration [s]", 1, 100, st.session_state.get('wait_duration', 10)) # Duration of wait time between snapshots

    # Beaches management
    st.subheader("Surf Webcams Mapped")

    # Initialize beaches dictionary in session state if not already present
    if 'beaches' not in st.session_state:
        st.session_state['beaches'] = beaches

    # Display the current list of beaches
    for beach, url_part in st.session_state['beaches'].items():
        st.write(f"{beach}: {url_part}")

    # Inputs for adding a new beach
    new_beach_name = st.text_input("New Webcam Name")
    new_beach_url = st.text_input("New Webcam URL Part")

    # Button to add a new beach
    if st.button("Map a New Webcam"):
        if new_beach_name and new_beach_url:
            # Add new beach to the session state beaches dictionary
            st.session_state['beaches'][new_beach_name] = new_beach_url
            st.success(f"Added webcam: {new_beach_name}")
        else:
            st.error("Please provide both a beach name and a URL part.")

# Use the settings page function
settings_page()


# Add a button to delete all videos in the folder
st.subheader("Delete saved videos")
st.session_state['video_dir'] = "surf_buddy/logic/videos"
video_dir = st.session_state['video_dir']
if st.button("Delete All Videos"):
    message = ut.delete_all_videos(video_dir)
    st.write(message)


# Add a button to reset all settings
st.subheader("Reset all configurations to default values")
if st.button("Reset configuration"):
    st.session_state['mode'] = 'Tracking'
    st.session_state['model_type'] = 'Yolo v10'
    st.session_state['fps'] = 5
    st.session_state['ROBOFLOW_API_KEY'] = 'yoS00JzuqGDiVdzefUJC'
    st.session_state['ROBOFLOW_PROJECT_ID'] = 'my-object-detection-co93y'
    st.session_state['ROBOFLOW_MODEL_VERSION'] = '1'
    st.session_state['confidence'] = 20
    st.session_state['overlap'] = 30
    st.session_state['max_age'] = 15
    st.session_state['n_init'] = 5
    st.session_state['max_iou_distance'] = 0.7
    st.session_state['snapshot_duration'] = 10
    st.session_state['wait_duration'] = 10
    st.session_state['beaches'] = beaches
