export default function ValuationMetrics({ data, loading, error }) {
  if (loading) {
    return (
      <div className="card valuation-metrics-card">
        <h2>Recycling Value Estimation Results</h2>
        <p className="muted">Loading model performance...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card valuation-metrics-card">
        <h2>Recycling Value Estimation Results</h2>
        <p className="metrics-error">{error}</p>
      </div>
    );
  }

  if (!data || !data.available) {
    return (
      <div className="card valuation-metrics-card">
        <h2>Recycling Value Estimation Results</h2>
        <p className="muted">Model evaluation metrics are not available yet.</p>
      </div>
    );
  }

  return (
    <div className="card valuation-metrics-card">
      <div className="metrics-header">
        <div>
          <h2>Recycling Value Estimation Results</h2>
          <p className="muted">Performance of the trained valuation model.</p>
        </div>

        <span className="model-badge">
          {data.model || "RandomForestRegressor"}
        </span>
      </div>

      <div className="metrics-grid">
        <div className="metric-box mae">
          <span>MAE</span>
          <strong>₹{Number(data.mae).toFixed(2)}</strong>
          <small>Mean Absolute Error</small>
        </div>

        <div className="metric-box rmse">
          <span>RMSE</span>
          <strong>₹{Number(data.rmse).toFixed(2)}</strong>
          <small>Root Mean Squared Error</small>
        </div>

        <div className="metric-box r2">
          <span>R² Score</span>
          <strong>{Number(data.r2_score).toFixed(4)}</strong>
          <small>Coefficient of Determination</small>
        </div>
      </div>

      <div className="dataset-info">
        <div>
          <span>Training Samples</span>
          <strong>{data.training_samples}</strong>
        </div>

        <div>
          <span>Testing Samples</span>
          <strong>{data.testing_samples}</strong>
        </div>
      </div>
    </div>
  );
}
