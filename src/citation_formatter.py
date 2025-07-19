"""
Coast Guard Award Citation Formatter
Ensures compliance with official CG award formatting requirements.
"""

import re
from typing import Dict, List, Optional, Tuple


class CitationFormatter:
    """Formats award citations according to Coast Guard standards."""
    
    # Standard opening phrases for each award type (based on official examples)
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
    
    # Standard closing phrases for each award type (based on official examples)
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
    
    # Line limits for each award type
    LINE_LIMITS = {
        "Distinguished Service Medal": 16,
        "Legion of Merit": 16,
        "Meritorious Service Medal": 12,
        "Coast Guard Commendation Medal": 12,
        "Coast Guard Achievement Medal": 12,
        "Coast Guard Letter of Commendation": 12
    }
    
    def __init__(self):
        self.max_line_length = 95  # Characters per line for landscape orientation
        
    def format_citation(self, award_type: str, awardee_info: Dict, achievement_data: Dict) -> str:
        """
        Format a complete citation according to CG standards.
        
        Args:
            award_type: Type of award (e.g., "Coast Guard Achievement Medal")
            awardee_info: Dict with name, rank, unit, position, etc.
            achievement_data: Dict with achievements, impacts, time_period, etc.
            
        Returns:
            Formatted citation text
        """
        # Extract key information
        name = awardee_info.get('name', 'Member')
        rank = awardee_info.get('rank', '')
        unit = awardee_info.get('unit', '')
        position = awardee_info.get('position', '')
        
        # Get last name for citation use
        last_name = name.split()[-1] if name else 'Member'
        
        # Determine pronoun
        pronoun = self._determine_pronoun(name)
        
        # Get time period
        time_period = achievement_data.get('time_period', '')
        if not time_period or time_period == "Not specified":
            time_period = "[dates of service]"
            
        # Build citation as single paragraph
        # Start with member name and opening phrase
        opening_template = self.OPENING_PHRASES.get(award_type, "is cited for outstanding achievement")
        
        if rank:
            # Capitalize rank properly
            rank_parts = rank.split()
            cap_rank_parts = []
            for part in rank_parts:
                if part.lower() in ['first', 'second', 'third', 'class']:
                    cap_rank_parts.append(part.capitalize())
                else:
                    cap_rank_parts.append(part.title())
            formatted_rank = ' '.join(cap_rank_parts)
            citation_parts = [f"{formatted_rank} {last_name.upper()}"]
        else:
            citation_parts = [f"Petty Officer {last_name.upper()}"]
            
        citation_parts.append(opening_template)
        
        # Add duty assignment
        if position and unit:
            citation_parts.append(f"while serving as {position}, {unit},")
        elif unit:
            citation_parts.append(f"while serving at {unit},")
        elif position:
            citation_parts.append(f"while serving as {position},")
            
        # Add time period
        citation_parts.append(f"from {time_period}.")
        
        # Add achievement narrative
        narrative = self._build_achievement_narrative(achievement_data, pronoun)
        citation_parts.append(narrative)
        
        # Add closing
        closing_template = self.CLOSING_PHRASES.get(award_type, 
            "{name}'s dedication and devotion to duty are most heartily commended and are in keeping with the highest traditions of the United States Coast Guard.")
        
        # Format closing with proper name reference
        if rank:
            # Capitalize rank properly
            rank_parts = rank.split()
            cap_rank_parts = []
            for part in rank_parts:
                if part.lower() in ['first', 'second', 'third', 'class']:
                    cap_rank_parts.append(part.capitalize())
                else:
                    cap_rank_parts.append(part.title())
            formatted_rank = ' '.join(cap_rank_parts)
            name_ref = f"{formatted_rank} {last_name.upper()}"
        else:
            name_ref = f"Petty Officer {last_name.upper()}"
            
        closing = closing_template.format(name=name_ref, pronoun=pronoun)
        citation_parts.append(closing)
        
        # Join all parts into single paragraph
        full_citation = " ".join(citation_parts)
        
        # Apply line formatting for landscape orientation
        formatted_citation = self._apply_line_formatting(full_citation, award_type)
        
        return formatted_citation
    
    def _build_achievement_narrative(self, achievement_data: Dict, pronoun: str) -> str:
        """Build the achievement narrative in Coast Guard style."""
        # Get achievements and impacts
        achievements = achievement_data.get('achievements', [])
        impacts = achievement_data.get('impacts', [])
        leadership = achievement_data.get('leadership_details', [])
        innovations = achievement_data.get('innovation_details', [])
        challenges = achievement_data.get('challenges', [])
        
        # Build narrative components
        narrative_parts = []
        
        # Focus on demonstrating exceptional performance
        if leadership and any('led' in l.lower() or 'supervised' in l.lower() for l in leadership):
            # Leadership-focused opening
            leadership_item = next(l for l in leadership if 'led' in l.lower() or 'supervised' in l.lower())
            narrative_parts.append(f"Demonstrating exceptional leadership, {pronoun} {self._clean_achievement(leadership_item)}.")
            
        # Add key achievements with impact
        key_achievements = []
        
        # Prioritize quantifiable achievements
        for achievement in achievements[:3]:
            if any(char.isdigit() for char in achievement):
                key_achievements.append(self._clean_achievement(achievement))
        
        # Add other significant achievements
        for achievement in achievements:
            if achievement not in key_achievements and len(key_achievements) < 3:
                key_achievements.append(self._clean_achievement(achievement))
                
        # Format achievements into flowing narrative
        if key_achievements:
            if len(key_achievements) == 1:
                narrative_parts.append(f"His efforts {key_achievements[0]}.")
            elif len(key_achievements) == 2:
                narrative_parts.append(f"His exceptional performance {key_achievements[0]} and {key_achievements[1]}.")
            else:
                # Multiple achievements
                narrative_parts.append(f"Through tireless dedication, {pronoun} {key_achievements[0]}, {key_achievements[1]}, and {key_achievements[2]}.")
        
        # Add significant impacts
        significant_impacts = []
        for impact in impacts[:2]:
            if '$' in impact or '%' in impact or any(word in impact.lower() for word in ['saved', 'increased', 'reduced', 'improved']):
                significant_impacts.append(self._clean_achievement(impact))
                
        if significant_impacts:
            impact_text = " and ".join(significant_impacts)
            narrative_parts.append(f"These efforts directly resulted in {impact_text}.")
            
        # Add innovation if present
        if innovations:
            innovation = self._clean_achievement(innovations[0])
            narrative_parts.append(f"His innovative approach {innovation}.")
            
        # Join narrative parts
        return " ".join(narrative_parts)
    
    def _clean_achievement(self, text: str) -> str:
        """Clean an achievement text for use in citation."""
        # Remove leading/trailing whitespace and periods
        text = text.strip().rstrip('.')
        
        # Keep the text mostly as-is, just ensure no double periods
        return text
    
    def _format_closing(self, award_type: str, full_name: str, pronoun: str) -> str:
        """Format the closing phrase of the citation."""
        closing_template = self.CLOSING_PHRASES.get(
            award_type, 
            "{name}'s dedication and devotion to duty reflect credit upon {pronoun} and the United States Coast Guard."
        )
        
        # Replace placeholders
        closing = closing_template.format(name=full_name, pronoun=pronoun)
        
        return closing
    
    def _apply_line_formatting(self, citation: str, award_type: str) -> str:
        """Apply line limits and formatting constraints."""
        max_lines = self.LINE_LIMITS.get(award_type, 12)
        
        # Clean up the citation text
        citation = self._clean_text(citation)
        
        # Split into words
        words = citation.split()
        
        # Build lines with word wrapping
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_length = len(word)
            
            # Check if adding this word would exceed line length
            if current_length + word_length + len(current_line) > self.max_line_length:
                # Save current line and start new one
                if current_line:
                    lines.append(" ".join(current_line))
                    current_line = [word]
                    current_length = word_length
            else:
                current_line.append(word)
                current_length += word_length
                
        # Add final line
        if current_line:
            lines.append(" ".join(current_line))
        
        # Check line limit
        if len(lines) > max_lines:
            # Need to condense - remove less critical details
            lines = self._condense_citation(lines, max_lines)
            
        return "\n".join(lines)
    
    def _condense_citation(self, lines: List[str], max_lines: int) -> List[str]:
        """Condense citation to fit within line limits."""
        # Rejoin to text
        text = " ".join(lines)
        
        # Remove less critical phrases
        condensing_patterns = [
            (r'\s+Additionally,.*?\.', '.'),  # Remove additional clauses
            (r'\s+Furthermore,.*?\.', '.'),   # Remove furthermore clauses
            (r'\s+Moreover,.*?\.', '.'),      # Remove moreover clauses
            (r',\s+which\s+.*?,', ','),       # Remove which clauses
            (r'\s+\([^)]+\)', ''),             # Remove parenthetical info
        ]
        
        for pattern, replacement in condensing_patterns:
            text = re.sub(pattern, replacement, text)
            
        # Re-split into lines
        words = text.split()
        new_lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_length = len(word)
            
            if current_length + word_length + len(current_line) > self.max_line_length:
                if current_line:
                    new_lines.append(" ".join(current_line))
                    current_line = [word]
                    current_length = word_length
            else:
                current_line.append(word)
                current_length += word_length
                
        if current_line:
            new_lines.append(" ".join(current_line))
            
        # If still too long, truncate
        if len(new_lines) > max_lines:
            new_lines = new_lines[:max_lines-1]
            # Ensure closing phrase is included
            closing_words = text.split()[-15:]  # Last ~15 words should be closing
            new_lines.append(" ".join(closing_words))
            
        return new_lines
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove markdown formatting
        text = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', text)
        text = re.sub(r'_{1,2}([^_]+)_{1,2}', r'\1', text)
        
        # Ensure proper sentence capitalization while preserving names in CAPS
        sentences = []
        for s in text.split('.'):
            s = s.strip()
            if s:
                # Preserve uppercase names
                words = s.split()
                cap_words = []
                for i, word in enumerate(words):
                    if word.isupper() and len(word) > 1:  # Preserve names in caps
                        cap_words.append(word)
                    elif i == 0:  # Capitalize first word
                        cap_words.append(word.capitalize())
                    else:
                        cap_words.append(word.lower())
                sentences.append(' '.join(cap_words))
        text = '. '.join(sentences) + '.' if sentences else ''
        
        # Fix common issues
        text = text.replace('..', '.')
        text = text.replace('  ', ' ')
        
        return text.strip()
    
    def _determine_pronoun(self, name: str) -> str:
        """Determine appropriate pronoun (simplified - in production would need better logic)."""
        # This is a simplified version - in production, you'd want proper pronoun handling
        # For now, using "he" as default based on examples, but should be configurable
        return "he"
    
    def _get_reflexive_pronoun(self, name: str) -> str:
        """Get reflexive pronoun form."""
        # Simplified - in production would need proper logic
        return "himself"
    
    def validate_citation(self, citation: str, award_type: str) -> Tuple[bool, List[str]]:
        """
        Validate citation meets CG requirements.
        
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        lines = citation.split('\n')
        
        # Check line count
        max_lines = self.LINE_LIMITS.get(award_type, 12)
        if len(lines) > max_lines:
            issues.append(f"Citation has {len(lines)} lines, exceeds limit of {max_lines}")
            
        # Check line length
        for i, line in enumerate(lines):
            if len(line) > self.max_line_length:
                issues.append(f"Line {i+1} exceeds {self.max_line_length} characters")
                
        # Check for required opening phrase (just check for "is cited for" pattern)
        if "is cited for" not in citation.lower()[:100]:
            issues.append("Missing standard opening phrase")
            
        # Check for closing phrase (case-insensitive)
        citation_lower = citation.lower()
        has_closing = any(phrase.lower() in citation_lower for phrase in [
            "traditions of the United States Coast Guard",
            "credit upon", "devotion to duty"
        ])
        if not has_closing:
            issues.append("Missing standard closing phrase")
            
        # Check for prohibited elements
        if re.search(r'\b(I|me|my)\b', citation):
            issues.append("Contains first person pronouns")
            
        if re.search(r'\b\w+\.\w+', citation):  # Acronyms
            issues.append("Contains acronyms (not authorized)")
            
        return len(issues) == 0, issues