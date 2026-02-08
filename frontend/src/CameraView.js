import React from "react";

function CameraView({ data }) {
  return (
    <div className="camera-box">
      <h3>Live Detection</h3>
      {data?.device ? (
        <div className="detected">
            <p className="status">✅ {data.device}</p>
            <p className="confidence">Confidence: {(data.confidence * 100).toFixed(1)}%</p>
        </div>
      ) : (
        <p>Scanning...</p>
      )}
      {/* In a real app, we would put an <img src="http://localhost:5000/video_feed" /> here */}
      <div className="video-container">
        <img src="http://localhost:5001/video_feed" alt="Live Camera Feed" style={{ width: "100%", borderRadius: "8px" }} />
      </div>
    </div>
  );
}

export default CameraView;
 