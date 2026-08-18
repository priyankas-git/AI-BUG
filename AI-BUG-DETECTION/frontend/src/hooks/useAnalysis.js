// Ownership: Rithi (Code Analysis + Code Editor)
import { useState, useCallback } from 'react';
import api from '../services/api';

export function useAnalysis() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const runAnalysis = useCallback(async (language, code, fileName, projectId = null) => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.analyzeCode(language, code, fileName, projectId);
      setResult(data);
      return data;
    } catch (err) {
      const errMsg = err.response?.data?.detail || "An error occurred during code analysis.";
      setError(errMsg);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    loading,
    error,
    result,
    runAnalysis,
  };
}

export default useAnalysis;
