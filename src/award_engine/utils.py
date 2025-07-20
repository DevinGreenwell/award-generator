"""
Utility functions for the Award Engine module.
"""

import re
import logging

logger = logging.getLogger(__name__)


def sent_tokenize(text):
    """Simple sentence tokenization fallback"""
    sentences = []
    for sent in text.split('.'):
        sent = sent.strip()
        if sent:
            sentences.append(sent)
    return sentences


# Try to import and use nltk for better sentence tokenization
try:
    import nltk
    try:
        nltk.download('punkt', quiet=True)
        from nltk.tokenize import sent_tokenize as nltk_sent_tokenize
        sent_tokenize = nltk_sent_tokenize  # Override with nltk version if available
        NLTK_AVAILABLE = True
    except (ImportError, ModuleNotFoundError, Exception):
        NLTK_AVAILABLE = False
        logger.info("NLTK not available, using fallback sentence tokenizer")
except (ImportError, ModuleNotFoundError, Exception):
    NLTK_AVAILABLE = False
    logger.info("NLTK not available, using fallback sentence tokenizer")


def bootstrap_fields(free_text: str) -> dict:
    """
    Populate minimal lists when only a narrative paragraph is provided.
    Relies on simple heuristics – no external LLM – so it is safe inside
    the award engine.
    """
    free_text_lc = free_text.lower()
    sents = sent_tokenize(free_text)
    
    # Initialize impacts list first
    impacts = []
    
    # Include social-media metric sentences even if number tokenization misses them
    social_sentences = [
        s for s in sents if any(tok in s.lower() for tok in ('view', 'views', 'follower', 'followers', 'reach'))
    ]
    for s in social_sentences:
        if s not in impacts:
            impacts.append(s)

    achievements = [s for s in sents if any(w in s.lower() for w in ('led', 'spearheaded', 'commanded'))]
    impacts.extend([s for s in sents if re.search(r'\d[\d,]*(?:\.\d+)?\s*(%|views|followers|\$)', s)])
    innovation_details = [s for s in sents if any(w in s.lower() for w in ('developed', 'created', 'pioneered', 'innovative'))]
    leadership_details = [s for s in sents if any(w in s.lower() for w in ('led', 'supervis', 'managed', 'commanded'))]
    quant_metrics = re.findall(r'\d[\d,]*(?:\.\d+)?\s*(?:%|views|followers|\$[\d,]+|hours|days)', free_text_lc)

    scope = ''
    for token in ('national', 'district', 'area', 'sector', 'unit'):
        if token in free_text_lc:
            scope = token
            break

    return {
        "achievements": achievements,
        "impacts": impacts,
        "innovation_details": innovation_details,
        "leadership_details": leadership_details,
        "quantifiable_metrics": quant_metrics,
        "scope": scope,
    }


def extract_quantifiable_metrics(text):
    """Extract quantifiable metrics from text."""
    metrics = []
    
    # Look for percentages
    percentages = re.findall(r'(\d+(?:\.\d+)?)\s*%', text)
    metrics.extend([f"{p}%" for p in percentages])
    
    # Look for dollar amounts
    dollars = re.findall(r'\$[\d,]+(?:\.\d{2})?', text)
    metrics.extend(dollars)
    
    # Look for time measurements
    time_saved = re.findall(r'(\d+)\s*(?:hours?|days?|weeks?|months?)', text)
    metrics.extend(time_saved)
    
    # Look for quantities
    quantities = re.findall(r'(\d+)\s*(?:lives|people|personnel|units|systems|processes)', text)
    metrics.extend(quantities)
    
    return metrics


def normalize_score(score, max_score=10.0):
    """Normalize a score to ensure it's within bounds (0-10 scale)."""
    return round(min(max_score, max(0, score)), 1)