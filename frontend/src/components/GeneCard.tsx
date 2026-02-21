import { Link } from 'react-router-dom';
import type { Gene } from '../api/client';

interface GeneCardProps {
  gene: Gene;
}

export function GeneCard({ gene }: GeneCardProps) {
  const statusColors: Record<string, string> = {
    draft: '#94a3b8',
    validated: '#22c55e',
    deprecated: '#ef4444',
  };

  return (
    <Link
      to={`/genes/${gene.id}`}
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
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h3 style={{ fontSize: '1rem', fontWeight: '600', margin: 0 }}>
          {gene.name}
        </h3>
        <span style={{
          padding: '0.25rem 0.75rem',
          borderRadius: '9999px',
          fontSize: '0.75rem',
          fontWeight: '500',
          background: statusColors[gene.status] || '#94a3b8',
          color: 'white',
        }}>
          {gene.status}
        </span>
      </div>
      {gene.description && (
        <p style={{ fontSize: '0.875rem', color: '#64748b', marginTop: '0.5rem', margin: 0 }}>
          {gene.description}
        </p>
      )}
      <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.75rem' }}>
        {gene.context_tags.slice(0, 3).map(tag => (
          <span key={tag} style={{
            padding: '0.125rem 0.5rem',
            background: '#f1f5f9',
            borderRadius: '0.25rem',
            fontSize: '0.75rem',
          }}>
            {tag}
          </span>
        ))}
      </div>
    </Link>
  );
}
