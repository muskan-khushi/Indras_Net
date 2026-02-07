import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';

// Placeholder Pages (To prevent crashes)
const GraphView = () => <div className="ml-[260px] p-8 text-white">Network Analysis Loading...</div>;
const Oracle = () => <div className="ml-[260px] p-8 text-white">Oracle Engine Loading...</div>;
const Intel = () => <div className="ml-[260px] p-8 text-white">Global Intel Loading...</div>;

function App() {
  return (
    <Router>
      <div className="flex min-h-screen bg-midnight-950 text-white">
        <Sidebar />
        <main className="flex-1 relative">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/graph" element={<GraphView />} />
            <Route path="/oracle" element={<Oracle />} />
            <Route path="/intel" element={<Intel />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;