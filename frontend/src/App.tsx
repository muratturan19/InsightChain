import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import MainCard from './components/MainCard';

export default function App() {
  const [dark, setDark] = useState(false);

  useEffect(() => {
    const root = document.documentElement;
    if (dark) {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
  }, [dark]);

  return (
    <div className="flex flex-col min-h-screen">
      <Header onToggleDark={() => setDark((v) => !v)} dark={dark} />
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 flex items-start justify-center p-6">
          <div className="w-full max-w-5xl">
            <MainCard />
          </div>
        </main>
      </div>
    </div>
  );
}
