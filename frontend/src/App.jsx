import { useState } from "react";
import axios from "axios";

const API_URL = " https://ai-idea-validator-1-z2b9.onrender.com";

function App() {
  const [token, setToken] = useState(null);
  const [isRegister, setIsRegister] = useState(false);

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [projects, setProjects] = useState([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [industry, setIndustry] = useState("");

  const [activeReport, setActiveReport] = useState(null);
  const [loadingAnalyze, setLoadingAnalyze] = useState(false);
  const [error, setError] = useState("");

  // ---- AUTH ----
  const handleRegister = async () => {
    setError("");
    try {
      await axios.post(`${API_URL}/auth/register`, { name, email, password });
      setIsRegister(false);
      alert("Registered! Now login.");
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed");
    }
  };

  const handleLogin = async () => {
    setError("");
    try {
      const form = new URLSearchParams();
      form.append("username", email);
      form.append("password", password);

      const res = await axios.post(`${API_URL}/auth/login`, form, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });
      setToken(res.data.access_token);
      fetchProjects(res.data.access_token);
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed");
    }
  };

  const handleLogout = () => {
    setToken(null);
    setProjects([]);
    setActiveReport(null);
  };

  // ---- PROJECTS ----
  const fetchProjects = async (authToken) => {
    try {
      const res = await axios.get(`${API_URL}/projects/`, {
        headers: { Authorization: `Bearer ${authToken || token}` },
      });
      setProjects(res.data);
    } catch (err) {
      setError("Could not fetch projects");
    }
  };

  const handleCreateProject = async () => {
    setError("");
    try {
      await axios.post(
        `${API_URL}/projects/`,
        { title, description, industry },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setTitle("");
      setDescription("");
      setIndustry("");
      fetchProjects();
    } catch (err) {
      setError(err.response?.data?.detail || "Could not create project");
    }
  };

  const handleAnalyze = async (projectId) => {
    setLoadingAnalyze(true);
    setError("");
    try {
      const res = await axios.post(
        `${API_URL}/projects/${projectId}/analyze`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setActiveReport(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Analysis failed");
    } finally {
      setLoadingAnalyze(false);
    }
  };

  const handleDelete = async (projectId) => {
    try {
      await axios.delete(`${API_URL}/projects/${projectId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchProjects();
      setActiveReport(null);
    } catch (err) {
      setError("Could not delete project");
    }
  };

  // ---- UI ----
  if (!token) {
    return (
      <div style={{ maxWidth: 400, margin: "60px auto", fontFamily: "sans-serif" }}>
        <h2>VentureLens AI</h2>
        <h3>{isRegister ? "Register" : "Login"}</h3>
        {error && <p style={{ color: "red" }}>{error}</p>}

        {isRegister && (
          <input placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} style={inputStyle} />
        )}
        <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} style={inputStyle} />
        <input
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={inputStyle}
        />

        <button onClick={isRegister ? handleRegister : handleLogin} style={btnStyle}>
          {isRegister ? "Register" : "Login"}
        </button>

        <p style={{ cursor: "pointer", color: "blue" }} onClick={() => setIsRegister(!isRegister)}>
          {isRegister ? "Already have an account? Login" : "New here? Register"}
        </p>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: 700, margin: "30px auto", fontFamily: "sans-serif" }}>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <h2>VentureLens AI</h2>
        <button onClick={handleLogout}>Logout</button>
      </div>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <h3>New Startup Idea</h3>
      <input placeholder="Title" value={title} onChange={(e) => setTitle(e.target.value)} style={inputStyle} />
      <textarea
        placeholder="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        style={{ ...inputStyle, height: 80 }}
      />
      <input
        placeholder="Industry (optional)"
        value={industry}
        onChange={(e) => setIndustry(e.target.value)}
        style={inputStyle}
      />
      <button onClick={handleCreateProject} style={btnStyle}>
        Create Project
      </button>

      <h3>Your Projects</h3>
      {projects.length === 0 && <p>No projects yet.</p>}
      {projects.map((p) => (
        <div key={p.id} style={cardStyle}>
          <strong>{p.title}</strong> <span style={{ color: "#666" }}>({p.industry || "N/A"})</span>
          <p>{p.description}</p>
          <button onClick={() => handleAnalyze(p.id)} disabled={loadingAnalyze}>
            {loadingAnalyze ? "Analyzing..." : "Analyze"}
          </button>
          <button onClick={() => handleDelete(p.id)} style={{ marginLeft: 8, color: "red" }}>
            Delete
          </button>
        </div>
      ))}

      {activeReport && (
        <div style={{ ...cardStyle, background: "#f5f5f5" }}>
          <h3>Report</h3>
          <p><b>Summary:</b> {activeReport.summary}</p>
          <p><b>Success Score:</b> {activeReport.success_score}/10</p>
          <p><b>Revenue Model:</b> {activeReport.revenue_model}</p>

          <b>Competitors:</b>
          <ul>{activeReport.competitors?.map((c, i) => <li key={i}>{c}</li>)}</ul>

          <b>Features:</b>
          <ul>{activeReport.features?.map((f, i) => <li key={i}>{f}</li>)}</ul>

          <b>Risks:</b>
          <ul>{activeReport.risks?.map((r, i) => <li key={i}>{r}</li>)}</ul>

          <b>Roadmap:</b>
          <ul>{activeReport.roadmap?.map((r, i) => <li key={i}>{r}</li>)}</ul>
        </div>
      )}
    </div>
  );
}

const inputStyle = {
  display: "block",
  width: "100%",
  padding: 8,
  margin: "8px 0",
  boxSizing: "border-box",
};

const btnStyle = {
  padding: "8px 16px",
  marginTop: 8,
  cursor: "pointer",
};

const cardStyle = {
  border: "1px solid #ddd",
  borderRadius: 8,
  padding: 12,
  margin: "12px 0",
};

export default App;