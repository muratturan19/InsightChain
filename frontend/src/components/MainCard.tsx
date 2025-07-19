import React from 'react';

export default function MainCard() {
  return (
    <div className="space-y-4">
      <div className="grid md:grid-cols-2 gap-4">
        <div className="bg-white dark:bg-slate-800 p-4 rounded shadow h-32" />
        <div className="bg-white dark:bg-slate-800 p-4 rounded shadow flex items-center space-x-2">
          <input
            type="text"
            className="flex-1 p-2 border border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-slate-700 text-slate-800 dark:text-slate-100"
            placeholder="Query"
          />
          <button className="px-4 py-2 rounded bg-blue-600 text-white">Run</button>
        </div>
      </div>
      <div className="bg-white dark:bg-slate-800 p-4 rounded shadow h-40" />
    </div>
  );
}
