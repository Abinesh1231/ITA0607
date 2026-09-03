import { useState } from "react";

import ImageUpload from "../components/ImageUpload";
import ClassificationCard from "../components/ClassificationCard";
import RecommendationCard from "../components/RecommendationCard";
import ValuationCard from "../components/ValuationCard";
import Loading from "../components/Loading";

import { analyzeWaste } from "../services/api";

export default function WasteAnalysis() {
  const [file, setFile] = useState(null);

  const [weight, setWeight] = useState("");

  const [qualityFactor, setQualityFactor] = useState("1.0");

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  // ==========================================================
  // ANALYZE WASTE
  // ==========================================================

  async function analyze() {
    if (!file) {
      setError("Please select an image.");
      return;
    }

    if (!weight || Number(weight) <= 0) {
      setError("Please enter a valid weight greater than 0 kg.");
      return;
    }

    setError("");
    setLoading(true);
    setResult(null);

    try {
      const data = await analyzeWaste(
        file,
        Number(weight),
        Number(qualityFactor),
      );

      setResult(data);
    } catch (e) {
      console.error("Waste analysis failed:", e);

      setError(
        e?.response?.data?.detail || e?.message || "Waste analysis failed.",
      );
    } finally {
      setLoading(false);
    }
  }

  // ==========================================================
  // UI
  // ==========================================================

  return (
    <section>
      <h1>Waste Analysis</h1>

      <p>
        Upload a waste image to identify the material, estimate its recycling
        value, and receive a recycling recommendation.
      </p>

      {/* ======================================================
          IMAGE UPLOAD
      ====================================================== */}

      <ImageUpload
        onSelect={(selectedFile) => {
          setFile(selectedFile);
          setResult(null);
          setError("");
        }}
      />

      {/* ======================================================
          WEIGHT
      ====================================================== */}

      <div className="form-group">
        <label htmlFor="weight">Waste Weight (kg)</label>

        <input
          id="weight"
          type="number"
          min="0.01"
          step="0.01"
          placeholder="Example: 2"
          value={weight}
          onChange={(e) => setWeight(e.target.value)}
        />
      </div>

      {/* ======================================================
          QUALITY FACTOR
      ====================================================== */}

      <div className="form-group">
        <label htmlFor="qualityFactor">Quality Factor</label>

        <input
          id="qualityFactor"
          type="number"
          min="0"
          max="1.2"
          step="0.1"
          value={qualityFactor}
          onChange={(e) => setQualityFactor(e.target.value)}
        />

        <small>
          Enter a value between 0 and 1.2. 1.0 represents normal quality.
        </small>
      </div>

      {/* ======================================================
          ERROR
      ====================================================== */}

      {error && <div className="error-message">{error}</div>}

      {/* ======================================================
          ANALYZE BUTTON
      ====================================================== */}

      <button
        className="primary"
        onClick={analyze}
        disabled={!file || !weight || loading}
      >
        {loading ? "Analyzing..." : "Analyze Waste"}
      </button>

      {/* ======================================================
          LOADING
      ====================================================== */}

      {loading && <Loading />}

      {/* ======================================================
          RESULTS
      ====================================================== */}

      {result && !loading && (
        <div className="result-grid">
          <ClassificationCard data={result} />

          <RecommendationCard
            data={{
              material: result.material,
              action: result.recommendation,
              detail: result.recommendation_detail,
            }}
          />

          <ValuationCard
            data={{
              material: result.material,
              weight_kg: result.weight_kg,
              rate_per_kg: result.rate_per_kg,
              quality_factor: result.quality_factor,
              estimated_value: result.estimated_value,
              currency: result.currency,
            }}
          />
        </div>
      )}
    </section>
  );
}
