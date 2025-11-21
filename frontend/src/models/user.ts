/**
 * User domain models
 */

export interface User {
  id: number;
  email: string;
  name: string;
  role: 'user' | 'admin' | 'researcher';
  is_active: boolean;
  created_at: string;
}

export interface UserCreate {
  email: string;
  name: string;
  role?: 'user' | 'admin' | 'researcher';
  password: string;
}

export interface UserUpdate {
  email?: string;
  name?: string;
  role?: 'user' | 'admin' | 'researcher';
}

