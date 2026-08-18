// Ownership: Priyanka (Bug Details + Fix/Validation + UI Integration)
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldAlert, ChevronRight, Filter, AlertTriangle } from 'lucide-react';
import api from '../services/api';

export default function BugsPage() {
  const navigate = useNavigate();
  const [bugs, setBugs] = useState([]);
  const [filterSeverity, setFilterSeverity] = useState('ALL');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadBugs() {
      setLoading(true);
      // Try to load latest analysis bugs from local storage or api
      const local = localStorage.getItem("latest_analysis");
      if (local) {
        const parsed = JSON.parse(local);
        setBugs(parsed.bugs || []);
        setLoading(false);
      } else {
        try {
          const data = await api.getBugs();
          setBugs(data);
        } catch (err) {
          // If no api, set fallback bugs
          setBugs([
            {
              id: "BUG-001",
              type: "Runtime Error",
              severity: "HIGH",
              confidence: 0.96,
              file: "example.py",
              line: 3,
              description: "Possible division by zero.",
              explanation: "The function may divide by zero when an empty list is supplied.",
              impact: "The application may terminate with ZeroDivisionError.",
              suggestion: "Validate the input before performing the division.",
              fixed_code: `def calculate_average(numbers):\n    if not numbers:\n        return 0\n\n    total = sum(numbers)\n    return total / len(numbers)`,
              test_case: `def test_empty_numbers():\n    assert calculate_average([]) == 0`,
              status: "OPEN"
            },
            {
              id: "BUG-002",
              type: "Security Vulnerability",
              severity: "CRITICAL",
              confidence: 0.98,
              file: "example.py",
              line: 8,
              description: "Hardcoded SQL string concatenation detected.",
              explanation: "Directly placing parameters in sql query makes it prone to sql injection.",
              impact: "Attacker can read, modify database records.",
              suggestion: "Use parameterized queries or ORM filter syntax.",
              fixed_code: `query = "SELECT * FROM users WHERE name = :name"`,
              test_case: `def test_sql_injection():\n    # Test validation payload\n    pass`,
              status: "OPEN"
            }
          ]);
        } finally {
          setLoading(false);
        }
      }
    }
    loadBugs();
  }, []);

  const filteredBugs = bugs.filter((bug) => {
    if (filterSeverity === 'ALL') return true;
    return bug.severity.toUpperCase() === filterSeverity.toUpperCase();
  });

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
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white">Detected Bugs</h1>
          <p className="text-slate-400 text-sm">Review, inspect, and automatically remediate detected vulnerabilities.</p>
        </div>

        {/* Filter */}
        <div className="flex items-center space-x-2 bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-lg text-sm">
          <Filter className="h-4 w-4 text-slate-400" />
          <span className="text-slate-400 font-medium">Filter:</span>
          <select
            value={filterSeverity}
            onChange={(e) => setFilterSeverity(e.target.value)}
            className="bg-slate-950 border-none text-slate-200 outline-none focus:ring-0 text-sm cursor-pointer"
          >
            <option value="ALL">All Severities</option>
            <option value="CRITICAL">Critical</option>
            <option value="HIGH">High</option>
            <option value="MEDIUM">Medium</option>
            <option value="LOW">Low</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-10 text-slate-500">Loading bugs...</div>
      ) : filteredBugs.length === 0 ? (
        <div className="bg-slate-900 border border-slate-800 rounded-lg p-10 text-center text-slate-500 space-y-2">
          <ShieldAlert className="h-10 w-10 mx-auto opacity-40 text-emerald-500" />
          <p className="font-semibold text-white">No Bugs Found</p>
          <p className="text-xs max-w-sm mx-auto">
            Your code appears clean of detected flaws. Run another analysis to verify code health.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4">
          {filteredBugs.map((bug) => (
            <div
              key={bug.id}
              onClick={() => {
                localStorage.setItem("selected_bug", JSON.stringify(bug));
                navigate(`/bugs/${bug.id}`);
              }}
              className="bg-slate-900 border border-slate-800 hover:border-slate-700 hover:bg-slate-800/40 p-5 rounded-lg cursor-pointer transition flex items-center justify-between"
            >
              <div className="space-y-2">
                <div className="flex items-center space-x-2 flex-wrap gap-y-1">
                  <span className={`px-2.5 py-0.5 rounded text-xs font-bold border ${getSeverityColor(bug.severity)}`}>
                    {bug.severity}
                  </span>
                  <span className="text-xs text-slate-500 font-mono">{bug.id}</span>
                  <span className="text-xs text-slate-400 font-mono">{bug.file}:{bug.line}</span>
                  <span className="text-xs text-slate-500 font-mono">Score: {(bug.confidence * 100).toFixed(0)}%</span>
                </div>
                <h3 className="text-base font-semibold text-white">{bug.type}</h3>
                <p className="text-sm text-slate-400 max-w-2xl">{bug.description}</p>
              </div>
              <ChevronRight className="h-6 w-6 text-slate-500 hover:text-white" />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
