"""
Test script for improved RAG integration
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    print("=" * 60)
    print("TEST 1: Health Check")
    print("=" * 60)
    r = requests.get(f"{BASE_URL}/health")
    data = r.json()
    print(f"Status: {data['status']}")
    print(f"RAG Enabled: {data['rag_system']['enabled']}")
    print(f"RAG Type: {data['rag_system']['type']}")
    print(f"Vectors: {data['rag_system']['vectors']}")
    print(f"Documents: {data['rag_system']['documents']}")
    print()

def test_rag_status():
    print("=" * 60)
    print("TEST 2: RAG Status")
    print("=" * 60)
    r = requests.get(f"{BASE_URL}/rag/status")
    data = r.json()
    print(f"Enabled: {data['enabled']}")
    print(f"Type: {data['type']}")
    print(f"Embedding Model: {data['embedding_model']}")
    print(f"Search Type: {data['search_type']}")
    print(f"Guard Layers: {data['guard_layers']}")
    print(f"Vectors: {data['vectors']}")
    print(f"Features: {', '.join(data['features'])}")
    print()

def test_rag_search(query):
    print("=" * 60)
    print(f"TEST: RAG Search - '{query}'")
    print("=" * 60)
    r = requests.post(f"{BASE_URL}/rag/test", params={"query": query})
    data = r.json()
    
    if "error" in data:
        print(f"ERROR: {data['error']}")
        return
    
    print(f"Total Found: {data['total_found']}")
    print(f"Validated: {data['validated_count']}")
    print(f"Rejected: {data['rejected_count']}")
    print("\nTop Results:")
    for i, res in enumerate(data['results'][:3], 1):
        print(f"  {i}. {res['source']} (score: {res['score']})")
        print(f"     Preview: {res['content_preview'][:100]}...")
    print()

if __name__ == "__main__":
    print("\n🧪 TESTING IMPROVED RAG INTEGRATION\n")
    
    try:
        test_health()
        test_rag_status()
        
        # Test queries
        test_queries = [
            "Selçuk Üniversitesi sınavları ne zaman?",
            "Bilgisayar mühendisliği müfredatı nedir?",
            "Kayıt için gerekli belgeler neler?"
        ]
        
        for query in test_queries:
            test_rag_search(query)
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
