export default function WasteTable({ rows = [] }) {
  return <div className="card"><h3>Recent Analyses</h3>
    <table><thead><tr><th>Material</th><th>Confidence</th><th>Value</th></tr></thead>
    <tbody>{rows.map((r,i)=><tr key={i}><td>{r.material}</td><td>{r.confidence}</td><td>₹{r.value}</td></tr>)}</tbody></table>
  </div>;
}
