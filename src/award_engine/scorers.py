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
        """Enhanced leadership scoring using dedicated leadership_details field - More stringent"""
        score = 0.0
        
        # Primary scoring from dedicated leadership_details field - STRICTER
        leadership_details = achievement_data.get('leadership_details', [])
        
        if len(leadership_details) >= 5:
            score += 3.5  # Exceptional leadership variety
        elif len(leadership_details) >= 4:
            score += 3.0  # Strong leadership
        elif len(leadership_details) >= 3:
            score += 2.5  # Good leadership
        elif len(leadership_details) >= 2:
            score += 2.0  # Some leadership
        elif len(leadership_details) >= 1:
            score += 1.5  # Minimal leadership
        
        # Bonus from training_provided field - REDUCED
        training_provided = achievement_data.get('training_provided', [])
        if len(training_provided) >= 3:
            score += 1.0  # Requires more training activities
        elif len(training_provided) >= 2:
            score += 0.5
        elif len(training_provided) >= 1:
            score += 0.25
        
        # Additional keyword analysis for context
        combined_text_lower = combined_text.lower()
        keyword_matches = sum(1 for keyword in LEADERSHIP_KEYWORDS['high'] + LEADERSHIP_KEYWORDS['medium'] 
                            if keyword in combined_text_lower)
        score += min(1.0, keyword_matches * 0.1)  # Max 1.0 bonus from keywords
        
        # Personnel number requirements - MORE REASONABLE
        personnel_numbers = re.findall(r'(\d+)\s*(?:people|personnel|staff|members|team|subordinates)', combined_text)
        if personnel_numbers:
            max_personnel = max([int(num) for num in personnel_numbers])
            if max_personnel >= 100:
                score += 2      # Large team
            elif max_personnel >= 50:
                score += 1.5    # Medium-large team
            elif max_personnel >= 25:
                score += 1      # Medium team
            elif max_personnel >= 10:
                score += 0.75   # Small-medium team
            elif max_personnel >= 5:
                score += 0.5    # Small team
            elif max_personnel >= 2:
                score += 0.25   # Very small team
        
        return normalize_score(score)
    
    @staticmethod
    def score_impact(achievement_data: dict, combined_text: str) -> float:
        """Enhanced impact scoring using dedicated impact field - More stringent"""
        score = 0.0
        combined_text_lower = combined_text.lower()
        
        # Primary scoring from impact field - REQUIRES MORE EVIDENCE
        impacts = achievement_data.get('impacts', [])
        
        # Check for concrete, measurable impacts
        measurable_impacts = 0
        for impact in impacts:
            if any(char.isdigit() for char in impact) or any(word in impact.lower() for word in ['percent', '%', 'saved', 'reduced', 'increased', 'eliminated']):
                measurable_impacts += 1
        
        # Score based on MEASURABLE impacts
        if measurable_impacts >= 4:
            score += 3.0  # Multiple measurable impacts
        elif measurable_impacts >= 3:
            score += 2.5
        elif measurable_impacts >= 2:
            score += 2.0
        elif measurable_impacts >= 1:
            score += 1.5
        
        # Credit for non-measurable impacts too
        non_measurable = len(impacts) - measurable_impacts
        score += min(1.0, non_measurable * 0.25)  # Max 1.0 for non-measurable
        
        # Keyword analysis - REDUCED WEIGHT
        high_count = sum(1 for keyword in IMPACT_KEYWORDS['high'] if keyword in combined_text_lower)
        medium_count = sum(1 for keyword in IMPACT_KEYWORDS['medium'] if keyword in combined_text_lower)
        
        if high_count >= 5:
            score += 0.75  # Requires more high-impact keywords
        elif high_count >= 3:
            score += 0.5
        elif high_count >= 2:
            score += 0.25
        
        if medium_count >= 5:
            score += 0.5   # Requires more medium-impact keywords
        elif medium_count >= 3:
            score += 0.25
        
        # Quantifiable impacts - MORE STRINGENT
        metrics = extract_quantifiable_metrics(combined_text)
        if len(metrics) >= 6:
            score += 1.5   # Requires 6+ quantifiable metrics
        elif len(metrics) >= 4:
            score += 1.0
        elif len(metrics) >= 2:
            score += 0.5
        # Less than 2 metrics = no bonus
        
        return normalize_score(score)
    
    @staticmethod
    def score_innovation(achievement_data: dict, combined_text: str) -> float:
        """Score innovation based on creative solutions - More stringent."""
        score = 0.0
        combined_text_lower = combined_text.lower()
        
        # Check for specific innovation details - REDUCED SCORES
        innovations = achievement_data.get('innovation_details', [])
        
        # Analyze quality of innovations
        significant_innovations = 0
        for innovation in innovations:
            if any(word in innovation.lower() for word in ['first', 'new', 'revolutionary', 'pioneered', 'created', 'developed', 'designed']):
                significant_innovations += 1
        
        if significant_innovations >= 3:
            score += 3.0  # Multiple significant innovations
        elif significant_innovations >= 2:
            score += 2.5
        elif significant_innovations >= 1:
            score += 2.0
        
        # Basic innovation credit
        basic_innovations = len(innovations) - significant_innovations
        score += min(1.5, basic_innovations * 0.5)
        
        # Count keyword occurrences - REDUCED WEIGHT
        keyword_matches = sum(1 for keyword in INNOVATION_KEYWORDS if keyword in combined_text_lower)
        score += min(1.0, keyword_matches * 0.1)  # Reduced from 0.2
        
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
        
        # Convert to 1-5 scale - MORE STRINGENT REQUIREMENTS
        if total_score >= 30:  # Multiple high-level indicators
            final_score = 5
        elif total_score >= 25:  # High-level + some medium
            final_score = 4.5
        elif total_score >= 20:   # Strong regional/area impact
            final_score = 4
        elif total_score >= 15:   # Clear multi-unit impact
            final_score = 3.5
        elif total_score >= 12:   # Sector/group level impact
            final_score = 3
        elif total_score >= 8:    # Clear unit-level impact
            final_score = 2.5
        elif total_score >= 5:    # Station/department level
            final_score = 2
        elif total_score >= 2:    # Team/division level
            final_score = 1.5
        else:                     # Individual level only
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
        """Enhanced quantifiable results scoring - Much more stringent"""
        score = 0.0
        
        # Primary scoring from quantifiable_metrics field - HIGHER REQUIREMENTS
        metrics = achievement_data.get('quantifiable_metrics', [])
        
        # Analyze quality of metrics (not just quantity)
        high_value_metrics = 0
        for metric in metrics:
            # Check for high-value indicators
            if any(indicator in metric.lower() for indicator in ['million', 'thousand', '%', 'percent', 'hours', 'days saved', 'cost savings', '$']):
                high_value_metrics += 1
        
        # Score based on HIGH-VALUE metrics
        if high_value_metrics >= 5:
            score += 4.0  # Exceptional quantification with significant values
        elif high_value_metrics >= 3:
            score += 3.5  # Strong quantification
        elif high_value_metrics >= 2:
            score += 2.5  # Some significant metrics
        elif high_value_metrics >= 1:
            score += 1.5  # At least one significant metric
        
        # Reduced credit for basic metrics
        basic_metrics = len(metrics) - high_value_metrics
        if basic_metrics >= 5:
            score += 1.0
        elif basic_metrics >= 3:
            score += 0.5
        elif basic_metrics >= 1:
            score += 0.25
        
        # Additional pattern matching - minimal bonus
        extracted_metrics = extract_quantifiable_metrics(combined_text)
        additional_count = len([m for m in extracted_metrics if m not in str(metrics)])
        
        if additional_count >= 3:
            score += 0.5  # Only reward if multiple additional metrics found
        
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
        Enhanced above-and-beyond scorer - MORE STRINGENT.
        """
        score = 0.0
        combined_text_lc = combined_text.lower()
        
        # Check for specific above_beyond_indicators from achievement data
        above_beyond_items = achievement_data.get('above_beyond_indicators', [])
        
        # Primary scoring based on concrete evidence
        if len(above_beyond_items) >= 3:
            score += 2.0  # Multiple concrete examples
        elif len(above_beyond_items) >= 2:
            score += 1.25
        elif len(above_beyond_items) >= 1:
            score += 0.75

        # Baseline adjectives - REDUCED WEIGHT
        if any(adj in combined_text_lc for adj in ABOVE_BEYOND_INDICATORS['baseline_adjectives']):
            score = max(score, 0.5)   # reduced from 1.5

        # Tiered indicators - STRICTER SCORING
        t1 = min(1, sum(1 for i in ABOVE_BEYOND_INDICATORS['tier1'] if i in combined_text_lc))
        t2 = min(2, sum(1 for i in ABOVE_BEYOND_INDICATORS['tier2'] if i in combined_text_lc))
        t3 = min(2, sum(1 for i in ABOVE_BEYOND_INDICATORS['tier3'] if i in combined_text_lc))
        t4 = min(3, sum(1 for i in ABOVE_BEYOND_INDICATORS['tier4'] if i in combined_text_lc))

        # Reduced multipliers
        score += t1 * 1.5    # heroic / superlative (reduced from 2.0)
        score += t2 * 1.0    # highly exceptional (reduced from 1.5)
        score += t3 * 0.5    # clearly above standard (reduced from 1.0)
        score += t4 * 0.25   # professional excellence (reduced from 0.5)

        # Voluntary time sacrifice bonus - REDUCED
        time_sacrifices = ['overtime', 'weekend', 'holiday', 'after hours', 'unpaid', 'personal time']
        time_bonus = 0.2 * sum(1 for w in time_sacrifices if w in combined_text_lc)  # Reduced from 0.3
        score += min(0.75, time_bonus)  # Reduced cap from 1.5

        # Quantified exceedance bonus - HIGHER BAR
        exceed_pct = re.findall(r'(\d+)\s*% (above|over|beyond|exceeded)', combined_text_lc)
        if exceed_pct:
            max_pct = max(int(p[0]) for p in exceed_pct)
            if max_pct >= 75:
                score += 1.0    # Requires 75%+ exceedance (was 50%)
            elif max_pct >= 50:
                score += 0.5    # Requires 50%+ exceedance (was 25%)
            elif max_pct >= 25:
                score += 0.25   # Requires 25%+ exceedance (was 10%)

        return normalize_score(score)