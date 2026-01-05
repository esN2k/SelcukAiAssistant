"""Bilgisayar Mühendisliği bölümünü scrape et."""
import asyncio
import json
from pathlib import Path
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup
import html2text


async def scrape_bilgisayar_muhendisligi():
    """Bilgisayar Mühendisliği ana sayfasını scrape et."""
    
    url = "https://www.selcuk.edu.tr/Birim/Bolum/teknoloji-bilgisayar_muhendisligi/15620"
    output_dir = Path("data/rag/scraped")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🌐 Scraping: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.get(url, timeout=30) as response:
                if response.status != 200:
                    print(f"❌ HTTP {response.status}: {url}")
                    return None
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Başlık
                title = soup.find('title')
                title_text = title.get_text(strip=True) if title else "Bilgisayar Mühendisliği"
                
                # Ana içerik
                main_content = soup.find('main') or soup.find('div', class_='content')
                
                # Script ve style temizle
                for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
                    tag.decompose()
                
                # HTML to Markdown
                h = html2text.HTML2Text()
                h.ignore_links = False
                h.ignore_images = True
                h.body_width = 0
                
                if main_content:
                    content_text = h.handle(str(main_content))
                else:
                    content_text = h.handle(html)
                
                # İletişim bilgileri
                email = soup.find('a', href=lambda x: x and 'mailto:' in x)
                email_text = email.get('href').replace('mailto:', '') if email else None
                
                phone_numbers = []
                for a in soup.find_all('a', href=lambda x: x and 'tel:' in x):
                    phone_numbers.append(a.get_text(strip=True))
                
                # Veri yapısı
                data = {
                    "url": url,
                    "title": title_text,
                    "scraped_at": datetime.now().isoformat(),
                    "category": "bilgisayar_muhendisligi",
                    "content": content_text,
                    "metadata": {
                        "faculty": "Teknoloji Fakültesi",
                        "location": "Alaeddin Keykubat Yerleşkesi",
                        "address": "Selçuk Üniversitesi Alaeddin Keykubat Yerleşkesi Teknoloji Fakültesi PK:42075 Selçuklu / KONYA",
                        "email": email_text or "tfdekanlik@selcuk.edu.tr",
                        "phones": phone_numbers,
                    }
                }
                
                # JSON kaydet
                json_file = output_dir / "bilgisayar_muhendisligi.json"
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                # Text kaydet
                text_file = output_dir / "bilgisayar_muhendisligi.txt"
                with open(text_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {title_text}\n\n")
                    f.write(f"**Kaynak:** {url}\n\n")
                    f.write("**Fakülte:** Teknoloji Fakültesi\n")
                    f.write("**Yerleşke:** Alaeddin Keykubat Yerleşkesi\n")
                    f.write("**Şehir:** Konya\n")
                    if email_text:
                        f.write(f"**E-posta:** {email_text}\n")
                    if phone_numbers:
                        f.write(f"**Telefonlar:** {', '.join(phone_numbers)}\n")
                    f.write("\n---\n\n")
                    f.write(content_text)
                
                print(f"✅ Kaydedildi: {json_file.name}")
                print(f"📄 İçerik: {len(content_text)} karakter")
                return data
                
        except asyncio.TimeoutError:
            print(f"⏱️ Timeout: {url}")
        except Exception as e:
            print(f"❌ Hata: {e}")
    
    return None


async def main():
    """Ana scraping fonksiyonu."""
    print("🚀 Bilgisayar Mühendisliği Web Scraping\n")
    
    data = await scrape_bilgisayar_muhendisligi()
    
    if data:
        print("\n" + "="*60)
        print("✅ Scraping tamamlandı!")
        print("="*60)
        print("📁 Dosyalar: data/rag/scraped/")
        print(f"📊 Toplam içerik: {len(data['content'])} karakter")
    else:
        print("\n❌ Scraping başarısız")


if __name__ == "__main__":
    asyncio.run(main())
