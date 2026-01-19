"""
Domain Knowledge for Selçuk University
Provides domain-specific boosting and intent detection
"""
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

DOMAIN_KNOWLEDGE = {
    "exam_schedule": {
        "aliases": [
            "sınav", "exam", "final", "vize", "ara sınav", "bütünleme", 
            "mazeret sınavı", "sınav tarihi", "sınav takvimi"
        ],
        "related_terms": [
            "takvim", "tarih", "program", "ne zaman", "hangi gün",
            "başlangıç", "bitiş", "dönem"
        ],
        "priority_sources": [
            "akademik_takvim.pdf",
            "/akademik/Sayfalar/akademik_takvim.aspx",
            "egitim_ogretim_yonetmeligi.pdf",
            "akademik_yil"
        ],
        "boost_factor": 1.8,
        "description": "Sınav tarihleri ve akademik takvim"
    },
    "registration": {
        "aliases": [
            "kayıt", "başvuru", "tescil", "kesin kayıt", "ön kayıt",
            "registration", "enrollment"
        ],
        "related_terms": [
            "belge", "evrak", "gerekli", "şart", "koşul",
            "son tarih", "deadline"
        ],
        "priority_sources": [
            "ogrenci_isleri.pdf",
            "oidb.selcuk.edu.tr",
            "kayit_yonetmeligi"
        ],
        "boost_factor": 1.5,
        "description": "Kayıt ve başvuru işlemleri"
    },
    "curriculum": {
        "aliases": [
            "müfredat", "ders programı", "dersler", "curriculum",
            "course", "program"
        ],
        "related_terms": [
            "kredi", "akts", "zorunlu", "seçmeli", "ders içeriği"
        ],
        "priority_sources": [
            "bologna.selcuk.edu.tr",
            "akts.selcuk.edu.tr",
            "ders_programi"
        ],
        "boost_factor": 1.6,
        "description": "Müfredat ve ders programları"
    },
    "academic_calendar": {
        "aliases": [
            "akademik takvim", "takvim", "academic calendar",
            "yarıyıl", "dönem", "semester"
        ],
        "related_terms": [
            "başlangıç", "bitiş", "tatil", "ara", "kayıt"
        ],
        "priority_sources": [
            "akademik_takvim.pdf",
            "/akademik/Sayfalar/akademik_takvim.aspx"
        ],
        "boost_factor": 2.0,
        "description": "Akademik takvim ve önemli tarihler"
    },
    "regulations": {
        "aliases": [
            "yönetmelik", "mevzuat", "regulation", "yönerge"
        ],
        "related_terms": [
            "madde", "kural", "hak", "sorumluluk", "ceza"
        ],
        "priority_sources": [
            "mevzuat",
            "yonetmelik",
            "yonerge"
        ],
        "boost_factor": 1.4,
        "description": "Yönetmelikler ve mevzuat"
    },
    "campus_life": {
        "aliases": [
            "kampüs", "yurt", "yemek", "sosyal", "kulüp",
            "campus", "dormitory"
        ],
        "related_terms": [
            "tesis", "spor", "kütüphane", "aktivite", "etkinlik"
        ],
        "priority_sources": [
            "kyk.selcuk.edu.tr",
            "yemek.selcuk.edu.tr",
            "kampus"
        ],
        "boost_factor": 1.3,
        "description": "Kampüs yaşamı ve sosyal tesisler"
    },
    "international": {
        "aliases": [
            "erasmus", "farabi", "mevlana", "yurtdışı",
            "exchange", "international"
        ],
        "related_terms": [
            "değişim", "burs", "başvuru", "partner", "anlaşma"
        ],
        "priority_sources": [
            "erasmus.selcuk.edu.tr",
            "farabi.selcuk.edu.tr",
            "mevlana.selcuk.edu.tr",
            "uio.selcuk.edu.tr"
        ],
        "boost_factor": 1.5,
        "description": "Uluslararası değişim programları"
    }
}


def detect_domain(query: str) -> Optional[str]:
    """
    Query'nin hangi domain'e ait olduğunu belirle
    Returns: domain key or None
    """
    query_lower = query.lower()
    
    # Check each domain
    for domain, config in DOMAIN_KNOWLEDGE.items():
        # Check aliases
        if any(alias in query_lower for alias in config['aliases']):
            logger.info(f"🎯 Domain detected: {domain}")
            return domain
        
        # Check related terms (weaker match)
        related_matches = sum(1 for term in config['related_terms'] if term in query_lower)
        if related_matches >= 2:
            logger.info(f"🎯 Domain detected (related terms): {domain}")
            return domain
    
    return None


def boost_priority_documents(query: str, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Domain-specific boosting
    Increases scores for documents from priority sources
    """
    domain = detect_domain(query)
    
    if not domain:
        logger.debug("No specific domain detected, no boosting applied")
        return documents
    
    config = DOMAIN_KNOWLEDGE[domain]
    priority_sources = config['priority_sources']
    boost = config['boost_factor']
    
    boosted_count = 0
    for doc in documents:
        source = doc['metadata'].get('source', '')
        
        # Check if source matches any priority source
        if any(ps.lower() in source.lower() for ps in priority_sources):
            original_score = doc.get('score', 0)
            doc['score'] = original_score * boost
            doc['boosted'] = True
            doc['boost_factor'] = boost
            doc['boost_domain'] = domain
            boosted_count += 1
            
            source_short = source[:40] + '...' if len(source) > 40 else source
            logger.info(f"⬆️ Boosted {source_short} by {boost}x (domain: {domain})")
    
    if boosted_count > 0:
        # Re-sort by score
        documents = sorted(documents, key=lambda x: x.get('score', 0), reverse=True)
        logger.info(f"✅ Boosted {boosted_count} documents for domain: {domain}")
    
    return documents


def get_domain_info(domain: str) -> Optional[Dict[str, Any]]:
    """Get information about a specific domain"""
    return DOMAIN_KNOWLEDGE.get(domain)


def get_all_domains() -> List[str]:
    """Get list of all available domains"""
    return list(DOMAIN_KNOWLEDGE.keys())


def get_domain_description(domain: str) -> str:
    """Get human-readable description of a domain"""
    config = DOMAIN_KNOWLEDGE.get(domain)
    if config:
        return config.get('description', domain)
    return domain


def suggest_domain(query: str) -> Optional[Dict[str, Any]]:
    """
    Suggest a domain for a query with confidence score
    """
    query_lower = query.lower()
    suggestions = []
    
    for domain, config in DOMAIN_KNOWLEDGE.items():
        score = 0
        
        # Check aliases (strong match)
        alias_matches = sum(1 for alias in config['aliases'] if alias in query_lower)
        score += alias_matches * 2
        
        # Check related terms (weaker match)
        related_matches = sum(1 for term in config['related_terms'] if term in query_lower)
        score += related_matches * 0.5
        
        if score > 0:
            suggestions.append({
                'domain': domain,
                'score': score,
                'description': config['description'],
                'boost_factor': config['boost_factor']
            })
    
    if suggestions:
        # Return highest scoring domain
        best = max(suggestions, key=lambda x: x['score'])
        logger.info(f"🎯 Suggested domain: {best['domain']} (score: {best['score']:.1f})")
        return best
    
    return None


def filter_by_domain(query: str, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter documents to only include those relevant to detected domain
    More aggressive than boosting - actually removes irrelevant docs
    """
    domain = detect_domain(query)
    
    if not domain:
        return documents
    
    config = DOMAIN_KNOWLEDGE[domain]
    priority_sources = config['priority_sources']
    
    # Keep documents that match priority sources
    filtered = []
    for doc in documents:
        source = doc['metadata'].get('source', '')
        
        if any(ps.lower() in source.lower() for ps in priority_sources):
            filtered.append(doc)
    
    # If filtering removed everything, return original
    if not filtered:
        logger.warning(f"⚠️ Domain filtering removed all documents, returning original set")
        return documents
    
    logger.info(f"🔍 Domain filtering: {len(documents)} → {len(filtered)} documents")
    return filtered


# Export main functions
__all__ = [
    'DOMAIN_KNOWLEDGE',
    'detect_domain',
    'boost_priority_documents',
    'get_domain_info',
    'get_all_domains',
    'get_domain_description',
    'suggest_domain',
    'filter_by_domain'
]
