"""
Keeping track of waves detected in the video
"""

class Wave:
    __slots__ = ('wave_id', 'start_time', 'end_time', 'num_detections', 'bbox_hight_sum','bbox_width_sum')

    def __init__(self, wave_id, start_time, bbox_hight,bbox_width ):
        self.wave_id = wave_id
        self.start_time = start_time  # Time when the wave was first detected
        self.end_time = start_time    # Time when the wave was last detected
        self.num_detections = 1       # Number of detections associated with this wave
        self.bbox_hight_sum = bbox_hight  # Sum of bounding box hight to calculate the average
        self.bbox_width_sum = bbox_width  # Sum of bounding box width to calculate the average

    def update(self, current_time, bbox_hight,bbox_width):
        self.end_time = current_time
        self.num_detections += 1
        self.bbox_hight_sum += bbox_hight
        self.bbox_width_sum += bbox_width
