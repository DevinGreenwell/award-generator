"""
Award criteria definitions for Coast Guard awards.
"""

# Weight definitions for different scoring criteria - Adjusted for stricter evaluation
SCORING_WEIGHTS = {
    "impact": 6,              # Increased - concrete impact is critical
    "scope": 6,              # Increased - organizational reach matters more
    "leadership": 6,         # Increased - leadership is essential for higher awards
    "quantifiable_results": 5,  # Increased - must have measurable outcomes
    "above_beyond": 4,
    "innovation": 3,         # Decreased - innovation alone isn't enough
    "challenges": 3,
    "valor": 5,
    "collaboration": 3,      # Decreased - collaboration is good but not primary
    "training_provided": 2,  # Decreased - training is expected duty
    "emergency_response": 4
}

# Award thresholds (percentages) - More stringent thresholds
AWARD_THRESHOLDS = {
    "Medal of Honor": 98,              # +3 (extremely rare)
    "Distinguished Service Medal": 92, # +7 (very rare, O-6+ typically)
    "Legion of Merit": 85,            # +10 (rare, senior officers/enlisted)
    "Meritorious Service Medal": 75,  # +10 (significant achievement required)
    "Coast Guard Commendation Medal": 65, # +10 (clear above-and-beyond performance)
    "Coast Guard Achievement Medal": 50,   # +5 (solid performance above expectations)
    "Coast Guard Letter of Commendation": 35  # +5 (good performance)
}

# Detailed award criteria
AWARD_CRITERIA = {
    "Medal of Honor": {
        "description": "May be awarded to any person who distinguishes themselves by gallantry and intrepidity at the risk of their life above and beyond the call of duty.",
        "threshold": 96,
        "min_requirements": {
            "valor": 5,
            "risk_to_life": 5,
            "gallantry": 5,
            "leadership": 4,
        }
    },
    "Distinguished Service Medal": {
        "description": "May be awarded to any person who distinguishes themselves by exceptionally meritorious service to the United States Government in a duty of great responsibility.",
        "threshold": 92,
        "min_requirements": {
            "leadership": 4.5,      # Increased from 4.0
            "impact": 4.5,          # Increased from 4.0
            "scope": 4.5,           # Increased from 4.0
            "quantifiable_results": 4.0  # Increased from 3.5
        }
    },
    "Legion of Merit": {
        "description": "Awarded to officers who have performed exceptionally meritorious service, except as to the degree of responsibility of the DSM.",
        "threshold": 85,
        "min_requirements": {
            "leadership": 4.0,      # Increased from 3.5
            "impact": 4.0,          # Increased from 3.5
            "scope": 4.0,           # Increased from 3.5
            "quantifiable_results": 3.5  # Increased from 3.0
        }
    },
    "Meritorious Service Medal": {
        "description": "May be awarded to any member who distinguishes themselves by outstanding meritorious achievement or service to the United States.",
        "threshold": 75,
        "min_requirements": {
            "leadership": 3.5,      # Increased from 3.0
            "impact": 3.5,          # Increased from 3.0
            "scope": 3.5,           # Increased from 3.0
            "quantifiable_results": 3.0  # Increased from 2.5
        }
    },
    "Coast Guard Commendation Medal": {
        "description": "May be awarded to a person who distinguishes themselves by heroic or meritorious achievement or service.",
        "threshold": 65,
        "min_requirements": {
            "leadership": 3.0,      # Increased from 2.5
            "impact": 3.0,          # Increased from 2.5
            "scope": 3.0,           # Increased from 2.5
            "quantifiable_results": 2.5  # Increased from 2.0
        }
    },
    "Coast Guard Achievement Medal": {
        "description": "May be awarded for professional and/or leadership achievement based on sustained performance or specific achievement of a superlative nature.",
        "threshold": 50,
        "min_requirements": {
            "impact": 2.5,          # Increased from 2.0
            "scope": 2.5,           # Increased from 2.0
            "quantifiable_results": 2.0  # Increased from 1.5
        }
    },
    "Coast Guard Letter of Commendation": {
        "description": "May be awarded for an act or service resulting in unusual and/or outstanding achievement but lesser than that required for the Achievement Medal.",
        "threshold": 45,
        "min_requirements": {
            "impact": 1.0,
            "scope": 1.0
        }
    }
}