"""
Coast Guard Award Citation Formatter
Ensures compliance with official CG award formatting requirements.
"""

import re
from typing import Dict, List, Optional, Tuple


class CitationFormatter:
    """Formats award citations according to Coast Guard standards."""
    
    # Standard opening phrases for each award type
    OPENING_PHRASES = {
        "Distinguished Service Medal": "For exceptionally meritorious service to the Government of the United States in a duty of great responsibility",
        "Legion of Merit": "For exceptionally meritorious conduct in the performance of outstanding services",
        "Meritorious Service Medal": "For outstanding meritorious service",
        "Coast Guard Commendation Medal": "For superior performance of duty",
        "Coast Guard Achievement Medal": "For professional achievement",
        "Coast Guard Letter of Commendation": "For outstanding performance of duty"
    }
    
    # Standard closing phrases for each award type
    CLOSING_PHRASES = {
        "Distinguished Service Medal": "{name}'s distinctive accomplishments, unrelenting perseverance, and steadfast devotion to duty reflect great credit upon {pronoun} and are in keeping with the highest traditions of the United States Coast Guard.",
        "Legion of Merit": "{name}'s initiative, perseverance, and devotion to duty reflect great credit upon {pronoun} and are in keeping with the highest traditions of the United States Coast Guard.",
        "Meritorious Service Medal": "{name}'s dedication, judgment, and devotion to duty are most heartily commended and are in keeping with the highest traditions of the United States Coast Guard.",
        "Coast Guard Commendation Medal": "{name}'s dedication, professional knowledge, and devotion to duty are most heartily commended and are in keeping with the highest traditions of the United States Coast Guard.",
        "Coast Guard Achievement Medal": "{name}'s dedication, perseverance, and devotion to duty are most heartily commended and are in keeping with the highest traditions of the United States Coast Guard.",
        "Coast Guard Letter of Commendation": "{name}'s initiative, perseverance, and devotion to duty reflect credit upon {pronoun} and the United States Coast Guard."
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
        
        # Format name with rank
        if rank:
            full_name = f"{rank} {name}".upper()
        else:
            full_name = name.upper()
            
        # Determine pronoun
        pronoun = self._determine_pronoun(name)
        
        # Get time period
        time_period = achievement_data.get('time_period', '')
        if not time_period or time_period == "Not specified":
            time_period = "[dates of service]"
            
        # Build citation components
        opening = self._format_opening(award_type, position, unit, time_period)
        body = self._format_body(full_name, achievement_data)
        closing = self._format_closing(award_type, full_name, pronoun)
        
        # Combine and format to line limits
        full_citation = f"{opening} {body} {closing}"
        
        # Apply line limits and formatting
        formatted_citation = self._apply_line_formatting(full_citation, award_type)
        
        return formatted_citation
    
    def _format_opening(self, award_type: str, position: str, unit: str, time_period: str) -> str:
        """Format the opening phrase of the citation."""
        opening = self.OPENING_PHRASES.get(award_type, "For outstanding performance of duty")
        
        # Add duty assignment if available
        if position and unit:
            opening += f" while serving as {position}, {unit},"
        elif unit:
            opening += f" while serving at {unit},"
        elif position:
            opening += f" while serving as {position},"
            
        # Add time period
        opening += f" from {time_period}."
        
        return opening
    
    def _format_body(self, full_name: str, achievement_data: Dict) -> str:
        """Format the body of the citation with achievements."""
        body_parts = []
        
        # Start with member name
        body_parts.append(f"{full_name} distinguished {self._get_reflexive_pronoun(full_name)} by")
        
        # Get key achievements and impacts
        achievements = achievement_data.get('achievements', [])
        impacts = achievement_data.get('impacts', [])
        leadership = achievement_data.get('leadership_details', [])
        
        # Combine and prioritize content
        key_accomplishments = []
        
        # Add most significant achievements
        for achievement in achievements[:3]:
            key_accomplishments.append(self._clean_text(achievement))
            
        # Add quantifiable impacts
        for impact in impacts[:2]:
            if any(char.isdigit() for char in impact):  # Prioritize quantifiable impacts
                key_accomplishments.append(self._clean_text(impact))
                
        # Add leadership if significant
        for lead in leadership[:1]:
            if 'led' in lead.lower() or 'supervised' in lead.lower():
                key_accomplishments.append(self._clean_text(lead))
        
        # Format accomplishments into narrative
        if key_accomplishments:
            # Clean up accomplishments - remove trailing periods
            cleaned_accomplishments = []
            for acc in key_accomplishments:
                acc = acc.rstrip('.')
                cleaned_accomplishments.append(acc)
            
            # Use conjunctions to create flowing narrative
            if len(cleaned_accomplishments) == 1:
                body_parts.append(cleaned_accomplishments[0])
            elif len(cleaned_accomplishments) == 2:
                body_parts.append(f"{cleaned_accomplishments[0]} and {cleaned_accomplishments[1]}")
            else:
                # Join with commas and 'and' for the last item
                accomplishment_text = ", ".join(cleaned_accomplishments[:-1])
                accomplishment_text += f", and {cleaned_accomplishments[-1]}"
                body_parts.append(accomplishment_text)
        
        return " ".join(body_parts)
    
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
        return "himself or herself"
    
    def _get_reflexive_pronoun(self, name: str) -> str:
        """Get reflexive pronoun form."""
        # Simplified - in production would need proper logic
        return "himself or herself"
    
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
                
        # Check for required opening phrase
        opening_phrase = self.OPENING_PHRASES.get(award_type, "")
        if opening_phrase and not citation.lower().startswith(opening_phrase[:20].lower()):
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