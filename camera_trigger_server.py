
# # from flask import Flask
# # from appwrite.client import Client
# # from appwrite.services.storage import Storage
# # from appwrite.input_file import InputFile
# # import cv2
# # import datetime
# # from io import BytesIO

# # app = Flask(__name__)


# # APPWRITE_ENDPOINT = "https://cloud.appwrite.io/v1"  
# # APPWRITE_PROJECT_ID = "67e25e080016d17344a1"    
# # APPWRITE_API_KEY = "standard_826e779be35c9ef95f2ce051718c5dfb9a01c6557984b81c07c876042e7f09ac811bfa2642875db220bf7e4c5b299d685146c5e6bfe5e37eb174a7259129d13306e4baac6d46263fada0054d09472db21db500429230925b82c62606c8f3c5f9389fb95314d6574219713861a9dc5b03bb54a66cc1b8fbb348b7b3c7e4a04319"          
# # STORAGE_BUCKET_ID = "image_id"     


# # client = Client()
# # client.set_endpoint(APPWRITE_ENDPOINT)      
# # client.set_project(APPWRITE_PROJECT_ID)       
# # client.set_key(APPWRITE_API_KEY)             
# # storage = Storage(client)

# # @app.route('/trigger', methods=['GET'])
# # def trigger_webcam():
# #     # Initialize camera
# #     cap = cv2.VideoCapture(0)
# #     ret, frame = cap.read()
# #     if not ret:
# #         cap.release()
# #         return "Failed to capture image", 400

# #     # Generate filename
# #     filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
    
# #     # Save locally (optional)
# #     cv2.imwrite(filename, frame)
# #     print(f"Captured {filename}")

# #     # Upload to Appwrite Storage
# #     try:
# #         with open(filename, 'rb') as file:
# #             file_data = file.read()
        
# #         result = storage.create_file(
# #             bucket_id=STORAGE_BUCKET_ID,
# #             file_id='unique',  
# #             file=InputFile.from_bytes(file_data, filename=filename)
# #         )
# #         cap.release()
# #         return f"Image captured & uploaded to Appwrite! File ID: {result['$id']}", 200
# #     except Exception as e:
# #         cap.release()
# #         return f"Appwrite upload failed: {str(e)}", 500

# # if __name__ == '__main__':
# #     app.run(host='0.0.0.0', port=5000)



# from flask import Flask
# from appwrite.client import Client
# from appwrite.services.storage import Storage
# from appwrite.input_file import InputFile
# from flask_cors import CORS
# import cv2
# import datetime
# from io import BytesIO
# import os

# app = Flask(__name__)
# CORS(app)


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
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_WIDTH)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_HEIGHT)

#     # Generate filename
#     filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".mp4"
#     temp_path = f"temp_{filename}"
    
#     # Define video writer
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter(temp_path, fourcc, FRAME_RATE, (VIDEO_WIDTH, VIDEO_HEIGHT))

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

#     # Upload to Appwrite Storage
#     try:
#         with open(temp_path, 'rb') as video_file:
#             result = storage.create_file(
#                 bucket_id=STORAGE_BUCKET_ID,
#                 file_id='unique',
#                 file=InputFile.from_bytes(video_file.read(), filename=filename)
#             ) 
        
#         return f"Video uploaded to Appwrite! File ID: {result['$id']}", 200
#     except Exception as e:
#         return f"Upload failed: {str(e)}", 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)




from flask import Flask
from appwrite.client import Client
from appwrite.services.storage import Storage
from appwrite.input_file import InputFile
from flask_cors import CORS
import cv2
import datetime
import os
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from PIL import Image
import numpy as np

app = Flask(__name__)
CORS(app)

# Appwrite configuration
APPWRITE_ENDPOINT = "https://cloud.appwrite.io/v1"
APPWRITE_PROJECT_ID = "67e25e080016d17344a1"
APPWRITE_API_KEY = "your_api_key_here"
STORAGE_BUCKET_ID = "image_id"

client = Client()
client.set_endpoint(APPWRITE_ENDPOINT)
client.set_project(APPWRITE_PROJECT_ID)
client.set_key(APPWRITE_API_KEY)
storage = Storage(client)

# Initialize face recognition models
mtcnn = MTCNN(image_size=160, margin=0)
resnet = InceptionResnetV1(pretrained='vggface2').eval()

# Simple known faces database (embeddings and names)
known_faces = {
    "John Doe": None,  # Placeholder for embedding
    "Jane Smith": None
}

# Load known face embeddings (you'd typically load these from a file or database)
def load_known_faces():
    # Example: Replace with actual loading logic
    # For now, we'll generate embeddings when a known face is first detected
    pass

@app.route('/record_video', methods=['GET'])
def record_video():
    VIDEO_DURATION = 7
    FRAME_RATE = 30
    VIDEO_WIDTH, VIDEO_HEIGHT = 640, 480

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_HEIGHT)

    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".mp4"
    temp_path = f"temp_{filename}"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_path, fourcc, FRAME_RATE, (VIDEO_WIDTH, VIDEO_HEIGHT))

    detected_name = "Unknown"
    start_time = datetime.datetime.now()
    while (datetime.datetime.now() - start_time).seconds < VIDEO_DURATION:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert frame to RGB for face detection
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb_frame)
        
        # Detect faces
        boxes, _ = mtcnn.detect(pil_img)
        if boxes is not None:
            for box in boxes:
                # Extract face
                face = pil_img.crop((box[0], box[1], box[2], box[3]))
                face_tensor = mtcnn(face).unsqueeze(0)
                embedding = resnet(face_tensor).detach()

                # Compare with known faces
                for name, known_embedding in known_faces.items():
                    if known_embedding is not None:
                        distance = torch.dist(embedding, known_embedding).item()
                        if distance < 0.6:  # Threshold for recognition
                            detected_name = name
                            break
                else:
                    # If no match and not already "Unknown", add to known faces (for demo)
                    if detected_name == "Unknown" and "Unknown" not in known_faces:
                        known_faces["Unknown"] = embedding

        # Draw detection info on frame
        if detected_name != "Unknown":
            cv2.putText(frame, f"Detected: {detected_name}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        out.write(frame)

    out.release()
    cap.release()

    # Upload to Appwrite
    try:
        with open(temp_path, 'rb') as video_file:
            result = storage.create_file(
                bucket_id=STORAGE_BUCKET_ID,
                file_id='unique',
                file=InputFile.from_bytes(video_file.read(), filename=filename)
            )
        os.remove(temp_path)
        return f"Video uploaded! Detected: {detected_name}, File ID: {result['$id']}", 200
    except Exception as e:
        os.remove(temp_path)
        return f"Upload failed: {str(e)}", 500

if __name__ == '__main__':
    load_known_faces()
    app.run(host='0.0.0.0', port=5000)