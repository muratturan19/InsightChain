# InsightChain Backend

Bu dizin FastAPI tabanlı REST servislerini içerir. Her bir ajan ve workflow modüler olarak `agents/`, `tools/` ve `workflows/` klasörlerinde yer alır.

## Çalıştırma

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

`requirements.txt` scraping aracı için Playwright, Selenium ve Scrapy gibi ek kütühaneler içerir. Playwright kullanılacaksa `playwright install` komutu ile tarayıcıları kurmayı unutmayın.

Yerel `.env` dosyanızı oluşturup gerekli API anahtarlarını tanımlayın.
