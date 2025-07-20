"""
Rank-based calibration for Coast Guard award scoring.
Adjusts expectations based on member's rank and position.
"""

import logging
import re
from typing import Dict, Tuple, Optional

logger = logging.getLogger(__name__)

# Coast Guard rank hierarchy with normalized values (0-1)
RANK_HIERARCHY = {
    # Enlisted (E-1 to E-9)
    "SR": 0.05,    # Seaman Recruit (E-1)
    "SA": 0.10,    # Seaman Apprentice (E-2)
    "SN": 0.15,    # Seaman (E-3)
    "FN": 0.15,    # Fireman (E-3)
    "PO3": 0.20,   # Petty Officer Third Class (E-4)
    "PO2": 0.30,   # Petty Officer Second Class (E-5)
    "PO1": 0.40,   # Petty Officer First Class (E-6)
    "CPO": 0.55,   # Chief Petty Officer (E-7)
    "SCPO": 0.70,  # Senior Chief Petty Officer (E-8)
    "MCPO": 0.85,  # Master Chief Petty Officer (E-9)
    
    # Warrant Officers (W-2 to W-4)
    "CWO2": 0.45,  # Chief Warrant Officer 2
    "CWO3": 0.55,  # Chief Warrant Officer 3
    "CWO4": 0.65,  # Chief Warrant Officer 4
    
    # Officers (O-1 to O-10)
    "ENS": 0.25,   # Ensign (O-1)
    "LTJG": 0.35,  # Lieutenant Junior Grade (O-2)
    "LT": 0.45,    # Lieutenant (O-3)
    "LCDR": 0.55,  # Lieutenant Commander (O-4)
    "CDR": 0.70,   # Commander (O-5)
    "CAPT": 0.85,  # Captain (O-6)
    "RDML": 0.90,  # Rear Admiral Lower Half (O-7)
    "RADM": 0.95,  # Rear Admiral (O-8)
    "VADM": 0.97,  # Vice Admiral (O-9)
    "ADM": 1.00,   # Admiral (O-10)
}

# Expected leadership scope by rank
EXPECTED_LEADERSHIP = {
    "SR": (0, 0),      # No leadership expected
    "SA": (0, 0),      # No leadership expected
    "SN": (0, 1),      # May assist with 1 person
    "FN": (0, 1),      # May assist with 1 person
    "PO3": (1, 3),     # Lead 1-3 people
    "PO2": (3, 8),     # Lead 3-8 people
    "PO1": (5, 15),    # Lead 5-15 people
    "CPO": (10, 30),   # Lead 10-30 people
    "SCPO": (20, 50),  # Lead 20-50 people
    "MCPO": (30, 100), # Lead 30-100 people
    "CWO2": (5, 20),   # Technical leadership
    "CWO3": (10, 30),  # Technical leadership
    "CWO4": (15, 40),  # Technical leadership
    "ENS": (5, 15),    # Division officer
    "LTJG": (10, 25),  # Division officer
    "LT": (15, 40),    # Department head
    "LCDR": (30, 80),  # Department head/XO
    "CDR": (50, 200),  # CO of cutter/unit
    "CAPT": (100, 500),# CO of major unit/sector
    "RDML": (500, 2000), # District/Area leadership
    "RADM": (1000, 5000), # Major command
    "VADM": (5000, 15000), # Vice Commandant level
    "ADM": (10000, 40000),  # Commandant
}

# Expected scope of impact by rank
EXPECTED_SCOPE = {
    "SR": "individual",
    "SA": "individual",
    "SN": "team",
    "FN": "team",
    "PO3": "division",
    "PO2": "department",
    "PO1": "department",
    "CPO": "unit",
    "SCPO": "unit",
    "MCPO": "unit/sector",
    "CWO2": "unit",
    "CWO3": "unit/sector",
    "CWO4": "sector",
    "ENS": "unit",
    "LTJG": "unit",
    "LT": "unit/sector",
    "LCDR": "sector",
    "CDR": "sector/district",
    "CAPT": "district/area",
    "RDML": "area/coast guard",
    "RADM": "coast guard",
    "VADM": "coast guard/national",
    "ADM": "national/international",
}

# Expected quantifiable impact by rank (as multiplier)
EXPECTED_IMPACT_MULTIPLIER = {
    "SR": 0.5,    # Small individual contributions
    "SA": 0.6,
    "SN": 0.7,
    "FN": 0.7,
    "PO3": 1.0,   # Baseline
    "PO2": 1.5,
    "PO1": 2.0,
    "CPO": 3.0,
    "SCPO": 4.0,
    "MCPO": 5.0,
    "CWO2": 2.5,
    "CWO3": 3.5,
    "CWO4": 4.5,
    "ENS": 2.0,
    "LTJG": 2.5,
    "LT": 3.5,
    "LCDR": 5.0,
    "CDR": 8.0,
    "CAPT": 12.0,
    "RDML": 20.0,
    "RADM": 30.0,
    "VADM": 40.0,
    "ADM": 50.0,
}


class RankCalibrator:
    """Calibrates award scores based on member's rank and expected performance."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def normalize_rank(self, rank_str: str) -> str:
        """Normalize rank string to standard abbreviation."""
        if not rank_str:
            return "PO3"  # Default to E-4 if unknown
        
        rank_upper = rank_str.upper().strip()
        
        # Direct match
        if rank_upper in RANK_HIERARCHY:
            return rank_upper
        
        # Common variations
        rank_mappings = {
            "E-1": "SR", "E1": "SR", "SEAMAN RECRUIT": "SR",
            "E-2": "SA", "E2": "SA", "SEAMAN APPRENTICE": "SA",
            "E-3": "SN", "E3": "SN", "SEAMAN": "SN", "FIREMAN": "FN",
            "E-4": "PO3", "E4": "PO3", "PETTY OFFICER THIRD CLASS": "PO3", "PO 3": "PO3",
            "E-5": "PO2", "E5": "PO2", "PETTY OFFICER SECOND CLASS": "PO2", "PO 2": "PO2",
            "E-6": "PO1", "E6": "PO1", "PETTY OFFICER FIRST CLASS": "PO1", "PO 1": "PO1",
            "E-7": "CPO", "E7": "CPO", "CHIEF PETTY OFFICER": "CPO", "CHIEF": "CPO",
            "E-8": "SCPO", "E8": "SCPO", "SENIOR CHIEF PETTY OFFICER": "SCPO", "SENIOR CHIEF": "SCPO",
            "E-9": "MCPO", "E9": "MCPO", "MASTER CHIEF PETTY OFFICER": "MCPO", "MASTER CHIEF": "MCPO",
            "W-2": "CWO2", "W2": "CWO2", "CHIEF WARRANT OFFICER 2": "CWO2", "CWO 2": "CWO2",
            "W-3": "CWO3", "W3": "CWO3", "CHIEF WARRANT OFFICER 3": "CWO3", "CWO 3": "CWO3",
            "W-4": "CWO4", "W4": "CWO4", "CHIEF WARRANT OFFICER 4": "CWO4", "CWO 4": "CWO4",
            "O-1": "ENS", "O1": "ENS", "ENSIGN": "ENS",
            "O-2": "LTJG", "O2": "LTJG", "LIEUTENANT JUNIOR GRADE": "LTJG", "LIEUTENANT JG": "LTJG",
            "O-3": "LT", "O3": "LT", "LIEUTENANT": "LT",
            "O-4": "LCDR", "O4": "LCDR", "LIEUTENANT COMMANDER": "LCDR",
            "O-5": "CDR", "O5": "CDR", "COMMANDER": "CDR",
            "O-6": "CAPT", "O6": "CAPT", "CAPTAIN": "CAPT",
            "O-7": "RDML", "O7": "RDML", "REAR ADMIRAL LOWER HALF": "RDML",
            "O-8": "RADM", "O8": "RADM", "REAR ADMIRAL": "RADM",
            "O-9": "VADM", "O9": "VADM", "VICE ADMIRAL": "VADM",
            "O-10": "ADM", "O10": "ADM", "ADMIRAL": "ADM",
        }
        
        for pattern, normalized in rank_mappings.items():
            if pattern in rank_upper:
                return normalized
        
        # Try to extract rank pattern
        if re.search(r'\bPO\s*3\b', rank_upper):
            return "PO3"
        elif re.search(r'\bPO\s*2\b', rank_upper):
            return "PO2"
        elif re.search(r'\bPO\s*1\b', rank_upper):
            return "PO1"
        
        logger.warning(f"Could not normalize rank '{rank_str}', defaulting to PO3")
        return "PO3"
    
    def calibrate_scores(self, scores: Dict[str, float], rank: str, 
                        achievement_data: Dict) -> Tuple[Dict[str, float], Dict[str, str]]:
        """
        Calibrate scores based on rank expectations.
        
        Returns:
            Tuple of (calibrated_scores, calibration_notes)
        """
        normalized_rank = self.normalize_rank(rank)
        rank_value = RANK_HIERARCHY.get(normalized_rank, 0.2)
        
        calibrated_scores = scores.copy()
        calibration_notes = {}
        
        # Calibrate leadership score
        calibrated_scores["leadership"], leadership_note = self._calibrate_leadership(
            scores.get("leadership", 0), normalized_rank, achievement_data
        )
        if leadership_note:
            calibration_notes["leadership"] = leadership_note
        
        # Calibrate scope score
        calibrated_scores["scope"], scope_note = self._calibrate_scope(
            scores.get("scope", 0), normalized_rank, achievement_data
        )
        if scope_note:
            calibration_notes["scope"] = scope_note
        
        # Calibrate quantifiable results
        calibrated_scores["quantifiable_results"], quant_note = self._calibrate_quantifiable(
            scores.get("quantifiable_results", 0), normalized_rank, achievement_data
        )
        if quant_note:
            calibration_notes["quantifiable_results"] = quant_note
        
        # Calibrate impact score
        calibrated_scores["impact"], impact_note = self._calibrate_impact(
            scores.get("impact", 0), normalized_rank, achievement_data
        )
        if impact_note:
            calibration_notes["impact"] = impact_note
        
        # Calibrate valor (context-sensitive)
        calibrated_scores["valor"], valor_note = self._calibrate_valor(
            scores.get("valor", 0), normalized_rank, achievement_data
        )
        if valor_note:
            calibration_notes["valor"] = valor_note
        
        # Recalculate total
        calibrated_scores["total_weighted"] = self._recalculate_total(calibrated_scores)
        
        return calibrated_scores, calibration_notes
    
    def _calibrate_leadership(self, score: float, rank: str, achievement_data: Dict) -> Tuple[float, str]:
        """Calibrate leadership score based on rank expectations."""
        expected_min, expected_max = EXPECTED_LEADERSHIP.get(rank, (1, 10))
        
        # Extract actual leadership numbers
        combined_text = self._build_combined_text(achievement_data)
        personnel_numbers = re.findall(r'(\d+)\s*(?:people|personnel|staff|members|team|subordinates)', combined_text)
        
        actual_led = 0
        if personnel_numbers:
            actual_led = max([int(num) for num in personnel_numbers])
        
        # Calculate calibration factor
        if expected_max == 0:
            # No leadership expected at this rank
            if actual_led > 0:
                # Exceeding expectations significantly
                calibration_factor = 1.5
                note = f"Led {actual_led} (exceptional for {rank})"
            else:
                calibration_factor = 0.5
                note = f"No leadership expected at {rank} level"
        else:
            # Compare to expectations
            if actual_led >= expected_max * 1.5:
                calibration_factor = 1.3
                note = f"Led {actual_led} (exceeds {rank} norm of {expected_min}-{expected_max})"
            elif actual_led >= expected_max:
                calibration_factor = 1.0
                note = ""
            elif actual_led >= expected_min:
                calibration_factor = 0.8
                note = f"Led {actual_led} (meets {rank} expectations)"
            else:
                calibration_factor = 0.6
                note = f"Led {actual_led} (below {rank} norm of {expected_min}-{expected_max})"
        
        calibrated_score = min(5.0, score * calibration_factor)
        return calibrated_score, note
    
    def _calibrate_scope(self, score: float, rank: str, achievement_data: Dict) -> Tuple[float, str]:
        """Calibrate scope score based on rank expectations."""
        expected_scope = EXPECTED_SCOPE.get(rank, "unit")
        actual_scope = achievement_data.get("scope", "").lower()
        
        # Define scope hierarchy
        scope_hierarchy = {
            "individual": 1,
            "team": 2,
            "division": 3,
            "department": 4,
            "unit": 5,
            "station": 5,
            "sector": 6,
            "district": 7,
            "area": 8,
            "coast guard": 9,
            "national": 10,
            "international": 11
        }
        
        expected_level = max(scope_hierarchy.get(word, 0) for word in expected_scope.split('/'))
        actual_level = max(scope_hierarchy.get(word, 0) for word in actual_scope.split() 
                          if word in scope_hierarchy)
        
        if actual_level == 0:
            actual_level = 1  # Default to individual
        
        # Calculate calibration
        level_diff = actual_level - expected_level
        
        if level_diff >= 3:
            calibration_factor = 1.4
            note = f"Far exceeds {rank} scope expectations"
        elif level_diff >= 2:
            calibration_factor = 1.2
            note = f"Exceeds {rank} scope expectations"
        elif level_diff >= 0:
            calibration_factor = 1.0
            note = ""
        elif level_diff >= -1:
            calibration_factor = 0.8
            note = f"Slightly below {rank} scope expectations"
        else:
            calibration_factor = 0.6
            note = f"Below expected scope for {rank}"
        
        calibrated_score = min(5.0, score * calibration_factor)
        return calibrated_score, note
    
    def _calibrate_quantifiable(self, score: float, rank: str, achievement_data: Dict) -> Tuple[float, str]:
        """Calibrate quantifiable results based on rank expectations."""
        multiplier = EXPECTED_IMPACT_MULTIPLIER.get(rank, 1.0)
        
        # Junior ranks get bonus for ANY quantifiable results
        if multiplier < 1.0 and score > 0:
            calibration_factor = 1.2
            note = f"Quantifiable results impressive for {rank}"
        # Senior ranks need MORE impressive numbers
        elif multiplier > 5.0:
            if score >= 4.0:
                calibration_factor = 1.0
                note = ""
            else:
                calibration_factor = 0.7
                note = f"Higher quantifiable impact expected at {rank} level"
        else:
            calibration_factor = 1.0
            note = ""
        
        calibrated_score = min(5.0, score * calibration_factor)
        return calibrated_score, note
    
    def _calibrate_impact(self, score: float, rank: str, achievement_data: Dict) -> Tuple[float, str]:
        """Calibrate impact score based on rank and scope."""
        # Similar to quantifiable results but focused on overall impact
        multiplier = EXPECTED_IMPACT_MULTIPLIER.get(rank, 1.0)
        
        if multiplier > 8.0:  # O-5 and above
            if score < 3.0:
                calibration_factor = 0.6
                note = f"Greater organizational impact expected at {rank} level"
            else:
                calibration_factor = 1.0
                note = ""
        elif multiplier < 1.0:  # Junior enlisted
            if score >= 2.0:
                calibration_factor = 1.3
                note = f"Significant impact for {rank}"
            else:
                calibration_factor = 1.0
                note = ""
        else:
            calibration_factor = 1.0
            note = ""
        
        calibrated_score = min(5.0, score * calibration_factor)
        return calibrated_score, note
    
    def _calibrate_valor(self, score: float, rank: str, achievement_data: Dict) -> Tuple[float, str]:
        """Calibrate valor score - less rank-dependent but context matters."""
        # Valor is valor regardless of rank, but context matters
        valor_items = achievement_data.get('valor_indicators', [])
        
        if not valor_items and score > 0:
            # Reduce score if no concrete valor indicators
            calibration_factor = 0.5
            note = "Valor score reduced - no specific indicators found"
        elif len(valor_items) >= 2:
            # Multiple valor actions deserve recognition at any rank
            calibration_factor = 1.0
            note = ""
        else:
            calibration_factor = 1.0
            note = ""
        
        calibrated_score = min(5.0, score * calibration_factor)
        return calibrated_score, note
    
    def _build_combined_text(self, achievement_data: Dict) -> str:
        """Build combined text from achievement data."""
        text_parts = []
        for field in ["achievements", "impacts", "leadership_details"]:
            items = achievement_data.get(field, [])
            if isinstance(items, list):
                text_parts.extend(str(item) for item in items)
        return " ".join(text_parts)
    
    def _recalculate_total(self, scores: Dict[str, float]) -> float:
        """Recalculate weighted total after calibration."""
        from .criteria import SCORING_WEIGHTS
        
        total_weighted = 0.0
        weight_sum = 0.0
        
        for criterion, score in scores.items():
            if criterion == "total_weighted":
                continue
            
            weight = SCORING_WEIGHTS.get(criterion, 1)
            if score == 0:
                continue
            
            total_weighted += score * weight
            weight_sum += weight
        
        percent = (total_weighted / (weight_sum * 5) * 100) if weight_sum else 0
        return round(percent, 1)