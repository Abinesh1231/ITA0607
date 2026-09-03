import { useEffect, useState } from "react";
import ValuationCard from "../components/ValuationCard";
import ValuationMetrics from "../components/ValuationMetrics";
import { estimateValue, getValuationMetrics } from "../services/api";

export default function Valuation() {
  const [material, setMaterial] = useState("plastic");
  const [weight, setWeight] = useState(1);
  const [data, setData] = useState(null);

  const [metrics, setMetrics] = useState(null);
  const [metricsLoading, setMetricsLoading] = useState(true);
  const [metricsError, setMetricsError] = useState("");

  const materials = [
    "paper",
    "cardboard",
    "plastic",
    "metal",
    "white-glass",
    "green-glass",
    "brown-glass",
    "battery",
    "clothes",
    "shoes",
    "biological",
    "trash",
  ];

  useEffect(() => {
    async function loadMetrics() {
      try {
        setMetricsLoading(true);
        setMetricsError("");

        const result = await getValuationMetrics();

        setMetrics(result);
      } catch (error) {
        console.error("Valuation metrics error:", error);
        setMetricsError("Unable to load valuation model metrics.");
      } finally {
        setMetricsLoading(false);
      }
    }

    loadMetrics();
  }, []);

  async function run() {
    try {
      const result = await estimateValue(material, Number(weight), 1);

      setData(result);
    } catch (error) {
      console.error("Valuation error:", error);
    }
  }

  return (
    <section>
      <div className="page-head">
        <h1>Recycling Value Estimation</h1>

        <p>
          Estimate the potential recovery value of recyclable materials based on
          weight and reference recycling rates.
        </p>
      </div>

      <div className="card form">
        <label>
          Material
          <select
            value={material}
            onChange={(e) => setMaterial(e.target.value)}
          >
            {materials.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </label>

        <label>
          Weight (kg)
          <input
            type="number"
            min="0.001"
            step="0.001"
            value={weight}
            onChange={(e) => setWeight(e.target.value)}
          />
        </label>

        <button className="primary" onClick={run}>
          Estimate
        </button>
      </div>

      <ValuationCard data={data} />

      <ValuationMetrics
        data={metrics}
        loading={metricsLoading}
        error={metricsError}
      />
    </section>
  );
}
