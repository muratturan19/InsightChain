import React from 'react';

export default function Sidebar() {
  return (
    <aside className="w-64 h-screen overflow-y-auto bg-slate-100 dark:bg-slate-800 border-r border-slate-200 dark:border-slate-700 px-4 py-8 flex flex-col justify-between">
      <nav className="space-y-4">
        <a
          href="#"
          className="block py-2 px-3 rounded font-semibold text-blue-700 dark:text-blue-400 bg-blue-100 dark:bg-blue-950"
        >
          Menu 1
        </a>
        <a
          href="#"
          className="block py-2 px-3 rounded font-semibold text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700"
        >
          Menu 2
        </a>
        <a
          href="#"
          className="block py-2 px-3 rounded font-semibold text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700"
        >
          Menu 3
        </a>
      </nav>
      <div className="text-xs text-slate-500 dark:text-slate-400 mt-8">Sidebar placeholder</div>
    </aside>
  );
}
