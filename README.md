# AI-wave-tracker

AI-wave-tracker is an advanced AI-powered system utilizing YOLOv10 and Deep Sort for real-time detection and tracking of surfable waves. It analyzes video or webcam streams to assess wave quality, helping surfers catch the best conditions. The project is optimized for efficiency and precision, offering reliable wave dynamics tracking for surf enthusiasts and researchers alike.

## Features

- Real-time detection of surfable waves using YOLOv10
- Tracking of wave movements and quality with Deep Sort
- Support for video or live webcam streams
- Optimized for precision and resource efficiency
- Calculation of Surf Quality Metrics

## Structure

### DTMS (package)
DTMS (Detect Track Mark and Send) is a module aimed to get in input a video and return the same video with Bonding Boxes
plus a JSON with Surf Quality Metrics, like the number of waves, the average and maximum lenght in seconds.

### CamAnalyzer (service)
The CamAnalyzer is a module that use the DTMS package to analyze realtime video coming from Meo BeachCam webcams.
It provides API to access the RealTime Marked VideoStream and the Metrics

### DemoSite (client)
The DemoSite is a simple application that allow to test visually the DTMS and the CamAnalyzer functioning.
