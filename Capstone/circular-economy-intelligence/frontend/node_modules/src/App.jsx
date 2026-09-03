import { useState } from "react";
import { Routes, Route, Link } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import WasteAnalysis from "./pages/WasteAnalysis";
import Detection from "./pages/Detection";
import Valuation from "./pages/Valuation";
import History from "./pages/History";
import About from "./pages/About";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Sidebar from "./components/Sidebar";

export default function App() {
  const [user, setUser] = useState(null);
  return (
    <div className="app-shell">
      <Sidebar />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/analysis" element={<WasteAnalysis />} />
          <Route path="/detection" element={<Detection />} />
          <Route path="/valuation" element={<Valuation />} />
          <Route path="/history" element={<History />} />
          <Route path="/about" element={<About />} />
          <Route path="/login" element={<Login onLogin={setUser} />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </main>
    </div>
  );
}
