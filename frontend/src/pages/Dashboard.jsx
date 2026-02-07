import React from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { ArrowUpRight, ArrowDownRight, Activity } from 'lucide-react';

// Reusable "Pro" Card
const Card = ({ title, children, className = '' }) => (
  <div className={`bg-midnight-900 border border-midnight-700 rounded-lg p-5 flex flex-col ${className}`}>
    <div className="flex justify-between items-center mb-4">
      <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider font-mono">{title}</h3>
      <Activity size={14} className="text-midnight-700" />
    </div>
    {children}
  </div>
);

// Stat Widget
const Stat = ({ label, value, trend, isUp }) => (
  <div>
    <p className="text-sm text-gray-500 mb-1">{label}</p>
    <div className="flex items-baseline gap-3">
      <h2 className="text-2xl font-mono font-medium text-white">{value}</h2>
      <span className={`text-xs font-medium flex items-center ${isUp ? 'text-accent-teal' : 'text-accent-rose'}`}>
        {isUp ? <ArrowUpRight size={14} /> : <ArrowDownRight size={14} />}
        {trend}
      </span>
    </div>
  </div>
);

// Fake Data for Chart
const data = Array.from({ length: 20 }, (_, i) => ({
  time: i,
  val: 50 + Math.random() * 30
}));

const Dashboard = () => {
  return (
    <div className="p-8 bg-midnight-950 min-h-screen font-sans ml-[260px]">
      
      {/* Header */}
      <div className="flex justify-between items-end mb-8 border-b border-midnight-700 pb-4">
        <div>
          <h1 className="text-2xl font-semibold text-white tracking-tight">System Overview</h1>
          <p className="text-sm text-gray-500 mt-1 font-mono">Real-time inference engine • Latency: 42ms</p>
        </div>
        <div className="flex gap-3">
           <span className="px-3 py-1 bg-accent-teal/10 text-accent-teal text-xs font-medium rounded-full border border-accent-teal/20 flex items-center gap-2">
             <div className="w-1.5 h-1.5 rounded-full bg-accent-teal animate-pulse"/> ONLINE
           </span>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
        <Card><Stat label="Nifty 50 Index" value="24,142" trend="+1.2%" isUp={true} /></Card>
        <Card><Stat label="Macro Stress" value="High" trend="+5.4%" isUp={false} /></Card>
        <Card><Stat label="Active Nodes" value="42" trend="Stable" isUp={true} /></Card>
        <Card><Stat label="Net Exposure" value="$12.4B" trend="-0.8%" isUp={true} /></Card>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-3 gap-4 h-[400px]">
        <Card title="Market Volatility Impact" className="col-span-2">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data}>
              <defs>
                <linearGradient id="colorVal" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.2}/>
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <XAxis dataKey="time" hide />
              <YAxis hide domain={['dataMin - 10', 'dataMax + 10']} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#090b10', borderColor: '#1e2433', color: '#fff' }}
                itemStyle={{ color: '#fff' }}
              />
              <Area type="monotone" dataKey="val" stroke="#3b82f6" strokeWidth={2} fill="url(#colorVal)" />
            </AreaChart>
          </ResponsiveContainer>
        </Card>

        <Card title="Critical Alerts" className="col-span-1">
          <div className="space-y-3">
            {[
              { t: '12:04', m: 'Crude Oil spike detected', lvl: 'high' },
              { t: '11:58', m: 'Rupee depreciation (>83.5)', lvl: 'med' },
              { t: '10:30', m: 'Steel sector volume surge', lvl: 'low' },
            ].map((alert, i) => (
              <div key={i} className="flex gap-3 items-start p-2 border-l-2 border-transparent hover:border-accent-blue transition-colors">
                <div className={`mt-1.5 w-1.5 h-1.5 rounded-full ${alert.lvl === 'high' ? 'bg-accent-rose' : alert.lvl === 'med' ? 'bg-accent-gold' : 'bg-accent-blue'}`} />
                <div>
                  <p className="text-xs text-gray-500 font-mono">{alert.t}</p>
                  <p className="text-sm text-gray-300">{alert.m}</p>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;