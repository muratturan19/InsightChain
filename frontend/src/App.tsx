import React from 'react';

export default function App() {
  return (
    <div className="min-h-screen grid grid-cols-12">
      <aside className="col-span-2 bg-slate-900 text-white p-4">Sidebar</aside>
      <main className="col-span-10 p-4">
        <header className="mb-4 text-2xl font-bold text-corporate">InsightChain</header>
        <section className="bg-white p-4 rounded shadow">Sonuçlar burada</section>
      </main>
    </div>
  );
}
