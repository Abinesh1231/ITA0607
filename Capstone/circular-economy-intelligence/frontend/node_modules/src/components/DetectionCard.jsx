export default function DetectionCard({ data }) {
  if (!data) return null;

  if (data.model_status !== "ready") {
    return (
      <div className="card detection-card">
        <h2>Detection Results</h2>

        <div className="status-row">
          Model Status:
          <strong>{data.model_status}</strong>
        </div>

        <p>
          {data.message || data.detail || "Object detection is unavailable."}
        </p>
      </div>
    );
  }

  const detections = data.detections || [];

  // Count detected objects by material
  const materialCounts = detections.reduce((counts, item) => {
    counts[item.label] = (counts[item.label] || 0) + 1;
    return counts;
  }, {});

  return (
    <div className="card detection-card">
      <div className="detection-header">
        <div>
          <h2>Detection Results</h2>
          <p className="muted">
            Objects identified by the YOLO detection model.
          </p>
        </div>

        <div className="ready-badge">● READY</div>
      </div>

      <div className="detection-stat">
        <span>Objects Detected</span>
        <strong>{detections.length}</strong>
      </div>

      {detections.length === 0 ? (
        <div className="empty-detection">
          <p>No objects detected with sufficient confidence.</p>
        </div>
      ) : (
        <>
          <h3>Material Summary</h3>

          <div className="material-summary">
            {Object.entries(materialCounts).map(([material, count]) => (
              <div className="material-summary-item" key={material}>
                <span>{material}</span>
                <strong>{count}</strong>
              </div>
            ))}
          </div>

          <h3 className="detected-title">Detected Objects</h3>

          <div className="detected-list">
            {detections.map((item, index) => (
              <div className="detected-item" key={index}>
                <div className="detected-item-main">
                  <span className="object-number">{index + 1}</span>

                  <div>
                    <strong>{item.label}</strong>

                    <p>
                      Confidence:{" "}
                      <strong>{(item.confidence * 100).toFixed(1)}%</strong>
                    </p>
                  </div>
                </div>

                <div className="confidence-bar">
                  <div
                    className="confidence-fill"
                    style={{
                      width: `${Math.min(item.confidence * 100, 100)}%`,
                    }}
                  />
                </div>

                <p className="bbox">
                  Bounding box:{" "}
                  {item.bbox
                    .map((value) => Number(value).toFixed(1))
                    .join(", ")}
                </p>
              </div>
            ))}
          </div>
        </>
      )}

      <div className="model-status">
        Model status: <strong>ready</strong>
      </div>
    </div>
  );
}
