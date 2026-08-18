// Ownership: Afreen (Dashboard + Analytics)
import React from 'react';

export default function StatCard({ title, value, icon: Icon, color }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-lg p-5 flex items-center justify-between">
      <div>
        <p className="text-slate-400 text-xs font-semibold uppercase tracking-wider">{title}</p>
        <h3 className={`text-2xl font-bold mt-1 ${color || 'text-white'}`}>{value}</h3>
      </div>
      {Icon && <Icon className="h-8 w-8 opacity-80" />}
    </div>
  );
}
