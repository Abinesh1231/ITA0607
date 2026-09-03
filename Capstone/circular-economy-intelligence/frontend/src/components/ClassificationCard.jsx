export default function ClassificationCard({ data }) {
  if (!data) return null;

  return (
    <div className="card">
      <h3>Material Identification</h3>

      <div className="result-label">{data.material}</div>

      <p>Confidence: {(data.confidence * 100).toFixed(1)}%</p>

      <p>
        Recyclable: <strong>{data.recyclable ? "Yes" : "No"}</strong>
      </p>

      {data.top_predictions && data.top_predictions.length > 0 && (
        <div style={{ marginTop: "24px" }}>
          <h4>Top Predictions</h4>

          <div>
            {data.top_predictions.map((prediction, index) => (
              <div
                key={index}
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  padding: "8px 0",
                  borderBottom: "1px solid #eee",
                }}
              >
                <span>
                  {index + 1}. <strong>{prediction.material}</strong>
                </span>

                <span>{(prediction.confidence * 100).toFixed(1)}%</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
