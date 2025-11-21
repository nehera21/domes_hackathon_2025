/**
 * ProjectList component - displays a list of projects from the API
 */
import { useState, useEffect } from 'react';
import { projectApi } from '@/services/api';
import type { Project } from '@/models/project';

export default function ProjectList() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await projectApi.getAll();
      setProjects(data);
    } catch (err) {
      setError('Failed to load projects. Make sure the backend is running.');
      console.error('Error loading projects:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading projects...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error">
        <p>{error}</p>
        <button onClick={loadProjects}>Retry</button>
      </div>
    );
  }

  return (
    <div className="project-list">
      <h2>Projects</h2>
      <div className="list-container">
        {projects.length === 0 ? (
          <p>No projects found.</p>
        ) : (
          <div className="grid">
            {projects.map((project) => (
              <div key={project.id} className="card">
                <div className="card-header">
                  <h3>{project.name}</h3>
                  <span className={`badge ${project.status}`}>{project.status}</span>
                </div>
                <div className="card-body">
                  <p className="description">
                    {project.description || 'No description provided'}
                  </p>
                  <p className="meta">
                    <span>Owner ID: {project.owner_id}</span>
                    <span className="date">
                      Updated: {new Date(project.updated_at).toLocaleDateString()}
                    </span>
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

