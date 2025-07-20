# InsightChain

**AI tabanlı, çok ajanlı veri toplama ve içgörü üretim platformu.** Bu repo hem FastAPI tabanlı backend'i hem de React/Tailwind ile yazılmış dashboard arayüzünü içerir.

## Monorepo Yapısı

- `backend/` – REST API ve ajan orkestrasyonu
- `frontend/` – Dashboard arayüzü
- `Agents.md` – Tanımlı ajan ve tool listesini içerir

## Hızlı Başlangıç

### Backend
Komutları depo kök dizininden çalıştırın:
```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Gerekli API anahtarları (Exa, OpenAI, Brave, SerpAPI ve Google Custom Search) için `backend/.env.example` dosyasını kopyalayıp `.env` adıyla doldurmayı unutmayın.

LinkedIn şirket sayfasını bulmak için backend'deki `/find_linkedin` endpoint'ini
kullanabilirsiniz.
Tam entegre analiz için `/analyze` endpoint'ine şirket web sitesini POST edin.
Reporter Agent'ın tool destekli çalışmasını görmek için `backend/examples/reporter_usage.py` dosyasını çalıştırabilirsiniz.
