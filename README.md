# WaveTracker

## Introduction
**WaveTracker** is a Python-based tool designed to detect and track waves in surf webcam video frames. By utilizing advanced computer vision techniques, including the **YOLOv10** object detection model and the **Deep SORT** tracking algorithm, WaveTracker identifies "wave pockets" in video frames and tracks these detections over time. The result is a comprehensive JSON file containing data about the tracked waves and a video annotated with bounding boxes highlighting the detected wave pockets.

This tool can be integrated with smart cameras to monitor surf conditions in real-time, making it valuable for surfers, lifeguards, coastal management authorities, and surf-related businesses.

## Features
- **Wave Detection:** Uses YOLOv10 to detect wave pockets in video frames.
- **Wave Tracking:** Employs Deep SORT to track detected waves across frames.
- **Surf Quality Metrics:** Calculates metrics like average bounding box size and wave duration.
- **Output Generation:**
    - ***Annotated Video:*** Saves a video with bounding boxes drawn around detected wave pockets.
    - ***JSON Data:*** Outputs a JSON file containing detailed information about each tracked wave.

## Table of Contents
Requirements
Installation
Usage
  Preparing the Input Video
  Running WaveTracker
  Understanding the Output
Configuration
  Environment Variables
  Parameter Tuning
Project Structure
Example
License
Acknowledgments

## Requirements
Python 3.7 or higher
Operating System: Compatible with Windows, macOS, and Linux.

### Python Dependencies
Install the following Python packages:

- opencv-python (cv2)
- ultralytics
- deep_sort_realtime
- numpy

You can install the dependencies using the following command:

'''
pip install -r requirements.txt
'''
**Note:** Ensure that you have the YOLOv10 model file available at the specified MODEL_PATH.

## Installation
Clone the Repository:

'''
git clone https://github.com/PaoloPiacenti/AI-wave-tracker/.git
cd AI-wave-tracker
'''


## Usage

### Preparing the Input Video
- Place your input video file (e.g., '''surf_video.mp4''') in the '''Resources/input''' directory.
- Supported video formats include '''.mp4''', '''.avi''', and other formats compatible with OpenCV.

### Running WaveTracker
Use the provided '''Makefile''' or run the script directly.

**Using the Makefile**
'''make run_WaveTracker ARGS=surf_video.mp4'''

**Running the Script Directly**
'''python main.py surf_video.mp4'''

### Understanding the Output
- **Annotated Video:** An output video with bounding boxes drawn around detected wave pockets will be saved in the Resources/output directory as output_surf_video.mp4.
- **JSON Data:** A JSON file containing detailed information about each tracked wave will be saved in the Resources/output directory as wave_data_surf_video.mp4.json.

**Sample JSON Output**

'''
[
    {
        "wave_id": 1,
        "start_time": 0.0,
        "end_time": 5.2,
        "num_detections": 130,
        "avg_bbox_height": 85.3,
        "avg_bbox_width": 120.5
    },
    {
        "wave_id": 2,
        "start_time": 2.5,
        "end_time": 7.8,
        "num_detections": 140,
        "avg_bbox_height": 90.1,
        "avg_bbox_width": 115.7
    }
]
'''

## Configuration
You can fine-tune the detection and tracking parameters by modifying the params.py file.

### YOLOv10 Detector Parameters
- '''fps''': Number of predictions per second. Adjusts the frequency of frame predictions relative to the video FPS.
- '''confidence_threshold''': Detections with a confidence lower than this threshold are discarded.

### Deep SORT Tracker Parameters
- '''max_age''': Maximum number of frames to keep a track alive without detections before removing it.
- '''n_init''': Number of consecutive detections required to confirm a track.
- '''max_iou_distance''': Maximum IoU distance for matching detections to tracks.


## Project Structure
'''
WaveTracker/
├── Resources/
│   ├── input/         # Directory for input videos
│   └── output/        # Directory for output videos and JSON files
├── detector.py        # Wave pocket detection logic using YOLOv10
├── tracker.py         # Wave tracking logic using Deep SORT
├── inout.py           # Input/output handling functions
├── waves.py           # Wave data structure and logic
├── params.py          # Configuration parameters
├── main.py            # Main script orchestrating the workflow
├── Makefile           # Makefile for easy execution
├── requirements.txt   # Python dependencies
└── README.md          # This README file
'''

## Example

### 1. Run WaveTracker:

'''
python main.py carcavelos.mp4
'''

### 2. Check the Output:

Annotated video: '''Resources/output/output_carcavelos.mp4'''
JSON data: '''Resources/output/wave_data_carcavelos.json'''

### 3. Analyze the Results:
Use the JSON file to analyze wave durations, sizes, and frequencies to determine surf conditions.

## License
MIT License

## Acknowledgments
- Ultralytics YOLOv10: For the state-of-the-art object detection model.
- Deep SORT: For the robust multi-object tracking algorithm.
- OpenCV: For providing comprehensive computer vision tools.

## Contact
For questions or support, please contact **work.paolopiacenti@gmail.com**.
