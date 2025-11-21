/**
 * API service for communicating with the backend
 */
import axios from 'axios';
import type { User, UserCreate } from '@/models/user';
import type { Project, ProjectCreate } from '@/models/project';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// User API
export const userApi = {
  /**
   * Get all users
   */
  async getAll(): Promise<User[]> {
    const response = await apiClient.get<User[]>('/api/v1/users');
    return response.data;
  },

  /**
   * Get a user by ID
   */
  async getById(id: number): Promise<User> {
    const response = await apiClient.get<User>(`/api/v1/users/${id}`);
    return response.data;
  },

  /**
   * Create a new user
   */
  async create(userData: UserCreate): Promise<User> {
    const response = await apiClient.post<User>('/api/v1/users', userData);
    return response.data;
  },

  /**
   * Delete a user
   */
  async delete(id: number): Promise<void> {
    await apiClient.delete(`/api/v1/users/${id}`);
  },
};

// Project API
export const projectApi = {
  /**
   * Get all projects
   */
  async getAll(): Promise<Project[]> {
    const response = await apiClient.get<Project[]>('/api/v1/projects');
    return response.data;
  },

  /**
   * Get a project by ID
   */
  async getById(id: number): Promise<Project> {
    const response = await apiClient.get<Project>(`/api/v1/projects/${id}`);
    return response.data;
  },

  /**
   * Get projects by owner
   */
  async getByOwner(ownerId: number): Promise<Project[]> {
    const response = await apiClient.get<Project[]>('/api/v1/projects', {
      params: { owner_id: ownerId },
    });
    return response.data;
  },

  /**
   * Create a new project
   */
  async create(projectData: ProjectCreate): Promise<Project> {
    const response = await apiClient.post<Project>('/api/v1/projects', projectData);
    return response.data;
  },

  /**
   * Delete a project
   */
  async delete(id: number): Promise<void> {
    await apiClient.delete(`/api/v1/projects/${id}`);
  },
};

export default apiClient;

