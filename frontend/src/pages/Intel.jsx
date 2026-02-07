import React, { useEffect, useState } from 'react';
import { Globe, ExternalLink, ShieldAlert, Zap, TrendingUp } from 'lucide-react';

const Intel = () => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/intel/news')
      .then(res => res.json())
      .then(data => {
        setNews(data);
        setLoading(false);
      })
      .catch(err => setLoading(false));
  }, []);

  return (
    <div className="p-8 bg-midnight-950 min-h-full w-full">
      
      {/* Header */}
      <div className="mb-8 border-b border-midnight-700 pb-4 flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-semibold text-white tracking-tight flex items-center gap-3">
            <Globe className="text-accent-teal" /> Global Intelligence
          </h1>
          <p className="text-sm text-gray-500 mt-1 font-mono">
            Live Sentiment Analysis • High-Frequency News Stream
          </p>
        </div>
        <div className="text-xs font-mono text-accent-teal animate-pulse">
          ● LIVE FEED ACTIVE
        </div>
      </div>

      {/* News Feed */}
      <div className="grid grid-cols-1 gap-4 max-w-5xl mx-auto">
        {loading ? (
            <div className="text-center text-gray-500 mt-20 font-mono">ESTABLISHING UPLINK...</div>
        ) : (
            news.map((item, i) => (
            <div 
                key={i} 
                onClick={() => window.open(item.link, '_blank')}
                className="group cursor-pointer bg-midnight-900 border border-midnight-700 p-5 rounded-lg flex items-center justify-between hover:border-accent-blue hover:bg-midnight-800 transition-all"
            >
                <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                        <span className="text-xs font-bold text-gray-500 font-mono">{item.time}</span>
                        <span className="text-xs px-2 py-0.5 rounded bg-midnight-800 text-gray-300 border border-midnight-700">{item.publisher}</span>
                        <span className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider border ${
                            item.sentiment === 'POSITIVE' ? 'bg-accent-teal/10 text-accent-teal border-accent-teal/20' :
                            item.sentiment === 'NEGATIVE' ? 'bg-accent-rose/10 text-accent-rose border-accent-rose/20' :
                            'bg-gray-800 text-gray-400 border-gray-700'
                        }`}>
                            {item.sentiment}
                        </span>
                    </div>
                    <h3 className="text-lg text-gray-200 font-medium group-hover:text-accent-blue transition-colors">
                        {item.title}
                    </h3>
                </div>
                
                <div className="flex flex-col items-end pl-6 border-l border-midnight-700 ml-6">
                    <span className="text-xs font-bold text-gray-400 mb-2">{item.related}</span>
                    <ExternalLink size={16} className="text-gray-600 group-hover:text-white transition-colors" />
                </div>
            </div>
            ))
        )}
      </div>
    </div>
  );
};

export default Intel;