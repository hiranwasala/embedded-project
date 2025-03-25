
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



from flask import Flask
from appwrite.client import Client
from appwrite.services.storage import Storage
from appwrite.input_file import InputFile
from flask_cors import CORS
import cv2
import datetime
from io import BytesIO
import os

app = Flask(__name__)
CORS(app)


APPWRITE_ENDPOINT = "https://cloud.appwrite.io/v1"  
APPWRITE_PROJECT_ID = "67e25e080016d17344a1"    
APPWRITE_API_KEY = "standard_826e779be35c9ef95f2ce051718c5dfb9a01c6557984b81c07c876042e7f09ac811bfa2642875db220bf7e4c5b299d685146c5e6bfe5e37eb174a7259129d13306e4baac6d46263fada0054d09472db21db500429230925b82c62606c8f3c5f9389fb95314d6574219713861a9dc5b03bb54a66cc1b8fbb348b7b3c7e4a04319"          
STORAGE_BUCKET_ID = "image_id"     


client = Client()
client.set_endpoint(APPWRITE_ENDPOINT)      
client.set_project(APPWRITE_PROJECT_ID)       
client.set_key(APPWRITE_API_KEY)             
storage = Storage(client)

@app.route('/record_video', methods=['GET'])
def record_video():
    # Video settings
    VIDEO_DURATION = 7  # Seconds
    FRAME_RATE = 30
    VIDEO_WIDTH, VIDEO_HEIGHT = 640, 480

    # Initialize camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_HEIGHT)

    # Generate filename
    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".mp4"
    temp_path = f"temp_{filename}"
    
    # Define video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_path, fourcc, FRAME_RATE, (VIDEO_WIDTH, VIDEO_HEIGHT))

    # Record for VIDEO_DURATION seconds
    start_time = datetime.datetime.now()
    while (datetime.datetime.now() - start_time).seconds < VIDEO_DURATION:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
    
    # Release resources
    out.release()
    cap.release()

    # Upload to Appwrite Storage
    try:
        with open(temp_path, 'rb') as video_file:
            result = storage.create_file(
                bucket_id=STORAGE_BUCKET_ID,
                file_id='unique',
                file=InputFile.from_bytes(video_file.read(), filename=filename)
            ) 
        
        return f"Video uploaded to Appwrite! File ID: {result['$id']}", 200
    except Exception as e:
        return f"Upload failed: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

