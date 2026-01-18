# RAG (Kaynak Destekli Yanıtlar)

RAG (Geri Getirim Destekli Üretim), modelin yanıtlarını kaynak belgelerle
desteklemesini sağlar. Bu sayede akademik doğruluk artar ve kaynak gösterimi
kolaylaşır.

## 1) Genel Akış
```
Soru -> Gömme -> FAISS -> En yakın parçalar -> İstem -> Yanıt + Kaynaklar
```

## 2) İndeksleme (İçe Aktarım)
Komut satırı aracı: `backend/rag_ingest.py`

Örnek:
```bash
cd backend
python rag_ingest.py --input ../docs --output ./data/rag
```

## 2.1) İndeks Yenileme Rutini
Dokümanlar güncellendiğinde indeksi sıfırlayıp yeniden üretmek için:
```bash
cd backend
powershell -ExecutionPolicy Bypass -File refresh_rag_index.ps1
```

Alternatif olarak aynı komutu doğrudan çalıştırabilirsiniz:
```bash
cd backend
python rag_ingest.py --input data/rag/selcuk --output data/rag --reset
```

Repo kökünden tek komutla çalıştırmak için:
```bash
python backend/rag_ingest.py --input backend/data/rag/selcuk --output backend/data/rag --reset
```

Desteklenen formatlar:
- PDF
- TXT / MD
- HTML

Her parça için kaynak (dosya adı) ve sayfa bilgisi saklanır.

## 3) Arka Uç Ayarları (.env)
```
RAG_ENABLED=true
RAG_VECTOR_DB_PATH=./data/rag
RAG_TOP_K=4
RAG_EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
RAG_STRICT_DEFAULT=true
```

## 3.1) Bağımlılıklar
- **Gömme** üretimi için `sentence-transformers` ve `torch` gerekir.
- Windows’ta `WinError 126 / torch_python.dll` görülürse:
  - Microsoft Visual C++ 2015–2022 Redistributable kurulu olmalı.
  - Gerekirse CPU PyTorch sürümünü kurun (bkz. `docs/ops/SORUN_GIDERME.md`).

## 4) Katı Mod
- RAG açıkken kaynak bulunamazsa arka uç: **“Bu bilgi kaynaklarda yok.”** döner.
- İstek bazında `rag_strict` ile geçersiz kılınabilir.

## 5) Atıflar
- `/chat` cevabında `citations` alanı döner.
- `/chat/stream` sonunda `end` olayı içinde `citations` taşınır.

## 6) CI ile Otomatik Yenileme
`RAG Index Refresh` GitHub Actions işi, RAG dokumanlari guncellendiginde
indeksi otomatik yeniler ve `main` dalına commit eder.

Branch korumasi varsa, Actions'in `main` dalina push atabilmesi icin:
- Repo Settings → Actions → General → Workflow permissions: Read and write
- Branch protection/rulesets: `github-actions[bot]` icin bypass veya push izni
- "Require pull request before merging" aciksa, Actions icin istisna tanimlayin
