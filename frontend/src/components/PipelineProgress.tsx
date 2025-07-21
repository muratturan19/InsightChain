import React from 'react';

export type StepStatus = 'pending' | 'in-progress' | 'success' | 'error';

export interface Step {
  label: string;
  status: StepStatus;
  duration?: number; // in milliseconds
  message?: string;
}

interface Props {
  steps: Step[];
  error?: string;
  onRetry: () => void;
}

export default function PipelineProgress({ steps, error, onRetry }: Props) {
  return (
    <div className="bg-slate-900 text-white p-4 rounded-lg w-full max-w-md font-mono text-sm space-y-1">
      {steps.map((step, idx) => (
        <div key={idx} className="flex justify-between items-center">
          <span>{step.label}</span>
          <span className="flex items-center space-x-2 min-w-[80px] justify-end">
            {step.status === 'in-progress' && (
              <div className="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin" />
            )}
            {step.status === 'success' && <span className="text-green-400">OK</span>}
            {step.status === 'error' && <span className="text-red-400">Error</span>}
            {(step.status === 'success' || step.status === 'error') &&
              step.duration !== undefined && (
                <span className="text-slate-400">{Math.round(step.duration)} ms</span>
              )}
          </span>
          {step.message && step.status === 'error' && (
            <span className="text-red-400 text-xs ml-2">{step.message}</span>
          )}
        </div>
      ))}
      <div className="pt-2 flex justify-between items-center">
        {error && <span className="text-red-400 text-xs">{error}</span>}
        <button onClick={onRetry} className="px-3 py-1 bg-blue-900 rounded text-white text-xs">
          Tekrar Dene
        </button>
      </div>
    </div>
  );
}
