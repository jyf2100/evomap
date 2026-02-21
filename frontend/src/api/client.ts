// API client for backend communication
const API_BASE = '/api/v1';

export interface Gene {
  id: string;
  name: string;
  description: string | null;
  implementation: string | null;
  prompt_template: string | null;
  status: string;
  success_rate: number;
  context_tags: string[];
  created_at: string;
  updated_at: string;
}

export interface Capsule {
  id: string;
  name: string;
  description: string | null;
  input_schema: Record<string, unknown> | null;
  output_schema: Record<string, unknown> | null;
  execution_time_ms: number | null;
  gene_ids: string[];
  created_at: string;
  updated_at: string;
}

export interface Event {
  id: string;
  capsule_id: string | null;
  event_type: string;
  description: string | null;
  payload: Record<string, unknown> | null;
  created_at: string;
}

async function fetchAPI<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`);
  }

  return response.json();
}

export const api = {
  // Genes
  getGenes: (skip = 0, limit = 100) =>
    fetchAPI<Gene[]>(`/genes?skip=${skip}&limit=${limit}`),

  getGene: (id: string) =>
    fetchAPI<Gene>(`/genes/${id}`),

  createGene: (data: Partial<Gene>) =>
    fetchAPI<Gene>('/genes', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  updateGene: (id: string, data: Partial<Gene>) =>
    fetchAPI<Gene>(`/genes/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  deleteGene: (id: string) =>
    fetchAPI<void>(`/genes/${id}`, { method: 'DELETE' }),

  // Capsules
  getCapsules: (skip = 0, limit = 100) =>
    fetchAPI<Capsule[]>(`/capsules?skip=${skip}&limit=${limit}`),

  getCapsule: (id: string) =>
    fetchAPI<Capsule>(`/capsules/${id}`),

  createCapsule: (data: Partial<Capsule>) =>
    fetchAPI<Capsule>('/capsules', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  // Events
  getEvents: (skip = 0, limit = 100) =>
    fetchAPI<Event[]>(`/events?skip=${skip}&limit=${limit}`),

  getEvent: (id: string) =>
    fetchAPI<Event>(`/events/${id}`),
};
