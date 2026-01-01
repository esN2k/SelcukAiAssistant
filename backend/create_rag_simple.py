"""RAG index'i manuel olarak oluştur (torch olmadan)."""
import json
from pathlib import Path
import sys

# Basit metin index oluştur
data_dir = Path("data/rag/selcuk")
output_dir = Path("data/rag")
output_dir.mkdir(parents=True, exist_ok=True)

documents = []
for txt_file in data_dir.glob("*.txt"):
    content = txt_file.read_text(encoding='utf-8')
    
    # Basit chunking (500 karakter)
    chunks = []
    for i in range(0, len(content), 500):
        chunk = content[i:i+500]
        if chunk.strip():
            chunks.append(chunk)
    
    for idx, chunk in enumerate(chunks):
        doc = {
            "content": chunk,
            "source": txt_file.name,
            "chunk": idx + 1,
            "category": "selcuk_uni"
        }
        documents.append(doc)

# JSON olarak kaydet
metadata_file = output_dir / "metadata.json"
with open(metadata_file, 'w', encoding='utf-8') as f:
    json.dump({
        "documents": documents,
        "total": len(documents),
        "source": "manual_selcuk_data"
    }, f, ensure_ascii=False, indent=2)

print(f"✅ RAG metadata oluşturuldu: {metadata_file}")
print(f"📊 Toplam {len(documents)} chunk")
print("\n📝 İlk belge önizleme:")
if documents:
    print(documents[0]['content'][:200] + "...")
