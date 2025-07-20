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
    
    # Character limits for each award (based on line limits x 125 chars per line)
    CHARACTER_LIMITS = {
        "Distinguished Service Medal": 2000,  # 16 lines x 125 chars
        "Legion of Merit": 2000,              # 16 lines x 125 chars
        "Meritorious Service Medal": 1500,   # 12 lines x 125 chars
        "Coast Guard Commendation Medal": 1500,  # 12 lines x 125 chars
        "Coast Guard Achievement Medal": 1500,    # 12 lines x 125 chars
        "Coast Guard Letter of Commendation": 1500,  # 12 lines x 125 chars
        "Air Medal": 1500,                    # 12 lines x 125 chars
        "Distinguished Flying Cross": 1750,   # 14 lines x 125 chars
        "Coast Guard Medal": 1750,            # 14 lines x 125 chars
        "Bronze Star Medal": 1750            # 14 lines x 125 chars
    }
    
    def __init__(self):
        self.max_line_length = 125  # Characters per line for landscape
        
    def generate_citation(self, award_type: str, awardee_info: Dict, achievement_data: Dict) -> str:
        """
        Generate a compelling, narrative citation that maximizes character usage.
        
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
        
        # Prioritize achievements by impact and quantifiable results
        prioritized_achievements = self._prioritize_achievements(achievement_data)
        
        # Build the citation narrative
        narrative_parts = []
        
        # Opening with member identification
        opening = self._build_opening(award_type, rank, last_name, position, unit, time_period)
        narrative_parts.append(opening)
        
        # Build narrative body with action-impact-result structure
        body_sentences = self._build_enhanced_narrative_body(prioritized_achievements, rank, last_name, pronoun)
        narrative_parts.extend(body_sentences)
        
        # Add closing
        closing = self._build_closing(award_type, rank, last_name, pronoun)
        narrative_parts.append(closing)
        
        # Combine into full narrative
        full_citation = " ".join(narrative_parts)
        
        # Format based on character count instead of lines
        formatted_citation = self._format_by_characters(full_citation, award_type)
        
        return formatted_citation
    
    def _prioritize_achievements(self, achievement_data: Dict) -> Dict:
        """Prioritize achievements based on quantifiable impact and results."""
        # Create a scoring system for achievements
        scored_achievements = []
        
        achievements = achievement_data.get('achievements', [])
        impacts = achievement_data.get('impacts', [])
        quantifiable_metrics = achievement_data.get('quantifiable_metrics', [])
        
        # Create achievement-impact pairs
        for achievement in achievements:
            score = 0
            related_impacts = []
            
            # Check for quantifiable elements in the achievement itself
            if any(char.isdigit() for char in achievement):
                score += 3
            
            # Find related impacts
            achievement_lower = achievement.lower()
            for impact in impacts:
                impact_lower = impact.lower()
                # Check for related keywords
                matching_words = sum(1 for word in achievement_lower.split() 
                                   if len(word) > 4 and word in impact_lower)
                if matching_words > 0:
                    related_impacts.append(impact)
                    # Higher score for quantifiable impacts
                    if any(char in impact for char in ['$', '%']) or any(char.isdigit() for char in impact):
                        score += 5
                    else:
                        score += 2
            
            # Check quantifiable metrics
            for metric in quantifiable_metrics:
                metric_lower = metric.lower()
                if any(word in metric_lower for word in achievement_lower.split() if len(word) > 4):
                    related_impacts.append(metric)
                    score += 4
            
            # Additional scoring factors
            if any(word in achievement_lower for word in ['saved', 'rescued', 'prevented']):
                score += 4  # Life-saving actions
            if any(word in achievement_lower for word in ['led', 'managed', 'supervised', 'directed']):
                score += 2  # Leadership
            if any(word in achievement_lower for word in ['developed', 'created', 'designed', 'implemented']):
                score += 2  # Innovation
            
            scored_achievements.append({
                'achievement': achievement,
                'impacts': related_impacts,
                'score': score
            })
        
        # Sort by score (highest first)
        scored_achievements.sort(key=lambda x: x['score'], reverse=True)
        
        # Return enhanced achievement data
        achievement_data['prioritized_achievements'] = scored_achievements
        return achievement_data
        
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
        
    def _build_enhanced_narrative_body(self, achievement_data: Dict, rank: str, last_name: str, pronoun: str) -> List[str]:
        """Build narrative body with action-impact-result structure for each achievement."""
        sentences = []
        
        # Get prioritized achievements
        prioritized = achievement_data.get('prioritized_achievements', [])
        if not prioritized:
            # Fallback to original method if prioritization failed
            return self._build_narrative_body(achievement_data, rank, last_name, pronoun)
        
        # Extract other relevant data
        leadership = achievement_data.get('leadership_details', [])
        innovations = achievement_data.get('innovation_details', [])
        challenges = achievement_data.get('challenges', [])
        
        # Process top achievements with their impacts
        max_achievements = 4  # Focus on top 4 to ensure quality over quantity
        for i, item in enumerate(prioritized[:max_achievements]):
            achievement = item['achievement']
            impacts = item['impacts']
            
            # Build action-impact-result sentence
            if i == 0:  # First achievement gets special treatment
                sentence = self._build_primary_achievement_sentence(achievement, impacts, pronoun)
            else:
                # Use transitions for subsequent achievements
                transition = random.choice(self.TRANSITIONS['addition'])
                sentence = self._build_achievement_with_impact(achievement, impacts, pronoun, transition)
            
            if sentence:
                sentences.append(sentence)
        
        # Add challenge narrative if significant
        if challenges and len(sentences) < 6:
            challenge_sentence = self._build_challenge_sentence(challenges, rank, last_name, pronoun)
            if challenge_sentence:
                sentences.append(challenge_sentence)
        
        # Add overall impact summary
        all_impacts = []
        for item in prioritized:
            all_impacts.extend(item['impacts'])
        
        if all_impacts and len(sentences) < 8:
            impact_summary = self._build_comprehensive_impact_summary(all_impacts, pronoun)
            if impact_summary:
                sentences.append(impact_summary)
            
        return sentences
    
    def _build_primary_achievement_sentence(self, achievement: str, impacts: List[str], pronoun: str) -> str:
        """Build the primary achievement sentence with full action-impact-result structure."""
        achievement_text = self._clean_for_narrative(achievement)
        
        # Determine the type of achievement
        if any(word in achievement_text.lower() for word in ['led', 'managed', 'supervised', 'directed']):
            adj = random.choice(self.ADJECTIVES['leadership'])
            intro = f"Demonstrating {adj} leadership and vision"
        elif any(word in achievement_text.lower() for word in ['developed', 'created', 'designed']):
            adj = random.choice(self.ADJECTIVES['innovation'])
            intro = f"Through {adj} innovation"
        else:
            adj = random.choice(self.ADJECTIVES['skill'])
            intro = f"With {adj} expertise"
        
        # Build the sentence with impact
        if impacts:
            # Choose the most significant impact
            impact = self._select_best_impact(impacts)
            impact_text = self._clean_for_narrative(impact)
            
            # Create flowing sentence
            if 'resulted in' in impact_text or 'led to' in impact_text:
                return f"{intro}, {pronoun} {achievement_text}, which {impact_text}."
            else:
                return f"{intro}, {pronoun} {achievement_text}, directly resulting in {impact_text}."
        else:
            return f"{intro}, {pronoun} {achievement_text}."
    
    def _build_achievement_with_impact(self, achievement: str, impacts: List[str], pronoun: str, transition: str) -> str:
        """Build an achievement sentence that includes its impact and result."""
        achievement_text = self._clean_for_narrative(achievement)
        pronoun_possessive = 'Her' if pronoun == 'she' else 'His'
        
        if impacts:
            impact = self._select_best_impact(impacts)
            impact_text = self._clean_for_narrative(impact)
            
            # Vary the sentence structure
            structures = [
                f"{transition}, {pronoun} {achievement_text}, yielding {impact_text}.",
                f"{pronoun_possessive} efforts to {achievement_text} resulted in {impact_text}.",
                f"{transition}, through {achievement_text}, {pronoun} achieved {impact_text}."
            ]
            return random.choice(structures)
        else:
            return f"{transition}, {pronoun} {achievement_text}."
    
    def _select_best_impact(self, impacts: List[str]) -> str:
        """Select the most significant impact from a list."""
        # Prioritize quantifiable impacts
        for impact in impacts:
            if any(char in impact for char in ['$', '%']) or any(char.isdigit() for char in impact):
                return impact
        
        # Then look for key result words
        for impact in impacts:
            if any(word in impact.lower() for word in ['saved', 'increased', 'reduced', 'improved', 'enhanced']):
                return impact
        
        # Return first impact as fallback
        return impacts[0] if impacts else "significant operational improvements"
    
    def _build_comprehensive_impact_summary(self, impacts: List[str], pronoun: str) -> str:
        """Build a comprehensive summary of all impacts."""
        # Filter for unique, significant impacts
        unique_impacts = []
        seen = set()
        
        for impact in impacts:
            # Simple deduplication based on first few words
            key = ' '.join(impact.lower().split()[:3])
            if key not in seen:
                seen.add(key)
                unique_impacts.append(impact)
        
        # Select top 2-3 impacts
        top_impacts = []
        for impact in unique_impacts[:3]:
            if any(char in impact for char in ['$', '%']) or any(char.isdigit() for char in impact):
                top_impacts.append(self._clean_for_narrative(impact))
        
        if len(top_impacts) >= 2:
            pronoun_possessive = 'Her' if pronoun == 'she' else 'His'
            return f"{pronoun_possessive} comprehensive efforts culminated in {top_impacts[0]}, {top_impacts[1]}, and enhanced operational readiness throughout the command."
        elif top_impacts:
            return f"These initiatives directly resulted in {top_impacts[0]} and significantly enhanced mission effectiveness."
        else:
            return None
    
    def _format_by_characters(self, citation: str, award_type: str) -> str:
        """Format citation based on character count, breaking into 125-character lines."""
        max_chars = self.CHARACTER_LIMITS.get(award_type, 1140)
        chars_per_line = 125
        
        # First check if citation exceeds total character limit
        if len(citation) > max_chars:
            # Trim intelligently by sentences
            sentences = self._split_into_sentences(citation)
            
            if len(sentences) < 3:
                # If we can't split properly, truncate at word boundary
                words = citation[:max_chars].split()
                citation = ' '.join(words[:-1]) + '...'
            else:
                # Keep opening and closing, trim middle
                opening = sentences[0]
                closing = sentences[-1]
                body_sentences = sentences[1:-1]
                
                current_citation = opening
                for sentence in body_sentences:
                    test_citation = current_citation + " " + sentence
                    if len(test_citation + " " + closing) <= max_chars:
                        current_citation = test_citation
                    else:
                        break
                
                citation = current_citation + " " + closing
        
        # Now format into lines of 125 characters each
        lines = []
        words = citation.split()
        current_line = ""
        
        for word in words:
            # Check if adding this word would exceed line limit
            if current_line and len(current_line + " " + word) > chars_per_line:
                # Current line is full, save it and start new line
                lines.append(current_line)
                current_line = word
            else:
                # Add word to current line
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
        
        # Don't forget the last line
        if current_line:
            lines.append(current_line)
        
        # Join lines with newlines and return
        return '\n'.join(lines)
        
    def _build_narrative_body(self, achievement_data: Dict, rank: str, last_name: str, pronoun: str) -> List[str]:
        """Fallback to original narrative body builder."""
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
        
    def _clean_for_narrative(self, text: str) -> str:
        """Clean text for use in narrative."""
        # Remove leading/trailing whitespace and periods
        text = text.strip().rstrip('.')
        
        # Remove JSON artifacts like brackets, quotes, etc.
        text = text.replace('[', '').replace(']', '')
        text = text.replace('"', '').replace("'", '')
        text = text.replace('{', '').replace('}', '')
        
        # Clean up any double spaces
        text = ' '.join(text.split())
        
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