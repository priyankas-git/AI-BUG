// Ownership: Priyanka (Bug Details + Fix/Validation + UI Integration)
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Play, ShieldAlert, Sparkles, Terminal, AlertTriangle, ShieldCheck } from 'lucide-react';
import api from '../services/api';

export default function BugDetails() {
  const { bug_id } = useParams();
  const navigate = useNavigate();
  const [bug, setBug] = useState(null);

  useEffect(() => {
    // Read from local storage first
    const storedBug = localStorage.getItem("selected_bug");
    if (storedBug) {
      const parsed = JSON.parse(storedBug);
      if (parsed.id === bug_id) {
        setBug(parsed);
        return;
      }
    }

    // Otherwise load via api
    async function loadBug() {
      try {
        const data = await api.getBugDetails(bug_id);
        setBug(data);
      } catch (err) {
        // Fallback for demo flow
        console.warn("Unable to fetch bug from database, checking local storage fallbacks");
      }
    }
    loadBug();
  }, [bug_id]);

  if (!bug) {
    return (
      <div className="text-slate-400 py-10 flex flex-col items-center justify-center space-y-3">
        <Loader2 className="h-8 w-8 animate-spin text-cyan-400" />
        <span>Loading bug details...</span>
      </div>
    );
  }

  const getSeverityColor = (sev) => {
    switch (sev.toUpperCase()) {
      case 'CRITICAL': return 'text-red-500 bg-red-500/10 border-red-500/20';
      case 'HIGH': return 'text-orange-500 bg-orange-500/10 border-orange-500/20';
      case 'MEDIUM': return 'text-yellow-500 bg-yellow-500/10 border-yellow-500/20';
      case 'LOW': return 'text-green-500 bg-green-500/10 border-green-500/20';
      default: return 'text-slate-400 bg-slate-400/10 border-slate-400/20';
    }
  };

  return (
    <div className="space-y-6">
      {/* Back button */}
      <button
        onClick={() => navigate(-1)}
        className="flex items-center space-x-2 text-sm text-slate-400 hover:text-white transition"
      >
        <ArrowLeft className="h-4 w-4" />
        <span>Back to results</span>
      </button>

      {/* Hero Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-2">
          <div className="flex items-center space-x-3">
            <span className={`px-3 py-1 rounded text-xs font-bold border ${getSeverityColor(bug.severity)}`}>
              {bug.severity}
            </span>
            <span className="text-sm font-mono text-cyan-400">{bug.id}</span>
            <span className="text-xs text-slate-500 font-mono">{bug.file}:{bug.line}</span>
          </div>
          <h1 className="text-2xl font-bold text-white tracking-tight">{bug.type}</h1>
          <p className="text-slate-300 text-sm">{bug.description}</p>
        </div>

        <button
          onClick={() => {
            localStorage.setItem("selected_bug", JSON.stringify(bug));
            navigate(`/fix`);
          }}
          className="bg-cyan-600 hover:bg-cyan-500 text-white font-medium px-5 py-2.5 rounded-lg flex items-center justify-center space-x-2 transition self-start md:self-auto"
        >
          <Sparkles className="h-4 w-4" />
          <span>Remediate Bug</span>
        </button>
      </div>

      {/* Grid Layout for Bug Specifics */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Side: Explanation & Impact */}
        <div className="lg:col-span-2 space-y-6">
          {/* Detailed Explanation */}
          <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-4">
            <h2 className="text-lg font-medium text-white flex items-center space-x-2">
              <Terminal className="h-5 w-5 text-cyan-400" />
              <span>Explanation</span>
            </h2>
            <div className="text-slate-300 text-sm space-y-2 leading-relaxed font-sans">
              <p>{bug.explanation}</p>
            </div>
          </div>

          {/* Impact */}
          <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-4">
            <h2 className="text-lg font-medium text-white flex items-center space-x-2">
              <AlertTriangle className="h-5 w-5 text-rose-500" />
              <span>Potential Impact</span>
            </h2>
            <div className="text-slate-300 text-sm leading-relaxed">
              <p>{bug.impact}</p>
            </div>
          </div>
        </div>

        {/* Right Side: Metadata / AI Metrics */}
        <div className="space-y-6">
          {/* AI Score */}
          <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-4">
            <h3 className="text-sm font-semibold uppercase text-slate-400 tracking-wider">AI Metrics</h3>
            <div>
              <p className="text-xs text-slate-500">AI Confidence Score</p>
              <div className="flex items-center space-x-3 mt-1">
                <span className="text-3xl font-extrabold text-white">{(bug.confidence * 100).toFixed(0)}%</span>
                <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-cyan-500 rounded-full"
                    style={{ width: `${bug.confidence * 100}%` }}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Suggested Fix */}
          <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-4">
            <h3 className="text-sm font-semibold uppercase text-slate-400 tracking-wider flex items-center space-x-2">
              <ShieldCheck className="h-4 w-4 text-emerald-500" />
              <span>Fix Recommendation</span>
            </h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              {bug.suggestion}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
