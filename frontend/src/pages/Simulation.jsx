import React, { useState } from 'react';
import { Play, Activity, AlertTriangle, TrendingUp, TrendingDown } from 'lucide-react';

const MACRO_FACTORS = [
  { id: 'CRUDE_OIL', name: 'Brent Crude Oil' },
  { id: 'USD_INR', name: 'USD/INR Exchange Rate' },
  { id: 'REPO_RATE', name: 'RBI Repo Rate' },
  { id: 'CPI_INFLATION', name: 'CPI Inflation' },
  { id: 'US_10Y', name: 'US 10Y Treasury Yield' },
];

const Simulation = () => {
  const [selectedMacro, setSelectedMacro] = useState(MACRO_FACTORS[0].id);
  const [magnitude, setMagnitude] = useState(0.10); // Default 10%
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

  const runSimulation = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/sim/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          target_node: selectedMacro, 
          magnitude: parseFloat(magnitude) 
        }),
      });
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error("Simulation Failed:", error);
      alert("Simulation Engine Offline. Check Backend.");
    }
    setLoading(false);
  };

  return (
    <div className="p-8 bg-midnight-950 min-h-screen font-sans ml-[260px] text-gray-300">
      
      {/* Header */}
      <div className="mb-8 border-b border-midnight-700 pb-4">
        <h1 className="text-2xl font-semibold text-white tracking-tight flex items-center gap-3">
          <Activity className="text-accent-rose" /> Simulation Engine
        </h1>
        <p className="text-sm text-gray-500 mt-1 font-mono">
          Causal Inference Protocol • Stress Test Scenarios
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* --- CONTROL DECK (Left Panel) --- */}
        <div className="bg-midnight-900 border border-midnight-700 rounded-lg p-6 h-fit">
          <h3 className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-6">Scenario Configuration</h3>
          
          {/* Factor Selection */}
          <div className="mb-6">
            <label className="block text-sm text-gray-400 mb-2">Trigger Event</label>
            <select 
              value={selectedMacro}
              onChange={(e) => setSelectedMacro(e.target.value)}
              className="w-full bg-midnight-950 border border-midnight-700 text-white p-3 rounded focus:border-accent-blue focus:outline-none transition-colors"
            >
              {MACRO_FACTORS.map(f => (
                <option key={f.id} value={f.id}>{f.name}</option>
              ))}
            </select>
          </div>

          {/* Magnitude Slider */}
          <div className="mb-8">
            <div className="flex justify-between mb-2">
              <label className="text-sm text-gray-400">Shock Magnitude</label>
              <span className={`font-mono font-bold ${magnitude > 0 ? 'text-accent-rose' : 'text-accent-teal'}`}>
                {magnitude > 0 ? '+' : ''}{(magnitude * 100).toFixed(0)}%
              </span>
            </div>
            <input 
              type="range" 
              min="-0.5" max="0.5" step="0.05"
              value={magnitude}
              onChange={(e) => setMagnitude(e.target.value)}
              className="w-full h-2 bg-midnight-700 rounded-lg appearance-none cursor-pointer accent-accent-blue"
            />
            <div className="flex justify-between text-[10px] text-gray-600 mt-1 font-mono">
              <span>-50%</span>
              <span>0%</span>
              <span>+50%</span>
            </div>
          </div>

          {/* Launch Button */}
          <button 
            onClick={runSimulation}
            disabled={loading}
            className={`w-full py-4 rounded font-bold tracking-wide flex items-center justify-center gap-2 transition-all ${
              loading 
                ? 'bg-midnight-800 text-gray-500 cursor-not-allowed' 
                : 'bg-accent-blue hover:bg-blue-600 text-white shadow-glow'
            }`}
          >
            {loading ? 'CALCULATING...' : <><Play size={18} fill="currentColor" /> RUN SCENARIO</>}
          </button>
        </div>

        {/* --- RESULTS FEED (Right Panel) --- */}
        <div className="lg:col-span-2">
          {!results ? (
            <div className="h-full flex flex-col items-center justify-center text-gray-600 border border-dashed border-midnight-700 rounded-lg min-h-[400px]">
              <Activity size={48} className="mb-4 opacity-20" />
              <p>Ready to simulate.</p>
              <p className="text-sm">Select a trigger to analyze propagation.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {/* Summary Card */}
              <div className="bg-midnight-900 border border-midnight-700 p-4 rounded-lg flex items-center justify-between">
                <div>
                  <h3 className="text-white font-bold">{results.source} Shock</h3>
                  <p className="text-sm text-gray-400">Initial Intensity: {(results.initial_shock * 100).toFixed(0)}%</p>
                </div>
                <div className="text-right">
                  <span className="text-2xl font-mono text-white block">{results.affected_count}</span>
                  <span className="text-xs text-gray-500 uppercase">Nodes Impacted</span>
                </div>
              </div>

              {/* Impact List */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {results.impacts.map((node, i) => (
                  <div key={i} className="bg-midnight-900/50 border border-midnight-700 p-3 rounded flex justify-between items-center hover:bg-midnight-800 transition-colors">
                    <div className="flex items-center gap-3">
                      <div className={`w-1 h-8 rounded-full ${node.impact < 0 ? 'bg-accent-rose' : 'bg-accent-teal'}`} />
                      <div>
                        <p className="font-bold text-gray-200 text-sm">{node.node}</p>
                        <p className="text-xs text-gray-500">via {node.source}</p>
                      </div>
                    </div>
                    <div className={`flex items-center gap-1 font-mono font-bold ${node.impact < 0 ? 'text-accent-rose' : 'text-accent-teal'}`}>
                      {node.impact < 0 ? <TrendingDown size={16} /> : <TrendingUp size={16} />}
                      {(node.impact * 100).toFixed(2)}%
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

      </div>
    </div>
  );
};

export default Simulation;