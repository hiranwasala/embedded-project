// import { useEffect, useState } from "react";
// import { Client, Storage } from "appwrite";
// import "../../src/index.css";  

// const APPWRITE_ENDPOINT = "https://cloud.appwrite.io/v1";
// const APPWRITE_PROJECT_ID = "67e25e080016d17344a1";
// const STORAGE_BUCKET_ID = "image_id";

// const client = new Client()
//   .setEndpoint(APPWRITE_ENDPOINT)
//   .setProject(APPWRITE_PROJECT_ID);
// const storage = new Storage(client);

// export default function VideoDetection() {
//   const [videos, setVideos] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [detectionStatus, setDetectionStatus] = useState("Ready to capture");

//   const fetchVideos = async () => {
//     try {
//       const files = await storage.listFiles(STORAGE_BUCKET_ID);
//       setVideos(files.files.reverse()); 
//     } catch (error) {
//       console.error("Error fetching videos:", error);
//     }
//   };

//   useEffect(() => {
//     fetchVideos();
//     const interval = setInterval(fetchVideos, 5000);
//     return () => clearInterval(interval);
//   }, []);

//   const recordVideo = async () => {
//     setLoading(true);
//     setDetectionStatus("Detecting objects...");
//     try {
//       const response = await fetch("http://localhost:5000/record_video");
//       const result = await response.text();
//       console.log(result);
//       setDetectionStatus("Detection complete! Processing video...");
//       await fetchVideos();
//       setDetectionStatus("Ready to capture");
//     } catch (error) {
//       console.error("Error recording video:", error);
//       setDetectionStatus("Error occurred. Try again.");
//     }
//     setLoading(false);
//   };

//   return (
//     <div className="app-container">
//       <div className="content-wrapper">
//         <header className="header">
//           <h1>Object Detection Video Capture</h1>
//           <p>Automatically record videos when objects are detected</p>
//         </header>

//         {/* Add controls section to use loading, detectionStatus, and recordVideo */}
//         <section className="controls">
//           <button
//             onClick={recordVideo}
//             disabled={loading}
//             className="record-button"
//           >
//             {loading ? "Recording..." : "Start Recording"}
//           </button>
//           <p className="status-text">Status: {detectionStatus}</p>
//         </section>

//         <section className="video-gallery">
//           <h2 className="gallery-title">Latest Detections</h2>
//           {videos.length === 0 ? (
//             <div className="empty-state">
//               <p>No videos captured yet</p>
//             </div>
//           ) : (
//             <div className="video-grid">
//               {videos.map((video) => {
//                 const videoUrl = `${APPWRITE_ENDPOINT}/storage/buckets/${STORAGE_BUCKET_ID}/files/${video.$id}/view?project=${APPWRITE_PROJECT_ID}`;
//                 console.log('Video URL:', videoUrl); // Debugging
                
//                 return (
//                   <div key={video.$id} className="video-card">
//                     <div className="video-container">
//                       <video 
//                         controls 
//                         autoPlay 
//                         // muted 
//                         loop 
//                         playsInline
//                         className="video-player"
                        
//                       >
//                         <source
//                           src={videoUrl}
//                           type="video/mp4"
//                         />
//                         Your browser does not support the video tag.
//                       </video>
//                     </div>
//                     <div className="video-info">
//                       <h3>{video.name.replace('.mp4', '')}</h3>
//                       <div className="video-meta">
//                         <span>{new Date(video.$createdAt).toLocaleString()}</span>
//                       </div>
//                     </div>
//                   </div>
//                 );
//               })}
//             </div>
//           )}
//         </section>

//         <footer className="footer">
//           <p>Object Detection System • {new Date().getFullYear()}</p>
//         </footer>
//       </div>
//     </div>
//   );
// }

import { useEffect, useState, useRef } from "react";
import { Client, Storage } from "appwrite";
import "../../src/index.css";  

const APPWRITE_ENDPOINT = "https://cloud.appwrite.io/v1";
const APPWRITE_PROJECT_ID = "67e25e080016d17344a1";
const STORAGE_BUCKET_ID = "image_id";

const client = new Client()
  .setEndpoint(APPWRITE_ENDPOINT)
  .setProject(APPWRITE_PROJECT_ID);
const storage = new Storage(client);

export default function VideoDetection() {
  const [videos, setVideos] = useState([]);
  const [latestVideoUrl, setLatestVideoUrl] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const videoRef = useRef(null);

  const fetchVideos = async () => {
    try {
      const files = await storage.listFiles(STORAGE_BUCKET_ID);
      const sortedFiles = files.files.reverse(); // Latest first
      setVideos(sortedFiles);
      
      // Auto-play the latest video if it’s new
      if (sortedFiles.length > 0) {
        const newLatestUrl = `${APPWRITE_ENDPOINT}/storage/buckets/${STORAGE_BUCKET_ID}/files/${sortedFiles[0].$id}/view?project=${APPWRITE_PROJECT_ID}`;
        if (newLatestUrl !== latestVideoUrl) {
          setLatestVideoUrl(newLatestUrl);
          setIsPlaying(true);
        }
      }
    } catch (error) {
      console.error("Error fetching videos:", error);
    }
  };

  useEffect(() => {
    // Start motion detection on backend
    fetch("http://localhost:5000/start_detection");

    // Poll for new videos every 5 seconds
    fetchVideos();
    const interval = setInterval(fetchVideos, 5000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (videoRef.current && isPlaying) {
      videoRef.current.play().catch((err) => console.error("Auto-play error:", err));
    }
  }, [latestVideoUrl, isPlaying]);

  const stopVideo = () => {
    if (videoRef.current) {
      videoRef.current.pause();
      setIsPlaying(false);
    }
  };

  return (
    <div className="app-container">
      <div className="content-wrapper">
        <header className="header">
          <h1>Smart Doorbell System</h1>
          <p>Automatically records and plays video when an object is detected</p>
        </header>

        <section className="video-player-section">
          {latestVideoUrl ? (
            <>
              <video
                ref={videoRef}
                controls
                className="video-player"
                src={latestVideoUrl}
                type="video/mp4"
                onError={(e) => console.error("Video playback error:", e)}
              >
                Your browser does not support the video tag.
              </video>
              <button
                onClick={stopVideo}
                className="stop-button"
                disabled={!isPlaying}
              >
                Stop Video
              </button>
            </>
          ) : (
            <p>Waiting for object detection...</p>
          )}
        </section>

        <section className="video-gallery">
          <h2 className="gallery-title">Previous Detections</h2>
          {videos.length === 0 ? (
            <div className="empty-state">
              <p>No videos captured yet</p>
            </div>
          ) : (
            <div className="video-grid">
              {videos.slice(1).map((video) => { // Skip the latest video (shown above)
                const videoUrl = `${APPWRITE_ENDPOINT}/storage/buckets/${STORAGE_BUCKET_ID}/files/${video.$id}/view?project=${APPWRITE_PROJECT_ID}`;
                return (
                  <div key={video.$id} className="video-card">
                    <video controls className="video-player">
                      <source src={videoUrl} type="video/mp4" />
                      Your browser does not support the video tag.
                    </video>
                    <div className="video-info">
                      <h3>{video.name.replace('.mp4', '')}</h3>
                      <span>{new Date(video.$createdAt).toLocaleString()}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </section>

        <footer className="footer">
          <p>Smart Doorbell System • {new Date().getFullYear()}</p>
        </footer>
      </div>
    </div>
  );
}