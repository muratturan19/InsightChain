# InsightChain Backend

Bu dizin FastAPI tabanlı REST servislerini içerir. Her bir ajan ve workflow modüler olarak `agents/`, `tools/` ve `workflows/` klasörlerinde yer alır.

## Çalıştırma
Komutları depo kök dizininden çalıştırın:
```bash
pip install -r requirements.txt
cd ..
uvicorn backend.main:app --reload
```

`requirements.txt` scraping aracı için Playwright, Selenium ve Scrapy gibi ek kütühaneler içerir. Playwright kullanılacaksa `playwright install` komutu ile tarayıcıları kurmayı unutmayın.

Yerel `.env` dosyanızı oluşturup gerekli API anahtarlarını tanımlayın.

### LinkedIn Company Finder Endpoint

Backend artık şirket adından LinkedIn sayfasını bulmak için `/find_linkedin`
endpoint'ini sunar.

```
GET /find_linkedin?company=OpenAI
```

İsteğe bağlı `contacts=true` parametresi eklenirse, sayfadaki herkese açık
çalışan kartları da toplanır.
