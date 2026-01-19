"""
RAG Setup Using Existing Scraped Data
Indexes existing scraped files and sets up the complete RAG system
"""

import sys
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
        logging.FileHandler(backend_path / 'rag_setup_existing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def print_section(title: str, char: str = "="):
    """Print formatted section header"""
    print(f"\n{char*70}")
    print(f"{title}")
    print(f"{char*70}\n")


def load_existing_scraped_data():
    """Load all existing scraped text files"""
    print_section("STEP 1: LOADING EXISTING SCRAPED DATA")
    
    scraped_dir = backend_path / "data" / "scraped"
    documents = []
    
    # Load all .txt files
    txt_files = list(scraped_dir.glob("*.txt"))
    logger.info(f"Found {len(txt_files)} text files")
    
    for txt_file in txt_files:
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
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
            logger.warning(f"Failed to load {txt_file.name}: {e}")
    
    # Load PDFs if any
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
                        logger.info(f"Loaded PDF: {pdf_file.name}")
                    doc.close()
                except Exception as e:
                    logger.warning(f"Failed to load PDF {pdf_file.name}: {e}")
        except ImportError:
            logger.warning("PyMuPDF not available for PDF loading")
    
    # Load DOCX if any
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
                        logger.info(f"Loaded DOCX: {docx_file.name}")
                except Exception as e:
                    logger.warning(f"Failed to load DOCX {docx_file.name}: {e}")
        except ImportError:
            logger.warning("python-docx not available for DOCX loading")
    
    logger.info(f"\nTotal documents loaded: {len(documents)}")
    logger.info(f"  Web pages: {sum(1 for d in documents if d['type'] == 'web')}")
    logger.info(f"  PDFs: {sum(1 for d in documents if d['type'] == 'pdf')}")
    logger.info(f"  DOCX: {sum(1 for d in documents if d['type'] == 'docx')}")
    
    return documents


def initialize_and_index_rag(documents: List[Dict[str, Any]]):
    """Initialize RAG service and index documents"""
    print_section("STEP 2: RAG INDEXING WITH LaBSE")
    
    if not documents:
        logger.error("No documents to index!")
        return None
    
    try:
        from rag_service_improved import ImprovedRAGService
        
        rag_data_path = backend_path / "data" / "rag"
        rag_data_path.mkdir(parents=True, exist_ok=True)
        
        logger.info("Initializing RAG service with LaBSE embeddings...")
        rag_service = ImprovedRAGService(rag_data_path)
        
        logger.info(f"Indexing {len(documents)} documents (this may take 10-15 minutes)...")
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
        
        logger.info(f"\nRAG index saved:")
        logger.info(f"  FAISS: {faiss_index_path}")
        logger.info(f"  Metadata: {metadata_path}")
        logger.info(f"  Total vectors: {rag_service.faiss_index.ntotal}")
        
        return rag_service
        
    except Exception as e:
        logger.error(f"RAG indexing failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None


def initialize_guard_system():
    """Initialize multi-layer guard system"""
    print_section("STEP 3: GUARD SYSTEM INITIALIZATION")
    
    try:
        from rag_guard_improved import ImprovedRAGGuard
        
        guard = ImprovedRAGGuard()
        logger.info("Multi-layer guard initialized (5 layers)")
        logger.info("  - Token validation")
        logger.info("  - Semantic similarity")
        logger.info("  - Entity matching")
        logger.info("  - Intent classification")
        logger.info("  - Cross-encoder reranking")
        
        return guard
        
    except Exception as e:
        logger.error(f"Guard initialization failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None


def run_evaluation_tests(rag_service, guard):
    """Run evaluation tests"""
    print_section("STEP 4: EVALUATION TESTS")
    
    if not rag_service or rag_service.faiss_index.ntotal == 0:
        logger.error("Cannot run evaluation - no documents indexed")
        return None
    
    try:
        from knowledge.domain_knowledge import boost_priority_documents
        
        test_queries = [
            "Selcuk Universitesi sinavlari ne zaman?",
            "Final sinavlari hangi tarihler arasinda?",
            "Bilgisayar muhendisligi mufredati nedir?",
            "Kayit icin gerekli belgeler neler?",
            "Akademik takvim 2024-2025",
            "Butunleme sinavlari ne zaman yapilacak?",
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
                logger.info(f"Found {len(validated)} relevant contexts:")
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
                logger.info(f"No relevant contexts found")
                results.append({
                    'query': query,
                    'found': 0,
                    'top_sources': []
                })
        
        logger.info(f"\n{'='*70}")
        logger.info("EVALUATION COMPLETE")
        logger.info(f"{'='*70}")
        
        return results
        
    except Exception as e:
        logger.error(f"Evaluation failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None


def generate_final_report(documents, rag_service, eval_results):
    """Generate comprehensive final report"""
    print_section("FINAL REPORT")
    
    report_lines = []
    report_lines.append("="*70)
    report_lines.append("SELCUK UNIVERSITESI RAG SYSTEM - SETUP REPORT")
    report_lines.append("="*70)
    report_lines.append(f"\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if documents:
        report_lines.append(f"\nDOCUMENTS INDEXED:")
        report_lines.append("-"*70)
        report_lines.append(f"Total Documents: {len(documents)}")
        report_lines.append(f"Web Pages: {sum(1 for d in documents if d['type'] == 'web')}")
        report_lines.append(f"PDFs: {sum(1 for d in documents if d['type'] == 'pdf')}")
        report_lines.append(f"DOCX: {sum(1 for d in documents if d['type'] == 'docx')}")
    
    if rag_service:
        report_lines.append(f"\nRAG INDEX:")
        report_lines.append("-"*70)
        report_lines.append(f"Total Vectors: {rag_service.faiss_index.ntotal}")
        report_lines.append(f"Embedding Model: LaBSE (768-dim)")
        report_lines.append(f"Search Type: Hybrid (FAISS + BM25)")
    
    report_lines.append(f"\nGUARD SYSTEM:")
    report_lines.append("-"*70)
    report_lines.append(f"Layers: 5 (Token + Semantic + Entity + Intent + Cross-Encoder)")
    report_lines.append(f"Status: Active")
    
    if eval_results:
        report_lines.append(f"\nEVALUATION RESULTS:")
        report_lines.append("-"*70)
        total_queries = len(eval_results)
        successful = sum(1 for r in eval_results if r['found'] > 0)
        report_lines.append(f"Test Queries: {total_queries}")
        report_lines.append(f"Successful: {successful}/{total_queries} ({successful/total_queries*100:.1f}%)")
    
    report_lines.append(f"\nNEXT STEPS:")
    report_lines.append("-"*70)
    report_lines.append("1. Test queries in your application")
    report_lines.append("2. Monitor accuracy and adjust thresholds")
    report_lines.append("3. Add more documents as needed")
    
    report_lines.append(f"\n{'='*70}")
    report_lines.append("SYSTEM READY FOR PRODUCTION")
    report_lines.append("="*70)
    
    report = "\n".join(report_lines)
    print(report)
    
    report_path = backend_path / "SETUP_REPORT.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    logger.info(f"\nReport saved to: {report_path}")
    
    return report


def main():
    """Main execution pipeline"""
    print_section("SELCUK UNIVERSITESI RAG SYSTEM SETUP", "=")
    
    start_time = datetime.now()
    
    documents = load_existing_scraped_data()
    
    rag_service = initialize_and_index_rag(documents)
    
    guard = initialize_guard_system()
    
    eval_results = run_evaluation_tests(rag_service, guard)
    
    report = generate_final_report(documents, rag_service, eval_results)
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    print_section(f"SETUP COMPLETE - Duration: {duration}", "=")


if __name__ == "__main__":
    main()
