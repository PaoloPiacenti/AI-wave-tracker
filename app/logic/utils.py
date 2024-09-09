import os

# Function to delete all videos in the video directory
def delete_all_videos(video_dir):
    video_files = [f for f in os.listdir(video_dir) if f.endswith(".mp4")]
    if video_files:
        for video in video_files:
            file_path = os.path.join(video_dir, video)
            try:
                os.remove(file_path)
                message = f"Deleted: {video}"
            except Exception as e:
                message = f"Error deleting {video}: {e}"
    else:
        message = "No videos to delete."

    return message
