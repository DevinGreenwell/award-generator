# Award Engine for Coast Guard Award Writing Tool

import json
import re
from datetime import datetime
from flask import current_app

class AwardEngine:
    """
    Engine for processing achievement data and generating award recommendations
    based on objective criteria from the Coast Guard manuals.
    """
    
    def __init__(self):
        """Initialize the award engine with criteria from Coast Guard manuals."""
        # Award criteria with thresholds and descriptions
        self.award_criteria = {
            "Achievement Medal": {
                "threshold": 15,
                "description": "Recognizes notable accomplishments within a command that have limited impact but exceed normal expectations.",
                "criteria": [
                    "Performance that exceeds normal expectations",
                    "Accomplishments that benefit a division or small unit",
                    "Initiative beyond basic requirements",
                    "Limited scope of impact"
                ]
            },
            "Commendation Medal": {
                "threshold": 25,
                "description": "Recognizes sustained performance or specific achievement of a superlative nature that has significant impact at the unit or district level.",
                "criteria": [
                    "Significant positive impact at unit or district level",
                    "Demonstration of exceptional professional ability",
                    "Superior initiative beyond normal expectations",
                    "Substantial operational improvements"
                ]
            },
            "Meritorious Service Medal": {
                "threshold": 35,
                "description": "Recognizes outstanding meritorious achievement or service to the United States that has significant impact at the regional or Coast Guard-wide level.",
                "criteria": [
                    "Outstanding achievement with Coast Guard-wide impact",
                    "Exceptional leadership with significant results",
                    "Innovation that creates substantial improvements",
                    "Performance that materially enhances mission accomplishment"
                ]
            },
            "Legion of Merit": {
                "threshold": 45,
                "description": "Recognizes exceptionally meritorious conduct in the performance of outstanding service that has a profound impact on Coast Guard operations or national interests.",
                "criteria": [
                    "Exceptionally meritorious service with national impact",
                    "Leadership resulting in major operational enhancements",
                    "Innovations with far-reaching positive effects",
                    "Contributions of national significance"
                ]
            },
            "Distinguished Service Medal": {
                "threshold": 55,
                "description": "Recognizes exceptionally distinguished service that has had a profound and long-lasting impact on Coast Guard strategic objectives and national security.",
                "criteria": [
                    "Distinguished service of national significance",
                    "Strategic impact on Coast Guard missions",
                    "Extraordinary leadership with exceptional results",
                    "Contributions that significantly advance national interests"
                ]
            }
        }
        
        # Special award criteria for heroism
        self.heroism_awards = {
            "Coast Guard Medal": {
                "description": "Awarded for heroism not involving actual conflict with an enemy.",
                "criteria": [
                    "Acts of heroism in non-combat situations",
                    "Voluntary risk of life",
                    "Actions beyond the call of duty",
                    "Saving of life or property"
                ]
            }
        }
    
    def process_achievement_data(self, analysis_text):
        """
        Process the achievement analysis from OpenAI and extract structured data.
        
        Args:
            analysis_text: Text containing the analysis from OpenAI
            
        Returns:
            Dict containing structured achievement data
        """
        try:
            # Try to parse as JSON
            # In a production environment, we would handle various formats more robustly
            achievement_data = json.loads(analysis_text)
            return achievement_data
        except json.JSONDecodeError:
            # If not valid JSON, try to extract key information using regex
            current_app.logger.warning("Failed to parse achievement data as JSON")
            
            # Extract basic information using regex patterns
            data = {
                "nominee_info": self._extract_pattern(analysis_text, r"nominee_info[\"']?\s*:\s*{([^}]+)}"),
                "achievements": self._extract_list(analysis_text, r"achievements[\"']?\s*:\s*\[(.*?)\]"),
                "impacts": self._extract_list(analysis_text, r"impacts[\"']?\s*:\s*\[(.*?)\]"),
                "scope": self._extract_pattern(analysis_text, r"scope[\"']?\s*:\s*[\"']([^\"']+)[\"']"),
                "challenges": self._extract_list(analysis_text, r"challenges[\"']?\s*:\s*\[(.*?)\]"),
                "recommended_award": self._extract_pattern(analysis_text, r"recommended_award[\"']?\s*:\s*[\"']([^\"']+)[\"']"),
                "justification": self._extract_pattern(analysis_text, r"justification[\"']?\s*:\s*[\"']([^\"']+)[\"']")
            }
            
            return data
    
    def _extract_pattern(self, text, pattern):
        """Extract a single pattern from text."""
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else ""
    
    def _extract_list(self, text, pattern):
        """Extract a list from text."""
        match = re.search(pattern, text, re.DOTALL)
        if not match:
            return []
        
        items_text = match.group(1)
        # Split by commas not inside quotes
        items = re.findall(r'"([^"]*)"', items_text)
        if not items:
            items = [item.strip() for item in items_text.split(',')]
        
        return items
    
    def score_achievements(self, achievement_data):
        """
        Score the achievements based on objective criteria.
        
        Args:
            achievement_data: Dict containing structured achievement data
            
        Returns:
            Dict containing scores and total score
        """
        scores = {
            "scope": self._score_scope(achievement_data),
            "impact": self._score_impact(achievement_data),
            "initiative": self._score_initiative(achievement_data),
            "complexity": self._score_complexity(achievement_data),
            "duration": self._score_duration(achievement_data),
            "heroism": self._score_heroism(achievement_data)
        }
        
        # Calculate total score
        total_score = sum(scores.values())
        
        return {
            "scores": scores,
            "total_score": total_score
        }
    
    def _score_scope(self, data):
        """Score based on scope of impact."""
        scope = data.get("scope", "").lower()
        
        if "national" in scope or "international" in scope:
            return 15
        elif "coast guard-wide" in scope or "service-wide" in scope:
            return 12
        elif "district" in scope or "regional" in scope or "area" in scope:
            return 9
        elif "unit" in scope or "command" in scope:
            return 6
        elif "division" in scope or "department" in scope:
            return 3
        else:
            return 1
    
    def _score_impact(self, data):
        """Score based on quantifiable impact."""
        impacts = data.get("impacts", [])
        score = 0
        
        # Look for percentages, numbers, and dollar amounts
        for impact in impacts:
            impact_str = str(impact).lower()
            
            # Check for percentages
            pct_matches = re.findall(r'(\d+)%', impact_str)
            for match in pct_matches:
                pct = int(match)
                if pct >= 50:
                    score += 5
                elif pct >= 25:
                    score += 3
                elif pct >= 10:
                    score += 2
                else:
                    score += 1
            
            # Check for dollar amounts
            dollar_matches = re.findall(r'\$(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:thousand|million|billion|k|m|b)?', impact_str)
            if dollar_matches:
                score += 3
            
            # Check for lives saved
            if "life" in impact_str or "lives" in impact_str:
                if "saved" in impact_str or "rescued" in impact_str:
                    score += 10
            
            # General impact scoring
            if any(term in impact_str for term in ["significant", "substantial", "major"]):
                score += 2
            
            if any(term in impact_str for term in ["revolutionary", "groundbreaking", "unprecedented"]):
                score += 4
        
        # Cap the impact score at 20
        return min(score, 20)
    
    def _score_initiative(self, data):
        """Score based on level of initiative shown."""
        achievements = data.get("achievements", [])
        score = 0
        
        initiative_keywords = {
            "led": 3,
            "developed": 3,
            "created": 3,
            "designed": 3,
            "implemented": 2,
            "established": 2,
            "initiated": 2,
            "pioneered": 4,
            "spearheaded": 3,
            "coordinated": 2,
            "organized": 2,
            "innovated": 4,
            "transformed": 3,
            "revolutionized": 4
        }
        
        for achievement in achievements:
            achievement_str = str(achievement).lower()
            for keyword, points in initiative_keywords.items():
                if keyword in achievement_str:
                    score += points
                    break  # Only count each achievement once
        
        # Cap the initiative score at 15
        return min(score, 15)
    
    def _score_complexity(self, data):
        """Score based on complexity of achievements."""
        achievements = data.get("achievements", [])
        challenges = data.get("challenges", [])
        score = 0
        
        complexity_keywords = {
            "complex": 2,
            "challenging": 2,
            "difficult": 2,
            "sophisticated": 3,
            "technical": 2,
            "advanced": 2,
            "intricate": 3,
            "complicated": 2,
            "multifaceted": 3,
            "interagency": 3,
            "international": 4,
            "joint": 2
        }
        
        all_text = " ".join([str(a) for a in achievements + challenges]).lower()
        
        for keyword, points in complexity_keywords.items():
            if keyword in all_text:
                score += points
        
        # Cap the complexity score at 10
        return min(score, 10)
    
    def _score_duration(self, data):
        """Score based on duration of effort."""
        achievements = data.get("achievements", [])
        score = 0
        
        duration_keywords = {
            "year": 3,
            "years": 3,
            "month": 1,
            "months": 1,
            "sustained": 2,
            "ongoing": 2,
            "continuous": 2,
            "persistent": 2,
            "long-term": 3,
            "career": 4
        }
        
        all_text = " ".join([str(a) for a in achievements]).lower()
        
        for keyword, points in duration_keywords.items():
            if keyword in all_text:
                score += points
        
        # Cap the duration score at 10
        return min(score, 10)
    
    def _score_heroism(self, data):
        """Score based on heroism or risk."""
        achievements = data.get("achievements", [])
        impacts = data.get("impacts", [])
        score = 0
        
        heroism_keywords = {
            "risk": 3,
            "danger": 3,
            "hazard": 3,
            "peril": 4,
            "rescue": 3,
            "save": 2,
            "saved": 2,
            "life": 3,
            "lives": 3,
            "heroic": 5,
            "brave": 3,
            "courage": 4,
            "selfless": 3,
            "sacrifice": 4
        }
        
        all_text = " ".join([str(a) for a in achievements + impacts]).lower()
        
        for keyword, points in heroism_keywords.items():
            if keyword in all_text:
                score += points
        
        # Cap the heroism score at 15
        return min(score, 15)
    
    def recommend_award(self, scores):
        """
        Recommend an award based on scores.
        
        Args:
            scores: Dict containing score breakdown and total score
            
        Returns:
            Dict containing award recommendation and justification
        """
        total_score = scores.get("total_score", 0)
        score_breakdown = scores.get("scores", {})
        
        # Check for heroism first
        if score_breakdown.get("heroism", 0) >= 10:
            return {
                "award": "Coast Guard Medal",
                "justification": "Based on the heroic actions described, which involved significant personal risk beyond the call of duty."
            }
        
        # Otherwise, recommend based on total score
        for award, criteria in sorted(self.award_criteria.items(), key=lambda x: x[1]["threshold"], reverse=True):
            if total_score >= criteria["threshold"]:
                return {
                    "award": award,
                    "justification": criteria["description"]
                }
        
        # Default to Achievement Medal if no thresholds met
        return {
            "award": "Achievement Medal",
            "justification": self.award_criteria["Achievement Medal"]["description"]
        }
    
    def generate_explanation(self, award_name, achievement_data, scores):
        """
        Generate a detailed explanation for the award recommendation.
        
        Args:
            award_name: Name of the recommended award
            achievement_data: Dict containing achievement data
            scores: Dict containing score breakdown
            
        Returns:
            HTML-formatted explanation text
        """
        # Get award criteria
        award_info = self.award_criteria.get(award_name, self.heroism_awards.get(award_name, {
            "description": "Recognition for service and achievement.",
            "criteria": ["Performance that exceeds expectations"]
        }))
        
        # Format the explanation
        explanation = f"""
        <h3>Award Recommendation: {award_name}</h3>
        
        <p><strong>Description:</strong> {award_info["description"]}</p>
        
        <h4>Justification:</h4>
        <p>Based on the information provided, this recommendation aligns with the criteria in the Coast Guard Military Medals and Awards Manual. The recommendation is based solely on the accomplishments described, not on the nominee's rank.</p>
        
        <h4>Key Factors:</h4>
        <ul>
        """
        
        # Add score breakdown
        score_breakdown = scores.get("scores", {})
        if score_breakdown.get("scope", 0) > 0:
            scope_text = achievement_data.get("scope", "the unit")
            explanation += f"<li><strong>Scope of Impact:</strong> {scope_text}</li>"
        
        if score_breakdown.get("impact", 0) > 0:
            impacts = achievement_data.get("impacts", [])
            if impacts:
                explanation += "<li><strong>Quantifiable Results:</strong><ul>"
                for impact in impacts[:3]:  # Limit to top 3 impacts
                    explanation += f"<li>{impact}</li>"
                explanation += "</ul></li>"
        
        if score_breakdown.get("initiative", 0) > 0:
            explanation += "<li><strong>Initiative Demonstrated:</strong> Above expected levels for the position</li>"
        
        if score_breakdown.get("complexity", 0) > 0:
            explanation += "<li><strong>Complexity of Achievement:</strong> Required significant skill and expertise</li>"
        
        if score_breakdown.get("duration", 0) > 0:
            explanation += "<li><strong>Sustained Performance:</strong> Demonstrated over a significant period</li>"
        
        if score_breakdown.get("heroism", 0) > 0:
            explanation += "<li><strong>Risk or Heroism:</strong> Actions involved personal risk or danger</li>"
        
        explanation += """
        </ul>
        
        <h4>Alignment with Manual Criteria:</h4>
        <ul>
        """
        
        # Add specific criteria from the manual
        for criterion in award_info["criteria"]:
            explanation += f"<li>{criterion}</li>"
        
        explanation += """
        </ul>
        
        <p><strong>Note:</strong> This recommendation is based on objective criteria from the Coast Guard manuals, focusing on accomplishments rather than rank or position.</p>
        """
        
        return explanation
