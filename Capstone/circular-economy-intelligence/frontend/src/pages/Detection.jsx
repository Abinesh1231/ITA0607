import { useState } from "react";
import ImageUpload from "../components/ImageUpload";
import DetectionCard from "../components/DetectionCard";
import { detectWaste } from "../services/api";

export default function Detection() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);
  const [imageSize, setImageSize] = useState({
    width: 1,
    height: 1,
  });
  const [loading, setLoading] = useState(false);

  function handleFileSelect(selectedFile) {
    setFile(selectedFile);
    setData(null);

    if (imageUrl) {
      URL.revokeObjectURL(imageUrl);
    }

    if (selectedFile) {
      const url = URL.createObjectURL(selectedFile);
      setImageUrl(url);
    } else {
      setImageUrl(null);
    }
  }

  function handleImageLoad(event) {
    setImageSize({
      width: event.currentTarget.naturalWidth,
      height: event.currentTarget.naturalHeight,
    });
  }

  async function run() {
    if (!file) return;

    setLoading(true);
    setData(null);

    try {
      const result = await detectWaste(file);
      setData(result);
    } catch (error) {
      setData({
        model_status: "error",
        detail:
          error.response?.data?.detail || error.message || "Detection failed.",
        detections: [],
      });
    } finally {
      setLoading(false);
    }
  }

  return (
    <section>
      <h1>Object Detection</h1>

      <p>Detect multiple waste objects in an image using YOLO.</p>

      <ImageUpload onSelect={handleFileSelect} />

      {imageUrl && (
        <div className="detection-image-wrapper">
          <img
            src={imageUrl}
            alt="Uploaded waste"
            className="detection-image"
            onLoad={handleImageLoad}
          />

          {data?.model_status === "ready" &&
            data.detections?.map((item, index) => {
              const [x1, y1, x2, y2] = item.bbox;

              const left = (x1 / imageSize.width) * 100;
              const top = (y1 / imageSize.height) * 100;
              const width = ((x2 - x1) / imageSize.width) * 100;
              const height = ((y2 - y1) / imageSize.height) * 100;

              return (
                <div
                  key={index}
                  className="detection-box"
                  style={{
                    left: `${left}%`,
                    top: `${top}%`,
                    width: `${width}%`,
                    height: `${height}%`,
                  }}
                >
                  <span className="detection-label">
                    {item.label} {(item.confidence * 100).toFixed(0)}%
                  </span>
                </div>
              );
            })}
        </div>
      )}

      <button className="primary" onClick={run} disabled={!file || loading}>
        {loading ? "Detecting..." : "Run Detection"}
      </button>

      {loading && <div className="loading">Running object detection...</div>}

      {data && <DetectionCard data={data} />}
    </section>
  );
}
