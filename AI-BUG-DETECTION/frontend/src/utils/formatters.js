// Shared File: Formatters and helpers
export const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

export const formatPercentage = (val) => {
  if (val === undefined || val === null) return '0%';
  return `${(val * 100).toFixed(0)}%`;
};

export const getSeverityBadgeClasses = (severity) => {
  switch (severity?.toUpperCase()) {
    case 'CRITICAL':
      return 'bg-red-950/40 text-red-400 border-red-500/20';
    case 'HIGH':
      return 'bg-orange-950/40 text-orange-400 border-orange-500/20';
    case 'MEDIUM':
      return 'bg-yellow-950/40 text-yellow-400 border-yellow-500/20';
    case 'LOW':
      return 'bg-green-950/40 text-green-400 border-green-500/20';
    default:
      return 'bg-slate-850 text-slate-400 border-slate-700';
  }
};
