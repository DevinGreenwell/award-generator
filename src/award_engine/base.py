"""
Base Award Engine class for Coast Guard award recommendations.
"""

import logging
from typing import Dict, List, Optional

from .criteria import SCORING_WEIGHTS, AWARD_THRESHOLDS, AWARD_CRITERIA
from .scorers import CriteriaScorer
from .utils import bootstrap_fields
from .exceptions import ScoringError, InsufficientDataError
from .rank_calibration import RankCalibrator

logger = logging.getLogger(__name__)


class AwardEngine:
    """
    Enhanced engine for processing achievement data and generating award recommendations
    based on Coast Guard award criteria with improved scoring algorithms.
    """
    
    def __init__(self):
        """Initialize the award engine with Coast Guard award criteria."""
        self.logger = logging.getLogger(__name__)
        self.weights = SCORING_WEIGHTS
        self.award_thresholds = AWARD_THRESHOLDS
        self.award_criteria = AWARD_CRITERIA
        self.scorer = CriteriaScorer()
        self.calibrator = RankCalibrator()
    
    def score_achievements(self, achievement_data: Dict, awardee_rank: Optional[str] = None) -> Dict[str, float]:
        """
        Enhanced scoring with comprehensive null safety and new field support.
        
        Args:
            achievement_data: Dictionary containing achievement information
            awardee_rank: Optional rank of the awardee for calibration
            
        Returns:
            Dictionary of scores for each criterion
            
        Raises:
            ScoringError: If there's an error during scoring
        """
        try:
            if achievement_data is None:
                achievement_data = {}

            # Auto-extract data when only a free-text narrative is supplied
            narrative = (
                achievement_data.get('free_text_narrative')
                or achievement_data.get('narrative')
                or achievement_data.get('narrative_text')
            )
            
            if narrative:
                extracted = bootstrap_fields(narrative)
                for k, v in extracted.items():
                    if not achievement_data.get(k):
                        achievement_data[k] = v

            # Initialize scores
            scores = {
                "leadership": 0.0,
                "impact": 0.0,
                "innovation": 0.0,
                "scope": 0.0,
                "challenges": 0.0,
                "quantifiable_results": 0.0,
                "valor": 0.0,
                "collaboration": 0.0,
                "training_provided": 0.0,
                "above_beyond": 0.0,
                "emergency_response": 0.0
            }

            # Build comprehensive text for analysis
            combined_text = self._build_combined_text(achievement_data, narrative)

            # Score each criterion
            scores["leadership"] = self.scorer.score_leadership(achievement_data, combined_text)
            scores["impact"] = self.scorer.score_impact(achievement_data, combined_text)
            scores["innovation"] = self.scorer.score_innovation(achievement_data, combined_text)
            scores["scope"] = self.scorer.score_scope(achievement_data, combined_text)
            scores["challenges"] = self.scorer.score_challenges(achievement_data, combined_text)
            scores["quantifiable_results"] = self.scorer.score_quantifiable_results(achievement_data, combined_text)
            scores["valor"] = self.scorer.score_valor(achievement_data, combined_text)
            scores["collaboration"] = self.scorer.score_collaboration(achievement_data, combined_text)
            scores["training_provided"] = self.scorer.score_training_provided(achievement_data, combined_text)
            scores["above_beyond"] = self.scorer.score_above_beyond(achievement_data, combined_text)
            scores["emergency_response"] = self.scorer.score_emergency_response(achievement_data, combined_text)

            # Calculate weighted total
            scores["total_weighted"] = self._calculate_weighted_total(scores)

            # Apply rank calibration if rank is provided
            if awardee_rank:
                logger.info(f"Applying rank calibration for {awardee_rank}")
                calibrated_scores, calibration_notes = self.calibrator.calibrate_scores(
                    scores, awardee_rank, achievement_data
                )
                
                # Log calibration adjustments
                for criterion, note in calibration_notes.items():
                    if note:
                        logger.info(f"  {criterion}: {note}")
                
                scores = calibrated_scores

            # Log scoring results
            self._log_scoring_results(achievement_data, scores, combined_text)

            return scores
            
        except Exception as e:
            logger.error(f"Scoring error: {e}", exc_info=True)
            raise ScoringError(f"Failed to score achievements: {str(e)}")
    
    def _build_combined_text(self, achievement_data: Dict, narrative: Optional[str]) -> str:
        """Build combined text from all achievement data fields."""
        text_components = []

        # Include primary narrative
        if narrative:
            text_components.append(narrative)

        # Include all possible fields from enhanced extraction
        text_fields = [
            "achievements", "impacts", "leadership_details", "innovation_details", 
            "challenges", "valor_indicators", "quantifiable_metrics", 
            "awards_received", "collaboration", "training_provided",
            "above_beyond_indicators", "emergency_response"
        ]

        for field in text_fields:
            field_data = achievement_data.get(field, [])
            if isinstance(field_data, list):
                text_components.extend([str(item) for item in field_data if item])
            elif field_data:
                text_components.append(str(field_data))

        # Add string fields
        for field in ["scope", "time_period", "justification"]:
            field_value = achievement_data.get(field)
            if field_value and field_value != "Not specified":
                text_components.append(str(field_value))

        return ' '.join(text_components).lower()
    
    def _calculate_weighted_total(self, scores: Dict[str, float]) -> float:
        """Calculate the weighted total score."""
        total_weighted = 0.0
        weight_sum = 0.0
        
        for criterion, score in scores.items():
            if criterion == "total_weighted":
                continue
                
            weight = self.weights.get(criterion, 1)
            if score == 0:
                continue   # do not drag total down for irrelevant criteria
            
            total_weighted += score * weight
            weight_sum += weight

        # Prevent divide-by-zero and normalize against a 5-point max for each weighted criterion
        percent = (total_weighted / (weight_sum * 5) * 100) if weight_sum else 0
        return round(percent, 1)
    
    def _log_scoring_results(self, achievement_data: Dict, scores: Dict[str, float], combined_text: str):
        """Log scoring results for debugging."""
        logger.info(f"SCORING RESULTS:")
        logger.info(f"Combined text length: {len(combined_text)} characters")
        logger.info(f"Achievement count: {len(achievement_data.get('achievements', []))}")
        logger.info(f"Impact count: {len(achievement_data.get('impacts', []))}")
        
        for key, value in scores.items():
            if key != "total_weighted":
                logger.info(f"  {key}: {value}/5.0")
        logger.info(f"TOTAL WEIGHTED SCORE: {scores['total_weighted']}")
    
    def recommend_award(self, scores: Dict[str, float]) -> Dict:
        """
        Stricter award recommendation that requires both total score AND minimum requirements.
        
        Args:
            scores: Dict containing scores for each criterion
            
        Returns:
            Dict containing the recommended award and score
        """
        total = scores.get("total_weighted", 0)
        
        logger.info(f"Award recommendation logic - Total score: {total}")
        
        # Check each award from highest to lowest
        for award, threshold in self.award_thresholds.items():
            logger.debug(f"Checking {award} - Threshold: {threshold}")

            # First, verify total-score gate
            if total < threshold:
                continue

            # Next, check minimum requirements
            min_reqs = self.award_criteria[award].get('min_requirements', {})
            
            # Count how many minimum requirements are met
            requirements_met = 0
            total_requirements = len(min_reqs)
            
            for criterion, min_score in min_reqs.items():
                if scores.get(criterion, 0) >= min_score:
                    requirements_met += 1
                else:
                    logger.debug(f"  {award} missed {criterion}: {scores.get(criterion, 0)} < {min_score}")
            
            # Require meeting at least 2/3 of minimum requirements (more balanced)
            required_count = max(1, int(total_requirements * 0.67))  # At least 67% of requirements
            meets_requirements = requirements_met >= required_count
            
            if not meets_requirements:
                logger.debug(f"  {award} only met {requirements_met}/{total_requirements} requirements (need {required_count})")
            
            # For the highest awards, ensure key criteria are strong
            if award in ["Distinguished Service Medal", "Legion of Merit"] and meets_requirements:
                # Double-check that leadership, impact, and scope are all reasonably strong
                key_criteria = ["leadership", "impact", "scope"]
                key_scores = [scores.get(c, 0) for c in key_criteria]
                avg_key_score = sum(key_scores) / len(key_scores)
                
                # Require average of key criteria to be at least 3.0 for these top awards
                if avg_key_score < 3.0:
                    meets_requirements = False
                    logger.debug(f"  {award} key criteria average too low: {avg_key_score:.2f}")

            if meets_requirements:
                return {"award": award, "score": total, "threshold_met": True}
        
        # If no award meets strict requirements, find the highest award they qualify for by score alone
        logger.info("No awards met minimum requirements. Finding best fit by score...")
        
        for award, threshold in self.award_thresholds.items():
            if total >= threshold:
                logger.info(f"Fallback recommendation: {award} (score-based only)")
                return {"award": award, "score": total, "threshold_met": False}
        
        # Absolute fallback
        logger.info("Default recommendation: Coast Guard Letter of Commendation")
        return {"award": "Coast Guard Letter of Commendation", "score": total, "threshold_met": True}
    
    def generate_explanation(self, award: str, achievement_data: Dict, scores: Dict[str, float]) -> str:
        """
        Generate a comprehensive explanation for the award recommendation.
        
        Args:
            award: Recommended award
            achievement_data: Dict containing structured achievement data
            scores: Dict containing scores for each criterion
            
        Returns:
            String containing the HTML-formatted explanation
        """
        # Get award criteria
        criteria = self.award_criteria.get(award, {})
        
        # Build explanation
        explanation = f"<h3>Award Recommendation: {award}</h3>"
        explanation += f"<p><strong>Description:</strong> {criteria.get('description', '')}</p>"
        
        # Remove scoring display - not compliant with CG format
        # Just provide justification
        explanation += "<h4>Justification:</h4>"
        explanation += f"<p>{achievement_data.get('justification', 'Based on the provided accomplishments and their impact.')}</p>"
        
        # Add sections for different achievement types
        sections = [
            ("achievements", "Key Achievements", 5),
            ("impacts", "Measurable Impact", 5),
            ("leadership_details", "Leadership Demonstrated", 3),
            ("innovation_details", "Innovation and Initiative", 3),
            ("challenges", "Challenges Overcome", 3)
        ]
        
        for field, title, limit in sections:
            items = achievement_data.get(field, [])
            if items:
                explanation += f"<h4>{title}:</h4>"
                explanation += "<ul>"
                for item in items[:limit]:
                    explanation += f"<li>{item}</li>"
                explanation += "</ul>"
        
        # Scope and time period
        scope = achievement_data.get("scope", "")
        if scope and scope != "Not specified":
            explanation += f"<h4>Scope of Impact:</h4>"
            explanation += f"<p>{scope}</p>"
        
        time_period = achievement_data.get("time_period", "")
        if time_period and time_period != "Not specified":
            explanation += f"<h4>Time Period:</h4>"
            explanation += f"<p>{time_period}</p>"
        
        # Remove scoring breakdown - not compliant with CG format
        
        return explanation
    
    def _generate_scoring_breakdown(self, scores: Dict[str, float]) -> str:
        """Generate HTML for scoring breakdown."""
        explanation = "<h4>Scoring Analysis:</h4>"
        explanation += "<div class='scoring-breakdown'>"
        
        high_scores = []
        medium_scores = []
        low_scores = []
        
        for criterion, score in scores.items():
            if criterion != 'total_weighted' and score > 0:
                formatted_name = criterion.replace('_', ' ').title()
                if score >= 4:
                    high_scores.append(f"{formatted_name}: {score}/5")
                elif score >= 2:
                    medium_scores.append(f"{formatted_name}: {score}/5")
                else:
                    low_scores.append(f"{formatted_name}: {score}/5")
        
        if high_scores:
            explanation += f"<p><strong>Strong Areas:</strong> {', '.join(high_scores)}</p>"
        if medium_scores:
            explanation += f"<p><strong>Good Areas:</strong> {', '.join(medium_scores)}</p>"
        if low_scores:
            explanation += f"<p><strong>Areas for Improvement:</strong> {', '.join(low_scores)}</p>"
        
        explanation += "</div>"
        return explanation
    
    def generate_improvement_suggestions(self, award: str, achievement_data: Dict) -> List[str]:
        """
        Generate specific suggestions for improving the award recommendation.
        
        Args:
            award: Recommended award
            achievement_data: Dict containing structured achievement data
            
        Returns:
            List of improvement suggestions
        """
        suggestions = []
        
        # Check for missing or weak areas in the data
        achievements = achievement_data.get("achievements", [])
        impacts = achievement_data.get("impacts", [])
        leadership = achievement_data.get("leadership_details", [])
        innovations = achievement_data.get("innovation_details", [])
        challenges = achievement_data.get("challenges", [])
        scope = achievement_data.get("scope", "")
        time_period = achievement_data.get("time_period", "")
        
        # Specific improvement suggestions based on missing elements
        if len(impacts) < 3:
            suggestions.append("Add more quantifiable impacts with specific numbers, percentages, or dollar amounts (cost savings, efficiency gains, etc.)")
        
        if len(leadership) < 2:
            suggestions.append("Include more leadership details: How many people did you supervise, train, or lead? What decisions did you make?")
        
        if not scope or "not specified" in scope.lower():
            suggestions.append("Clarify the scope of impact: Was this unit-level, sector-level, district-level, or Coast Guard-wide?")
        
        if len(innovations) < 2:
            suggestions.append("Highlight innovative approaches: What new methods, processes, or solutions did you develop or implement?")
        
        if len(challenges) < 2:
            suggestions.append("Describe specific challenges overcome: What obstacles, constraints, or difficult circumstances did you face?")
        
        if not time_period or "not specified" in time_period.lower():
            suggestions.append("Specify the time period: Over what duration did these accomplishments occur? (weeks, months, years)")
        
        # Award-level specific suggestions
        award_hierarchy = [
            "Coast Guard Letter of Commendation",
            "Coast Guard Achievement Medal",
            "Coast Guard Commendation Medal", 
            "Meritorious Service Medal",
            "Legion of Merit",
            "Distinguished Service Medal"
        ]
        
        current_index = -1
        for i, aw in enumerate(award_hierarchy):
            if aw.lower() in award.lower():
                current_index = i
                break
        
        # Award thresholds based on achievement type
        if current_index >= 0:
            # Check if there are fundamental barriers to higher awards
            has_life_saving = any('life' in str(item).lower() or 'lives' in str(item).lower() or 'rescue' in str(item).lower() 
                                for item in achievements + impacts)
            has_heroism = any('heroic' in str(item).lower() or 'courage' in str(item).lower() or 'risk' in str(item).lower() 
                             for item in achievements + impacts)
            has_combat = any('combat' in str(item).lower() or 'hostile' in str(item).lower() or 'enemy' in str(item).lower() 
                           for item in achievements + impacts)
            
            # Coast Guard Medal and higher heroism awards have specific requirements
            if current_index < 3 and not has_life_saving and not has_heroism:
                suggestions.append("Note: Higher personal awards (Coast Guard Medal, Bronze Star) typically require life-saving actions, extraordinary heroism, or combat-related achievements")
            elif current_index >= 0 and current_index < len(award_hierarchy) - 1:
                next_award = award_hierarchy[current_index + 1]
                # More realistic suggestions based on award level
                if current_index < 2:  # Letter or Achievement Medal
                    suggestions.append(f"To potentially qualify for a {next_award}, demonstrate leadership of larger teams (10+ people), district-wide impact, or significant cost savings ($500K+)")
                elif current_index == 2:  # Commendation Medal
                    suggestions.append(f"To potentially qualify for a {next_award}, show sustained superior performance over 2+ years, lead major initiatives, or achieve Coast Guard-wide impact")
                else:  # Higher awards
                    suggestions.append(f"Higher awards require exceptional service in positions of great responsibility, typically at O-5 level or above")
        
        # Always include these general suggestions if we don't have enough specific ones
        if len(suggestions) < 4:
            additional_suggestions = [
                "Include any awards, commendations, or formal recognition received for this work",
                "Add details about collaboration with other units, agencies, or organizations", 
                "Mention any training you provided to others or best practices you established",
                "Describe the lasting impact or long-term benefits of your accomplishments"
            ]
            
            for sugg in additional_suggestions:
                if len(suggestions) < 6:
                    suggestions.append(sugg)
        
        return suggestions[:6]  # Return maximum 6 suggestions