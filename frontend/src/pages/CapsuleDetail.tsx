import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { api } from '../api/client';

export function CapsuleDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { data: capsule, isLoading } = useQuery({
    queryKey: ['capsule', id],
    queryFn: () => api.getCapsule(id!),
    enabled: !!id,
  });

  const { data: genes } = useQuery({
    queryKey: ['genes'],
    queryFn: () => api.getGenes(0, 100),
  });

  if (isLoading) return <p>Loading...</p>;
  if (!capsule) return <p>Capsule not found</p>;

  const capsuleGenes = genes?.filter(g => capsule.gene_ids.includes(g.id)) || [];

  return (
    <div>
      <button
        onClick={() => navigate('/capsules')}
        style={{
          marginBottom: '1rem',
          padding: '0.5rem 1rem',
          background: '#f1f5f9',
          border: 'none',
          borderRadius: '0.375rem',
          cursor: 'pointer',
        }}
      >
        ← Back to Capsules
      </button>

      <div style={{
        background: 'white',
        padding: '1.5rem',
        borderRadius: '0.5rem',
        border: '1px solid #e2e8f0',
      }}>
        <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '0.5rem' }}>
          {capsule.name}
        </h1>

        {capsule.description && (
          <p style={{ color: '#64748b', marginBottom: '1.5rem' }}>{capsule.description}</p>
        )}

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '1.5rem' }}>
          {capsule.input_schema && (
            <div>
              <h3 style={{ fontSize: '1rem', fontWeight: '600', marginBottom: '0.5rem' }}>Input Schema</h3>
              <pre style={{
                padding: '1rem',
                background: '#f8fafc',
                borderRadius: '0.5rem',
                fontSize: '0.875rem',
                overflow: 'auto',
              }}>
                {JSON.stringify(capsule.input_schema, null, 2)}
              </pre>
            </div>
          )}

          {capsule.output_schema && (
            <div>
              <h3 style={{ fontSize: '1rem', fontWeight: '600', marginBottom: '0.5rem' }}>Output Schema</h3>
              <pre style={{
                padding: '1rem',
                background: '#f8fafc',
                borderRadius: '0.5rem',
                fontSize: '0.875rem',
                overflow: 'auto',
              }}>
                {JSON.stringify(capsule.output_schema, null, 2)}
              </pre>
            </div>
          )}
        </div>

        <div>
          <h3 style={{ fontSize: '1rem', fontWeight: '600', marginBottom: '0.5rem' }}>
            Genes ({capsuleGenes.length})
          </h3>
          {capsuleGenes.length > 0 ? (
            <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
              {capsuleGenes.map(gene => (
                <li key={gene.id} style={{
                  padding: '0.75rem',
                  background: '#f8fafc',
                  borderRadius: '0.375rem',
                  marginBottom: '0.5rem',
                }}>
                  <span style={{ fontWeight: '500' }}>{gene.name}</span>
                  <span style={{ marginLeft: '0.5rem', color: '#64748b', fontSize: '0.875rem' }}>
                    ({gene.status})
                  </span>
                </li>
              ))}
            </ul>
          ) : (
            <p style={{ color: '#64748b' }}>No genes associated</p>
          )}
        </div>
      </div>
    </div>
  );
}
