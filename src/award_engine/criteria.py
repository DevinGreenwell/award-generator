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

# Award thresholds (percentages) - Even more stringent thresholds
AWARD_THRESHOLDS = {
    "Medal of Honor": 99,              # +1 (almost impossible)
    "Distinguished Service Medal": 94, # +2 (extremely rare, O-6+ only)
    "Legion of Merit": 88,            # +3 (very rare, senior officers/enlisted)
    "Meritorious Service Medal": 78,  # +3 (exceptional achievement required)
    "Coast Guard Commendation Medal": 68, # +3 (significant above-and-beyond)
    "Coast Guard Achievement Medal": 53,   # +3 (strong performance above expectations)
    "Coast Guard Letter of Commendation": 38  # +3 (solid performance)
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
            "leadership": 4.75,     # Further increased by 0.25
            "impact": 4.75,         # Further increased by 0.25
            "scope": 4.75,          # Further increased by 0.25
            "quantifiable_results": 4.25  # Further increased by 0.25
        }
    },
    "Legion of Merit": {
        "description": "Awarded to officers who have performed exceptionally meritorious service, except as to the degree of responsibility of the DSM.",
        "threshold": 85,
        "min_requirements": {
            "leadership": 4.25,     # Further increased by 0.25
            "impact": 4.25,         # Further increased by 0.25
            "scope": 4.25,          # Further increased by 0.25
            "quantifiable_results": 3.75  # Further increased by 0.25
        }
    },
    "Meritorious Service Medal": {
        "description": "May be awarded to any member who distinguishes themselves by outstanding meritorious achievement or service to the United States.",
        "threshold": 75,
        "min_requirements": {
            "leadership": 3.75,     # Further increased by 0.25
            "impact": 3.75,         # Further increased by 0.25
            "scope": 3.75,          # Further increased by 0.25
            "quantifiable_results": 3.25  # Further increased by 0.25
        }
    },
    "Coast Guard Commendation Medal": {
        "description": "May be awarded to a person who distinguishes themselves by heroic or meritorious achievement or service.",
        "threshold": 65,
        "min_requirements": {
            "leadership": 3.25,     # Further increased by 0.25
            "impact": 3.25,         # Further increased by 0.25
            "scope": 3.25,          # Further increased by 0.25
            "quantifiable_results": 2.75  # Further increased by 0.25
        }
    },
    "Coast Guard Achievement Medal": {
        "description": "May be awarded for professional and/or leadership achievement based on sustained performance or specific achievement of a superlative nature.",
        "threshold": 50,
        "min_requirements": {
            "impact": 2.75,         # Further increased by 0.25
            "scope": 2.75,          # Further increased by 0.25
            "quantifiable_results": 2.25  # Further increased by 0.25
        }
    },
    "Coast Guard Letter of Commendation": {
        "description": "May be awarded for an act or service resulting in unusual and/or outstanding achievement but lesser than that required for the Achievement Medal.",
        "threshold": 45,
        "min_requirements": {
            "impact": 1.25,         # Further increased by 0.25
            "scope": 1.25           # Further increased by 0.25
        }
    }
}