import React from 'react';

interface HeaderProps {
  onToggleDark: () => void;
  dark: boolean;
}

export default function Header({ onToggleDark, dark }: HeaderProps) {
  return (
    <header className="flex items-center justify-between w-full h-16 px-6 py-4 bg-white dark:bg-slate-800 text-slate-900 dark:text-white shadow-md">
      <div className="flex items-center space-x-2 font-semibold">
        <div className="w-8 h-8 rounded-full bg-blue-900" />
        <span>InsightChain</span>
      </div>
      <button
        aria-label="Toggle dark mode"
        onClick={onToggleDark}
        className="w-8 h-8 flex items-center justify-center rounded-full hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
      >
        {dark ? '☀️' : '🌙'}
      </button>
    </header>
  );
}
