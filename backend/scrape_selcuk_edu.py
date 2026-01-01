"""Selçuk Üniversitesi web sitelerinden veri toplama scripti.

Bu script Rektörlük izni ile üniversite sitelerinden akademik içerik toplar.
"""
import asyncio
import json
import logging
from pathlib import Path
from typing import List, Dict, Set
from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup
import html2text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SelcukEduScraper:
    """Selçuk Üniversitesi web scraper."""

    def __init__(self, output_dir: str = "data/rag/scraped"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Ana sayfa ve önemli bölümler
        self.base_urls = {
            "anasayfa": "https://www.selcuk.edu.tr",
            "bilgisayar": "https://bilgisayar.selcuk.edu.tr",
            "muhendislik": "https://muhendislik.selcuk.edu.tr",
            "akademik": "https://akademik.selcuk.edu.tr",
            "ogrenci": "https://ogrenci.selcuk.edu.tr",
            "hakkimizda": "https://www.selcuk.edu.tr/hakkimizda",
        }
        
        # İşlenecek sayfalar
        self.pages_to_scrape = [
            # Genel bilgiler
            "/hakkimizda/Pages/default.aspx",
            "/hakkimizda/tarihce/Pages/default.aspx",
            "/hakkimizda/misyon-vizyon/Pages/default.aspx",
            "/hakkimizda/rektorumuz/Pages/default.aspx",
            "/akademik/Pages/default.aspx",
            "/akademik/fakulteler/Pages/default.aspx",
            "/ogrenci/yeni-ogrenci/Pages/default.aspx",
            "/kampus-yasam/Pages/default.aspx",
            
            # Bilgisayar Mühendisliği
            "/hakkimizda/Pages/default.aspx",  # bilgisayar.selcuk.edu.tr
            "/akademik/Pages/default.aspx",
            "/lisans-programi/Pages/default.aspx",
            "/lisansustu/Pages/default.aspx",
            "/arastirma/Pages/default.aspx",
            "/mezunlar/Pages/default.aspx",
        ]
        
        self.visited: Set[str] = set()
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = False
        self.h2t.body_width = 0
        
    async def fetch_page(self, session: aiohttp.ClientSession, url: str) -> str:
        """Sayfa içeriğini al."""
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status == 200:
                    return await response.text()
                logger.warning(f"HTTP {response.status}: {url}")
                return ""
        except Exception as e:
            logger.error(f"Hata {url}: {e}")
            return ""
    
    def extract_text(self, html: str, url: str) -> Dict:
        """HTML'den metin ve metadata çıkar."""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Script, style, nav vb. gereksiz tagları temizle
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            tag.decompose()
        
        # Title
        title = soup.find('title')
        title_text = title.get_text().strip() if title else ""
        
        # Ana içerik
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
        if main_content:
            text = self.h2t.handle(str(main_content))
        else:
            text = self.h2t.handle(str(soup.body)) if soup.body else ""
        
        # Temizleme
        text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())
        
        return {
            "url": url,
            "title": title_text,
            "content": text,
            "scraped_at": datetime.now().isoformat(),
            "word_count": len(text.split()),
        }
    
    async def scrape_all(self):
        """Tüm sayfaları topla."""
        all_data = []
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            
            # Ana sayfa
            for name, base in self.base_urls.items():
                url = base
                if url not in self.visited:
                    self.visited.add(url)
                    tasks.append(self.scrape_page(session, url, name))
            
            # Bilgisayar Müh. sayfaları
            for page in self.pages_to_scrape:
                url = f"https://bilgisayar.selcuk.edu.tr{page}"
                if url not in self.visited:
                    self.visited.add(url)
                    tasks.append(self.scrape_page(session, url, "bilgisayar"))
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, dict) and result.get("content"):
                    all_data.append(result)
        
        # Kaydet
        output_file = self.output_dir / f"selcuk_edu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ {len(all_data)} sayfa toplandı: {output_file}")
        return all_data
    
    async def scrape_page(self, session: aiohttp.ClientSession, url: str, category: str) -> Dict:
        """Tek sayfa scrape."""
        logger.info(f"📄 Toplanan: {url}")
        html = await self.fetch_page(session, url)
        
        if not html:
            return {}
        
        data = self.extract_text(html, url)
        data["category"] = category
        
        # Dosyaya kaydet
        safe_filename = url.replace("https://", "").replace("/", "_").replace(":", "_")
        file_path = self.output_dir / f"{safe_filename}.txt"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"# {data['title']}\n\n")
            f.write(f"URL: {url}\n")
            f.write(f"Kategori: {category}\n\n")
            f.write(data['content'])
        
        return data


async def main():
    """Ana scraping fonksiyonu."""
    scraper = SelcukEduScraper()
    
    logger.info("🚀 Selçuk Üniversitesi veri toplama başlıyor...")
    logger.info("📋 Rektörlük izni ile akademik içerik toplanıyor")
    
    data = await scraper.scrape_all()
    
    logger.info(f"✅ Toplam {len(data)} sayfa işlendi")
    logger.info(f"📁 Veriler: {scraper.output_dir}")
    
    # İstatistikler
    total_words = sum(d.get("word_count", 0) for d in data)
    logger.info(f"📊 Toplam kelime: {total_words:,}")
    
    return data


if __name__ == "__main__":
    asyncio.run(main())
