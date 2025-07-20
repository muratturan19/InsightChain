import React, { useState } from 'react';
import ConnectionPopup from './ConnectionPopup';

export default function MainCard() {
  const [query, setQuery] = useState('');
  const [company, setCompany] = useState('');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('');
  const [result, setResult] = useState('');
  const [showPopup, setShowPopup] = useState(false);

  const checkInternet = async () => {
    try {
      const ping = await fetch('/check_internet');
      const pingRes = await ping.json();
      return Boolean(pingRes.ok);
    } catch {
      return false;
    }
  };

  const handleSearch = async () => {
    if (!query) return;
    setLoading(true);
    setResult('');
    setStatus('İnternet bağlantısı kontrol ediliyor...');
    const ok = await checkInternet();
    if (!ok) {
      setLoading(false);
      setStatus('');
      setShowPopup(true);
      return;
    }
    setStatus('Web sitesi inceleniyor...');
    const statusTimer = setTimeout(() => {
      setStatus('LinkedIn şirket ve kontak bilgileri analiz ediliyor...');
    }, 1500);
    try {
      const res = await fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ website: query, company: company || null })
      });
      setStatus('Rapor hazırlanıyor...');
      const data = await res.json();
      setResult(data.report || data.analysis?.summary || '');
      setStatus('');
      clearTimeout(statusTimer);
    } catch (err) {
      setStatus('Hata oluştu');
      clearTimeout(statusTimer);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-8 space-y-8 relative">
      {showPopup && (
        <ConnectionPopup
          onRetry={checkInternet}
          onClose={() => setShowPopup(false)}
        />
      )}
      <div className="grid gap-8 md:grid-cols-2">
        <div className="space-y-4">
          <label htmlFor="query" className="block text-slate-800 dark:text-slate-200 font-semibold">
            Web sitesi veya Query
          </label>
          <input
            id="query"
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full px-4 py-2 rounded border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500"
            placeholder="example.com or search term"
          />
          <label htmlFor="company" className="block text-slate-800 dark:text-slate-200 font-semibold">
            Şirket İsmi (opsiyonel)
          </label>
          <input
            id="company"
            type="text"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            className="w-full px-4 py-2 rounded border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500"
            placeholder="Acme Corp"
          />
          <button
            onClick={handleSearch}
            className="w-full h-11 bg-blue-900 hover:bg-blue-700 active:bg-blue-800 text-white rounded flex items-center justify-center"
            disabled={loading}
          >
            {loading ? '...' : 'Ara'}
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
      <div className="p-4 bg-slate-50 dark:bg-slate-900 rounded-lg shadow-sm min-h-40">
        {loading && (
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
            <p className="text-sm text-slate-700 dark:text-slate-300">{status}</p>
          </div>
        )}
        {!loading && result && (
          <div
            className="prose dark:prose-invert text-sm"
            dangerouslySetInnerHTML={{ __html: result }}
          />
        )}
      </div>
    </div>
  );
}
