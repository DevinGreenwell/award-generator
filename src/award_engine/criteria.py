"""
Award criteria definitions for Coast Guard awards.
"""

# Weight definitions for different scoring criteria
SCORING_WEIGHTS = {
    "impact": 5,
    "scope": 5,
    "leadership": 5,
    "above_beyond": 4,
    "innovation": 4,
    "quantifiable_results": 4,
    "challenges": 3,
    "valor": 5,
    "collaboration": 4,
    "training_provided": 3,
    "emergency_response": 3
}

# Award thresholds (percentages)
AWARD_THRESHOLDS = {
    "Medal of Honor": 92,
    "Distinguished Service Medal": 84,
    "Legion of Merit": 76,
    "Meritorious Service Medal": 70,
    "Coast Guard Commendation Medal": 60,
    "Coast Guard Achievement Medal": 50,
    "Coast Guard Letter of Commendation": 40
}

# Detailed award criteria
AWARD_CRITERIA = {
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