import React, { useEffect, useState, useRef } from 'react';
import ForceGraph3D from 'react-force-graph-3d';
import { Share2 } from 'lucide-react';

const GraphView = () => {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const fgRef = useRef();

  useEffect(() => {
    // Fetch the topology from our new Backend API
    fetch('http://localhost:8000/api/graph/topology')
      .then(res => res.json())
      .then(data => setGraphData(data))
      .catch(err => console.error("Graph Load Error:", err));
  }, []);

  return (
    <div className="h-full w-full bg-midnight-950 relative overflow-hidden">
      
      {/* Overlay Header */}
      <div className="absolute top-6 left-8 z-10 pointer-events-none">
        <h1 className="text-2xl font-semibold text-white tracking-tight flex items-center gap-3">
          <Share2 className="text-accent-blue" /> Network Topology
        </h1>
        <p className="text-sm text-gray-500 mt-1 font-mono">
          {graphData.nodes.length} Active Nodes • {graphData.links.length} Causal Links
        </p>
      </div>

      {/* The 3D Canvas */}
      <div className="absolute inset-0">
        <ForceGraph3D
          ref={fgRef}
          graphData={graphData}
          backgroundColor="#020408" // midnight-950
          
          // --- NODES ---
          nodeLabel="label"
          nodeColor={node => node.group === 'Macro' ? '#d97706' : '#3b82f6'} // Gold vs Blue
          nodeVal="val"
          nodeOpacity={0.9}
          nodeResolution={16}
          
          // --- LINKS ---
          linkColor={() => 'rgba(30, 36, 51, 0.8)'} // Subtle grey lines
          linkWidth={1}
          linkDirectionalParticles={2} // Little dots flowing on lines
          linkDirectionalParticleWidth={2}
          linkDirectionalParticleSpeed={0.005}
          
          // --- CAMERA ---
          showNavInfo={false}
          onEngineStop={() => fgRef.current.zoomToFit(400)} // Auto-center
        />
      </div>
    </div>
  );
};

export default GraphView;