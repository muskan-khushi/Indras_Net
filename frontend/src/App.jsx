import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Simulation from './pages/Simulation'; 
import GraphView from './pages/GraphView'; 
import Intel from './pages/Intel'; 


function App() {
  return (
    <Router>
      {/* 1. WRAPPER: Fixed to screen height (h-screen) & hides window scrollbar */}
      <div className="flex h-screen bg-midnight-950 text-white overflow-hidden">
        
        <Sidebar />
        
        {/* 2. MAIN CONTENT: 
            - ml-[260px]: Pushes content right to respect the Fixed Sidebar
            - h-full: Takes full height of screen
            - overflow-y-auto: SCROLLS only this area 
        */}
        <main className="flex-1 ml-[260px] h-full overflow-y-auto relative">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            
            {/* 👇 THIS loads the real 3D Graph now */}
            <Route path="/graph" element={<GraphView />} /> 
            
            {/* 👇 Fixed: Only ONE route for Oracle/Simulation */}
            <Route path="/oracle" element={<Simulation />} />
            
            <Route path="/intel" element={<Intel />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;