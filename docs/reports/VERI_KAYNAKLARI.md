# Veri Kaynakları ve Toplama Özeti

Bu dosyada RAG veri toplama süreci için kullanılan resmi kaynaklar ve oluşan veri seti özetlenmiştir.

## 1) Kaynak Alanı
- İzinli alan adı: `selcuk.edu.tr`

## 2) Başlangıç URL'leri
- https://www.selcuk.edu.tr/
- https://www.selcuk.edu.tr/ogrenci
- https://www.selcuk.edu.tr/akademik
- https://www.selcuk.edu.tr/idari
- https://www.selcuk.edu.tr/duyurular
- https://www.selcuk.edu.tr/dokumanlar
- https://www.selcuk.edu.tr/haberler

## 3) Site Haritası
- https://www.selcuk.edu.tr/sitemap.xml

## 4) Toplanan Veri İstatistikleri
- Ham HTML sayfa sayısı: `400`
- Temizlenmiş doküman sayısı: `400`
- FAISS indeksine eklenen parça sayısı: `1481`
- Kullanılan gömme modeli: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`

## 5) Depolama Konumları
- Ham içerik: `data/raw_web/html`
- Temizlenmiş içerik: `data/processed_web/docs`
- FAISS indeks: `data/rag`

## 6) Notlar
- Toplama sadece `selcuk.edu.tr` alan adları ile sınırlandırılmıştır.
- SSL doğrulama hataları gözlenirse `tools/collect_sources.py` içinde `--insecure` seçeneği kullanılmalıdır.
