"""
Scoring methods for various achievement criteria.
"""

import re
import logging
from typing import Dict, List, Tuple
from .keywords import *
from .utils import normalize_score, extract_quantifiable_metrics

logger = logging.getLogger(__name__)


class CriteriaScorer:
    """Base class for scoring different criteria."""
    
    @staticmethod
    def score_leadership(achievement_data: dict, combined_text: str) -> float:
        """Enhanced leadership scoring using dedicated leadership_details field"""
        score = 0.0
        
        # Primary scoring from dedicated leadership_details field
        leadership_details = achievement_data.get('leadership_details', [])
        
        if len(leadership_details) >= 4:
            score += 3.0  # Exceptional leadership variety
        elif len(leadership_details) >= 3:
            score += 2.5  # Strong leadership
        elif len(leadership_details) >= 2:
            score += 2.0  # Good leadership
        elif len(leadership_details) >= 1:
            score += 1.5  # Some leadership
        
        # Bonus from training_provided field
        training_provided = achievement_data.get('training_provided', [])
        if len(training_provided) >= 2:
            score += 2.0
        elif len(training_provided) >= 1:
            score += 1.0
        
        # Additional keyword analysis for context
        combined_text_lower = combined_text.lower()
        keyword_matches = sum(1 for keyword in LEADERSHIP_KEYWORDS['high'] + LEADERSHIP_KEYWORDS['medium'] 
                            if keyword in combined_text_lower)
        score += min(1.0, keyword_matches * 0.1)  # Max 1.0 bonus from keywords
        
        # Personnel number requirements
        personnel_numbers = re.findall(r'(\d+)\s*(?:people|personnel|staff|members|team|subordinates)', combined_text)
        if personnel_numbers:
            max_personnel = max([int(num) for num in personnel_numbers])
            if max_personnel >= 100:
                score += 2
            elif max_personnel >= 50:
                score += 1.5
            elif max_personnel >= 25:
                score += 1
            elif max_personnel >= 10:
                score += 0.5
            elif max_personnel >= 5:
                score += 0.25
        
        return normalize_score(score)
    
    @staticmethod
    def score_impact(achievement_data: dict, combined_text: str) -> float:
        """Enhanced impact scoring using dedicated impact field"""
        score = 0.0
        combined_text_lower = combined_text.lower()
        
        # Primary scoring from impact field
        impacts = achievement_data.get('impacts', [])
        
        if len(impacts) >= 4:
            score += 3.0  # Exceptional impact
        elif len(impacts) >= 3:
            score += 2.5
        elif len(impacts) >= 2:
            score += 2.0
        elif len(impacts) >= 1:
            score += 1.0
        
        # Keyword analysis
        high_count = sum(1 for keyword in IMPACT_KEYWORDS['high'] if keyword in combined_text_lower)
        medium_count = sum(1 for keyword in IMPACT_KEYWORDS['medium'] if keyword in combined_text_lower)
        
        if high_count >= 4:
            score += 1.0
        elif high_count >= 3:
            score += 0.75
        elif high_count >= 2:
            score += 0.5
        
        if medium_count >= 3:
            score += 1.0
        elif medium_count >= 2:
            score += 0.75
        elif medium_count >= 1:
            score += 0.5
        
        # Quantifiable impacts
        metrics = extract_quantifiable_metrics(combined_text)
        if len(metrics) >= 5:
            score += 1.0
        elif len(metrics) >= 4:
            score += 0.75
        elif len(metrics) >= 3:
            score += 0.5
        
        return normalize_score(score)
    
    @staticmethod
    def score_innovation(achievement_data: dict, combined_text: str) -> float:
        """Score innovation based on creative solutions and new approaches."""
        score = 0.0
        combined_text_lower = combined_text.lower()
        
        # Check for specific innovation details
        innovations = achievement_data.get('innovation_details', [])
        if len(innovations) >= 3:
            score += 2.0
        elif len(innovations) >= 2:
            score += 1.5
        elif len(innovations) >= 1:
            score += 1.0
        
        # Count keyword occurrences
        keyword_matches = sum(1 for keyword in INNOVATION_KEYWORDS if keyword in combined_text_lower)
        score += min(3.0, keyword_matches * 0.2)
        
        return normalize_score(score)
    
    @staticmethod
    def score_scope(achievement_data: dict, combined_text: str) -> float:
        """Score scope based on reach and organizational impact using weighted scoring."""
        scope_text = achievement_data.get("scope", "").lower()
        combined_scope = scope_text + " " + combined_text.lower()
        
        # Calculate weighted score based on all matches found
        total_score = 0
        matches_found = []
        
        for indicator, points in SCOPE_INDICATORS.items():
            if indicator in combined_scope:
                total_score += points
                matches_found.append(f"{indicator}({points})")
        
        # If no specific indicators found, default to individual level
        if total_score == 0:
            total_score = 1
            matches_found = ["individual(1)"]
        
        # Convert to 1-5 scale with bonus for multiple scope levels
        if total_score >= 25:  # Multiple high-level indicators
            final_score = 5
        elif total_score >= 20:  # High-level + some medium
            final_score = 4.5
        elif total_score >= 15:   # Multiple medium-level
            final_score = 4
        elif total_score >= 12:   # Medium + some lower
            final_score = 3.5
        elif total_score >= 9:   # Some medium or multiple lower
            final_score = 3
        elif total_score >= 6:   # Single medium or multiple unit-level
            final_score = 2.5
        elif total_score >= 3:   # Single unit-level
            final_score = 2
        else:                    # Individual level only
            final_score = 1
        
        logger.debug(f"SCOPE ANALYSIS: Found {len(matches_found)} indicators: {matches_found}")
        logger.debug(f"SCOPE SCORING: Raw points: {total_score} → Final score: {final_score}/5")
        
        return normalize_score(final_score)
    
    @staticmethod
    def score_challenges(achievement_data: dict, combined_text: str) -> float:
        """Score based on challenges overcome."""
        score = 0.0
        combined_text_lower = combined_text.lower()
        
        # Check for specific challenge details
        challenges = achievement_data.get('challenges', [])
        score += min(3, len(challenges))  # Up to 3 points for specific challenges
        
        # Keyword analysis
        keyword_matches = sum(1 for keyword in CHALLENGE_KEYWORDS if keyword in combined_text_lower)
        score += min(2.0, keyword_matches * 0.1)
        
        return normalize_score(score)
    
    @staticmethod
    def score_quantifiable_results(achievement_data: dict, combined_text: str) -> float:
        """Enhanced quantifiable results scoring using dedicated metrics field"""
        score = 0.0
        
        # Primary scoring from quantifiable_metrics field
        metrics = achievement_data.get('quantifiable_metrics', [])
        
        if len(metrics) >= 5:
            score += 4.0  # Outstanding quantification
        elif len(metrics) >= 4:
            score += 3.5  # Excellent quantification
        elif len(metrics) >= 3:
            score += 3.0  # Good quantification
        elif len(metrics) >= 2:
            score += 2.5  # Some quantification
        elif len(metrics) >= 1:
            score += 1.5  # Limited quantification
        
        # Additional pattern matching for missed metrics
        extracted_metrics = extract_quantifiable_metrics(combined_text)
        additional_count = len([m for m in extracted_metrics if m not in str(metrics)])
        
        if additional_count > 0:
            score += min(1.0, additional_count * 0.2)
        
        return normalize_score(score)
    
    @staticmethod
    def score_valor(achievement_data: dict, combined_text: str) -> float:
        """Enhanced valor scoring using dedicated valor_indicators field"""
        score = 0.0
        combined_text_lower = combined_text.lower()
        
        # Primary scoring from valor_indicators field
        valor_items = achievement_data.get('valor_indicators', [])
        
        if len(valor_items) >= 2:
            score += 4.0  # Multiple valor actions
        elif len(valor_items) >= 1:
            score += 3.0  # Valor demonstrated
        
        # Keyword analysis
        keyword_matches = sum(1 for keyword in VALOR_KEYWORDS if keyword in combined_text_lower)
        score += min(2.0, keyword_matches * 0.3)  # Max 2.0 bonus from keywords
        
        return normalize_score(score)
    
    @staticmethod
    def score_collaboration(achievement_data: dict, combined_text: str) -> float:
        """Score collaboration and inter-agency work"""
        score = 0.0
        combined_text_lower = combined_text.lower()
        
        # Primary scoring from collaboration field
        collaboration_items = achievement_data.get('collaboration', [])
        
        if len(collaboration_items) >= 3:
            score += 3.0  # Extensive collaboration
        elif len(collaboration_items) >= 2:
            score += 2.0  # Good collaboration
        elif len(collaboration_items) >= 1:
            score += 1.0  # Some collaboration
        
        # Keyword analysis
        keyword_matches = sum(1 for keyword in COLLABORATION_KEYWORDS if keyword in combined_text_lower)
        score += min(2.0, keyword_matches * 0.2)  # Max 2.0 bonus from keywords
        
        return normalize_score(score)
    
    @staticmethod
    def score_training_provided(achievement_data: dict, combined_text: str) -> float:
        """Score training and knowledge transfer activities"""
        score = 0.0
        combined_text_lower = combined_text.lower()
        
        # Primary scoring from training_provided field
        training_items = achievement_data.get('training_provided', [])
        
        if len(training_items) >= 3:
            score += 3.0  # Extensive training role
        elif len(training_items) >= 2:
            score += 2.0  # Good training activity
        elif len(training_items) >= 1:
            score += 1.0  # Some training
        
        # Keyword analysis
        keyword_matches = sum(1 for keyword in TRAINING_KEYWORDS if keyword in combined_text_lower)
        score += min(2.0, keyword_matches * 0.2)  # Max 2.0 bonus from keywords
        
        return normalize_score(score)
    
    @staticmethod
    def score_emergency_response(achievement_data: dict, combined_text: str) -> float:
        """Score emergency response and crisis management"""
        score = 0.0
        combined_text_lower = combined_text.lower()
        
        # Primary scoring from emergency_response field
        emergency_items = achievement_data.get('emergency_response', [])
        
        if len(emergency_items) >= 2:
            score += 3.0  # Multiple emergency responses
        elif len(emergency_items) >= 1:
            score += 2.0  # Emergency response experience
        
        # Keyword analysis
        keyword_matches = sum(1 for keyword in EMERGENCY_KEYWORDS if keyword in combined_text_lower)
        score += min(3.0, keyword_matches * 0.3)  # Max 3.0 bonus from keywords
        
        return normalize_score(score)
    
    @staticmethod
    def score_above_beyond(achievement_data: dict, combined_text: str) -> float:
        """
        Enhanced above-and-beyond scorer with lenient scoring.
        """
        score = 0.0
        combined_text_lc = combined_text.lower()

        # Safety net adjectives
        if any(adj in combined_text_lc for adj in ABOVE_BEYOND_INDICATORS['baseline_adjectives']):
            score = max(score, 1.5)   # automatic baseline

        # Tiered indicators (relaxed caps & stronger multipliers)
        t1 = min(2, sum(1 for i in ABOVE_BEYOND_INDICATORS['tier1'] if i in combined_text_lc))
        t2 = min(2, sum(1 for i in ABOVE_BEYOND_INDICATORS['tier2'] if i in combined_text_lc))
        t3 = min(3, sum(1 for i in ABOVE_BEYOND_INDICATORS['tier3'] if i in combined_text_lc))
        t4 = min(4, sum(1 for i in ABOVE_BEYOND_INDICATORS['tier4'] if i in combined_text_lc))

        # Relaxed multipliers
        score += t1 * 2.0    # heroic / superlative
        score += t2 * 1.5    # highly exceptional
        score += t3 * 1.0    # clearly above standard
        score += t4 * 0.5    # professional excellence

        # Voluntary time sacrifice bonus
        time_sacrifices = ['overtime', 'weekend', 'holiday', 'after hours', 'unpaid', 'personal time']
        time_bonus = 0.3 * sum(1 for w in time_sacrifices if w in combined_text_lc)
        score += min(1.5, time_bonus)

        # Quantified exceedance bonus
        exceed_pct = re.findall(r'(\d+)\s*% (above|over|beyond|exceeded)', combined_text_lc)
        if exceed_pct:
            max_pct = max(int(p[0]) for p in exceed_pct)
            if max_pct >= 50:
                score += 1.0
            elif max_pct >= 25:
                score += 0.75
            elif max_pct >= 10:
                score += 0.5

        return normalize_score(score)