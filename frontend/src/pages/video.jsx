import { useEffect, useState } from "react";
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
  const [loading, setLoading] = useState(false);
  const [detectionStatus, setDetectionStatus] = useState("Ready to capture");

  const fetchVideos = async () => {
    try {
      const files = await storage.listFiles(STORAGE_BUCKET_ID);
      setVideos(files.files.reverse()); 
    } catch (error) {
      console.error("Error fetching videos:", error);
    }
  };

  useEffect(() => {
    fetchVideos();
    const interval = setInterval(fetchVideos, 5000);
    return () => clearInterval(interval);
  }, []);

  const recordVideo = async () => {
    setLoading(true);
    setDetectionStatus("Detecting objects...");
    try {
      const response = await fetch("http://localhost:5000/record_video");
      const result = await response.text();
      console.log(result);
      setDetectionStatus("Detection complete! Processing video...");
      await fetchVideos();
      setDetectionStatus("Ready to capture");
    } catch (error) {
      console.error("Error recording video:", error);
      setDetectionStatus("Error occurred. Try again.");
    }
    setLoading(false);
  };

  return (
    <div className="app-container">
      <div className="content-wrapper">
        <header className="header">
          <h1>Object Detection Video Capture</h1>
          <p>Automatically record videos when objects are detected</p>
        </header>

        <section className="video-gallery">
          <h2 className="gallery-title">Latest Detections</h2>
          {videos.length === 0 ? (
            <div className="empty-state">
              <p>No videos captured yet</p>
            </div>
          ) : (
            <div className="video-grid">
              {videos.map((video) => {
                const videoUrl = `${APPWRITE_ENDPOINT}/storage/buckets/${STORAGE_BUCKET_ID}/files/${video.$id}/view?project=${APPWRITE_PROJECT_ID}`;
                console.log('Video URL:', videoUrl); // Debugging
                
                return (
                  <div key={video.$id} className="video-card">
                    <div className="video-container">
                      <video 
                        controls 
                        autoPlay 
                        muted 
                        loop 
                        playsInline
                        className="video-player"
                      >
                        <source
                          src={videoUrl}
                          type="video/mp4"
                        />
                        Your browser does not support the video tag.
                      </video>
                    </div>
                    <div className="video-info">
                      <h3>{video.name.replace('.mp4', '')}</h3>
                      <div className="video-meta">
                        <span>{new Date(video.$createdAt).toLocaleString()}</span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </section>

        <footer className="footer">
          <p>Object Detection System • {new Date().getFullYear()}</p>
        </footer>
      </div>
    </div>
  );
}