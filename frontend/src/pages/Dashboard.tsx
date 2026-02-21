import { useQuery } from '@tanstack/react-query';
import { api } from '../api/client';

export function Dashboard() {
  const { data: genes } = useQuery({ queryKey: ['genes'], queryFn: () => api.getGenes(0, 100) });
  const { data: capsules } = useQuery({ queryKey: ['capsules'], queryFn: () => api.getCapsules(0, 100) });
  const { data: events } = useQuery({ queryKey: ['events'], queryFn: () => api.getEvents(0, 100) });

  const stats = [
    { label: 'Total Genes', value: genes?.length ?? 0, color: '#3b82f6' },
    { label: 'Validated', value: genes?.filter(g => g.status === 'validated').length ?? 0, color: '#22c55e' },
    { label: 'Capsules', value: capsules?.length ?? 0, color: '#8b5cf6' },
    { label: 'Events', value: events?.length ?? 0, color: '#f59e0b' },
  ];

  return (
    <div>
      <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1.5rem' }}>
        Dashboard
      </h1>

      {/* Stats Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '1rem',
        marginBottom: '2rem',
      }}>
        {stats.map(stat => (
          <div key={stat.label} style={{
            padding: '1.5rem',
            background: 'white',
            borderRadius: '0.5rem',
            border: '1px solid #e2e8f0',
          }}>
            <p style={{ fontSize: '0.875rem', color: '#64748b', margin: 0 }}>{stat.label}</p>
            <p style={{
              fontSize: '2rem',
              fontWeight: 'bold',
              color: stat.color,
              margin: '0.5rem 0 0 0',
            }}>
              {stat.value}
            </p>
          </div>
        ))}
      </div>

      {/* Recent Events */}
      <div style={{
        background: 'white',
        borderRadius: '0.5rem',
        border: '1px solid #e2e8f0',
        padding: '1.5rem',
      }}>
        <h2 style={{ fontSize: '1.125rem', fontWeight: '600', marginBottom: '1rem' }}>
          Recent Events
        </h2>
        {events && events.length > 0 ? (
          <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
            {events.slice(0, 5).map(event => (
              <li key={event.id} style={{
                padding: '0.75rem 0',
                borderBottom: '1px solid #f1f5f9',
                display: 'flex',
                justifyContent: 'space-between',
              }}>
                <span style={{
                  padding: '0.125rem 0.5rem',
                  background: event.event_type === 'mutation' ? '#fef3c7' :
                    event.event_type === 'validation' ? '#d1fae5' : '#e0e7ff',
                  borderRadius: '0.25rem',
                  fontSize: '0.75rem',
                  fontWeight: '500',
                }}>
                  {event.event_type}
                </span>
                <span style={{ fontSize: '0.875rem', color: '#64748b' }}>
                  {event.description || 'No description'}
                </span>
              </li>
            ))}
          </ul>
        ) : (
          <p style={{ color: '#64748b' }}>No events yet</p>
        )}
      </div>
    </div>
  );
}
