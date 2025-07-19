"""
Advanced Coast Guard Award Citation Generator
Creates rich, narrative citations that match official CG language and style.
"""

import re
import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class CitationGenerator:
    """Generates compelling award citations in Coast Guard style."""
    
    # Opening phrases by award type
    OPENING_PHRASES = {
        "Distinguished Service Medal": "is cited for exceptionally meritorious service to the Government of the United States in a position of great responsibility",
        "Legion of Merit": "is cited for outstanding meritorious service",
        "Distinguished Flying Cross": "is cited for extraordinary heroism while participating in aerial flight",
        "Coast Guard Medal": "is cited for extraordinary heroism",
        "Bronze Star Medal": "For meritorious achievement in connection with combat operations",
        "Meritorious Service Medal": "is cited for meritorious service in the performance of duty",
        "Air Medal": "is cited for meritorious achievement in aerial flight",
        "Coast Guard Commendation Medal": "is cited for outstanding achievement",
        "Coast Guard Achievement Medal": "is cited for superior performance of duty",
        "Coast Guard Letter of Commendation": "For outstanding performance of duty"
    }
    
    # Powerful descriptive adjectives by category
    ADJECTIVES = {
        'leadership': ['exceptional', 'superb', 'outstanding', 'superior', 'extraordinary', 'aggressive', 
                      'decisive', 'unwavering', 'steadfast', 'tireless', 'masterful'],
        'skill': ['expert', 'precise', 'skillful', 'comprehensive', 'meticulous', 'flawless', 
                 'exceptional', 'remarkable', 'superlative'],
        'dedication': ['dedicated', 'devoted', 'committed', 'zealous', 'passionate', 'relentless',
                      'unfailing', 'unrelenting', 'persistent'],
        'courage': ['courageous', 'fearless', 'heroic', 'valiant', 'daring', 'intrepid', 'bold'],
        'innovation': ['innovative', 'creative', 'pioneering', 'groundbreaking', 'visionary', 'ingenious'],
        'impact': ['significant', 'critical', 'vital', 'essential', 'instrumental', 'pivotal', 'crucial']
    }
    
    # Transition phrases for narrative flow
    TRANSITIONS = {
        'addition': ['Additionally', 'Furthermore', 'Moreover', 'In addition'],
        'sequence': ['Subsequently', 'Following this success', 'Building upon these efforts'],
        'contrast': ['Despite', 'In spite of', 'Overcoming', 'Notwithstanding'],
        'result': ['As a result', 'Consequently', 'This directly resulted in', 'These efforts yielded'],
        'emphasis': ['Notably', 'Particularly noteworthy', 'Of special significance', 'Most importantly']
    }
    
    # Action verbs by category
    ACTION_VERBS = {
        'leadership': ['spearheaded', 'orchestrated', 'directed', 'championed', 'pioneered', 'galvanized'],
        'management': ['expertly managed', 'skillfully coordinated', 'masterfully oversaw', 'efficiently administered'],
        'achievement': ['accomplished', 'achieved', 'attained', 'secured', 'realized', 'delivered'],
        'innovation': ['developed', 'engineered', 'devised', 'formulated', 'conceived', 'designed'],
        'improvement': ['enhanced', 'optimized', 'streamlined', 'transformed', 'revolutionized', 'modernized']
    }
    
    # Closing phrases by award type
    CLOSING_PHRASES = {
        "Distinguished Service Medal": "{name}'s leadership, dedication, and devotion to duty are most heartily commended and are in keeping with the highest traditions of the United States Coast Guard.",
        "Legion of Merit": "{name}'s ability, diligence, and devotion to duty are most heartily commended and are in keeping with the highest traditions of the United States Coast Guard.",
        "Distinguished Flying Cross": "{name}'s courage, judgment, and devotion to duty in the face of hazardous conditions are most heartily commended and are in keeping with the highest traditions of the United States Coast Guard.",
        "Coast Guard Medal": "{name}'s courage and devotion to duty are in keeping with the highest traditions of the United States Coast Guard.",
        "Bronze Star Medal": "{name}'s courage and devotion to duty reflect great credit upon {pronoun} and are in keeping with the highest traditions of the United States Coast Guard.",
        "Meritorious Service Medal": "{name}'s dedication and devotion to duty are most heartily commended and are in keeping with the highest traditions of the United States Coast Guard.",
        "Air Medal": "{name}'s courage, judgment, and devotion to duty are most heartily commended and are in keeping with the highest traditions of the United States Coast Guard.",
        "Coast Guard Commendation Medal": "{name}'s dedication, judgment, and devotion to duty are most heartily commended and are in keeping with the highest traditions of the United States Coast Guard.",
        "Coast Guard Achievement Medal": "{name}'s diligence, perseverance, and devotion to duty are most heartily commended and are in keeping with the highest traditions of the United States Coast Guard.",
        "Coast Guard Letter of Commendation": "By your meritorious service you have upheld the highest traditions of the United States Coast Guard."
    }
    
    # Line limits for each award
    LINE_LIMITS = {
        "Distinguished Service Medal": 16,
        "Legion of Merit": 16,
        "Meritorious Service Medal": 12,
        "Coast Guard Commendation Medal": 12,
        "Coast Guard Achievement Medal": 12,
        "Coast Guard Letter of Commendation": 12,
        "Air Medal": 12,
        "Distinguished Flying Cross": 14,
        "Coast Guard Medal": 14,
        "Bronze Star Medal": 14
    }
    
    def __init__(self):
        self.max_line_length = 95  # Characters per line for landscape
        
    def generate_citation(self, award_type: str, awardee_info: Dict, achievement_data: Dict) -> str:
        """
        Generate a compelling, narrative citation that maximizes line count.
        
        Args:
            award_type: Type of award
            awardee_info: Member information
            achievement_data: Achievements and impacts
            
        Returns:
            Formatted citation text
        """
        # Extract member info
        name = awardee_info.get('name', 'Member')
        last_name = name.split()[-1] if name else 'Member'
        rank = awardee_info.get('rank', '')
        unit = awardee_info.get('unit', '')
        position = awardee_info.get('position', '')
        
        # Get time period
        time_period = achievement_data.get('time_period', '')
        if not time_period or time_period == "Not specified":
            time_period = "[dates of service]"
            
        # Determine pronoun based on name
        pronoun = self._determine_pronoun(name)
        
        # Build the citation narrative
        narrative_parts = []
        
        # Opening with member identification
        opening = self._build_opening(award_type, rank, last_name, position, unit, time_period)
        narrative_parts.append(opening)
        
        # Build rich narrative body - aim for MORE content than needed
        body_sentences = self._build_narrative_body(achievement_data, rank, last_name, pronoun)
        
        # Add extra detail sentences if we have room
        extra_sentences = self._generate_additional_context(achievement_data, rank, last_name, pronoun)
        body_sentences.extend(extra_sentences)
        
        narrative_parts.extend(body_sentences)
        
        # Add closing
        closing = self._build_closing(award_type, rank, last_name, pronoun)
        narrative_parts.append(closing)
        
        # Combine into full narrative
        full_citation = " ".join(narrative_parts)
        
        # Format to maximize character usage per line
        formatted_citation = self._format_to_maximize_usage(full_citation, award_type)
        
        return formatted_citation
        
    def _build_opening(self, award_type: str, rank: str, last_name: str, 
                      position: str, unit: str, time_period: str) -> str:
        """Build the opening sentence with proper identification."""
        # Format rank and name
        if rank:
            member_ref = f"{self._format_rank(rank)} {last_name.upper()}"
        else:
            member_ref = f"Petty Officer {last_name.upper()}"
            
        # Get opening phrase
        opening_phrase = self.OPENING_PHRASES.get(award_type, "is cited for outstanding achievement")
        
        # Build complete opening
        parts = [member_ref, opening_phrase]
        
        # Add position and unit
        if position and unit:
            parts.append(f"while serving as {position}, {unit},")
        elif unit:
            parts.append(f"while serving at {unit},")
        elif position:
            parts.append(f"while serving as {position},")
            
        parts.append(f"from {time_period}.")
        
        return " ".join(parts)
        
    def _build_narrative_body(self, achievement_data: Dict, rank: str, last_name: str, pronoun: str) -> List[str]:
        """Build the narrative body with rich, descriptive sentences."""
        sentences = []
        
        # Extract data
        achievements = achievement_data.get('achievements', [])
        impacts = achievement_data.get('impacts', [])
        leadership = achievement_data.get('leadership_details', [])
        innovations = achievement_data.get('innovation_details', [])
        challenges = achievement_data.get('challenges', [])
        
        # Determine primary narrative focus
        has_leadership = bool(leadership) or any('led' in a.lower() or 'supervised' in a.lower() for a in achievements)
        has_innovation = bool(innovations) or any('developed' in a.lower() or 'created' in a.lower() for a in achievements)
        has_challenges = bool(challenges)
        
        # Build leadership narrative if applicable
        if has_leadership:
            leadership_sentence = self._build_leadership_sentence(achievements, leadership, impacts, pronoun)
            if leadership_sentence:
                sentences.append(leadership_sentence)
                
        # Build primary achievement narrative
        achievement_sentences = self._build_achievement_narrative(achievements, impacts, pronoun)
        sentences.extend(achievement_sentences)
        
        # Add innovation narrative if applicable
        if has_innovation:
            innovation_sentence = self._build_innovation_sentence(innovations, achievements, impacts, pronoun)
            if innovation_sentence:
                sentences.append(innovation_sentence)
                
        # Add challenge narrative if applicable
        if has_challenges:
            challenge_sentence = self._build_challenge_sentence(challenges, rank, last_name, pronoun)
            if challenge_sentence:
                sentences.append(challenge_sentence)
                
        # Add impact summary
        impact_sentence = self._build_impact_summary(impacts, achievements, pronoun)
        if impact_sentence:
            sentences.append(impact_sentence)
            
        # Add collaboration/recognition if space allows
        if len(sentences) < 8:  # Leave room for more detail
            extra_sentences = self._build_additional_details(achievement_data, rank, last_name, pronoun)
            sentences.extend(extra_sentences[:2])  # Add up to 2 more sentences
            
        return sentences
        
    def _build_leadership_sentence(self, achievements: List[str], 
                                 leadership: List[str], impacts: List[str], pronoun: str) -> Optional[str]:
        """Build a compelling leadership sentence."""
        # Find leadership-related content
        leadership_items = []
        
        for item in leadership:
            if any(word in item.lower() for word in ['led', 'supervised', 'managed', 'directed']):
                leadership_items.append(item)
                
        for achievement in achievements:
            if any(word in achievement.lower() for word in ['led', 'supervised', 'team', 'personnel']):
                leadership_items.append(achievement)
                
        if not leadership_items:
            return None
            
        # Choose the most impactful
        item = leadership_items[0]
        
        # Extract numbers if present
        numbers = re.findall(r'\d+', item)
        
        # Build sentence with powerful language
        adj = random.choice(self.ADJECTIVES['leadership'])
        
        if numbers:
            return f"Demonstrating {adj} leadership and vision, {pronoun} {self._clean_for_narrative(item)}."
        else:
            return f"Through {adj} leadership, {pronoun} {self._clean_for_narrative(item)}."
            
    def _build_achievement_narrative(self, achievements: List[str], impacts: List[str], pronoun: str) -> List[str]:
        """Build the main achievement narrative with multiple sentences."""
        sentences = []
        
        # Group achievements by type
        operational = []
        quantifiable = []
        innovative = []
        
        for achievement in achievements:
            if any(char.isdigit() for char in achievement):
                quantifiable.append(achievement)
            elif any(word in achievement.lower() for word in ['developed', 'created', 'designed', 'implemented']):
                innovative.append(achievement)
            else:
                operational.append(achievement)
                
        # Build operational excellence sentence
        if operational:
            verb = random.choice(self.ACTION_VERBS['achievement'])
            adj = random.choice(self.ADJECTIVES['skill'])
            achievement_text = self._clean_for_narrative(operational[0])
            # Create more natural sentence flow
            if 'developed' in achievement_text.lower() or 'created' in achievement_text.lower():
                sentences.append(f"{pronoun.capitalize()} {achievement_text} with {adj} expertise.")
            else:
                sentences.append(f"Through {adj} dedication, {pronoun} {achievement_text}.")
            
        # Build quantifiable impact sentences
        if quantifiable:
            # Check if we've already used these achievements
            used_achievements = []
            for sent in sentences:
                used_achievements.extend(sent.lower().split())
            
            # First quantifiable achievement
            pronoun_possessive = 'Her' if pronoun == 'she' else 'His'
            
            # Skip if already used
            if not any(key_word in " ".join(used_achievements) for key_word in ['tons', 'ammunition'] if key_word in quantifiable[0].lower()):
                achievement_text = self._clean_for_narrative(quantifiable[0])
                if not any(verb in achievement_text.lower() for verb in ['led', 'managed', 'supervised', 'directed', 'achieved']):
                    verb = random.choice(['resulted in', 'included', 'encompassed'])
                    sentences.append(f"{pronoun_possessive} extraordinary efforts {verb} {achievement_text}.")
                else:
                    sentences.append(f"{pronoun_possessive} exceptional performance {achievement_text}.")
            
            # Additional quantifiable achievements
            if len(quantifiable) > 1:
                achievement_text = self._clean_for_narrative(quantifiable[1])
                # Skip if similar content already used
                if not any(key_word in " ".join(used_achievements) for key_word in achievement_text.lower().split()[:3]):
                    transition = random.choice(self.TRANSITIONS['addition'])
                    # Ensure the achievement flows properly
                    first_word = achievement_text.split()[0].lower() if achievement_text else ""
                    if first_word in ['led', 'managed', 'supervised', 'directed', 'spearheaded', 'orchestrated']:
                        sentences.append(f"{transition}, {pronoun} {achievement_text}.")
                    elif any(word in achievement_text.lower() for word in ['distribution', 'development', 'management']):
                        sentences.append(f"{transition}, {pronoun} orchestrated {achievement_text}.")
                    else:
                        sentences.append(f"{transition}, {pronoun} {achievement_text}.")
                
        # Build innovative achievement sentence
        if innovative and len(sentences) < 6:
            achievement_text = self._clean_for_narrative(innovative[0])
            # Check if achievement already contains development verbs
            if any(verb in achievement_text.lower() for verb in ['developed', 'created', 'designed', 'engineered']):
                sentences.append(f"Through innovative thinking, {pronoun} {achievement_text}.")
            else:
                verb = random.choice(self.ACTION_VERBS['innovation'])
                sentences.append(f"{pronoun.capitalize()} {verb} {achievement_text}.")
            
        return sentences
        
    def _build_innovation_sentence(self, innovations: List[str], 
                                 achievements: List[str], impacts: List[str], pronoun: str) -> Optional[str]:
        """Build a sentence highlighting innovation."""
        innovation_items = innovations[:]
        
        # Find innovation in achievements
        for achievement in achievements:
            if any(word in achievement.lower() for word in ['developed', 'created', 'pioneered', 'designed']):
                innovation_items.append(achievement)
                
        if not innovation_items:
            return None
            
        item = innovation_items[0]
        cleaned_item = self._clean_for_narrative(item)
        adj = random.choice(self.ADJECTIVES['innovation'])
        
        # Look for impact
        impact_clause = ""
        if impacts:
            impact_clause = f", which {self._find_related_impact(item, impacts)}"
            
        pronoun_possessive = 'Her' if pronoun == 'she' else 'His'
        
        # Check if item already contains approach/solution words
        if any(word in cleaned_item.lower() for word in ['approach', 'solution', 'method', 'system']):
            return f"{pronoun_possessive} {adj} {cleaned_item}{impact_clause}."
        else:
            return f"{pronoun_possessive} {adj} approach {cleaned_item}{impact_clause}."
        
    def _build_challenge_sentence(self, challenges: List[str], rank: str, last_name: str, pronoun: str) -> Optional[str]:
        """Build a sentence about overcoming challenges."""
        if not challenges:
            return None
            
        challenge = challenges[0]
        challenge_text = self._clean_for_narrative(challenge)
        
        # Check if challenge already starts with a verb
        first_word = challenge_text.split()[0].lower() if challenge_text else ""
        pronoun_possessive = 'her' if pronoun == 'she' else 'his'
        
        if first_word in ['overcame', 'faced', 'navigated', 'managed']:
            # Challenge already has a verb, use different structure
            return f"Although {pronoun} {challenge_text}, {pronoun_possessive} determination and expertise ensured mission success."
        else:
            transition = random.choice(self.TRANSITIONS['contrast'])
            return f"{transition} {challenge_text}, {pronoun_possessive} determination and expertise ensured mission success."
        
    def _build_impact_summary(self, impacts: List[str], achievements: List[str], pronoun: str) -> Optional[str]:
        """Build a summary sentence of overall impact."""
        significant_impacts = []
        
        # Find quantifiable impacts
        for impact in impacts:
            if any(char in impact for char in ['$', '%']) or any(word in impact.lower() for word in ['saved', 'increased', 'reduced']):
                significant_impacts.append(impact)
                
        if not significant_impacts:
            return None
            
        # Build impact sentence
        if len(significant_impacts) == 1:
            return f"These efforts directly resulted in {self._clean_for_narrative(significant_impacts[0])}."
        else:
            impact1 = self._clean_for_narrative(significant_impacts[0])
            impact2 = self._clean_for_narrative(significant_impacts[1])
            pronoun_possessive = 'Her' if pronoun == 'she' else 'His'
            return f"{pronoun_possessive} contributions yielded exceptional results, including {impact1} and {impact2}."
            
    def _build_additional_details(self, achievement_data: Dict, rank: str, last_name: str, pronoun: str) -> List[str]:
        """Build additional detail sentences to maximize line count."""
        sentences = []
        
        # Add scope of impact
        scope = achievement_data.get('scope', '')
        if scope and scope != 'Not specified':
            adj = random.choice(self.ADJECTIVES['impact'])
            pronoun_possessive = 'her' if pronoun == 'she' else 'his'
            sentences.append(f"The {adj} impact of {pronoun_possessive} efforts extended throughout {scope}.")
            
        # Add collaboration details
        if 'joint' in str(achievement_data).lower() or 'inter-agency' in str(achievement_data).lower():
            pronoun_possessive = 'Her' if pronoun == 'she' else 'His'
            sentences.append(f"{pronoun_possessive} collaborative approach fostered unprecedented inter-agency cooperation and operational synergy.")
            
        # Add recognition
        if 'award' in str(achievement_data).lower() or 'recognized' in str(achievement_data).lower():
            pronoun_possessive = 'Her' if pronoun == 'she' else 'His'
            sentences.append(f"{pronoun_possessive} exceptional performance earned widespread recognition from senior leadership.")
            
        return sentences
        
    def _generate_additional_context(self, achievement_data: Dict, rank: str, last_name: str, pronoun: str) -> List[str]:
        """Generate additional contextual sentences to fill space."""
        additional = []
        
        # Add time-based context
        time_period = achievement_data.get('time_period', '')
        if 'year' in time_period.lower() or 'month' in time_period.lower():
            duration_match = re.search(r'(\d+)\s*(year|month)', time_period.lower())
            if duration_match:
                num = duration_match.group(1)
                unit = duration_match.group(2)
                additional.append(f"Throughout this {num}-{unit} period, {pronoun} maintained unwavering commitment to excellence.")
        
        # Add quantitative summaries
        all_numbers = []
        for field in ['achievements', 'impacts', 'quantifiable_metrics']:
            for item in achievement_data.get(field, []):
                numbers = re.findall(r'\$?[\d,]+\.?\d*\s*(?:million|thousand|percent|%)?', str(item))
                all_numbers.extend(numbers)
        
        if len(all_numbers) >= 3:
            pronoun_possessive = 'her' if pronoun == 'she' else 'his'
            additional.append(f"These remarkable metrics underscore {pronoun_possessive} exceptional contribution to mission success.")
        
        # Add leadership amplification
        if achievement_data.get('leadership_details'):
            pronoun_possessive = 'her' if pronoun == 'she' else 'his'
            additional.append(f"Under {pronoun_possessive} inspired guidance, unit morale and operational effectiveness reached unprecedented levels.")
        
        # Add innovation emphasis
        if achievement_data.get('innovation_details'):
            additional.append(f"This innovative mindset permeated throughout the organization, inspiring others to pursue creative solutions.")
        
        # Add closing amplification
        pronoun_possessive = 'her' if pronoun == 'she' else 'his'
        additional.append(f"The lasting legacy of {pronoun_possessive} contributions will benefit the Coast Guard for years to come.")
        
        return additional
        
    def _build_closing(self, award_type: str, rank: str, last_name: str, pronoun: str) -> str:
        """Build the closing statement."""
        # Format member reference
        if rank:
            member_ref = f"{self._format_rank(rank)} {last_name.upper()}"
        else:
            member_ref = f"Petty Officer {last_name.upper()}"
            
        # Get closing template
        closing_template = self.CLOSING_PHRASES.get(award_type,
            "{name}'s dedication and devotion to duty are most heartily commended and are in keeping with the highest traditions of the United States Coast Guard.")
            
        pronoun_reflexive = 'herself' if pronoun == 'she' else 'himself'
        return closing_template.format(name=member_ref, pronoun=pronoun_reflexive)
        
    def _format_to_lines(self, citation: str, award_type: str) -> str:
        """Format citation to maximize lines within limits."""
        max_lines = self.LINE_LIMITS.get(award_type, 12)
        
        # Split into words
        words = citation.split()
        
        # Build lines trying to maximize usage
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_length = len(word)
            
            # Check if adding this word would exceed line length
            # Calculate the actual line length including spaces
            if current_line:
                test_line = " ".join(current_line + [word])
                if len(test_line) > self.max_line_length:
                    lines.append(" ".join(current_line))
                    current_line = [word]
                    current_length = word_length
                else:
                    current_line.append(word)
                    current_length += word_length + 1  # +1 for space
            else:
                current_line.append(word)
                current_length = word_length
                
        # Add final line
        if current_line:
            lines.append(" ".join(current_line))
            
        # If we have too few lines, try to rebalance
        if len(lines) < max_lines - 2:
            lines = self._rebalance_lines(lines, max_lines)
            
        # If we have too many lines, we need to condense
        if len(lines) > max_lines:
            lines = self._condense_lines(lines, max_lines)
            
        return "\n".join(lines)
        
    def _rebalance_lines(self, lines: List[str], target_lines: int) -> List[str]:
        """Rebalance lines to get closer to target line count."""
        # Calculate target characters per line
        total_chars = sum(len(line) for line in lines)
        target_chars_per_line = total_chars // target_lines
        
        # Rebuild with shorter lines
        all_words = " ".join(lines).split()
        new_lines = []
        current_line = []
        current_length = 0
        
        for word in all_words:
            word_length = len(word)
            
            space_count = len(current_line) - 1 if current_line else 0
            if current_line and current_length + word_length + space_count + 1 > target_chars_per_line:
                new_lines.append(" ".join(current_line))
                current_line = [word]
                current_length = word_length
            else:
                current_line.append(word)
                current_length += word_length
                
        if current_line:
            new_lines.append(" ".join(current_line))
            
        return new_lines
        
    def _condense_lines(self, lines: List[str], max_lines: int) -> List[str]:
        """Condense citation to fit within line limits."""
        # This is a fallback - we should rarely need this with proper generation
        text = " ".join(lines)
        
        # Remove less critical phrases - DISABLED due to issues with decimal numbers
        # These patterns were matching decimal points (like 28.6) as sentence endings
        # causing text like "FREEDOM. Furthermore... 28.6 million" to become "FREEDOM..6 million"
        # condensing_patterns = [
        #     (r'\s+Additionally,[^.]+\.', '.'),  # Problem: matches decimal points
        #     (r'\s+Furthermore,[^.]+\.', '.'),   # Problem: matches decimal points
        #     (r',\s+which\s+[^,]+,', ','),      # This one might be OK
        # ]
        
        # for pattern, replacement in condensing_patterns:
        #     text = re.sub(pattern, replacement, text)
            
        # Re-split into lines WITHOUT calling _format_to_lines to avoid recursion
        words = text.split()
        new_lines = []
        current_line = []
        
        for word in words:
            if current_line:
                test_line = " ".join(current_line + [word])
                if len(test_line) > self.max_line_length:
                    new_lines.append(" ".join(current_line))
                    current_line = [word]
                else:
                    current_line.append(word)
            else:
                current_line.append(word)
                
        if current_line:
            new_lines.append(" ".join(current_line))
            
        # If still too long, truncate
        if len(new_lines) > max_lines:
            new_lines = new_lines[:max_lines]
            
        return new_lines
        
    def _clean_for_narrative(self, text: str) -> str:
        """Clean text for use in narrative."""
        # Remove leading/trailing whitespace and periods
        text = text.strip().rstrip('.')
        
        # Ensure lowercase for mid-sentence flow (unless it starts with an acronym)
        if text and text[0].isupper() and not text.split()[0].isupper():
            text = text[0].lower() + text[1:]
            
        return text
        
    def _format_rank(self, rank: str) -> str:
        """Format rank with proper capitalization."""
        parts = rank.split()
        formatted_parts = []
        
        for part in parts:
            if part.lower() in ['first', 'second', 'third', 'class']:
                formatted_parts.append(part.capitalize())
            else:
                formatted_parts.append(part.title())
                
        return ' '.join(formatted_parts)
        
    def _find_related_impact(self, achievement: str, impacts: List[str]) -> str:
        """Find an impact related to an achievement."""
        # Simple keyword matching for now
        achievement_lower = achievement.lower()
        
        for impact in impacts:
            impact_lower = impact.lower()
            # Look for common words
            if any(word in impact_lower for word in achievement_lower.split() if len(word) > 4):
                return self._clean_for_narrative(impact)
                
        # Return first impact if no match
        return self._clean_for_narrative(impacts[0]) if impacts else "enhanced operational effectiveness"
    
    def _determine_pronoun(self, name: str) -> str:
        """Determine appropriate pronoun based on name."""
        # In a real system, this would be configurable or based on user preference
        # For now, using a simple heuristic based on common names
        female_indicators = ['sarah', 'mary', 'jennifer', 'jessica', 'lisa', 'nancy', 
                           'karen', 'betty', 'dorothy', 'susan', 'margaret', 'carol',
                           'patricia', 'barbara', 'elizabeth', 'maria', 'donna', 'laura']
        
        first_name = name.split()[0].lower() if name else ''
        
        if any(indicator in first_name for indicator in female_indicators):
            return 'she'
        else:
            return 'he'  # Default for military citations when gender unknown
    
    def _format_to_maximize_usage(self, citation: str, award_type: str) -> str:
        """Format citation to maximize character usage per line."""
        max_lines = self.LINE_LIMITS.get(award_type, 12)
        target_chars_per_line = self.max_line_length - 5  # Aim for 90 chars minimum
        
        # First, split into sentences
        sentences = self._split_into_sentences(citation)
        
        # Build lines with maximum character usage
        lines = []
        current_line = []
        current_length = 0
        sentence_index = 0
        
        while sentence_index < len(sentences) and len(lines) < max_lines - 1:  # Save last line for closing
            sentence = sentences[sentence_index]
            words = sentence.split()
            word_index = 0
            
            while word_index < len(words):
                word = words[word_index]
                
                # Calculate if adding this word keeps us under limit
                if current_line:
                    test_line = " ".join(current_line + [word])
                    test_length = len(test_line)
                else:
                    test_line = word
                    test_length = len(word)
                
                if test_length <= self.max_line_length:
                    # Word fits, add it
                    current_line.append(word)
                    current_length = test_length
                    word_index += 1
                    
                    # Check if we're close to the target and could add more
                    if current_length >= target_chars_per_line and word_index < len(words):
                        # See if we can fit one more short word
                        next_word = words[word_index]
                        if len(next_word) <= 4 and len(" ".join(current_line + [next_word])) <= self.max_line_length:
                            current_line.append(next_word)
                            word_index += 1
                            
                else:
                    # Word doesn't fit
                    if current_length < target_chars_per_line and len(lines) < max_lines - 2:
                        # Line is too short, try to add filler words
                        current_line = self._expand_line(current_line, self.max_line_length)
                    
                    # Save the line
                    lines.append(" ".join(current_line))
                    current_line = [word]
                    current_length = len(word)
                    word_index += 1
            
            sentence_index += 1
        
        # Add remaining content
        if current_line:
            # Expand the last line if it's too short
            if len(" ".join(current_line)) < target_chars_per_line:
                current_line = self._expand_line(current_line, self.max_line_length)
            lines.append(" ".join(current_line))
        
        # Handle the closing sentence specially
        closing_markers = ["dedication and devotion to duty", "traditions of the United States Coast Guard"]
        
        # Check if closing is already properly formatted in lines
        closing_found = False
        closing_line_start = -1
        for i, line in enumerate(lines):
            if any(marker in line for marker in closing_markers):
                closing_found = True
                closing_line_start = i
                break
        
        # If closing found but incomplete (doesn't end with "Coast Guard"), complete it
        if closing_found and closing_line_start >= 0:
            # Check if the closing continues to the end properly
            remaining_text = " ".join(lines[closing_line_start:])
            if "United States Coast Guard" not in remaining_text:
                # Find the full closing sentence
                for sent in sentences:
                    if any(marker in sent for marker in closing_markers):
                        # Replace the partial closing with the full one
                        lines = lines[:closing_line_start]
                        
                        # Format the full closing
                        closing_words = sent.split()
                        current_closing_line = []
                        
                        for word in closing_words:
                            test_line = " ".join(current_closing_line + [word])
                            if len(test_line) <= self.max_line_length:
                                current_closing_line.append(word)
                            else:
                                if current_closing_line:
                                    lines.append(" ".join(current_closing_line))
                                current_closing_line = [word]
                        
                        if current_closing_line:
                            lines.append(" ".join(current_closing_line))
                        break
        
        # Final check: ensure we don't exceed max lines
        if len(lines) > max_lines:
            lines = lines[:max_lines]
        
        return "\n".join(lines)
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences, preserving periods in numbers."""
        # Simple sentence splitter that preserves decimal numbers
        sentences = []
        current = []
        words = text.split()
        
        for i, word in enumerate(words):
            current.append(word)
            
            # Check if this word ends a sentence
            if word.endswith('.') and not (i + 1 < len(words) and words[i + 1][0].islower()):
                # Don't split on decimal points
                if not re.match(r'\d+\.$', word):
                    sentences.append(" ".join(current))
                    current = []
        
        if current:
            sentences.append(" ".join(current))
            
        return sentences
    
    def _expand_line(self, words: List[str], max_length: int) -> List[str]:
        """Expand a line by adding descriptive words to fill space."""
        expanded = words[:]
        current_length = len(" ".join(expanded))
        
        # Expansion words by context
        expansions = {
            'the': ['the exceptional', 'the remarkable', 'the outstanding'],
            'his': ['his exemplary', 'his distinguished', 'his exceptional'],
            'her': ['her exemplary', 'her distinguished', 'her exceptional'],
            'and': ['and notably', 'and significantly', 'and importantly'],
            'with': ['with remarkable', 'with exceptional', 'with outstanding'],
            'through': ['through dedicated', 'through persistent', 'through tireless'],
            'for': ['for critical', 'for essential', 'for vital'],
            'of': ['of significant', 'of critical', 'of exceptional'],
            'in': ['in crucial', 'in critical', 'in essential'],
            'to': ['to successfully', 'to effectively', 'to expertly'],
        }
        
        # Try to expand articles and prepositions
        i = 0
        while i < len(expanded) and current_length < max_length - 10:
            word = expanded[i].lower()
            base_word = word.rstrip('.,;:')
            
            if base_word in expansions:
                # Find the shortest expansion that fits
                for expansion in sorted(expansions[base_word], key=len):
                    test_expanded = expanded[:]
                    test_expanded[i] = expansion + word[len(base_word):]  # Preserve punctuation
                    test_length = len(" ".join(test_expanded))
                    
                    if test_length <= max_length:
                        expanded = test_expanded
                        current_length = test_length
                        break
            
            i += 1
        
        return expanded