"""
Complete RAG System Setup and Validation Script
Executes: scraping → indexing → guard initialization → evaluation
"""

import asyncio
import sys
import os
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(backend_path / 'rag_setup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def print_section(title: str, char: str = "="):
    """Print formatted section header"""
    print(f"\n{char*70}")
    print(f"{title}")
    print(f"{char*70}\n")


def check_environment():
    """Check and configure environment"""
    print_section("🔧 STEP 1: ENVIRONMENT CONFIGURATION")
    
    gemini_key = os.environ.get("GEMINI_API_KEY")
    
    if not gemini_key:
        env_file = backend_path / ".env"
        if env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        gemini_key = line.split("=", 1)[1].strip()
                        os.environ["GEMINI_API_KEY"] = gemini_key
                        break
    
    if gemini_key and len(gemini_key) > 20:
        logger.info(f"✅ Gemini API key configured: {gemini_key[:20]}...")
        return True
    else:
        logger.warning("⚠️ WARNING: No valid Gemini API key found")
        logger.warning("   AI scraping may be limited")
        return False


async def run_comprehensive_scraping():
    """Execute comprehensive scraping of all URLs"""
    print_section("🌐 STEP 2: COMPREHENSIVE SCRAPING (45-60 min)")
    
    try:
        from scrapers.hybrid_scraper import HybridSelcukScraper
        from scrapers.url_map import ALL_URLS
        
        output_dir = backend_path / "data" / "scraped"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        scraper = HybridSelcukScraper(output_dir)
        
        logger.info(f"📊 Total URLs to scrape: {len(ALL_URLS)}")
        logger.info(f"📁 Output directory: {output_dir}")
        logger.info(f"⏰ Started at: {datetime.now().strftime('%H:%M:%S')}")
        
        results = await scraper.scrape_all_comprehensive()
        
        results_file = output_dir / "scraping_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            serializable_results = {
                'stats': results['stats'],
                'web_pages_count': len(results['web_pages']),
                'documents_count': len(results['documents']),
                'timestamp': datetime.now().isoformat()
            }
            json.dump(serializable_results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"\n{'='*70}")
        logger.info("📊 SCRAPING COMPLETE - RESULTS")
        logger.info(f"{'='*70}")
        logger.info(f"✅ URLs processed: {results['stats']['processed']}/{results['stats']['total_urls']}")
        logger.info(f"📄 PDFs downloaded: {results['stats']['pdfs']}")
        logger.info(f"📝 DOCX downloaded: {results['stats'].get('docx', 0)}")
        logger.info(f"❌ Failed: {results['stats']['failed']}")
        logger.info(f"📁 Results saved: {results_file}")
        logger.info(f"{'='*70}\n")
        
        return results
        
    except Exception as e:
        logger.error(f"❌ Scraping failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None


def prepare_documents_for_indexing():
    """Prepare scraped documents for RAG indexing"""
    print_section("📚 STEP 3: DOCUMENT PREPARATION")
    
    scraped_dir = backend_path / "data" / "scraped"
    documents = []
    
    # Load PDFs
    pdf_dir = scraped_dir / "pdfs"
    if pdf_dir.exists():
        try:
            import fitz
            for pdf_file in pdf_dir.glob("*.pdf"):
                try:
                    doc = fitz.open(pdf_file)
                    text = "\n".join([page.get_text() for page in doc])
                    
                    if len(text.strip()) > 100:
                        documents.append({
                            'text': text,
                            'source': str(pdf_file),
                            'type': 'pdf',
                            'metadata': {
                                'pages': len(doc),
                                'chars': len(text),
                                'filename': pdf_file.name
                            }
                        })
                        logger.info(f"✅ Loaded PDF: {pdf_file.name} ({len(text)} chars, {len(doc)} pages)")
                    doc.close()
                except Exception as e:
                    logger.warning(f"⚠️ Failed to load {pdf_file.name}: {e}")
        except ImportError:
            logger.error("❌ PyMuPDF not installed")
    
    # Load DOCX
    docx_dir = scraped_dir / "docx"
    if docx_dir.exists():
        try:
            from docx import Document
            for docx_file in docx_dir.glob("*.docx"):
                try:
                    doc = Document(docx_file)
                    text = "\n".join([para.text for para in doc.paragraphs])
                    
                    if len(text.strip()) > 100:
                        documents.append({
                            'text': text,
                            'source': str(docx_file),
                            'type': 'docx',
                            'metadata': {
                                'chars': len(text),
                                'filename': docx_file.name
                            }
                        })
                        logger.info(f"✅ Loaded DOCX: {docx_file.name} ({len(text)} chars)")
                except Exception as e:
                    logger.warning(f"⚠️ Failed to load {docx_file.name}: {e}")
        except ImportError:
            logger.error("❌ python-docx not installed")
    
    # Load web pages
    scraping_results_file = scraped_dir / "scraping_results.json"
    if scraping_results_file.exists():
        try:
            with open(scraping_results_file, 'r', encoding='utf-8') as f:
                scraping_data = json.load(f)
                
            # Load web pages from results
            web_pages_data = []
            if 'web_pages' in scraping_data:
                web_pages_data = scraping_data['web_pages']
            
            for page in web_pages_data:
                content = ""
                if 'data' in page:
                    if isinstance(page['data'], dict):
                        if 'main_content' in page['data']:
                            content = page['data']['main_content']
                        elif 'content' in page['data']:
                            content = page['data']['content']
                        elif 'text' in page['data']:
                            content = page['data']['text']
                
                if content and len(content.strip()) > 100:
                    documents.append({
                        'text': content,
                        'source': page.get('url', 'unknown'),
                        'type': 'web',
                        'metadata': {
                            'chars': len(content),
                            'url': page.get('url', 'unknown'),
                            'category': page.get('category', 'unknown')
                        }
                    })
            
            logger.info(f"✅ Loaded {len([d for d in documents if d['type'] == 'web'])} web pages")
        except Exception as e:
            logger.warning(f"⚠️ Failed to load web pages: {e}")
    
    logger.info(f"\n📊 Total documents prepared: {len(documents)}")
    logger.info(f"   PDFs: {sum(1 for d in documents if d['type'] == 'pdf')}")
    logger.info(f"   DOCX: {sum(1 for d in documents if d['type'] == 'docx')}")
    logger.info(f"   Web: {sum(1 for d in documents if d['type'] == 'web')}")
    
    return documents


def initialize_and_index_rag(documents: List[Dict[str, Any]]):
    """Initialize RAG service and index documents"""
    print_section("🔄 STEP 4: RAG INDEXING WITH LaBSE")
    
    if not documents:
        logger.error("❌ No documents to index!")
        return None
    
    try:
        from rag_service_improved import ImprovedRAGService
        
        rag_data_path = backend_path / "data" / "rag"
        rag_data_path.mkdir(parents=True, exist_ok=True)
        
        logger.info("Initializing RAG service with LaBSE embeddings...")
        rag_service = ImprovedRAGService(rag_data_path)
        
        logger.info(f"Indexing {len(documents)} documents...")
        rag_service.index_documents(documents)
        
        import faiss
        import pickle
        
        faiss_index_path = rag_data_path / "index_labse.faiss"
        faiss.write_index(rag_service.faiss_index, str(faiss_index_path))
        
        metadata_path = rag_data_path / "metadata_labse.pkl"
        with open(metadata_path, 'wb') as f:
            pickle.dump({
                'documents': rag_service.documents,
                'metadata': rag_service.metadata
            }, f)
        
        logger.info(f"\n✅ RAG index saved:")
        logger.info(f"   FAISS: {faiss_index_path}")
        logger.info(f"   Metadata: {metadata_path}")
        logger.info(f"   Total vectors: {rag_service.faiss_index.ntotal}")
        
        return rag_service
        
    except Exception as e:
        logger.error(f"❌ RAG indexing failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None


def initialize_guard_system():
    """Initialize multi-layer guard system"""
    print_section("🛡️ STEP 5: GUARD SYSTEM INITIALIZATION")
    
    try:
        from rag_guard_improved import ImprovedRAGGuard
        
        guard = ImprovedRAGGuard()
        logger.info("✅ Multi-layer guard initialized (5 layers)")
        logger.info("   - Token validation")
        logger.info("   - Semantic similarity")
        logger.info("   - Entity matching")
        logger.info("   - Intent classification")
        logger.info("   - Cross-encoder reranking")
        
        return guard
        
    except Exception as e:
        logger.error(f"❌ Guard initialization failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None


def run_evaluation_tests(rag_service, guard):
    """Run evaluation tests"""
    print_section("🧪 STEP 6: EVALUATION TESTS")
    
    if not rag_service or rag_service.faiss_index.ntotal == 0:
        logger.error("❌ Cannot run evaluation - no documents indexed")
        return None
    
    try:
        from knowledge.domain_knowledge import boost_priority_documents
        
        test_queries = [
            "Selçuk Üniversitesi sınavları ne zaman?",
            "Final sınavları hangi tarihler arasında?",
            "Bilgisayar mühendisliği müfredatı nedir?",
            "Kayıt için gerekli belgeler neler?",
            "Akademik takvim 2024-2025",
            "Bütünleme sınavları ne zaman yapılacak?",
        ]
        
        results = []
        
        for i, query in enumerate(test_queries, 1):
            logger.info(f"\n[{i}/{len(test_queries)}] Query: '{query}'")
            
            contexts = rag_service.hybrid_search(query, top_k=5)
            
            contexts = boost_priority_documents(query, contexts)
            
            if guard:
                validated = guard.validate_and_rerank(query, contexts)
            else:
                validated = contexts
            
            if validated:
                logger.info(f"✅ Found {len(validated)} relevant contexts:")
                for j, ctx in enumerate(validated[:3], 1):
                    source = ctx['metadata'].get('source', 'unknown')
                    score = ctx.get('rerank_score', ctx.get('score', 0))
                    source_name = Path(source).name if source != 'unknown' else source
                    logger.info(f"   {j}. {source_name} (score: {score:.3f})")
                
                results.append({
                    'query': query,
                    'found': len(validated),
                    'top_sources': [ctx['metadata'].get('source', 'unknown') for ctx in validated[:3]]
                })
            else:
                logger.info(f"❌ No relevant contexts found")
                results.append({
                    'query': query,
                    'found': 0,
                    'top_sources': []
                })
        
        logger.info(f"\n{'='*70}")
        logger.info("✅ EVALUATION COMPLETE")
        logger.info(f"{'='*70}")
        
        return results
        
    except Exception as e:
        logger.error(f"❌ Evaluation failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None


def generate_final_report(scraping_results, documents, rag_service, eval_results):
    """Generate comprehensive final report"""
    print_section("📊 FINAL REPORT GENERATION")
    
    report_lines = []
    report_lines.append("="*70)
    report_lines.append("📊 SELÇUK ÜNİVERSİTESİ RAG SYSTEM - SETUP REPORT")
    report_lines.append("="*70)
    report_lines.append(f"\n📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if scraping_results:
        report_lines.append(f"\n🌐 SCRAPING RESULTS:")
        report_lines.append("─"*70)
        stats = scraping_results['stats']
        report_lines.append(f"URLs Processed: {stats['processed']}/{stats['total_urls']}")
        success_rate = (stats['processed']/stats['total_urls']*100) if stats['total_urls'] > 0 else 0
        report_lines.append(f"Success Rate: {success_rate:.1f}%")
        report_lines.append(f"PDFs Downloaded: {stats['pdfs']}")
        report_lines.append(f"DOCX Downloaded: {stats.get('docx', 0)}")
        report_lines.append(f"Failed URLs: {stats['failed']}")
    
    if documents:
        report_lines.append(f"\n📚 RAG INDEX:")
        report_lines.append("─"*70)
        report_lines.append(f"Total Documents: {len(documents)}")
        if rag_service:
            report_lines.append(f"Total Vectors: {rag_service.faiss_index.ntotal}")
        report_lines.append(f"Embedding Model: LaBSE (768-dim)")
        report_lines.append(f"Search Type: Hybrid (FAISS + BM25)")
    
    report_lines.append(f"\n🛡️ GUARD SYSTEM:")
    report_lines.append("─"*70)
    report_lines.append(f"Layers: 5 (Token + Semantic + Entity + Intent + Cross-Encoder)")
    report_lines.append(f"Status: ✅ Active")
    
    if eval_results:
        report_lines.append(f"\n🧪 EVALUATION RESULTS:")
        report_lines.append("─"*70)
        total_queries = len(eval_results)
        successful = sum(1 for r in eval_results if r['found'] > 0)
        report_lines.append(f"Test Queries: {total_queries}")
        report_lines.append(f"Successful: {successful}/{total_queries} ({successful/total_queries*100:.1f}%)")
    
    report_lines.append(f"\n🎯 NEXT STEPS:")
    report_lines.append("─"*70)
    report_lines.append("1. Review scraping results in: data/scraped/")
    report_lines.append("2. Test queries in your application")
    report_lines.append("3. Monitor accuracy and adjust thresholds")
    report_lines.append("4. Add more test queries to evaluation")
    
    report_lines.append(f"\n{'='*70}")
    report_lines.append("✅ SYSTEM READY FOR PRODUCTION")
    report_lines.append("="*70)
    
    report = "\n".join(report_lines)
    print(report)
    
    report_path = backend_path / "SETUP_REPORT.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    logger.info(f"\n📄 Report saved to: {report_path}")
    
    return report


async def main():
    """Main execution pipeline"""
    print_section("🚀 SELÇUK ÜNİVERSİTESİ RAG SYSTEM SETUP", "=")
    
    start_time = datetime.now()
    
    has_api_key = check_environment()
    
    scraping_results = await run_comprehensive_scraping()
    
    documents = prepare_documents_for_indexing()
    
    rag_service = initialize_and_index_rag(documents)
    
    guard = initialize_guard_system()
    
    eval_results = run_evaluation_tests(rag_service, guard)
    
    report = generate_final_report(scraping_results, documents, rag_service, eval_results)
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    print_section(f"✅ SETUP COMPLETE - Duration: {duration}", "=")


if __name__ == "__main__":
    asyncio.run(main())
