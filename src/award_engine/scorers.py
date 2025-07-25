"""
Scoring methods for various achievement criteria.
Updated to use 10.0 scale and integrate language credibility analysis.
"""

import re
import logging
from typing import Dict, List, Tuple
from .keywords import *
from .utils import normalize_score, extract_quantifiable_metrics
from .language_analyzer import LanguageAnalyzer

logger = logging.getLogger(__name__)


class CriteriaScorer:
    """Base class for scoring different criteria with language analysis."""
    
    def __init__(self):
        """Initialize scorer with language analyzer."""
        self.language_analyzer = LanguageAnalyzer()
    
    def score_leadership(self, achievement_data: dict, combined_text: str) -> float:
        """Enhanced leadership scoring using 10-point scale with language analysis"""
        score = 0.0
        
        # Primary scoring from dedicated leadership_details field
        leadership_details = achievement_data.get('leadership_details', [])
        
        if len(leadership_details) >= 5:
            score += 7.0  # Exceptional leadership variety (doubled from 3.5)
        elif len(leadership_details) >= 4:
            score += 6.0  # Strong leadership (doubled from 3.0)
        elif len(leadership_details) >= 3:
            score += 5.0  # Good leadership (doubled from 2.5)
        elif len(leadership_details) >= 2:
            score += 4.0  # Some leadership (doubled from 2.0)
        elif len(leadership_details) >= 1:
            score += 3.0  # Minimal leadership (doubled from 1.5)
        
        # Bonus from training_provided field
        training_provided = achievement_data.get('training_provided', [])
        if len(training_provided) >= 3:
            score += 2.0  # Requires more training activities (doubled from 1.0)
        elif len(training_provided) >= 2:
            score += 1.0  # (doubled from 0.5)
        elif len(training_provided) >= 1:
            score += 0.5  # (doubled from 0.25)
        
        # Additional keyword analysis for context
        combined_text_lower = combined_text.lower()
        keyword_matches = sum(1 for keyword in LEADERSHIP_KEYWORDS['high'] + LEADERSHIP_KEYWORDS['medium'] 
                            if keyword in combined_text_lower)
        score += min(2.0, keyword_matches * 0.2)  # Max 2.0 bonus from keywords (doubled)
        
        # Personnel number requirements
        personnel_numbers = re.findall(r'(\d+)\s*(?:people|personnel|staff|members|team|subordinates)', combined_text)
        if personnel_numbers:
            max_personnel = max([int(num) for num in personnel_numbers])
            if max_personnel >= 100:
                score += 4.0    # Large team (doubled from 2)
            elif max_personnel >= 50:
                score += 3.0    # Medium-large team (doubled from 1.5)
            elif max_personnel >= 25:
                score += 2.0    # Medium team (doubled from 1)
            elif max_personnel >= 10:
                score += 1.5    # Small-medium team (doubled from 0.75)
            elif max_personnel >= 5:
                score += 1.0    # Small team (doubled from 0.5)
            elif max_personnel >= 2:
                score += 0.5    # Very small team (doubled from 0.25)
        
        # Apply language credibility check
        leadership_text = ' '.join(str(item) for item in leadership_details + training_provided)
        adjusted_score, explanation = self.language_analyzer.adjust_score_for_language(
            score, leadership_text + ' ' + combined_text, 'leadership'
        )
        
        if explanation and adjusted_score < score:
            logger.debug(f"Leadership score adjusted for language: {score:.1f} -> {adjusted_score:.1f} ({explanation})")
        
        return normalize_score(adjusted_score)
    
    def score_impact(self, achievement_data: dict, combined_text: str) -> float:
        """Enhanced impact scoring using 10-point scale with credibility checks"""
        score = 0.0
        combined_text_lower = combined_text.lower()
        
        # Primary scoring from impact field
        impacts = achievement_data.get('impacts', [])
        
        # Check for concrete, measurable impacts
        measurable_impacts = 0
        for impact in impacts:
            if any(char.isdigit() for char in impact) or any(word in impact.lower() for word in ['percent', '%', 'saved', 'reduced', 'increased', 'eliminated']):
                measurable_impacts += 1
        
        # Score based on MEASURABLE impacts
        if measurable_impacts >= 4:
            score += 6.0  # Multiple measurable impacts (doubled from 3.0)
        elif measurable_impacts >= 3:
            score += 5.0  # (doubled from 2.5)
        elif measurable_impacts >= 2:
            score += 4.0  # (doubled from 2.0)
        elif measurable_impacts >= 1:
            score += 3.0  # (doubled from 1.5)
        
        # Credit for non-measurable impacts too
        non_measurable = len(impacts) - measurable_impacts
        score += min(2.0, non_measurable * 0.5)  # Max 2.0 for non-measurable (doubled)
        
        # Keyword analysis
        high_count = sum(1 for keyword in IMPACT_KEYWORDS['high'] if keyword in combined_text_lower)
        medium_count = sum(1 for keyword in IMPACT_KEYWORDS['medium'] if keyword in combined_text_lower)
        
        if high_count >= 5:
            score += 1.5  # Requires more high-impact keywords (doubled from 0.75)
        elif high_count >= 3:
            score += 1.0  # (doubled from 0.5)
        elif high_count >= 2:
            score += 0.5  # (doubled from 0.25)
        
        if medium_count >= 5:
            score += 1.0   # Requires more medium-impact keywords (doubled from 0.5)
        elif medium_count >= 3:
            score += 0.5   # (doubled from 0.25)
        
        # Quantifiable impacts
        metrics = extract_quantifiable_metrics(combined_text)
        if len(metrics) >= 6:
            score += 3.0   # Requires 6+ quantifiable metrics (doubled from 1.5)
        elif len(metrics) >= 4:
            score += 2.0   # (doubled from 1.0)
        elif len(metrics) >= 2:
            score += 1.0   # (doubled from 0.5)
        
        # Apply language credibility check - especially important for impact
        impact_text = ' '.join(str(item) for item in impacts)
        adjusted_score, explanation = self.language_analyzer.adjust_score_for_language(
            score, impact_text + ' ' + combined_text, 'impact'
        )
        
        if explanation and adjusted_score < score:
            logger.debug(f"Impact score adjusted for language: {score:.1f} -> {adjusted_score:.1f} ({explanation})")
        
        return normalize_score(adjusted_score)
    
    def score_innovation(self, achievement_data: dict, combined_text: str) -> float:
        """Score innovation based on creative solutions - 10-point scale"""
        score = 0.0
        combined_text_lower = combined_text.lower()
        
        # Check for specific innovation details
        innovations = achievement_data.get('innovation_details', [])
        
        # Analyze quality of innovations
        significant_innovations = 0
        for innovation in innovations:
            if any(word in innovation.lower() for word in ['first', 'new', 'revolutionary', 'pioneered', 'created', 'developed', 'designed']):
                significant_innovations += 1
        
        if significant_innovations >= 3:
            score += 6.0  # Multiple significant innovations (doubled from 3.0)
        elif significant_innovations >= 2:
            score += 5.0  # (doubled from 2.5)
        elif significant_innovations >= 1:
            score += 4.0  # (doubled from 2.0)
        
        # Basic innovation credit
        basic_innovations = len(innovations) - significant_innovations
        score += min(3.0, basic_innovations * 1.0)  # (doubled from min 1.5, * 0.5)
        
        # Count keyword occurrences
        keyword_matches = sum(1 for keyword in INNOVATION_KEYWORDS if keyword in combined_text_lower)
        score += min(2.0, keyword_matches * 0.2)  # (doubled from min 1.0, * 0.1)
        
        # Apply language check - innovation claims often exaggerated
        innovation_text = ' '.join(str(item) for item in innovations)
        adjusted_score, explanation = self.language_analyzer.adjust_score_for_language(
            score, innovation_text + ' ' + combined_text, 'innovation'
        )
        
        return normalize_score(adjusted_score)
    
    def score_scope(self, achievement_data: dict, combined_text: str) -> float:
        """Score scope based on reach and organizational impact - 10-point scale"""
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
        
        # Convert to 1-10 scale (doubled thresholds)
        if total_score >= 30:  # Multiple high-level indicators
            final_score = 10.0
        elif total_score >= 25:  # High-level + some medium
            final_score = 9.0
        elif total_score >= 20:   # Strong regional/area impact
            final_score = 8.0
        elif total_score >= 15:   # Clear multi-unit impact
            final_score = 7.0
        elif total_score >= 12:   # Sector/group level impact
            final_score = 6.0
        elif total_score >= 8:    # Clear unit-level impact
            final_score = 5.0
        elif total_score >= 5:    # Station/department level
            final_score = 4.0
        elif total_score >= 2:    # Team/division level
            final_score = 3.0
        else:                     # Individual level only
            final_score = 2.0
        
        logger.debug(f"SCOPE ANALYSIS: Found {len(matches_found)} indicators: {matches_found}")
        logger.debug(f"SCOPE SCORING: Raw points: {total_score} → Final score: {final_score}/10")
        
        # Language check for inflated scope claims
        adjusted_score, explanation = self.language_analyzer.adjust_score_for_language(
            final_score, combined_scope, 'scope'
        )
        
        return normalize_score(adjusted_score)
    
    def score_challenges(self, achievement_data: dict, combined_text: str) -> float:
        """Score based on challenges overcome - 10-point scale"""
        score = 0.0
        combined_text_lower = combined_text.lower()
        
        # Check for specific challenge details
        challenges = achievement_data.get('challenges', [])
        score += min(6.0, len(challenges) * 2.0)  # Up to 6 points for specific challenges (doubled)
        
        # Keyword analysis
        keyword_matches = sum(1 for keyword in CHALLENGE_KEYWORDS if keyword in combined_text_lower)
        score += min(4.0, keyword_matches * 0.2)  # (doubled from min 2.0, * 0.1)
        
        # Apply language check
        challenge_text = ' '.join(str(item) for item in challenges)
        adjusted_score, explanation = self.language_analyzer.adjust_score_for_language(
            score, challenge_text + ' ' + combined_text, 'challenges'
        )
        
        return normalize_score(adjusted_score)
    
    def score_quantifiable_results(self, achievement_data: dict, combined_text: str) -> float:
        """Enhanced quantifiable results scoring - 10-point scale, very stringent"""
        score = 0.0
        
        # Primary scoring from quantifiable_metrics field
        metrics = achievement_data.get('quantifiable_metrics', [])
        
        # Analyze quality of metrics (not just quantity)
        high_value_metrics = 0
        for metric in metrics:
            # Check for high-value indicators
            if any(indicator in metric.lower() for indicator in ['million', 'thousand', '%', 'percent', 'hours', 'days saved', 'cost savings', '$']):
                high_value_metrics += 1
        
        # Score based on HIGH-VALUE metrics
        if high_value_metrics >= 5:
            score += 8.0  # Exceptional quantification (doubled from 4.0)
        elif high_value_metrics >= 3:
            score += 7.0  # Strong quantification (doubled from 3.5)
        elif high_value_metrics >= 2:
            score += 5.0  # Some significant metrics (doubled from 2.5)
        elif high_value_metrics >= 1:
            score += 3.0  # At least one significant metric (doubled from 1.5)
        
        # Reduced credit for basic metrics
        basic_metrics = len(metrics) - high_value_metrics
        if basic_metrics >= 5:
            score += 2.0  # (doubled from 1.0)
        elif basic_metrics >= 3:
            score += 1.0  # (doubled from 0.5)
        elif basic_metrics >= 1:
            score += 0.5  # (doubled from 0.25)
        
        # Additional pattern matching - minimal bonus
        extracted_metrics = extract_quantifiable_metrics(combined_text)
        additional_count = len([m for m in extracted_metrics if m not in str(metrics)])
        
        if additional_count >= 3:
            score += 1.0  # Only reward if multiple additional metrics found (doubled from 0.5)
        
        # Language check - quantifiable results must be credible
        metrics_text = ' '.join(str(item) for item in metrics)
        adjusted_score, explanation = self.language_analyzer.adjust_score_for_language(
            score, metrics_text + ' ' + combined_text, 'quantifiable_results'
        )
        
        return normalize_score(adjusted_score)
    
    def score_valor(self, achievement_data: dict, combined_text: str) -> float:
        """Valor scoring - ONLY for actual emergency response and life-saving actions - 10-point scale"""
        score = 0.0
        combined_text_lower = combined_text.lower()
        
        # Define strict valor indicators - actual emergency response only
        strict_valor_keywords = [
            'saved life', 'saved lives', 'life-saving action', 'heroic rescue',
            'water rescue', 'maritime rescue', 'helicopter rescue', 'boat rescue',
            'swimmer rescue', 'aviation rescue', 'search and rescue operation',
            'medevac', 'medical evacuation', 'casualty evacuation',
            'man overboard', 'person in water', 'drowning victim', 
            'hypothermia rescue', 'ice rescue', 'cliff rescue', 'mountain rescue',
            'swift water rescue', 'flood rescue', 'surf rescue', 'night rescue',
            'recovered survivors', 'extracted personnel', 'evacuated civilians',
            'rescued crew', 'pulled from wreckage', 'freed from entrapment',
            'rescued from fire', 'saved from drowning', 'prevented loss of life',
            'rescued from burning', 'rescued from sinking', 'emergency evacuation'
        ]
        
        # Check for actual life-saving/rescue actions
        life_saving_found = False
        rescue_count = 0
        
        for keyword in strict_valor_keywords:
            if keyword in combined_text_lower:
                life_saving_found = True
                rescue_count += 1
        
        # Also check for specific rescue numbers (e.g., "rescued 3 people")
        rescue_patterns = [
            r'rescued\s+(\d+)\s+(?:people|persons|individuals|crew|passengers|victims)',
            r'saved\s+(\d+)\s+(?:lives|people|persons|individuals)',
            r'evacuated\s+(\d+)\s+(?:people|persons|individuals|casualties)',
            r'recovered\s+(\d+)\s+(?:survivors|victims|people)'
        ]
        
        for pattern in rescue_patterns:
            matches = re.findall(pattern, combined_text_lower)
            if matches:
                life_saving_found = True
                rescue_count += len(matches)
        
        # Primary scoring from valor_indicators field - but verify they're actual emergencies
        valor_items = achievement_data.get('valor_indicators', [])
        verified_valor_items = []
        
        for item in valor_items:
            item_lower = str(item).lower()
            # Check if this is an actual emergency response
            if any(keyword in item_lower for keyword in ['rescue', 'saved', 'emergency', 'evacuation', 'life-saving']):
                verified_valor_items.append(item)
        
        # Score based on verified emergency response actions (10-point scale)
        if len(verified_valor_items) >= 2 and life_saving_found:
            score = 10.0  # Multiple verified life-saving actions (doubled from 5.0)
        elif len(verified_valor_items) >= 1 and life_saving_found:
            score = 8.0   # Verified life-saving action (doubled from 4.0)
        elif life_saving_found and rescue_count >= 2:
            score = 7.0   # Multiple rescue keywords found (doubled from 3.5)
        elif life_saving_found:
            score = 6.0   # Life-saving action found (doubled from 3.0)
        else:
            # No actual emergency response found
            score = 0.0
        
        # Log if valor score is being applied
        if score > 0:
            logger.info(f"Valor score applied: {score} (rescue_count: {rescue_count}, verified_items: {len(verified_valor_items)})")
        
        # No language adjustment for valor - either it happened or it didn't
        return normalize_score(score)
    
    def score_collaboration(self, achievement_data: dict, combined_text: str) -> float:
        """Score collaboration and inter-agency work - 10-point scale"""
        score = 0.0
        combined_text_lower = combined_text.lower()
        
        # Primary scoring from collaboration field
        collaboration_items = achievement_data.get('collaboration', [])
        
        if len(collaboration_items) >= 3:
            score += 6.0  # Extensive collaboration (doubled from 3.0)
        elif len(collaboration_items) >= 2:
            score += 4.0  # Good collaboration (doubled from 2.0)
        elif len(collaboration_items) >= 1:
            score += 2.0  # Some collaboration (doubled from 1.0)
        
        # Keyword analysis
        keyword_matches = sum(1 for keyword in COLLABORATION_KEYWORDS if keyword in combined_text_lower)
        score += min(4.0, keyword_matches * 0.4)  # Max 4.0 bonus from keywords (doubled)
        
        # Apply language check
        collab_text = ' '.join(str(item) for item in collaboration_items)
        adjusted_score, explanation = self.language_analyzer.adjust_score_for_language(
            score, collab_text + ' ' + combined_text, 'collaboration'
        )
        
        return normalize_score(adjusted_score)
    
    def score_training_provided(self, achievement_data: dict, combined_text: str) -> float:
        """Score training and knowledge transfer activities - 10-point scale"""
        score = 0.0
        combined_text_lower = combined_text.lower()
        
        # Primary scoring from training_provided field
        training_items = achievement_data.get('training_provided', [])
        
        if len(training_items) >= 3:
            score += 6.0  # Extensive training role (doubled from 3.0)
        elif len(training_items) >= 2:
            score += 4.0  # Good training activity (doubled from 2.0)
        elif len(training_items) >= 1:
            score += 2.0  # Some training (doubled from 1.0)
        
        # Keyword analysis
        keyword_matches = sum(1 for keyword in TRAINING_KEYWORDS if keyword in combined_text_lower)
        score += min(4.0, keyword_matches * 0.4)  # Max 4.0 bonus from keywords (doubled)
        
        # Apply language check
        training_text = ' '.join(str(item) for item in training_items)
        adjusted_score, explanation = self.language_analyzer.adjust_score_for_language(
            score, training_text + ' ' + combined_text, 'training'
        )
        
        return normalize_score(adjusted_score)
    
    def score_emergency_response(self, achievement_data: dict, combined_text: str) -> float:
        """Score emergency response - actual emergency/crisis situations only - 10-point scale"""
        score = 0.0
        combined_text_lower = combined_text.lower()
        
        # Define strict emergency indicators - actual emergencies only
        strict_emergency_keywords = [
            'emergency response', 'crisis response', 'disaster response',
            'search and rescue', 'sar operation', 'mayday', 'distress call',
            'emergency evacuation', 'disaster relief', 'humanitarian assistance',
            'incident command', 'emergency operations center', 
            'time-critical mission', 'urgent mission', 'emergency deployment',
            'natural disaster', 'hurricane response', 'flood response',
            'fire response', 'earthquake response', 'tsunami response',
            'mass casualty', 'triage', 'emergency medical', 'trauma response',
            'vessel in distress', 'aircraft emergency', 'maritime emergency',
            'immediate response', 'rapid response team', 'first on scene',
            'emergency activation', 'crisis management', 'disaster recovery'
        ]
        
        # Check for actual emergency situations
        actual_emergency_found = False
        emergency_count = 0
        
        for keyword in strict_emergency_keywords:
            if keyword in combined_text_lower:
                actual_emergency_found = True
                emergency_count += 1
        
        # Primary scoring from emergency_response field - but verify they're actual emergencies
        emergency_items = achievement_data.get('emergency_response', [])
        verified_emergency_items = []
        
        for item in emergency_items:
            item_lower = str(item).lower()
            # Check if this is an actual emergency situation (not routine or prevention)
            if any(keyword in item_lower for keyword in ['response', 'crisis', 'emergency', 'disaster', 'distress', 'urgent']):
                verified_emergency_items.append(item)
        
        # Score based on verified emergency responses (10-point scale)
        if len(verified_emergency_items) >= 2 and actual_emergency_found:
            score = 8.0  # Multiple verified emergency responses (doubled from 4.0)
        elif len(verified_emergency_items) >= 1 and actual_emergency_found:
            score = 6.0  # Verified emergency response (doubled from 3.0)
        elif actual_emergency_found and emergency_count >= 2:
            score = 5.0  # Multiple emergency keywords found (doubled from 2.5)
        elif actual_emergency_found:
            score = 4.0  # Emergency response found (doubled from 2.0)
        else:
            # No actual emergency response found
            score = 0.0
        
        # Language check - emergency claims often exaggerated
        emergency_text = ' '.join(str(item) for item in emergency_items)
        adjusted_score, explanation = self.language_analyzer.adjust_score_for_language(
            score, emergency_text + ' ' + combined_text, 'emergency'
        )
        
        return normalize_score(adjusted_score)
    
    def score_above_beyond(self, achievement_data: dict, combined_text: str) -> float:
        """Enhanced above-and-beyond scorer - 10-point scale, more stringent"""
        score = 0.0
        combined_text_lc = combined_text.lower()
        
        # Check for specific above_beyond_indicators from achievement data
        above_beyond_items = achievement_data.get('above_beyond_indicators', [])
        
        # Primary scoring based on concrete evidence
        if len(above_beyond_items) >= 3:
            score += 4.0  # Multiple concrete examples (doubled from 2.0)
        elif len(above_beyond_items) >= 2:
            score += 2.5  # (doubled from 1.25)
        elif len(above_beyond_items) >= 1:
            score += 1.5  # (doubled from 0.75)

        # Baseline adjectives
        if any(adj in combined_text_lc for adj in ABOVE_BEYOND_INDICATORS['baseline_adjectives']):
            score = max(score, 1.0)   # (doubled from 0.5)

        # Tiered indicators
        t1 = min(1, sum(1 for i in ABOVE_BEYOND_INDICATORS['tier1'] if i in combined_text_lc))
        t2 = min(2, sum(1 for i in ABOVE_BEYOND_INDICATORS['tier2'] if i in combined_text_lc))
        t3 = min(2, sum(1 for i in ABOVE_BEYOND_INDICATORS['tier3'] if i in combined_text_lc))
        t4 = min(3, sum(1 for i in ABOVE_BEYOND_INDICATORS['tier4'] if i in combined_text_lc))

        # Multipliers (doubled)
        score += t1 * 3.0    # heroic / superlative (doubled from 1.5)
        score += t2 * 2.0    # highly exceptional (doubled from 1.0)
        score += t3 * 1.0    # clearly above standard (doubled from 0.5)
        score += t4 * 0.5    # professional excellence (doubled from 0.25)

        # Voluntary time sacrifice bonus
        time_sacrifices = ['overtime', 'weekend', 'holiday', 'after hours', 'unpaid', 'personal time']
        time_bonus = 0.4 * sum(1 for w in time_sacrifices if w in combined_text_lc)  # (doubled from 0.2)
        score += min(1.5, time_bonus)  # (doubled cap from 0.75)

        # Quantified exceedance bonus
        exceed_pct = re.findall(r'(\d+)\s*% (above|over|beyond|exceeded)', combined_text_lc)
        if exceed_pct:
            max_pct = max(int(p[0]) for p in exceed_pct)
            if max_pct >= 75:
                score += 2.0    # Requires 75%+ exceedance (doubled from 1.0)
            elif max_pct >= 50:
                score += 1.0    # Requires 50%+ exceedance (doubled from 0.5)
            elif max_pct >= 25:
                score += 0.5    # Requires 25%+ exceedance (doubled from 0.25)

        # Apply language check - "above and beyond" claims often inflated
        above_text = ' '.join(str(item) for item in above_beyond_items)
        adjusted_score, explanation = self.language_analyzer.adjust_score_for_language(
            score, above_text + ' ' + combined_text, 'above_beyond'
        )

        return normalize_score(adjusted_score)