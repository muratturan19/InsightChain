# InsightChain — Agent ve Tool Tanımları

## 1. Search Agent
- Görev: Şirket/sektör/website arama ve ilk veri toplama
- Kullanılan Tool’lar: BingSearch, GoogleSearch, DuckDuckGo, Company API

## 2. Scraper Agent
- Görev: Web sitesinden/company page’den veri çıkarma (title, ürünler, iletişim, about, vs)
- Kullanılan Tool’lar: WebScraperTool, Requests, BeautifulSoup/Playwright

## 3. Enrichment Agent
- Görev: Firma LinkedIn, sosyal medya, ekstra email, telefon, karar verici isimleri bulma
- Kullanılan Tool’lar: LinkedInAPI, Hunter.io, Clearbit, Apollo API

## 4. Data Analyst Agent
- Görev: Toplanan veri üzerinde özet, bulgu, insight, aksiyon önerisi üretmek
- Kullanılan Tool’lar: LangChain LLM, özel prompt’lar, OpenAI Function calling

## 5. Orchestrator Agent
- Görev: Tüm agent’ları zincir halinde sırayla tetiklemek, veri akışını yönetmek, hata yönetimi
- Kullanılan Tool’lar: LangChain workflow, event dispatcher

---

## Her bir agent için:  
- Açıklama  
- Kullandığı tool’lar  
- Örnek output (JSON)  
- Zincirdeki yeri (1. step, 2. step...)

---

**Eklenebilecek Yeni Agent/Tool’lar**
- PDF, Excel, doküman tarayıcı
- E-posta toplayıcı
- Notion, Airtable, CRM entegrasyonları

---

Bu dosya, projenin ilerlemesiyle sürekli güncellenecek. Her yeni agent ve workflow burada tarif edilecek.

