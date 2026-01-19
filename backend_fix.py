#!/usr/bin/env python3
# backend_fix.py - Backend kritik hatalarını düzelt

import os
from pathlib import Path

print("BACKEND FIX SCRIPT")
print("="*60)

# FIX 1: .env dosyası oluştur/güncelle
print("\n1. .env dosyası düzeltiliyor...")
env_path = Path('.env')
env_content = []

if env_path.exists():
    with open(env_path, 'r', encoding='utf-8') as f:
        env_content = f.readlines()

# RAG_VECTOR_DB_PATH ekle/güncelle
rag_path_found = False
for i, line in enumerate(env_content):
    if line.startswith('RAG_VECTOR_DB_PATH'):
        env_content[i] = 'RAG_VECTOR_DB_PATH="data/rag/chromadb"\n'
        rag_path_found = True
        break

if not rag_path_found:
    env_content.append('RAG_VECTOR_DB_PATH="data/rag/chromadb"\n')

# RAG_ENABLED kontrol et
rag_enabled_found = any(line.startswith('RAG_ENABLED') for line in env_content)
if not rag_enabled_found:
    env_content.append('RAG_ENABLED=true\n')

# .env dosyasını kaydet
with open(env_path, 'w', encoding='utf-8') as f:
    f.writelines(env_content)

print("✓ .env dosyası güncellendi")

# FIX 2: RAG dizini oluştur
print("\n2. RAG dizini oluşturuluyor...")
rag_dir = Path('data/rag/chromadb')
rag_dir.mkdir(parents=True, exist_ok=True)
print(f"✓ {rag_dir} dizini oluşturuldu")

# FIX 3: Chat endpoint test senaryosu
print("\n3. Chat endpoint test formatı:")
print('''
DOĞRU FORMAT:
{
  "message": "Final sınavları ne zaman?",
  "user_id": "test_user",
  "session_id": "test_session"
}

YANLIŞ FORMAT (422 hatasına neden olur):
{
  "messages": [{"role": "user", "content": "..."}]
}
''')

print("="*60)
print("DÜZELTİLDİ! ✅")
print("\nŞimdi backend'i restart et:")
print("  python backend/main.py")
print("="*60)
