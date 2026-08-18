// Ownership: Afreen (Dashboard + Analytics)
import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Code, ShieldAlert, Settings, HelpCircle, Terminal } from 'lucide-react';

export default function Sidebar() {
  const menuItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Code Analysis', path: '/analyze', icon: Code },
    { name: 'Detected Bugs', path: '/bugs', icon: ShieldAlert },
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col justify-between h-screen sticky top-0">
      <div className="flex-1 py-6">
        {/* Logo */}
        <div className="flex items-center space-x-2 px-6 mb-8">
          <Terminal className="h-6 w-6 text-cyan-400" />
          <span className="font-bold text-white text-base tracking-wider">BUG DETECTOR</span>
        </div>

        {/* Navigation */}
        <nav className="px-3 space-y-1">
          {menuItems.map((item) => (
            <NavLink
              key={item.name}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center space-x-3 px-4 py-2.5 rounded-lg text-sm font-medium transition ${
                  isActive
                    ? 'bg-cyan-950/60 text-cyan-400 border-l-2 border-cyan-500 rounded-l-none'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
                }`
              }
            >
              <item.icon className="h-4.5 w-4.5 shrink-0" />
              <span>{item.name}</span>
            </NavLink>
          ))}
        </nav>
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-slate-800 space-y-1">
        <button className="flex items-center space-x-3 w-full px-4 py-2 text-slate-400 hover:text-white rounded-lg text-sm transition">
          <Settings className="h-4.5 w-4.5" />
          <span>Settings</span>
        </button>
        <button className="flex items-center space-x-3 w-full px-4 py-2 text-slate-400 hover:text-white rounded-lg text-sm transition">
          <HelpCircle className="h-4.5 w-4.5" />
          <span>Documentation</span>
        </button>
      </div>
    </aside>
  );
}
