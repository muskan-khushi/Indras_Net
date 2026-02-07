import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutGrid, Network, BrainCircuit, Globe, LogOut } from 'lucide-react';

const Sidebar = () => {
  const links = [
    { name: 'Overview', icon: LayoutGrid, path: '/' },
    { name: 'Network Analysis', icon: Network, path: '/graph' },
    { name: 'Simulation Engine', icon: BrainCircuit, path: '/oracle' },
    { name: 'Global Intel', icon: Globe, path: '/intel' },
  ];

  return (
    <div className="h-screen w-[260px] bg-midnight-950 border-r border-midnight-700 flex flex-col fixed left-0 top-0 z-50">
      {/* Brand Header */}
      <div className="h-16 flex items-center px-6 border-b border-midnight-700 bg-midnight-950">
        <div className="w-5 h-5 bg-accent-blue rounded-sm mr-3 shadow-glow"></div>
        <div>
          <h1 className="text-sm font-bold text-gray-100 tracking-wide font-sans">INDRA SYSTEMS</h1>
          <p className="text-[10px] text-gray-500 uppercase tracking-wider">Causal Twin v1.0</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 py-6 px-3 space-y-1">
        <div className="px-3 mb-3 text-[10px] font-bold text-gray-600 uppercase tracking-widest">Modules</div>
        {links.map((link) => (
          <NavLink
            key={link.path}
            to={link.path}
            className={({ isActive }) =>
              `group flex items-center justify-between px-3 py-2.5 rounded-md text-sm transition-all duration-200 ${
                isActive 
                  ? 'bg-midnight-900 text-white border border-midnight-700 shadow-card' 
                  : 'text-gray-400 hover:text-gray-200 hover:bg-midnight-900/50'
              }`
            }
          >
            {({ isActive }) => (
              <div className="flex items-center gap-3">
                <link.icon size={18} strokeWidth={1.5} className={isActive ? 'text-accent-blue' : 'text-gray-500 group-hover:text-gray-300'} />
                <span className="font-medium">{link.name}</span>
              </div>
            )}
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-midnight-700">
        <button className="flex items-center gap-3 w-full px-3 py-2 text-sm text-gray-400 hover:text-accent-rose transition-colors">
          <LogOut size={16} />
          <span>Disconnect</span>
        </button>
      </div>
    </div>
  );
};

export default Sidebar;