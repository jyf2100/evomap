import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api, type Gene } from '../api/client';
import { GeneCard } from '../components/GeneCard';

export function Genes() {
  const queryClient = useQueryClient();
  const [showForm, setShowForm] = useState(false);
  const [newGene, setNewGene] = useState({ name: '', description: '' });

  const { data: genes, isLoading } = useQuery({
    queryKey: ['genes'],
    queryFn: () => api.getGenes(0, 100),
  });

  const createMutation = useMutation({
    mutationFn: (data: Partial<Gene>) => api.createGene(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['genes'] });
      setShowForm(false);
      setNewGene({ name: '', description: '' });
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createMutation.mutate(newGene);
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', margin: 0 }}>Genes</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          style={{
            padding: '0.5rem 1rem',
            background: '#3b82f6',
            color: 'white',
            border: 'none',
            borderRadius: '0.375rem',
            cursor: 'pointer',
          }}
        >
          {showForm ? 'Cancel' : 'New Gene'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} style={{
          background: 'white',
          padding: '1.5rem',
          borderRadius: '0.5rem',
          border: '1px solid #e2e8f0',
          marginBottom: '1.5rem',
        }}>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '500', marginBottom: '0.5rem' }}>
              Name
            </label>
            <input
              type="text"
              value={newGene.name}
              onChange={e => setNewGene({ ...newGene, name: e.target.value })}
              style={{
                width: '100%',
                padding: '0.5rem',
                border: '1px solid #e2e8f0',
                borderRadius: '0.375rem',
              }}
              required
            />
          </div>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '500', marginBottom: '0.5rem' }}>
              Description
            </label>
            <textarea
              value={newGene.description}
              onChange={e => setNewGene({ ...newGene, description: e.target.value })}
              style={{
                width: '100%',
                padding: '0.5rem',
                border: '1px solid #e2e8f0',
                borderRadius: '0.375rem',
                minHeight: '80px',
              }}
            />
          </div>
          <button
            type="submit"
            disabled={createMutation.isPending}
            style={{
              padding: '0.5rem 1rem',
              background: '#22c55e',
              color: 'white',
              border: 'none',
              borderRadius: '0.375rem',
              cursor: createMutation.isPending ? 'wait' : 'pointer',
            }}
          >
            {createMutation.isPending ? 'Creating...' : 'Create Gene'}
          </button>
        </form>
      )}

      {isLoading ? (
        <p>Loading...</p>
      ) : genes && genes.length > 0 ? (
        <div style={{ display: 'grid', gap: '1rem' }}>
          {genes.map(gene => (
            <GeneCard key={gene.id} gene={gene} />
          ))}
        </div>
      ) : (
        <p style={{ color: '#64748b' }}>No genes found. Create one to get started!</p>
      )}
    </div>
  );
}
