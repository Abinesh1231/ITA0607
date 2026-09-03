import { NavLink } from "react-router-dom";

const links = [
  ["/", "Dashboard"], ["/analysis", "Waste Analysis"], ["/detection", "Detection"],
  ["/valuation", "Valuation"], ["/history", "History"], ["/about", "About"]
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <h2>♻️ CEI</h2>
      <p className="muted">Waste Intelligence</p>
      <nav>{links.map(([to, label]) => (
        <NavLink key={to} to={to} className={({isActive}) => isActive ? "nav active" : "nav"}>
          {label}
        </NavLink>
      ))}</nav>
    </aside>
  );
}
