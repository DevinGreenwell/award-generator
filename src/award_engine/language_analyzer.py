"""
Language analyzer for detecting inflated or exaggerated language in achievement descriptions.
Helps ensure scoring system isn't fooled by buzzwords or empty phrases.
"""

import re
import logging
from typing import List, Dict, Tuple, Set

logger = logging.getLogger(__name__)

# Inflated language patterns that often sound important but lack substance
INFLATED_INDICATORS = {
    'vague_superlatives': [
        'outstanding', 'exceptional', 'remarkable', 'extraordinary', 
        'phenomenal', 'unprecedented', 'unparalleled', 'superior',
        'excellent', 'superb', 'tremendous', 'fantastic', 'amazing',
        'incredible', 'awesome', 'great', 'wonderful', 'brilliant'
    ],
    
    'empty_buzzwords': [
        'synergy', 'leverage', 'optimize', 'paradigm', 'cutting-edge',
        'world-class', 'best-in-class', 'state-of-the-art', 'innovative',
        'revolutionary', 'game-changing', 'transformational', 'disruptive',
        'strategic', 'tactical', 'holistic', 'robust', 'scalable',
        'seamless', 'turnkey', 'mission-critical', 'enterprise-level',
        'next-generation', 'bleeding-edge', 'groundbreaking'
    ],
    
    'vague_actions': [
        'facilitated', 'coordinated', 'engaged', 'interfaced', 'liaised',
        'collaborated', 'partnered', 'supported', 'assisted', 'contributed',
        'participated', 'involved', 'helped', 'aided', 'enabled'
    ],
    
    'unquantified_claims': [
        'significant', 'substantial', 'considerable', 'numerous', 'various',
        'multiple', 'extensive', 'comprehensive', 'wide-ranging', 'broad',
        'vast', 'immense', 'enormous', 'huge', 'massive', 'major',
        'countless', 'many', 'several', 'some', 'few'
    ],
    
    'passive_language': [
        'was responsible for', 'was involved in', 'played a role in',
        'took part in', 'was part of', 'contributed to', 'assisted with',
        'helped with', 'supported the', 'participated in'
    ]
}

# Concrete, valuable language patterns
CONCRETE_INDICATORS = {
    'specific_metrics': [
        r'\d+%', r'\$[\d,]+', r'\d+\s*hours?', r'\d+\s*days?',
        r'\d+\s*personnel', r'\d+\s*people', r'\d+\s*members',
        r'saved\s+\$?[\d,]+', r'reduced.*by\s+\d+', r'increased.*by\s+\d+'
    ],
    
    'direct_actions': [
        'created', 'built', 'developed', 'implemented', 'designed',
        'established', 'launched', 'executed', 'completed', 'achieved',
        'delivered', 'produced', 'generated', 'resolved', 'fixed'
    ],
    
    'measurable_outcomes': [
        'resulting in', 'which led to', 'achieving', 'producing',
        'generating', 'saving', 'reducing', 'increasing', 'improving'
    ]
}


class LanguageAnalyzer:
    """Analyzes text for inflated language and assigns credibility scores."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def analyze_credibility(self, text: str) -> Tuple[float, Dict[str, List[str]]]:
        """
        Analyze text for inflated language and return credibility score.
        
        Args:
            text: Text to analyze
            
        Returns:
            Tuple of (credibility_multiplier, findings_dict)
            credibility_multiplier: 0.5 to 1.0 (1.0 = highly credible, 0.5 = highly inflated)
        """
        if not text:
            return 1.0, {}
        
        text_lower = text.lower()
        findings = {
            'inflated_terms': [],
            'vague_claims': [],
            'concrete_evidence': [],
            'specific_metrics': []
        }
        
        # Count inflated language
        inflated_count = 0
        
        # Check vague superlatives
        for term in INFLATED_INDICATORS['vague_superlatives']:
            if term in text_lower and not self._has_supporting_evidence(text_lower, term):
                inflated_count += 1
                findings['inflated_terms'].append(term)
        
        # Check empty buzzwords
        for term in INFLATED_INDICATORS['empty_buzzwords']:
            if term in text_lower:
                inflated_count += 1
                findings['inflated_terms'].append(term)
        
        # Check unquantified claims
        for term in INFLATED_INDICATORS['unquantified_claims']:
            if term in text_lower and not self._has_quantification_nearby(text_lower, term):
                inflated_count += 0.5  # Less penalty than pure buzzwords
                findings['vague_claims'].append(term)
        
        # Check passive language
        for phrase in INFLATED_INDICATORS['passive_language']:
            if phrase in text_lower:
                inflated_count += 0.3  # Minor penalty for passive voice
        
        # Count concrete evidence
        concrete_count = 0
        
        # Check for specific metrics
        for pattern in CONCRETE_INDICATORS['specific_metrics']:
            matches = re.findall(pattern, text_lower)
            concrete_count += len(matches)
            findings['specific_metrics'].extend(matches)
        
        # Check for direct actions
        for term in CONCRETE_INDICATORS['direct_actions']:
            if term in text_lower:
                concrete_count += 0.5
                findings['concrete_evidence'].append(term)
        
        # Calculate credibility multiplier
        text_words = len(text.split())
        inflated_ratio = inflated_count / max(text_words / 10, 1)  # Normalize by text length
        concrete_ratio = concrete_count / max(text_words / 20, 1)
        
        # Start with base credibility
        credibility = 1.0
        
        # Reduce for inflated language (max reduction to 0.5)
        credibility -= min(0.5, inflated_ratio * 0.3)
        
        # Boost for concrete evidence (max boost of 0.2)
        credibility += min(0.2, concrete_ratio * 0.1)
        
        # Ensure credibility stays in bounds
        credibility = max(0.5, min(1.0, credibility))
        
        # Log findings if significant inflation detected
        if credibility < 0.8:
            logger.info(f"Language inflation detected - credibility: {credibility:.2f}")
            logger.debug(f"Inflated terms: {findings['inflated_terms'][:5]}")
            logger.debug(f"Vague claims: {findings['vague_claims'][:5]}")
        
        return credibility, findings
    
    def _has_supporting_evidence(self, text: str, term: str) -> bool:
        """Check if a superlative has supporting evidence nearby."""
        # Look for quantification within 50 characters of the term
        term_pos = text.find(term)
        if term_pos == -1:
            return False
        
        surrounding = text[max(0, term_pos-50):term_pos+50]
        
        # Check for numbers or specific outcomes
        if re.search(r'\d+', surrounding):
            return True
        
        # Check for specific results
        result_words = ['resulted', 'achieved', 'saved', 'reduced', 'increased', 'generated']
        return any(word in surrounding for word in result_words)
    
    def _has_quantification_nearby(self, text: str, term: str) -> bool:
        """Check if a vague quantifier has actual numbers nearby."""
        term_pos = text.find(term)
        if term_pos == -1:
            return False
        
        # Look within 30 characters
        surrounding = text[max(0, term_pos-30):term_pos+30]
        
        # Check for specific numbers
        return bool(re.search(r'\d+', surrounding))
    
    def adjust_score_for_language(self, base_score: float, text: str, 
                                  criterion: str = None) -> Tuple[float, str]:
        """
        Adjust a score based on language credibility analysis.
        
        Args:
            base_score: Original score (0-10 scale)
            text: Text to analyze
            criterion: Optional criterion name for specific adjustments
            
        Returns:
            Tuple of (adjusted_score, explanation)
        """
        credibility, findings = self.analyze_credibility(text)
        
        # Apply credibility multiplier
        adjusted_score = base_score * credibility
        
        # Additional adjustments for specific criteria
        if criterion == "impact" and len(findings['specific_metrics']) == 0:
            # Impact claims without metrics get extra penalty
            adjusted_score *= 0.8
            explanation = "Impact claims lack specific metrics"
        elif criterion == "leadership" and len(findings['vague_claims']) > 3:
            # Leadership with too many vague claims
            adjusted_score *= 0.85
            explanation = "Leadership claims lack specificity"
        elif criterion == "quantifiable_results" and len(findings['specific_metrics']) < 2:
            # Quantifiable results MUST have metrics
            adjusted_score *= 0.7
            explanation = "Insufficient quantifiable evidence"
        else:
            explanation = f"Language credibility: {credibility:.2f}"
        
        # Round to 1 decimal place
        adjusted_score = round(adjusted_score, 1)
        
        return adjusted_score, explanation