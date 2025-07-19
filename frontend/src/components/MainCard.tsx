import React from 'react';

export default function MainCard() {
  return (
    <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-8 space-y-8">
      <div className="grid gap-8 md:grid-cols-2">
        <div className="space-y-4">
          <label htmlFor="query" className="block text-slate-800 dark:text-slate-200 font-semibold">
            Web sitesi veya Query
          </label>
          <input
            id="query"
            type="text"
            className="w-full px-4 py-2 rounded border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500"
            placeholder="example.com or search term"
          />
          <button className="w-full h-11 bg-blue-900 hover:bg-blue-700 active:bg-blue-800 text-white rounded">
            Ara
          </button>
        </div>
        <div className="space-y-2">
          <h2 className="text-base font-semibold text-slate-900 dark:text-white">Ayarlar / Filtreler</h2>
          <label className="flex items-center space-x-2 text-slate-800 dark:text-slate-200">
            <input type="checkbox" className="accent-blue-600" />
            <span>Seçenek 1</span>
          </label>
          <label className="flex items-center space-x-2 text-slate-800 dark:text-slate-200">
            <input type="checkbox" className="accent-blue-600" />
            <span>Seçenek 2</span>
          </label>
          <p className="text-sm text-slate-400 dark:text-slate-500">Future filters here</p>
        </div>
      </div>
      <div className="p-4 bg-slate-50 dark:bg-slate-900 rounded-lg shadow-sm h-40" />
    </div>
  );
}
