import { useEffect, useState } from "react";
import { getWasteHistory } from "../services/api";

export default function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadHistory() {
      try {
        setLoading(true);
        setError("");

        const data = await getWasteHistory(100);

        setHistory(data.analyses || []);
      } catch (err) {
        console.error("History error:", err);
        setError("Unable to load analysis history.");
      } finally {
        setLoading(false);
      }
    }

    loadHistory();
  }, []);

  return (
    <section>
      <div className="page-head">
        <div>
          <h1>Analysis History</h1>
          <p>Previously analyzed waste items.</p>
        </div>
      </div>

      {loading && (
        <div className="card">
          <p>Loading analysis history...</p>
        </div>
      )}

      {error && (
        <div className="card">
          <p>{error}</p>
        </div>
      )}

      {!loading && !error && history.length === 0 && (
        <div className="card">
          <h2>No analyses yet</h2>
          <p>Analyze a waste image to create your first history record.</p>
        </div>
      )}

      {!loading && !error && history.length > 0 && (
        <div className="card">
          <h2>Recent Analyses</h2>

          <div style={{ overflowX: "auto" }}>
            <table
              style={{
                width: "100%",
                borderCollapse: "collapse",
                marginTop: "20px",
              }}
            >
              <thead>
                <tr>
                  <th style={thStyle}>ID</th>
                  <th style={thStyle}>Material</th>
                  <th style={thStyle}>Confidence</th>
                  <th style={thStyle}>Weight</th>
                  <th style={thStyle}>Value</th>
                  <th style={thStyle}>Recommendation</th>
                  <th style={thStyle}>Date</th>
                </tr>
              </thead>

              <tbody>
                {history.map((item) => (
                  <tr key={item.id}>
                    <td style={tdStyle}>{item.id}</td>

                    <td style={tdStyle}>
                      <strong>{formatMaterial(item.material)}</strong>
                    </td>

                    <td style={tdStyle}>
                      {item.confidence != null
                        ? `${(Number(item.confidence) * 100).toFixed(1)}%`
                        : "-"}
                    </td>

                    <td style={tdStyle}>
                      {item.weight_kg != null
                        ? `${Number(item.weight_kg).toFixed(2)} kg`
                        : "-"}
                    </td>

                    <td style={tdStyle}>
                      ₹
                      {item.estimated_value != null
                        ? Number(item.estimated_value).toFixed(2)
                        : "0.00"}
                    </td>

                    <td style={tdStyle}>{item.recommendation || "-"}</td>

                    <td style={tdStyle}>
                      {item.created_at ? formatDate(item.created_at) : "-"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </section>
  );
}

function formatMaterial(material) {
  if (!material) return "-";

  return material
    .split("-")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

function formatDate(date) {
  const parsed = new Date(date);

  if (Number.isNaN(parsed.getTime())) {
    return date;
  }

  return parsed.toLocaleString();
}

const thStyle = {
  textAlign: "left",
  padding: "12px",
  borderBottom: "2px solid #ddd",
  whiteSpace: "nowrap",
};

const tdStyle = {
  padding: "12px",
  borderBottom: "1px solid #eee",
  whiteSpace: "nowrap",
};
