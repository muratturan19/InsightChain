# InsightChain

**AI tabanlı, çok ajanlı veri toplama ve içgörü üretim platformu.** Bu repo hem FastAPI tabanlı backend'i hem de React/Tailwind ile yazılmış dashboard arayüzünü içerir.

## Monorepo Yapısı

- `backend/` – REST API ve ajan orkestrasyonu
- `frontend/` – Dashboard arayüzü
- `Agents.md` – Tanımlı ajan ve tool listesini içerir

## Hızlı Başlangıç

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Gerekli API anahtarlarını `backend/.env.example` dosyasını kopyalayıp `.env` adında oluşturmayı unutmayın.
