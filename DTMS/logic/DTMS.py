# Library Imports
import cv2
import time
from datetime import datetime
from google.cloud import bigquery
import pandas as pd

# Local Imports
import params as pr
from wind_request_func import get_wind_info
from wave_request_func import WaveForecast
from visualizations import draw_predictions
import detector as dt
import tracker as tr

def logic(spot_name):
    video_source = f'https://video-auth1.iol.pt/beachcam/{spot_name}/playlist.m3u8'
    cap = cv2.VideoCapture(video_source)


    model = dt.inizialize_model()
    tracker = tr.initialize_tracker()
    mapping_wind_stations = pr.mapping_wind_stations

    if not cap.isOpened():
        raise RuntimeError(f"Could not open video source: {spot_name}")

    # Calculate the interval between frames to predict


    original_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(original_fps / pr.fps)
    frame_count = 0


    # Snapshot and wait durations (in seconds)
    snapshot_duration = pr.snapshot_duration  # Duration of each snapshot in seconds
    wait_duration = pr.wait_duration      # Duration of wait time between snapshots

    # Initialize timing variables
    snapshot_mode = True  # Start in snapshot mode
    current_frame_count = pr.current_frame_count
    snapshot_frame_count = pr.snapshot_frame_count
    previous_average_wave_length = pr.previous_average_wave_length
    previous_max_wave_length = pr.previous_max_wave_length
    previous_num_waves = pr.previous_num_waves

    # Track data initialization
    current_snapshot_track_ids = set()
    track_start_times = pr.track_start_times
    track_end_times = pr.track_end_times


    # Snapshot and wait durations in terms of frames
    snapshot_duration_frames = snapshot_duration * pr.fps  # 10 seconds * fps
    wait_duration_frames = wait_duration * pr.fps  # 10 seconds * fps

    # While loop to continuously grab, process, and display frames
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        current_time = time.time()
        if snapshot_frame_count == 0:
            snaptime = datetime.now()
        current_frame_count += 1
        snapshot_frame_count += 1
        # Skip frames if not within the prediction interval
        if frame_count % frame_interval == 0:
                predictions = dt.detect_wave_pockets(frame, model)
                detections = draw_predictions(frame, predictions)[1]
                tracks = tr.update_tracker(tracker, frame, detections)[1]

                # Update tracking data
                for track in tracks:
                    track_id = track.track_id
                    if track_id not in track_start_times:
                        track_start_times[track_id] = current_time  # Start tracking time for new object

                    track_end_times[track_id] = current_time  # Update end time for all objects

                    # Add current track ID to the snapshot set
                    current_snapshot_track_ids.add(track_id)

                # Calculate durations for all tracked objects
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
                    wave_forecast = WaveForecast()
                    wave_pred = wave_forecast.run()
                    snapshot_data = [{
                        'Beach_Code':f'{spot_name}',
                        'Start_Date':snaptime.strftime(f"%Y-%m-%d %H:%M:%S"),
                        'Finish_Date': datetime.now().strftime(f"%Y-%m-%d %H:%M:%S"),
                        'N_of_Waves': num_waves_in_snapshot,
                        'Avg_Wave_Len_in_seconds': float(round(average_wave_time, 2)),
                        'Max_Wave_Len_in_seconds': float(round(max_tracking_duration, 2)),
                        'Wind_Speed_in_knots': get_wind_info(mapping_wind_stations[f'{spot_name}'])[0],
                        'Wind_Dir_in_str':get_wind_info(mapping_wind_stations[f'{spot_name}'])[1],
                        'Peak_Dist_Min_in_seconds':wave_pred['wavePeriodMin'],
                        'Peak_Dist_Max_in_seconds':wave_pred['wavePeriodMax'],
                        'Heigth_Swell_Min_in_meters':wave_pred['waveHighMin'],
                        'Heigth_Swell_Max_in_meters':wave_pred['waveHighMax'],
                        'Height_Waves_Min_in_meters':wave_pred['totalSeaMin'],
                        'Height_Waves_Max_in_meters':wave_pred['totalSeaMax'],
                        'Wave_Wind_Dir':wave_pred['predWaveDir']
                    }]

                    # Convert the accumulated snapshot data to a DataFrame if needed
                    #summary_df = pd.DataFrame(snapshot_data,columns=list(snapshot_data.keys()),index=range(1))
                    #summary_df.to_csv(f'SQM_CSV/SQM_row_{frame_count}.csv',index=False)
                    #print (snapshot_data)
                    try:
                        client = bigquery.Client()
                        table_id = "lewagon-data-428814.SQM_Dataset.SQM"
                        errors = client.insert_rows_json(table_id,snapshot_data)
                        if errors == []:
                            print('New rows have been added')
                        else:
                            print('Encountered errors while inserting rows onto table')
                            print(errors)
                    except:
                        print('Not able to connect to BQ')




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

        frame_count += 1

    # Release resources
    cap.release()
