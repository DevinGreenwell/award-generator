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

# Award thresholds (percentages) - Adjusted to be more realistic
AWARD_THRESHOLDS = {
    "Medal of Honor": 95,
    "Distinguished Service Medal": 85,
    "Legion of Merit": 75,
    "Meritorious Service Medal": 65,
    "Coast Guard Commendation Medal": 55,
    "Coast Guard Achievement Medal": 45,
    "Coast Guard Letter of Commendation": 30
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
        "threshold": 90,
        "min_requirements": {
            "leadership": 4.0,
            "impact": 4.0,
            "scope": 4.0,
            "quantifiable_results": 3.5
        }
    },
    "Legion of Merit": {
        "description": "Awarded to officers who have performed exceptionally meritorious service, except as to the degree of responsibility of the DSM.",
        "threshold": 82,
        "min_requirements": {
            "leadership": 3.5,
            "impact": 3.5,
            "scope": 3.5,
            "quantifiable_results": 3.0
        }
    },
    "Meritorious Service Medal": {
        "description": "May be awarded to any member who distinguishes themselves by outstanding meritorious achievement or service to the United States.",
        "threshold": 74,
        "min_requirements": {
            "leadership": 3.0,
            "impact": 3.0,
            "scope": 3.0,
            "quantifiable_results": 2.5
        }
    },
    "Coast Guard Commendation Medal": {
        "description": "May be awarded to a person who distinguishes themselves by heroic or meritorious achievement or service.",
        "threshold": 65,
        "min_requirements": {
            "leadership": 2.5,
            "impact": 2.5,
            "scope": 2.5,
            "quantifiable_results": 2.0
        }
    },
    "Coast Guard Achievement Medal": {
        "description": "May be awarded for professional and/or leadership achievement based on sustained performance or specific achievement of a superlative nature.",
        "threshold": 56,
        "min_requirements": {
            "impact": 2.0,
            "scope": 2.0,
            "quantifiable_results": 1.5
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