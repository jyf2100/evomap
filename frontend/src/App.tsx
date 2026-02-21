import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Layout } from './components/Layout';
import { Dashboard } from './pages/Dashboard';
import { Genes } from './pages/Genes';
import { GeneDetail } from './pages/GeneDetail';
import { Capsules } from './pages/Capsules';
import { CapsuleDetail } from './pages/CapsuleDetail';
import { Events } from './pages/Events';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="genes" element={<Genes />} />
            <Route path="genes/:id" element={<GeneDetail />} />
            <Route path="capsules" element={<Capsules />} />
            <Route path="capsules/:id" element={<CapsuleDetail />} />
            <Route path="events" element={<Events />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
