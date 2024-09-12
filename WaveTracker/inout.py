
import os
import sys
import shutil
import cv2

video_writer = None


def upload_video(video_name):
    """
    Upload a video from the video folder
    """

    video_folder = os.path.join("WaveTracker","videos")

    video_path = os.path.join(video_folder, video_name)

    # Check if the video folder exists
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)
        raise FileNotFoundError(f"The video folder '{video_folder}' does not exist. Creating video folder...")

    # Check if the video file exists
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"The video '{video_name}' does not exist in '{video_folder}'.")

    # Simulate the upload process
    print(f"Uploading video: {video_name} from folder: {video_folder}")

    # Return the video path
    return video_path


def initialize_video_writer(output_folder,video_name,frame_size, fps):
    """
    Initializes the VideoWriter and manages the output folder.

    Args:
        output_folder (str): Path to the output folder.
        frame_size (tuple): Size of the video frames (width, height).
        fps (float): Frames per second of the output video.

    Returns:
        VideoWriter object: The OpenCV VideoWriter object.
    """
    global video_writer

    # Delete the output folder if it exists and create a new one
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

    # Define the output video path and initialize VideoWriter
    output_video_path = os.path.join(output_folder, f'output_{video_name}')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size)
    print(f"VideoWriter initialized, saving video to {output_video_path}")


def save_frame_with_bbs(frame):
    """
    Saves a single frame with bounding boxes to the output video.

    Args:
        frame (ndarray): The frame to be saved.
    """
    global video_writer
    if video_writer is not None:
        video_writer.write(frame)


def finalize_video_writer(output_folder):
    """
    Finalizes and releases the VideoWriter object.
    """
    global video_writer
    if video_writer is not None:
        video_writer.release()
        video_writer = None
        print(f"VideoWriter finalized and video saved on {output_folder}")
