import React, { useEffect, useState } from "react";
import CameraView from "./CameraView";
import ManualPanel from "./ManualPanel";
import "./styles.css";

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const interval = setInterval(() => {
      fetch("http://localhost:5001/detect")
        .then(res => res.json())
        .then(d => setData(d))
        .catch(err => console.error("API Error:", err));
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="app">
      <h1>🧠 AI Smart Manual Scanner</h1>
      
      <div className="controls">
        <button onClick={() => fetch("http://localhost:5001/set_mode/macbook", {method: "POST"})}>💻 MacBook Mode</button>
        <button onClick={() => fetch("http://localhost:5001/set_mode/gobolt", {method: "POST"})}>🎧 GoBOLT Mode</button>
      </div>

      <div className="container">
        <CameraView data={data} />
        <ManualPanel manual={data?.manual} type={data?.type} />
      </div>
    </div>
  );
}

export default App;
