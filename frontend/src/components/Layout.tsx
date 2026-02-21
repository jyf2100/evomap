import { Link, Outlet, useLocation } from 'react-router-dom';

export function Layout() {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Dashboard' },
    { path: '/genes', label: 'Genes' },
    { path: '/capsules', label: 'Capsules' },
    { path: '/events', label: 'Events' },
  ];

  return (
    <div style={{ minHeight: '100vh', display: 'flex' }}>
      {/* Sidebar */}
      <nav style={{
        width: '220px',
        background: '#1e293b',
        color: 'white',
        padding: '1rem',
      }}>
        <h1 style={{ fontSize: '1.25rem', fontWeight: 'bold', marginBottom: '2rem' }}>
          EvoMap GEP
        </h1>
        <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
          {navItems.map(item => (
            <li key={item.path} style={{ marginBottom: '0.5rem' }}>
              <Link
                to={item.path}
                style={{
                  display: 'block',
                  padding: '0.75rem 1rem',
                  borderRadius: '0.5rem',
                  textDecoration: 'none',
                  color: location.pathname === item.path ? '#1e293b' : '#e2e8f0',
                  background: location.pathname === item.path ? '#f1f5f9' : 'transparent',
                }}
              >
                {item.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>

      {/* Main content */}
      <main style={{
        flex: 1,
        padding: '2rem',
        background: '#f8fafc',
        overflow: 'auto',
      }}>
        <Outlet />
      </main>
    </div>
  );
}
