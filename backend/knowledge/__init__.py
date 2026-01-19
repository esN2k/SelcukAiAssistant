"""
Knowledge package for domain-specific information
"""
from .domain_knowledge import (
    DOMAIN_KNOWLEDGE,
    detect_domain,
    boost_priority_documents,
    get_domain_info,
    suggest_domain
)

__all__ = [
    'DOMAIN_KNOWLEDGE',
    'detect_domain',
    'boost_priority_documents',
    'get_domain_info',
    'suggest_domain'
]
