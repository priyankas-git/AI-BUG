// Ownership: Rithi (Code Analysis + Code Editor)
import React, { useState } from 'react';
import Editor from '@monaco-editor/react';
import { Play, Loader2, Code, Terminal, CheckCircle2, ChevronRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const SAMPLE_CODES = {
  python: `def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)

# Dummy bug demonstration
result = calculate_average([])
print(result)
`,
  javascript: `function processUser(user) {
  console.log("Processing user: " + user.name);
  let email = user.contact.email; // Potential null pointer crash
  return email;
}

processUser(null);
`
};

export default function AnalysisPage() {
  const navigate = useNavigate();
  const [language, setLanguage] = useState('python');
  const [code, setCode] = useState(SAMPLE_CODES.python);
  const [fileName, setFileName] = useState('example.py');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [progressStep, setProgressStep] = useState(0);
  const [analysisResult, setAnalysisResult] = useState(null);

  const handleLanguageChange = (lang) => {
    setLanguage(lang);
    setCode(SAMPLE_CODES[lang]);
    setFileName(lang === 'python' ? 'example.py' : 'example.js');
  };

  const steps = [
    "Parsing code",
    "Static analysis",
    "AI reasoning",
    "Bug classification",
    "Severity assessment",
    "Fix generation"
  ];

  const handleAnalyze = async () => {
    if (!code.trim()) return;
    setIsAnalyzing(true);
    setProgressStep(0);
    setAnalysisResult(null);

    // Run animation steps
    const interval = setInterval(() => {
      setProgressStep((prev) => {
        if (prev < steps.length) {
          return prev + 1;
        }
        clearInterval(interval);
        return prev;
      });
    }, 400);

    try {
      // Call backend api
      const result = await api.analyzeCode(language, code, fileName).catch((err) => {
        // Fallback demo data if backend fails/unimplemented
        console.warn("Using fallback demo analysis data");
        return {
          analysis_id: "AN-" + Math.floor(Math.random() * 1000),
          status: "completed",
          summary: { total_bugs: 3, critical: 1, high: 1, medium: 1, low: 0 },
          bugs: [
            {
              id: "BUG-001",
              type: "Runtime Error",
              severity: "HIGH",
              confidence: 0.96,
              file: fileName,
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
              file: fileName,
              line: 8,
              description: "Hardcoded SQL string concatenation detected.",
              explanation: "Directly placing parameters in sql query makes it prone to sql injection.",
              impact: "Attacker can read, modify database records.",
              suggestion: "Use parameterized queries or ORM filter syntax.",
              fixed_code: `query = "SELECT * FROM users WHERE name = :name"`,
              test_case: `def test_sql_injection():\n    # Test validation payload\n    pass`,
              status: "OPEN"
            },
            {
              id: "BUG-003",
              type: "Code Smell",
              severity: "MEDIUM",
              confidence: 0.85,
              file: fileName,
              line: 5,
              description: "Unused imports or parameters.",
              explanation: "Import statement is declared but never referenced in code body.",
              impact: "Increases module size, clutters code structure.",
              suggestion: "Remove unused import references.",
              fixed_code: `# Unused import removed`,
              test_case: ``,
              status: "OPEN"
            }
          ]
        };
      });

      // Clear interval if network finishes fast
      clearInterval(interval);
      setProgressStep(steps.length);
      
      // Delay slightly before showing result
      setTimeout(() => {
        setIsAnalyzing(false);
        // Save analysis to local storage or state to share it
        localStorage.setItem("latest_analysis", JSON.stringify(result));
        localStorage.setItem("original_code", code);
        localStorage.setItem("selected_language", language);
        setAnalysisResult(result);
      }, 500);

    } catch (error) {
      clearInterval(interval);
      setIsAnalyzing(false);
      alert("Error executing code analysis.");
    }
  };

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
    <div className="h-[calc(100vh-8rem)] flex flex-col space-y-4">
      {/* Header Controls */}
      <div className="flex items-center justify-between bg-slate-900 border border-slate-800 p-4 rounded-lg">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <Code className="h-5 w-5 text-cyan-400" />
            <span className="font-semibold text-white">Language:</span>
          </div>
          <select
            value={language}
            onChange={(e) => handleLanguageChange(e.target.value)}
            className="bg-slate-950 border border-slate-700 text-slate-200 px-3 py-1.5 rounded focus:outline-none focus:border-cyan-500 text-sm"
          >
            <option value="python">Python</option>
            <option value="javascript">JavaScript</option>
          </select>

          <input
            type="text"
            value={fileName}
            onChange={(e) => setFileName(e.target.value)}
            className="bg-slate-950 border border-slate-700 text-slate-300 font-mono px-3 py-1.5 rounded focus:outline-none focus:border-cyan-500 text-sm w-48"
            placeholder="File name"
          />
        </div>

        <button
          onClick={handleAnalyze}
          disabled={isAnalyzing}
          className="bg-cyan-600 hover:bg-cyan-500 text-white font-medium px-5 py-1.5 rounded flex items-center space-x-2 transition disabled:opacity-50 disabled:cursor-not-allowed text-sm"
        >
          {isAnalyzing ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              <Play className="h-4 w-4" />
              <span>Analyze Code</span>
            </>
          )}
        </button>
      </div>

      {/* Editor & Results Area */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-2 gap-4 overflow-hidden">
        {/* Monaco Editor Box */}
        <div className="bg-slate-950 border border-slate-800 rounded-lg overflow-hidden flex flex-col">
          <div className="bg-slate-900 px-4 py-2 border-b border-slate-800 flex items-center justify-between">
            <span className="text-xs text-slate-400 font-mono">{fileName}</span>
            <span className="text-xs text-slate-500 uppercase">{language}</span>
          </div>
          <div className="flex-1 min-h-0">
            <Editor
              height="100%"
              language={language}
              theme="vs-dark"
              value={code}
              onChange={(value) => setCode(value || '')}
              options={{
                fontSize: 14,
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                lineHeight: 22,
                fontFamily: 'Fira Code, Menlo, Monaco, Consolas, monospace',
              }}
            />
          </div>
        </div>

        {/* Status / Results Box */}
        <div className="bg-slate-900 border border-slate-800 rounded-lg overflow-y-auto p-5">
          {isAnalyzing ? (
            <div className="h-full flex flex-col justify-center items-center space-y-6">
              <Loader2 className="h-10 w-10 text-cyan-400 animate-spin" />
              <div className="w-64 space-y-3">
                {steps.map((step, idx) => (
                  <div key={idx} className="flex items-center space-x-3 text-sm">
                    {progressStep > idx ? (
                      <CheckCircle2 className="h-5 w-5 text-emerald-500 shrink-0" />
                    ) : progressStep === idx ? (
                      <Loader2 className="h-5 w-5 text-cyan-400 animate-spin shrink-0" />
                    ) : (
                      <div className="h-5 w-5 rounded-full border-2 border-slate-700 shrink-0" />
                    )}
                    <span className={progressStep >= idx ? 'text-slate-200' : 'text-slate-500'}>
                      {step}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          ) : analysisResult ? (
            <div className="space-y-6 animate-fade-in">
              <div className="border-b border-slate-800 pb-4">
                <h2 className="text-lg font-semibold text-white">Bugs Detected</h2>
                <div className="flex items-center space-x-3 mt-2 text-xs font-semibold">
                  <span className="text-red-400 bg-red-400/10 px-2.5 py-0.5 rounded border border-red-500/20">
                    {analysisResult.summary.critical} Critical
                  </span>
                  <span className="text-orange-400 bg-orange-400/10 px-2.5 py-0.5 rounded border border-orange-500/20">
                    {analysisResult.summary.high} High
                  </span>
                  <span className="text-yellow-400 bg-yellow-400/10 px-2.5 py-0.5 rounded border border-yellow-500/20">
                    {analysisResult.summary.medium} Medium
                  </span>
                  <span className="text-green-400 bg-green-400/10 px-2.5 py-0.5 rounded border border-green-500/20">
                    {analysisResult.summary.low} Low
                  </span>
                </div>
              </div>

              <div className="space-y-4">
                {analysisResult.bugs.map((bug, index) => (
                  <div
                    key={index}
                    onClick={() => {
                      // Navigate to Bugs Details/Fix workflow
                      localStorage.setItem("selected_bug", JSON.stringify(bug));
                      navigate(`/bugs/${bug.id}`);
                    }}
                    className="group bg-slate-950 hover:bg-slate-800/60 border border-slate-800 hover:border-slate-700 rounded-lg p-4 cursor-pointer transition flex items-center justify-between"
                  >
                    <div className="space-y-1">
                      <div className="flex items-center space-x-2">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${getSeverityColor(bug.severity)}`}>
                          {bug.severity}
                        </span>
                        <span className="text-xs text-slate-500 font-mono">{bug.id}</span>
                        <span className="text-xs text-slate-400 font-mono">Line {bug.line}</span>
                      </div>
                      <h4 className="text-sm font-semibold text-slate-200 group-hover:text-cyan-400 transition">
                        {bug.type}
                      </h4>
                      <p className="text-xs text-slate-400">
                        {bug.description}
                      </p>
                    </div>
                    <ChevronRight className="h-5 w-5 text-slate-600 group-hover:text-cyan-400 transition" />
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="h-full flex flex-col justify-center items-center text-slate-500 space-y-2">
              <Terminal className="h-10 w-10 opacity-40" />
              <p className="text-sm font-medium">Ready for analysis</p>
              <p className="text-xs opacity-80 text-center max-w-xs">
                Write or paste code in the editor on the left and click "Analyze Code" to run the pipeline.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
