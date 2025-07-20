import React, { useState } from 'react';
import ConnectionPopup from './ConnectionPopup';
import PipelineProgress, { Step } from './PipelineProgress';

export default function MainCard() {
  const [query, setQuery] = useState('');
  const [company, setCompany] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState('');
  const [showPopup, setShowPopup] = useState(false);
  const [steps, setSteps] = useState<Step[]>([]);
  const [showPipeline, setShowPipeline] = useState(false);

  const handleSavePdf = () => {
    const reportEl = document.getElementById('report-area');
    if (!reportEl) return;
    const newWin = window.open('', '_blank');
    if (!newWin) return;
    newWin.document.write(
      `<html><head><title>Report</title></head><body>${reportEl.innerHTML}</body></html>`
    );
    newWin.document.close();
    newWin.print();
  };

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
    setShowPipeline(true);

    const newSteps: Step[] = [
      { label: 'İnternet Bağlantısı Kontrol Ediliyor', status: 'pending' },
      { label: 'Web Sitesi İnceleniyor', status: 'pending' },
      { label: 'LinkedIn Bilgileri Alınıyor', status: 'pending' },
      { label: 'Rapor Hazırlanıyor', status: 'pending' }
    ];
    setSteps(newSteps);

    const update = (i: number, data: Partial<Step>) =>
      setSteps((prev) => {
        const copy = [...prev];
        copy[i] = { ...copy[i], ...data };
        return copy;
      });

    const s0 = performance.now();
    update(0, { status: 'in-progress' });
    const ok = await checkInternet();
    update(0, {
      status: ok ? 'success' : 'error',
      duration: performance.now() - s0
    });
    if (!ok) {
      setLoading(false);
      setShowPipeline(false);
      setShowPopup(true);
      return;
    }

    const s1 = performance.now();
    update(1, { status: 'in-progress' });
    await new Promise((r) => setTimeout(r, 500));
    update(1, { status: 'success', duration: performance.now() - s1 });

    const s2 = performance.now();
    update(2, { status: 'in-progress' });
    await new Promise((r) => setTimeout(r, 500));
    update(2, { status: 'success', duration: performance.now() - s2 });

    const s3 = performance.now();
    update(3, { status: 'in-progress' });
    try {
      const res = await fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ website: query, company: company || null })
      });
      const data = await res.json();
      setResult(data.report || data.analysis?.summary || '');
      update(3, { status: 'success', duration: performance.now() - s3 });
    } catch (err) {
      update(3, { status: 'error', duration: performance.now() - s3 });
    } finally {
      setLoading(false);
      setTimeout(() => setShowPipeline(false), 1000);
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
      {showPipeline && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
          <PipelineProgress steps={steps} />
        </div>
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
      <div id="report-area" className="p-4 bg-slate-50 dark:bg-slate-900 rounded-lg shadow-sm min-h-40">
        {!loading && result && (
          <div
            className="prose dark:prose-invert text-sm"
            dangerouslySetInnerHTML={{ __html: result }}
          />
        )}
      </div>
      {!loading && result && (
        <div className="flex justify-end">
          <button
            onClick={handleSavePdf}
            className="mt-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded"
          >
            PDF olarak Kaydet
          </button>
        </div>
      )}
    </div>
  );
}
