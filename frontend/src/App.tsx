/**
 * Main App component with routing
 */
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import HomePage from '@/pages/HomePage';
import UsersPage from '@/pages/UsersPage';
import ProjectsPage from '@/pages/ProjectsPage';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <nav className="navbar">
          <div className="nav-container">
            <Link to="/" className="nav-logo">
              Hackathon
            </Link>
            <ul className="nav-menu">
              <li className="nav-item">
                <Link to="/" className="nav-link">
                  Home
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/users" className="nav-link">
                  Users
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/projects" className="nav-link">
                  Projects
                </Link>
              </li>
            </ul>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/users" element={<UsersPage />} />
            <Route path="/projects" element={<ProjectsPage />} />
          </Routes>
        </main>

        <footer className="footer">
          <p>&copy; 2025 Hackathon Project. Built with React + FastAPI</p>
        </footer>
      </div>
    </BrowserRouter>
  );
}

export default App;

