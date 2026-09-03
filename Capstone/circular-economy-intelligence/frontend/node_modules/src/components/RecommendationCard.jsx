export default function RecommendationCard({ data }) {
  if (!data) return null;
  return <div className="card"><h3>Recommendation</h3><strong>{data.action}</strong><p>{data.detail}</p></div>;
}
