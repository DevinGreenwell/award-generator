# Enhanced Award Engine for Coast Guard Award Writing Tool

import json
import logging
import re as _re

# Fallback sentence tokenization function
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
    import nltk # type: ignore
    try:
        nltk.download('punkt', quiet=True)
        from nltk.tokenize import sent_tokenize as nltk_sent_tokenize # type: ignore
        sent_tokenize = nltk_sent_tokenize  # Override with nltk version if available
        NLTK_AVAILABLE = True
    except (ImportError, ModuleNotFoundError, Exception):
        # If any part of nltk import/setup fails, use fallback
        NLTK_AVAILABLE = False
except (ImportError, ModuleNotFoundError, Exception):
    # Use fallback function defined above
    NLTK_AVAILABLE = False

def _bootstrap_fields(free_text: str) -> dict:
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
    impacts.extend([s for s in sents if _re.search(r'\d[\d,]*(?:\.\d+)?\s*(%|views|followers|\$)', s)])
    innovation_details = [s for s in sents if any(w in s.lower() for w in ('developed', 'created', 'pioneered', 'innovative'))]
    leadership_details = [s for s in sents if any(w in s.lower() for w in ('led', 'supervis', 'managed', 'commanded'))]
    quant_metrics = _re.findall(r'\d[\d,]*(?:\.\d+)?\s*(?:%|views|followers|\$[\d,]+|hours|days)', free_text_lc)

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
 # -------------------------------------------------------------------------
from datetime import datetime

class AwardEngine:
    """
    Enhanced engine for processing achievement data and generating award recommendations
    based on Coast Guard award criteria with improved scoring algorithms.
    """
    
    def __init__(self):
        """Initialize the award engine with Coast Guard award criteria."""
        self.logger = logging.getLogger(__name__)

        # Enhanced weights for different scoring criteria (re-balanced June 2024)
        self.WEIGHTS = {
            "impact": 5,
            "scope": 5,
            "leadership": 5,
            "above_beyond": 4,
            "innovation": 4,
            "quantifiable_results": 4,
            "challenges": 3,
            # Keep existing weights for categories that trigger only when non‑zero
            "valor": 5,
            "collaboration": 4,
            "training_provided": 3,

        }

        # Updated thresholds based on comprehensive scoring (now percentages)
        self.award_thresholds = {
            "Medal of Honor": 95,
            "Distinguished Service Medal": 90,
            "Legion of Merit": 80,
            "Meritorious Service Medal": 70,
            "Coast Guard Commendation Medal": 60,
            "Coast Guard Achievement Medal": 50,
            "Coast Guard Letter of Commendation": 40
        }

        # Define award criteria based on Coast Guard manuals
        self.award_criteria = {
            "Medal of Honor": {
                "description": "May be awarded to any person who distinguishes themselves by gallantry and intrepidity at the risk of their life above and beyond the call of duty.",
                "threshold": 95,
                "min_requirements": {
                    "valor": 5,
                    "risk_to_life": 5,
                    "gallantry": 5,
                    "leadership": 3,
                }
            },
            "Distinguished Service Medal": {
                "description": "May be awarded to any person who distinguishes themselves by exceptionally meritorious service to the United States Government in a duty of great responsibility.",
                "threshold": 90,
                "min_requirements": {
                    "leadership": 4.5,
                    "impact": 4.5,
                    "scope": 4.5
                }
            },
            "Legion of Merit": {
                "description": "Awarded to officers who have performed exceptionally meritorious service, except as to the degree of responsibility of the DSM.",
                "threshold": 80,
                "min_requirements": {
                    "leadership": 4,
                    "impact": 4,
                    "scope": 4
                }
            },
            "Meritorious Service Medal": {
                "description": "May be awarded to any member who distinguishes themselves by outstanding meritorious achievement or service to the United States.",
                "threshold": 70,
                "min_requirements": {
                    "leadership": 3.5,
                    "impact": 3.5,
                    "scope": 4
                }
            },
            "Coast Guard Commendation Medal": {
                "description": "May be awarded to a person who distinguishes themselves by heroic or meritorious achievement or service.",
                "threshold": 60,
                "min_requirements": {
                    "leadership": 2.5,
                    "impact": 2.5,
                    "scope": 3
                }
            },
            "Coast Guard Achievement Medal": {
                "description": "May be awarded for professional and/or leadership achievement based on sustained performance or specific achievement of a superlative nature.",
                "threshold": 50,
                "min_requirements": {
                    "impact": 2,
                    "scope": 2
                }
            },
            "Coast Guard Letter of Commendation": {
                "description": "May be awarded for an act or service resulting in unusual and/or outstanding achievement but lesser than that required for the Achievement Medal.",
                "threshold": 40,
                "min_requirements": {
                    "impact": 1
                }
            }
        }

    def score_achievements(self, achievement_data):
        """Enhanced scoring with comprehensive null safety and new field support"""
    
        if achievement_data is None:
            achievement_data = {}

        # Auto‑extract data when only a free‑text narrative is supplied
        narrative = (
            achievement_data.get('free_text_narrative')
            or achievement_data.get('narrative')        # <- new
            or achievement_data.get('narrative_text')   # <- new
)
        if narrative:
            extracted = _bootstrap_fields(narrative)
            for k, v in extracted.items():
                if not achievement_data.get(k):
                    achievement_data[k] = v
            for _key in ("impacts", "innovation_details", "quantifiable_metrics"):
                achievement_data.setdefault(_key, extracted.get(_key, []))
    
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
    
        # Build comprehensive text for analysis - include ALL new fields
        all_text_components = []

        # INCLUDE PRIMARY NARRATIVE
        if narrative:
            all_text_components.append(narrative)

    
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
                all_text_components.extend([str(item) for item in field_data if item])
            elif field_data:
                all_text_components.append(str(field_data))
    
        # Add string fields
        for field in ["scope", "time_period", "justification"]:
            field_value = achievement_data.get(field)
            if field_value and field_value != "Not specified":
                all_text_components.append(str(field_value))
    
        combined_text = ' '.join(all_text_components).lower()
    
        # Enhanced scoring with error handling and new field integration
        try:
            # Core scoring methods (enhanced)
            scores["leadership"] = round(self._score_leadership_enhanced(achievement_data, combined_text), 1)
            scores["impact"] = round(self._score_impact_enhanced(achievement_data, combined_text), 1)
            scores["innovation"] = round(self._score_innovation_enhanced(achievement_data, combined_text), 1)
            scores["scope"] = round(self._score_scope_enhanced(achievement_data, combined_text), 1)
            scores["challenges"] = round(self._score_challenges_enhanced(achievement_data, combined_text), 1)
            # Removed time_factor score calculation
            # Enhanced quantifiable results using dedicated field
            scores["quantifiable_results"] = round(self._score_quantifiable_enhanced(achievement_data, combined_text), 1)
            # Valor scoring using dedicated field
            scores["valor"] = round(self._score_valor_enhanced(achievement_data, combined_text), 1)
            # NEW: Collaboration scoring
            scores["collaboration"] = round(self._score_collaboration(achievement_data, combined_text), 1)
            # NEW: Training provided scoring
            scores["training_provided"] = round(self._score_training_provided(achievement_data, combined_text), 1)
            # Enhanced above and beyond scoring
            scores["above_beyond"] = round(self._score_above_beyond_enhanced(achievement_data, combined_text), 1)
            # NEW: Emergency response scoring
            scores["emergency_response"] = round(self._score_emergency_response(achievement_data, combined_text), 1)
        except Exception as e:
            print(f"Scoring error: {e}")
            import traceback
            traceback.print_exc()
            
            # Ensure all scores are valid numbers
            for key in scores:
                if not isinstance(scores[key], (int, float)) or scores[key] is None:
                    scores[key] = 0.0
    
        # Dynamic weighting – ignore criteria that truly score 0
        total_weighted = 0.0
        weight_sum = 0.0
        for criterion, score in scores.items():
            weight = self.WEIGHTS.get(criterion, 1)
            if score == 0:
                continue   # do not drag total down for irrelevant criteria
            total_weighted += score * weight
            weight_sum += weight

        # Prevent divide‑by‑zero and normalize against a 5‑point max for each weighted criterion
        # This ensures a perfect 5/5 across all counted criteria yields 100 %
        percent = (total_weighted / (weight_sum * 5) * 100) if weight_sum else 0
        scores["total_weighted"] = round(percent, 1)
    
        # Enhanced debug output
        print(f"ENHANCED SCORING RESULTS:")
        print(f"Combined text length: {len(combined_text)} characters")
        print(f"Achievement count: {len(achievement_data.get('achievements', []))}")
        print(f"Impact count: {len(achievement_data.get('impacts', []))}")
        print(f"Leadership details: {len(achievement_data.get('leadership_details', []))}")
        print(f"Innovation details: {len(achievement_data.get('innovation_details', []))}")
        print(f"Valor indicators: {len(achievement_data.get('valor_indicators', []))}")
        print(f"Quantifiable metrics: {len(achievement_data.get('quantifiable_metrics', []))}")
        
        for key, value in scores.items():
            if key != "total_weighted":
                print(f"  {key}: {value}/5.0")
        print(f"TOTAL WEIGHTED SCORE: {scores['total_weighted']}")
        
        return scores

    def _score_leadership_enhanced(self, achievement_data, combined_text):
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
        leadership_keywords = [
            'supervised', 'managed', 'led', 'directed', 'commanded', 'oversaw',
            'coordinated', 'organized', 'mentored', 'trained', 'guided',
            'team leader', 'project manager', 'department head', 'section chief'
        ]
        
        keyword_matches = sum(1 for keyword in leadership_keywords if keyword in combined_text)
        score += min(1.0, keyword_matches * 0.1)  # Max 1.0 bonus from keywords
        
        return min(5.0, score)

    def _score_collaboration(self, achievement_data, combined_text):
        """Score collaboration and inter-agency work"""
        score = 0.0
        
        # Primary scoring from collaboration field
        collaboration_items = achievement_data.get('collaboration', [])
        
        if len(collaboration_items) >= 3:
            score += 3.0  # Extensive collaboration
        elif len(collaboration_items) >= 2:
            score += 2.0  # Good collaboration
        elif len(collaboration_items) >= 1:
            score += 1.0  # Some collaboration
        
        # Collaboration keywords for additional context
        collaboration_keywords = [
            'inter-agency', 'joint operation', 'multi-unit', 'cross-functional',
            'partnership', 'coordinated with', 'worked with', 'collaborated',
            'liaison', 'interface', 'external agency', 'other services'
        ]
        
        keyword_matches = sum(1 for keyword in collaboration_keywords if keyword in combined_text)
        score += min(2.0, keyword_matches * 0.2)  # Max 2.0 bonus from keywords
        
        return min(5.0, score)

    def _score_training_provided(self, achievement_data, combined_text):
        """Score training and knowledge transfer activities"""
        score = 0.0
        
        # Primary scoring from training_provided field
        training_items = achievement_data.get('training_provided', [])
        
        if len(training_items) >= 3:
            score += 3.0  # Extensive training role
        elif len(training_items) >= 2:
            score += 2.0  # Good training activity
        elif len(training_items) >= 1:
            score += 1.0  # Some training
        
        # Training keywords
        training_keywords = [
            'trained', 'instructed', 'taught', 'mentored', 'coached',
            'developed personnel', 'knowledge transfer', 'skill development',
            'curriculum', 'lesson plan', 'training program'
        ]
        
        keyword_matches = sum(1 for keyword in training_keywords if keyword in combined_text)
        score += min(2.0, keyword_matches * 0.2)  # Max 2.0 bonus from keywords
        
        return min(5.0, score)

    def _score_emergency_response(self, achievement_data, combined_text):
        """Score emergency response and crisis management"""
        score = 0.0
        
        # Primary scoring from emergency_response field
        emergency_items = achievement_data.get('emergency_response', [])
        
        if len(emergency_items) >= 2:
            score += 3.0  # Multiple emergency responses
        elif len(emergency_items) >= 1:
            score += 2.0  # Emergency response experience
        
        # Emergency keywords
        emergency_keywords = [
            'emergency', 'crisis', 'urgent', 'immediate response', 'rapid response',
            'disaster', 'catastrophe', 'critical situation', 'life-threatening',
            'search and rescue', 'sar', 'mayday', 'distress call'
        ]
        
        keyword_matches = sum(1 for keyword in emergency_keywords if keyword in combined_text)
        score += min(3.0, keyword_matches * 0.3)  # Max 3.0 bonus from keywords
        
        return min(5.0, score)

    def _score_quantifiable_enhanced(self, achievement_data, combined_text):
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
        import re
        
        # Look for percentages
        percentages = re.findall(r'(\d+(?:\.\d+)?)\s*%', combined_text)
        if percentages:
            score += min(1.0, len(percentages) * 0.3)
        
        # Look for dollar amounts
        dollars = re.findall(r'\$[\d,]+(?:\.\d{2})?', combined_text)
        if dollars:
            score += min(1.0, len(dollars) * 0.3)
        
        # Look for time measurements
        time_saved = re.findall(r'(\d+)\s*(?:hours?|days?|weeks?|months?)', combined_text)
        if time_saved:
            score += min(1.0, len(time_saved) * 0.2)
        
        return min(5.0, score)

    def _score_above_beyond_enhanced(self, achievement_data, combined_text):
        """
        *Much* more lenient above‑and‑beyond scorer.
        • Any single strong adjective or indicator now guarantees at least 1.5 / 5.
        • Tier multipliers relaxed so that fewer matches yield higher credit.
        • Adds broad adjective fall‑back list so typical narratives don’t score zero.
        """
        score = 0.0
        combined_text_lc = combined_text.lower()

        # --- 0.  Safety net adjectives -------------------------------------------------
        baseline_adjectives = [
            'outstanding', 'exemplary', 'exceptional', 'remarkable',
            'superb', 'stellar', 'tremendous', 'extraordinary',
            'significant', 'notable', 'noteworthy', 'impressive'
        ]
        if any(adj in combined_text_lc for adj in baseline_adjectives):
            score = max(score, 1.5)   # automatic baseline

        # -------------------------------------------------------------------------------
        # Tiered indicators (relaxed caps & stronger multipliers)
        tier1_indicators = [
            'above and beyond', 'beyond the call of duty', 'superhuman',
            'heroic effort', 'personal sacrifice', 'risked own safety',
            'selfless service', 'life‑threatening situation', 'extreme danger'
        ]
        tier2_indicators = [
            'extraordinary', 'exceptional', 'remarkable', 'outstanding', 'exemplary',
            'voluntary overtime', 'unpaid hours', 'weekend work', 'holiday duty',
            'personal time', 'took charge', 'stepped up', 'extra mile'
        ]
        tier3_indicators = [
            'exceeded', 'surpassed', 'outperformed', 'exceeded expectations',
            'voluntary service', 'community service', 'mentorship', 'coached others',
            'innovative approach', 'creative solution'
        ]
        tier4_indicators = [
            'professional excellence', 'technical mastery', 'consistent results',
            'reliable performance', 'dependable service'
        ]

        # Count matches (no caps – let them accumulate)
        t1 = min(2, sum(1 for i in tier1_indicators if i in combined_text_lc))
        t2 = min(2, sum(1 for i in tier2_indicators if i in combined_text_lc))
        t3 = min(3, sum(1 for i in tier3_indicators if i in combined_text_lc))
        t4 = min(4, sum(1 for i in tier4_indicators if i in combined_text_lc))

        # Relaxed multipliers
        score += t1 * 2.0    # heroic / superlative
        score += t2 * 1.5    # highly exceptional
        score += t3 * 1.0    # clearly above standard
        score += t4 * 0.5    # professional excellence

        # --- 1.  Voluntary time sacrifice bonus (unchanged) -----------------------------
        time_sacrifices = ['overtime', 'weekend', 'holiday', 'after hours', 'unpaid', 'personal time']
        time_bonus = 0.3 * sum(1 for w in time_sacrifices if w in combined_text_lc)  # up to ~1.5
        score += min(1.5, time_bonus)

        # --- 2.  Quantified exceedance bonus -------------------------------------------
        import re
        exceed_pct = re.findall(r'(\d+)\s*% (above|over|beyond|exceeded)', combined_text_lc)
        if exceed_pct:
            max_pct = max(int(p[0]) for p in exceed_pct)
            if max_pct >= 50:
                score += 1.0
            elif max_pct >= 25:
                score += 0.75
            elif max_pct >= 10:
                score += 0.5

        # Clamp to 5
        return round(min(5.0, score), 1)

    def _score_valor_enhanced(self, achievement_data, combined_text):
        """Enhanced valor scoring using dedicated valor_indicators field"""
        score = 0.0
        
        # Primary scoring from valor_indicators field
        valor_items = achievement_data.get('valor_indicators', [])
        
        if len(valor_items) >= 2:
            score += 4.0  # Multiple valor actions
        elif len(valor_items) >= 1:
            score += 3.0  # Valor demonstrated
        
        # High-value valor keywords
        valor_keywords = [
            'life-threatening', 'rescued', 'saved life', 'saved lives',
            'personal risk', 'dangerous conditions', 'heroic',
            'risked safety', 'brave', 'courageous', 'gallant'
        ]
        
        keyword_matches = sum(1 for keyword in valor_keywords if keyword in combined_text)
        score += min(2.0, keyword_matches * 0.3)  # Max 2.0 bonus from keywords
        
        return min(5.0, score)
    
    def _score_leadership(self, achievement_data, combined_text):
        """Score leadership based on specific leadership details and keywords - STRICTER STANDARDS."""
        score = 0
        
        # Check for specific leadership details - stricter requirements
        leadership_details = achievement_data.get('leadership_details', [])
        if len(leadership_details) >= 3:
            score += 2.5
        elif len(leadership_details) >= 2:
            score += 1.5
        elif len(leadership_details) >= 1:
            score += 0.5
        
        # Enhanced leadership keyword analysis with comprehensive descriptors
        high_leadership = [
            'commanded', 'directed', 'managed team', 'supervised', 'led team', 'oversaw', 'coordinated',
            'executive leadership', 'commanding officer', 'officer in charge', 'department head',
            'operational command', 'mission commander', 'incident commander', 'team leader',
            'project manager', 'program director', 'division chief', 'section head', 'unit commander',
            'managed personnel', 'supervised staff', 'led operations', 'directed activities',
            'orchestrated efforts', 'spearheaded initiative', 'headed up', 'took command',
            'assumed leadership', 'exercised authority', 'wielded responsibility', 'held accountability',
            'strategic leadership', 'organizational leadership', 'tactical command', 'operational control',
            'personnel management', 'resource allocation', 'budget authority', 'decision-making authority',
            'chain of command', 'leadership hierarchy', 'command structure', 'reporting structure',
            'performance management', 'personnel evaluation', 'career development', 'succession planning',
            'policy implementation', 'standard enforcement', 'discipline administration', 'corrective action'
        ]
        
        medium_leadership = [
            'guided', 'mentored', 'trained personnel', 'delegated', 'organized team', 'facilitated',
            'instructed', 'coached', 'developed personnel', 'supervised training', 'led training',
            'team coordination', 'group facilitation', 'workshop leadership', 'meeting facilitation',
            'project coordination', 'task coordination', 'activity coordination', 'event coordination',
            'cross-functional leadership', 'matrix management', 'collaborative leadership', 'shared leadership',
            'influenced others', 'motivated team', 'inspired personnel', 'encouraged participation',
            'built consensus', 'forged agreement', 'negotiated solutions', 'mediated conflicts',
            'knowledge transfer', 'skill development', 'capacity building', 'competency development',
            'performance coaching', 'professional mentoring', 'career guidance', 'advisory role',
            'team development', 'group dynamics', 'team building', 'morale enhancement',
            'communication leadership', 'information sharing', 'briefing delivery', 'presentation leadership',
            'quality assurance', 'process improvement', 'workflow optimization', 'efficiency enhancement',
            'technical leadership', 'subject matter expertise', 'specialized guidance', 'expert consultation',
            'planning leadership', 'strategic planning', 'tactical planning', 'resource planning',
            'risk management', 'safety oversight', 'compliance monitoring', 'standard maintenance'
        ]
        
        low_leadership = [
            'assisted leadership', 'helped manage', 'supported supervision',
            'participated in leadership', 'contributed to management', 'aided supervision',
            'backup leadership', 'deputy role', 'assistant position', 'support role',
            'helped coordinate', 'assisted with planning', 'supported organization', 'aided implementation',
            'team member', 'working group participant', 'committee member', 'task force member',
            'collaborated with leadership', 'worked under supervision', 'followed guidance', 'took direction',
            'peer leadership', 'informal leadership', 'situational leadership', 'temporary leadership',
            'helped train', 'assisted with development', 'supported mentoring', 'aided coaching',
            'subject matter input', 'technical assistance', 'advisory support', 'consultation provided',
            'documentation support', 'administrative assistance', 'logistics support', 'clerical support',
            'communication support', 'coordination assistance', 'scheduling help', 'meeting support',
            'research assistance', 'analysis support', 'data collection help', 'information gathering',
            'implementation support', 'execution assistance', 'follow-up help', 'monitoring support',
            'quality control assistance', 'review support', 'evaluation help', 'assessment assistance',
            'training assistance', 'education support', 'learning facilitation', 'knowledge support'
        ]
        
        # Stricter scoring - require multiple instances for higher scores
        high_count = sum(1 for keyword in high_leadership if keyword in combined_text)
        medium_count = sum(1 for keyword in medium_leadership if keyword in combined_text)
        low_count = sum(1 for keyword in low_leadership if keyword in combined_text)
        
        if high_count >= 2:
            score += 1.5
        elif high_count >= 1:
            score += 1
        
        if medium_count >= 2:
            score += 1
        elif medium_count >= 1:
            score += 0.5
        
        if low_count >= 1:
            score += 0.25
        
        # Stricter personnel number requirements
        personnel_numbers = _re.findall(r'(\d+)\s*(?:people|personnel|staff|members|team|subordinates)', combined_text)
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
        
        return round(min(5, score), 1)
    
    def _score_impact(self, achievement_data, combined_text):
        """Score impact based on specific impacts and measurable outcomes - STRICTER STANDARDS."""
        score = 0
        
        # Stricter requirements for impact details
        impacts = achievement_data.get('impacts', [])
        if len(impacts) >= 4:
            score += 3
        elif len(impacts) >= 3:
            score += 2.5
        elif len(impacts) >= 2:
            score += 2
        elif len(impacts) >= 1:
            score += 1
        
        # Enhanced impact keyword analysis with comprehensive descriptors
        high_impact = [
            'saved lives', 'prevented disaster', 'eliminated risk', 'increased by', 'reduced by', 'improved by',
            'rescued', 'life-saving', 'prevented death', 'averted catastrophe', 'eliminated threat', 'significantly enhanced', 'significantly improved',
            'critical intervention', 'emergency response', 'crisis management', 'disaster mitigation', 'critical capability', 'high-impact',
            'casualty prevention', 'safety enhancement', 'risk elimination', 'hazard removal',
            'mission-critical', 'operational success', 'breakthrough achievement', 'revolutionary change',
            'game-changing', 'transformational', 'unprecedented results', 'exceptional outcomes',
            'dramatically improved', 'substantially increased', 'significantly reduced', 'completely eliminated',
            'fully resolved', 'successfully prevented', 'effectively mitigated'
        ]
        
        medium_impact = [
            'enhanced significantly', 'optimized', 'boosted', 'accelerated', 'streamlined', 'improved', 'increased',
            'modernized', 'upgraded', 'refined', 'strengthened', 'elevated', 'advanced', 'boosted',
            'facilitated', 'expedited', 'enhanced efficiency', 'increased effectiveness',
            'improved performance', 'better outcomes', 'positive results', 'beneficial changes',
            'noteworthy improvement', 'meaningful progress', 'substantial gains', 'considerable advancement',
            'enhanced capability', 'increased capacity', 'improved readiness', 'better coordination',
            'enhanced collaboration', 'improved communication', 'increased productivity', 'better processes',
            'more efficient', 'faster response', 'higher quality', 'greater accuracy',
            'improved reliability', 'enhanced stability', 'increased availability', 'better compliance'
        ]
        
        low_impact = [
            'contributed to', 'supported improvement', 'assisted in', 'helped',
            'participated in', 'took part in', 'was involved in', 'played a role',
            'helped with', 'aided in', 'supported the effort', 'contributed towards',
            'assisted with development', 'helped implement', 'supported implementation',
            'participated in planning', 'involved in coordination', 'helped facilitate',
            'supported the team', 'assisted leadership', 'helped organize', 'supported operations',
            'contributed ideas', 'provided input', 'offered suggestions', 'shared knowledge',
            'helped coordinate', 'assisted with training', 'supported the mission',
            'helped maintain', 'assisted with planning', 'supported analysis',
            'helped document', 'assisted with reporting', 'supported communication',
            'helped prepare', 'assisted with evaluation', 'supported review'
        ]
        
        # Require multiple high-impact indicators
        high_count = sum(1 for keyword in high_impact if keyword in combined_text)
        medium_count = sum(1 for keyword in medium_impact if keyword in combined_text)
        
        if high_count >= 4:
            score += 1
        elif high_count >= 3:
            score += 0.75
        elif high_count >= 2:
            score += 0.5
        
        if medium_count >= 3:
            score += 1
        elif medium_count >= 2:
            score += 0.75
        elif medium_count >= 1:
            score += 0.5
        
        # Quantifiable impacts - stricter requirements
        quant_score = self._find_quantifiable_metrics(combined_text)
        if quant_score >= 5:
            score += 1
        elif quant_score >= 4:
            score += 0.75
        elif quant_score >= 3:
            score += 0.5
        
        return round(min(5, score), 1)
    
    def _score_innovation(self, achievement_data, combined_text):
        """Score innovation based on creative solutions and new approaches."""
        score = 0
        
        # Check for specific innovation details
        innovations = achievement_data.get('innovation_details', [])
        if len(innovations) >= 3:
            score += 2
        elif len(innovations) >= 2:
            score += 1.5
        elif len(innovations) >= 1:
            score += 1
        
        # Enhanced innovation keywords with comprehensive descriptors
        innovation_keywords = [
            'pioneered', 'created', 'developed', 'designed', 'revolutionized', 
            'first time', 'new approach', 'innovative', 'creative solution', 
            'breakthrough', 'original', 'novel', 'ingenuity',
            'invented', 'conceived', 'originated', 'initiated', 'launched',
            'established', 'founded', 'instituted', 'introduced', 'implemented',
            'devised', 'formulated', 'engineered', 'architected', 'constructed',
            'built from scratch', 'ground-breaking', 'cutting-edge', 'state-of-the-art',
            'next-generation', 'advanced technology', 'modernization', 'digital transformation',
            'process improvement', 'workflow optimization', 'system enhancement', 'methodology development',
            'best practices', 'standard operating procedures', 'new protocols', 'innovative procedures',
            'creative approach', 'unique solution', 'alternative method', 'unconventional approach',
            'out-of-the-box thinking', 'paradigm shift', 'game changer', 'disruptive innovation',
            'technological advancement', 'automation', 'digitization', 'streamlined process',
            'efficiency improvement', 'cost-saving innovation', 'resource optimization',
            'first-of-its-kind', 'never before attempted', 'unprecedented approach', 'trailblazing',
            'pilot program', 'proof of concept', 'prototype development', 'beta testing',
            'experimental approach', 'research and development', 'innovation initiative',
            'creative problem-solving', 'inventive solution', 'forward-thinking approach',
            'visionary leadership', 'strategic innovation', 'transformative change',
            'reimagined process', 'redesigned system', 'reconfigured approach',
            'customized solution', 'tailored approach', 'specialized method',
            'integrated solution', 'cross-functional innovation', 'collaborative development',
            'knowledge transfer', 'lessons learned application', 'continuous improvement',
            'adaptation', 'modification', 'enhancement', 'upgrade', 'evolution'
        ]
        
        # Count keyword occurrences and add to score
        for keyword in innovation_keywords:
            if keyword in combined_text:
                score += 0.2
        
        return round(min(5, score), 1)

    def _score_scope(self, achievement_data, combined_text):
        """Score scope based on reach and organizational impact using weighted scoring."""
        scope_text = achievement_data.get("scope", "").lower()
        combined_scope = scope_text + " " + combined_text
        
        # Define scope indicators with their point values
        scope_indicators = {
            # Highest level - National/International (5 points each)
            "national": 5, "international": 5, "coast guard-wide": 5, "service-wide": 5, 
            "enterprise": 5, "organizationally": 5, "global": 5, "worldwide": 5, 
            "continental": 5, "federal": 5, "government-wide": 5, "department of defense": 5,
            "joint operations": 5, "nato": 5, "multinational": 5, "cross-service": 5,
            
            # Area/District/Regional level (4 points each)
            "area": 4, "district": 4, "regional": 4, "multi-unit": 4, "command": 4, 
            "interagency": 4, "state-wide": 4, "multi-district": 4, "headquarters": 4,
            "area command": 4, "district office": 4, "regional command": 4,
            
            # Sector/Group level (3 points each)
            "sector": 3, "group": 3, "multiple units": 3, "inter-agency": 3, 
            "base-wide": 3, "installation": 3, "flotilla": 3, "multi-station": 3,
            "sector command": 3, "air station": 3, "training center": 3,
            
            # Unit/Station level (2 points each)
            "unit": 2, "station": 2, "department": 2, "division": 2,
            "coast guard station": 2, "cutter": 2, "vessel": 2, "ship": 2,
            "boat": 2, "facility": 2, "office": 2, "detachment": 2,
            
            # Individual/Team level (1 point each)
            "team": 1, "crew": 1, "watch": 1, "shift": 1, "individual": 1,
            "personal": 1, "self": 1, "own": 1, "my": 1
        }
        
        # Calculate weighted score based on all matches found
        total_score = 0
        matches_found = []
        
        for indicator, points in scope_indicators.items():
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
        
        # Debug logging
        print(f"SCOPE ANALYSIS: Found {len(matches_found)} indicators: {matches_found}")
        print(f"SCOPE SCORING: Raw points: {total_score} → Final score: {final_score}/5")
        
        return round(final_score, 1)
    
    def _score_challenges(self, achievement_data, combined_text):
        """Score based on challenges overcome."""
        score = 0
        
        # Check for specific challenge details
        challenges = achievement_data.get('challenges', [])
        score += min(3, len(challenges))  # Up to 3 points for specific challenges
        
        # Enhanced challenge keywords with comprehensive descriptors
        challenge_keywords = [
            'emergency', 'crisis', 'difficult', 'complex', 'unprecedented', 
            'challenging', 'obstacle', 'constraint', 'pressure', 'deadline',
            'limited resources', 'adverse conditions',
            'catastrophic', 'disaster', 'critical situation', 'urgent response', 'life-threatening',
            'high-stakes', 'time-sensitive', 'mission-critical', 'under pressure', 'tight timeline',
            'severe weather', 'harsh environment', 'dangerous conditions', 'hazardous situation',
            'extreme circumstances', 'hostile environment', 'treacherous conditions', 'perilous situation',
            'budget constraints', 'funding shortfall', 'resource shortage', 'personnel shortage',
            'equipment failure', 'system breakdown', 'technical malfunction', 'infrastructure failure',
            'competing priorities', 'conflicting demands', 'multiple deadlines', 'simultaneous crises',
            'high complexity', 'intricate problem', 'multi-faceted challenge', 'layered complications',
            'regulatory hurdles', 'compliance challenges', 'policy constraints', 'legal obstacles',
            'political pressure', 'public scrutiny', 'media attention', 'stakeholder demands',
            'resistance to change', 'organizational inertia', 'cultural barriers', 'communication barriers',
            'interagency coordination', 'multi-jurisdictional', 'cross-functional complexity',
            'language barriers', 'cultural differences', 'geographical challenges', 'remote location',
            'operational tempo', 'high workload', 'overwhelming demand', 'capacity limitations',
            'skill gaps', 'knowledge deficits', 'training limitations', 'inexperienced team',
            'technology constraints', 'legacy systems', 'outdated equipment', 'compatibility issues',
            'coordination difficulties', 'communication breakdown', 'information gaps', 'data limitations',
            'unexpected setbacks', 'unforeseen complications', 'sudden changes', 'shifting requirements',
            'ambiguous guidance', 'unclear objectives', 'conflicting instructions', 'changing priorities',
            'first-time situation', 'uncharted territory', 'no precedent', 'learning curve',
            'high visibility', 'zero tolerance for error', 'mission failure not an option',
            'lives at stake', 'national security implications', 'strategic importance',
            'overwhelming odds', 'seemingly impossible', 'against all odds', 'uphill battle'
        ]
        
        for keyword in challenge_keywords:
            if keyword in combined_text:
                score += 0.1
        
        return round(min(5, score), 1)
    
    def _score_quantifiable_results(self, achievement_data, combined_text):
        """Score based on presence of quantifiable, measurable results."""
        return round(self._find_quantifiable_metrics(combined_text), 1)
    
    def _find_quantifiable_metrics(self, text):
        """Find and score quantifiable metrics in text."""
        score = 0
        
        # Look for percentages
        percentages = _re.findall(r'(\d+(?:\.\d+)?)\s*%', text)
        if percentages:
            score += min(2, len(percentages) * 0.75)
        
        # Look for dollar amounts
        dollars = _re.findall(r'\$[\d,]+(?:\.\d{2})?', text)
        if dollars:
            score += min(2, len(dollars) * 0.75)
        
        # Look for time savings
        time_saved = _re.findall(r'(\d+)\s*(?:hours?|days?|weeks?|months?)\s*(?:saved|reduced)', text)
        if time_saved:
            score += min(1.5, len(time_saved) * 0.75)
        
        # Look for quantities
        quantities = _re.findall(r'(\d+)\s*(?:lives|people|personnel|units|systems|processes)', text)
        if quantities:
            score += min(1, len(quantities) * 0.5)
        
        return min(5, score)
    
    def _score_time_factor(self, achievement_data, combined_text):
        """
        Lenient time‑factor scorer.
        • Gives credit whenever a simple “from … to …” range is present, even if dates are placeholders.
        • Raises base scores across the board so that most narratives earn ≥ 2 / 5 by default.
        """
        import re

        time_period = achievement_data.get('time_period', '').lower()
        combined_time = (time_period + " " + combined_text).lower()

        # 1.  Default baseline now 1.5 instead of 1.0
        max_duration_score = 1.5

        # 2.  Extract explicit numeric durations
        years  = re.findall(r'(\d+(?:\.\d+)?)\s*(?:years?|yrs?)', combined_time)
        months = re.findall(r'(\d+(?:\.\d+)?)\s*(?:months?|mos?)', combined_time)
        weeks  = re.findall(r'(\d+(?:\.\d+)?)\s*(?:weeks?|wks?)', combined_time)

        if years:
            y = max(float(v) for v in years)
            if y >= 3:        # 3+ years
                max_duration_score = 5.0
            elif y >= 2:
                max_duration_score = 4.5
            elif y >= 1:
                max_duration_score = 4.0
            else:
                max_duration_score = 3.5

        elif months:
            m = max(float(v) for v in months)
            if m >= 18:
                max_duration_score = 4.0
            elif m >= 12:
                max_duration_score = 3.5
            elif m >= 6:
                max_duration_score = 3.0
            elif m >= 3:
                max_duration_score = 2.75
            else:
                max_duration_score = 2.25

        elif weeks:
            w = max(float(v) for v in weeks)
            if w >= 12:
                max_duration_score = 2.75
            elif w >= 4:
                max_duration_score = 2.25
            else:
                max_duration_score = 1.75

        # 3.  Lenient catch‑all: any “from … to …” narrative counts for 2.5
        if max_duration_score < 2.5:
            if re.search(r'from\s+[^\s]+\s+.*?\s+to\s+[^\s]+\s+', combined_time):
                max_duration_score = 2.5

        # 4.  Sustained‑performance phrases grant +0.5 (capped at 5)
        sustained_phrases = (
            'consistently', 'continuously', 'ongoing', 'sustained',
            'throughout', 'entire period', 'over the course', 'for the duration'
        )
        if any(p in combined_time for p in sustained_phrases):
            max_duration_score = min(5.0, max_duration_score + 0.5)

        return round(max_duration_score, 1)
    
    def _score_valor(self, achievement_data, combined_text):
        """Score valor and heroic actions."""
        # Enhanced valor indicators with comprehensive descriptors
        valor_indicators = [
            'valor', 'heroic', 'courageous', 'brave', 'life-threatening', 
            'dangerous', 'rescue', 'saved life', 'saved lives', 'risked',
            'perilous', 'hazardous',
            'gallant', 'fearless', 'intrepid', 'dauntless', 'undaunted', 'bold',
            'selfless', 'self-sacrifice', 'personal risk', 'risked own life', 'put life on the line',
            'life-saving action', 'heroic rescue', 'daring rescue', 'emergency rescue', 'water rescue',
            'maritime rescue', 'helicopter rescue', 'boat rescue', 'swimmer rescue', 'aviation rescue',
            'search and rescue', 'SAR operation', 'medevac', 'medical evacuation', 'casualty evacuation',
            'under fire', 'enemy action', 'combat situation', 'hostile environment', 'war zone',
            'extreme danger', 'mortal peril', 'deadly situation', 'fatal circumstances', 'near-death',
            'treacherous waters', 'rough seas', 'severe storm', 'hurricane conditions', 'blizzard conditions',
            'burning vessel', 'sinking ship', 'aircraft emergency', 'vessel in distress', 'mayday call',
            'man overboard', 'person in water', 'drowning victim', 'hypothermia rescue', 'ice rescue',
            'cliff rescue', 'mountain rescue', 'swift water rescue', 'flood rescue', 'surf rescue',
            'night rescue', 'zero visibility', 'adverse weather rescue', 'dangerous surf conditions',
            'risked personal safety', 'disregarded personal safety', 'ignored personal danger',
            'voluntarily exposed to danger', 'entered dangerous area', 'faced imminent threat',
            'extraordinary heroism', 'conspicuous gallantry', 'distinguished courage', 'exceptional bravery',
            'above and beyond', 'call of duty exceeded', 'superhuman effort', 'extraordinary determination',
            'life or death situation', 'split-second decision', 'instant response', 'immediate action',
            'without regard for safety', 'despite personal risk', 'in face of danger', 'under extreme stress',
            'prevented loss of life', 'averted disaster', 'prevented catastrophe', 'saved from certain death',
            'recovered survivors', 'extracted personnel', 'evacuated civilians', 'rescued crew members',
            'pulled from wreckage', 'freed from entrapment', 'rescued from fire', 'saved from drowning',
            'protective action', 'shielded others', 'took incoming fire', 'absorbed impact',
            'first responder', 'emergency response', 'rapid intervention', 'immediate assistance',
            'ultimate sacrifice', 'supreme dedication', 'unwavering commitment', 'steadfast courage'
        ]
        
        score = 0
        for indicator in valor_indicators:
            if indicator in combined_text:
                score += 0.2
        
        return round(min(5, score), 1)
    
    def _score_above_beyond(self, achievement_data, combined_text):
        """
        Improved scoring for 'above and beyond' with weighted tiers and stricter requirements.
        Focus on truly exceptional performance indicators.
        """
        score = 0
        
        # TIER 1: Exceptional/Heroic Level (2.0 points each, max 2 counted)
        tier1_indicators = [
            'above and beyond', 'beyond the call of duty', 'superhuman', 'heroic effort',
            'personal sacrifice', 'risked own safety', 'selfless service', 'extraordinary dedication',
            'unprecedented achievement', 'record-breaking', 'first time ever', 'never before accomplished',
            'life-threatening situation', 'extreme danger', 'against all odds', 'impossible circumstances'
        ]
        
        # TIER 2: Highly Exceptional (1.0 points each, max 3 counted)
        tier2_indicators = [
            'extraordinary', 'exceptional', 'remarkable', 'outstanding', 'exemplary',
            'far exceeded', 'significantly surpassed', 'greatly exceeded', 'vastly outperformed',
            'voluntary overtime', 'unpaid hours', 'weekend work', 'holiday duty', 'personal time',
            'additional duties', 'outside normal scope', 'beyond assigned responsibilities',
            'took charge', 'stepped up', 'personal initiative', 'self-starter', 'leadership initiative',
            'went the extra mile', 'extra effort', 'additional work', 'supplementary duties'
        ]
        
        # TIER 3: Above Standard (0.5 points each, max 4 counted)
        tier3_indicators = [
            'exceeded', 'surpassed', 'outperformed', 'exceeded expectations', 'exceeded standards',
            'surpassed goals', 'beat targets', 'over-achieved', 'delivered more than required',
            'voluntary service', 'community service', 'mentorship provided', 'coached others',
            'knowledge sharing', 'skill transfer', 'training others', 'developing personnel',
            'innovative approach', 'creative solution', 'new method', 'improved process',
            'quality focus', 'attention to detail', 'perfectionist approach', 'zero defects'
        ]
        
        # TIER 4: Professional Excellence (0.25 points each, max 4 counted)
        tier4_indicators = [
            'professional excellence', 'technical mastery', 'subject matter expertise',
            'continual improvement', 'skill development', 'professional growth',
            'team building', 'morale boosting', 'positive influence', 'role model',
            'mission success', 'goal achievement', 'objective completion', 'target met',
            'reliable performance', 'consistent results', 'dependable service'
        ]
        
        # Count matches for each tier with limits
        tier1_matches = min(2, sum(1 for indicator in tier1_indicators if indicator in combined_text))
        tier2_matches = min(2, sum(1 for indicator in tier2_indicators if indicator in combined_text))
        tier3_matches = min(2, sum(1 for indicator in tier3_indicators if indicator in combined_text))
        tier4_matches = min(4, sum(1 for indicator in tier4_indicators if indicator in combined_text))
        
        # Calculate weighted score
        score += tier1_matches * 3.0   # Max 6.0 points
        score += tier2_matches * 2.5   # Max 5.0 points  
        score += tier3_matches * 2.0   # Max 4.0 points
        score += tier4_matches * 1.5   # Max 3.0 points
        
        # Guarantee at least 0.5 pts if narrative says “outstanding” or “exemplary”
        if 'outstanding' in combined_text or 'exemplary' in combined_text:
            score = max(score, 1.0)
        
        # Additional factors that indicate truly above and beyond performance
        
        # Time sacrifice indicators (bonus up to 0.5)
        time_sacrifice_score = 0
        time_sacrifices = ['overtime', 'weekend', 'holiday', 'after hours', 'unpaid', 'personal time', 'vacation time used']
        time_sacrifice_count = sum(1 for sacrifice in time_sacrifices if sacrifice in combined_text)
        if time_sacrifice_count >= 3:
            time_sacrifice_score = 1.5
        elif time_sacrifice_count >= 2:
            time_sacrifice_score = 1.0
        elif time_sacrifice_count >= 1:
            time_sacrifice_score = 0.5
        
        # Quantifiable evidence of exceeding standards (bonus up to 0.5)
        exceed_quantifiable = 0
        import re
        
        # Look for specific percentages of improvement/exceeding
        exceed_percentages = re.findall(r'exceeded?\s+(?:by\s+)?(\d+)%', combined_text)
        exceed_percentages.extend(re.findall(r'(\d+)%\s+(?:above|over|beyond)', combined_text))
        
        if exceed_percentages:
            max_exceed = max([int(p) for p in exceed_percentages])
            if max_exceed >= 50:
                exceed_quantifiable = 0.9
            elif max_exceed >= 25:
                exceed_quantifiable = 0.75
            elif max_exceed >= 10:
                exceed_quantifiable = 0.5
        
        # Multiple responsibility areas (bonus up to 0.3)
        responsibility_bonus = 0
        responsibility_areas = ['leadership', 'training', 'operations', 'administration', 'safety', 'community']
        areas_count = sum(1 for area in responsibility_areas if area in combined_text)
        if areas_count >= 3:
            responsibility_bonus = 0.75
        elif areas_count >= 2:
            responsibility_bonus = 0.5
        elif areas_count >= 1:
            responsibility_bonus = 0.25
        
        # Add bonuses
        score += time_sacrifice_score + exceed_quantifiable + responsibility_bonus
        
        # Debug output
        print(f"ABOVE & BEYOND SCORING:")
        print(f"  Tier 1 (2.0pts): {tier1_matches} matches = {tier1_matches * 2.0} pts")
        print(f"  Tier 2 (1.0pts): {tier2_matches} matches = {tier2_matches * 1.0} pts")
        print(f"  Tier 3 (0.5pts): {tier3_matches} matches = {tier3_matches * 0.5} pts")
        print(f"  Tier 4 (0.25pts): {tier4_matches} matches = {tier4_matches * 0.25} pts")
        print(f"  Time sacrifice bonus: {time_sacrifice_score}")
        print(f"  Quantifiable exceed bonus: {exceed_quantifiable}")
        print(f"  Multiple responsibility bonus: {responsibility_bonus}")
        print(f"  TOTAL: {score}/5.0")
        
        return round(min(5.0, score), 1)
    
    def recommend_award(self, scores):
        """
        Stricter award recommendation that requires both total score AND minimum requirements.
        
        Args:
            scores: Dict containing scores for each criterion
            
        Returns:
            Dict containing the recommended award and score
        """
        total = scores.get("total_weighted", 0)
        
        print(f"Award recommendation logic - Total score: {total}")
        
        # Composite gate – require two of the Big Three (leadership, impact, scope) ≥ min score
        big_three = ("leadership", "impact", "scope")
        # Check each award from highest to lowest - MUST meet minimum requirements
        for award, threshold in self.award_thresholds.items():
            print(f"Checking {award} - Threshold: {threshold}")

            min_reqs = self.award_criteria[award].get('min_requirements', {})
            # default assumption
            meets_requirements = True

            # First, verify total‑score gate
            if total < threshold:
                meets_requirements = False

            # Next, composite Big‑Three gate
            big3_passes = sum(1 for crit in big_three
                              if scores.get(crit, 0) >= min_reqs.get(crit, 3))
            if big3_passes < 2:
                meets_requirements = False

            if meets_requirements:
                return {"award": award, "score": total, "threshold_met": True}
        
        # If no award meets strict requirements, find the highest award they qualify for by score alone
        # but mark it as not meeting requirements
        print("No awards met minimum requirements. Finding best fit by score...")
        
        for award, threshold in self.award_thresholds.items():
            if total >= threshold:
                print(f"✓ Fallback recommendation: {award} (score-based only)")
                return {"award": award, "score": total, "threshold_met": False}
        
        # Absolute fallback
        print("✓ Default recommendation: Coast Guard Letter of Commendation")
        return {"award": "Coast Guard Letter of Commendation", "score": total, "threshold_met": True}
    
    def generate_explanation(self, award, achievement_data, scores):
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
        
        # Add scoring summary
        total_score = scores.get('total_weighted', 0)
        threshold = criteria.get('threshold', 0)
        explanation += f"<p><strong>Score:</strong> {total_score} (Threshold: {threshold})</p>"
        
        explanation += "<h4>Justification:</h4>"
        explanation += f"<p>{achievement_data.get('justification', 'Based on the provided accomplishments and their impact.')}</p>"
        
        # Key achievements
        achievements = achievement_data.get("achievements", [])
        if achievements:
            explanation += "<h4>Key Achievements:</h4>"
            explanation += "<ul>"
            for achievement in achievements[:5]:  # Limit to top 5
                explanation += f"<li>{achievement}</li>"
            explanation += "</ul>"
        
        # Quantifiable impacts
        impacts = achievement_data.get("impacts", [])
        if impacts:
            explanation += "<h4>Measurable Impact:</h4>"
            explanation += "<ul>"
            for impact in impacts[:5]:  # Limit to top 5
                explanation += f"<li>{impact}</li>"
            explanation += "</ul>"
        
        # Leadership details
        leadership = achievement_data.get("leadership_details", [])
        if leadership:
            explanation += "<h4>Leadership Demonstrated:</h4>"
            explanation += "<ul>"
            for item in leadership[:3]:  # Limit to top 3
                explanation += f"<li>{item}</li>"
            explanation += "</ul>"
        
        # Innovation details
        innovations = achievement_data.get("innovation_details", [])
        if innovations:
            explanation += "<h4>Innovation and Initiative:</h4>"
            explanation += "<ul>"
            for item in innovations[:3]:  # Limit to top 3
                explanation += f"<li>{item}</li>"
            explanation += "</ul>"
        
        # Scope
        scope = achievement_data.get("scope", "")
        if scope and scope != "Not specified":
            explanation += f"<h4>Scope of Impact:</h4>"
            explanation += f"<p>{scope}</p>"
        
        # Challenges overcome
        challenges = achievement_data.get("challenges", [])
        if challenges:
            explanation += "<h4>Challenges Overcome:</h4>"
            explanation += "<ul>"
            for challenge in challenges[:3]:  # Limit to top 3
                explanation += f"<li>{challenge}</li>"
            explanation += "</ul>"
        
        # Time period
        time_period = achievement_data.get("time_period", "")
        if time_period and time_period != "Not specified":
            explanation += f"<h4>Time Period:</h4>"
            explanation += f"<p>{time_period}</p>"
        
        # Scoring breakdown
        explanation += "<h4>Scoring Analysis:</h4>"
        explanation += "<div class='scoring-breakdown'>"
        
        high_scores = []
        medium_scores = []
        low_scores = []
        
        for criterion, score in scores.items():
            if criterion != 'total_weighted' and score > 0:
                if score >= 4:
                    high_scores.append(f"{criterion.replace('_', ' ').title()}: {score}/5")
                elif score >= 2:
                    medium_scores.append(f"{criterion.replace('_', ' ').title()}: {score}/5")
                else:
                    low_scores.append(f"{criterion.replace('_', ' ').title()}: {score}/5")
        
        if high_scores:
            explanation += f"<p><strong>Strong Areas:</strong> {', '.join(high_scores)}</p>"
        if medium_scores:
            explanation += f"<p><strong>Good Areas:</strong> {', '.join(medium_scores)}</p>"
        if low_scores:
            explanation += f"<p><strong>Areas for Improvement:</strong> {', '.join(low_scores)}</p>"
        
        explanation += "</div>"
        
        return explanation
    
    def generate_improvement_suggestions(self, award, achievement_data):
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
        
        if current_index >= 0 and current_index < len(award_hierarchy) - 1:
            next_award = award_hierarchy[current_index + 1]
            suggestions.append(f"To potentially qualify for a {next_award}, focus on broader scope, greater leadership responsibility, and more significant quantifiable impact")
        
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
# Alias: if the enhanced impact scorer isn’t present, fall back to the strict version
if not hasattr(AwardEngine, "_score_impact_enhanced"):
    AwardEngine._score_impact_enhanced = AwardEngine._score_impact

# ------------------------------------------------------------------
# Graceful fallback aliases: map *_enhanced methods to baseline
# versions when they are not explicitly implemented.

_alias_pairs = {
    "_score_impact_enhanced": "_score_impact",
    "_score_innovation_enhanced": "_score_innovation",
    "_score_scope_enhanced": "_score_scope",
    "_score_challenges_enhanced": "_score_challenges",
}

for enhanced_name, base_name in _alias_pairs.items():
    if not hasattr(AwardEngine, enhanced_name) and hasattr(AwardEngine, base_name):
        setattr(AwardEngine, enhanced_name, getattr(AwardEngine, base_name))
        print(f"[Alias] {enhanced_name} → {base_name}")