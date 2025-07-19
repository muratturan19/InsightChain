InsightChain Dashboard UI & Design System Guide

Amaç

Tüm InsightChain platformunda tutarlı, şık ve profesyonel bir kullanıcı deneyimi sunmak.
Aşağıdaki kurallar, tüm UI geliştirmeleri için değiştirilemez referanstır.

1. Layout Yapısı (AppShell)

Header:

Full width, ekrandan ekrana uzanır, yüksekliği 64px.

Sol başta: Logo (renkli, yuvarlak veya minimal ikon) ve “InsightChain” markası.

Sağda: Dark mode toggle (🌙/☀️ ikonlu, yuvarlak buton, hover ve aktif animasyonlu).

Arka plan rengi: bg-white dark:bg-slate-800

Gölge: shadow-md

Yazı rengi: text-slate-900 dark:text-white

Padding: px-6 py-4

Logo için Tailwind: bg-blue-900 veya bg-red-500 gibi kurumsal renk.

Sidebar:

Sol tarafta sabit; genişlik w-64 (256px).

Tam ekran yüksekliği; overflow’da scroll.

Arka plan: bg-slate-100 dark:bg-slate-800

Menü başlıkları text-slate-600 dark:text-slate-300 font-semibold

Seçili menüde: bg-blue-100 dark:bg-blue-950 text-blue-700 dark:text-blue-400

Alt kısımda, küçük puntolu Sidebar placeholder alanı (açıklama veya footer)

Padding: px-4 py-8

Menü öğeleri arasında dikey boşluk: space-y-4

Border: border-r border-slate-200 dark:border-slate-700

Ana İçerik (Main Content):

Ortada, max-w-5xl genişliğinde, tam ortalanmış.

Tüm içerik büyük bir card içinde (bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-8).

Ana card içinde 2 katmanlı grid:

Üst grid (2 kolon):

Sağ:

“Ayarlar/filtreler” başlığı

Checkboxlar (accent-blue-600), label’lar text-slate-800 dark:text-slate-200

Kısa açıklamalar/placeholder metinler

Sol:

Web sitesi veya query için bir text input

Altında Sorgula/Run/Ara butonu (bg-blue-900 text-white, dark modda bg-blue-700)

Geniş, konforlu input ve büyük buton (height min 44px)

Alt grid:

Tek satır, tam genişlik

Burada oluşacak rapor/sonuç/feedback veya AI çıktısı gösterilir (p-4, bg-slate-50 dark:bg-slate-900 rounded-lg shadow-sm)

Grid arası boşluk: gap-8 veya daha geniş (kurumsal nefesli bir görünüm için)

2. Renk Paleti (Sadece Tailwind)
Ana Renk: blue-900 (#1e3a8a),
secondary olarak red-500 veya slate-900

Background: slate-50 (light), slate-900 (dark)

Card/White Area: white (light), slate-800 (dark)

Vurgu:

Butonlar: bg-blue-900 hover:bg-blue-700 active:bg-blue-800 text-white

Checkbox/Accent: accent-blue-600

Border: border-slate-200 dark:border-slate-700

Typography:

Başlıklar: text-slate-900 dark:text-white

Gövde: text-slate-700 dark:text-slate-300

Placeholder/metin: text-slate-400 dark:text-slate-500

3. Tipografi ve Spacing
Font: Tailwind’in varsayılanı (Inter, sans-serif)

Başlık: text-xl font-bold, alt başlıklar: text-base font-semibold

Kutu/Card:

Köşe: rounded-2xl

Gölge: shadow-md veya shadow-xl (ana card)

İç padding: cardlarda p-8, input/butonda px-4 py-2

Grid Boşluğu:

Üst grid: gap-8

Alt grid: mt-8

Buton-input arası: mb-4

4. Dark Mode
Tüm arka plan, metin, input ve butonlarda dark mode tam destekli.

Toggle ikonu ile veya Tailwind’in dark: sınıflarıyla aktive edilir.

Her component’te:

bg-* ve text-* ile hem light hem dark görünüm

Ör: bg-white dark:bg-slate-800, text-slate-900 dark:text-white

5. Responsive & Kurumsal Dokunuşlar
Tüm layout md ve üzeri için grid/flex, sm ve altında dikey yığılır (grid-cols-1 md:grid-cols-2)

Mobilde sidebar ve header otomatik olarak küçülür, menüye dönüşebilir (isteğe bağlı, ilk fazda sabit bırakılabilir)

Bileşenler arasında rahat nefes (padding/margin), arayüz “sıkışık” olmayacak

6. Komponentlere Dair
Header, Sidebar, MainCard, Input, Checkbox, Button, ReportArea tekil ve yalıtılmış component olacak

Ana state yönetimi ve veri akışı en dış componentte (App.tsx/MainLayout.tsx)

Placeholder componentleri sade ve açıklamalı şekilde tasarlanacak (ör: “Future filters here”)

7. UI Library
Ek olarak, shadcn/ui, DaisyUI veya benzeri modern React UI kütüphanesinden ilham alınabilir.

Sadece styling, layout ve component mantığı için, business logic sonradan eklenecek.


Summary & Golden Rule
Bu doküman, InsightChain UI/UX için değişmez kaynaktır.
Kod yazılırken, review edilirken veya yeni bir feature eklenirken burası referans alınmalı.
Herhangi bir eksik, farklılık ya da yeni tasarım ihtiyacı varsa önce bu dosya güncellenmeli, sonra kod yazılmalı.

Mükemmel, kurumsal, şık ve sürdürülebilir bir frontend için başka hiçbir detayı atlama!