# InsightChain — Agent ve Tool Tanımları

Ajanlar, platformun çekirdek işlevlerini modüler şekilde üstlenir. Her ajan kendi klasöründe yer alır ve ihtiyaç duyduğu araçlara (`tools/`) erişir.

## 1. Search Agent
- **Görev:** Şirket/sektör/website arama ve ilk veri toplama
- **Kullandığı Tool’lar:** BingSearch, GoogleSearch, DuckDuckGo, Company API
- **Örnek Kullanım:** `run_search(["open source ai"])`

## 2. Scraper Agent
- **Görev:** Web sitesinden/company page’den veri çıkarma (title, ürünler, iletişim, about, vs). GPT-4 kullanarak uygun scraping aracını seçer ve gerçek scraping işlemini tetikler.
- **Kullandığı Tool’lar:** staticscraper, jsrender, formbot, masscrawler, llmscraper

## 3. Enrichment Agent
- **Görev:** Firma LinkedIn, sosyal medya, ekstra email, telefon, karar verici isimleri bulma
- **Kullandığı Tool’lar:** LinkedInAPI, Hunter.io, Clearbit, Apollo API

## 4. Data Analyst Agent
- **Görev:** Toplanan veri üzerinde özet, bulgu, insight, aksiyon önerisi üretmek
- **Kullandığı Tool’lar:** LangChain LLM, özel prompt’lar, OpenAI Function calling

## 5. Orchestrator Agent
- **Görev:** Tüm agent’ları zincir halinde sırayla tetiklemek, veri akışını yönetmek, hata yönetimi
- **Kullandığı Tool’lar:** LangChain workflow, event dispatcher

## 6. Reporter Agent
- **Görev:** Analiz JSON'unu modern kart tabanlı HTML rapora dönüştürmek
- **Kullandığı Tool'lar:** newsfinder, linkedin_search, trend_fetcher, product_catalogue, web_search

---

Bu dosya, projenin ilerlemesiyle sürekli güncellenecek. Her yeni agent ve workflow burada tarif edilecek.

