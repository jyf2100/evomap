import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { api } from '../api/client';

export function Capsules() {
  const { data: capsules, isLoading } = useQuery({
    queryKey: ['capsules'],
    queryFn: () => api.getCapsules(0, 100),
  });

  if (isLoading) return <p>Loading...</p>;

  return (
    <div>
      <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1.5rem' }}>Capsules</h1>

      {capsules && capsules.length > 0 ? (
        <div style={{ display: 'grid', gap: '1rem' }}>
          {capsules.map(capsule => (
            <Link
              key={capsule.id}
              to={`/capsules/${capsule.id}`}
              style={{
                display: 'block',
                padding: '1rem',
                background: 'white',
                borderRadius: '0.5rem',
                border: '1px solid #e2e8f0',
                textDecoration: 'none',
                color: 'inherit',
              }}
            >
              <h3 style={{ fontSize: '1rem', fontWeight: '600', margin: 0 }}>
                {capsule.name}
              </h3>
              {capsule.description && (
                <p style={{ fontSize: '0.875rem', color: '#64748b', marginTop: '0.5rem', margin: 0 }}>
                  {capsule.description}
                </p>
              )}
              <div style={{ display: 'flex', gap: '1rem', marginTop: '0.75rem', fontSize: '0.875rem', color: '#64748b' }}>
                <span>{capsule.gene_ids.length} genes</span>
                {capsule.execution_time_ms && <span>{capsule.execution_time_ms}ms</span>}
              </div>
            </Link>
          ))}
        </div>
      ) : (
        <p style={{ color: '#64748b' }}>No capsules found.</p>
      )}
    </div>
  );
}
