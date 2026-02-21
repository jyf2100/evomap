import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../api/client';

export function GeneDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: gene, isLoading } = useQuery({
    queryKey: ['gene', id],
    queryFn: () => api.getGene(id!),
    enabled: !!id,
  });

  const deleteMutation = useMutation({
    mutationFn: () => api.deleteGene(id!),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['genes'] });
      navigate('/genes');
    },
  });

  const updateMutation = useMutation({
    mutationFn: (status: string) => api.updateGene(id!, { status }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['gene', id] });
    },
  });

  if (isLoading) return <p>Loading...</p>;
  if (!gene) return <p>Gene not found</p>;

  return (
    <div>
      <button
        onClick={() => navigate('/genes')}
        style={{
          marginBottom: '1rem',
          padding: '0.5rem 1rem',
          background: '#f1f5f9',
          border: 'none',
          borderRadius: '0.375rem',
          cursor: 'pointer',
        }}
      >
        ← Back to Genes
      </button>

      <div style={{
        background: 'white',
        padding: '1.5rem',
        borderRadius: '0.5rem',
        border: '1px solid #e2e8f0',
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '1rem' }}>
          <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', margin: 0 }}>{gene.name}</h1>
          <span style={{
            padding: '0.25rem 0.75rem',
            borderRadius: '9999px',
            fontSize: '0.875rem',
            fontWeight: '500',
            background: gene.status === 'validated' ? '#22c55e' :
              gene.status === 'deprecated' ? '#ef4444' : '#94a3b8',
            color: 'white',
          }}>
            {gene.status}
          </span>
        </div>

        {gene.description && (
          <p style={{ color: '#64748b', marginBottom: '1.5rem' }}>{gene.description}</p>
        )}

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
          <div>
            <h3 style={{ fontSize: '1rem', fontWeight: '600', marginBottom: '0.5rem' }}>Success Rate</h3>
            <div style={{
              height: '8px',
              background: '#e2e8f0',
              borderRadius: '4px',
              overflow: 'hidden',
            }}>
              <div style={{
                width: `${gene.success_rate * 100}%`,
                height: '100%',
                background: '#22c55e',
              }} />
            </div>
            <p style={{ fontSize: '0.875rem', color: '#64748b', marginTop: '0.25rem' }}>
              {(gene.success_rate * 100).toFixed(1)}%
            </p>
          </div>

          <div>
            <h3 style={{ fontSize: '1rem', fontWeight: '600', marginBottom: '0.5rem' }}>Context Tags</h3>
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              {gene.context_tags.map(tag => (
                <span key={tag} style={{
                  padding: '0.25rem 0.75rem',
                  background: '#f1f5f9',
                  borderRadius: '0.25rem',
                  fontSize: '0.875rem',
                }}>
                  {tag}
                </span>
              ))}
            </div>
          </div>
        </div>

        {gene.implementation && (
          <div style={{ marginTop: '1.5rem' }}>
            <h3 style={{ fontSize: '1rem', fontWeight: '600', marginBottom: '0.5rem' }}>Implementation</h3>
            <pre style={{
              padding: '1rem',
              background: '#1e293b',
              color: '#e2e8f0',
              borderRadius: '0.5rem',
              overflow: 'auto',
              fontSize: '0.875rem',
            }}>
              {gene.implementation}
            </pre>
          </div>
        )}

        <div style={{ marginTop: '1.5rem', display: 'flex', gap: '0.5rem' }}>
          {gene.status !== 'validated' && (
            <button
              onClick={() => updateMutation.mutate('validated')}
              style={{
                padding: '0.5rem 1rem',
                background: '#22c55e',
                color: 'white',
                border: 'none',
                borderRadius: '0.375rem',
                cursor: 'pointer',
              }}
            >
              Validate
            </button>
          )}
          {gene.status !== 'deprecated' && (
            <button
              onClick={() => updateMutation.mutate('deprecated')}
              style={{
                padding: '0.5rem 1rem',
                background: '#f59e0b',
                color: 'white',
                border: 'none',
                borderRadius: '0.375rem',
                cursor: 'pointer',
              }}
            >
              Deprecate
            </button>
          )}
          <button
            onClick={() => deleteMutation.mutate()}
            style={{
              padding: '0.5rem 1rem',
              background: '#ef4444',
              color: 'white',
              border: 'none',
              borderRadius: '0.375rem',
              cursor: 'pointer',
            }}
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}
