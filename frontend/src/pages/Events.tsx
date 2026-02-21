import { useQuery } from '@tanstack/react-query';
import { api } from '../api/client';

export function Events() {
  const { data: events, isLoading } = useQuery({
    queryKey: ['events'],
    queryFn: () => api.getEvents(0, 100),
  });

  const eventTypeColors: Record<string, string> = {
    mutation: '#fef3c7',
    repair: '#fee2e2',
    validation: '#d1fae5',
    creation: '#e0e7ff',
    deprecation: '#f3e8ff',
    execution: '#fef9c3',
  };

  if (isLoading) return <p>Loading...</p>;

  return (
    <div>
      <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1.5rem' }}>Events</h1>

      {events && events.length > 0 ? (
        <div style={{
          background: 'white',
          borderRadius: '0.5rem',
          border: '1px solid #e2e8f0',
          overflow: 'hidden',
        }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: '#f8fafc', borderBottom: '1px solid #e2e8f0' }}>
                <th style={{ padding: '0.75rem 1rem', textAlign: 'left', fontSize: '0.875rem', fontWeight: '500' }}>Type</th>
                <th style={{ padding: '0.75rem 1rem', textAlign: 'left', fontSize: '0.875rem', fontWeight: '500' }}>Description</th>
                <th style={{ padding: '0.75rem 1rem', textAlign: 'left', fontSize: '0.875rem', fontWeight: '500' }}>Time</th>
              </tr>
            </thead>
            <tbody>
              {events.map(event => (
                <tr key={event.id} style={{ borderBottom: '1px solid #f1f5f9' }}>
                  <td style={{ padding: '0.75rem 1rem' }}>
                    <span style={{
                      padding: '0.25rem 0.75rem',
                      borderRadius: '0.25rem',
                      fontSize: '0.75rem',
                      fontWeight: '500',
                      background: eventTypeColors[event.event_type] || '#f1f5f9',
                    }}>
                      {event.event_type}
                    </span>
                  </td>
                  <td style={{ padding: '0.75rem 1rem', fontSize: '0.875rem' }}>
                    {event.description || '-'}
                  </td>
                  <td style={{ padding: '0.75rem 1rem', fontSize: '0.875rem', color: '#64748b' }}>
                    {new Date(event.created_at).toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p style={{ color: '#64748b' }}>No events recorded yet.</p>
      )}
    </div>
  );
}
