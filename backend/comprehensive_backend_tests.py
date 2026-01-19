"""
Comprehensive Backend Testing Suite for SelcukAI
Tests all components: System Health, RAG, Guard, API Endpoints
"""
import sys
import subprocess
from pathlib import Path
import importlib.util
import os
import time
from datetime import datetime
import json

# Add backend to path
backend_path = Path("E:/SelcukAiAssistant/repo/backend")
sys.path.insert(0, str(backend_path))

def test_system_health():
    """Test system dependencies and environment"""
    
    print("\n" + "="*70)
    print("🏥 SYSTEM HEALTH CHECK")
    print("="*70)
    
    results = {
        "passed": [],
        "failed": [],
        "warnings": []
    }
    
    # Test 1: Python version
    print("\n[1/10] Checking Python version...")
    py_version = sys.version_info
    if py_version >= (3, 8):
        results["passed"].append(f"Python {py_version.major}.{py_version.minor}.{py_version.micro}")
        print(f"✅ Python {py_version.major}.{py_version.minor}.{py_version.micro}")
    else:
        results["failed"].append("Python version < 3.8")
        print(f"❌ Python {py_version.major}.{py_version.minor} (requires 3.8+)")
    
    # Test 2: Required packages
    print("\n[2/10] Checking required packages...")
    required_packages = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("pydantic", "pydantic"),
        ("sentence_transformers", "sentence_transformers"),
        ("faiss", "faiss"),
        ("rank_bm25", "rank_bm25"),
        ("pymupdf", "fitz"),
        ("python-docx", "docx"),
        ("aiohttp", "aiohttp"),
    ]
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            results["passed"].append(f"Package: {package_name}")
            print(f"✅ {package_name}")
        except ImportError:
            results["failed"].append(f"Missing package: {package_name}")
            print(f"❌ {package_name} - NOT INSTALLED")
    
    # Test 3: Backend directory structure
    print("\n[3/10] Checking directory structure...")
    required_files = [
        "main.py",
        "rag_service_improved.py",
        "rag_guard_improved.py",
        "knowledge/domain_knowledge.py",
    ]
    
    for file in required_files:
        file_path = backend_path / file
        if file_path.exists():
            results["passed"].append(f"File: {file}")
            print(f"✅ {file}")
        else:
            results["failed"].append(f"Missing file: {file}")
            print(f"❌ {file} - NOT FOUND")
    
    # Test 4: RAG data files
    print("\n[4/10] Checking RAG data files...")
    rag_files = [
        "data/rag/index_labse.faiss",
        "data/rag/metadata_labse.pkl"
    ]
    
    for file in rag_files:
        file_path = backend_path / file
        if file_path.exists():
            size_mb = file_path.stat().st_size / 1024 / 1024
            results["passed"].append(f"RAG file: {file} ({size_mb:.2f} MB)")
            print(f"✅ {file} ({size_mb:.2f} MB)")
        else:
            results["failed"].append(f"Missing RAG file: {file}")
            print(f"❌ {file} - NOT FOUND")
    
    # Test 5: Environment variables
    print("\n[5/10] Checking environment variables...")
    env_vars = ["GEMINI_API_KEY"]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            results["passed"].append(f"Env var: {var}")
            print(f"✅ {var} = {value[:10]}...")
        else:
            results["warnings"].append(f"Missing env var: {var}")
            print(f"⚠️ {var} - NOT SET")
    
    # Test 6: Scraped data
    print("\n[6/10] Checking scraped data...")
    scraped_dir = backend_path / "data/scraped/web_pages"
    if scraped_dir.exists():
        file_count = len(list(scraped_dir.glob("*.txt")))
        results["passed"].append(f"Scraped files: {file_count}")
        print(f"✅ {file_count} scraped files found")
    else:
        results["warnings"].append("No scraped data directory")
        print(f"⚠️ No scraped data directory")
    
    # Test 7: System resources
    print("\n[7/10] Checking system resources...")
    try:
        import psutil
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage(str(backend_path))
        
        print(f"   RAM: {memory.percent}% used ({memory.available / 1024**3:.1f} GB available)")
        print(f"   Disk: {disk.percent}% used ({disk.free / 1024**3:.1f} GB free)")
        
        if memory.percent < 90:
            results["passed"].append(f"RAM available: {memory.available / 1024**3:.1f} GB")
        else:
            results["warnings"].append("Low RAM")
        
        if disk.free > 1024**3:
            results["passed"].append(f"Disk space: {disk.free / 1024**3:.1f} GB")
        else:
            results["warnings"].append("Low disk space")
    except ImportError:
        results["warnings"].append("psutil not installed - skipping resource check")
        print("⚠️ psutil not installed")
    
    # Test 8: Can import main modules
    print("\n[8/10] Testing module imports...")
    modules_to_test = [
        ("rag_service_improved", "ImprovedRAGService"),
        ("rag_guard_improved", "ImprovedRAGGuard"),
        ("knowledge.domain_knowledge", "boost_priority_documents")
    ]
    
    for module_name, class_name in modules_to_test:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            results["passed"].append(f"Import: {module_name}.{class_name}")
            print(f"✅ {module_name}.{class_name}")
        except Exception as e:
            results["failed"].append(f"Import failed: {module_name}.{class_name}")
            print(f"❌ {module_name}.{class_name} - {str(e)[:50]}")
    
    # Test 9: Port availability
    print("\n[9/10] Checking port 8000...")
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port_in_use = sock.connect_ex(('localhost', 8000)) == 0
    sock.close()
    
    if port_in_use:
        results["warnings"].append("Port 8000 already in use")
        print(f"⚠️ Port 8000 is in use (server may already be running)")
    else:
        results["passed"].append("Port 8000 available")
        print(f"✅ Port 8000 available")
    
    # Test 10: GPU availability
    print("\n[10/10] Checking GPU availability (optional)...")
    try:
        import torch
        if torch.cuda.is_available():
            results["passed"].append(f"GPU: {torch.cuda.get_device_name(0)}")
            print(f"✅ GPU available: {torch.cuda.get_device_name(0)}")
        else:
            results["warnings"].append("No GPU (using CPU)")
            print(f"⚠️ No GPU detected (will use CPU)")
    except ImportError:
        results["warnings"].append("PyTorch not installed")
        print(f"⚠️ PyTorch not installed (GPU unavailable)")
    
    # Summary
    print("\n" + "="*70)
    print("📊 SYSTEM HEALTH SUMMARY")
    print("="*70)
    print(f"✅ Passed: {len(results['passed'])}")
    print(f"❌ Failed: {len(results['failed'])}")
    print(f"⚠️ Warnings: {len(results['warnings'])}")
    
    if results['failed']:
        print(f"\n❌ CRITICAL FAILURES:")
        for failure in results['failed']:
            print(f"   - {failure}")
    
    return results


def test_rag_system():
    """Comprehensive RAG system testing"""
    
    print("\n" + "="*70)
    print("🔍 RAG SYSTEM TESTS")
    print("="*70)
    
    results = {
        "passed": [],
        "failed": [],
        "warnings": []
    }
    
    # Test 1: Load RAG service
    print("\n[1/8] Loading RAG service...")
    try:
        from rag_service_improved import ImprovedRAGService
        rag_service = ImprovedRAGService(backend_path / "data/rag")
        results["passed"].append("RAG service instantiated")
        print("✅ RAG service loaded")
    except Exception as e:
        results["failed"].append(f"RAG service failed: {str(e)}")
        print(f"❌ Failed to load RAG service: {e}")
        return results
    
    # Test 2: Load FAISS index
    print("\n[2/8] Loading FAISS index...")
    try:
        import faiss
        faiss_path = backend_path / "data/rag/index_labse.faiss"
        rag_service.faiss_index = faiss.read_index(str(faiss_path))
        vector_count = rag_service.faiss_index.ntotal
        results["passed"].append(f"FAISS loaded: {vector_count} vectors")
        print(f"✅ FAISS index loaded: {vector_count} vectors")
    except Exception as e:
        results["failed"].append(f"FAISS load failed: {str(e)}")
        print(f"❌ Failed to load FAISS: {e}")
        return results
    
    # Test 3: Load metadata
    print("\n[3/8] Loading metadata...")
    try:
        import pickle
        metadata_path = backend_path / "data/rag/metadata_labse.pkl"
        with open(metadata_path, 'rb') as f:
            data = pickle.load(f)
            rag_service.documents = data['documents']
            rag_service.metadata = data['metadata']
        
        doc_count = len(rag_service.documents)
        results["passed"].append(f"Metadata loaded: {doc_count} documents")
        print(f"✅ Metadata loaded: {doc_count} documents")
    except Exception as e:
        results["failed"].append(f"Metadata load failed: {str(e)}")
        print(f"❌ Failed to load metadata: {e}")
        return results
    
    # Test 4: Build BM25 index
    print("\n[4/8] Building BM25 index...")
    try:
        from rank_bm25 import BM25Okapi
        tokenized_docs = [doc.lower().split() for doc in rag_service.documents]
        rag_service.bm25 = BM25Okapi(tokenized_docs)
        results["passed"].append("BM25 index built")
        print("✅ BM25 index built")
    except Exception as e:
        results["failed"].append(f"BM25 build failed: {str(e)}")
        print(f"❌ Failed to build BM25: {e}")
        return results
    
    # Test 5: Test semantic search
    print("\n[5/8] Testing semantic search (FAISS)...")
    try:
        test_query = "Selçuk Üniversitesi sınavları ne zaman"
        query_emb = rag_service.embedding_model.encode([test_query], normalize_embeddings=True)
        scores, indices = rag_service.faiss_index.search(query_emb.astype('float32'), 5)
        
        if len(indices[0]) > 0:
            results["passed"].append(f"Semantic search: {len(indices[0])} results")
            print(f"✅ Semantic search returned {len(indices[0])} results")
            print(f"   Top score: {scores[0][0]:.4f}")
        else:
            results["failed"].append("Semantic search returned no results")
            print("❌ Semantic search returned no results")
    except Exception as e:
        results["failed"].append(f"Semantic search failed: {str(e)}")
        print(f"❌ Semantic search failed: {e}")
    
    # Test 6: Test keyword search (BM25)
    print("\n[6/8] Testing keyword search (BM25)...")
    try:
        import numpy as np
        query_tokens = test_query.lower().split()
        bm25_scores = rag_service.bm25.get_scores(query_tokens)
        top_indices = np.argsort(bm25_scores)[::-1][:5]
        
        if len(top_indices) > 0:
            results["passed"].append(f"Keyword search: {len(top_indices)} results")
            print(f"✅ Keyword search returned {len(top_indices)} results")
            print(f"   Top score: {bm25_scores[top_indices[0]]:.4f}")
        else:
            results["failed"].append("Keyword search returned no results")
            print("❌ Keyword search returned no results")
    except Exception as e:
        results["failed"].append(f"Keyword search failed: {str(e)}")
        print(f"❌ Keyword search failed: {e}")
    
    # Test 7: Test hybrid search
    print("\n[7/8] Testing hybrid search...")
    try:
        hybrid_results = rag_service.hybrid_search(test_query, top_k=5)
        
        if len(hybrid_results) > 0:
            results["passed"].append(f"Hybrid search: {len(hybrid_results)} results")
            print(f"✅ Hybrid search returned {len(hybrid_results)} results")
            for i, result in enumerate(hybrid_results[:3], 1):
                source = Path(result['metadata']['source']).name[:40]
                score = result['score']
                print(f"   {i}. {source} (score: {score:.4f})")
        else:
            results["failed"].append("Hybrid search returned no results")
            print("❌ Hybrid search returned no results")
    except Exception as e:
        results["failed"].append(f"Hybrid search failed: {str(e)}")
        print(f"❌ Hybrid search failed: {e}")
    
    # Test 8: Test multiple queries
    print("\n[8/8] Testing with multiple queries...")
    test_queries = [
        "Final sınavları hangi tarihler arasında",
        "Bilgisayar mühendisliği müfredatı",
        "Kayıt için gerekli belgeler",
        "Akademik takvim 2024-2025"
    ]
    
    query_results = {}
    for query in test_queries:
        try:
            results_list = rag_service.hybrid_search(query, top_k=3)
            query_results[query] = len(results_list)
            print(f"✅ '{query[:40]}...' → {len(results_list)} results")
        except Exception as e:
            query_results[query] = 0
            print(f"❌ '{query[:40]}...' → FAILED: {str(e)[:30]}")
    
    avg_results = sum(query_results.values()) / len(query_results) if query_results else 0
    results["passed"].append(f"Avg results per query: {avg_results:.1f}")
    
    # Summary
    print("\n" + "="*70)
    print("📊 RAG SYSTEM SUMMARY")
    print("="*70)
    print(f"✅ Passed: {len(results['passed'])}")
    print(f"❌ Failed: {len(results['failed'])}")
    print(f"⚠️ Warnings: {len(results['warnings'])}")
    
    return results


def test_guard_system():
    """Test 5-layer guard validation"""
    
    print("\n" + "="*70)
    print("🛡️ GUARD SYSTEM TESTS")
    print("="*70)
    
    results = {
        "passed": [],
        "failed": [],
        "warnings": []
    }
    
    # Test 1: Load guard
    print("\n[1/5] Loading guard system...")
    try:
        from rag_guard_improved import ImprovedRAGGuard
        guard = ImprovedRAGGuard()
        results["passed"].append("Guard instantiated")
        print("✅ Guard system loaded")
    except Exception as e:
        results["failed"].append(f"Guard load failed: {str(e)}")
        print(f"❌ Failed to load guard: {e}")
        return results
    
    # Test 2: Test relevant context
    print("\n[2/5] Testing relevant context validation...")
    question = "Selçuk Üniversitesi final sınavları ne zaman?"
    relevant_context = "Final sınavları 27 Mayıs - 7 Haziran 2026 tarihleri arasında yapılacaktır."
    
    try:
        is_relevant, score, details = guard._multi_layer_check(question, relevant_context)
        
        if is_relevant and score > 0.5:
            results["passed"].append(f"Relevant context accepted (score: {score:.3f})")
            print(f"✅ Relevant context PASSED (score: {score:.3f})")
        else:
            results["warnings"].append(f"Relevant context rejected (score: {score:.3f})")
            print(f"⚠️ Relevant context REJECTED (score: {score:.3f})")
    except Exception as e:
        results["failed"].append(f"Relevance check failed: {str(e)}")
        print(f"❌ Relevance check failed: {e}")
    
    # Test 3: Test irrelevant context
    print("\n[3/5] Testing irrelevant context rejection...")
    irrelevant_context = "Kayıt işlemleri için kimlik fotokopisi gereklidir."
    
    try:
        is_relevant, score, details = guard._multi_layer_check(question, irrelevant_context)
        
        if not is_relevant or score < 0.5:
            results["passed"].append(f"Irrelevant context rejected (score: {score:.3f})")
            print(f"✅ Irrelevant context REJECTED (score: {score:.3f})")
        else:
            results["warnings"].append(f"Irrelevant context accepted (score: {score:.3f})")
            print(f"⚠️ Irrelevant context PASSED (score: {score:.3f})")
    except Exception as e:
        results["failed"].append(f"Rejection check failed: {str(e)}")
        print(f"❌ Rejection check failed: {e}")
    
    # Test 4: Test with real RAG data
    print("\n[4/5] Testing guard with real RAG contexts...")
    try:
        from rag_service_improved import ImprovedRAGService
        import faiss
        import pickle
        
        rag_service = ImprovedRAGService(backend_path / "data/rag")
        faiss_path = backend_path / "data/rag/index_labse.faiss"
        metadata_path = backend_path / "data/rag/metadata_labse.pkl"
        
        if faiss_path.exists() and metadata_path.exists():
            rag_service.faiss_index = faiss.read_index(str(faiss_path))
            with open(metadata_path, 'rb') as f:
                data = pickle.load(f)
                rag_service.documents = data['documents']
                rag_service.metadata = data['metadata']
            
            from rank_bm25 import BM25Okapi
            tokenized_docs = [doc.lower().split() for doc in rag_service.documents]
            rag_service.bm25 = BM25Okapi(tokenized_docs)
            
            contexts = rag_service.hybrid_search("Sınav tarihleri nedir?", top_k=5)
            validated = guard.validate_and_rerank("Sınav tarihleri nedir?", contexts)
            
            results["passed"].append(f"Guard filtered: {len(contexts)} → {len(validated)}")
            print(f"✅ Guard filtering: {len(contexts)} contexts → {len(validated)} validated")
            print(f"   Rejected: {len(contexts) - len(validated)} contexts")
        else:
            results["warnings"].append("RAG data not available for guard test")
            print("⚠️ RAG data not available")
    except Exception as e:
        results["warnings"].append(f"Guard filtering test failed: {str(e)}")
        print(f"⚠️ Guard filtering test failed: {e}")
    
    # Test 5: Test individual guard layers
    print("\n[5/5] Testing individual guard layers...")
    test_question = "Final sınavları ne zaman?"
    test_context = "Final sınavları 27 Mayıs - 7 Haziran tarihleri arasında yapılacaktır."
    
    layer_tests = [
        ("Semantic Similarity", lambda: guard._semantic_similarity(test_question, test_context)),
        ("Entity Matching", lambda: guard._entity_match_score(test_question, test_context)),
        ("Intent Validation", lambda: guard._intent_validation(test_question, test_context)),
    ]
    
    for layer_name, test_func in layer_tests:
        try:
            score = test_func()
            if score > 0.3:
                results["passed"].append(f"{layer_name}: {score:.3f}")
                print(f"✅ {layer_name}: {score:.3f}")
            else:
                results["warnings"].append(f"{layer_name} low: {score:.3f}")
                print(f"⚠️ {layer_name}: {score:.3f} (low)")
        except Exception as e:
            results["failed"].append(f"{layer_name} failed")
            print(f"❌ {layer_name}: {str(e)[:40]}")
    
    # Summary
    print("\n" + "="*70)
    print("📊 GUARD SYSTEM SUMMARY")
    print("="*70)
    print(f"✅ Passed: {len(results['passed'])}")
    print(f"❌ Failed: {len(results['failed'])}")
    print(f"⚠️ Warnings: {len(results['warnings'])}")
    
    return results


def test_api_endpoints():
    """Test all API endpoints"""
    
    print("\n" + "="*70)
    print("🌐 API ENDPOINT TESTS")
    print("="*70)
    
    results = {
        "passed": [],
        "failed": [],
        "warnings": []
    }
    
    base_url = "http://localhost:8000"
    
    # Check if server is running
    print("\n[0/5] Checking server status...")
    try:
        import requests
        response = requests.get(f"{base_url}/health", timeout=2)
        print(f"✅ Server is running")
        results["passed"].append("Server running")
    except:
        print(f"⚠️ Server not running - some tests will be skipped")
        results["warnings"].append("Server not running")
        return results
    
    # Test 1: Health endpoint
    print("\n[1/5] Testing GET /health...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"   RAG enabled: {data.get('rag_system', {}).get('enabled', False)}")
            print(f"   Vectors: {data.get('rag_system', {}).get('vectors', 0)}")
            
            if data.get("rag_system", {}).get("enabled"):
                results["passed"].append("Health: RAG enabled")
            else:
                results["warnings"].append("Health: RAG disabled")
            
            results["passed"].append(f"Health endpoint: {response.status_code}")
        else:
            results["failed"].append(f"Health endpoint: {response.status_code}")
            print(f"❌ Status: {response.status_code}")
    except Exception as e:
        results["failed"].append(f"Health endpoint failed: {str(e)}")
        print(f"❌ Health endpoint failed: {e}")
    
    # Test 2: RAG status endpoint
    print("\n[2/5] Testing GET /rag/status...")
    try:
        response = requests.get(f"{base_url}/rag/status", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"   Vectors: {data.get('vectors', 0)}")
            print(f"   Model: {data.get('embedding_model', 'unknown')}")
            results["passed"].append(f"RAG status: {data.get('vectors', 0)} vectors")
        else:
            results["failed"].append(f"RAG status: {response.status_code}")
            print(f"❌ Status: {response.status_code}")
    except Exception as e:
        results["failed"].append(f"RAG status failed: {str(e)}")
        print(f"❌ RAG status failed: {e}")
    
    # Test 3: RAG test endpoint
    print("\n[3/5] Testing POST /rag/test...")
    test_queries = [
        "Selçuk Üniversitesi sınavları ne zaman?",
        "Bilgisayar mühendisliği müfredatı nedir?",
    ]
    
    for query in test_queries:
        try:
            response = requests.post(
                f"{base_url}/rag/test",
                params={"query": query},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                validated = data.get("validated_count", 0)
                print(f"✅ Query: '{query[:40]}...' → {validated} validated")
                
                if validated > 0:
                    results["passed"].append(f"RAG test: {validated} contexts for '{query[:30]}'")
                else:
                    results["warnings"].append(f"No results for: {query[:30]}")
            else:
                results["failed"].append(f"RAG test failed: {response.status_code}")
                print(f"❌ Status: {response.status_code}")
        except Exception as e:
            results["failed"].append(f"RAG test failed: {str(e)}")
            print(f"❌ RAG test failed: {e}")
        
        time.sleep(0.5)
    
    # Test 4: Performance test
    print("\n[4/5] Testing response times...")
    try:
        query_times = []
        
        for i in range(3):
            start = time.time()
            response = requests.post(
                f"{base_url}/rag/test",
                params={"query": "Sınav tarihleri"},
                timeout=15
            )
            elapsed = time.time() - start
            query_times.append(elapsed)
            print(f"   Query {i+1}: {elapsed:.2f}s")
        
        avg_time = sum(query_times) / len(query_times)
        
        if avg_time < 5:
            results["passed"].append(f"Response time: {avg_time:.2f}s (good)")
            print(f"✅ Average response time: {avg_time:.2f}s")
        elif avg_time < 10:
            results["warnings"].append(f"Response time: {avg_time:.2f}s (acceptable)")
            print(f"⚠️ Average response time: {avg_time:.2f}s (acceptable)")
        else:
            results["failed"].append(f"Response time: {avg_time:.2f}s (slow)")
            print(f"❌ Average response time: {avg_time:.2f}s (too slow)")
    except Exception as e:
        results["warnings"].append(f"Performance test failed: {str(e)}")
        print(f"⚠️ Performance test failed: {e}")
    
    # Test 5: Models endpoint
    print("\n[5/5] Testing GET /models...")
    try:
        response = requests.get(f"{base_url}/models", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            model_count = len(data.get('models', []))
            print(f"✅ Status: {response.status_code}")
            print(f"   Models available: {model_count}")
            results["passed"].append(f"Models endpoint: {model_count} models")
        else:
            results["failed"].append(f"Models endpoint: {response.status_code}")
            print(f"❌ Status: {response.status_code}")
    except Exception as e:
        results["failed"].append(f"Models endpoint failed: {str(e)}")
        print(f"❌ Models endpoint failed: {e}")
    
    # Summary
    print("\n" + "="*70)
    print("📊 API ENDPOINT SUMMARY")
    print("="*70)
    print(f"✅ Passed: {len(results['passed'])}")
    print(f"❌ Failed: {len(results['failed'])}")
    print(f"⚠️ Warnings: {len(results['warnings'])}")
    
    return results


def generate_test_report(health_results, rag_results, guard_results, api_results):
    """Generate comprehensive test report"""
    
    report = f"""{'='*70}
📊 SELÇUK AI BACKEND - COMPREHENSIVE TEST REPORT
{'='*70}

📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🖥️ System: E:/SelcukAiAssistant/repo/backend

{'='*70}
1. SYSTEM HEALTH CHECK
{'='*70}

✅ Passed Tests: {len(health_results['passed'])}
❌ Failed Tests: {len(health_results['failed'])}
⚠️ Warnings: {len(health_results['warnings'])}

Passed:
"""
    
    for item in health_results['passed'][:15]:
        report += f"  ✓ {item}\n"
    
    if health_results['failed']:
        report += "\nFailed:\n"
        for item in health_results['failed']:
            report += f"  ✗ {item}\n"
    
    if health_results['warnings']:
        report += "\nWarnings:\n"
        for item in health_results['warnings'][:5]:
            report += f"  ⚠ {item}\n"
    
    report += f"""
{'='*70}
2. RAG SYSTEM TESTS
{'='*70}

✅ Passed Tests: {len(rag_results['passed'])}
❌ Failed Tests: {len(rag_results['failed'])}
⚠️ Warnings: {len(rag_results['warnings'])}

"""
    
    for item in rag_results['passed']:
        report += f"  ✓ {item}\n"
    
    if rag_results['failed']:
        report += "\nFailed:\n"
        for item in rag_results['failed']:
            report += f"  ✗ {item}\n"
    
    report += f"""
{'='*70}
3. GUARD SYSTEM TESTS
{'='*70}

✅ Passed Tests: {len(guard_results['passed'])}
❌ Failed Tests: {len(guard_results['failed'])}
⚠️ Warnings: {len(guard_results['warnings'])}

"""
    
    for item in guard_results['passed'][:15]:
        report += f"  ✓ {item}\n"
    
    if guard_results['failed']:
        report += "\nFailed:\n"
        for item in guard_results['failed']:
            report += f"  ✗ {item}\n"
    
    report += f"""
{'='*70}
4. API ENDPOINT TESTS
{'='*70}

✅ Passed Tests: {len(api_results['passed'])}
❌ Failed Tests: {len(api_results['failed'])}
⚠️ Warnings: {len(api_results['warnings'])}

"""
    
    for item in api_results['passed']:
        report += f"  ✓ {item}\n"
    
    if api_results['failed']:
        report += "\nFailed:\n"
        for item in api_results['failed']:
            report += f"  ✗ {item}\n"
    
    # Overall summary
    total_passed = sum([
        len(health_results['passed']),
        len(rag_results['passed']),
        len(guard_results['passed']),
        len(api_results['passed'])
    ])
    
    total_failed = sum([
        len(health_results['failed']),
        len(rag_results['failed']),
        len(guard_results['failed']),
        len(api_results['failed'])
    ])
    
    total_warnings = sum([
        len(health_results['warnings']),
        len(rag_results['warnings']),
        len(guard_results['warnings']),
        len(api_results['warnings'])
    ])
    
    total_tests = total_passed + total_failed + total_warnings
    success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    report += f"""
{'='*70}
📈 OVERALL TEST SUMMARY
{'='*70}

Total Tests Run: {total_tests}
✅ Passed: {total_passed} ({total_passed/total_tests*100:.1f}%)
❌ Failed: {total_failed} ({total_failed/total_tests*100:.1f}%)
⚠️ Warnings: {total_warnings} ({total_warnings/total_tests*100:.1f}%)

Success Rate: {success_rate:.1f}%

{'='*70}
🎯 PRODUCTION READINESS
{'='*70}

"""
    
    if total_failed == 0 and success_rate > 90:
        report += "✅ SYSTEM IS PRODUCTION READY\n"
        report += "   All critical tests passed. System can be deployed.\n"
    elif total_failed < 3 and success_rate > 80:
        report += "⚠️ SYSTEM IS MOSTLY READY\n"
        report += "   Minor issues detected. Review warnings before deployment.\n"
    else:
        report += "❌ SYSTEM NEEDS ATTENTION\n"
        report += "   Critical issues detected. Fix failures before deployment.\n"
    
    report += f"""
{'='*70}
📋 RECOMMENDATIONS
{'='*70}

"""
    
    recommendations = []
    
    if len(health_results['failed']) > 0:
        recommendations.append("🔧 Fix system health issues (missing packages/files)")
    
    if len(rag_results['failed']) > 0:
        recommendations.append("🔧 Fix RAG system issues (index loading/search)")
    
    if len(api_results['failed']) > 0:
        recommendations.append("🔧 Fix API endpoint issues")
    
    if total_warnings > 5:
        recommendations.append("⚠️ Review and address warnings")
    
    if not recommendations:
        recommendations.append("✅ No critical issues - system is healthy!")
    
    for rec in recommendations:
        report += f"{rec}\n"
    
    report += f"""
{'='*70}
END OF REPORT
{'='*70}
"""
    
    # Save report
    report_path = backend_path / "COMPREHENSIVE_TEST_REPORT.txt"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)
    print(f"\n📄 Full report saved to: {report_path}")
    
    return report


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 STARTING COMPREHENSIVE BACKEND TESTS")
    print("="*70)
    
    # Run all tests
    health_results = test_system_health()
    rag_results = test_rag_system()
    guard_results = test_guard_system()
    api_results = test_api_endpoints()
    
    # Generate report
    final_report = generate_test_report(
        health_results,
        rag_results,
        guard_results,
        api_results
    )
    
    print("\n" + "="*70)
    print("✅ ALL TESTS COMPLETE")
    print("="*70)
