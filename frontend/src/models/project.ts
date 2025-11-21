/**
 * Project domain models
 */

export interface Project {
  id: number;
  name: string;
  description: string | null;
  status: 'active' | 'completed' | 'archived';
  owner_id: number;
  created_at: string;
  updated_at: string;
}

export interface ProjectCreate {
  name: string;
  description?: string;
  status?: 'active' | 'completed' | 'archived';
  owner_id: number;
}

export interface ProjectUpdate {
  name?: string;
  description?: string;
  status?: 'active' | 'completed' | 'archived';
}

