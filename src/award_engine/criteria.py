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

# Award thresholds (percentages) - Balanced for realistic expectations
AWARD_THRESHOLDS = {
    "Medal of Honor": 98,              # Almost impossible - valor required
    "Distinguished Service Medal": 90, # Extremely rare, O-6+ only typically
    "Legion of Merit": 82,            # Very rare, senior officers/enlisted
    "Meritorious Service Medal": 72,  # Exceptional sustained achievement
    "Coast Guard Commendation Medal": 62, # Significant above-and-beyond
    "Coast Guard Achievement Medal": 48,   # Strong performance above expectations
    "Coast Guard Letter of Commendation": 35  # Solid performance
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
            "leadership": 4.0,     # High leadership required
            "impact": 4.0,         # Significant organizational impact
            "scope": 4.0,          # Wide organizational reach
            "quantifiable_results": 3.5  # Strong measurable outcomes
        }
    },
    "Legion of Merit": {
        "description": "Awarded to officers who have performed exceptionally meritorious service, except as to the degree of responsibility of the DSM.",
        "threshold": 82,
        "min_requirements": {
            "leadership": 3.5,     # Strong leadership
            "impact": 3.5,         # Clear organizational impact
            "scope": 3.5,          # Broad scope of influence
            "quantifiable_results": 3.0  # Measurable results
        }
    },
    "Meritorious Service Medal": {
        "description": "May be awarded to any member who distinguishes themselves by outstanding meritorious achievement or service to the United States.",
        "threshold": 72,
        "min_requirements": {
            "leadership": 3.0,     # Good leadership demonstration
            "impact": 3.0,         # Meaningful impact
            "scope": 3.0,          # Unit or sector level
            "quantifiable_results": 2.5  # Some measurable results
        }
    },
    "Coast Guard Commendation Medal": {
        "description": "May be awarded to a person who distinguishes themselves by heroic or meritorious achievement or service.",
        "threshold": 62,
        "min_requirements": {
            "leadership": 2.5,     # Moderate leadership
            "impact": 2.5,         # Clear positive impact
            "scope": 2.5,          # Department or unit level
            "quantifiable_results": 2.0  # Some quantifiable elements
        }
    },
    "Coast Guard Achievement Medal": {
        "description": "May be awarded for professional and/or leadership achievement based on sustained performance or specific achievement of a superlative nature.",
        "threshold": 48,
        "min_requirements": {
            "impact": 2.0,         # Positive impact demonstrated
            "scope": 2.0,          # Team or department level
            "quantifiable_results": 1.5  # Basic measurable results
        }
    },
    "Coast Guard Letter of Commendation": {
        "description": "May be awarded for an act or service resulting in unusual and/or outstanding achievement but lesser than that required for the Achievement Medal.",
        "threshold": 35,
        "min_requirements": {
            "impact": 1.0,         # Any positive impact
            "scope": 1.0           # Individual or team level
        }
    }
}