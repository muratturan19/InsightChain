import React from 'react';

export default function Sidebar() {
  return (
    <aside className="w-64 h-full overflow-y-auto border-r border-slate-200 dark:border-slate-700 p-4">
      <nav className="space-y-2">
        <a href="#" className="block py-2 px-3 rounded hover:bg-slate-100 dark:hover:bg-slate-800">Menu 1</a>
        <a href="#" className="block py-2 px-3 rounded hover:bg-slate-100 dark:hover:bg-slate-800">Menu 2</a>
        <a href="#" className="block py-2 px-3 rounded hover:bg-slate-100 dark:hover:bg-slate-800">Menu 3</a>
      </nav>
    </aside>
  );
}
