
# from flask import Flask
# from appwrite.client import Client
# from appwrite.services.storage import Storage
# from appwrite.input_file import InputFile
# import cv2
# import datetime
# from io import BytesIO

# app = Flask(__name__)


# APPWRITE_ENDPOINT = "https://cloud.appwrite.io/v1"  
# APPWRITE_PROJECT_ID = "67e25e080016d17344a1"    
# APPWRITE_API_KEY = "standard_826e779be35c9ef95f2ce051718c5dfb9a01c6557984b81c07c876042e7f09ac811bfa2642875db220bf7e4c5b299d685146c5e6bfe5e37eb174a7259129d13306e4baac6d46263fada0054d09472db21db500429230925b82c62606c8f3c5f9389fb95314d6574219713861a9dc5b03bb54a66cc1b8fbb348b7b3c7e4a04319"          
# STORAGE_BUCKET_ID = "image_id"     


# client = Client()
# client.set_endpoint(APPWRITE_ENDPOINT)      
# client.set_project(APPWRITE_PROJECT_ID)       
# client.set_key(APPWRITE_API_KEY)             
# storage = Storage(client)

# @app.route('/trigger', methods=['GET'])
# def trigger_webcam():
#     # Initialize camera
#     cap = cv2.VideoCapture(0)
#     ret, frame = cap.read()
#     if not ret:
#         cap.release()
#         return "Failed to capture image", 400

#     # Generate filename
#     filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
    
#     # Save locally (optional)
#     cv2.imwrite(filename, frame)
#     print(f"Captured {filename}")

#     # Upload to Appwrite Storage
#     try:
#         with open(filename, 'rb') as file:
#             file_data = file.read()
        
#         result = storage.create_file(
#             bucket_id=STORAGE_BUCKET_ID,
#             file_id='unique',  
#             file=InputFile.from_bytes(file_data, filename=filename)
#         )
#         cap.release()
#         return f"Image captured & uploaded to Appwrite! File ID: {result['$id']}", 200
#     except Exception as e:
#         cap.release()
#         return f"Appwrite upload failed: {str(e)}", 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)



# from flask import Flask
# from appwrite.client import Client
# from appwrite.services.storage import Storage
# from appwrite.input_file import InputFile
# from flask_cors import CORS
# import cv2
# import datetime
# import os

# app = Flask(__name__)
# CORS(app)

# # Appwrite configuration
# APPWRITE_ENDPOINT = "https://cloud.appwrite.io/v1"  
# APPWRITE_PROJECT_ID = "67e25e080016d17344a1"    
# APPWRITE_API_KEY = "standard_826e779be35c9ef95f2ce051718c5dfb9a01c6557984b81c07c876042e7f09ac811bfa2642875db220bf7e4c5b299d685146c5e6bfe5e37eb174a7259129d13306e4baac6d46263fada0054d09472db21db500429230925b82c62606c8f3c5f9389fb95314d6574219713861a9dc5b03bb54a66cc1b8fbb348b7b3c7e4a04319"          
# STORAGE_BUCKET_ID = "image_id"     

# client = Client()
# client.set_endpoint(APPWRITE_ENDPOINT)      
# client.set_project(APPWRITE_PROJECT_ID)       
# client.set_key(APPWRITE_API_KEY)             
# storage = Storage(client)

# @app.route('/record_video', methods=['GET'])
# def record_video():
#     # Video settings
#     VIDEO_DURATION = 7  # Seconds
#     FRAME_RATE = 30
#     VIDEO_WIDTH, VIDEO_HEIGHT = 640, 480

#     # Initialize camera
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         return "Failed to open camera", 500
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_WIDTH)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_HEIGHT)

#     # Generate filename
#     filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".mp4"
#     temp_path = f"temp_{filename}"
    
#     # Define video writer with H264 codec for better compatibility
#     fourcc = cv2.VideoWriter_fourcc(*'H264')  # Use H264 instead of mp4v
#     out = cv2.VideoWriter(temp_path, fourcc, FRAME_RATE, (VIDEO_WIDTH, VIDEO_HEIGHT))

#     if not out.isOpened():
#         cap.release()
#         return "Failed to initialize video writer", 500

#     # Record for VIDEO_DURATION seconds
#     start_time = datetime.datetime.now()
#     while (datetime.datetime.now() - start_time).seconds < VIDEO_DURATION:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         out.write(frame)
    
#     # Release resources
#     out.release()
#     cap.release()

#     # Verify file exists and is not empty
#     if not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
#         return "Failed to save video file", 500

#     # Upload to Appwrite Storage
#     try:
#         with open(temp_path, 'rb') as video_file:
#             result = storage.create_file(
#                 bucket_id=STORAGE_BUCKET_ID,
#                 file_id='unique()',  # Generate unique ID
#                 file=InputFile.from_bytes(video_file.read(), filename=filename, mime_type="video/mp4")
#             )
#         print(f"Uploaded file ID: {result['$id']}")  # Debug: Log file ID
#         os.remove(temp_path)
#         return f"Video uploaded to Appwrite! File ID: {result['$id']}", 200
#     except Exception as e:
#         if os.path.exists(temp_path):
#             os.remove(temp_path)
#         return f"Upload failed: {str(e)}", 500

# @app.route('/')
# def home():
#     return "Welcome to the Camera Trigger Server!", 200

# @app.route('/favicon.ico')
# def favicon():
#     return "", 204

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

from flask import Flask, Response
from appwrite.client import Client
from appwrite.services.storage import Storage
from appwrite.input_file import InputFile
from flask_cors import CORS
import cv2
import datetime
import os
import numpy as np
import threading

app = Flask(__name__)
CORS(app)

# Appwrite configuration
APPWRITE_ENDPOINT = "https://cloud.appwrite.io/v1"
APPWRITE_PROJECT_ID = "67e25e080016d17344a1"
APPWRITE_API_KEY = "standard_826e779be35c9ef95f2ce051718c5dfb9a01c6557984b81c07c876042e7f09ac811bfa2642875db220bf7e4c5b299d685146c5e6bfe5e37eb174a7259129d13306e4baac6d46263fada0054d09472db21db500429230925b82c62606c8f3c5f9389fb95314d6574219713861a9dc5b03bb54a66cc1b8fbb348b7b3c7e4a04319"
STORAGE_BUCKET_ID = "image_id"

client = Client()
client.set_endpoint(APPWRITE_ENDPOINT)
client.set_project(APPWRITE_PROJECT_ID)
client.set_key(APPWRITE_API_KEY)
storage = Storage(client)

# Global flag to control recording
is_recording = False

def record_video():
    global is_recording
    VIDEO_DURATION = 7  # Seconds
    FRAME_RATE = 30
    VIDEO_WIDTH, VIDEO_HEIGHT = 640, 480

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open camera")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_HEIGHT)

    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".mp4"
    temp_path = f"temp_{filename}"
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use mp4v for compatibility
    out = cv2.VideoWriter(temp_path, fourcc, FRAME_RATE, (VIDEO_WIDTH, VIDEO_HEIGHT))

    if not out.isOpened():
        cap.release()
        print("Failed to initialize video writer")
        return

    start_time = datetime.datetime.now()
    while (datetime.datetime.now() - start_time).seconds < VIDEO_DURATION:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
    
    out.release()
    cap.release()

    if not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
        print("Failed to save video file")
        return

    try:
        with open(temp_path, 'rb') as video_file:
            result = storage.create_file(
                bucket_id=STORAGE_BUCKET_ID,
                file_id='unique()',
                file=InputFile.from_bytes(video_file.read(), filename=filename, mime_type="video/mp4")
            )
        print(f"Uploaded file ID: {result['$id']}")
        os.remove(temp_path)
    except Exception as e:
        print(f"Upload failed: {str(e)}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
    finally:
        is_recording = False

def detect_motion():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open camera for motion detection")
        return

    # Initialize background subtractor for motion detection
    fgbg = cv2.createBackgroundSubtractorMOG2()
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Apply background subtraction
        fgmask = fgbg.apply(frame)
        motion_detected = np.sum(fgmask) > 10000  # Threshold for motion (adjust as needed)

        global is_recording
        if motion_detected and not is_recording:
            is_recording = True
            print("Motion detected, starting recording...")
            threading.Thread(target=record_video).start()

        # Optional: Show live feed for debugging (remove in production)
        # cv2.imshow('Frame', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    cap.release()
    cv2.destroyAllWindows()

@app.route('/start_detection', methods=['GET'])
def start_detection():
    if not threading.active_count() > 1:  # Ensure detection isn’t already running
        threading.Thread(target=detect_motion, daemon=True).start()
        return "Motion detection started", 200
    return "Motion detection already running", 200

@app.route('/')
def home():
    return "Welcome to the Smart Doorbell Server!", 200

@app.route('/favicon.ico')
def favicon():
    return "", 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)