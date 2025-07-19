# InsightChain Backend

Bu dizin FastAPI tabanlı REST servislerini içerir. Her bir ajan ve workflow modüler olarak `agents/`, `tools/` ve `workflows/` klasörlerinde yer alır.

## Çalıştırma

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Yerel `.env` dosyanızı oluşturup gerekli API anahtarlarını tanımlayın.
