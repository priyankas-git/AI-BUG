// Shared File: App routing and main layout structure
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/dashboard/Sidebar';
import Topbar from './components/dashboard/Topbar';
import Dashboard from './pages/Dashboard';
import AnalysisPage from './pages/AnalysisPage';
import BugsPage from './pages/BugsPage';
import BugDetails from './pages/BugDetails';
import FixPage from './pages/FixPage';

function AppLayout({ children }) {
  return (
    <div className="flex bg-slate-950 min-h-screen text-slate-100">
      {/* Left Sidebar */}
      <Sidebar />

      {/* Right Content Panel */}
      <div className="flex-1 flex flex-col min-w-0">
        <Topbar />
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <AppLayout>
              <Dashboard />
            </AppLayout>
          }
        />
        <Route
          path="/analyze"
          element={
            <AppLayout>
              <AnalysisPage />
            </AppLayout>
          }
        />
        <Route
          path="/bugs"
          element={
            <AppLayout>
              <BugsPage />
            </AppLayout>
          }
        />
        <Route
          path="/bugs/:bug_id"
          element={
            <AppLayout>
              <BugDetails />
            </AppLayout>
          }
        />
        <Route
          path="/fix"
          element={
            <AppLayout>
              <FixPage />
            </AppLayout>
          }
        />
      </Routes>
    </Router>
  );
}
