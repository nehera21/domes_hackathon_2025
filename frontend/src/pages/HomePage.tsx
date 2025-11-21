/**
 * HomePage - main landing page
 */
import { Link } from 'react-router-dom';

export default function HomePage() {
  return (
    <div className="home-page">
      <div className="hero">
        <h1>🚀 Hackathon Project</h1>
        <p className="tagline">
          A fullstack ML application template with React + FastAPI + PostgreSQL
        </p>
      </div>

      <div className="features">
        <div className="feature-card">
          <h2>⚡ Fast Backend</h2>
          <p>Built with FastAPI for high-performance async operations</p>
        </div>
        <div className="feature-card">
          <h2>⚛️ Modern Frontend</h2>
          <p>React with TypeScript for type-safe development</p>
        </div>
        <div className="feature-card">
          <h2>🗄️ PostgreSQL Ready</h2>
          <p>Database connection setup with asyncpg</p>
        </div>
      </div>

      <div className="cta-section">
        <h2>Explore the Data</h2>
        <div className="button-group">
          <Link to="/users" className="btn btn-primary">
            View Users
          </Link>
          <Link to="/projects" className="btn btn-secondary">
            View Projects
          </Link>
        </div>
      </div>

      <div className="info-section">
        <h3>Getting Started</h3>
        <ol>
          <li>Install backend dependencies: <code>cd backend && uv sync</code></li>
          <li>Install frontend dependencies: <code>cd frontend && npm install</code></li>
          <li>Start the backend: <code>cd backend && uv run python -m backend.main</code></li>
          <li>Start the frontend: <code>cd frontend && npm run dev</code></li>
        </ol>
      </div>
    </div>
  );
}

