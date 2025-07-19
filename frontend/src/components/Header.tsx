import React from 'react';

interface HeaderProps {
  onToggleDark: () => void;
}

export default function Header({ onToggleDark }: HeaderProps) {
  return (
    <header className="flex items-center justify-between h-16 px-4 border-b border-slate-200 dark:border-slate-700">
      <div className="flex items-center font-semibold">InsightChain</div>
      <button
        aria-label="Toggle dark mode"
        onClick={onToggleDark}
        className="p-2 rounded hover:bg-slate-200 dark:hover:bg-slate-700"
      >
        🌙
      </button>
    </header>
  );
}
