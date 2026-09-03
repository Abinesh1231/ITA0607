import { useEffect, useState } from "react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  Legend,
  LineChart,
  Line,
} from "recharts";

import StatisticsCard from "../components/StatisticsCard";
import { getDashboardStats } from "../services/api";

const MATERIAL_COLORS = {
  metal: "#3B82F6",
  plastic: "#F59E0B",
  paper: "#8B5CF6",
  glass: "#06B6D4",
  cardboard: "#92400E",
  shoes: "#EC4899",
  battery: "#EF4444",
  clothes: "#10B981",
  waste: "#6B7280",
};

const RECYCLABILITY_COLORS = ["#2E7D32", "#EF4444"];

export default function Dashboard() {
  const [dashboard, setDashboard] = useState({
    stats: {
      total_analyses: 0,
      recyclable_analyses: 0,
      non_recyclable_analyses: 0,
      recyclable_percentage: 0,
      total_weight_kg: 0,
      estimated_value: 0,
    },
    material_distribution: [],
    recent_analyses: [],
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadDashboard() {
    try {
      setLoading(true);
      setError("");

      const data = await getDashboardStats();

      setDashboard({
        stats: {
          total_analyses: Number(data.stats?.total_analyses) || 0,
          recyclable_analyses: Number(data.stats?.recyclable_analyses) || 0,
          non_recyclable_analyses:
            Number(data.stats?.non_recyclable_analyses) || 0,
          recyclable_percentage: Number(data.stats?.recyclable_percentage) || 0,
          total_weight_kg: Number(data.stats?.total_weight_kg) || 0,
          estimated_value: Number(data.stats?.estimated_value) || 0,
        },

        material_distribution: Array.isArray(data.material_distribution)
          ? data.material_distribution
          : [],

        recent_analyses: Array.isArray(data.recent_analyses)
          ? data.recent_analyses
          : [],
      });
    } catch (err) {
      console.error("Dashboard error:", err);
      setError("Unable to load dashboard statistics.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  const stats = dashboard.stats;

  // ------------------------------------------------------------
  // PIE CHART DATA
  // ------------------------------------------------------------

  const recyclabilityData = [
    {
      name: "Recyclable",
      value: stats.recyclable_analyses,
    },
    {
      name: "Non-Recyclable",
      value: stats.non_recyclable_analyses,
    },
  ];

  // ------------------------------------------------------------
  // CONFIDENCE CHART DATA
  // ------------------------------------------------------------

  const confidenceData = [...dashboard.recent_analyses]
    .reverse()
    .map((item, index) => ({
      name: `#${index + 1}`,
      confidence: Number(item.confidence || 0) * 100,
      material: item.material,
    }));

  return (
    <section className="dashboard-page">
      {/* -------------------------------------------------- */}
      {/* HEADER */}
      {/* -------------------------------------------------- */}

      <div className="page-head dashboard-header">
        <div>
          <h1>Dashboard</h1>

          <p>Waste intelligence and circular economy insights.</p>
        </div>

        <button className="primary" onClick={loadDashboard} disabled={loading}>
          {loading ? "Refreshing..." : "Refresh Dashboard"}
        </button>
      </div>

      {/* -------------------------------------------------- */}
      {/* ERROR */}
      {/* -------------------------------------------------- */}

      {error && (
        <div className="card dashboard-error">
          <p>{error}</p>
        </div>
      )}

      {/* -------------------------------------------------- */}
      {/* STATISTICS */}
      {/* -------------------------------------------------- */}

      <div className="stats-grid">
        <StatisticsCard
          title="Total Analyses"
          value={loading ? "..." : stats.total_analyses}
          subtitle="Images processed"
        />

        <StatisticsCard
          title="Recyclable"
          value={loading ? "..." : stats.recyclable_analyses}
          subtitle={`${stats.recyclable_percentage}% of analyses`}
        />

        <StatisticsCard
          title="Estimated Value"
          value={loading ? "..." : `₹${stats.estimated_value.toFixed(2)}`}
          subtitle={`${stats.total_weight_kg.toFixed(2)} kg processed`}
        />
      </div>

      {/* -------------------------------------------------- */}
      {/* CHART ROW 1 */}
      {/* -------------------------------------------------- */}

      <div className="dashboard-chart-grid">
        {/* MATERIAL BAR CHART */}

        <div className="card chart-card">
          <div className="chart-header">
            <div>
              <h2>Material Distribution</h2>

              <p className="muted">Waste materials identified by the system.</p>
            </div>
          </div>

          <div className="chart-container">
            {dashboard.material_distribution.length === 0 ? (
              <div className="chart-empty">No material data available.</div>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={dashboard.material_distribution}
                  margin={{
                    top: 10,
                    right: 20,
                    left: 0,
                    bottom: 20,
                  }}
                >
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />

                  <XAxis dataKey="material" tick={{ fontSize: 12 }} />

                  <YAxis allowDecimals={false} />

                  <Tooltip
                    formatter={(value) => [value, "Analyses"]}
                    contentStyle={{
                      backgroundColor: "#ffffff",
                      border: "1px solid #dce5dd",
                      borderRadius: "10px",
                      boxShadow: "0 6px 18px rgba(0,0,0,0.08)",
                    }}
                  />
                  <Bar
                    dataKey="count"
                    name="Analyses"
                    radius={[8, 8, 0, 0]}
                    activeBar={{
                      opacity: 0.75,
                    }}
                  >
                    {dashboard.material_distribution.map((entry) => (
                      <Cell
                        key={entry.material}
                        fill={
                          MATERIAL_COLORS[
                            String(entry.material).toLowerCase()
                          ] || "#2E7D32"
                        }
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

        {/* RECYCLABILITY PIE CHART */}

        <div className="card chart-card">
          <div className="chart-header">
            <div>
              <h2>Recyclability</h2>

              <p className="muted">Recyclable versus non-recyclable waste.</p>
            </div>
          </div>

          <div className="chart-container">
            {stats.total_analyses === 0 ? (
              <div className="chart-empty">No analysis data available.</div>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={recyclabilityData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    innerRadius={55}
                    paddingAngle={3}
                    label={false}
                  >
                    {recyclabilityData.map((entry, index) => (
                      <Cell
                        key={entry.name}
                        fill={RECYCLABILITY_COLORS[index]}
                      />
                    ))}
                  </Pie>

                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#ffffff",
                      border: "1px solid #dce5dd",
                      borderRadius: "10px",
                      boxShadow: "0 6px 18px rgba(0,0,0,0.08)",
                    }}
                  />

                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>
      </div>

      {/* -------------------------------------------------- */}
      {/* CHART ROW 2 */}
      {/* -------------------------------------------------- */}

      <div className="card chart-card chart-card-wide">
        <div className="chart-header">
          <div>
            <h2>Recent Analysis Confidence</h2>

            <p className="muted">
              Classification confidence for the latest analyses.
            </p>
          </div>
        </div>

        <div className="chart-container">
          {confidenceData.length === 0 ? (
            <div className="chart-empty">
              No recent analysis data available.
            </div>
          ) : (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={confidenceData}
                margin={{
                  top: 10,
                  right: 20,
                  left: 0,
                  bottom: 20,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" vertical={false} />

                <XAxis dataKey="name" />

                <YAxis
                  domain={[0, 100]}
                  tickFormatter={(value) => `${value}%`}
                />

                <Tooltip
                  formatter={(value, name, props) => [
                    `${Number(value).toFixed(1)}%`,
                    props.payload.material || "Confidence",
                  ]}
                />

                <Line
                  type="monotone"
                  dataKey="confidence"
                  stroke="#2E7D32"
                  strokeWidth={3}
                  dot={{
                    r: 5,
                    fill: "#2E7D32",
                    strokeWidth: 2,
                  }}
                  activeDot={{
                    r: 8,
                    fill: "#1B5E20",
                  }}
                  name="Confidence"
                />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      {/* -------------------------------------------------- */}
      {/* PIPELINE */}
      {/* -------------------------------------------------- */}

      <div className="card pipeline-card">
        <h2>Project Pipeline</h2>

        <p>
          Upload a waste image to identify the material, assess recyclability,
          estimate value, and receive a recommended action.
        </p>

        <div className="pipeline-steps">
          <div>
            <span>01</span>
            <strong>Detect</strong>
            <small>Identify waste material</small>
          </div>

          <div>
            <span>02</span>
            <strong>Analyze</strong>
            <small>Assess recyclability</small>
          </div>

          <div>
            <span>03</span>
            <strong>Value</strong>
            <small>Estimate recovery value</small>
          </div>

          <div>
            <span>04</span>
            <strong>Recommend</strong>
            <small>Suggest next action</small>
          </div>
        </div>
      </div>
    </section>
  );
}
