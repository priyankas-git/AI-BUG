// Ownership: Afreen (Dashboard + Analytics)
import React from 'react';
import { Bell, User, CheckCircle2 } from 'lucide-react';

export default function Topbar() {
  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900 px-6 flex items-center justify-between sticky top-0 z-10">
      {/* System Status */}
      <div className="flex items-center space-x-2">
        <div className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
        <span className="text-xs text-slate-400 font-medium">All engines operational</span>
      </div>

      {/* Profile & Notifications */}
      <div className="flex items-center space-x-4">
        <button className="text-slate-400 hover:text-white transition p-1.5 hover:bg-slate-800 rounded-full">
          <Bell className="h-4.5 w-4.5" />
        </button>
        <div className="h-6 w-px bg-slate-800" />
        <div className="flex items-center space-x-2">
          <div className="h-8 w-8 rounded-full bg-cyan-900 border border-cyan-500/30 flex items-center justify-center text-xs font-semibold text-cyan-400">
            D
          </div>
          <span className="text-sm font-medium text-slate-200 hidden sm:inline">Disha (Developer)</span>
        </div>
      </div>
    </header>
  );
}
