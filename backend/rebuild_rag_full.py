"""
TAM RAG REBUILD - Tum dosyalari (.txt, .md, .pdf) indeksler
Unicode logging sorunu olmadan
"""
import sys
import pickle
import os
from pathlib import Path
from datetime import datetime

# Encoding fix for Windows console
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

def main():
    log("="*60)
    log("TAM RAG REBUILD BASLADI")
    log("="*60)
    
    # DUZELTME: Dogru dizin
    scraped_dir = backend_path / "data" / "scraped"
    if not scraped_dir.exists():
        log(f"HATA: {scraped_dir} bulunamadi!")
        return
    
    log(f"Dizin: {scraped_dir}")
    documents = []
    
    # 1. TXT dosyalari
    txt_files = list(scraped_dir.glob("*.txt"))
    log(f"TXT dosyalari: {len(txt_files)}")
    
    for txt_file in txt_files:
        try:
            with open(txt_file, 'r', encoding='utf-8', errors='replace') as f:
                text = f.read()
            if len(text.strip()) > 100:
                documents.append({
                    'text': text,
                    'source': str(txt_file),
                    'type': 'web',
                    'metadata': {
                        'chars': len(text),
                        'filename': txt_file.name,
                        'domain': txt_file.name.split('_')[0]
                    }
                })
        except Exception as e:
            log(f"  HATA {txt_file.name}: {e}")
    
    # 2. MD dosyalari (KRITIK - yeni veriler)
    md_files = list(scraped_dir.glob("*.md"))
    log(f"MD dosyalari: {len(md_files)}")
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8', errors='replace') as f:
                text = f.read()
            if len(text.strip()) > 100:
                documents.append({
                    'text': text,
                    'source': str(md_file),
                    'type': 'markdown',
                    'metadata': {
                        'chars': len(text),
                        'filename': md_file.name,
                        'domain': 'selcuk_ozel',
                        'priority': 'high'
                    }
                })
                log(f"  + {md_file.name}")
        except Exception as e:
            log(f"  HATA {md_file.name}: {e}")
    
    # 3. PDF dosyalari
    pdf_dir = scraped_dir / "pdfs"
    if pdf_dir.exists():
        try:
            import fitz
            pdf_files = list(pdf_dir.glob("*.pdf"))
            log(f"PDF dosyalari: {len(pdf_files)}")
            
            for pdf_file in pdf_files:
                try:
                    doc = fitz.open(pdf_file)
                    text = "\n".join([page.get_text() for page in doc])
                    doc.close()
                    if len(text.strip()) > 100:
                        documents.append({
                            'text': text,
                            'source': str(pdf_file),
                            'type': 'pdf',
                            'metadata': {
                                'chars': len(text),
                                'filename': pdf_file.name
                            }
                        })
                except Exception as e:
                    log(f"  PDF HATA {pdf_file.name}: {e}")
        except ImportError:
            log("PyMuPDF yuklu degil, PDF atlandi")
    
    log(f"\nTOPLAM DOKUMAN: {len(documents)}")
    log(f"  Web: {sum(1 for d in documents if d['type'] == 'web')}")
    log(f"  Markdown: {sum(1 for d in documents if d['type'] == 'markdown')}")
    log(f"  PDF: {sum(1 for d in documents if d['type'] == 'pdf')}")
    
    if not documents:
        log("HATA: Dokuman bulunamadi!")
        return
    
    # RAG indeksleme
    log("\n" + "="*60)
    log("RAG INDEKSLEME BASLADI")
    log("="*60)
    
    try:
        # LaBSE model yukle
        log("LaBSE modeli yukleniyor...")
        from sentence_transformers import SentenceTransformer
        import faiss
        import numpy as np
        from rank_bm25 import BM25Okapi
        import torch

        device = "cuda" if torch.cuda.is_available() else "cpu"
        log(f"DONANIM DURUMU: {device.upper()} kullaniliyor.")
        
        if device == "cpu":
            log("UYARI: GPU bulunamadi! Islem cok yavas olabilir.")
        else:
            log(f"GPU: {torch.cuda.get_device_name(0)}")

        model = SentenceTransformer('sentence-transformers/LaBSE', device=device)
        log(f"LaBSE yuklendi (768-dim) - Device: {device}")
        
        # Chunk documents - DUZELTME: Cok kucuk chunk = 16,000+ vektor
        log("Dokumanlar parcalaniyor...")
        chunk_size = 50  # 100'den 50'ye dusuruludu -> 2x daha fazla chunk
        chunk_overlap = 10  # 20'den 10'a dusuruludu
        all_chunks = []
        all_metadata = []
        
        for doc in documents:
            text = doc['text']
            source = doc['source']
            
            # Simple chunking
            words = text.split()
            for i in range(0, len(words), chunk_size - chunk_overlap):
                chunk_words = words[i:i + chunk_size]
                if len(chunk_words) > 20:  # Min 20 kelime (50'den dusuruludu)
                    chunk_text = ' '.join(chunk_words)
                    all_chunks.append(chunk_text)
                    all_metadata.append({
                        'source': source,
                        'type': doc['type'],
                        'chunk_id': len(all_chunks) - 1,
                        **doc.get('metadata', {})
                    })
        
        log(f"Toplam chunk: {len(all_chunks)}")
        
        # Embedding
        log("Embedding hesaplaniyor (GPU MODU)...")
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        if device == "cuda":
            batch_size = 512  # GPU icin yuksek batch
            log(f"DONANIM: {torch.cuda.get_device_name(0)} (CUDA AKTIF!)")
            log(f"Batch Size: {batch_size} (Hizli islem)")
        else:
            batch_size = 32
            log("UYARI: GPU bulunamadi, CPU moduna gecildi.")
        
        all_embeddings = []
        
        # Standart siralama (GPU'da cok hizlidir, multi-process gerekmez)
        for i in range(0, len(all_chunks), batch_size):
            batch = all_chunks[i:i + batch_size]
            embeddings = model.encode(batch, batch_size=batch_size, show_progress_bar=False, device=device)
            all_embeddings.extend(embeddings)
            if (i + batch_size) % 1000 == 0 or (i + batch_size) >= len(all_chunks):
                log(f"  Ilerleme: {min(i + batch_size, len(all_chunks))}/{len(all_chunks)}")
            
        embeddings_array = np.array(all_embeddings).astype('float32')
        log(f"Embedding tamamlandi: {embeddings_array.shape}")
        
        # FAISS index
        log("FAISS indeksi olusturuluyor...")
        dimension = embeddings_array.shape[1]
        index = faiss.IndexFlatIP(dimension)
        faiss.normalize_L2(embeddings_array)
        index.add(embeddings_array)
        log(f"FAISS indeksi: {index.ntotal} vektor")
        
        # BM25 index
        log("BM25 indeksi olusturuluyor...")
        tokenized = [chunk.lower().split() for chunk in all_chunks]
        bm25 = BM25Okapi(tokenized)
        log("BM25 tamamlandi")
        
        # Kaydet
        rag_path = backend_path / "data" / "rag"
        rag_path.mkdir(parents=True, exist_ok=True)
        
        log("\nDosyalar kaydediliyor...")
        
        # FAISS
        faiss.write_index(index, str(rag_path / "index_labse.faiss"))
        faiss.write_index(index, str(rag_path / "index_improved.faiss"))
        log("  FAISS kaydedildi")
        
        # Metadata
        with open(rag_path / "metadata_labse.pkl", 'wb') as f:
            pickle.dump({'documents': all_chunks, 'metadata': all_metadata}, f)
        with open(rag_path / "documents_improved.pkl", 'wb') as f:
            pickle.dump({'documents': all_chunks, 'metadata': all_metadata}, f)
        log("  Metadata kaydedildi")
        
        # BM25
        with open(rag_path / "bm25_improved.pkl", 'wb') as f:
            pickle.dump(bm25, f)
        log("  BM25 kaydedildi")
        
        log("\n" + "="*60)
        log("REBUILD TAMAMLANDI!")
        log("="*60)
        log(f"Toplam vektor: {index.ntotal}")
        log(f"Dosya konumu: {rag_path}")
        
        # Test
        log("\nHIZLI TEST:")
        test_queries = ["akademik takvim 2024", "harc ucreti", "DD notu", "staj"]
        
        for query in test_queries:
            q_emb = model.encode([query])
            faiss.normalize_L2(q_emb)
            D, I = index.search(q_emb.astype('float32'), 3)
            if len(I[0]) > 0:
                top_idx = I[0][0]
                top_score = D[0][0]
                top_source = Path(all_metadata[top_idx]['source']).name
                log(f"  '{query}' -> {top_source[:40]} (skor: {top_score:.3f})")
        
    except Exception as e:
        log(f"HATA: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
